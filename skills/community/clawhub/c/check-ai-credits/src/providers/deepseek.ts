import type { Provider, Snapshot } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { hermesEnv, nowIso, toFloat } from "../core/env";
import { httpJson } from "../core/http";
import { baseSnapshot, errorSnapshot } from "../core/snapshot";

const BALANCE_URL = "https://api.deepseek.com/user/balance";

interface BalanceInfo {
  currency?: string;
  total_balance?: unknown;
  granted_balance?: unknown;
  topped_up_balance?: unknown;
}

/** Pure mapping: GET /user/balance response -> snapshot. */
export function parseDeepseek(data: Record<string, unknown>): Snapshot {
  const infos = Array.isArray(data.balance_infos)
    ? (data.balance_infos as BalanceInfo[])
    : [];
  const info = infos[0] ?? {};
  const snap = baseSnapshot("deepseek", "api");
  snap.currency = info.currency || "USD";
  snap.balance = toFloat(info.total_balance);
  snap.details = {
    isAvailable: data.is_available,
    grantedBalance: toFloat(info.granted_balance),
    toppedUpBalance: toFloat(info.topped_up_balance),
    currencies: infos.map((i) => i.currency),
  };
  return snap;
}

export const deepseekProvider: Provider = {
  id: "deepseek",
  label: "DeepSeek (official)",
  loginUrl: LOGIN_URLS.deepseek,

  async detect() {
    const key = hermesEnv("DEEPSEEK_API_KEY");
    return key
      ? { configured: true, source: "DEEPSEEK_API_KEY" }
      : { configured: false, reason: "DEEPSEEK_API_KEY missing (env or $HERMES_HOME/.env)" };
  },

  async fetch() {
    const key = hermesEnv("DEEPSEEK_API_KEY");
    if (!key) {
      return errorSnapshot(
        "deepseek",
        "DEEPSEEK_API_KEY missing (env or $HERMES_HOME/.env)",
        "api",
        LOGIN_URLS.deepseek,
      );
    }
    const [status, data] = await httpJson(BALANCE_URL, { Authorization: `Bearer ${key}` });
    if (status === 401 || status === 403) {
      return errorSnapshot(
        "deepseek",
        `auth token is invalid — DEEPSEEK_API_KEY rejected (HTTP ${status})`,
        "api",
        LOGIN_URLS.deepseek,
      );
    }
    if (status !== 200 || typeof data !== "object" || data === null) {
      return errorSnapshot("deepseek", `DeepSeek balance request failed (HTTP ${status})`);
    }
    const snap = parseDeepseek(data as Record<string, unknown>);
    // relay keys are rejected on purpose; keep timestamp fresh for trend ordering
    snap.timestamp = nowIso();
    return snap;
  },
};
