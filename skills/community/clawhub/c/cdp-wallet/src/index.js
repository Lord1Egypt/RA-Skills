#!/usr/bin/env node
/**
 * cdp-wallet — minimal CLI wrapper around the CDP server wallet v2 SDK.
 *
 * Subcommands:
 *   address                       Print the wallet's EVM address.
 *   balance                       Print ETH and USDC balances on Base mainnet.
 *   send-usdc <to> <amount>       Send USDC on Base mainnet to <to>. Returns the tx hash.
 *   history [--limit N]           Print the last N USDC Transfer events involving this wallet.
 *   pay-x402 <url> [options]      Call an x402-protected URL, paying inline. Returns
 *                                 the resource body and settlement details (tx hash,
 *                                 settled amount). Supports any EVM network the
 *                                 resource server requests; the network is determined
 *                                 by the server's PaymentRequirements, not by
 *                                 CDP_NETWORK.
 *
 * Output is JSON on a single line for machine consumption. Errors print
 * `{"ok":false,"error":"..."}` to stdout and exit with status 1.
 *
 * Required env: CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET.
 * Optional env: CDP_ACCOUNT_NAME (default "openclaw-default"),
 *               CDP_NETWORK     (default "base"; use "base-sepolia" for testing
 *                                — affects address/balance/send-usdc/history;
 *                                does not constrain pay-x402, which honours the
 *                                resource server's requested network).
 *               BASE_RPC_URL    (override the default public Base RPC).
 */

import "dotenv/config";
import { Command } from "commander";
import { CdpClient } from "@coinbase/cdp-sdk";
import {
  createPublicClient,
  http,
  parseUnits,
  formatUnits,
  formatEther,
  isAddress,
  getAddress,
} from "viem";
import { toAccount } from "viem/accounts";
import { base, baseSepolia } from "viem/chains";
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { decodePaymentResponseHeader } from "@x402/core/http";
import { registerExactEvmScheme } from "@x402/evm/exact/client";

// --- Configuration --------------------------------------------------------

const NETWORK = (process.env.CDP_NETWORK || "base").trim();
const ACCOUNT_NAME = (process.env.CDP_ACCOUNT_NAME || "openclaw-default").trim();

const NETWORK_INFO = {
  base: {
    chain: base,
    explorer: "https://basescan.org/tx/",
    usdc: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    defaultRpc: "https://mainnet.base.org",
  },
  "base-sepolia": {
    chain: baseSepolia,
    explorer: "https://sepolia.basescan.org/tx/",
    usdc: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    defaultRpc: "https://sepolia.base.org",
  },
};

const network = NETWORK_INFO[NETWORK];
if (!network) {
  exitError(
    `Unsupported CDP_NETWORK: ${NETWORK}. Use "base" or "base-sepolia".`,
  );
}

// --- Utilities ------------------------------------------------------------

function exitOk(payload) {
  process.stdout.write(JSON.stringify({ ok: true, ...payload }) + "\n");
  process.exit(0);
}

function exitError(message, extra = {}) {
  process.stdout.write(
    JSON.stringify({ ok: false, error: message, ...extra }) + "\n",
  );
  process.exit(1);
}

function requireEnv() {
  const missing = [
    "CDP_API_KEY_ID",
    "CDP_API_KEY_SECRET",
    "CDP_WALLET_SECRET",
  ].filter((k) => !process.env[k]);
  if (missing.length > 0) {
    exitError(
      `Missing required env: ${missing.join(", ")}. See .env.example.`,
    );
  }
}

function publicClient() {
  const rpcUrl = process.env.BASE_RPC_URL || network.defaultRpc;
  return createPublicClient({ chain: network.chain, transport: http(rpcUrl) });
}

async function loadAccount() {
  // CdpClient reads CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET
  // from process.env automatically.
  const cdp = new CdpClient();
  // getOrCreateAccount is idempotent: same name → same address across runs.
  // This is what makes the wallet persistent on Railway despite ephemeral
  // filesystems — the wallet is held in CDP's TEE infrastructure, not on disk.
  const account = await cdp.evm.getOrCreateAccount({ name: ACCOUNT_NAME });
  return { cdp, account };
}

