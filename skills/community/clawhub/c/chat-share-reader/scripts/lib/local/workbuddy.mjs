// WorkBuddy 本地会话解析（~/.workbuddy/projects/<工作区 slug>/<sessionId>.jsonl）。
//
// 一行一个事件：session-meta 是元信息，message 才是对话。消息结构接近 Anthropic
// 口径，content 是数组，取其中的 text 字段。
//
// 坑在注入：每条用户消息前面都挂着 <system-reminder> 包住的 user_info、identity
// 文件和自定义指令，整段粘贴进去会有几千字噪音，标题也会变成 "<system-reminder"。
// 这里整块剥掉，只留 <user_query> 里的真实提问。
//
// 同一工作区下的 `<sessionId>/tool-results/` 是工具输出，不是会话文件，由
// sessions.mjs 的 filter 排除。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const source = 'workbuddy';

const REMINDER = /<system-reminder[\s\S]*?<\/system-reminder>/g;
const IDENTITY = /<identity_context>[\s\S]*?<\/identity_context>/g;
const CUSTOM = /<user_custom_instructions>[\s\S]*?<\/user_custom_instructions>/g;

function clean(text) {
  return String(text || '')
    .replace(REMINDER, '')
    .replace(IDENTITY, '')
    .replace(CUSTOM, '')
    .replace(/<\/?user_query>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function clock(ts) {
  const ms = Number(ts);
  if (!Number.isFinite(ms) || ms <= 0) return '';
  const d = new Date(ms > 1e12 ? ms : ms * 1000);
  const p = (n) => String(n).padStart(2, '0');
  return `${p(d.getHours())}:${p(d.getMinutes())}`;
}

// WorkBuddy 的时间戳是毫秒数，导出时统一成 ISO，跨分片合并才排得对
function msToIso(ts) {
  const ms = Number(ts);
  if (!Number.isFinite(ms) || ms <= 0) return '';
  return new Date(ms > 1e12 ? ms : ms * 1000).toISOString();
}

export async function parse(file) {
  const raw = await readFile(file, 'utf8');
  const messages = [];
  let sessionId = '';
  let workspace = '';

  for (const line of raw.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    let ev;
    try {
      ev = JSON.parse(s);
    } catch {
      /* 半行或损坏行跳过 */
      continue;
    }
    if (ev.type === 'session-meta') {
      sessionId = sessionId || ev.sessionId || '';
      continue;
    }
    if (ev.type !== 'message') continue;
    if (ev.role !== 'user' && ev.role !== 'assistant') continue;

    const content = ev.content;
    const parts = [];
    if (typeof content === 'string') parts.push(content);
    else if (Array.isArray(content)) {
      for (const c of content) {
        if (c && typeof c.text === 'string') parts.push(c.text);
      }
    }
    const body = clean(parts.join('\n'));
    if (!body) continue;

    messages.push({
      role: ev.role === 'user' ? '用户' : 'WorkBuddy',
      time: clock(ev.timestamp),
      at: msToIso(ev.timestamp),
      body,
    });
  }

  workspace = path.basename(path.dirname(file));

  return {
    title: titleOf(messages) || path.basename(file, '.jsonl'),
    messages,
    source: file,
    note: workspace && '工作区 ' + workspace,
    meta: { sessionId, cwd: workspace },
  };
}

function titleOf(messages) {
  const first = messages.find((m) => m.role === '用户');
  if (!first) return '';
  return first.body
    .replace(/[#*`>\n]/g, ' ')
    .replace(/[，。、？！；："'（）《》…—\s]+/g, ' ')
    .trim()
    .slice(0, 24)
    .trim();
}
