// Qwen Code 的本地会话。
//
//   ~/.qwen/projects/<encoded-project>/chats/*.jsonl
//
// 目录编码和 Claude Code 一样（路径里的斜杠与冒号换成横线）。每一行一个 JSON：
//   {type, sessionId, timestamp, message:{role, parts:[{text, thought?}]}}
//
// role 为 model 映射成助手、user 映射成用户；role 缺失时用顶层 type。
// parts 里带 thought: true 的是思考过程，排除。tool 调用也在 parts 里（functionCall /
// functionResponse），默认不取。
//
// 与 Gemini CLI 不通用：那边正文在 content，这边在 message.parts，且多了 thought 标记。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const source = 'qwen';

export async function parse(file) {
  const raw = await readFile(file, 'utf8');
  const messages = [];
  let sessionId = '';

  for (const line of raw.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    let j;
    try {
      j = JSON.parse(s);
    } catch {
      continue;
    }
    sessionId = sessionId || j.sessionId || '';

    const msg = j.message || {};
    const roleRaw = String(msg.role || j.type || '').toLowerCase();
    const role =
      roleRaw === 'user' ? '用户' : roleRaw === 'model' || roleRaw === 'assistant' ? 'Qwen' : '';
    if (!role) continue;

    const parts = Array.isArray(msg.parts) ? msg.parts : Array.isArray(msg.content) ? msg.content : [];
    const texts = parts
      .filter((p) => p && !p.thought && typeof p.text === 'string' && p.text.trim())
      .map((p) => p.text);
    const body = texts.join('\n\n').trim();
    if (!body) continue;

    const ts = j.timestamp || '';
    messages.push({
      role,
      time: typeof ts === 'number' ? new Date(ts).toTimeString().slice(0, 5) : String(ts).slice(11, 16),
      body,
    });
  }

  return {
    title: titleOf(messages) || path.basename(file, '.jsonl'),
    messages,
    source: file,
    note: sessionId ? 'session ' + sessionId : '',
    meta: { sessionId },
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
