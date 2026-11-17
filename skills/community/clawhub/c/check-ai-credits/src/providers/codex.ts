import path from "node:path";
import { homedir } from "node:os";
import type { Provider, Snapshot } from "../types";
import { LOGIN_URLS } from "../core/auth";
import { isoFromEpoch, readJson, toFloat } from "../core/env";
import { httpJson } from "../core/http";
import { baseSnapshot, errorSnapshot } from "../core/snapshot";

const USAGE_URL = "https://chatgpt.com/backend-api/wham/usage";
const RESET_CREDITS_URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits";

type Obj = Record<string, unknown>;

function authPath(): string {
  const home = process.env.CODEX_HOME;
  return home ? path.join(home, "auth.json") : path.join(homedir(), ".codex", "auth.json");
}

interface AuthShape {
  tokens?: { access_token?: string; account_id?: string };
}

/** Read-only: the access token is used as-is; NEVER refreshed (refreshing would
 *  rotate the Codex CLI's own refresh token and log the user out). */
export const codexProvider: Provider = {
  id: "codex",
  label: "Codex (ChatGPT)",
  loginUrl: LOGIN_URLS.codex,

  async detect() {
    const auth = readJson<AuthShape>(authPath());
    return auth?.tokens?.access_token
      ? { configured: true, source: authPath() }
      : { configured: false, reason: `no access_token in ${authPath()}` };
  },

  async fetch() {
    const auth = readJson<AuthShape>(authPath());
    const tokens = auth?.tokens ?? {};
    if (!tokens.access_token) {
      return errorSnapshot(
        "codex",
        "codex auth token is expired or missing (no access_token in auth store)",
        "api",
        LOGIN_URLS.codex,
      );
    }
    const headers: Record<string, string> = {
      Authorization: `Bearer ${tokens.access_token}`,
      "ChatGPT-Account-Id": tokens.account_id ?? "",
      Origin: "https://chatgpt.com",
      Referer: "https://chatgpt.com/codex/settings/usage",
    };

    const [status, data] = await httpJson(USAGE_URL, headers);
    if (status === 401 || status === 403) {
      return errorSnapshot(
        "codex",
        "auth token is expired — run the codex CLI once to refresh",
        "api",
        LOGIN_URLS.codex,
      );
    }
    if (status !== 200 || typeof data !== "object" || data === null) {
      return errorSnapshot("codex", `chatgpt.com usage request failed (HTTP ${status})`);
    }

    const body = data as Obj;
    const rate = (body.rate_limit ?? {}) as Obj;
    const primary = (rate.primary_window ?? {}) as Obj;
    const secondary = (rate.secondary_window ?? {}) as Obj;
    const credits = (body.credits ?? {}) as Obj;

    const snap = baseSnapshot("codex", "api");
    snap.currency = "USD";
    snap.balance = toFloat(credits.balance);
    snap.usedPercent = toFloat(primary.used_percent);
    snap.resetsAt = isoFromEpoch(primary.reset_at);
    snap.details = {
      accountEmail: body.email,
      planType: body.plan_type,
      hasCredits: credits.has_credits,
      creditsUnlimited: credits.unlimited,
      windowMinutes:
        typeof primary.limit_window_seconds === "number"
          ? Math.round(primary.limit_window_seconds / 60)
          : null,
      secondaryUsedPercent: toFloat(secondary.used_percent),
      secondaryResetsAt: isoFromEpoch(secondary.reset_at),
      rateLimitReached: rate.limit_reached,
      resetCreditsAvailable: (body.rate_limit_reset_credits as Obj | undefined)?.available_count ?? null,
    };

    // optional: names/expiry of redeemable full-reset credits
    const [status2, resets] = await httpJson(RESET_CREDITS_URL, headers);
    if (status2 === 200 && typeof resets === "object" && resets !== null) {
      const items = ((resets as Obj).credits as Obj[] | undefined) ?? [];
      (snap.details as Record<string, unknown>).resetCreditItems = items
        .filter((c) => c.status === "available")
        .map((c) => ({ title: c.title, expiresAt: c.expires_at }));
    }
    return snap;
  },
};
