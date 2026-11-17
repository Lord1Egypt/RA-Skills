import type { Provider, Snapshot } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { codexbarAvailable, codexbarUsage, extractUsageSnapshot } from "../core/codexbar";
import { hermesEnv, nowIso, parseMoneyPrefix, toFloat } from "../core/env";
import { httpJson } from "../core/http";
import { baseSnapshot, errorSnapshot } from "../core/snapshot";

const BASE = "https://platform.xiaomimimo.com/api/v1";
const REFERER = "https://platform.xiaomimimo.com/#/console/balance";
type Obj = Record<string, unknown>;

const REQUIRED_COOKIES = ["api-platform_serviceToken", "userId"];

function resolveCookie(): { header: string; source: string } | { header: null; reason: string } {
  const explicit = hermesEnv("MIMO_COOKIE");
  if (explicit) return { header: explicit.trim(), source: "env:MIMO_COOKIE" };
  return {
    header: null,
    reason: "no MIMO_COOKIE set and Chrome cookie decryption not enabled on this host",
  };
}

/** CodexBar fallback: wallet balance from usage.details rows. */
function fromCodexbar(): Snapshot | null {
  const items = codexbarUsage("mimo");
  const item = items[0];
  if (!item) return null;
  const snap = extractUsageSnapshot(item);
  const usage = (item.usage ?? {}) as Obj;
  const details = Array.isArray(usage.details) ? (usage.details as Obj[]) : [];
  let currency = snap.currency ?? "CNY";
  for (const section of details) {
    const rows = Array.isArray(section.rows) ? (section.rows as Obj[]) : [];
    for (const row of rows) {
      if (String(row.label ?? "").toLowerCase() !== "balance") continue;
      const raw = String(row.value ?? "");
      const parsed = parseMoneyPrefix(raw);
      if (parsed !== null) snap.balance = parsed;
      if (raw.includes("CN¥") || raw.includes("CNY")) currency = "CNY";
    }
  }
  snap.source = "codexbar-fallback";
  snap.currency = currency;
  snap.details = {
    ...(snap.details ?? {}),
    fallbackReason: "no usable MiMo console cookie",
    cookieError: "MIMO_COOKIE not set",
  };
  snap.timestamp = nowIso();
  return snap;
}

export const mimoProvider: Provider = {
  id: "mimo",
  label: "Xiaomi MiMo",
  loginUrl: LOGIN_URLS.mimo,

  async detect() {
    const cookie = resolveCookie();
    if (cookie.header) return { configured: true, source: cookie.source };
    if (codexbarAvailable()) {
      return { configured: true, source: "codexbar-fallback" };
    }
    return { configured: false, reason: cookie.header === null ? cookie.reason : "unreachable" };
  },

  async fetch() {
    const cookie = resolveCookie();
    if (!cookie.header) {
      const fallback = fromCodexbar();
      if (fallback) return fallback;
      return errorSnapshot("mimo", `MiMo 凭据不可用 — set MIMO_COOKIE or log in to the console`, "codexbar-fallback", LOGIN_URLS.mimo);
    }

    const headers: Record<string, string> = {
      Cookie: cookie.header,
      Referer: REFERER,
      Origin: "https://platform.xiaomimimo.com",
    };

    const [status, balanceRaw] = await httpJson(`${BASE}/balance`, headers);
    if (status === 401 || status === 403) {
      return errorSnapshot("mimo", "Xiaomi MiMo session expired — log in again", "api", LOGIN_URLS.mimo);
    }
    const balanceData = typeof balanceRaw === "object" && balanceRaw !== null ? (balanceRaw as Obj) : {};
    const payload = (balanceData.data ?? {}) as Obj;
    if (status !== 200 || (balanceData.code !== 0 && balanceData.code != null) || !Object.keys(payload).length) {
      return errorSnapshot(
        "mimo",
        `MiMo balance rejected: ${String(balanceData.message ?? balanceData.code ?? `HTTP ${status}`)}`,
        "api",
        LOGIN_URLS.mimo,
      );
    }

    const [, usageRaw] = await httpJson(`${BASE}/usage`, headers);
    const usagePayload = ((usageRaw as Obj | null)?.data ?? {}) as Obj;
    const [, planRaw] = await httpJson(`${BASE}/tokenPlan/detail`, headers);
    const planPayload = ((planRaw as Obj | null)?.data ?? {}) as Obj;

    const tokenUsage = (usagePayload.tokenUsage ?? {}) as Obj;
    const costUsage = (usagePayload.costUsage ?? {}) as Obj;
    const periodEndRaw = planPayload.currentPeriodEnd;
    const resetsAt =
      typeof periodEndRaw === "string" && periodEndRaw
        ? `${periodEndRaw.replace(" ", "T")}Z` // console value has no offset; treated as UTC (same as CodexBar)
        : null;

    const snap = baseSnapshot("mimo", "api");
    snap.currency = (payload.currency as string | undefined) || "CNY";
    snap.balance = toFloat(payload.balance);
    snap.resetsAt = resetsAt;
    snap.monthCost = toFloat(costUsage.currentMonthCost);
    snap.monthPeriod = new Date().toISOString().slice(0, 7);
    snap.details = {
      credentialSource: cookie.source,
      cashBalance: toFloat(payload.cashBalance),
      giftBalance: toFloat(payload.giftBalance),
      frozenBalance: toFloat(payload.frozenBalance),
      overdraftLimit: toFloat(payload.overdraftLimit),
      totalCost: toFloat(costUsage.totalCost),
      totalToken: tokenUsage.totalToken ?? null,
      inputToken: tokenUsage.inputToken ?? null,
      outputToken: tokenUsage.outputToken ?? null,
      cacheToken: tokenUsage.cacheToken ?? null,
      rateLimitTpm: ((usagePayload.accountRateLimit ?? {}) as Obj).tpm ?? null,
      planName: planPayload.planName ?? null,
      planExpired: planPayload.expired ?? null,
      autoRenew: planPayload.enableAutoRenew ?? null,
      planPeriodEndRaw: periodEndRaw ?? null,
      requiredCookies: REQUIRED_COOKIES,
    };
    return snap;
  },
};
