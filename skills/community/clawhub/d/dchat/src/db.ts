import Database from "better-sqlite3";
import path from "path";
import fs from "fs";
import type { Message, MessageStatus } from "./types.js";

const SCHEMA = `
CREATE TABLE IF NOT EXISTS message (
  id TEXT PRIMARY KEY,
  sender TEXT NOT NULL,
  receiver TEXT NOT NULL,
  content_type TEXT NOT NULL,
  content TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'sending',
  is_outbound INTEGER NOT NULL DEFAULT 0,
  options TEXT,
  local_file_path TEXT,
  delete_at INTEGER,
  is_delete INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_message_sender ON message(sender);
CREATE INDEX IF NOT EXISTS idx_message_receiver ON message(receiver);
CREATE INDEX IF NOT EXISTS idx_message_created ON message(created_at);
CREATE INDEX IF NOT EXISTS idx_message_delete_at ON message(delete_at) WHERE delete_at IS NOT NULL;

CREATE TABLE IF NOT EXISTS peer (
  address TEXT PRIMARY KEY,
  name TEXT,
  last_seen_at INTEGER,
  created_at INTEGER NOT NULL
);
`;

export class MessageDb {
  private db: Database.Database;

  constructor(dataDir: string) {
    fs.mkdirSync(dataDir, { recursive: true });
    const dbPath = path.join(dataDir, "messages.db");
    this.db = new Database(dbPath);
    this.db.pragma("journal_mode = WAL");
    this.db.pragma("foreign_keys = ON");
    this.db.exec(SCHEMA);
  }

  insertMessage(msg: Message): void {
    this.db
      .prepare(
        `INSERT OR IGNORE INTO message
         (id, sender, receiver, content_type, content, status, is_outbound, options, local_file_path, delete_at, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .run(
        msg.id,
        msg.sender,
        msg.receiver,
        msg.contentType,
        msg.content,
        msg.status,
        msg.isOutbound ? 1 : 0,
        msg.options ?? null,
        msg.localFilePath ?? null,
        msg.deleteAt ?? null,
        msg.createdAt,
        msg.createdAt,
      );
  }

  updateStatus(id: string, status: MessageStatus): void {
    this.db.prepare("UPDATE message SET status = ?, updated_at = ? WHERE id = ?").run(status, Date.now(), id);
  }

  /** Update status only if current status is not already "delivered" or "read" (prevents downgrade). */
  updateStatusIfNotDelivered(id: string, status: MessageStatus): void {
    this.db
      .prepare("UPDATE message SET status = ?, updated_at = ? WHERE id = ? AND status NOT IN ('delivered', 'read')")
      .run(status, Date.now(), id);
  }

  updateLocalFilePath(id: string, filePath: string): void {
    this.db.prepare("UPDATE message SET local_file_path = ?, updated_at = ? WHERE id = ?").run(filePath, Date.now(), id);
  }

  hasMessage(id: string): boolean {
    const row = this.db.prepare("SELECT 1 FROM message WHERE id = ?").get(id);
    return !!row;
  }

  getMessages(peerAddress: string, limit = 50, before?: number): Message[] {
    const query = before
      ? `SELECT * FROM message WHERE ((sender = ? OR receiver = ?) AND is_delete = 0 AND created_at < ?) ORDER BY created_at DESC LIMIT ?`
      : `SELECT * FROM message WHERE ((sender = ? OR receiver = ?) AND is_delete = 0) ORDER BY created_at DESC LIMIT ?`;

    const rows = before
      ? (this.db.prepare(query).all(peerAddress, peerAddress, before, limit) as any[])
      : (this.db.prepare(query).all(peerAddress, peerAddress, limit) as any[]);

    return rows.map(this.rowToMessage).reverse();
  }

  /** Find and mark expired burn-after-read messages */
  burnExpired(): string[] {
    const now = Date.now();
    const expired = this.db
      .prepare("SELECT id FROM message WHERE delete_at IS NOT NULL AND delete_at <= ? AND is_delete = 0")
      .all(now) as { id: string }[];

    if (expired.length > 0) {
      const ids = expired.map((r) => r.id);
      this.db.prepare(`UPDATE message SET is_delete = 1, updated_at = ? WHERE id IN (${ids.map(() => "?").join(",")})`)
        .run(now, ...ids);
      return ids;
    }
    return [];
  }

  upsertPeer(address: string, name?: string): void {
    this.db
      .prepare(
        `INSERT INTO peer (address, name, last_seen_at, created_at)
         VALUES (?, ?, ?, ?)
         ON CONFLICT(address) DO UPDATE SET last_seen_at = ?, name = COALESCE(?, name)`,
      )
      .run(address, name ?? null, Date.now(), Date.now(), Date.now(), name ?? null);
  }

  // ── Contacts ─────────────────────────────────────────────

  addContact(address: string, alias: string): void {
    this.db
      .prepare(
        `INSERT INTO peer (address, name, last_seen_at, created_at)
         VALUES (?, ?, ?, ?)
         ON CONFLICT(address) DO UPDATE SET name = ?`,
      )
      .run(address, alias, Date.now(), Date.now(), alias);
  }

  removeContact(addressOrAlias: string): boolean {
    const address = this.resolveAlias(addressOrAlias) ?? addressOrAlias;
    const result = this.db.prepare("DELETE FROM peer WHERE address = ?").run(address);
    return result.changes > 0;
  }

  listContacts(): { address: string; name: string | null; lastSeenAt: number | null }[] {
    const rows = this.db
      .prepare("SELECT address, name, last_seen_at FROM peer ORDER BY name, address")
      .all() as any[];
    return rows.map((r) => ({ address: r.address, name: r.name, lastSeenAt: r.last_seen_at }));
  }

  /** Resolve an alias to an NKN address. Returns null if not found. */
  resolveAlias(alias: string): string | null {
    const row = this.db
      .prepare("SELECT address FROM peer WHERE name = ? COLLATE NOCASE")
      .get(alias) as { address: string } | undefined;
    return row?.address ?? null;
  }

  /** Get the alias for an NKN address. Returns null if no alias set. */
  getAlias(address: string): string | null {
    const row = this.db
      .prepare("SELECT name FROM peer WHERE address = ?")
      .get(address) as { name: string | null } | undefined;
    return row?.name ?? null;
  }

  close(): void {
    this.db.close();
  }

  private rowToMessage(row: any): Message {
    return {
      id: row.id,
      sender: row.sender,
      receiver: row.receiver,
      contentType: row.content_type,
      content: row.content,
      status: row.status,
      isOutbound: !!row.is_outbound,
      options: row.options ?? undefined,
      localFilePath: row.local_file_path ?? undefined,
      deleteAt: row.delete_at ?? undefined,
      createdAt: row.created_at,
    };
  }
}
