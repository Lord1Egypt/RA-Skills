// pi 系 harness 的会话解析，同时覆盖 pi 与 omp（两者格式同源）。
//
// 位置：
//   pi  : ~/.pi/agent/sessions/<项目>/<时间>_<id>.jsonl
//   omp : ~/.omp/agent/sessions/<项目>/<时间>_<id>.jsonl
//
// 一行一个 JSON，type 有 session / title / model_change / thinking_level_change / message /
// custom。对话在 type === "message" 里，message.role 为 system / user / assistant。
// system 是系统提示，跳过；omp 另有 type === "title" 存会话标题，优先用它。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const source = 'pi';

export async function parse(file, { full = false } = {}) {
  const raw = await readFile(file, 'utf8');
  const events = [];
  for (const line of raw.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    try {
      events.push(JSON.parse(s));
    } catch {
      /* 忽略损坏行 */
    }
  }

  const messages = [];
  let cwd = '';
  let title = '';
  let model = '';
  let sessionId = '';

  for (const ev of events) {
    if (ev.type === 'session') {
      cwd = cwd || ev.cwd || '';
      sessionId = sessionId || ev.id || '';
      continue;
    }
    if (ev.type === 'title') {
      title = title || ev.title || ev.text || '';
      continue;
    }
    if (ev.type === 'model_change') {
      model = model || ev.model || '';
      continue;
    }
    if (ev.type !== 'message') continue;

    const msg = ev.message || {};
    const role = msg.role;
    if (role !== 'user' && role !== 'assistant') continue;

    const parts = [];
    const content = msg.content;
    if (typeof content === 'string') parts.push(content);
    else if (Array.isArray(content)) {
      for (const c of content) {
        if (!c || typeof c !== 'object') continue;
        if (c.type === 'text' && c.text) parts.push(c.text);
        else if (full && c.type === 'tool_use') {
          parts.push(
            '**工具调用** `' + (c.name || '') + '`\n\n```json\n' +
              JSON.stringify(c.input || {}, null, 2) + '\n```'
          );
        } else if (full && c.type === 'tool_result') {
          const t = typeof c.content === 'string' ? c.content : JSON.stringify(c.content || '');
          if (t.trim()) parts.push('**工具结果**\n\n```\n' + t.slice(0, 4000) + '\n```');
        }
      }
    }

    const body = parts.join('\n\n').trim();
    if (!body) continue;
    messages.push({
      role: role === 'user' ? '用户' : 'Agent',
      time: ev.timestamp ? String(ev.timestamp).slice(11, 16) : '',
      body,
    });
    model = model || msg.model || '';
  }

  return {
    title: title || titleOf(messages) || path.basename(file, '.jsonl'),
    messages,
    source: file,
    note: [model && '模型 ' + model, cwd && '目录 ' + cwd].filter(Boolean).join('｜'),
    meta: { sessionId, cwd, model },
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
