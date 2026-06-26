#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const ENV_PATH = ".env";
const REQUIRED_ENV_NAMES = [
  "AICADE_GALAXY_BASE_URL",
  "AICADE_GALAXY_API_KEY",
  "AICADE_GALAXY_OUTPUT_PATH",
];

async function main() {
  const existing = await loadEnvFile(ENV_PATH);
  const missing = REQUIRED_ENV_NAMES.filter((name) => !existing[name]);

  if (missing.length > 0) {
    console.log(
      `Missing required environment values: ${missing.join(", ")}. Running setup_env.mjs...`,
    );
    runScript(process.execPath, [resolve(SCRIPT_DIR, "setup_env.mjs")], "setup_env.mjs");
  } else {
    console.log("Environment already configured. Skipping setup_env.mjs.");
  }

  console.log("Running export_artifact.mjs...");
  runScript(process.execPath, [resolve(SCRIPT_DIR, "export_artifact.mjs")], "export_artifact.mjs");
  console.log("Bootstrap completed.");
}

async function loadEnvFile(path) {
  try {
    const content = await readFile(path, "utf8");
    return parseEnv(content);
  } catch {
    return {};
  }
}

function parseEnv(content) {
  const result = {};

  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const equalsIndex = line.indexOf("=");
    if (equalsIndex <= 0) {
      continue;
    }

    const key = line.slice(0, equalsIndex).trim();
    const value = line.slice(equalsIndex + 1).trim();
    result[key] = stripQuotes(value);
  }

  return result;
}

function stripQuotes(value) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }

  return value;
}

function runScript(command, args, label) {
  const result = spawnSync(command, args, {
    stdio: "inherit",
  });

  if (result.error) {
    throw new Error(`Failed to run ${label}: ${result.error.message}`);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

await main();
