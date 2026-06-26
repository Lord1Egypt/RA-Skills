#!/usr/bin/env node
/**
 * start-all.mjs — Auto-start bridges based on .env config
 *
 * Reads .env and starts only the bridges whose tokens are configured.
 */

import { readFileSync, existsSync } from "fs";

// Load .env if present
try {
  const envPath = new URL(".env", import.meta.url).pathname;
  if (existsSync(envPath)) {
    for (const line of readFileSync(envPath, "utf-8").split("\n")) {
      const t = line.trim();
      if (!t || t.startsWith("#")) continue;
      const eq = t.indexOf("=");
      if (eq < 1) continue;
      const k = t.slice(0, eq).trim();
      const v = t.slice(eq + 1).trim();
      if (k && !(k in process.env)) process.env[k] = v;
    }
  }
} catch {}

const ts = () => new Date().toISOString();
const bridges = [];

if (process.env.TELEGRAM_BOT_TOKEN) {
  console.log(ts(), "[START] Telegram bridge enabled");
  import("./bridge-telegram.mjs");
  bridges.push("Telegram");
}

if (process.env.WECOM_BOT_ID && process.env.WECOM_SECRET) {
  console.log(ts(), "[START] WeChat Work bridge enabled");
  import("./bridge-wecom.mjs");
  bridges.push("WeChat Work");
}

if (process.env.QQ_APP_ID && process.env.QQ_APP_SECRET) {
  console.log(ts(), "[START] QQ Bot bridge enabled");
  import("./bridge-qq.mjs");
  bridges.push("QQ");
}

if (bridges.length === 0) {
  console.error(ts(), "[ERROR] No bridges configured. Set tokens in .env");
  process.exit(1);
}

console.log(ts(), `[START] Claude Anywhere running: ${bridges.join(", ")}`);
