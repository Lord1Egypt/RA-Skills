#!/usr/bin/env node
/**
 * bump-version.js — Calculate next semver version based on conventional commits.
 *
 * Usage:
 *   node bump-version.js [--type=patch|minor|major] [--dry-run]
 *
 * Without --type, auto-detects from commits since last tag.
 * Outputs the new version string to stdout.
 */

import { execSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "../..");
const PKG_PATH = join(ROOT, "package.json");

// ---------------------------------------------------------------------------
// Conventional commit parsing
// ---------------------------------------------------------------------------

const COMMIT_RE = /^(\w+)(?:\(([^)]+)\))?(!)?:\s+(.+)$/;

const BUMP_MAP = {
  feat: "minor",
  fix: "patch",
  perf: "patch",
  refactor: "patch",
  docs: "patch",
  chore: "patch",
  ci: "patch",
  test: "patch",
  style: "patch",
  build: "patch",
};

function parseCommits(sinceTag) {
  const range = sinceTag ? `${sinceTag}..HEAD` : "HEAD";
  let log;
  try {
    log = execSync(`git log ${range} --pretty=format:"%s|||%b" --no-merges`, {
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
      const [subject, body = ""] = line.split("|||");
      const m = subject.match(COMMIT_RE);
      if (!m) return null;
      return {
        type: m[1],
        scope: m[2] || null,
        breaking: !!m[3] || body.includes("BREAKING CHANGE"),
        subject: m[4],
        raw: subject,
      };
    })
    .filter(Boolean);
}

function calculateBump(commits, forceType) {
  if (forceType) return forceType;

  let bump = null;
  for (const c of commits) {
    if (c.breaking) return "major";
    const mapped = BUMP_MAP[c.type];
    if (mapped === "minor") bump = "minor";
    if (!bump && mapped === "patch") bump = "patch";
  }
  return bump || "patch";
}

function bumpSemver(current, type) {
  const [major, minor, patch] = current.split(".").map(Number);
  switch (type) {
    case "major":
      return `${major + 1}.0.0`;
    case "minor":
      return `${major}.${minor + 1}.0`;
    case "patch":
      return `${major}.${minor}.${patch + 1}`;
    default:
      throw new Error(`Unknown bump type: ${type}`);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

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

function getCurrentVersion() {
  const pkg = JSON.parse(readFileSync(PKG_PATH, "utf-8"));
  return pkg.version;
}

function updatePackageVersion(newVersion) {
  const pkg = JSON.parse(readFileSync(PKG_PATH, "utf-8"));
  pkg.version = newVersion;
  writeFileSync(PKG_PATH, JSON.stringify(pkg, null, 2) + "\n");
}

// CLI
const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const forceType = args.find((a) => a.startsWith("--type="))?.split("=")[1];

const lastTag = getLastTag();
const currentVersion = getCurrentVersion();
const commits = parseCommits(lastTag);
const bumpType = calculateBump(commits, forceType);
const newVersion = bumpSemver(currentVersion, bumpType);

if (dryRun) {
  console.log(`[bump-version] Current: v${currentVersion}`);
  console.log(`[bump-version] Bump type: ${bumpType}`);
  console.log(`[bump-version] New version: v${newVersion}`);
  console.log(`[bump-version] Commits since ${lastTag || "beginning"}: ${commits.length}`);
  for (const c of commits) {
    console.log(`  ${c.breaking ? "⚠️" : "  "} ${c.raw}`);
  }
} else {
  updatePackageVersion(newVersion);
  console.log(newVersion);
}
