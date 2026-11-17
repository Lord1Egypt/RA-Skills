// Relay (relay.link) moves value between Solana and Robinhood Chain in about a second. `fund` uses it to bring USDC
// from Solana; every quote is checked against what goes in before anything is signed, so a bad price stops the move
// instead of costing the worker.

import type { Address, Hex } from "viem";

export const RELAY_API = "https://api.relay.link";
export const SOLANA_CHAIN_ID = 792703809;
/** USDC on Solana. */
export const SOLANA_USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";
export const NATIVE = "0x0000000000000000000000000000000000000000";
/** The most a move may cost, as a share of its dollar value; small moves may cost up to FIXED_LOSS_USD instead. */
export const MAX_LOSS = 0.03;
/** The stake token's market alone costs about 3.7% at any size on top of Relay's fee, so the stake leg gets more room. */
export const MAX_STAKE_LOSS = 0.05;
/** Relay's fee is partly fixed (about 0.2 USD), so a small move is allowed to lose up to this much in dollars. */
export const FIXED_LOSS_USD = 0.5;

export interface EvmItem {
  to: Address;
  data: Hex;
  value: string;
  chainId: number;
}

export interface SvmItem {
  instructions: { keys: { pubkey: string; isSigner: boolean; isWritable: boolean }[]; programId: string; data: string }[];
  addressLookupTableAddresses: string[];
}

export interface RelayQuote {
  requestId: string;
  steps: { id: string; requestId?: string; items: { data: EvmItem | SvmItem }[] }[];
  inUsd: number;
  outUsd: number;
  outAmount: bigint;
  outFormatted: string;
  /** Who the quote pays and in what, as its details name them. */
  recipient?: string;
  outCurrency?: string;
  outChainId?: number;
}

export interface QuoteRequest {
  user: string;
  recipient: string;
  originChainId: number;
  destinationChainId: number;
  originCurrency: string;
  destinationCurrency: string;
  amount: bigint;
}

export class RelayError extends Error {}

export async function relayQuote(request: QuoteRequest, fetchImpl: typeof fetch = fetch): Promise<RelayQuote> {
  const response = await fetchImpl(`${RELAY_API}/quote`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ ...request, amount: request.amount.toString(), tradeType: "EXACT_INPUT" }),
    signal: AbortSignal.timeout(30_000),
  });
  const body = (await response.json().catch(() => ({}))) as Record<string, any>;
  if (!response.ok || !body.details || !Array.isArray(body.steps)) {
    throw new RelayError(`Relay has no route for this move right now${body.message ? `: ${body.message}` : ""}`);
  }
  const requestId = body.steps.find((s: { requestId?: string }) => s.requestId)?.requestId;
  if (!requestId) throw new RelayError("Relay's quote carries no request id to follow");
  const out = body.details.currencyOut;
  return {
    requestId,
    steps: body.steps,
    inUsd: Number(body.details.currencyIn?.amountUsd ?? 0),
    outUsd: Number(out?.amountUsd ?? 0),
    outAmount: /^\d+$/.test(String(out?.amount)) ? BigInt(out.amount) : 0n,
    outFormatted: String(out?.amountFormatted ?? "0"),
    recipient: body.details.recipient,
    outCurrency: out?.currency?.address,
    outChainId: out?.currency?.chainId,
  };
}

/** Refuses a quote that loses more than `maxLoss` of its dollar value, or FIXED_LOSS_USD on a small move. */
export function checkReturn(quote: Pick<RelayQuote, "inUsd" | "outUsd">, maxLoss = MAX_LOSS): void {
  if (!(quote.inUsd > 0)) throw new RelayError("Relay's quote has no dollar value for what goes in, so its price cannot be checked");
  const loss = quote.inUsd - quote.outUsd;
  const allowed = Math.max(quote.inUsd * maxLoss, FIXED_LOSS_USD);
  if (loss > allowed) {
    throw new RelayError(`Relay would keep ${loss.toFixed(2)} USD of ${quote.inUsd.toFixed(2)}, more than the ${allowed.toFixed(2)} this command accepts (${Math.round(maxLoss * 100)}%, or 0.50 USD on a small move). Nothing was sent; try again later.`);
  }
}

export type RelayStatus = "success" | "failure" | "refund" | "pending";

export async function relayStatus(requestId: string, fetchImpl: typeof fetch = fetch): Promise<RelayStatus> {
  const response = await fetchImpl(`${RELAY_API}/intents/status/v2?requestId=${encodeURIComponent(requestId)}`, { signal: AbortSignal.timeout(20_000) });
  const body = (await response.json().catch(() => ({}))) as { status?: string };
  if (body.status === "success" || body.status === "failure" || body.status === "refund") return body.status;
  return "pending";
}

/** Follows a move until Relay answers anything but pending, for at most `ms`. Its `failure` is usually not final: Relay can still retry or refund. */
export async function waitForRelay(requestId: string, ms = 600_000, fetchImpl: typeof fetch = fetch, sleep = (t: number) => new Promise((r) => setTimeout(r, t))): Promise<RelayStatus> {
  const end = Date.now() + ms;
  for (;;) {
    const status = await relayStatus(requestId, fetchImpl).catch(() => "pending" as const);
    if (status !== "pending" || Date.now() > end) return status;
    await sleep(3_000);
  }
}
