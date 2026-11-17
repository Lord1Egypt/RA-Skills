import { spawnSync } from "node:child_process";
import type { Snapshot } from "../types";
import { detectAuthError } from "./auth";
import { nowIso, parseMoneyPrefix } from "./env";

type Json = Record<string, unknown> | null;

/** Run the CodexBar CLI and parse stdout as JSON (never throws). */
function runJson(args: string[], timeoutMs = 45_000): Json {
  try {
    const res = spawnSync("codexbar", args, { encoding: "utf8", timeout: timeoutMs });
    if (!res.stdout) return null;
    const parsed: unknown = JSON.parse(res.stdout);
    return typeof parsed === "object" && parsed !== null
      ? (parsed as Record<string, unknown>)
      : null;
  } catch {
    return null;
  }
}

export function codexbarAvailable(): boolean {
  try {
    const res = spawnSync("codexbar", ["--version"], { encoding: "utf8", timeout: 10_000 });
    return Boolean(res.stdout) || res.error === undefined;
  } catch {
    return false;
  }
}

/** `codexbar usage [--provider X] --format json` -> array (or single) item. */
export function codexbarUsage(provider?: string): Record<string, unknown>[] {
  const args = ["usage", "--format", "json"];
  if (provider) args.push("--provider", provider);
  const data = runJson(args);
  if (!data) return [];
  if (Array.isArray(data)) return data as Record<string, unknown>[];
  return [data];
}

/** `codexbar plugins fetch <id> --json --pretty` -> plugin snapshot. */
export function codexbarPlugin(id: string): Json {
  return runJson(["plugins", "fetch", id, "--json", "--pretty"], 60_000);
}

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null
    ? (value as Record<string, unknown>)
    : {};
}

/** CodexBar errors are usually strings but some providers return
 *  `{kind, message, code}` objects — normalize to a message string. */
export function normalizeError(raw: unknown): string | null {
  if (typeof raw === "string" && raw) return raw;
  if (raw && typeof raw === "object") {
    const rec = raw as Record<string, unknown>;
    if (typeof rec.message === "string" && rec.message) return rec.message;
    try {
      return JSON.stringify(raw);
    } catch {
      return null;
    }
  }
  return null;
}

/** Flatten a CodexBar usage item into our snapshot schema (extras under details). */
export function extractUsageSnapshot(item: Record<string, unknown>): Snapshot {
  const provider = String(item.provider ?? "unknown");
  const usage = asRecord(item.usage);
  const pace = asRecord(item.pace);
  const primary = asRecord(usage.primary);

  const details: Record<string, unknown> = {};
  if (primary.usedPercent !== undefined) details.resetDescription = primary.resetDescription;
  if (primary.windowMinutes !== undefined) details.windowMinutes = primary.windowMinutes;
  const primaryPace = asRecord(pace.primary);
  if (primaryPace.summary !== undefined) details.paceSummary = primaryPace.summary;
  if (primaryPace.willLastToReset !== undefined) details.willLastToReset = primaryPace.willLastToReset;
  if (primaryPace.etaSeconds !== undefined) details.etaSeconds = primaryPace.etaSeconds;

  const errorStr = normalizeError(item.error);
  const snap: Snapshot = {
    provider,
    source: String(item.source ?? "codexbar"),
    timestamp: nowIso(),
    usedPercent: typeof primary.usedPercent === "number" ? primary.usedPercent : null,
    resetsAt: typeof primary.resetsAt === "string" ? primary.resetsAt : null,
    balance: null,
    monthCost: null,
    monthPeriod: null,
    details,
    error: errorStr,
  };

  // mimo carries wallet fields inside usage.mimoUsage
  if (provider === "mimo") {
    const mimo = asRecord(usage.mimoUsage);
    if (mimo.balance !== undefined) snap.balance = Number(mimo.balance);
    if (typeof mimo.currency === "string") snap.currency = mimo.currency;
    details.tokenUsed = mimo.tokenUsed;
    details.tokenLimit = mimo.tokenLimit;
    details.planExpired = mimo.planExpired;
    details.planPeriodEnd = mimo.planPeriodEnd;
  }

  const hint = detectAuthError({ ...item, error: errorStr ?? undefined });
  if (hint) snap.authHint = hint;
  return snap;
}

/** Flatten a CodexBar plugin snapshot (apikey.fun style) into our schema. */
export function extractPluginSnapshot(
  data: Record<string, unknown> | null,
  provider: string,
): Snapshot {
  const snap: Snapshot = {
    provider,
    source: "codexbar-plugin",
    timestamp: nowIso(),
    balance: null,
    usedPercent: null,
    resetsAt: null,
    monthCost: null,
    monthPeriod: null,
    details: null,
    error: data ? null : "plugin fetch returned no snapshot",
  };
  if (!data) return snap;

  const cost = asRecord(data.providerCost ?? data.cost);
  const details: Record<string, unknown> = {};
  if (typeof cost.balance === "number") snap.balance = cost.balance;
  const currency = cost.currencyCode ?? cost.currency;
  if (typeof currency === "string") snap.currency = currency;
  if (typeof cost.used === "number") details.windowSpend = cost.used;
  if (typeof cost.period === "string") details.windowPeriod = cost.period;

  const sections = Array.isArray(data.details) ? (data.details as unknown[]) : [];
  for (const rawSection of sections) {
    const rows = asRecord(rawSection).rows;
    if (!Array.isArray(rows)) continue;
    for (const rawRow of rows) {
      const row = asRecord(rawRow);
      const label = String(row.label ?? "").toLowerCase();
      if (label === "balance") {
        const parsed = parseMoneyPrefix(row.value);
        if (parsed !== null) snap.balance = parsed;
      } else if (label === "today") {
        details.todayCost = parseMoneyPrefix(row.value);
      } else if (label === "all time") {
        details.allTimeCost = parseMoneyPrefix(row.value);
      }
    }
  }
  snap.details = details;
  return snap;
}
