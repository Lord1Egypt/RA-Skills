import process from "node:process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { doctorSkill } from "./doctor.mjs";

function printHelp() {
  console.log(`Usage:
  node scripts/setup.mjs [options]

Options:
  --project <path>   Optional project directory for context only
  --json             Print JSON output
  -h, --help         Show help

What this does:
  1) Runs the read-only readiness check
  2) Confirms whether a supported local compressor is available
  3) Prints the next step for first-time use

This skill does not need an API key or generated config files. It only needs one local compressor tool.`);
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
  lines.push(`Project: ${summary.projectDir}`);
  lines.push(`Ready: ${summary.ok ? "yes" : "no"}`);
  lines.push("Config: no API key or secret setup is required for this skill.");
  if (summary.errors.length) {
    lines.push("Errors:");
    for (const error of summary.errors) lines.push(`- ${error}`);
  }
  if (summary.warnings.length) {
    lines.push("Warnings:");
    for (const warning of summary.warnings) lines.push(`- ${warning}`);
  }
  lines.push("Next:");
  if (summary.ok) {
    lines.push("- Run npm run compress -- <input> -f webp -q 80");
  } else {
    lines.push("- Install at least one of sips, cwebp, or ImageMagick");
    lines.push("- Re-run npm run ensure-ready");
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
