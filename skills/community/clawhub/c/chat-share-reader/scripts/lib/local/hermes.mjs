// Hermes 的本地会话。
//
//   ~/.hermes/state.db                     0.17+
//   ~/.hermes/profiles/<profile>/state.db  旧版，每个 profile 一个库
//
// SQLite 关系型存储。列名随版本变，所以不写死：读 messages 表的列，按名字猜出
// 角色列与正文列，认不出就报出实际列名，方便补映射。
import os from 'node:os';
import path from 'node:path';
import { existsSync, readdirSync } from 'node:fs';

export const source = 'hermes';

export function dbPaths() {
  const home = process.env.HERMES_HOME || path.join(os.homedir(), '.hermes');
  const out = [];
  const main = path.join(home, 'state.db');
  if (existsSync(main)) out.push(main);
  const profiles = path.join(home, 'profiles');
  if (existsSync(profiles)) {
    // 每个 profile 一个 state.db
    try {
      for (const d of readdirSync(profiles)) {
        const p = path.join(profiles, d, 'state.db');
        if (existsSync(p)) out.push(p);
      }
    } catch {
      /* 读不到就算了 */
    }
  }
  return out;
}

export function dbPath() {
  const all = dbPaths();
  return all[0] || '';
}

async function open(file) {
  const p = file || dbPath();
  if (!p) throw new Error('没找到 Hermes 的 state.db');
  const { DatabaseSync } = await import('node:sqlite');
  return { db: new DatabaseSync(p, { readOnly: true }), file: p };
}

function pickCol(cols, cands) {
  for (const c of cands) {
    const hit = cols.find((x) => x.toLowerCase() === c.toLowerCase());
    if (hit) return hit;
  }
  for (const c of cands) {
    const hit = cols.find((x) => x.toLowerCase().includes(c.toLowerCase()));
    if (hit) return hit;
  }
  return '';
}

export async function list({ limit = 50 } = {}) {
  const out = [];
  for (const dbFile of dbPaths()) {
    const { db } = await open(dbFile);
    try {
      const tables = db
        .prepare("select name from sqlite_master where type='table'")
        .all()
        .map((r) => r.name);
      const tMsg = tables.find((t) => /^messages?$/i.test(t)) || tables.find((t) => /message/i.test(t));
      if (!tMsg) continue;

      const cols = db.prepare(`pragma table_info("${tMsg}")`).all().map((c) => c.name);
      const cSession = pickCol(cols, ['session_id', 'sessionId', 'thread_id', 'conversation_id']);
      const cTime = pickCol(cols, ['timestamp', 'created_at', 'time']);

      if (!cSession) continue;
      const sql = `select ${cSession} as sid, count(*) as n${cTime ? ', max(' + cTime + ') as t' : ''} from "${tMsg}" group by ${cSession} order by ${cTime ? 't' : 'n'} desc limit ${Number(limit) || 50}`;
      for (const r of db.prepare(sql).all()) {
        out.push({
          source,
          id: String(r.sid),
          time: r.t ? Number(new Date(r.t)) || Number(r.t) : 0,
          title: String(r.sid).slice(0, 14),
          count: r.n,
          ref: { kind: 'hermes', id: String(r.sid), file: dbFile },
        });
      }
    } catch {
      /* 单个库读不动就跳过 */
    } finally {
      db.close();
    }
  }
  return out;
}

export async function parse(ref) {
  const id = typeof ref === 'string' ? ref : ref.id;
  const file = typeof ref === 'string' ? '' : ref.file;
  const { db, file: dbFile } = await open(file);
  try {
    const tables = db
      .prepare("select name from sqlite_master where type='table'")
      .all()
      .map((r) => r.name);
    const tMsg = tables.find((t) => /^messages?$/i.test(t)) || tables.find((t) => /message/i.test(t));
    if (!tMsg) throw new Error('state.db 里没有 messages 表');

    const cols = db.prepare(`pragma table_info("${tMsg}")`).all().map((c) => c.name);
    const cSession = pickCol(cols, ['session_id', 'sessionId', 'thread_id', 'conversation_id']);
    const cRole = pickCol(cols, ['role', 'sender', 'author', 'type']);
    const cText = pickCol(cols, ['content', 'text', 'body', 'message']);
    const cTime = pickCol(cols, ['timestamp', 'created_at', 'time']);

    if (!cSession || !cRole || !cText) {
      throw new Error(`columns not mapped on ${tMsg}: ${cols.join(', ')}`);
    }

    const rows = db
      .prepare(
        `select "${cRole}" as role, "${cText}" as body${cTime ? ', "' + cTime + '" as t' : ''} from "${tMsg}" where "${cSession}" = ?${cTime ? ' order by "' + cTime + '"' : ''}`
      )
      .all(id);

    const messages = [];
    for (const r of rows) {
      const role = String(r.role || '').toLowerCase();
      if (role !== 'user' && role !== 'assistant') continue;
      const body = String(r.body || '').trim();
      if (!body) continue;
      messages.push({
        role: role === 'user' ? '用户' : 'Hermes',
        time: r.t ? new Date(Number(new Date(r.t)) || Number(r.t)).toTimeString().slice(0, 5) : '',
        body,
      });
    }

    return {
      title: titleOf(messages) || String(id).slice(0, 12),
      messages,
      source: dbFile + '#' + id,
      note: '',
      meta: { sessionId: id },
    };
  } finally {
    db.close();
  }
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
