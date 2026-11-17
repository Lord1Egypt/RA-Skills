// Cline 的本地会话。
//
// 新版 CLI/SDK：
//   ~/.cline/data/sessions/<sessionId>/<sessionId>.messages.json   正文
//   ~/.cline/data/sessions/<sessionId>/<sessionId>.json            清单（标题、cwd、时间）
//
// 旧版 VS Code 扩展（saoudrizwan.claude-dev）：
//   <globalStorage>/tasks/<taskId>/api_conversation_history.json
//
// 两代都是整文件 JSON、每次改动整体重写。本机只装了新版目录结构但没跑过对话，
// 所以这里按结构自适应解析：找出消息数组，逐项认角色与正文，认不出就跳过。
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { existsSync } from 'node:fs';

export const source = 'cline';

const USER_WORDS = /^(user|human)$/i;
const AI_WORDS = /^(assistant|ai|agent|cline|bot|model)$/i;

function roleOf(o) {
  for (const k of ['role', 'type', 'author', 'sender']) {
    const v = o && o[k];
    if (typeof v === 'string') {
      if (USER_WORDS.test(v)) return 'user';
      if (AI_WORDS.test(v)) return 'ai';
    }
  }
  return '';
}

function textOf(o) {
  if (!o || typeof o !== 'object') return '';
  for (const k of ['text', 'content', 'message']) {
    const v = o[k];
    if (typeof v === 'string' && v.trim()) return v;
    if (Array.isArray(v)) {
      const parts = v
        .map((p) => (typeof p === 'string' ? p : p && (p.text || (p.type === 'text' ? p.content : '')) || ''))
        .filter(Boolean);
      const joined = parts.join('\n\n').trim();
      if (joined) return joined;
    }
  }
  return '';
}

// 从任意 JSON 里找消息数组：优先 messages / conversation，其次第一个元素像消息的数组
function findMessageArray(doc) {
  if (Array.isArray(doc)) return doc;
  if (!doc || typeof doc !== 'object') return [];
  for (const k of ['messages', 'conversation', 'history', 'apiConversationHistory']) {
    if (Array.isArray(doc[k])) return doc[k];
  }
  for (const v of Object.values(doc)) {
    if (Array.isArray(v) && v.length && v[0] && typeof v[0] === 'object' && roleOf(v[0])) return v;
  }
  return [];
}

export async function parse(payload) {
  // payload 是 { messagesFile, metaFile }，也允许直接传 messages.json 路径
  const messagesFile = typeof payload === 'string' ? payload : payload.messagesFile;
  const metaFile = typeof payload === 'string' ? '' : payload.metaFile || '';

  const doc = JSON.parse(await readFile(messagesFile, 'utf8'));
  const list = findMessageArray(doc);
  const messages = [];
  for (const m of list) {
    const role = roleOf(m);
    if (!role) continue;
    const body = textOf(m).trim();
    if (!body) continue;
    messages.push({
      role: role === 'user' ? '用户' : 'Cline',
      time: m.ts ? new Date(Number(m.ts)).toTimeString().slice(0, 5) : '',
      body,
    });
  }

  let title = '';
  let cwd = '';
  if (metaFile && existsSync(metaFile)) {
    try {
      const meta = JSON.parse(await readFile(metaFile, 'utf8'));
      title = meta.title || meta.name || '';
      cwd = meta.cwd || meta.workspace || '';
    } catch {
      /* 清单坏了不影响正文 */
    }
  }

  const id = path.basename(path.dirname(messagesFile));
  return {
    title: title || titleOf(messages) || id.slice(0, 12),
    messages,
    source: messagesFile,
    note: cwd ? '目录 ' + cwd : '',
    meta: { sessionId: id, cwd },
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
