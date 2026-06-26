#!/usr/bin/env node
/**
 * Install AgentNotes OpenClaw skill into ~/.openclaw/workspace/skills/agentnotes
 * Usage: npx agentnotes-openclaw install
 *        npx agentnotes-openclaw install --workspace /path/to/workspace
 */

import { cpSync, existsSync, mkdirSync, rmSync } from "fs";
import { homedir } from "os";
import { dirname, join, resolve } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(__dirname, "..");

function parseWorkspaceArg() {
  const i = process.argv.indexOf("--workspace");
  if (i !== -1 && process.argv[i + 1]) return resolve(process.argv[i + 1]);
  return join(homedir(), ".openclaw", "workspace");
}

const workspace = parseWorkspaceArg();
const dest = join(workspace, "skills", "agentnotes");

if (!existsSync(join(skillRoot, "SKILL.md"))) {
  console.error("SKILL.md not found in package — broken install");
  process.exit(1);
}

mkdirSync(join(workspace, "skills"), { recursive: true });
if (existsSync(dest)) rmSync(dest, { recursive: true, force: true });

cpSync(skillRoot, dest, {
  recursive: true,
  filter: (src) => {
    const base = src.replace(/\\/g, "/");
    return !base.includes("/node_modules/") && !base.endsWith("/package.json");
  },
});

console.log("AgentNotes OpenClaw skill installed:");
console.log(" ", dest);
console.log("");
console.log("Next:");
console.log("  1. Add env to ~/.openclaw/openclaw.json (skills.entries.agentnotes.env)");
console.log("     See: https://github.com/mattmerrick/agentnotes/blob/main/integrations/openclaw/openclaw.example.json5");
console.log("  2. Restart OpenClaw / new session");
console.log("  3. Verify: node", join(dest, "scripts/verify.mjs"));
