#!/usr/bin/env node

/**
 * query.js — Query the memory graph via SQLite index.
 *
 * Usage:
 *   node ~/memory/scripts/query.js --search "immutability"          # full-text search
 *   node ~/memory/scripts/query.js --node projects/flowmind         # node details + relations
 *   node ~/memory/scripts/query.js --related-to tools/typescript    # all nodes related to X
 *   node ~/memory/scripts/query.js --tag side-project               # all nodes with tag
 *   node ~/memory/scripts/query.js --type project                   # all nodes of type
 *   node ~/memory/scripts/query.js --type project --status active   # filtered
 *   node ~/memory/scripts/query.js --stats                          # graph statistics
 *   node ~/memory/scripts/query.js --recent 7                       # nodes modified in last N days
 *   node ~/memory/scripts/query.js --stale 30                       # nodes not updated in N days
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const DB_PATH = path.join(MEMORY_ROOT, "indexes", "memory.db");

if (!fs.existsSync(DB_PATH)) {
  console.error("Missing memory.db — run rebuild-indexes.js first");
  process.exit(1);
}

const db = new DatabaseSync(DB_PATH);
const args = process.argv.slice(2);

function getArg(flag) {
  const idx = args.indexOf(flag);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

function printRows(rows, label) {
  if (rows.length === 0) {
    console.log(`No results.`);
    return;
  }
  if (label) console.log(`\n${label} (${rows.length}):\n`);
  for (const row of rows) {
    const parts = [];
    for (const [k, v] of Object.entries(row)) {
      if (v !== null && v !== undefined && v !== "") parts.push(`${k}: ${v}`);
    }
    console.log(`  ${parts.join(" | ")}`);
  }
  console.log();
}

// --- Commands ---

if (args.includes("--search")) {
  const query = getArg("--search");
  try {
    const escaped = `"${query.replace(/"/g, '""')}"`;
    const rows = db.prepare(`
      SELECT path, title, tags FROM nodes_fts WHERE nodes_fts MATCH ? LIMIT 20
    `).all(escaped);
    printRows(rows, `Search: "${query}"`);
  } catch {
    // Fallback to LIKE if FTS fails
    const rows = db.prepare(`
      SELECT path, title, tags FROM nodes WHERE body LIKE ? OR title LIKE ? LIMIT 20
    `).all(`%${query}%`, `%${query}%`);
    printRows(rows, `Search: "${query}" (fallback)`);
  }
}

else if (args.includes("--node")) {
  const nodePath = getArg("--node");
  const node = db.prepare("SELECT * FROM nodes WHERE path = ?").get(nodePath);
  if (!node) {
    console.log(`Node not found: ${nodePath}`);
  } else {
    console.log(`\n${node.title} (${node.path})`);
    console.log(`  type: ${node.type} | status: ${node.status || "—"} | created: ${node.created || "—"} | updated: ${node.updated || "—"}`);
    console.log(`  tags: ${node.tags || "—"}`);

    const outgoing = db.prepare(
      "SELECT target, type, reason FROM relations WHERE source = ? AND derived = 0"
    ).all(nodePath);
    if (outgoing.length > 0) {
      console.log(`\n  Relations (outgoing):`);
      for (const r of outgoing) {
        console.log(`    → ${r.target} [${r.type}]${r.reason ? ` (${r.reason})` : ""}`);
      }
    }

    const incoming = db.prepare(
      "SELECT source, type, reason FROM relations WHERE target = ? AND derived = 0"
    ).all(nodePath);
    if (incoming.length > 0) {
      console.log(`\n  Relations (incoming):`);
      for (const r of incoming) {
        console.log(`    ← ${r.source} [${r.type}]${r.reason ? ` (${r.reason})` : ""}`);
      }
    }
    console.log();
  }
}

else if (args.includes("--related-to")) {
  const nodePath = getArg("--related-to");
  const type = getArg("--type");
  let rows;
  if (type) {
    rows = db.prepare(`
      SELECT DISTINCT n.path, n.title, n.type, r.type as rel_type
      FROM relations r JOIN nodes n ON (r.target = n.path OR r.source = n.path)
      WHERE (r.source = ? OR r.target = ?) AND n.path != ? AND n.type = ?
    `).all(nodePath, nodePath, nodePath, type);
  } else {
    rows = db.prepare(`
      SELECT DISTINCT n.path, n.title, n.type, r.type as rel_type
      FROM relations r JOIN nodes n ON (r.target = n.path OR r.source = n.path)
      WHERE (r.source = ? OR r.target = ?) AND n.path != ?
    `).all(nodePath, nodePath, nodePath);
  }
  printRows(rows, `Related to: ${nodePath}`);
}

else if (args.includes("--tag")) {
  const tag = getArg("--tag");
  const rows = db.prepare(`
    SELECT n.path, n.title, n.type, n.status
    FROM tags t JOIN nodes n ON t.node_path = n.path
    WHERE t.tag = ?
  `).all(tag);
  printRows(rows, `Tag: ${tag}`);
}

else if (args.includes("--type")) {
  const type = getArg("--type");
  const status = getArg("--status");
  let rows;
  if (status) {
    rows = db.prepare("SELECT path, title, status, tags FROM nodes WHERE type = ? AND status = ?").all(type, status);
  } else {
    rows = db.prepare("SELECT path, title, status, tags FROM nodes WHERE type = ?").all(type);
  }
  printRows(rows, `Type: ${type}${status ? ` (status: ${status})` : ""}`);
}

else if (args.includes("--stats")) {
  const nodes = db.prepare("SELECT COUNT(*) as c FROM nodes").get().c;
  const rels = db.prepare("SELECT COUNT(*) as c FROM relations").get().c;
  const fwdRels = db.prepare("SELECT COUNT(*) as c FROM relations WHERE derived = 0").get().c;
  const tags = db.prepare("SELECT COUNT(DISTINCT tag) as c FROM tags").get().c;
  const types = db.prepare("SELECT type, COUNT(*) as c FROM nodes GROUP BY type ORDER BY c DESC").all();
  const topTags = db.prepare("SELECT tag, COUNT(*) as c FROM tags GROUP BY tag ORDER BY c DESC LIMIT 10").all();
  const mostConnected = db.prepare(`
    SELECT path, COUNT(*) as connections FROM (
      SELECT source as path FROM relations WHERE derived = 0
      UNION ALL
      SELECT target as path FROM relations WHERE derived = 0
    ) GROUP BY path ORDER BY connections DESC LIMIT 5
  `).all();

  console.log(`\nGraph Statistics`);
  console.log(`  Nodes: ${nodes}`);
  console.log(`  Relations: ${fwdRels} (${rels} incl. derived)`);
  console.log(`  Unique tags: ${tags}`);
  console.log(`\n  By type:`);
  for (const t of types) console.log(`    ${t.type}: ${t.c}`);
  console.log(`\n  Top tags:`);
  for (const t of topTags) console.log(`    ${t.tag}: ${t.c}`);
  console.log(`\n  Most connected:`);
  for (const m of mostConnected) console.log(`    ${m.path}: ${m.connections} relations`);
  console.log();
}

else if (args.includes("--recent")) {
  const days = parseInt(getArg("--recent") || "7", 10);
  const since = Date.now() - days * 24 * 60 * 60 * 1000;
  const rows = db.prepare("SELECT path, title, type, status FROM nodes WHERE mtime_ms > ? ORDER BY mtime_ms DESC").all(since);
  printRows(rows, `Modified in last ${days} day(s)`);
}

else if (args.includes("--stale")) {
  const days = parseInt(getArg("--stale") || "30", 10);
  const cutoff = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  const rows = db.prepare(`
    SELECT path, title, type, updated, status
    FROM nodes
    WHERE updated IS NOT NULL AND updated < ?
    ORDER BY updated ASC
  `).all(cutoff);
  printRows(rows, `Stale nodes (not updated in ${days}+ days)`);
}

else {
  console.log(`Usage:
  --search <query>        Full-text search
  --node <path>           Node details + relations
  --related-to <path>     All related nodes (optional --type filter)
  --tag <tag>             All nodes with tag
  --type <type>           All nodes of type (optional --status filter)
  --stats                 Graph statistics
  --recent <days>         Recently modified nodes
  --stale <days>          Nodes not updated in N days`);
}

db.close();
