/**
 * Carbium — Connection setup and retry helper
 *
 * Copy this file as a starting point for any Carbium integration.
 *
 * Prerequisites:
 *   npm install @solana/web3.js
 *   export CARBIUM_RPC_KEY="your-rpc-key"
 *   export CARBIUM_API_KEY="your-swap-api-key"
 */

import { Connection } from "@solana/web3.js";

// --- Environment ---

const CARBIUM_RPC_KEY = process.env.CARBIUM_RPC_KEY;
const CARBIUM_API_KEY = process.env.CARBIUM_API_KEY;

if (!CARBIUM_RPC_KEY) throw new Error("CARBIUM_RPC_KEY not set");

// --- RPC Connection (with WebSocket) ---

export const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${CARBIUM_RPC_KEY}`,
  {
    commitment: "confirmed",
    wsEndpoint: `wss://wss-rpc.carbium.io/?apiKey=${CARBIUM_RPC_KEY}`,
  }
);

// --- Swap API helper ---

export async function carbiumApi(
  path: string,
  params: Record<string, string>
): Promise<any> {
  if (!CARBIUM_API_KEY) throw new Error("CARBIUM_API_KEY not set");

  const url = new URL(`https://api.carbium.io/api/v2${path}`);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, v);
  }

  const res = await fetch(url, {
    headers: { "X-API-KEY": CARBIUM_API_KEY },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Carbium API ${res.status}: ${text}`);
  }

  return res.json();
}

// --- Retry with exponential backoff ---

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function withRetry<T>(
  fn: () => Promise<T>,
  retries = 3,
  baseMs = 300
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === retries - 1) throw e;
      await delay(baseMs * 2 ** i + Math.random() * 100);
    }
  }
  throw new Error("unreachable");
}

// --- Common token mints ---

export const MINTS = {
  SOL: "So11111111111111111111111111111111111111112",
  USDC: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  USDT: "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
} as const;
