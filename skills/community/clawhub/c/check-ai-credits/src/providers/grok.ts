import path from "node:path";
import { homedir } from "node:os";
import type { Provider } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { readJson, toFloat } from "../core/env";
import { httpJson } from "../core/http";
import { baseSnapshot, errorSnapshot } from "../core/snapshot";

const BASE = "https://cli-chat-proxy.grok.com/v1";
type Obj = Record<string, unknown>;

function authPath(): string {
  const home = process.env.GROK_HOME;
  return home ? path.join(home, "auth.json") : path.join(homedir(), ".grok", "auth.json");
}

function loadToken(auth: Obj | null): { key?: string; expiresAt?: string; email?: string } {
  if (!auth) return {};
  for (const value of Object.values(auth)) {
    if (value && typeof value === "object" && (value as Obj).key) {
      const rec = value as Obj;
      return {
        key: String(rec.key),
        expiresAt: typeof rec.expires_at === "string" ? rec.expires_at : undefined,
        email: typeof rec.email === "string" ? rec.email : undefined,
      };
    }
  }
  return {};
}

/** Units are provider *credits*, not dollars — currency stays "CREDITS".
 *  Read-only: the token is never refreshed here. */
export const grokProvider: Provider = {
  id: "grok",
  label: "Grok (xAI)",
  loginUrl: LOGIN_URLS.grok,

  async detect() {
    const { key } = loadToken(readJson<Obj>(authPath()));
    return key
      ? { configured: true, source: authPath() }
      : { configured: false, reason: "no auth token — run `grok login`" };
  },

  async fetch() {
    const { key, expiresAt, email } = loadToken(readJson<Obj>(authPath()));
    if (!key) {
      return errorSnapshot("grok", "grok auth token is expired or missing — run `grok login`", "api", LOGIN_URLS.grok);
    }
    const headers: Record<string, string> = {
      Authorization: `Bearer ${key}`,
      "X-XAI-Token-Auth": "xai-grok-cli",
      "User-Agent": "grok-cli/1.0.41",
    };

    const [statusM, monthlyRaw] = await httpJson(`${BASE}/billing`, headers);
    const [statusC, creditsRaw] = await httpJson(`${BASE}/billing?format=credits`, headers);
    if (statusM === 401 || statusM === 403 || statusC === 401 || statusC === 403) {
      return errorSnapshot("grok", "grok auth token is expired — run `grok login`", "api", LOGIN_URLS.grok);
    }
    const monthly = typeof monthlyRaw === "object" && monthlyRaw !== null ? (monthlyRaw as Obj) : {};
    const credits = typeof creditsRaw === "object" && creditsRaw !== null ? (creditsRaw as Obj) : {};
    if (!Object.keys(monthly).length && !Object.keys(credits).length) {
      return errorSnapshot("grok", `grok billing request failed (HTTP ${statusM}/${statusC})`);
    }

    const mconf = (monthly.config ?? {}) as Obj;
    const cconf = (credits.config ?? {}) as Obj;
    const limit = toFloat((mconf.monthlyLimit as Obj | undefined)?.val);
    const used = toFloat((mconf.used as Obj | undefined)?.val);
    const prepaid = toFloat((cconf.prepaidBalance as Obj | undefined)?.val);
    const remaining = prepaid !== null ? prepaid : limit !== null && used !== null ? limit - used : null;

    let tokenExpiresInHours: number | null = null;
    if (expiresAt) {
      const exp = Date.parse(expiresAt);
      if (Number.isFinite(exp)) tokenExpiresInHours = Math.round(((exp - Date.now()) / 3_600_000) * 10) / 10;
    }

    const snap = baseSnapshot("grok", "api");
    snap.currency = "CREDITS";
    snap.balance = remaining;
    snap.usedPercent = limit && used !== null ? Math.round((used / limit) * 10000) / 100 : null;
    snap.resetsAt = typeof mconf.billingPeriodEnd === "string" ? mconf.billingPeriodEnd : null;
    snap.details = {
      accountEmail: email ?? null,
      monthlyLimit: limit,
      monthlyUsed: used,
      remainingCredits: remaining,
      monthlyPeriodStart: mconf.billingPeriodStart ?? null,
      monthlyPeriodEnd: mconf.billingPeriodEnd ?? null,
      weeklyPeriodStart: (cconf.currentPeriod as Obj | undefined)?.start ?? null,
      weeklyPeriodEnd: (cconf.currentPeriod as Obj | undefined)?.end ?? null,
      onDemandCap: toFloat((cconf.onDemandCap as Obj | undefined)?.val),
      onDemandUsed: toFloat((cconf.onDemandUsed as Obj | undefined)?.val),
      topUpMethod: cconf.topUpMethod ?? null,
      unifiedBillingUser: cconf.isUnifiedBillingUser ?? null,
      tokenExpiresInHours,
    };
    return snap;
  },
};
