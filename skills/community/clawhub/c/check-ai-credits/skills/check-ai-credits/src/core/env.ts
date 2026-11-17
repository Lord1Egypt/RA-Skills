import fs from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export function hermesHome(): string {
  return process.env.HERMES_HOME ?? join(homedir(), ".hermes");
}

/** Read one key from the process env, then $HERMES_HOME/.env (never exported). */
export function hermesEnv(name: string): string | undefined {
  const fromProcess = Bun.env[name];
  if (fromProcess) return fromProcess;
  try {
    const lines = fs.readFileSync(join(hermesHome(), ".env"), "utf8").split("\n");
    for (const raw of lines) {
      const line = raw.trim();
      if (!line.startsWith(`${name}=`)) continue;
      const value = line.slice(name.length + 1).trim().replace(/^["']|["']$/g, "");
      if (value) return value;
    }
  } catch {
    // .env missing or unreadable — treated as "not set"
  }
  return undefined;
}

export function readJson<T>(path: string): T | null {
  try {
    return JSON.parse(fs.readFileSync(path, "utf8")) as T;
  } catch {
    return null;
  }
}

export function nowIso(): string {
  return new Date().toISOString();
}

export function isoFromEpoch(value: unknown): string | null {
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return null;
  try {
    return new Date(n * 1000).toISOString();
  } catch {
    return null;
  }
}

/** Lenient numeric coercion: "$1,234.50 USD" / 12 / "12" -> number; bool -> null. */
export function toFloat(value: unknown): number | null {
  if (typeof value === "boolean") return null;
  if (typeof value === "number") return Number.isFinite(value) ? value : null;
  if (typeof value === "string") {
    const cleaned = value.replace(/[$,]/g, "").replace("USD", "").trim();
    const n = Number(cleaned);
    return Number.isFinite(n) ? n : null;
  }
  return null;
}

/** "CN¥6.38 (Paid: ...)" -> 6.38 — first numeric run in the string. */
export function parseMoneyPrefix(text: unknown): number | null {
  if (typeof text !== "string") return null;
  const m = text.match(/\d+(?:\.\d+)?/);
  if (!m) return null;
  const n = Number(m[0]);
  return Number.isFinite(n) ? n : null;
}
