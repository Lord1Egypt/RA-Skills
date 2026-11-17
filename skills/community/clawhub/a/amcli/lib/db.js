'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { appleDate, toAppleNanos, messageText } = require('./decode');

const DB_PATH = path.join(os.homedir(), 'Library', 'Messages', 'chat.db');

const NOT_AUTHORIZED_MESSAGE =
  `Cannot read ${DB_PATH}: your terminal app needs Full Disk Access. ` +
  'Grant it in System Settings > Privacy & Security > Full Disk Access, then restart the terminal.';

class AmcliError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

// Tapbacks and other reactions are stored as messages; listings skip them.
const NOT_REACTION = 'm.associated_message_type NOT BETWEEN 2000 AND 3999 AND m.item_type = 0';

function open() {
  try {
    fs.statSync(DB_PATH);
  } catch (err) {
    if (err.code === 'ENOENT') throw new AmcliError('NO_DATABASE', `No Messages database at ${DB_PATH}`);
    throw new AmcliError('NOT_AUTHORIZED', NOT_AUTHORIZED_MESSAGE);
  }
  const { DatabaseSync } = require('node:sqlite');
  let db;
  try {
    db = new DatabaseSync(DB_PATH, { readOnly: true });
    db.prepare('SELECT 1 FROM message LIMIT 1').get();
  } catch {
    throw new AmcliError('NOT_AUTHORIZED', NOT_AUTHORIZED_MESSAGE);
  }
  return db;
}

/** Dates are nanoseconds past 2^53, so every statement reads integers as BigInt. */
function all(db, sql, ...params) {
  const stmt = db.prepare(sql);
  stmt.setReadBigInts(true);
  return stmt.all(...params);
}

function iterate(db, sql, ...params) {
  const stmt = db.prepare(sql);
  stmt.setReadBigInts(true);
  return stmt.iterate(...params);
}

function iso(raw) {
  const d = appleDate(raw);
  return d ? d.toISOString() : null;
}

function participants(db, chatId) {
  return all(
    db,
    'SELECT h.id FROM chat_handle_join chj JOIN handle h ON h.ROWID = chj.handle_id WHERE chj.chat_id = ? ORDER BY h.id',
    chatId,
  ).map((r) => r.id);
}

function chatName(row, members) {
  if (row.display_name) return row.display_name;
  if (members.length > 1) return members.join(', ');
  return row.chat_identifier;
}

function toChat(db, row) {
  const members = participants(db, row.id);
  return {
    id: Number(row.id),
    guid: row.guid,
    name: chatName(row, members),
    identifier: row.chat_identifier,
    service: row.service_name,
    group: Number(row.style) === 43,
    participants: members,
    lastMessageAt: iso(row.last_date),
    unread: Number(row.unread || 0),
  };
}

const CHAT_SELECT = `
  SELECT c.ROWID AS id, c.guid, c.chat_identifier, c.display_name, c.service_name, c.style,
    MAX(cmj.message_date) AS last_date,
    SUM(CASE WHEN m.is_read = 0 AND m.is_from_me = 0 AND ${NOT_REACTION} THEN 1 ELSE 0 END) AS unread
  FROM chat c
  JOIN chat_message_join cmj ON cmj.chat_id = c.ROWID
  JOIN message m ON m.ROWID = cmj.message_id`;

/** Chats with the newest message first. */
function listChats(db, { limit = 20, unreadOnly = false } = {}) {
  const having = unreadOnly ? 'HAVING unread > 0' : '';
  return all(db, `${CHAT_SELECT} GROUP BY c.ROWID ${having} ORDER BY last_date DESC LIMIT ?`, limit).map((r) =>
    toChat(db, r),
  );
}

/** A chat by ROWID, guid, or identifier (the phone, email or group id it is keyed on). */
function findChat(db, ref) {
  let rows = /^\d+$/.test(ref) ? all(db, `${CHAT_SELECT} WHERE c.ROWID = ? GROUP BY c.ROWID`, Number(ref)) : [];
  if (!rows.length) {
    rows = all(
      db,
      `${CHAT_SELECT} WHERE c.guid = ? OR c.chat_identifier = ? GROUP BY c.ROWID ORDER BY last_date DESC`,
      ref,
      ref,
    );
  }
  if (!rows.length) throw new AmcliError('CHAT_NOT_FOUND', `No chat matches ${ref}`);
  return toChat(db, rows[0]);
}

function attachmentsOf(db, messageId) {
  return all(
    db,
    `SELECT a.transfer_name, a.filename FROM message_attachment_join maj
     JOIN attachment a ON a.ROWID = maj.attachment_id WHERE maj.message_id = ?`,
    messageId,
  )
    .map((a) => a.transfer_name || (a.filename ? path.basename(a.filename) : null))
    .filter(Boolean);
}

function toMessage(db, row) {
  const fromMe = Number(row.is_from_me) === 1;
  return {
    id: Number(row.id),
    guid: row.guid,
    chatId: row.chat_id == null ? null : Number(row.chat_id),
    date: iso(row.date),
    fromMe,
    sender: fromMe ? null : row.handle || null,
    service: row.service,
    text: messageText(row.text, row.attributedBody),
    attachments: Number(row.cache_has_attachments) ? attachmentsOf(db, row.id) : [],
  };
}

const MESSAGE_SELECT = `
  SELECT m.ROWID AS id, m.guid, m.text, m.attributedBody, m.is_from_me, m.service, m.date,
    m.cache_has_attachments, h.id AS handle, cmj.chat_id
  FROM message m
  JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
  LEFT JOIN handle h ON h.ROWID = m.handle_id`;

/** The newest `limit` messages in a chat, returned oldest first. */
function chatMessages(db, chatId, { limit = 20, since = null } = {}) {
  const rows = all(
    db,
    `${MESSAGE_SELECT} WHERE cmj.chat_id = ? AND m.date >= ? AND ${NOT_REACTION} ORDER BY m.date DESC LIMIT ?`,
    chatId,
    since ? toAppleNanos(since) : 0n,
    limit,
  );
  return rows.map((r) => toMessage(db, r)).reverse();
}

/**
 * Messages whose text contains `query`, newest first. Text may live only in
 * attributedBody, so matching happens after decoding, not in SQL.
 */
function searchMessages(db, query, { limit = 20, since = null, chatId = null } = {}) {
  const needle = query.toLowerCase();
  const where = [`m.date >= ?`, NOT_REACTION, '(m.text IS NOT NULL OR m.attributedBody IS NOT NULL)'];
  const params = [since ? toAppleNanos(since) : 0n];
  if (chatId != null) {
    where.push('cmj.chat_id = ?');
    params.push(chatId);
  }
  const found = [];
  const names = new Map();
  for (const row of iterate(db, `${MESSAGE_SELECT} WHERE ${where.join(' AND ')} ORDER BY m.date DESC`, ...params)) {
    const text = messageText(row.text, row.attributedBody);
    if (!text || !text.toLowerCase().includes(needle)) continue;
    const msg = toMessage(db, row);
    if (!names.has(msg.chatId)) names.set(msg.chatId, findChat(db, String(msg.chatId)).name);
    msg.chat = names.get(msg.chatId);
    found.push(msg);
    if (found.length >= limit) break;
  }
  return found;
}

module.exports = {
  DB_PATH,
  NOT_AUTHORIZED_MESSAGE,
  AmcliError,
  open,
  listChats,
  findChat,
  chatMessages,
  searchMessages,
};
