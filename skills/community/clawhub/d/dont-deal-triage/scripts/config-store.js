import path from "node:path";
import fs from "node:fs/promises";
import { dontDealHome, pathExists, writeJsonFile } from "./utils.js";

function configPath(env = process.env) {
  return path.join(dontDealHome(env), "config.json");
}

function defaultConfig() {
  return {
    version: 1,
    language_preference: "bilingual",
    last_detected_language: null,
    first_run_completed: false,
    initialized_at: null,
    updated_at: null
  };
}

export async function loadConfig(env = process.env) {
  const targetPath = configPath(env);
  if (!(await pathExists(targetPath))) {
    return defaultConfig();
  }

  const text = await fs.readFile(targetPath, "utf8");
  if (!text.trim()) {
    return defaultConfig();
  }

  return {
    ...defaultConfig(),
    ...JSON.parse(text)
  };
}

export async function saveConfig(config, env = process.env) {
  const current = await loadConfig(env);
  const now = new Date().toISOString();
  const nextConfig = {
    ...current,
    ...config,
    version: 1,
    initialized_at: current.initialized_at ?? now,
    updated_at: now
  };

  await writeJsonFile(configPath(env), nextConfig);
  return nextConfig;
}

export async function ensureConfig(env = process.env) {
  const current = await loadConfig(env);
  if (current.initialized_at) {
    return current;
  }

  return saveConfig(current, env);
}
