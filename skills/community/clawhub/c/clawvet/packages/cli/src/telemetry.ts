import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir, platform, release } from "node:os";
import { randomUUID } from "node:crypto";
import type { ScanResult } from "@clawvet/shared";

const CONFIG_DIR = join(homedir(), ".clawvet");
const CONFIG_FILE = join(CONFIG_DIR, "config.json");
const TELEMETRY_ENDPOINT = "https://bazzzz--0ab7a9301f3911f1ab9942dde27851f2.web.val.run";

interface Config {
  telemetry?: "on" | "off" | undefined; // undefined = not yet asked
  deviceId?: string;
  scanCount?: number;
}

function loadConfig(): Config {
  try {
    if (existsSync(CONFIG_FILE)) {
      return JSON.parse(readFileSync(CONFIG_FILE, "utf-8"));
    }
  } catch {
    // corrupted config, start fresh
  }
  return {};
}

function saveConfig(config: Config): void {
  try {
    mkdirSync(CONFIG_DIR, { recursive: true });
    writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  } catch {
    // non-critical, ignore
  }
}

export function isTelemetryEnabled(): boolean {
  const env = process.env.CLAWVET_TELEMETRY;
  if (env === "0" || env === "off") return false;
  if (env === "1" || env === "on") return true;
  const config = loadConfig();
  return config.telemetry === "on";
}

export function setTelemetry(enabled: boolean): void {
  const config = loadConfig();
  config.telemetry = enabled ? "on" : "off";
  saveConfig(config);
}

export function hasBeenAsked(): boolean {
  const config = loadConfig();
  return config.telemetry !== undefined;
}

function getDeviceId(): string {
  const config = loadConfig();
  if (!config.deviceId) {
    config.deviceId = randomUUID();
    saveConfig(config);
  }
  return config.deviceId;
}

function incrementScanCount(): number {
  const config = loadConfig();
  config.scanCount = (config.scanCount || 0) + 1;
  saveConfig(config);
  return config.scanCount;
}

export function getScanCount(): number {
  return loadConfig().scanCount || 0;
}

export function sendTelemetry(result: ScanResult): Promise<void> {
  if (!isTelemetryEnabled()) return Promise.resolve();

  const scanCount = incrementScanCount();

  const payload = {
    deviceId: getDeviceId(),
    scanCount,
    ts: new Date().toISOString(),
    os: platform(),
    osVersion: release(),
    skillName: result.skillName,
    riskScore: result.riskScore,
    riskGrade: result.riskGrade,
    findingsCount: result.findingsCount,
    cached: result.cached ?? false,
  };

  return fetch(TELEMETRY_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(3000),
  }).then(() => {}).catch(() => {
    // silently ignore — telemetry is best-effort
  });
}