// Minimal ERC-20 ABI — only the bits this CLI needs.
const ERC20_ABI = [
  {
    type: "function",
    name: "balanceOf",
    stateMutability: "view",
    inputs: [{ type: "address", name: "account" }],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "decimals",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint8" }],
  },
  {
    type: "event",
    name: "Transfer",
    inputs: [
      { type: "address", indexed: true, name: "from" },
      { type: "address", indexed: true, name: "to" },
      { type: "uint256", indexed: false, name: "value" },
    ],
  },
];

// --- Subcommand handlers --------------------------------------------------

async function cmdAddress() {
  requireEnv();
  const { account } = await loadAccount();
  exitOk({
    address: account.address,
    network: NETWORK,
    account_name: ACCOUNT_NAME,
  });
}

async function cmdBalance() {
  requireEnv();
  const { account } = await loadAccount();
  const client = publicClient();

  // Read native ETH balance and USDC balance in parallel.
  const [ethWei, usdcRaw] = await Promise.all([
    client.getBalance({ address: account.address }),
    client.readContract({
      address: network.usdc,
      abi: ERC20_ABI,
      functionName: "balanceOf",
      args: [account.address],
    }),
  ]);

  exitOk({
    address: account.address,
    network: NETWORK,
    eth: formatEther(ethWei),
    usdc: formatUnits(usdcRaw, 6),
    raw: {
      eth_wei: ethWei.toString(),
      usdc_atoms: usdcRaw.toString(),
    },
  });
}

async function cmdSendUsdc(toRaw, amountRaw) {
  requireEnv();

  if (!toRaw || !amountRaw) {
    exitError("Usage: cdp-wallet send-usdc <to_address> <amount_usdc>");
  }
  if (!isAddress(toRaw)) {
    exitError(`Recipient address is not a valid Ethereum address: ${toRaw}`);
  }
  const to = getAddress(toRaw); // checksum normalization

  const amountStr = String(amountRaw).trim();
  if (!/^\d+(\.\d+)?$/.test(amountStr)) {
    exitError(`Amount must be a positive decimal number, got: ${amountRaw}`);
  }

  let amountAtoms;
  try {
    amountAtoms = parseUnits(amountStr, 6); // USDC = 6 decimals
  } catch (err) {
    exitError(`Could not parse amount: ${err.message}`);
  }
  if (amountAtoms <= 0n) {
    exitError("Amount must be greater than 0.");
  }

  const { account } = await loadAccount();

  let transactionHash;
  try {
    const result = await account.transfer({
      to,
      amount: amountAtoms,
      token: "usdc",
      network: NETWORK,
    });
    transactionHash = result.transactionHash;
  } catch (err) {
    exitError(`CDP transfer failed: ${err.message}`, { phase: "submit" });
  }

  // Wait for one confirmation so the caller can rely on the tx being mined
  // before reporting success. zooidfund's confirm_donation needs the tx
  // visible on-chain before it'll accept.
  try {
    const client = publicClient();
    const receipt = await client.waitForTransactionReceipt({
      hash: transactionHash,
      timeout: 60_000,
    });
    if (receipt.status !== "success") {
      exitError(`Transaction reverted on-chain.`, {
        tx_hash: transactionHash,
        explorer: network.explorer + transactionHash,
      });
    }
  } catch (err) {
    // Submission succeeded but confirmation timed out — still useful info.
    exitOk({
      tx_hash: transactionHash,
      status: "submitted_unconfirmed",
      explorer: network.explorer + transactionHash,
      warning: `Submitted but not confirmed within timeout: ${err.message}`,
      from: account.address,
      to,
      amount_usdc: amountStr,
      network: NETWORK,
    });
  }

  exitOk({
    tx_hash: transactionHash,
    status: "confirmed",
    explorer: network.explorer + transactionHash,
    from: account.address,
    to,
    amount_usdc: amountStr,
    network: NETWORK,
  });
}

