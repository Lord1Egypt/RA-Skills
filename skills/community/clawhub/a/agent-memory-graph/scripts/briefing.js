#!/usr/bin/env node

/**
 * briefing.js — Context assembly for agents.
 *
 * Generates a markdown briefing document with:
 *   - Target node's full content
 *   - 1-hop related nodes (titles + key fields)
 *   - 2-hop relations (titles only)
 *   - Recent log entries referencing the node (last 7 days)
 *   - Staleness information
 *
 * Usage:
 *   node ~/memory/scripts/briefing.js --node projects/flowmind
 *   node ~/memory/scripts/briefing.js --topic "immutability"
 *   node ~/memory/scripts/briefing.js --node projects/flowmind --days 14
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const GRAPH_DIR = path.join(MEMORY_ROOT, "graph");
const LOG_DIR = path.join(MEMORY_ROOT, "log");
const DB_PATH = path.join(MEMORY_ROOT, "indexes", "memory.db");

const args = process.argv.slice(2);

function getArg(flag) {
  const idx = args.indexOf(flag);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

if (!fs.existsSync(DB_PATH)) {
  console.error("Missing memory.db — run rebuild-indexes.js first");
  process.exit(1);
}

const db = new DatabaseSync(DB_PATH);
const LOG_DAYS = parseInt(getArg("--days") || "7", 10);

// --- Helpers ---

function getNode(nodePath) {
  return db.prepare("SELECT * FROM nodes WHERE path = ?").get(nodePath);
}

function getRelated(nodePath) {
  // Only use forward (non-derived) relations to avoid duplicates.
  // We show direction by checking whether nodePath is source (→) or target (←).
  const forward = db.prepare(`
    SELECT n.path, n.title, n.type, n.status, n.updated, n.tags, r.type as rel_type, 0 as derived
    FROM relations r
    JOIN nodes n ON r.target = n.path
    WHERE r.source = ? AND r.derived = 0 AND n.path != ?
  `).all(nodePath, nodePath);
  const incoming = db.prepare(`
    SELECT n.path, n.title, n.type, n.status, n.updated, n.tags, r.type as rel_type, 1 as derived
    FROM relations r
    JOIN nodes n ON r.source = n.path
    WHERE r.target = ? AND r.derived = 0 AND n.path != ?
  `).all(nodePath, nodePath);
  // Dedupe by path — prefer forward entries
  const seen = new Set();
  const results = [];
  for (const r of [...forward, ...incoming]) {
    if (!seen.has(r.path)) { seen.add(r.path); results.push(r); }
  }
  return results;
}

function get2ndHop(nodePath, firstHopPaths) {
  const exclude = new Set([nodePath, ...firstHopPaths]);
  const results = [];
  for (const hop1 of firstHopPaths) {
    const fwd = db.prepare(`SELECT n.path, n.title, n.type, r.type as rel_type FROM relations r JOIN nodes n ON r.target = n.path WHERE r.source = ? AND r.derived = 0`).all(hop1);
    const inc = db.prepare(`SELECT n.path, n.title, n.type, r.type as rel_type FROM relations r JOIN nodes n ON r.source = n.path WHERE r.target = ? AND r.derived = 0`).all(hop1);
    const neighbors = [...fwd, ...inc];
    for (const n of neighbors) {
      if (!exclude.has(n.path)) {
        results.push({ ...n, via: hop1 });
        exclude.add(n.path); // dedupe
      }
    }
  }
  return results;
}

function getNodeFileContent(nodePath) {
  const fullPath = path.join(GRAPH_DIR, nodePath + ".md");
  try {
    return fs.readFileSync(fullPath, "utf-8");
  } catch {
    return null;
  }
}

function getRecentLogEntries(nodePath, days) {
  const entries = [];
  const now = new Date();
  try {
    const logFiles = fs.readdirSync(LOG_DIR).filter(f => f.endsWith(".md")).sort().reverse();
    for (const file of logFiles) {
      const dateStr = file.replace(".md", "");
      const fileDate = new Date(dateStr);
      const diffDays = (now - fileDate) / (1000 * 60 * 60 * 24);
      if (diffDays > days) break;

      const content = fs.readFileSync(path.join(LOG_DIR, file), "utf-8");
      for (const line of content.split("\n")) {
        if (line.includes(nodePath) || line.toLowerCase().includes(nodePath.split("/").pop())) {
          entries.push({ date: dateStr, line: line.trim() });
        }
      }
    }
  } catch {}
  return entries;
}

function staleness(updated) {
  if (!updated) return "unknown";
  const diff = Math.floor((Date.now() - new Date(updated).getTime()) / (1000 * 60 * 60 * 24));
  if (diff <= 7) return `fresh (${diff}d ago)`;
  if (diff <= 30) return `recent (${diff}d ago)`;
  if (diff <= 90) return `aging (${diff}d ago)`;
  return `stale (${diff}d ago)`;
}

// --- Briefing by node ---

function briefNode(nodePath) {
  const node = getNode(nodePath);
  if (!node) {
    console.error(`Node not found: ${nodePath}`);
    process.exit(1);
  }

  const fileContent = getNodeFileContent(nodePath);
  const related = getRelated(nodePath);
  const firstHopPaths = related.map(r => r.path);
  const secondHop = get2ndHop(nodePath, firstHopPaths);
  const logEntries = getRecentLogEntries(nodePath, LOG_DAYS);

  let out = `# Briefing: ${node.title}\n\n`;
  out += `**Path:** ${node.path}  \n`;
  out += `**Type:** ${node.type} | **Status:** ${node.status || "—"} | **Created:** ${node.created || "—"}  \n`;
  out += `**Updated:** ${node.updated || "—"} (${staleness(node.updated)})  \n`;
  out += `**Tags:** ${node.tags || "—"}\n\n`;

  // Full content
  out += `---\n\n## Full Content\n\n`;
  if (fileContent) {
    // Strip frontmatter for cleaner reading
    const body = fileContent.replace(/^---\n[\s\S]*?\n---\n*/, "").trim();
    out += body + "\n\n";
  }

  // 1-hop relations
  if (related.length > 0) {
    out += `---\n\n## Direct Relations (${related.length})\n\n`;
    for (const r of related) {
      const dir = r.derived ? "←" : "→";
      out += `- ${dir} **${r.title}** (\`${r.path}\`) [${r.rel_type}]\n`;
      out += `  Type: ${r.type} | Status: ${r.status || "—"} | Updated: ${staleness(r.updated)}\n`;
      if (r.tags) out += `  Tags: ${r.tags}\n`;
    }
    out += "\n";
  }

  // 2nd-hop relations
  if (secondHop.length > 0) {
    out += `---\n\n## 2nd-Hop Relations (${secondHop.length})\n\n`;
    for (const r of secondHop) {
      out += `- **${r.title}** (\`${r.path}\`) via ${r.via} [${r.rel_type}]\n`;
    }
    out += "\n";
  }

  // Recent log entries
  if (logEntries.length > 0) {
    out += `---\n\n## Recent Activity (last ${LOG_DAYS} days)\n\n`;
    for (const e of logEntries) {
      out += `- [${e.date}] ${e.line}\n`;
    }
    out += "\n";
  } else {
    out += `---\n\n## Recent Activity\n\n_No log entries in last ${LOG_DAYS} days._\n\n`;
  }

  return out;
}

