#!/usr/bin/env node

/**
 * promote.js — Discover recurring topics in logs that deserve their own nodes.
 *
 * Scans log files for entities/topics mentioned 3+ times that don't have
 * existing graph nodes. Suggests node creation with pre-filled templates.
 *
 * Usage:
 *   node ~/memory/scripts/promote.js
 *   node ~/memory/scripts/promote.js --min 5         # minimum mentions (default: 3)
 *   node ~/memory/scripts/promote.js --days 30       # lookback window (default: all)
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const LOG_DIR = path.join(MEMORY_ROOT, "log");
const GRAPH_DIR = path.join(MEMORY_ROOT, "graph");
const DB_PATH = path.join(MEMORY_ROOT, "indexes", "memory.db");

const args = process.argv.slice(2);

function getArg(flag) {
  const idx = args.indexOf(flag);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

const MIN_MENTIONS = parseInt(getArg("--min") || "3", 10);
const DAYS = getArg("--days") ? parseInt(getArg("--days"), 10) : null;

// --- File walker for graph ---

function walkDir(dir, base = dir) {
  const paths = new Set();
  try {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, item.name);
      if (item.isDirectory()) {
        for (const p of walkDir(full, base)) paths.add(p);
      } else if (item.isFile() && item.name.endsWith(".md")) {
        paths.add(path.relative(base, full).replace(/\.md$/, ""));
      }
    }
  } catch {}
  return paths;
}

// --- Extract candidate entities from log text ---

function extractCandidates(text) {
  const candidates = new Set();

  // Extract {ref: ...} references
  const refMatches = text.matchAll(/\{ref:\s*([^}]+)\}/g);
  for (const m of refMatches) {
    for (const ref of m[1].split(",").map(s => s.trim()).filter(Boolean)) {
      candidates.add(ref);
    }
  }

  // Extract capitalized multi-word phrases (potential proper nouns / project names)
  // e.g., "Discussed Flowmind architecture" → "Flowmind"
  const wordMatches = text.matchAll(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/g);
  for (const m of wordMatches) {
    const phrase = m[1].trim();
    // Skip common words
    if (["The", "This", "That", "What", "When", "Where", "How", "Why", "Who",
         "New", "No", "Yes", "Not", "All", "Any", "Some", "Many", "Few",
         "After", "Before", "During", "About", "Into",
         "Discussed", "Created", "Updated", "Added", "Removed", "Fixed",
         "Built", "Designed", "Implemented", "Refactored", "Deployed",
         "Decision", "Session", "Started", "Upgraded", "Integrated",
         "Scaffolded", "Validated", "Generated", "Moved", "Wired"].includes(phrase)) continue;
    candidates.add(phrase.toLowerCase());
  }

  // Extract [agent] names — skip these
  // Extract quoted strings as potential topics
  const quoteMatches = text.matchAll(/"([^"]{3,30})"/g);
  for (const m of quoteMatches) {
    candidates.add(m[1].toLowerCase());
  }

  return candidates;
}

function main() {
  // Get existing node paths
  const existingNodes = walkDir(GRAPH_DIR);

  // Also check existing node titles via SQLite if available
  const existingTitles = new Set();
  if (fs.existsSync(DB_PATH)) {
    const db = new DatabaseSync(DB_PATH);
    const rows = db.prepare("SELECT path, title FROM nodes").all();
    for (const r of rows) {
      existingTitles.add(r.title.toLowerCase());
      existingNodes.add(r.path);
    }
    db.close();
  }

  // Scan logs
  let logFiles;
  try {
    logFiles = fs.readdirSync(LOG_DIR).filter(f => f.endsWith(".md")).sort();
  } catch {
    console.log("No log directory found.");
    return;
  }

  // Filter by days if specified
  if (DAYS) {
    const cutoff = new Date(Date.now() - DAYS * 24 * 60 * 60 * 1000);
    logFiles = logFiles.filter(f => {
      const dateStr = f.replace(".md", "");
      return new Date(dateStr) >= cutoff;
    });
  }

  // Count mentions
  const mentions = new Map(); // candidate → { count, logDates }

  for (const file of logFiles) {
    const dateStr = file.replace(".md", "");
    const content = fs.readFileSync(path.join(LOG_DIR, file), "utf-8");

    for (const line of content.split("\n")) {
      if (!line.trim() || line.startsWith("#")) continue;

      const candidates = extractCandidates(line);
      for (const candidate of candidates) {
        // Skip if already a node
        const normalized = candidate.toLowerCase();
        if (existingNodes.has(candidate)) continue;
        // Check if the candidate matches any existing node path segment
        let found = false;
        for (const nodePath of existingNodes) {
          if (nodePath.endsWith("/" + normalized) || nodePath === normalized) {
            found = true;
            break;
          }
        }
        if (found) continue;
        if (existingTitles.has(normalized)) continue;

        if (!mentions.has(normalized)) mentions.set(normalized, { count: 0, dates: new Set(), original: candidate });
        const entry = mentions.get(normalized);
        entry.count++;
        entry.dates.add(dateStr);
      }
    }
  }

  // Filter to those with enough mentions
  const promotable = [...mentions.entries()]
    .filter(([, v]) => v.count >= MIN_MENTIONS)
    .sort((a, b) => b[1].count - a[1].count);

  if (promotable.length === 0) {
    console.log(`✓ No topics found with ${MIN_MENTIONS}+ mentions without existing nodes.`);
    return;
  }

  console.log(`\nPromotion Suggestions (${promotable.length} topics with ${MIN_MENTIONS}+ mentions):\n`);

  for (const [name, data] of promotable) {
    const dates = [...data.dates].sort().join(", ");
    console.log(`  ${data.original || name} — ${data.count} mentions across ${data.dates.size} day(s)`);
    console.log(`    Dates: ${dates}`);
    console.log(`    Suggested node: graph/concepts/${name.replace(/\s+/g, "-")}.md`);
    console.log(`    Template:`);
    console.log(`      ---`);
    console.log(`      type: concept`);
    console.log(`      created: ${new Date().toISOString().split("T")[0]}`);
    console.log(`      updated: ${new Date().toISOString().split("T")[0]}`);
    console.log(`      tags: []`);
    console.log(`      relations: []`);
    console.log(`      ---`);
    console.log(`      # ${data.original || name}`);
    console.log();
  }
}

main();