async function cmdHistory(opts) {
  requireEnv();
  const limit = Math.max(1, Math.min(50, parseInt(opts.limit ?? "10", 10) || 10));
  const lookback = BigInt(opts.lookback ?? "20000"); // default ~24h on Base

  const { account } = await loadAccount();
  const client = publicClient();

  const head = await client.getBlockNumber();
  const fromBlock = head > lookback ? head - lookback : 0n;

  // Pull both directions: USDC sent FROM us and USDC sent TO us.
  const [outgoing, incoming] = await Promise.all([
    client.getContractEvents({
      address: network.usdc,
      abi: ERC20_ABI,
      eventName: "Transfer",
      args: { from: account.address },
      fromBlock,
      toBlock: head,
    }),
    client.getContractEvents({
      address: network.usdc,
      abi: ERC20_ABI,
      eventName: "Transfer",
      args: { to: account.address },
      fromBlock,
      toBlock: head,
    }),
  ]);

  const events = [...outgoing, ...incoming]
    .map((ev) => ({
      direction:
        ev.args.from?.toLowerCase() === account.address.toLowerCase()
          ? "out"
          : "in",
      from: ev.args.from,
      to: ev.args.to,
      amount_usdc: formatUnits(ev.args.value ?? 0n, 6),
      block_number: ev.blockNumber.toString(),
      tx_hash: ev.transactionHash,
      explorer: network.explorer + ev.transactionHash,
    }))
    // Sort newest first.
    .sort((a, b) => Number(BigInt(b.block_number) - BigInt(a.block_number)))
    .slice(0, limit);

  exitOk({
    address: account.address,
    network: NETWORK,
    from_block: fromBlock.toString(),
    to_block: head.toString(),
    count: events.length,
    transfers: events,
  });
}

// --- x402 payment ---------------------------------------------------------

// Convert a CDP server-wallet account into a viem LocalAccount that the x402
// client can use as a signer. CDP accounts expose the methods toAccount() needs
// (signTypedData in particular), so this is the canonical bridge.
function toX402Signer(cdpAccount) {
  return toAccount(cdpAccount);
}

// Pull settlement metadata out of the response. v2 uses PAYMENT-RESPONSE,
// v1 uses X-PAYMENT-RESPONSE. Returns null if neither is present, which can
// happen on a 402 that the client could not satisfy.
function extractSettlement(response) {
  const v2 = response.headers.get("PAYMENT-RESPONSE");
  const v1 = response.headers.get("X-PAYMENT-RESPONSE");
  const headerValue = v2 ?? v1;
  if (!headerValue) return null;
  try {
    const decoded = decodePaymentResponseHeader(headerValue);
    return decoded;
  } catch (err) {
    return { _decode_error: err.message };
  }
}

// Convert a settlement amount string in atomic units into a USDC decimal.
// Settlement amounts come back in token base units; for USDC that's 6 decimals.
// We don't assume the asset is USDC (the caller might pay an x402 endpoint that
// settles in something else), so we only convert when explicitly told.
function parseSettlementAmount(decoded) {
  if (!decoded || typeof decoded !== "object") return null;
  const raw = decoded.amount;
  if (raw === undefined || raw === null) return null;
  const parsed =
    typeof raw === "number" ? raw : Number(String(raw).trim());
  if (!Number.isFinite(parsed)) return null;
  // Atomic units → USDC decimal. If the asset isn't USDC, this is wrong
  // and the caller should ignore it; we still surface it because most x402
  // endpoints settle in USDC and the convenience is worth the caveat.
  return parsed / 1_000_000;
}

