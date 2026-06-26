#!/usr/bin/env node

/**
 * lint.js — Validate memory graph nodes.
 *
 * Checks:
 *   - Missing required fields (type, created)
 *   - Broken relation targets (pointing to nodes that don't exist)
 *   - Orphan nodes (zero relations)
 *   - Duplicate/near-duplicate titles
 *   - Inconsistent relation type naming
 *   - Non-standard relation types (info-level)
 *
 * Usage:
 *   node ~/memory/scripts/lint.js
 *   node ~/memory/scripts/lint.js --fix   # auto-fix what can be fixed (adds updated field)
 *
 * Exit code 0 if only warnings/info, 1 if errors.
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const GRAPH_DIR = path.join(MEMORY_ROOT, "graph");
const FIX = process.argv.includes("--fix");

// Standard relation type taxonomy
const STANDARD_TYPES = new Set([
  // Structural
  "uses", "built-with", "part-of", "contains",
  // Ownership
  "creator", "owner", "maintainer",
  // Conceptual
  "related-to", "inspired-by", "alternative-to", "core-concept-of", "core-value-of",
  // Temporal
  "led-to", "preceded-by", "evolved-into",
  // Contextual
  "home-of", "lives-in", "works-at",
  // Common extras
  "used-in", "powers", "built-on", "core-concept", "core-value",
]);

// --- YAML frontmatter parser (same as rebuild-indexes.js) ---

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return { meta: {}, body: content, raw: null };
  return { meta: parseYaml(match[1]), body: content.slice(match[0].length).trim(), raw: match[1] };
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
  try {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, item.name);
      if (item.isDirectory()) entries.push(...walkDir(full, base));
      else if (item.isFile() && item.name.endsWith(".md")) {
        entries.push({
          fullPath: full,
          relPath: path.relative(base, full).replace(/\.md$/, ""),
        });
      }
    }
  } catch {}
  return entries;
}

// --- Similarity for near-duplicate detection ---

function normalize(str) {
  return str.toLowerCase().replace(/[^a-z0-9]/g, "");
}

// --- Main ---

function main() {
  const files = walkDir(GRAPH_DIR);
  const allPaths = new Set(files.map(f => f.relPath));
  const issues = []; // { severity, path, message }

  // Collect data for cross-node checks
  const titles = new Map(); // normalized → [{ path, original }]
  const relationTypes = new Map(); // type → count
  const nodeRelationCounts = new Map(); // path → count

  // Initialize relation counts
  for (const f of files) nodeRelationCounts.set(f.relPath, 0);

  for (const { fullPath, relPath } of files) {
    const content = fs.readFileSync(fullPath, "utf-8");
    const { meta, body, raw } = parseFrontmatter(content);

    // Check required fields
    if (!meta.type) {
      issues.push({ severity: "error", path: relPath, message: "Missing required field: type" });
    }
    if (!meta.created) {
      issues.push({ severity: "error", path: relPath, message: "Missing required field: created" });
    }

    // Check for 'updated' field (info if missing)
    if (!meta.updated) {
      issues.push({ severity: "info", path: relPath, message: "Missing optional field: updated (recommended for temporal tracking)" });
      // Auto-fix: add updated field based on file mtime
      if (FIX && raw) {
        const stat = fs.statSync(fullPath);
        const updated = new Date(stat.mtimeMs).toISOString().split("T")[0];
        const newFrontmatter = raw + `\nupdated: ${updated}`;
        const newContent = content.replace(raw, newFrontmatter);
        fs.writeFileSync(fullPath, newContent);
        issues.push({ severity: "info", path: relPath, message: `Fixed: added updated: ${updated}` });
      }
    }

    // Title dedup check
    const titleMatch = body.match(/^#\s+(.+)/m);
    const title = titleMatch ? titleMatch[1].trim() : relPath.split("/").pop();
    const norm = normalize(title);
    if (!titles.has(norm)) titles.set(norm, []);
    titles.get(norm).push({ path: relPath, original: title });

    // Relations checks
    const rels = Array.isArray(meta.relations) ? meta.relations : [];
    for (const rel of rels) {
      if (!rel || !rel.to) continue;

      // Broken target
      if (!allPaths.has(rel.to)) {
        issues.push({ severity: "error", path: relPath, message: `Broken relation target: ${rel.to} does not exist` });
      }

      // Track relation type
      if (rel.type) {
        relationTypes.set(rel.type, (relationTypes.get(rel.type) || 0) + 1);
      }

      // Count relations for orphan detection
      nodeRelationCounts.set(relPath, (nodeRelationCounts.get(relPath) || 0) + 1);
      if (allPaths.has(rel.to)) {
        nodeRelationCounts.set(rel.to, (nodeRelationCounts.get(rel.to) || 0) + 1);
      }
    }
  }

  // Check for duplicate/near-duplicate titles
  for (const [norm, entries] of titles) {
    if (entries.length > 1) {
      const paths = entries.map(e => e.path).join(", ");
      issues.push({ severity: "warning", path: entries[0].path, message: `Duplicate/near-duplicate title "${entries[0].original}" also at: ${paths}` });
    }
  }

  // Check for orphan nodes
  for (const [nodePath, count] of nodeRelationCounts) {
    if (count === 0) {
      issues.push({ severity: "warning", path: nodePath, message: "Orphan node: zero relations (incoming or outgoing)" });
    }
  }

  // Check for non-standard relation types
  for (const [type, count] of relationTypes) {
    if (!STANDARD_TYPES.has(type)) {
      issues.push({ severity: "info", path: "(global)", message: `Non-standard relation type "${type}" (used ${count}x) — consider using a standard type` });
    }
  }

  // Check for similar relation type names (potential consolidation)
  const typeNames = [...relationTypes.keys()].sort();
  for (let i = 0; i < typeNames.length; i++) {
    for (let j = i + 1; j < typeNames.length; j++) {
      const a = typeNames[i];
      const b = typeNames[j];
      // Simple similarity: one is a suffix/prefix of the other, or they differ by only a hyphen/plural
      const aNorm = a.replace(/-/g, "").toLowerCase();
      const bNorm = b.replace(/-/g, "").toLowerCase();
      if (aNorm === bNorm || aNorm + "s" === bNorm || bNorm + "s" === aNorm ||
          aNorm.includes(bNorm) || bNorm.includes(aNorm)) {
        if (a !== b) {
          issues.push({ severity: "info", path: "(global)", message: `Similar relation types: "${a}" and "${b}" — consider consolidating` });
        }
      }
    }
  }

  // Sort issues by severity
  const severityOrder = { error: 0, warning: 1, info: 2 };
  issues.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);

  // Report
  const errors = issues.filter(i => i.severity === "error");
  const warnings = issues.filter(i => i.severity === "warning");
  const infos = issues.filter(i => i.severity === "info");

  if (issues.length === 0) {
    console.log("✓ No issues found.");
  } else {
    console.log(`\nLint Results: ${errors.length} error(s), ${warnings.length} warning(s), ${infos.length} info\n`);
    for (const issue of issues) {
      const icon = issue.severity === "error" ? "✗" : issue.severity === "warning" ? "⚠" : "ℹ";
      console.log(`  ${icon} [${issue.severity}] ${issue.path}: ${issue.message}`);
    }
    console.log();
  }

  // Exit code
  process.exit(errors.length > 0 ? 1 : 0);
}

main();
