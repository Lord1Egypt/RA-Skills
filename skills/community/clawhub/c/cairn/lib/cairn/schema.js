// v1 shipped without a migration runtime. v1.1 introduces `entity_tags` —
// purely additive (new table + new index), so `CREATE … IF NOT EXISTS` in
// the template handles upgrade for free. SCHEMA_VERSION bumps to 2 as a
// label; existing v1 DBs keep their `'1'` meta-stamp because the INSERT OR
// IGNORE below is a no-op when the row exists. The label is informational
// only until a non-additive change forces the migration runtime back.
export const SCHEMA_VERSION = 2;
export const EMBED_DIM = 768; // pinned to nomic-embed-text; embedded in DDL
export const VEC_OVERFETCH = 5; // KNN over-fetch multiplier when filter post-prunes results
export const SCHEMA = `
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS sources (
  id              INTEGER PRIMARY KEY,
  kind            TEXT NOT NULL CHECK (kind IN ('web','code','file','text','pdf')),
  uri             TEXT UNIQUE NOT NULL,
  label           TEXT,
  embed_model     TEXT NOT NULL CHECK (embed_model IN ('nomic-embed-text')),
  added_at        INTEGER NOT NULL,
  last_indexed_at INTEGER NOT NULL
) STRICT;

CREATE INDEX IF NOT EXISTS idx_sources_kind ON sources(kind);

CREATE TABLE IF NOT EXISTS files (
  id                  INTEGER PRIMARY KEY,
  source_id           INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  path                TEXT NOT NULL,
  hash                TEXT NOT NULL,
  mtime               INTEGER NOT NULL,
  lang                TEXT,
  -- File hash at the time doc-extraction last succeeded for this file.
  -- NULL = never run. When current hash differs, doc-extraction re-runs.
  doc_extracted_hash  TEXT,
  UNIQUE(source_id, path)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_files_source ON files(source_id);

CREATE TABLE IF NOT EXISTS chunks (
  id         INTEGER PRIMARY KEY,
  file_id    INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
  content    TEXT NOT NULL,
  start_line INTEGER NOT NULL,
  end_line   INTEGER NOT NULL
) STRICT;

CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunks(file_id);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  content,
  content='chunks',
  content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, content) VALUES ('delete', old.id, old.content);
END;

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_vec USING vec0(
  embedding float[${EMBED_DIM}]
);

-- chunks_vec has no FK; trigger keeps it in sync with chunks deletes (incl. cascade).
CREATE TRIGGER IF NOT EXISTS chunks_av AFTER DELETE ON chunks BEGIN
  DELETE FROM chunks_vec WHERE rowid = old.id;
END;

-- ─── Knowledge graph tables ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS entities (
  id         TEXT PRIMARY KEY,         -- "<source_id>:<filepath>:<name>"
  source_id  INTEGER REFERENCES sources(id) ON DELETE CASCADE,
  kind       TEXT NOT NULL CHECK (kind IN ('function','struct','enum','constant','concept')),
  name       TEXT NOT NULL,
  source     TEXT,                     -- relative file path within source
  line_start INTEGER,
  line_end   INTEGER,
  created_at INTEGER NOT NULL,
  removed_at INTEGER                   -- soft-delete; null = active
) STRICT;

-- Vector embeddings for entities. Mirrors the chunks_vec pattern —
-- sqlite-vec virtual table joined by rowid. SQLite has no native typed-array
-- column; \`F32[N]\` inline isn't valid syntax.
CREATE VIRTUAL TABLE IF NOT EXISTS entities_vec USING vec0(
  entity_rowid INTEGER PRIMARY KEY,
  embedding FLOAT[${EMBED_DIM}]
);

-- entities_vec has no FK; trigger keeps it in sync with entities deletes
-- (including the FK cascade from sources → entities → edges).
CREATE TRIGGER IF NOT EXISTS entities_ad AFTER DELETE ON entities BEGIN
  DELETE FROM entities_vec WHERE entity_rowid = old.rowid;
END;

CREATE TABLE IF NOT EXISTS edges (
  from_id    TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
  to_id      TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
  relation   TEXT NOT NULL CHECK (relation IN ('calls','defines','verifies','references','depends_on','evolved_from','mitigates')),
  confidence REAL NOT NULL DEFAULT 1.0,  -- 1.0 = explicit, 0.7 = LLM-inferred
  derive     TEXT NOT NULL DEFAULT 'parse' CHECK (derive IN ('parse','doc')),
  PRIMARY KEY (from_id, to_id, relation)
) STRICT;

-- Reverse-lookup index for "what calls X?" / called_by queries.
CREATE INDEX IF NOT EXISTS edges_to_id ON edges(to_id, relation);

-- ─── Cross-source linkage ────────────────────────────────────────────
--
-- Directional: source_a's function bodies are scanned for references that
-- resolve to source_b's entities (used to emit cross-source parse edges).
-- For a→b AND b→a, insert two rows. ON DELETE CASCADE on either side keeps
-- the link table consistent when a source is removed.
CREATE TABLE IF NOT EXISTS source_links (
  source_a INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  source_b INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  PRIMARY KEY (source_a, source_b)
) STRICT;

CREATE INDEX IF NOT EXISTS source_links_b ON source_links(source_b);

-- entities.source_id is on the table from the start in v1 (no migration
-- backfill path). The supporting index is part of the baseline.
CREATE INDEX IF NOT EXISTS entities_source_id ON entities(source_id);

-- ─── Tags (v1.1) ─────────────────────────────────────────────────────
-- Free-form descriptive metadata, primarily LLM-emitted on concept entities.
-- Multi-tag (PK is composite). Slugified at write time. FK cascade handles
-- cleanup on entity hard-delete; soft-deleted entities keep their tag rows
-- but are filtered out of read queries via the active-entity join.
CREATE TABLE IF NOT EXISTS entity_tags (
  entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
  tag       TEXT NOT NULL,
  PRIMARY KEY (entity_id, tag)
) STRICT;

-- "Give me everything tagged X" lookup.
CREATE INDEX IF NOT EXISTS entity_tags_tag ON entity_tags(tag);

-- Stamp the schema version on fresh DBs. INSERT OR IGNORE so existing DBs
-- preserve whatever stamp they were last opened with — useful breadcrumb if
-- a future v1.x ever needs to migrate.
INSERT OR IGNORE INTO meta(key, value) VALUES ('schema_version', '${SCHEMA_VERSION}');
`;
