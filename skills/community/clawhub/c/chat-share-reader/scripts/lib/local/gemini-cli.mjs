// Gemini CLI 的本地会话。
//
//   ~/.gemini/tmp/<project-id>/chats/*.json   整会话 JSON
//   ~/.gemini/tmp/<project-id>/chats/*.jsonl  可回放格式（新版）
//
// 两代格式并存，同一个会话可能两份都在，按 sessionId 去重、优先取 JSONL。
// JSON: {sessionId, projectHash, startTime, lastUpdated, messages:[{id,timestamp,type,content}]}
// JSONL: 首行 session 字段，后续每行一条 message 或控制记录。
//
// type 映射：user → 用户；gemini / model → 助手；其余（info、error 等）忽略。
// content 可能是字符串，也可能是一组 {text} 片段。
//
// 路径规则来自 deja-vu 的 registry/gemini.md（社区对上游输出的观测记录，不是官方规范）。
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const source = 'gemini-cli';

export async function parse(file) {
  const raw = await readFile(file, 'utf8');
  let session = null;
  let records = [];

  if (file.endsWith('.jsonl')) {
    for (const line of raw.split('\n')) {
      const s = line.trim();
      if (!s) continue;
      let j;
      try {
        j = JSON.parse(s);
      } catch {
        continue;
      }
      if (!session && (j.sessionId || j.startTime)) {
        session = j;
        continue;
      }
      if (j.id || j.type) records.push(j);
    }
  } else {
    let doc;
    try {
      doc = JSON.parse(raw);
    } catch {
      throw new Error('不是合法 JSON：' + path.basename(file));
    }
    session = doc;
    records = doc.messages || [];
  }

  const messages = [];
  for (const m of records) {
    const t = String(m.type || m.role || '').toLowerCase();
    const role = t === 'user' ? '用户' : t === 'gemini' || t === 'model' || t === 'assistant' ? 'Gemini' : '';
    if (!role) continue;

    const parts = [];
    const c = m.content;
    if (typeof c === 'string') parts.push(c);
    else if (Array.isArray(c)) {
      for (const p of c) if (p && p.text) parts.push(p.text);
    }
    const body = parts.join('\n\n').trim();
    if (!body) continue;

    const ts = m.timestamp || (session && session.startTime) || '';
    messages.push({
      role,
      time: ts ? String(ts).slice(11, 16) : '',
      body,
    });
  }

  return {
    title: titleOf(messages) || path.basename(file).replace(/\.jsonl?$/, ''),
    messages,
    source: file,
    note: [session && session.sessionId && 'session ' + session.sessionId].filter(Boolean).join('｜'),
    meta: { sessionId: session && session.sessionId },
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
