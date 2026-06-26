/**
 * fraud-filter OpenClaw plugin entry point.
 *
 * Registers two hooks:
 *
 * 1. before_tool_call — enforcement layer.
 *    Checks the payment endpoint against the trust database and hotlist.
 *    Blocks or warns based on the configured on_block / on_caution policy.
 *    Fails open — any internal error allows the call through.
 *
 * 2. tool_result_persist — observation layer.
 *    Detects failed payment outcomes and queues anonymous reports.
 *    Covers both post_payment_failure (paid, received nothing) and
 *    pre_payment_failure (endpoint unreachable before payment).
 *
 * The two hooks share state via pendingPayments (keyed by toolCallId) so that
 * tool_result_persist has access to the endpoint URL extracted in before_tool_call.
 */

import { checkEndpoint, loadConfig } from "./trust-db.js";
import { queueReport } from "./reporter.js";
import { syncHotlist } from "./hotlist-sync.js";

const PAYMENT_PATTERNS = [
  /pay/i, /purchase/i, /checkout/i, /buy/i, /wallet/i,
  /v402/i, /x402/i, /clawrouter/i, /stripe/i, /paypal/i,
  /payment[_-]?skill/i,
];

// Bridge: before_tool_call stashes the URL here so tool_result_persist can use it.
// Keyed by toolCallId. Cleaned up after each tool_result_persist fires.
const pendingPayments = new Map();

function extractUrl(params) {
  const str = typeof params === "string" ? params : JSON.stringify(params ?? {});
  const match = str.match(/https?:\/\/[^\s"\\]+/);
  return match ? match[0] : null;
}

function isGarbage(str) {
  if (!str || str.trim() === "") return true;
  const t = str.trim();
  if (t === "null" || t === "{}" || t === "[]" || t === '""') return true;
  try {
    const parsed = JSON.parse(str);
    if (parsed && typeof parsed === "object" && (parsed.error || parsed.Error)) return true;
  } catch {}
  return false;
}

function looksLikePrePayment(str) {
  return /dns|enotfound|econnrefused|econnreset|etimedout|unreachable|network error|connection refused/i.test(
    str
  );
}

export function register(api) {

  // Sync hotlist on load, then refresh every hour.
  // Runs in the background — never blocks registration.
  // Download-only (no user data sent). Disable with sync_hotlist: false in config.
  const cfg = loadConfig();
  if (cfg.sync_hotlist !== false) {
    syncHotlist();
    setInterval(syncHotlist, 60 * 60 * 1000);
  }

  // ── Enforcement ─────────────────────────────────────────────────────────────
  // Fires before the tool executes. Checks endpoint trust; blocks or warns.

  api.on("before_tool_call", async (event, ctx) => {
    const { toolName, params, toolCallId } = event;

    if (!PAYMENT_PATTERNS.some((p) => p.test(toolName))) return { params };

    const url = extractUrl(params);
    if (!url) return { params };

    // Stash URL for tool_result_persist.
    if (toolCallId) pendingPayments.set(toolCallId, { url, toolName });

    let assessment, config;
    try {
      assessment = checkEndpoint(url);
      config = loadConfig();
    } catch {
      return { params }; // fail open — never block due to internal error
    }

    const onBlock   = config.on_block   || "block";
    const onCaution = config.on_caution || "warn";

    if (assessment.recommendation === "block") {
      const reason = assessment.hotlisted
        ? "hotlisted — surge of recent failure reports"
        : `satisfaction score ${assessment.score}/100`;
      if (onBlock === "block") {
        return {
          block: true,
          blockReason: `fraud-filter: blocked payment to ${url} (${reason})`,
        };
      }
      // onBlock === "warn" — let it through
      return { params };
    }

    if (assessment.recommendation === "caution") {
      if (onCaution === "block") {
        return {
          block: true,
          blockReason: `fraud-filter: blocked payment to ${url} (caution — score ${assessment.score}/100)`,
        };
      }
      // "warn" or "allow" — let it through
      return { params };
    }

    return { params };
  });

  // ── Observation ──────────────────────────────────────────────────────────────
  // Fires after the tool completes. Queues a report if the outcome was a failure.

  api.on("tool_result_persist", (event, ctx) => {
    const { toolName, toolCallId, message } = event;

    // Retrieve URL stashed by before_tool_call, fall back to event.params.
    const pending = toolCallId ? pendingPayments.get(toolCallId) : null;
    if (toolCallId) pendingPayments.delete(toolCallId);

    // If before_tool_call didn't stash (e.g., no toolCallId), check pattern here.
    const effectiveToolName = pending?.toolName ?? toolName;
    if (!pending && !PAYMENT_PATTERNS.some((p) => p.test(effectiveToolName))) return;

    const url = pending?.url ?? extractUrl(event.params ?? {});
    if (!url) return;

    // Normalize tool result from the message content.
    const toolResult =
      typeof message?.content === "string"
        ? message.content
        : Array.isArray(message?.content)
        ? message.content.map((b) => b.text ?? b.content ?? "").join("")
        : JSON.stringify(message?.content ?? "");

    if (!isGarbage(toolResult)) return;

    const outcome = looksLikePrePayment(toolResult)
      ? "pre_payment_failure"
      : "post_payment_failure";

    queueReport({
      endpoint_url: url,
      outcome,
      amount_usd:   "0",
      reason:       `Payment tool returned empty or error response. Tool: ${effectiveToolName}`,
    });
  });
}
