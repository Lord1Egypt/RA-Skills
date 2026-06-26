#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/poll-auth.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// poll-auth.js — Background device auth polling for awareness-memory skill.
//
// SSOT — edit this file in sdks/_shared/scripts/, NOT in the synced copies.
// See docs/features/f-036/shared-scripts-consolidation.md
//
// Spawned detached by recall.js after /auth/device/init.
// Polls /auth/device/poll until approved or expired,
// then writes apiKey + memoryId to ~/.openclaw/openclaw.json.
//
// TS variant: sdks/openclaw/src/poll-auth.ts (manually maintained)
//
// Usage: node poll-auth.js <device_code> <base_url> <interval_sec> <expires_in_sec>
// ---------------------------------------------------------------------------

"use strict";

const fs = require("fs");
const path = require("path");

const HOME = process.env.HOME || process.env.USERPROFILE || "";
const OPENCLAW_CONFIG_PATH = path.join(HOME, ".openclaw", "openclaw.json");
const AUTH_CACHE_FILE = path.join(HOME, ".awareness", "device-auth-result.json");

async function poll(baseUrl, deviceCode, intervalMs, expiresAt) {
  while (Date.now() < expiresAt) {
    await new Promise((r) => setTimeout(r, intervalMs));
    try {
      const resp = await fetch(`${baseUrl}/auth/device/poll`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_code: deviceCode }),
        signal: AbortSignal.timeout(8000),
      });
      const data = await resp.json();

      if (data.status === "approved" && data.api_key) {
        const apiKey = String(data.api_key);

        // Fetch memories to pick the first one
        let memoryId = "";
        try {
          const memResp = await fetch(`${baseUrl}/memories`, {
            headers: { Authorization: `Bearer ${apiKey}` },
            signal: AbortSignal.timeout(8000),
          });
          const memData = await memResp.json();
          const memories = Array.isArray(memData) ? memData : (Array.isArray(memData.memories) ? memData.memories : []);
          if (memories.length > 0) {
            memoryId = String(memories[0].id ?? "");
          }
        } catch { /* best-effort */ }

        // Write result cache file
        const cacheDir = path.dirname(AUTH_CACHE_FILE);
        if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
        fs.writeFileSync(
          AUTH_CACHE_FILE,
          JSON.stringify({ status: "approved", apiKey, memoryId, ts: Date.now() }),
          "utf8",
        );

        // Patch ~/.openclaw/openclaw.json — write under skills["awareness-memory"].config
        patchOpenClawConfig(apiKey, memoryId);
        return;
      }

      if (data.status === "expired") {
        writeFailure("expired");
        return;
      }
      // status === "pending" → keep polling
    } catch { /* network error — keep polling */ }
  }
  writeFailure("timeout");
}

function writeFailure(reason) {
  try {
    const cacheDir = path.dirname(AUTH_CACHE_FILE);
    if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
    fs.writeFileSync(
      AUTH_CACHE_FILE,
      JSON.stringify({ status: "failed", reason, ts: Date.now() }),
      "utf8",
    );
  } catch { /* best-effort */ }
}

function patchOpenClawConfig(apiKey, memoryId) {
  try {
    let cfg = {};
    try { cfg = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG_PATH, "utf8")); } catch { /* new file */ }

    // Write under skills["awareness-memory"].config (skill config path)
    const skills = (cfg.skills ?? {});
    const skillEntry = (skills["awareness-memory"] ?? {});
    const skillConfig = (skillEntry.config ?? {});

    skillConfig.apiKey = apiKey;
    if (memoryId) skillConfig.memoryId = memoryId;

    skillEntry.config = skillConfig;
    skills["awareness-memory"] = skillEntry;
    cfg.skills = skills;

    // Also patch plugins.entries["openclaw-memory"].config for cross-compatibility
    const plugins = (cfg.plugins ?? {});
    const entries = (plugins.entries ?? {});
    const pluginEntry = (entries["openclaw-memory"] ?? {});
    const pluginConfig = (pluginEntry.config ?? {});
    pluginConfig.apiKey = apiKey;
    if (memoryId) pluginConfig.memoryId = memoryId;
    pluginEntry.config = pluginConfig;
    entries["openclaw-memory"] = pluginEntry;
    plugins.entries = entries;
    cfg.plugins = plugins;

    const configDir = path.dirname(OPENCLAW_CONFIG_PATH);
    if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });
    fs.writeFileSync(OPENCLAW_CONFIG_PATH, JSON.stringify(cfg, null, 4), "utf8");
  } catch { /* best-effort */ }
}

// Entry point
const [, , deviceCode, baseUrl, intervalStr, expiresInStr] = process.argv;
if (!deviceCode || !baseUrl) process.exit(1);

const intervalMs = (Number(intervalStr) || 5) * 1000;
// Default expires_in aligned with backend DEVICE_AUTH_TTL=900s (F-035)
// so the background poller stays alive for cross-device headless auth.
const expiresIn = Number(expiresInStr) || 900;
const expiresAt = Date.now() + expiresIn * 1000;

poll(baseUrl, deviceCode, intervalMs, expiresAt).catch(() => writeFailure("error"));
