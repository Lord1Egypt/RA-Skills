#!/usr/bin/env node
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

export const SWAP_ROUTER02 = "0x2626664c2603336E57B271c5C0b26F421741e481";
export const PERMIT2 = "0x000000000022D473030F116dDEE9F6B43aC78BA3";
export const UNIVERSAL_ROUTER = "0x6fF5693b99212Da76ad316178A184AB56D299b43";
export const UNIVERSAL_ROUTER_V1_2 = "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD";
export const UNIVERSAL_ROUTER_V2_1_1 = "0xFdf682F51FE81Aa4898F0AE2163d8A55c127fbC7";
export const APPROVE_SELECTOR = "095ea7b3";
export const CHAIN_ID = "8453";
const UINT_MAX = (1n << 256n) - 1n;
const UNLIMITED_MIN = 1n << 255n;

export const UNISWAP_SPENDERS = [
  SWAP_ROUTER02,
  PERMIT2,
  UNIVERSAL_ROUTER,
  UNIVERSAL_ROUTER_V1_2,
  UNIVERSAL_ROUTER_V2_1_1,
].map((a) => a.toLowerCase());

const TICKERS = {
  usdc: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  usd: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  weth: "0x4200000000000000000000000000000000000006",
  eth: "0x4200000000000000000000000000000000000006",
  cbbtc: "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
  btc: "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
};

export function resolveTokenIn(raw) {
  const s = String(raw || "").trim();
  if (/^0x[0-9a-fA-F]{40}$/.test(s)) return s.toLowerCase();
  const mapped = TICKERS[s.toLowerCase()];
  return mapped ? mapped.toLowerCase() : null;
}

function normAddr(raw) {
  const s = String(raw || "").trim().toLowerCase();
  return /^0x[0-9a-f]{40}$/.test(s) ? s : null;
}

function parseAmount(raw) {
  try {
    return BigInt(String(raw ?? "").trim());
  } catch {
    return null;
  }
}

export function verifyApprove(input) {
  const chainId = String(input.chainId ?? "").trim();
  if (chainId !== CHAIN_ID) return { ok: false, error: "chainId must be 8453" };

  const tokenIn = resolveTokenIn(input.tokenIn);
  if (!tokenIn) return { ok: false, error: "tokenIn is not a known ticker or 0x address" };

  const to = normAddr(input.to);
  if (!to) return { ok: false, error: "to is not a 0x address" };
  if (to !== tokenIn) return { ok: false, error: "to must equal locally resolved tokenIn" };

  const amountIn = parseAmount(input.amountIn);
  if (amountIn === null) return { ok: false, error: "amountIn must be an integer string" };
  if (amountIn < 0n) return { ok: false, error: "amountIn must be >= 0 (0 = revoke)" };

  let value = 0n;
  if (input.value != null && String(input.value).trim() !== "") {
    const v = parseAmount(input.value);
    if (v === null) return { ok: false, error: "value must be an integer" };
    value = v;
  }
  if (value !== 0n) return { ok: false, error: "native value must be 0" };

  const data = String(input.data ?? input.calldata ?? "").trim().toLowerCase();
  if (!data.startsWith("0x")) return { ok: false, error: "data must be 0x-hex" };
  const hex = data.slice(2);
  if (!/^[0-9a-f]*$/.test(hex)) return { ok: false, error: "data is not hex" };
  if (hex.length !== 136) return { ok: false, error: "approve calldata must be exactly 68 bytes" };
  if (hex.slice(0, 8) !== APPROVE_SELECTOR) {
    return { ok: false, error: "selector must be approve(address,uint256) 0x095ea7b3" };
  }

  const spenderWord = hex.slice(8, 72);
  const amountWord = hex.slice(72, 136);
  if (spenderWord.slice(0, 24) !== "0".repeat(24)) {
    return { ok: false, error: "spender word is not a 20-byte address" };
  }
  const spender = "0x" + spenderWord.slice(24);
  if (!UNISWAP_SPENDERS.includes(spender)) {
    return { ok: false, error: "spender must be allowlisted Uniswap SwapRouter02, Permit2, or Universal Router on Base" };
  }

  const amount = BigInt("0x" + amountWord);
  if (amount !== amountIn) return { ok: false, error: "approve amount must equal amountIn" };
  if (amount === UINT_MAX || amount >= UNLIMITED_MIN) {
    return { ok: false, error: "unlimited / max uint approve rejected" };
  }

  return {
    ok: true,
    chainId: Number(CHAIN_ID),
    token: to,
    spender,
    amount: amount.toString(),
  };
}

function parseArgs(argv) {
  const o = {};
  for (let i = 2; i < argv.length; i += 1) {
    const k = argv[i];
    if (!k.startsWith("--")) continue;
    o[k.slice(2)] = argv[i + 1];
    i += 1;
  }
  return o;
}

function main() {
  const r = verifyApprove(parseArgs(process.argv));
  if (!r.ok) {
    console.error(r.error);
    process.exit(1);
  }
  console.log(JSON.stringify(r));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
