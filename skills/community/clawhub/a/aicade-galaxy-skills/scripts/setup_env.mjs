#!/usr/bin/env node

import { readFile, writeFile } from "node:fs/promises";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const ENV_PATH = ".env";

const DEFAULTS = {
  AICADE_GALAXY_BASE_URL: "https://aicadegalaxy.com/agent",
  AICADE_GALAXY_API_KEY: "xxxx",
  AICADE_GALAXY_OUTPUT_PATH: "output",
};

async function main() {
  const existing = await loadEnvFile(ENV_PATH);
  const rl = createInterface({ input, output });

  try {
    const values = {
      AICADE_GALAXY_BASE_URL: await askRequired(
        rl,
        "AICADE_GALAXY_BASE_URL",
        existing.AICADE_GALAXY_BASE_URL ??
          existing.CLAWHUB_BASE_URL ??
          DEFAULTS.AICADE_GALAXY_BASE_URL,
      ),
      AICADE_GALAXY_API_KEY: await askRequired(
        rl,
        "AICADE_GALAXY_API_KEY",
        existing.AICADE_GALAXY_API_KEY ?? DEFAULTS.AICADE_GALAXY_API_KEY,
        true,
      ),
      AICADE_GALAXY_OUTPUT_PATH: await askRequired(
        rl,
        "AICADE_GALAXY_OUTPUT_PATH",
        existing.AICADE_GALAXY_OUTPUT_PATH ??
          DEFAULTS.AICADE_GALAXY_OUTPUT_PATH,
      ),
    };

    await writeFile(ENV_PATH, serializeEnv(values), "utf8");

    output.write(`Saved ${ENV_PATH}\n`);
    output.write("Configured header: X-API-Key from AICADE_GALAXY_API_KEY\n");
    output.write("Using fixed services path: /admin/gateway/services\n");
    output.write(
      `Using output directory: ${values.AICADE_GALAXY_OUTPUT_PATH}\nOutput file: ${values.AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json\n`,
    );
  } finally {
    rl.close();
  }
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

function serializeEnv(values) {
  return `${Object.entries(values)
    .map(([key, value]) => `${key}=${escapeEnvValue(value)}`)
    .join("\n")}\n`;
}

function escapeEnvValue(value) {
  if (value === "" || /\s/.test(value) || value.includes('"')) {
    return JSON.stringify(value);
  }

  return value;
}

async function askRequired(rl, key, currentValue, secret = false) {
  while (true) {
    const shownDefault = currentValue ? maskIfNeeded(currentValue, secret) : "";
    const suffix = shownDefault ? ` [${shownDefault}]` : "";
    const answer = await rl.question(`${key}${suffix}: `);
    const value = answer.trim() || currentValue;

    if (value) {
      return value;
    }

    output.write(`${key} is required.\n`);
  }
}

function maskIfNeeded(value, secret) {
  if (!secret) {
    return value;
  }

  if (value.length <= 4) {
    return "*".repeat(value.length);
  }

  return `${"*".repeat(value.length - 4)}${value.slice(-4)}`;
}

await main();
