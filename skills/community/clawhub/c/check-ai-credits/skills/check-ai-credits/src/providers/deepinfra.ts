import type { FetchOptions, Provider, Snapshot } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { hermesEnv, toFloat } from "../core/env";
import { httpJson } from "../core/http";
import { baseSnapshot, errorSnapshot } from "../core/snapshot";

const BASE = "https://api.deepinfra.com";

type Obj = Record<string, unknown>;

async function apiGet(path: string, key: string, retries = 0): Promise<[Obj | null, string | null]> {
  let lastErr: string | null = null;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const [status, data] = await httpJson(`${BASE}${path}`, { Authorization: `Bearer ${key}` });
    if (status === 401) return [null, "auth: API key rejected (HTTP 401) — create a new key at https://deepinfra.com/dash"];
    if (status === 403) return [null, "auth: key cannot access billing data (HTTP 403)"];
    if (status === 200 && typeof data === "object" && data !== null) return [data as Obj, null];
    lastErr = typeof data === "string" ? `http ${status}: ${data.slice(0, 200)}` : `http ${status}`;
    if (attempt < retries) await new Promise((r) => setTimeout(r, 2000));
  }
  return [null, lastErr];
}

/** Pure computation from the 3 billing endpoints -> snapshot fields.
 *  Unit rules (verified): checklist amounts are USD; /payment/usage costs are CENTS. */
export function calcDeepinfra(
  checklist: Obj,
  usage: Obj | null,
  config: Obj | null,
  withModels = false,
): Snapshot {
  const snap = baseSnapshot("deepinfra", "deepinfra-api");
  const rawStripe = Number(checklist.stripe_balance ?? 0) || 0;
  const recent = Math.max(0, Number(checklist.recent ?? 0) || 0);
  const credit = rawStripe < 0 ? -rawStripe : 0;
  const owed = rawStripe > 0 ? rawStripe : 0;
  const spendable = Math.round((credit - recent) * 1e6) / 1e6;

  let limit = checklist.limit;
  if (limit === undefined && config && config.limit !== undefined) limit = config.limit;
  const limitNum = toFloat(limit);

  const details: Record<string, unknown> = {
    creditUsd: Math.round(credit * 1e6) / 1e6,
    unbilledUsd: Math.round(recent * 1e6) / 1e6,
    owedUsd: Math.round(owed * 1e6) / 1e6,
    spendableUsd: spendable,
    suspended: Boolean(checklist.suspended),
    suspendReason: checklist.suspend_reason ?? null,
    overdueInvoices: Number(checklist.overdue_invoices ?? 0) || 0,
    billingType: checklist.billing_type ?? null,
    stripeBalanceRaw: rawStripe,
    limitUsd: limitNum !== null && limitNum > 0 ? limitNum : null,
    topup: {
      enabled: Boolean(checklist.topup),
      amountUsd: Math.round(Number(checklist.topup_amount ?? 0) || 0) / 100,
      thresholdUsd: Math.round(Number(checklist.topup_threshold ?? 0) || 0) / 100,
      failed: Boolean(checklist.topup_failed),
    },
  };

  snap.balance = spendable;
  snap.currency = "USD";

  const months = usage && Array.isArray(usage.months) ? (usage.months as Obj[]) : [];
  const month = months[months.length - 1];
  if (month) {
    const totalCents = Number(month.total_cost ?? 0) || 0;
    const monthCost = Math.round((totalCents / 100) * 1e6) / 1e6;
    snap.monthCost = monthCost;
    snap.monthPeriod = typeof month.period === "string" ? month.period : null;
    details.monthInvoiceId = month.invoice_id ?? null;
    if (withModels && Array.isArray(month.items)) {
      const perModel = new Map<string, number>();
      for (const raw of month.items as Obj[]) {
        const model = raw.model as Obj | undefined;
        const name = (model?.model_name as string | undefined) ?? "unknown";
        const cost = (Number(raw.cost ?? 0) || 0) / 100;
        perModel.set(name, (perModel.get(name) ?? 0) + cost);
      }
      details.models = [...perModel.entries()]
        .map(([model, costUsd]) => ({ model, costUsd: Math.round(costUsd * 1e6) / 1e6 }))
        .filter((row) => row.costUsd > 0)
        .sort((a, b) => b.costUsd - a.costUsd);
    }
  }
  snap.details = details;
  return snap;
}

export const deepinfraProvider: Provider = {
  id: "deepinfra",
  label: "DeepInfra",
  loginUrl: LOGIN_URLS.deepinfra,

  async detect() {
    const key = hermesEnv("DEEPINFRA_API_KEY") ?? hermesEnv("DEEPINFRA_TOKEN");
    return key
      ? { configured: true, source: "DEEPINFRA_API_KEY" }
      : { configured: false, reason: "DEEPINFRA_API_KEY missing (env or $HERMES_HOME/.env)" };
  },

  async fetch(opts?: FetchOptions) {
    const key = hermesEnv("DEEPINFRA_API_KEY") ?? hermesEnv("DEEPINFRA_TOKEN");
    if (!key) {
      return errorSnapshot(
        "deepinfra",
        "DEEPINFRA_API_KEY missing (env or $HERMES_HOME/.env)",
        "deepinfra-api",
        LOGIN_URLS.deepinfra,
      );
    }
    const [checklist, err] = await apiGet("/payment/checklist?compute_owed=true", key);
    if (err || !checklist) {
      return errorSnapshot("deepinfra", err ?? "billing checklist failed", "deepinfra-api");
    }
    const [usage] = await apiGet("/payment/usage?from=current", key, 1);
    const [config] = await apiGet("/payment/config", key);
    const snap = calcDeepinfra(checklist, usage, config, opts?.models ?? false);
    if (snap.error === null && snap.monthCost === null && !usage) {
      snap.details = { ...(snap.details ?? {}), usageError: "month usage unavailable" };
    }
    return snap;
  },
};
