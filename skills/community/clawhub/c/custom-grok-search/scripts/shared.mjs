#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

export function parseDotEnv(content) {
  const out = {};
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const eq = line.indexOf("=");
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let value = line.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    out[key] = value;
  }
  return out;
}

export function loadEnvFiles() {
  const candidates = [
    path.join(process.cwd(), ".env"),
    path.join(os.homedir(), ".openclaw", ".env"),
  ];
  const loaded = {};
  for (const p of candidates) {
    try {
      const text = fs.readFileSync(p, "utf8");
      Object.assign(loaded, parseDotEnv(text));
    } catch {}
  }
  return loaded;
}

export function readConfigJson() {
  try {
    const p = path.join(os.homedir(), ".clawdbot", "clawdbot.json");
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return null;
  }
}

export function getValue(...keys) {
  const fileEnv = loadEnvFiles();
  for (const key of keys) {
    if (process.env[key]) return process.env[key];
    if (fileEnv[key]) return fileEnv[key];
  }
  return undefined;
}

export function readApiKeys() {
  const configJson = readConfigJson();
  const customApiKey = getValue("CUSTOM_GROK_APIKEY");
  const officialApiKey =
    getValue("XAI_API_KEY") ||
    configJson?.env?.XAI_API_KEY ||
    configJson?.env?.vars?.XAI_API_KEY ||
    configJson?.skills?.entries?.["grok-search"]?.apiKey ||
    configJson?.skills?.entries?.["search-x"]?.apiKey ||
    configJson?.skills?.entries?.xai?.apiKey ||
    null;
  return { customApiKey, officialApiKey, apiKey: customApiKey || officialApiKey || null };
}

export function getRuntimeConfig() {
  const { customApiKey, apiKey } = readApiKeys();
  const useCustom = Boolean(customApiKey);
  const baseUrl = useCustom
    ? getValue("CUSTOM_GROK_BASE_URL") || "https://api.x.ai/v1"
    : getValue("XAI_BASE_URL") || "https://api.x.ai/v1";
  const model = useCustom
    ? getValue("CUSTOM_GROK_MODEL") || "grok-4.20-beta"
    : getValue("GROK_MODEL") || "grok-4-1-fast";
  const userAgent = useCustom
    ? getValue("CUSTOM_GROK_USER_AGENT") || "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    : getValue("XAI_USER_AGENT") || undefined;

  return {
    useCustom,
    apiKey,
    baseUrl: String(baseUrl).replace(/\/$/, ""),
    model,
    userAgent,
  };
}

export function collectCitations(resp) {
  const out = new Set();
  if (Array.isArray(resp?.citations)) {
    for (const u of resp.citations) if (typeof u === "string" && u) out.add(u);
  }
  if (Array.isArray(resp?.output)) {
    for (const item of resp.output) {
      const content = Array.isArray(item?.content) ? item.content : [];
      for (const c of content) {
        const ann = Array.isArray(c?.annotations) ? c.annotations : [];
        for (const a of ann) {
          const url = a?.url || a?.web_citation?.url;
          if (typeof url === "string" && url) out.add(url);
        }
      }
    }
  }
  return [...out];
}
