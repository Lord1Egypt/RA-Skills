// opencode 的本地会话。
//
//   ~/.local/share/opencode/opencode.db
//   $XDG_DATA_HOME/opencode/opencode.db（设了 XDG_DATA_HOME 时）
//   $OPENCODE_DB 可覆盖文件名
//
// 两代 schema 并存，要自动判：
//   2.0  session_v2(id, title, directory, time_created, time_updated)
//        session_message(session_id, type, seq, data)
//        user 行的 text 在 data.text 顶层；assistant 行的 parts 在 data.content[]
//   1.x  session / message / part（与 zcode 同构，正文在 part.data.type === "text"）
//
// 升级过的库两套表都在，优先 2.0；某个会话还没迁移到 session_v2 时，回落到 1.x 的表。
// 路径与 schema 来自 deja-vu 的 registry/opencode.md。
import os from 'node:os';
import path from 'node:path';
import { existsSync } from 'node:fs';

export const source = 'opencode';

export function dbPath() {
  const base =
    process.env.OPENCODE_DB ||
    path.join(process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local', 'share'), 'opencode', 'opencode.db');
  return existsSync(base) ? base : '';
}

async function open() {
  const p = dbPath();
  if (!p) throw new Error('没找到 opencode.db');
  const { DatabaseSync } = await import('node:sqlite');
  const db = new DatabaseSync(p, { readOnly: true });
  const tables = new Set(
    db.prepare("select name from sqlite_master where type='table'").all().map((r) => r.name)
  );
  return { db, file: p, tables };
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
  const { db, file, tables } = await open();
  try {
    const v2 = tables.has('session_v2');
    const sql = v2
      ? 'select id, title, directory, time_created, time_updated from session_v2 order by time_updated desc'
      : 'select id, title, directory, time_created, time_updated from session order by time_updated desc';
    let rows = [];
    try {
      rows = db.prepare(sql).all();
    } catch {
      rows = [];
    }

    const out = [];
    for (const r of rows) {
      let n = 0;
      try {
        const q = v2
          ? db.prepare('select count(*) c from session_message where session_id = ?')
          : db.prepare('select count(*) c from message where session_id = ?');
        n = q.get(r.id).c;
      } catch {
        n = 0;
      }
      if (!n) continue;
      out.push({
        source,
        id: r.id,
        time: Number(r.time_updated || r.time_created || 0),
        title: tidy(r.title) || String(r.id).slice(0, 14),
        count: n,
        ref: { kind: 'opencode', id: r.id, file, v2 },
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
  const { db, file, tables } = await open();
  try {
    const messages = [];
    let meta = null;

    if (tables.has('session_v2')) {
      meta = db.prepare('select * from session_v2 where id = ?').get(id) || null;
    }
    if (!meta && tables.has('session')) {
      meta = db.prepare('select * from session where id = ?').get(id) || null;
    }
    if (!meta) throw new Error('这个会话不存在：' + id);

    // 优先 2.0 的 session_message
    let used = false;
    if (tables.has('session_message')) {
      const rows = db
        .prepare('select type, data, time_created from session_message where session_id = ? order by seq, time_created')
        .all(id);
      for (const r of rows) {
        let d;
        try {
          d = JSON.parse(r.data || '{}');
        } catch {
          continue;
        }
        const role = r.type || d.role;
        if (role !== 'user' && role !== 'assistant') continue;

        let body = '';
        if (role === 'user') {
          body = String(d.text || '').trim();
        } else {
          const parts = Array.isArray(d.content) ? d.content : [];
          body = parts
            .filter((p) => p && p.type === 'text' && p.text)
            .map((p) => p.text)
            .join('\n\n')
            .trim();
        }
        if (!body) continue;
        used = true;
        messages.push({
          role: role === 'user' ? '用户' : 'opencode',
          time: r.time_created ? new Date(Number(r.time_created)).toTimeString().slice(0, 5) : '',
          body,
        });
      }
    }

    // 回落 1.x 的 message / part
    if (!used && tables.has('message') && tables.has('part')) {
      const msgs = db
        .prepare('select id, data, time_created from message where session_id = ? order by time_created')
        .all(id);
      for (const m of msgs) {
        let md;
        try {
          md = JSON.parse(m.data || '{}');
        } catch {
          continue;
        }
        if (md.role !== 'user' && md.role !== 'assistant') continue;
        const parts = db.prepare('select data from part where message_id = ? order by time_created').all(m.id);
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
          role: md.role === 'user' ? '用户' : 'opencode',
          time: m.time_created ? new Date(Number(m.time_created)).toTimeString().slice(0, 5) : '',
          body,
        });
      }
    }

    return {
      title: tidy(meta.title) || tidy(messages.find((m) => m.role === '用户')?.body) || String(id).slice(0, 14),
      messages,
      source: file + '#' + id,
      note: [meta.directory && '目录 ' + meta.directory].filter(Boolean).join('｜'),
      meta: { sessionId: id, cwd: meta.directory },
    };
  } finally {
    db.close();
  }
}
