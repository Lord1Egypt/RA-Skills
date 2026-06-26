#!/usr/bin/env node

/**
 * suggest-backfill.js
 *
 * Scoped backfill: finds candidate connections via four strategies:
 *   1. Shared tags (SQLite tag joins)
 *   2. FTS5 title/keyword match
 *   3. Log co-references
 *   4. QMD semantic similarity (if qmd is installed)
 *
 * Uses SQLite index (memory.db) for structural lookups.
 * Uses QMD (optional) for semantic similarity search.
 *
 * Usage:
 *   node ~/memory/scripts/suggest-backfill.js                    # default min-score 2
 *   node ~/memory/scripts/suggest-backfill.js --min-score 3
 *   node ~/memory/scripts/suggest-backfill.js --scope recent     # only nodes modified in last 7 days
 *   node ~/memory/scripts/suggest-backfill.js --scope node:projects/flowmind  # specific node
 *   node ~/memory/scripts/suggest-backfill.js --no-qmd           # skip semantic search
 *
 * Requires Node.js 22+ (node:sqlite built-in). QMD is optional (npm i -g @tobilu/qmd).
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const LOG_DIR = path.join(MEMORY_ROOT, "log");
const INDEX_DIR = path.join(MEMORY_ROOT, "indexes");
const DB_PATH = path.join(INDEX_DIR, "memory.db");
const BACKFILL_DIR = path.join(MEMORY_ROOT, "backfill");
const HISTORY_FILE = path.join(BACKFILL_DIR, "history.md");
const SUGGESTIONS_FILE = path.join(BACKFILL_DIR, "suggestions.md");

// Parse args
const args = process.argv.slice(2);
const MIN_SCORE = parseInt(args[args.indexOf("--min-score") + 1] || "2", 10);
const SCOPE = args.includes("--scope") ? args[args.indexOf("--scope") + 1] : "all";
const NO_QMD = args.includes("--no-qmd");

// --- QMD semantic search (optional) ---

function isQmdAvailable() {
  if (NO_QMD) return false;
  try {
    execSync("qmd status", { stdio: "pipe", timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

function qmdSemanticSearch(query, limit = 10) {
  try {
    const result = execSync(
      `qmd vsearch ${JSON.stringify(query)} -c memory-graph --json -n ${limit}`,
      { stdio: ["pipe", "pipe", "pipe"], timeout: 30000 }
    );
    const parsed = JSON.parse(result.toString());
    // Extract graph paths from results — QMD returns collection-relative paths
    return (parsed.results || parsed || [])
      .filter(r => r.score >= 0.4)
      .map(r => {
        // QMD returns paths like "qmd://memory-graph/concepts/autonomy.md" or "concepts/autonomy.md"
        let p = (r.path || r.file || "");
        // Strip qmd://collection-name/ prefix
        p = p.replace(/^qmd:\/\/[^/]+\//, "");
        // Strip .md extension
        p = p.replace(/\.md$/, "");
        return { path: p, score: r.score };
      })
      .filter(r => r.path);
  } catch {
    return [];
  }
}

// --- Load rejected suggestions ---

function loadRejected() {
  const rejected = new Set();
  try {
    const content = fs.readFileSync(HISTORY_FILE, "utf-8");
    const re = /REJECTED.*?(\S+\/\S+)\s*↔\s*(\S+\/\S+)/g;
    let m;
    while ((m = re.exec(content)) !== null) {
      rejected.add(`${m[1]}|${m[2]}`);
      rejected.add(`${m[2]}|${m[1]}`);
    }
  } catch {}
  return rejected;
}

// --- Log co-references ---

function findLogCoRefs() {
  const coRefs = {};
  try {
    for (const file of fs.readdirSync(LOG_DIR).filter(f => f.endsWith(".md"))) {
      for (const line of fs.readFileSync(path.join(LOG_DIR, file), "utf-8").split("\n")) {
        const m = line.match(/\{ref:\s*([^}]+)\}/);
        if (!m) continue;
        const refs = m[1].split(",").map(s => s.trim()).filter(Boolean);
        for (let i = 0; i < refs.length; i++)
          for (let j = i + 1; j < refs.length; j++) {
            const key = [refs[i], refs[j]].sort().join("|");
            coRefs[key] = (coRefs[key] || 0) + 1;
          }
      }
    }
  } catch {}
  return coRefs;
}

// --- Main ---

function main() {
  if (!fs.existsSync(DB_PATH)) {
    console.error("Missing memory.db — run rebuild-indexes.js first");
    process.exit(1);
  }

  const db = new DatabaseSync(DB_PATH);
  const rejected = loadRejected();
  const coRefs = findLogCoRefs();

  // Determine scope: which nodes to find suggestions FOR
  let scopeNodes;
  if (SCOPE === "recent") {
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    scopeNodes = db.prepare("SELECT path, title, tags FROM nodes WHERE mtime_ms > ?").all(sevenDaysAgo);
  } else if (SCOPE.startsWith("node:")) {
    const nodePath = SCOPE.slice(5);
    scopeNodes = db.prepare("SELECT path, title, tags FROM nodes WHERE path = ?").all(nodePath);
  } else {
    scopeNodes = db.prepare("SELECT path, title, tags FROM nodes").all();
  }

  if (scopeNodes.length === 0) {
    console.log("No nodes in scope.");
    return;
  }

  // Get all existing relations as a set for fast lookup
  const existingRels = new Set();
  for (const r of db.prepare("SELECT source, target FROM relations").all()) {
    existingRels.add(`${r.source}|${r.target}`);
    existingRels.add(`${r.target}|${r.source}`);
  }

  // For each scope node, find candidates via:
  // 1. Shared tags (from tags table)
  // 2. FTS title/keyword match
  // 3. Log co-references

  const candidateScores = new Map(); // "a|b" → { score, reasons }

  const tagNeighborsStmt = db.prepare(`
    SELECT DISTINCT t2.node_path
    FROM tags t1
    JOIN tags t2 ON t1.tag = t2.tag AND t1.node_path != t2.node_path
    WHERE t1.node_path = ?
  `);

  const sharedTagsStmt = db.prepare(`
    SELECT t1.tag
    FROM tags t1
    JOIN tags t2 ON t1.tag = t2.tag
    WHERE t1.node_path = ? AND t2.node_path = ?
  `);

  const titleSearchStmt = db.prepare(`
    SELECT path FROM nodes_fts WHERE nodes_fts MATCH ? AND path != ?
  `);

  for (const node of scopeNodes) {
    const a = node.path;

    // 1. Tag-based candidates
    const tagNeighbors = tagNeighborsStmt.all(a);
    for (const { node_path: b } of tagNeighbors) {
      if (existingRels.has(`${a}|${b}`) || rejected.has(`${a}|${b}`)) continue;
      const key = [a, b].sort().join("|");
      if (!candidateScores.has(key)) candidateScores.set(key, { a: key.split("|")[0], b: key.split("|")[1], score: 0, reasons: [] });
      const entry = candidateScores.get(key);
      // Only add tag score once per pair
      if (!entry.reasons.some(r => r.startsWith("shared tags"))) {
        const shared = sharedTagsStmt.all(a, b).map(r => r.tag);
        if (shared.length > 0) {
          entry.score += shared.length;
          entry.reasons.push(`shared tags: ${shared.join(", ")}`);
        }
      }
    }

    // 2. FTS-based candidates (search for this node's title in other nodes)
    const title = node.title || "";
    if (title.length > 3) {
      try {
        // Escape FTS5 special characters
        const escaped = `"${title.replace(/"/g, '""')}"`;
        const ftsResults = titleSearchStmt.all(escaped, a);
        for (const { path: b } of ftsResults) {
          if (existingRels.has(`${a}|${b}`) || rejected.has(`${a}|${b}`)) continue;
          const key = [a, b].sort().join("|");
          if (!candidateScores.has(key)) candidateScores.set(key, { a: key.split("|")[0], b: key.split("|")[1], score: 0, reasons: [] });
          const entry = candidateScores.get(key);
          if (!entry.reasons.some(r => r.includes(`"${title}"`))) {
            entry.score += 2;
            entry.reasons.push(`"${title}" mentioned in ${b}`);
          }
        }
      } catch {
        // FTS query might fail on some titles — skip silently
      }
    }
  }

  // 3. QMD semantic similarity (if available)
  const useQmd = isQmdAvailable();
  if (useQmd) {
    for (const node of scopeNodes) {
      const a = node.path;
      const tags = node.tags ? node.tags.replace(/,\s*/g, " ") : "";
      const query = `${node.title || ""} ${tags}`.trim();
      if (query.length < 3) continue;

      const results = qmdSemanticSearch(query);
      for (const { path: b, score } of results) {
        if (b === a) continue;
        if (existingRels.has(`${a}|${b}`) || rejected.has(`${a}|${b}`)) continue;
        const key = [a, b].sort().join("|");
        if (!candidateScores.has(key)) candidateScores.set(key, { a: key.split("|")[0], b: key.split("|")[1], score: 0, reasons: [] });
        const entry = candidateScores.get(key);
        if (!entry.reasons.some(r => r.startsWith("semantic similarity"))) {
          const bonus = score >= 0.7 ? 3 : score >= 0.5 ? 2 : 1;
          entry.score += bonus;
          entry.reasons.push(`semantic similarity via QMD (${Math.round(score * 100)}%)`);
        }
      }
    }
  }

  // 4. Log co-reference candidates
  for (const [key, count] of Object.entries(coRefs)) {
    const [a, b] = key.split("|");
    if (existingRels.has(`${a}|${b}`) || rejected.has(`${a}|${b}`)) continue;
    if (!candidateScores.has(key)) candidateScores.set(key, { a, b, score: 0, reasons: [] });
    const entry = candidateScores.get(key);
    entry.score += count;
    entry.reasons.push(`co-referenced ${count}x in activity logs`);
  }

  // Filter by min score and sort
  const suggestions = [...candidateScores.values()]
    .filter(s => s.score >= MIN_SCORE)
    .map(s => ({ ...s, confidence: s.score >= 4 ? "high" : s.score >= 2 ? "medium" : "low" }))
    .sort((x, y) => y.score - x.score);

  // Write output
  const date = new Date().toISOString().split("T")[0];
  let md = `# Backfill Suggestions — ${date}\n\n`;
  md += `Generated by suggest-backfill.js (min score: ${MIN_SCORE}, scope: ${SCOPE}, semantic: ${useQmd ? "on" : "off"})\n\n`;

  if (suggestions.length === 0) {
    md += "_No new suggestions._\n";
  } else {
    for (const level of ["high", "medium", "low"]) {
      const group = suggestions.filter(s => s.confidence === level);
      if (group.length === 0) continue;
      md += `## ${level.charAt(0).toUpperCase() + level.slice(1)} Confidence\n\n`;
      for (const s of group) {
        md += `- **${s.a}** ↔ **${s.b}** (score: ${s.score})\n`;
        for (const r of s.reasons) md += `  - ${r}\n`;
        md += `  - [ ] Accept  [ ] Reject\n\n`;
      }
    }
  }

  fs.mkdirSync(BACKFILL_DIR, { recursive: true });
  fs.writeFileSync(SUGGESTIONS_FILE, md);
  console.log(`✓ ${suggestions.length} suggestion(s) — scope: ${SCOPE}, semantic: ${useQmd ? "on" : "off"}`);

  db.close();
}

main();
