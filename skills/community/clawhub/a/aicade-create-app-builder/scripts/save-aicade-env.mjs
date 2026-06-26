#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_API_URL = "https://aicadegalaxy.com/v1";

const MIRROR_KEYS = new Map([
  ["AICADE_API_KEY", ["AICADE_API_KEY", "VITE_AICADE_API_KEY"]],
  ["VITE_AICADE_API_KEY", ["AICADE_API_KEY", "VITE_AICADE_API_KEY"]],
  ["AICADE_API_SECRET_KEY", ["AICADE_API_SECRET_KEY", "VITE_AICADE_API_SECRET_KEY"]],
  ["VITE_AICADE_API_SECRET_KEY", ["AICADE_API_SECRET_KEY", "VITE_AICADE_API_SECRET_KEY"]],
  ["AICADE_API_URL", ["AICADE_API_URL", "VITE_AICADE_API_URL"]],
  ["VITE_AICADE_API_URL", ["AICADE_API_URL", "VITE_AICADE_API_URL"]],
  ["VITE_AICADE_API_UPLOAD", ["VITE_AICADE_API_UPLOAD"]],
  ["DAPP_KEY", ["AICADE_API_KEY", "VITE_AICADE_API_KEY", "DAPP_KEY"]],
  ["DAPP_SECRET_KEY", ["AICADE_API_SECRET_KEY", "VITE_AICADE_API_SECRET_KEY", "DAPP_SECRET_KEY"]],
  ["UPLOAD_URL", ["VITE_AICADE_API_UPLOAD", "UPLOAD_URL"]],
]);

function printUsage(exitCode = 0) {
  console.log(`Usage:
  node save-aicade-env.mjs --cwd /path/to/project --set KEY=VALUE [--set KEY=VALUE ...]

Options:
  --cwd    Project directory whose .env file should be updated. Default: current working directory
  --set    One env assignment per flag. Can be repeated.
  -h, --help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = { cwd: process.cwd(), sets: [] };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];

    if (current === "-h" || current === "--help") {
      printUsage(0);
    }

    if (current === "--cwd") {
      args.cwd = path.resolve(argv[index + 1]);
      index += 1;
      continue;
    }

    if (current === "--set") {
      args.sets.push(argv[index + 1]);
      index += 1;
    }
  }

  if (!args.sets.length) {
    console.error("Missing required argument: --set");
    printUsage(1);
  }

  return args;
}

function parseAssignment(raw) {
  const eqIndex = raw.indexOf("=");
  if (eqIndex <= 0) {
    throw new Error(`Invalid assignment: ${raw}`);
  }

  const key = raw.slice(0, eqIndex).trim();
  const value = raw.slice(eqIndex + 1).trim();
  if (!key || !value) {
    throw new Error(`Invalid assignment: ${raw}`);
  }

  return { key, value };
}

function loadEnvLines(filePath) {
  if (!fs.existsSync(filePath)) {
    return [];
  }

  return fs.readFileSync(filePath, "utf8").split(/\r?\n/);
}

function quoteIfNeeded(value) {
  return /\s/.test(value) ? JSON.stringify(value) : value;
}

function upsertAssignments(lines, assignments) {
  const nextLines = [...lines];

  for (const [key, value] of assignments.entries()) {
    const rendered = `${key}=${quoteIfNeeded(value)}`;
    const matchIndex = nextLines.findIndex((line) => {
      const trimmed = line.trim();
      return trimmed === key || trimmed.startsWith(`${key}=`);
    });

    if (matchIndex >= 0) {
      nextLines[matchIndex] = rendered;
    } else {
      nextLines.push(rendered);
    }
  }

  return nextLines;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const envPath = path.join(args.cwd, ".env");
  const assignments = new Map();

  for (const raw of args.sets) {
    const { key, value } = parseAssignment(raw);
    const targets = MIRROR_KEYS.get(key) || [key];
    for (const target of targets) {
      assignments.set(target, value);
    }
  }

  if (!assignments.has("AICADE_API_URL") && !assignments.has("VITE_AICADE_API_URL")) {
    assignments.set("AICADE_API_URL", DEFAULT_API_URL);
    assignments.set("VITE_AICADE_API_URL", DEFAULT_API_URL);
  }

  const currentLines = loadEnvLines(envPath);
  const nextLines = upsertAssignments(currentLines, assignments);
  const output = nextLines.join("\n").replace(/\n*$/, "\n");
  fs.writeFileSync(envPath, output, "utf8");

  process.stdout.write(
    `${JSON.stringify({ cwd: args.cwd, envPath, savedKeys: [...assignments.keys()] }, null, 2)}\n`,
  );
}

main();
