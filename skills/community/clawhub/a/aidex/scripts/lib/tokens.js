// Local token registry for the AIDEX skill.
// The registry is a copy of the server token list bundled with the skill,
// used as an independent anchor for swap transaction validation.

import { readFileSync } from "fs";

const TOKENS = JSON.parse(
  readFileSync(new URL("../data/tokens.json", import.meta.url), "utf8")
);

const TOKENS_BY_ADDRESS = new Map();
const TOKENS_BY_SYMBOL = new Map();
for (const token of TOKENS) {
  const address = token.address.toLowerCase();
  const symbol = token.symbol.toLowerCase();
  if (TOKENS_BY_ADDRESS.has(address)) {
    throw new Error(`Duplicate token address in registry: ${address}`);
  }
  if (TOKENS_BY_SYMBOL.has(symbol)) {
    throw new Error(`Duplicate token symbol in registry: ${symbol}`);
  }
  TOKENS_BY_ADDRESS.set(address, token);
  TOKENS_BY_SYMBOL.set(symbol, token);
}

/**
 * Resolves a token by symbol or address against the local registry.
 * Mirrors the server resolution rules: 0x-prefixed 42-char strings are looked up by address,
 * everything else is treated as a symbol. Comparisons are case-insensitive.
 * Returns the full token object ({address, symbol, decimals, name, imageUrl}) or null.
 */
export function resolveToken(symbolOrAddress) {
  if (symbolOrAddress.startsWith("0x") && symbolOrAddress.length === 42) {
    if (!/^0x[0-9a-fA-F]{40}$/.test(symbolOrAddress)) return null;
    return TOKENS_BY_ADDRESS.get(symbolOrAddress.toLowerCase()) ?? null;
  }
  return TOKENS_BY_SYMBOL.get(symbolOrAddress.toLowerCase()) ?? null;
}
