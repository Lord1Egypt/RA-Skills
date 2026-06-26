#!/usr/bin/env node

/**
 * commit.js — Auto-commit changes in ~/memory/.
 *
 * Stages changes in graph/ and log/, auto-commits with a descriptive message.
 * Does NOT auto-push.
 *
 * Usage:
 *   node ~/memory/scripts/commit.js
 *   node ~/memory/scripts/commit.js --message "custom message"
 *
 * Requires Node.js 22+. No external dependencies.
 */

const { execSync } = require("child_process");
const path = require("path");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const args = process.argv.slice(2);

function getArg(flag) {
  const idx = args.indexOf(flag);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

function run(cmd) {
  return execSync(cmd, { cwd: MEMORY_ROOT, encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] }).trim();
}

function main() {
  // Check if it's a git repo
  try {
    run("git rev-parse --git-dir");
  } catch {
    console.error("Not a git repo. Run 'git init' in ~/memory/ first.");
    process.exit(1);
  }

  // Stage graph/ and log/ changes
  try { run("git add graph/"); } catch {}
  try { run("git add log/"); } catch {}
  try { run("git add backfill/history.md"); } catch {}
  try { run("git add README.md"); } catch {}

  // Check if there's anything staged to commit
  let staged;
  try {
    staged = run("git diff --cached --name-only");
  } catch {
    staged = "";
  }

  if (!staged.trim()) {
    console.log("✓ Nothing to commit — working tree clean.");
    return;
  }

  // Build descriptive message from staged changes
  const customMsg = getArg("--message");
  let commitMsg;

  if (customMsg) {
    commitMsg = customMsg;
  } else {
    let status;
    try { status = run("git diff --cached --name-status"); } catch { status = ""; }
    const lines = status.split("\n").filter(Boolean);
    const added = [];
    const modified = [];
    const deleted = [];

    for (const line of lines) {
      const parts = line.split("\t");
      if (parts.length < 2) continue;
      const code = parts[0].trim();
      const file = parts[1].trim();
      // Only describe graph/ and log/ changes in the message
      if (!file.startsWith("graph/") && !file.startsWith("log/")) continue;
      const name = file.replace(/\.md$/, "").replace(/^(graph|log)\//, "");
      if (code === "A") added.push(name);
      else if (code === "M") modified.push(name);
      else if (code === "D") deleted.push(name);
    }

    const msgParts = [];
    if (added.length > 0) msgParts.push(`add: ${added.join(", ")}`);
    if (modified.length > 0) msgParts.push(`update: ${modified.join(", ")}`);
    if (deleted.length > 0) msgParts.push(`remove: ${deleted.join(", ")}`);

    commitMsg = msgParts.length > 0 ? msgParts.join("; ") : "memory update";
  }

  // Also stage any other tracked changes (backfill/, indexes/ are gitignored typically)
  try {
    run(`git commit -m "${commitMsg.replace(/"/g, '\\"')}"`);
    console.log(`✓ Committed: ${commitMsg}`);
  } catch (e) {
    console.error(`Commit failed: ${e.message}`);
    process.exit(1);
  }
}

main();
