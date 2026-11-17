// Cursor 的本地对话（Composer / Chat）。
//
// 存在 SQLite 里，不是文件：
//   Windows : %APPDATA%/Cursor/User/globalStorage/state.vscdb
//   macOS   : ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
//   Linux   : ~/.config/Cursor/User/globalStorage/state.vscdb
//
// 表 cursorDiskKV 里 key 为 `composerData:<uuid>` 的行存一次会话，value 是 JSON，
// conversation 数组里 type 1 是用户、2 是助手，正文直接在 .text 字段。
// 不需要再去 `bubbleId:` 那批行取正文（实测那些行大多不存在，正文就在 composerData 里）。
//
// 用 Node 22 内置的 node:sqlite，只读打开，不加依赖。
import os from 'node:os';
import path from 'node:path';
import { existsSync } from 'node:fs';

export const source = 'cursor';

const PATHS = {
  win32: path.join(process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'), 'Cursor', 'User', 'globalStorage', 'state.vscdb'),
  darwin: path.join(os.homedir(), 'Library', 'Application Support', 'Cursor', 'User', 'globalStorage', 'state.vscdb'),
  linux: path.join(os.homedir(), '.config', 'Cursor', 'User', 'globalStorage', 'state.vscdb'),
};

export function dbPath() {
  const p = PATHS[process.platform] || PATHS.linux;
  return existsSync(p) ? p : '';
}

async function open() {
  const p = dbPath();
  if (!p) throw new Error('没找到 Cursor 的 state.vscdb');
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
      .prepare("select key, value from cursorDiskKV where key like 'composerData:%'")
      .all();
    const out = [];
    for (const r of rows) {
      let j;
      try {
        j = JSON.parse(r.value);
      } catch {
        continue;
      }
      const conv = (j.conversation || []).filter((c) => c && c.text && String(c.text).trim());
      if (!conv.length) continue;
      out.push({
        source,
        id: String(r.key).replace('composerData:', ''),
        time: Number(j.lastUpdatedAt || j.createdAt || 0),
        title: tidy(j.name || conv.find((c) => c.type === 1)?.text || ''),
        count: conv.length,
        ref: { kind: 'cursor', id: String(r.key).replace('composerData:', ''), file },
      });
    }
    return out.sort((a, b) => b.time - a.time).slice(0, limit);
  } finally {
    db.close();
  }
}

export async function parse(ref) {
  const id = typeof ref === 'string' ? ref : ref.id;
  const { db, file } = await open();
  try {
    const row = db.prepare('select value from cursorDiskKV where key = ?').get('composerData:' + id);
    if (!row) throw new Error('这个 composer 不存在：' + id);
    const j = JSON.parse(row.value);
    const conv = j.conversation || [];
    const messages = [];
    for (const c of conv) {
      const text = String(c.text || '').trim();
      if (!text) continue;
      messages.push({
        role: c.type === 1 ? '用户' : 'Cursor',
        time: '',
        body: text,
      });
    }
    // 用最后一条的更新时间兜底，Cursor 不存每条消息的时间
    const t = j.lastUpdatedAt || j.createdAt;
    const clock = t ? new Date(Number(t)).toTimeString().slice(0, 5) : '';
    if (clock) messages.forEach((m) => (m.time = clock));

    return {
      title: tidy(j.name || messages.find((m) => m.role === '用户')?.body || '') || id.slice(0, 8),
      messages,
      source: file + '#' + id,
      note: 'Cursor Composer，SQLite 存储；不带头条消息时间，统一用会话最后更新时间',
      meta: { sessionId: id },
    };
  } finally {
    db.close();
  }
}
