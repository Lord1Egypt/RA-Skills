import process from "node:process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { doctorSkill } from "./doctor.mjs";

function printHelp() {
  console.log(`Usage:
  node scripts/ensure-ready.mjs [options]

Options:
  --project <path>   Optional project directory for context only
  --json             Print JSON output
  -h, --help         Show help`);
}

function parseArgs(argv) {
  const args = { project: process.cwd(), json: false };
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--project") args.project = argv[++i] ?? args.project;
    else if (current === "--json") args.json = true;
    else if (current === "--help" || current === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function formatText(summary) {
  const lines = [];
  lines.push(`Skill dir: ${summary.skillDir}`);
  lines.push(`Project dir: ${summary.projectDir}`);
  lines.push(`Ready: ${summary.ok ? "yes" : "no"}`);
  if (summary.warnings.length) {
    lines.push("Warnings:");
    for (const warning of summary.warnings) lines.push(`- ${warning}`);
  }
  if (summary.suggestions.length) {
    lines.push("Suggestions:");
    for (const suggestion of summary.suggestions) lines.push(`- ${suggestion}`);
  }
  return lines.join("\n");
}

const isDirectRun =
  process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));

if (isDirectRun) {
  try {
    const args = parseArgs(process.argv.slice(2));
    const summary = doctorSkill({ projectDir: args.project });
    if (args.json) console.log(JSON.stringify(summary, null, 2));
    else console.log(formatText(summary));
    if (!summary.ok) process.exitCode = 1;
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}
