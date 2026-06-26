import type { Request, Response, NextFunction } from "express";
import crypto from "node:crypto";
import { env } from "../config/env";
import {
  findCreationTier,
  findFundingTier,
  toAtomicUsdc
} from "../config/pricing";
import { paymentService } from "../services/paymentService";
import { emitMetric, startTimer } from "../services/metrics";
import type {
  PaymentPayload,
  PaymentRequired,
  PaymentRequirements,
} from "../types/x402";

type PaidPurpose = "create" | "fund";

const getChallengeDescription = (purpose: PaidPurpose, amount: number): string => {
  if (purpose === "create") {
    return `Create ASG Card with $${amount} load`;
  }
  return `Fund ASG Card with $${amount}`;
};

// ── Rollout gate ─────────────────────────────────────────────

/**
 * Deterministic hash-based rollout check.
 * Uses SHA-256(payer) mod 100 < ROLLOUT_PCT.
 * Requires a valid payer identifier; requests without one are excluded
 * from the paid path (never routed through gate).
 */
function isInRollout(payer: string): boolean {
  // Kill-switch — immediate off
  if (env.ROLLOUT_ENABLED !== "true") return false;

  // ROLLOUT_PCT=0 — all gated
  if (env.ROLLOUT_PCT <= 0) return false;

  // ROLLOUT_PCT >= 100 — all pass
  if (env.ROLLOUT_PCT >= 100) return true;

  // Deterministic: SHA-256(payer) mod 100 < ROLLOUT_PCT
  const hash = crypto.createHash("sha256").update(payer).digest();
  const bucket = hash.readUInt16BE(0) % 100;
  return bucket < env.ROLLOUT_PCT;
}

/**
 * Build x402 v2 PaymentRequired (402 response)
 */
const buildChallenge = (
  req: Request,
  amount: number,
  requiredAtomic: string,
  purpose: PaidPurpose
): PaymentRequired => ({
  x402Version: 2,
  resource: {
    url: `https://${req.get("host")}${req.originalUrl}`,
    description: getChallengeDescription(purpose, amount),
    mimeType: "application/json",
  },
  accepts: [
    {
      scheme: "exact",
      network: env.STELLAR_NETWORK,
      amount: requiredAtomic,
      payTo: env.STELLAR_TREASURY_ADDRESS,
      maxTimeoutSeconds: 300,
      asset: env.STELLAR_USDC_ASSET,
      extra: { areFeesSponsored: true },
    }
  ]
});

/**
 * Parse v2 PaymentPayload from X-PAYMENT header.
 * Header value is Base64-encoded JSON: {x402Version, accepted, payload:{transaction}}
 */
const parsePaymentPayload = (headerValue: string): PaymentPayload | null => {
  try {
    // Try raw JSON first
    let parsed: unknown;
    try {
      parsed = JSON.parse(headerValue);
    } catch {
      // Try base64 decode
      const decoded = Buffer.from(headerValue, "base64").toString("utf8");
      parsed = JSON.parse(decoded);
    }

    const pp = parsed as PaymentPayload;

    // Validate v2 structure
    if (pp.x402Version !== 2) return null;
    if (!pp.accepted || !pp.payload) return null;
    if (!("transaction" in pp.payload) || typeof pp.payload.transaction !== "string") return null;

    return pp;
  } catch {
    return null;
  }
};

export const requireX402Payment = (purpose: PaidPurpose) => {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const elapsed = startTimer();
    const metricEvent = purpose === "create" ? "request_create" as const : "request_fund" as const;

    const amount = Number(req.params.amount);
    const tier = purpose === "create" ? findCreationTier(amount) : findFundingTier(amount);

    if (!tier) {
      res.status(400).json({ error: "Unsupported tier amount" });
      return;
    }

    const requiredAtomic = toAtomicUsdc(tier.totalCost);

    // ── Check for payment header (canonical X-PAYMENT, legacy X-Payment) ──
    const paymentHeader = req.header("X-PAYMENT") ?? req.header("X-Payment");

    if (!paymentHeader) {
      res.status(402).json(buildChallenge(req, amount, requiredAtomic, purpose));
      return;
    }

    // ── Parse v2 PaymentPayload ──────────────────────
    const paymentPayload = parsePaymentPayload(paymentHeader);

    if (!paymentPayload) {
      res.status(401).json({ error: "Invalid X-PAYMENT header: expected x402 v2 PaymentPayload" });
      return;
    }

    // ── Validate accepted requirements match ours ────
    const accepted = paymentPayload.accepted;
    if (accepted.scheme !== "exact" || accepted.network !== env.STELLAR_NETWORK) {
      res.status(401).json({ error: "Unsupported payment scheme or network" });
      return;
    }

    if (accepted.payTo !== env.STELLAR_TREASURY_ADDRESS) {
      res.status(401).json({ error: "Payment recipient mismatch" });
      return;
    }

    // ── Rollout gate ─────────────────────────────────
    // Use payTo as deterministic payer identifier
    const payerIdentifier = accepted.payTo;
    if (!isInRollout(payerIdentifier)) {
      const reason = env.ROLLOUT_ENABLED !== "true"
        ? "rollout_kill_switch"
        : "rollout_gated";
      emitMetric({
        eventType: reason === "rollout_kill_switch" ? "rollout_kill_switch" : "rollout_gated",
        metadata: { pct: env.ROLLOUT_PCT }
      });
      res.status(503)
        .set("Retry-After", "300")
        .json({ error: "Service temporarily unavailable", retryAfter: 300 });
      return;
    }

    // ── Build server-side PaymentRequirements ────────
    const paymentRequirements: PaymentRequirements = {
      scheme: "exact",
      network: env.STELLAR_NETWORK,
      amount: requiredAtomic,
      payTo: env.STELLAR_TREASURY_ADDRESS,
      maxTimeoutSeconds: 300,
      asset: env.STELLAR_USDC_ASSET,
      extra: { areFeesSponsored: true },
    };

    // ── Verify + Settle via facilitator ──────────────
    const result = await paymentService.verifyAndSettle({
      paymentPayload,
      paymentRequirements,
      payer: accepted.payTo,  // will be overridden by facilitator's payer field
      tierAmount: amount as 10 | 25 | 50 | 100 | 200 | 500,
    });

    if (!result.valid) {
      const isFacilitatorDown = result.error?.includes("Payment verification failed:");
      const statusCode = isFacilitatorDown ? 503 : 401;
      emitMetric({
        eventType: metricEvent,
        latencyMs: elapsed(),
        metadata: { status: statusCode, error: result.error?.substring(0, 100) }
      });
      res.status(statusCode).json({
        error: result.error ?? "Payment verification failed"
      });
      return;
    }

    // ── Success: emit metric + populate context ─────
    emitMetric({
      eventType: metricEvent,
      latencyMs: elapsed(),
      metadata: { status: 201 }
    });

    req.paymentContext = {
      payer: result.settleResponse?.payer ?? "",
      txHash: result.settleResponse?.transaction ?? "",
      atomicAmount: requiredAtomic,
      tierAmount: amount as 10 | 25 | 50 | 100 | 200 | 500,
      totalCostUsd: tier.totalCost
    };

    next();
  };
};
