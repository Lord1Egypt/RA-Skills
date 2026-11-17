// zcode 的本地会话。
//
//   ~/.zcode/cli/db/db.sqlite
//
// 三张表：session / message / part。message.data 与 part.data 都是 JSON 字符串。
// message.data.role 为 user / assistant；part.data.type 有 text / reasoning / step-start /
// tool / timeline，正文只取 text。
//
// 这个 schema 和 opencode 同源，接 opencode 时可以照这个改路径。
import os from 'node:os';
import path from 'node:path';
import { existsSync } from 'node:fs';

export const source = 'zcode';

export function dbPath() {
  const p = path.join(os.homedir(), '.zcode', 'cli', 'db', 'db.sqlite');
  return existsSync(p) ? p : '';
}

async function open() {
  const p = dbPath();
  if (!p) throw new Error('没找到 zcode 的 db.sqlite');
  const { DatabaseSync } = await import('node:sqlite');
  return { db: new DatabaseSync(p, { readOnly: true }), file: p };
}

function tidy(t) {
  return String(t || '')
    .replace(/[#*`>\n]/g, ' ')
    .replace(/[，。、？！；："'（）《》…—\s]+/g, ' ')
    .trim()
    .slice(0, 40)
    .trim();
}

export async function list({ limit = 50 } = {}) {
  const { db, file } = await open();
  try {
    const rows = db
      .prepare('select id, title, directory, time_created, time_updated from session order by time_updated desc')
      .all();
    const out = [];
    for (const r of rows) {
      const n = db.prepare('select count(*) c from message where session_id = ?').get(r.id);
      if (!n.c) continue;
      out.push({
        source,
        id: r.id,
        time: Number(r.time_updated || r.time_created || 0),
        title: tidy(r.title) || r.id.slice(0, 12),
        count: n.c,
        ref: { kind: 'zcode', id: r.id, file },
      });
      if (out.length >= limit) break;
    }
    return out;
  } finally {
    db.close();
  }
}

export async function parse(ref) {
  const id = typeof ref === 'string' ? ref : ref.id;
  const { db, file } = await open();
  try {
    const s = db.prepare('select * from session where id = ?').get(id);
    if (!s) throw new Error('这个会话不存在：' + id);

    const msgs = db
      .prepare('select id, data, time_created from message where session_id = ? order by sequence, time_created')
      .all(id);

    const messages = [];
    for (const m of msgs) {
      let meta;
      try {
        meta = JSON.parse(m.data || '{}');
      } catch {
        meta = {};
      }
      if (meta.role !== 'user' && meta.role !== 'assistant') continue;

      const parts = db
        .prepare('select data from part where message_id = ? order by sequence, time_created')
        .all(m.id);
      const texts = [];
      for (const p of parts) {
        let pd;
        try {
          pd = JSON.parse(p.data || '{}');
        } catch {
          continue;
        }
        if (pd.type === 'text' && pd.text) texts.push(pd.text);
      }
      const body = texts.join('\n\n').trim();
      if (!body) continue;

      messages.push({
        role: meta.role === 'user' ? '用户' : 'zcode',
        time: m.time_created ? new Date(Number(m.time_created)).toTimeString().slice(0, 5) : '',
        body,
      });
    }

    return {
      title: tidy(s.title) || tidy(messages.find((m) => m.role === '用户')?.body) || id.slice(0, 12),
      messages,
      source: file + '#' + id,
      note: [s.directory && '目录 ' + s.directory].filter(Boolean).join('｜'),
      meta: { sessionId: id, cwd: s.directory },
    };
  } finally {
    db.close();
  }
}
