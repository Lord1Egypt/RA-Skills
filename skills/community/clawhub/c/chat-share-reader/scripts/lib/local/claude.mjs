// Claude Code 本地会话解析（~/.claude/projects/<项目>/<sessionId>.jsonl）。
//
// 文件是一行一个事件，混着多种 type：user / assistant 是对话，其余（attachment、
// queue-operation、api-request、cost-state、system、atis-latch…）是运行期记录，不进正文。
//
// 注意 isSidechain：子代理的消息也写进同一个文件，带 isSidechain: true。默认跳过，
// 否则主对话里会混进一堆子任务的往返。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const source = 'claude';

export async function parse(file, { full = false } = {}) {
  const raw = await readFile(file, 'utf8');
  const events = [];
  for (const line of raw.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    try {
      events.push(JSON.parse(s));
    } catch {
      /* 半行或损坏行跳过 */
    }
  }

  const messages = [];
  let cwd = '';
  let branch = '';
  let model = '';
  let sessionId = '';

  for (const ev of events) {
    if (ev.type !== 'user' && ev.type !== 'assistant') continue;
    if (ev.isSidechain) continue;

    const msg = ev.message || {};
    const role = msg.role || ev.type;
    const parts = [];

    const content = msg.content;
    if (typeof content === 'string') {
      parts.push(content);
    } else if (Array.isArray(content)) {
      for (const c of content) {
        if (!c || typeof c !== 'object') continue;
        if (c.type === 'text' && c.text) parts.push(c.text);
        else if (c.type === 'tool_use' && full) {
          const input = c.input && Object.keys(c.input).length ? JSON.stringify(c.input, null, 2) : '';
          parts.push('**工具调用** `' + (c.name || '') + '`\n\n```json\n' + input + '\n```');
        } else if (c.type === 'tool_result' && full) {
          const t =
            typeof c.content === 'string'
              ? c.content
              : Array.isArray(c.content)
                ? c.content.map((x) => (x && x.text) || '').join('\n')
                : '';
          if (t.trim()) parts.push('**工具结果**\n\n```\n' + t.slice(0, 4000) + '\n```');
        }
      }
    }

    const body = parts.join('\n\n').trim();
    if (!body) continue;
    messages.push({
      role: role === 'user' ? '用户' : 'Claude',
      time: ev.timestamp ? String(ev.timestamp).slice(11, 16) : '',
      at: ev.timestamp || '',
      body,
    });

    cwd = cwd || ev.cwd || '';
    branch = branch || ev.gitBranch || '';
    model = model || msg.model || '';
    sessionId = sessionId || ev.sessionId || '';
  }

  return {
    title: titleOf(messages) || path.basename(file, '.jsonl'),
    messages,
    source: file,
    note: [model && '模型 ' + model, cwd && '目录 ' + cwd, branch && '分支 ' + branch]
      .filter(Boolean)
      .join('｜'),
    meta: { sessionId, cwd, branch, model },
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
