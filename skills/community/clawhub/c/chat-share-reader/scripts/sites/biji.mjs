// biji.com（得到大脑 / Get 笔记）分享页：纯 HTTP，免认证。
//
// 页面本身是 Vue SPA，桌面视口渲染出来是空白，只有移动端视口才出内容；
// 而且正文是懒加载的，DOM 抓取会漏段（实测漏掉整个「课堂金句」小节）。
// 所以这里不碰页面，直接打前端自用的分享接口：
//
//   GET /voicenotes/web/share/notes/<id>            笔记全文，c.note.content 是 markdown 原文
//   GET /voicenotes/web/share/notes/<id>/original   逐字稿，c.content 是 JSON 字符串，内含 sentence_list
//   GET /voicenotes/web/share/notes/<id>/sprouts    子笔记（枝叶），多数笔记为空，默认不取
//
// 三个接口都不需要 cookie、不需要 Referer、不校验 UA，桌面 UA 直接 200。
import { httpGetJson } from '../lib/http.mjs';
import { t } from '../lib/i18n.mjs';

const API = 'https://get-notes.luojilab.com/voicenotes/web/share/notes/';

export const name = 'biji.com';
export const channel = 'http';
export const match = (url) => /biji\.com\/note\/share_note\//.test(url);

function shareId(url) {
  const m = url.match(/share_note\/([A-Za-z0-9_-]+)/);
  if (!m) throw new Error(t('链接里没有 share_note id：', 'No share_note id in link: ') + url);
  return m[1];
}

// 站内回听深链 [00:54:00](https://getnotes.seek:3240) 只在 App 里能跳，
// 导出成 markdown 后留着是死链，还原成纯时间戳。
const SEEK = /\[(\d{2}:\d{2}:\d{2})\]\(https:\/\/getnotes\.seek:\d+\)/g;
export const stripSeek = (s) => s.replace(SEEK, '**$1**');

export function clock(ms) {
  const s = Math.floor((ms || 0) / 1000);
  return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
}

// 逐字稿按 90 秒切段，和界面上的段落感对齐；句子本身带标点，直接拼不用加分隔符
// 传完整信封 { h, c } 或只传 c 都能吃，登录态批量接口那侧返回的是后者
export function transcriptFrom(payload) {
  const holder = payload && payload.c ? payload.c : payload;
  const raw = holder && holder.content;
  if (!raw) return '';
  let list;
  try {
    list = (typeof raw === 'string' ? JSON.parse(raw) : raw).sentence_list;
  } catch {
    return '';
  }
  if (!Array.isArray(list) || !list.length) return '';

  const out = [];
  let buf = [];
  let segStart = null;
  for (const s of list) {
    const text = (s.text || '').trim();
    if (!text) continue;
    if (segStart === null) segStart = s.start_time || 0;
    buf.push(text);
    if ((s.start_time || 0) - segStart >= 90000) {
      out.push(`**[${clock(segStart)}]**\n\n${buf.join('')}`);
      buf = [];
      segStart = null;
    }
  }
  if (buf.length) out.push(`**[${clock(segStart)}]**\n\n${buf.join('')}`);
  return out.join('\n\n');
}

export async function read(url) {
  const id = shareId(url);
  const body = await httpGetJson(API + id);

  // h.c 为 0 才是成功；非 0 时 h.e 带原因（分享被取消、笔记已删除等）
  if (body && body.h && body.h.c) {
    throw new Error(t(`接口返回错误 ${body.h.c}：${body.h.e || '分享可能已失效'}`, `API error ${body.h.c}: ${body.h.e || 'share may have expired'}`));
  }
  const note = body && body.c && body.c.note;
  if (!note) throw new Error(t('接口没返回 note，可能不是公开分享或笔记已删除', 'No note in response. It may be private or deleted.'));

  const messages = [];
  const md = stripSeek(note.content || note.body_text || '');
  if (md.trim()) messages.push({ role: '课堂笔记', body: md });

  let transcript = '';
  try {
    transcript = transcriptFrom(await httpGetJson(API + id + '/original'));
  } catch {
    // 语音笔记才有逐字稿；纯手写或图片笔记这里 404，静默跳过
  }
  if (transcript) messages.push({ role: '逐字稿', body: transcript });

  if (!messages.length) throw new Error(t('笔记正文为空', 'Note body is empty'));

  return {
    title: note.title || '得到大脑笔记',
    messages,
    source: API + id,
    // 笔记正文本身是完整文档（h3/h4 分级），再降两级就只剩 h5/h6，所以免降级
    demote: false,
    note: '内容由「得到大脑」自动整理，AI 生成部分请核实',
  };
}
