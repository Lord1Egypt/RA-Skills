#!/usr/bin/env node

/**
 * rebuild-indexes.js
 *
 * Walks ~/memory/graph/, parses YAML frontmatter from every .md file,
 * and populates:
 *   - indexes/memory.db   (SQLite — nodes, relations, tags, FTS5)
 *
 * Usage:
 *   node ~/memory/scripts/rebuild-indexes.js              # full rebuild (default)
 *   node ~/memory/scripts/rebuild-indexes.js --incremental # only changed files
 *   node ~/memory/scripts/rebuild-indexes.js --with-backfill  # after rebuild, run scoped backfill on changed nodes
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const GRAPH_DIR = path.join(MEMORY_ROOT, "graph");
const INDEX_DIR = path.join(MEMORY_ROOT, "indexes");
const DB_PATH = path.join(INDEX_DIR, "memory.db");
const INCREMENTAL = process.argv.includes("--incremental");
const WITH_BACKFILL = process.argv.includes("--with-backfill");

// --- YAML frontmatter parser (no dependencies) ---

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return { meta: {}, body: content };
  return { meta: parseYaml(match[1]), body: content.slice(match[0].length).trim() };
}

function parseYaml(raw) {
  const result = {};
  const lines = raw.split("\n");
  let i = 0;
  while (i < lines.length) {
    const m = lines[i].match(/^(\w[\w-]*):\s*(.*)/);
    if (!m) { i++; continue; }
    const key = m[1];
    let val = m[2].trim();
    if (val === "" || val === "|") {
      const items = [];
      i++;
      while (i < lines.length && lines[i].match(/^\s+-\s/)) {
        items.push(parseInlineValue(lines[i].replace(/^\s+-\s*/, "").trim()));
        i++;
      }
      result[key] = items.length > 0 ? items : val;
      continue;
    }
    result[key] = val.startsWith("[") ? parseFlowArray(val) : parseScalar(val);
    i++;
  }
  return result;
}

function parseFlowArray(str) {
  const inner = str.slice(1, -1).trim();
  if (inner === "") return [];
  if (inner.startsWith("{")) {
    const objects = [];
    const re = /\{([^}]*)\}/g;
    let m;
    while ((m = re.exec(inner)) !== null) objects.push(parseInlineObject(m[1]));
    return objects;
  }
  return inner.split(",").map(s => parseScalar(s.trim()));
}

function parseInlineObject(str) {
  const obj = {};
  for (const pair of str.split(/,\s*(?=\w[\w-]*:)/)) {
    const m = pair.match(/(\w[\w-]*):\s*(.*)/);
    if (m) obj[m[1]] = parseScalar(m[2].trim());
  }
  return obj;
}

function parseInlineValue(str) {
  return str.startsWith("{") ? parseInlineObject(str.replace(/^\{|\}$/g, "").trim()) : parseScalar(str);
}

function parseScalar(str) {
  if (str === "true") return true;
  if (str === "false") return false;
  if (str === "null") return null;
  if ((str.startsWith('"') && str.endsWith('"')) || (str.startsWith("'") && str.endsWith("'")))
    return str.slice(1, -1);
  if (/^-?\d+(\.\d+)?$/.test(str)) return Number(str);
  return str;
}

// --- File walker ---

function walkDir(dir, base = dir) {
  const entries = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, item.name);
    if (item.isDirectory()) entries.push(...walkDir(full, base));
    else if (item.isFile() && item.name.endsWith(".md")) {
      const stat = fs.statSync(full);
      entries.push({
        fullPath: full,
        relPath: path.relative(base, full).replace(/\.md$/, ""),
        mtimeMs: stat.mtimeMs,
      });
    }
  }
  return entries;
}

// --- Database setup ---