async function cmdPayX402(url, opts) {
  requireEnv();

  if (!url || typeof url !== "string") {
    exitError("Usage: cdp-wallet pay-x402 <url> [--method M] [--header H]... [--body B]");
  }

  let parsedUrl;
  try {
    parsedUrl = new URL(url);
  } catch {
    exitError(`Invalid URL: ${url}`);
  }
  if (parsedUrl.protocol !== "https:" && parsedUrl.protocol !== "http:") {
    exitError(`URL must be http or https: ${url}`);
  }

  const method = (opts.method || "GET").toUpperCase();

  // Build request headers from --header flags. Each --header is "Name: Value".
  const headers = {};
  const rawHeaders = Array.isArray(opts.header)
    ? opts.header
    : opts.header
      ? [opts.header]
      : [];
  for (const h of rawHeaders) {
    const idx = h.indexOf(":");
    if (idx === -1) {
      exitError(`Malformed header (expected "Name: Value"): ${h}`);
    }
    const name = h.slice(0, idx).trim();
    const value = h.slice(idx + 1).trim();
    if (!name) {
      exitError(`Empty header name in: ${h}`);
    }
    headers[name] = value;
  }

  const body = typeof opts.body === "string" ? opts.body : undefined;
  if (body && method === "GET") {
    exitError("Cannot send a body with method GET. Use --method POST or similar.");
  }

  // Construct the x402 client with the CDP-backed signer.
  let response;
  try {
    const { account } = await loadAccount();
    const signer = toX402Signer(account);
    const client = new x402Client();
    registerExactEvmScheme(client, { signer });
    const fetchWithPayment = wrapFetchWithPayment(fetch, client);

    response = await fetchWithPayment(url, {
      method,
      headers,
      ...(body !== undefined ? { body } : {}),
    });
  } catch (err) {
    exitError(`x402 request failed: ${err.message}`, { phase: "request" });
  }

  // Extract settlement metadata if a payment was made. A 200 without settlement
  // headers is also valid: the resource may have been free, or the server may
  // not echo settlement on this path.
  const settlement = extractSettlement(response);
  const settledAmountUsdc = settlement ? parseSettlementAmount(settlement) : null;

  // Read the response body. Try JSON first; fall back to text. For large/binary
  // bodies, truncate to a sane limit to keep the JSON output usable on a CLI.
  const contentType = response.headers.get("content-type") || "";
  const MAX_BODY_CHARS = 200_000;
  let bodyOut;
  let bodyTruncated = false;

  try {
    const text = await response.text();
    if (text.length > MAX_BODY_CHARS) {
      bodyOut = { _truncated: true, _length: text.length, preview: text.slice(0, MAX_BODY_CHARS) };
      bodyTruncated = true;
    } else if (contentType.includes("application/json")) {
      try {
        bodyOut = JSON.parse(text);
      } catch {
        bodyOut = text;
      }
    } else {
      bodyOut = text;
    }
  } catch (err) {
    exitError(`Could not read response body: ${err.message}`, {
      status: response.status,
      phase: "read_body",
    });
  }

  // Failure case: the response is non-2xx. We still want to return what we got
  // — the x402 client may have given up on payment, or the server may have
  // returned a 4xx/5xx after settlement. Caller can read status to decide.
  const ok = response.status >= 200 && response.status < 300;

  if (!ok) {
    exitError(`x402 endpoint returned ${response.status} ${response.statusText}`, {
      status: response.status,
      content_type: contentType,
      body: bodyOut,
      body_truncated: bodyTruncated,
      settlement,
      settled_amount_usdc: settledAmountUsdc,
    });
  }

  exitOk({
    status: response.status,
    content_type: contentType,
    body: bodyOut,
    body_truncated: bodyTruncated,
    settlement,
    settled_amount_usdc: settledAmountUsdc,
  });
}

// --- CLI wiring -----------------------------------------------------------

const program = new Command();
program
  .name("cdp-wallet")
  .description(
    "Minimal CDP server wallet v2 CLI for OpenClaw / Hermes / any agentskills.io runtime.",
  )
  .version("0.2.2");

program
  .command("address")
  .description("Print the wallet's EVM address")
  .action(cmdAddress);

program
  .command("balance")
  .description("Print ETH and USDC balances")
  .action(cmdBalance);

program
  .command("send-usdc <to> <amount>")
  .description("Send USDC on Base; returns the transaction hash")
  .action(cmdSendUsdc);

program
  .command("history")
  .description("Print recent USDC Transfer events involving this wallet")
  .option("-l, --limit <n>", "max events to return (1-50)", "10")
  .option(
    "--lookback <blocks>",
    "how many blocks back to scan (default 20000 ≈ 24h on Base)",
    "20000",
  )
  .action(cmdHistory);

program
  .command("pay-x402 <url>")
  .description(
    "Call an x402-protected URL, paying inline. Returns the resource body and settlement details (tx hash, settled amount).",
  )
  .option("-X, --method <method>", "HTTP method", "GET")
  .option(
    "-H, --header <header...>",
    'request header in "Name: Value" form; can be repeated',
  )
  .option("-d, --body <body>", "request body string (for non-GET methods)")
  .action(cmdPayX402);

program.parseAsync(process.argv).catch((err) => {
  exitError(`Unexpected error: ${err.message}`, { stack: err.stack });
});
