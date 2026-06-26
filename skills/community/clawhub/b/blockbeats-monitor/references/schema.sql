-- 本文件定义 BlockBeats 舆情监控使用的 SQLite 表结构。

CREATE TABLE IF NOT EXISTS keyword_groups (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  expression TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_items (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  source_type TEXT NOT NULL,
  title TEXT,
  abstract TEXT,
  content TEXT,
  url TEXT,
  published_at TEXT,
  raw_json TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_sources (
  item_id TEXT NOT NULL,
  source_type TEXT NOT NULL,
  raw_json TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  PRIMARY KEY (item_id, source_type),
  FOREIGN KEY (item_id) REFERENCES source_items(id)
);

CREATE TABLE IF NOT EXISTS item_matches (
  item_id TEXT NOT NULL,
  group_id TEXT NOT NULL,
  matched_text TEXT,
  matched_at TEXT NOT NULL,
  PRIMARY KEY (item_id, group_id),
  FOREIGN KEY (item_id) REFERENCES source_items(id),
  FOREIGN KEY (group_id) REFERENCES keyword_groups(id)
);

CREATE TABLE IF NOT EXISTS daily_keyword_metrics (
  report_date TEXT NOT NULL,
  window_start TEXT NOT NULL,
  window_end TEXT NOT NULL,
  group_id TEXT NOT NULL,
  mention_count INTEGER NOT NULL,
  previous_mention_count INTEGER NOT NULL,
  PRIMARY KEY (report_date, group_id),
  FOREIGN KEY (group_id) REFERENCES keyword_groups(id)
);

CREATE TABLE IF NOT EXISTS report_runs (
  id TEXT PRIMARY KEY,
  report_date TEXT NOT NULL,
  window_start TEXT NOT NULL,
  window_end TEXT NOT NULL,
  markdown TEXT NOT NULL,
  telegram_status TEXT,
  created_at TEXT NOT NULL
);
