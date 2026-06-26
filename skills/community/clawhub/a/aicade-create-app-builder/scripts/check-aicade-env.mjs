#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_API_URL = "https://aicadegalaxy.com/v1";

const ACCESS_GROUP = [
  ["AICADE_API_KEY"],
  ["AICADE_API_SECRET_KEY"],
  ["AICADE_API_URL", "VITE_AICADE_API_URL"],
];

const UPLOAD_REQUIRED_GROUP = [
  ["AICADE_API_KEY", "VITE_AICADE_API_KEY", "DAPP_KEY"],
  ["AICADE_API_SECRET_KEY", "VITE_AICADE_API_SECRET_KEY", "DAPP_SECRET_KEY"],
];

const UPLOAD_OPTIONAL_GROUP = [
  ["VITE_AICADE_API_UPLOAD", "UPLOAD_URL"],
  ["AICADE_API_URL", "VITE_AICADE_API_URL"],
];

const DEFAULT_MODE = "all";
const SUPPORTED_MODES = new Set(["access", "upload", "all"]);

function printUsage(exitCode = 0) {
  console.log(`Usage:
  node check-aicade-env.mjs [--mode access|upload|all] [--cwd /path/to/project]

Options:
  --mode   Which variable set to inspect. Default: ${DEFAULT_MODE}
  --cwd    Project directory to inspect for .env files. Default: current working directory
  -h, --help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = { mode: DEFAULT_MODE, cwd: process.cwd() };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];

    if (current === "-h" || current === "--help") {
      printUsage(0);
    }

    if (current === "--mode") {
      args.mode = argv[index + 1];
      index += 1;
      continue;
    }

    if (current === "--cwd") {
      args.cwd = path.resolve(argv[index + 1]);
      index += 1;
    }
  }

  if (!SUPPORTED_MODES.has(args.mode)) {
    console.error(`Unsupported mode: ${args.mode}`);
    printUsage(1);
  }

  return args;
}

function parseEnvFile(filePath) {
  const result = {};
  if (!fs.existsSync(filePath)) {
    return result;
  }

  const content = fs.readFileSync(filePath, "utf8");
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const exportLine = line.startsWith("export ") ? line.slice(7).trim() : line;
    const eqIndex = exportLine.indexOf("=");
    if (eqIndex <= 0) {
      continue;
    }

    const key = exportLine.slice(0, eqIndex).trim();
    let value = exportLine.slice(eqIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }

  return result;
}

function loadProjectEnv(cwd) {
  const env = {};
  for (const name of [".env", ".env.local"]) {
    Object.assign(env, parseEnvFile(path.join(cwd, name)));
  }
  return env;
}

function getValue(nameCandidates, projectEnv) {
  for (const name of nameCandidates) {
    const fromProcess = process.env[name];
    if (typeof fromProcess === "string" && fromProcess.trim()) {
      return { key: name, value: fromProcess.trim(), source: "process.env" };
    }

    const fromProject = projectEnv[name];
    if (typeof fromProject === "string" && fromProject.trim()) {
      return { key: name, value: fromProject.trim(), source: ".env" };
    }
  }

  if (nameCandidates.includes("AICADE_API_URL") || nameCandidates.includes("VITE_AICADE_API_URL")) {
    return { key: "AICADE_API_URL", value: DEFAULT_API_URL, source: "default" };
  }

  return null;
}

function inspectGroup(entries, projectEnv) {
  return entries.map((nameCandidates) => {
    const found = getValue(nameCandidates, projectEnv);
    return {
      candidates: nameCandidates,
      present: Boolean(found),
      resolvedKey: found ? found.key : null,
      source: found ? found.source : null,
    };
  });
}

function summarizeStatus(results) {
  return {
    present: results.filter((item) => item.present),
    missing: results.filter((item) => !item.present),
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const projectEnv = loadProjectEnv(args.cwd);

  const payload = {
    cwd: args.cwd,
    mode: args.mode,
  };

  if (args.mode === "access" || args.mode === "all") {
    payload.access = summarizeStatus(inspectGroup(ACCESS_GROUP, projectEnv));
  }

  if (args.mode === "upload" || args.mode === "all") {
    payload.upload = {
      required: summarizeStatus(inspectGroup(UPLOAD_REQUIRED_GROUP, projectEnv)),
      optional: summarizeStatus(inspectGroup(UPLOAD_OPTIONAL_GROUP, projectEnv)),
    };
  }

  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

main();