// --- Briefing by topic ---

function briefTopic(query) {
  let results;
  try {
    const escaped = `"${query.replace(/"/g, '""')}"`;
    results = db.prepare(`
      SELECT path, title, tags FROM nodes_fts WHERE nodes_fts MATCH ? LIMIT 10
    `).all(escaped);
  } catch {
    results = db.prepare(`
      SELECT path, title, tags FROM nodes WHERE body LIKE ? OR title LIKE ? LIMIT 10
    `).all(`%${query}%`, `%${query}%`);
  }

  if (results.length === 0) {
    console.error(`No nodes found for topic: "${query}"`);
    process.exit(1);
  }

  let out = `# Topic Briefing: "${query}"\n\n`;
  out += `Found ${results.length} relevant node(s).\n\n`;

  for (const result of results) {
    out += `---\n\n`;
    out += briefNode(result.path);
  }

  return out;
}

// --- Main ---

if (args.includes("--node")) {
  const nodePath = getArg("--node");
  console.log(briefNode(nodePath));
} else if (args.includes("--topic")) {
  const query = getArg("--topic");
  console.log(briefTopic(query));
} else {
  console.log(`Usage:
  --node <path>           Briefing for a specific node
  --topic <query>         Search-based briefing (FTS)
  --days <N>              Log lookback window (default: 7)`);
}

db.close();
