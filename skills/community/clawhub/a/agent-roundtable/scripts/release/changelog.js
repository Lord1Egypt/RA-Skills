#!/usr/bin/env node
/**
 * changelog.js — Generate CHANGELOG.md from conventional commits.
 *
 * Follows the "Keep a Changelog" format: https://keepachangelog.com/
 *
 * Usage:
 *   node changelog.js [--version=X.Y.Z] [--dry-run]
 *
 * Outputs the new changelog entry to stdout (or writes CHANGELOG.md).
 */

import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "../..");
const CHANGELOG_PATH = join(ROOT, "CHANGELOG.md");

// ---------------------------------------------------------------------------
// Commit parsing (same as bump-version.js)
// ---------------------------------------------------------------------------

const COMMIT_RE = /^(\w+)(?:\(([^)]+)\))?(!)?:\s+(.+)$/;

const TYPE_LABELS = {
  feat: "✨ Features",
  fix: "🐛 Bug Fixes",
  perf: "⚡ Performance",
  refactor: "♻️ Refactoring",
  docs: "📝 Documentation",
  chore: "🔧 Chores",
  ci: "💚 CI",
  test: "✅ Tests",
  style: "💄 Style",
  build: "📦 Build",
};

function parseCommits(sinceTag) {
  const range = sinceTag ? `${sinceTag}..HEAD` : "HEAD";
  let log;
  try {
    log = execSync(`git log ${range} --pretty=format:"%H|||%s|||%b|||%aI" --no-merges`, {
      cwd: ROOT,
      encoding: "utf-8",
    }).trim();
  } catch {
    return [];
  }
  if (!log) return [];

  return log
    .split("\n")
    .map((line) => {
      const [hash, subject, body, date] = line.split("|||");
      if (!subject) return null;
      const m = subject.match(COMMIT_RE);
      if (!m) return null;
      return {
        hash: hash.slice(0, 7),
        type: m[1],
        scope: m[2] || null,
        breaking: !!m[3] || (body || "").includes("BREAKING CHANGE"),
        subject: m[4],
        date: date?.slice(0, 10) || new Date().toISOString().slice(0, 10),
      };
    })
    .filter(Boolean);
}

function getLastTag() {
  try {
    return execSync("git describe --tags --abbrev=0", {
      cwd: ROOT,
      encoding: "utf-8",
    }).trim();
  } catch {
    return null;
  }
}

function groupByType(commits) {
  const groups = {};
  for (const c of commits) {
    const label = TYPE_LABELS[c.type] || `🔖 ${c.type}`;
    if (!groups[label]) groups[label] = [];
    groups[label].push(c);
  }
  return groups;
}

function formatEntry(version, date, commits) {
  const lines = [];
  lines.push(`## [${version}] - ${date}`);
  lines.push("");

  // Breaking changes first
  const breaking = commits.filter((c) => c.breaking);
  if (breaking.length > 0) {
    lines.push("### ⚠️ BREAKING CHANGES");
    lines.push("");
    for (const c of breaking) {
      const scope = c.scope ? `**${c.scope}:** ` : "";
      lines.push(`- ${scope}${c.subject} (\`${c.hash}\`)`);
    }
    lines.push("");
  }

  // Group by type
  const groups = groupByType(commits.filter((c) => !c.breaking));
  for (const [label, items] of Object.entries(groups)) {
    lines.push(`### ${label}`);
    lines.push("");
    for (const c of items) {
      const scope = c.scope ? `**${c.scope}:** ` : "";
      lines.push(`- ${scope}${c.subject} (\`${c.hash}\`)`);
    }
    lines.push("");
  }

  return lines.join("\n");
}

function mergeWithExisting(newEntry) {
  if (!existsSync(CHANGELOG_PATH)) {
    return `# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/).\n\n${newEntry}`;
  }

  const existing = readFileSync(CHANGELOG_PATH, "utf-8");
  // Insert after the header (first ## line)
  const firstEntryIdx = existing.indexOf("\n## ");
  if (firstEntryIdx === -1) {
    return existing.trimEnd() + "\n\n" + newEntry;
  }
  return (
    existing.slice(0, firstEntryIdx + 1) +
    newEntry +
    "\n" +
    existing.slice(firstEntryIdx + 1)
  );
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const forceVersion = args.find((a) => a.startsWith("--version="))?.split("=")[1];

const lastTag = getLastTag();
const commits = parseCommits(lastTag);

if (commits.length === 0) {
  console.error("[changelog] No commits found since last tag.");
  process.exit(1);
}

const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf-8"));
const version = forceVersion || pkg.version;
const date = new Date().toISOString().slice(0, 10);
const entry = formatEntry(version, date, commits);

if (dryRun) {
  console.log("[changelog] Dry run — would add:\n");
  console.log(entry);
} else {
  const full = mergeWithExisting(entry);
  writeFileSync(CHANGELOG_PATH, full);
  console.log(`[changelog] CHANGELOG.md updated for v${version}`);
}
