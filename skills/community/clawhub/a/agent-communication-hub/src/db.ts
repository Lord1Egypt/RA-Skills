import Database from "better-sqlite3";

export type SqliteDatabase = Database.Database;

export function openDatabase(filename: string): SqliteDatabase {
  const db = new Database(filename);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  initializeSchema(db);
  return db;
}

function initializeSchema(db: SqliteDatabase): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS agents (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      status TEXT NOT NULL,
      metadata_json TEXT NOT NULL,
      last_seen_at TEXT NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      agent_id TEXT NOT NULL,
      status TEXT NOT NULL,
      connected_at TEXT NOT NULL,
      disconnected_at TEXT,
      metadata_json TEXT NOT NULL,
      FOREIGN KEY (agent_id) REFERENCES agents(id)
    );

    CREATE TABLE IF NOT EXISTS messages (
      id TEXT PRIMARY KEY,
      kind TEXT NOT NULL,
      sender_id TEXT NOT NULL,
      recipient_id TEXT,
      payload_json TEXT NOT NULL,
      status TEXT NOT NULL,
      topic TEXT,
      created_at TEXT NOT NULL,
      delivered_at TEXT,
      acknowledged_at TEXT,
      correlation_id TEXT,
      FOREIGN KEY (sender_id) REFERENCES agents(id),
      FOREIGN KEY (recipient_id) REFERENCES agents(id)
    );

    CREATE TABLE IF NOT EXISTS events (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,
      source_agent_id TEXT,
      payload_json TEXT NOT NULL,
      metadata_json TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY (source_agent_id) REFERENCES agents(id)
    );

    CREATE TABLE IF NOT EXISTS event_subscriptions (
      id TEXT PRIMARY KEY,
      agent_id TEXT NOT NULL,
      event_type TEXT NOT NULL,
      filter_json TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY (agent_id) REFERENCES agents(id)
    );

    CREATE INDEX IF NOT EXISTS idx_messages_recipient_status
      ON messages(recipient_id, status, created_at);
    CREATE INDEX IF NOT EXISTS idx_messages_sender
      ON messages(sender_id, created_at);
    CREATE INDEX IF NOT EXISTS idx_events_type_created
      ON events(type, created_at);
    CREATE INDEX IF NOT EXISTS idx_subscriptions_agent_type
      ON event_subscriptions(agent_id, event_type);
  `);
}

export function nowIso(): string {
  return new Date().toISOString();
}

export function createId(prefix: string): string {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

export function toJson(value: Record<string, unknown>): string {
  return JSON.stringify(value);
}

export function fromJson(value: string): Record<string, unknown> {
  return JSON.parse(value) as Record<string, unknown>;
}