function initDB(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS nodes (
      path TEXT PRIMARY KEY,
      type TEXT,
      title TEXT,
      status TEXT,
      created TEXT,
      updated TEXT,
      tags TEXT,
      body TEXT,
      mtime_ms REAL
    );

    CREATE TABLE IF NOT EXISTS relations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source TEXT NOT NULL,
      target TEXT NOT NULL,
      type TEXT NOT NULL,
      reason TEXT,
      derived INTEGER DEFAULT 0,
      UNIQUE(source, target, type)
    );

    CREATE TABLE IF NOT EXISTS tags (
      tag TEXT NOT NULL,
      node_path TEXT NOT NULL,
      PRIMARY KEY(tag, node_path)
    );

    CREATE TABLE IF NOT EXISTS meta (
      key TEXT PRIMARY KEY,
      value TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source);
    CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target);
    CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(type);
    CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);
    CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
    CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status);
  `);

  // Add 'updated' column if missing (migration for existing databases)
  try {
    db.exec("ALTER TABLE nodes ADD COLUMN updated TEXT");
  } catch (e) {
    // Column already exists — ignore
  }

  // FTS5 for full-text search (standalone, not content-synced — we manage inserts/deletes)
  try {
    db.exec(`
      CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
        path, title, body, tags
      );
    `);
  } catch (e) {
    if (!e.message.includes("already exists")) throw e;
  }
}

// --- Main ---

function main() {
  fs.mkdirSync(INDEX_DIR, { recursive: true });

  const db = new DatabaseSync(DB_PATH);
  db.exec("PRAGMA journal_mode=WAL");
  db.exec("PRAGMA synchronous=NORMAL");
  initDB(db);

  const files = walkDir(GRAPH_DIR);
  let lastBuildTime = 0;

  if (INCREMENTAL) {
    const row = db.prepare("SELECT value FROM meta WHERE key = 'last_build_ms'").get();
    if (row) lastBuildTime = parseFloat(row.value);
  }

  // Determine which files need processing
  let toProcess;
  if (INCREMENTAL && lastBuildTime > 0) {
    toProcess = files.filter(f => f.mtimeMs > lastBuildTime);
    // Also detect deletions: nodes in DB but not on disk
    const allPaths = new Set(files.map(f => f.relPath));
    const dbPaths = db.prepare("SELECT path FROM nodes").all().map(r => r.path);
    const deleted = dbPaths.filter(p => !allPaths.has(p));
    for (const p of deleted) {
      db.prepare("DELETE FROM nodes WHERE path = ?").run(p);
      db.prepare("DELETE FROM relations WHERE source = ? OR target = ?").run(p, p);
      db.prepare("DELETE FROM tags WHERE node_path = ?").run(p);
      db.prepare("DELETE FROM nodes_fts WHERE path = ?").run(p);
    }
    if (deleted.length > 0) {
      console.log(`  Removed ${deleted.length} deleted node(s)`);
    }
  } else {
    // Full rebuild — clear everything
    db.exec("DELETE FROM nodes");
    db.exec("DELETE FROM relations");
    db.exec("DELETE FROM tags");
    db.exec("DELETE FROM nodes_fts");
    toProcess = files;
  }

  // Prepared statements
  const upsertNode = db.prepare(`
    INSERT INTO nodes (path, type, title, status, created, updated, tags, body, mtime_ms)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(path) DO UPDATE SET
      type=excluded.type, title=excluded.title, status=excluded.status,
      created=excluded.created, updated=excluded.updated, tags=excluded.tags,
      body=excluded.body, mtime_ms=excluded.mtime_ms
  `);

  const deleteRelations = db.prepare("DELETE FROM relations WHERE source = ? AND derived = 0");
  const insertRelation = db.prepare(`
    INSERT OR IGNORE INTO relations (source, target, type, reason, derived)
    VALUES (?, ?, ?, ?, ?)
  `);

  const deleteTags = db.prepare("DELETE FROM tags WHERE node_path = ?");
  const insertTag = db.prepare("INSERT OR IGNORE INTO tags (tag, node_path) VALUES (?, ?)");

  const deleteFts = db.prepare("DELETE FROM nodes_fts WHERE path = ?");
  const insertFts = db.prepare("INSERT INTO nodes_fts (path, title, body, tags) VALUES (?, ?, ?, ?)");

  // Track changed nodes for --with-backfill
  const changedPaths = [];

  // Process files
  let processed = 0;
  for (const { fullPath, relPath, mtimeMs } of toProcess) {
    const content = fs.readFileSync(fullPath, "utf-8");
    const { meta, body } = parseFrontmatter(content);
    const titleMatch = body.match(/^#\s+(.+)/m);
    const title = titleMatch ? titleMatch[1].trim() : relPath.split("/").pop();
    const tags = Array.isArray(meta.tags) ? meta.tags : [];
    const tagsStr = tags.join(", ");

    // Parse 'updated' field — fall back to file mtime as ISO date
    let updated = meta.updated ? String(meta.updated) : null;
    if (!updated) {
      updated = new Date(mtimeMs).toISOString().split("T")[0];
    }

    // Upsert node
    upsertNode.run(
      relPath, meta.type || null, title, meta.status || null,
      meta.created ? String(meta.created) : null, updated, tagsStr, body, mtimeMs
    );

    // Relations (forward only — we'll compute reverse after)
    deleteRelations.run(relPath);
    const rels = Array.isArray(meta.relations) ? meta.relations : [];
    for (const rel of rels) {
      if (rel?.to && rel?.type) {
        insertRelation.run(relPath, rel.to, rel.type, rel.reason || null, 0);
      }
    }

    // Tags
    deleteTags.run(relPath);
    for (const tag of tags) {
      insertTag.run(tag, relPath);
    }

    // FTS
    deleteFts.run(relPath);
    insertFts.run(relPath, title, body, tagsStr);

    changedPaths.push(relPath);
    processed++;
  }

  // Compute reverse (derived) relations
  // Clear old derived relations and recompute from current forward relations
  db.exec("DELETE FROM relations WHERE derived = 1");
  db.exec(`
    INSERT OR IGNORE INTO relations (source, target, type, reason, derived)
    SELECT target, source, type, reason, 1 FROM relations WHERE derived = 0
  `);

  // Update build timestamp
  db.prepare("INSERT OR REPLACE INTO meta (key, value) VALUES ('last_build_ms', ?)").run(String(Date.now()));

  // Stats
  const nodeCount = db.prepare("SELECT COUNT(*) as c FROM nodes").get().c;
  const relCount = db.prepare("SELECT COUNT(*) as c FROM relations").get().c;
  const tagCount = db.prepare("SELECT COUNT(DISTINCT tag) as c FROM tags").get().c;

  const mode = INCREMENTAL && lastBuildTime > 0 ? `incremental — ${processed} file(s) updated` : "full rebuild";
  console.log(`✓ ${mode}: ${nodeCount} nodes, ${relCount} relations, ${tagCount} tags`);

  db.close();

  // --with-backfill: run scoped backfill on changed nodes
  if (WITH_BACKFILL && changedPaths.length > 0) {
    const backfillScript = path.join(__dirname, "suggest-backfill.js");
    if (fs.existsSync(backfillScript)) {
      console.log(`\nRunning scoped backfill on ${changedPaths.length} changed node(s)...`);
      for (const nodePath of changedPaths) {
        try {
          const output = execSync(
            `node ${JSON.stringify(backfillScript)} --scope node:${nodePath} --no-qmd`,
            { encoding: "utf-8", timeout: 30000 }
          );
          if (output.trim()) console.log(`  ${nodePath}: ${output.trim()}`);
        } catch (e) {
          console.error(`  ${nodePath}: backfill failed — ${e.message}`);
        }
      }
    } else {
      console.log("  suggest-backfill.js not found — skipping backfill");
    }
  }
}

main();
