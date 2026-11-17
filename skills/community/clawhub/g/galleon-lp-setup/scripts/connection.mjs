#!/usr/bin/env node
import { pathToFileURL } from "node:url";
import { realpathSync } from "node:fs";

const quantity = (value) => typeof value === "string" && /^0x(?:0|[1-9a-f][0-9a-f]*)$/i.test(value);
const failure = (code) => { throw new Error(code); };

export async function diagnose({ url, expectedChainId, maxAgeSeconds = 180, timeoutMs = 10000, fetcher = fetch, now = Date.now() }) {
  if (!/^[1-9][0-9]*$/.test(String(expectedChainId)) || !Number.isFinite(maxAgeSeconds) || maxAgeSeconds < 1) failure("INVALID_INPUT");
  if (!url) failure("MISSING_RPC_URL");
  let endpoint;
  try { endpoint = new URL(url); } catch { failure("INVALID_RPC_URL"); }
  if (!["https:", "http:"].includes(endpoint.protocol) || (endpoint.protocol === "http:" && !["localhost", "127.0.0.1", "[::1]"].includes(endpoint.hostname))) failure("INVALID_RPC_URL");
  async function read(method, params, id) {
    let response;
    try {
      response = await fetcher(endpoint.href, { method: "POST", redirect: "error", headers: { "content-type": "application/json" }, body: JSON.stringify({ jsonrpc: "2.0", id, method, params }), signal: AbortSignal.timeout(timeoutMs) });
    } catch { failure("RPC_UNAVAILABLE"); }
    if (!response.ok) failure("RPC_HTTP_ERROR");
    let body;
    try { body = await response.json(); } catch { failure("MALFORMED_RPC_RESPONSE"); }
    if (!body || body.jsonrpc !== "2.0" || body.id !== id || body.error || !("result" in body)) failure("INVALID_RPC_RESPONSE");
    return body.result;
  }
  const chain = await read("eth_chainId", [], 1);
  if (!quantity(chain)) failure("MALFORMED_CHAIN_ID");
  if (BigInt(chain) !== BigInt(expectedChainId)) failure("CHAIN_MISMATCH");
  const block = await read("eth_getBlockByNumber", ["latest", false], 2);
  if (!block || !quantity(block.number) || !quantity(block.timestamp) || !/^0x[0-9a-f]{64}$/i.test(block.hash ?? "")) failure("MALFORMED_BLOCK");
  const seconds = Number(BigInt(block.timestamp));
  if (!Number.isSafeInteger(seconds) || seconds < 0 || seconds > 8640000000000) failure("MALFORMED_BLOCK");
  const age = Math.floor(now / 1000) - seconds;
  if (age < -30) failure("FUTURE_BLOCK");
  if (age > maxAgeSeconds) failure("STALE_BLOCK");
  return { ok: true, scope: "rpc-connectivity-only", observedAt: new Date(now).toISOString(), chainId: BigInt(chain).toString(), blockNumber: BigInt(block.number).toString(), blockHash: block.hash, blockTimestamp: new Date(seconds * 1000).toISOString(), ageSeconds: age, fresh: true, walletReadiness: "not-tested", protocolReadiness: "not-tested" };
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  try {
    const args = process.argv.slice(2);
    if (args.length === 1 && args[0] === "--help") {
      process.stdout.write("Usage: node scripts/connection.mjs --chain-id <decimal> [--max-age-seconds <seconds>]\nReads LP_RPC_URL from environment; never prints it. Only eth_chainId and eth_getBlockByNumber are called.\n");
    } else {
      const values = {};
      for (let i = 0; i < args.length; i += 2) {
        const key = args[i];
        if (!["--chain-id", "--max-age-seconds"].includes(key) || values[key] !== undefined || !args[i + 1]) failure("INVALID_INPUT");
        values[key] = args[i + 1];
      }
      const result = await diagnose({ url: process.env.LP_RPC_URL, expectedChainId: values["--chain-id"], maxAgeSeconds: values["--max-age-seconds"] === undefined ? 180 : Number(values["--max-age-seconds"]) });
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    }
  } catch (error) {
    const allowed = new Set(["INVALID_INPUT", "MISSING_RPC_URL", "INVALID_RPC_URL", "RPC_UNAVAILABLE", "RPC_HTTP_ERROR", "MALFORMED_RPC_RESPONSE", "INVALID_RPC_RESPONSE", "MALFORMED_CHAIN_ID", "CHAIN_MISMATCH", "MALFORMED_BLOCK", "FUTURE_BLOCK", "STALE_BLOCK"]);
    process.stdout.write(`${JSON.stringify({ ok: false, error: { code: allowed.has(error.message) ? error.message : "DIAGNOSTIC_FAILED" }, walletReadiness: "not-tested" })}\n`);
    process.exitCode = 1;
  }
}
