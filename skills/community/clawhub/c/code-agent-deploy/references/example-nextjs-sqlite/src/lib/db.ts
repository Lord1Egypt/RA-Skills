import Database from 'better-sqlite3';
import fs from 'node:fs';
import path from 'node:path';

// DATABASE_URL is injected by the platform (file:/app/data/app.db); locally it defaults to ./data/app.db
const file = (process.env.DATABASE_URL ?? 'file:./data/app.db').replace(/^file:/, '');

let db: Database.Database | undefined;

export function getDb() {
  if (!db) {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    db = new Database(file);
    db.pragma('journal_mode = WAL');
    db.exec('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL)');
  }
  return db;
}
