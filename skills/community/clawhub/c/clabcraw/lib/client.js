/**
 * x402 payment and signing helpers for Clabcraw skill scripts.
 *
 * Provides:
 * - createSigner(privateKey) — viem account from private key
 * - createPaymentFetch(signer) — fetch wrapper that auto-handles x402 402 flows
 */

import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

/**
 * Create a viem account from a hex private key.
 * Accepts with or without "0x" prefix.
 */
export function createSigner(privateKey) {
  const key = privateKey.startsWith("0x") ? privateKey : `0x${privateKey}`;
  return privateKeyToAccount(key);
}

/**
 * Create a fetch function that automatically handles x402 payment flows.
 * When a request returns HTTP 402, the wrapper signs a USDC authorization
 * and retries with the payment-signature header.
 */
export function createPaymentFetch(signer) {
  const client = new x402Client();
  registerExactEvmScheme(client, { signer });
  return wrapFetchWithPayment(fetch, client);
}
