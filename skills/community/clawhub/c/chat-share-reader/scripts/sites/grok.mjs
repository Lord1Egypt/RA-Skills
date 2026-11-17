// Grok 分享页（grok.com/share/<id>）：必须走浏览器。
// 与 Gemini 同形态：Next.js + RSC，SSR 数据里只有 shareLinkId，正文由客户端二次请求。
// 2026-11-13 复验：分享页 HTML 已经能 curl 到 200（194 KB，不再挑战），但 RSC payload
// 里只有 UI 配置和标题，一条消息都没有，所以 DOM 兜底仍然必须走浏览器。同一天
// `uvx convolvger` 读同一条分享成功（8 条消息），vendor 是首选，细节见 references/sites.md。
//
// 选择器已实测（2026-11-07，一条 2 轮分享）：user-message / assistant-message 按 DOM 顺序交错，
// 一条组合选择器取回即是时间序。下面的候选列表是换版时的退路。
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pickJson } from '../lib/md.mjs';

export const name = 'grok.com';
export const channel = 'browser';
export const useVendor = true;
export const match = (url) => /(^|\/\/|\.)grok\.com\/share\//.test(url);

const HERE = path.dirname(fileURLToPath(import.meta.url));

// 实测选择器（2026-11-07，一条 2 轮分享验证）：
// [data-testid="user-message"] 与 [data-testid="assistant-message"] 在 DOM 里天然按对话顺序交错，
// 组合选择器一次取回即是时间序。容器是 [data-testid="share-transcript-scroller"]。
// 后面的候选是换版时的退路，命中数 >= 2 才算数。
const PRIMARY = [
  '[data-testid="user-message"],[data-testid="assistant-message"]',
  '[data-testid^="user-message"],[data-testid^="assistant-message"]',
  '.message-bubble',
  'div[class*="response-content"]',
];

export async function read(url, { session, keepOpen = false } = {}) {
  if (!session) throw new Error('这个站点需要浏览器后端，但调用方没有传入 session');
  await session.open(url);
  try {
    await session.waitReady({
      // 不能用「正文长度」判断就绪：导航栏本身就有 400+ 字，会在内容还没渲染时提前通过。
      // 真正的就绪信号是消息容器出现。
      probe:
        `JSON.stringify({ok: document.querySelectorAll('${PRIMARY[0]}').length > 0, ` +
        `n: document.querySelectorAll('${PRIMARY[0]}').length, url: location.href})`,
      tries: 24,
      delay: 3000,
    });

    const domToMd = await readFile(path.join(HERE, '..', 'lib', 'dom-to-md.js'), 'utf8');
    const extract = `
      (function(){
        var cands = ${JSON.stringify(PRIMARY)};
        var nodes = [];
        for (var i = 0; i < cands.length; i++) {
          var found = document.querySelectorAll(cands[i]);
          if (found.length >= 2) { nodes = Array.prototype.slice.call(found); break; }
        }
        if (!nodes.length) {
          return JSON.stringify({ error: "no message container matched", probes: cands,
            testids: Array.prototype.slice.call(document.querySelectorAll("[data-testid]"))
              .slice(0, 25).map(function(e){ return e.getAttribute("data-testid"); }) });
        }
        var out = nodes.map(function(n){
          var tid = n.getAttribute("data-testid") || "";
          // 有 data-testid 就以它为准，class 里的 "user" 字样容易误判（外层容器也带）
          var isUser = tid ? /^user/i.test(tid) : /user/i.test(n.className.toString());
          return { role: isUser ? "user" : "ai", body: window.__csrMd(n) };
        });
        return JSON.stringify({ title: document.title, url: location.href, turns: out });
      })()
    `;

    const raw = await session.eval(domToMd + '\n' + extract);
    const data = pickJson(raw);

    if (data.error) {
      throw new Error(
        data.error + '；候选选择器：' + (data.probes || []).join('，') +
        '；页面上出现的 data-testid：' + (data.testids || []).join('，')
      );
    }

    const messages = [];
    for (const t of data.turns || []) {
      if (!t.body || !t.body.trim()) continue;
      messages.push({ role: t.role === 'user' ? '用户' : 'Grok', body: t.body });
    }

    const title = (data.title || '').replace(/\s*\|\s*Shared Grok Conversation\s*$/, '').trim() ||
      'Grok 分享';

    return {
      title,
      messages,
      source: `https://grok.com/rest/app-chat/share_links/${(url.split('/').filter(Boolean).pop() || '')}（本机被 CF 拦，改走渲染）`,
      note: '正文由渲染 DOM 重建。角色标签（sr-only 的「你」「Grok」）已排除',
    };
  } finally {
    if (!keepOpen) await session.close();
  }
}
