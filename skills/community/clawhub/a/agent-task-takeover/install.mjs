#!/usr/bin/env node
/**
 * agent-task-takeover installer.
 *
 * Copies the skill folder (SKILL.md + references/ + scripts/ + tests/) into
 * the conventional agent skills directory so any agent that scans
 * ~/.agents/skills picks it up:
 *
 *   npx agent-task-takeover            # install / refresh
 *   npx agent-task-takeover --where    # print the target dir and exit
 *
 * Pure stdlib Node >= 18; never touches anything outside the target dir.
 */
import { cpSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SKILL_NAME = "agent-task-takeover";
const SRC = dirname(fileURLToPath(import.meta.url));
const TARGET = join(homedir(), ".agents", "skills", SKILL_NAME);
const PARTS = ["SKILL.md", "README.md", "LICENSE", "references", "scripts", "tests"];

if (process.argv.includes("--where")) {
  console.log(TARGET);
  process.exit(0);
}

// Running from an already-installed copy: nothing to do.
if (SRC.replace(/[\\/]+$/, "") === TARGET.replace(/[\\/]+$/, "")) {
  console.log(`✔ already installed at ${TARGET} (self-copy skipped)`);
  process.exit(0);
}

mkdirSync(TARGET, { recursive: true });
for (const part of PARTS) {
  const from = join(SRC, part);
  if (!existsSync(from)) continue;
  cpSync(from, join(TARGET, part), { recursive: true, force: true });
}

// Never publish/install the node-only files into the skill dir.
const installed = readdirSync(TARGET).join(", ");
console.log(`✔ ${SKILL_NAME} installed to ${TARGET}`);
console.log(`  files: ${installed}`);
console.log(`  reload your agent, then ask it to "take over" another agent's task.`);
