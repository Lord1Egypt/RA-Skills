"use strict";

const fs = require("fs");
const paths = require("./paths");
const { loadWallet } = require("./wallet");
const { checkCaps, appendReceipt } = require("./spend");
const { getBalances } = require("./balance");

const BASE_NETWORK = "eip155:8453";
const USDC_DECIMALS = 6;

function atomicToUsd(amount) {
  return Number(amount) / 10 ** USDC_DECIMALS;
}

function buildHttpClient(privateKey) {
  const { x402Client } = require("@x402/core/client");
  const { x402HTTPClient } = require("@x402/core/http");
  const { registerExactEvmScheme } = require("@x402/evm/exact/client");
  const { privateKeyToAccount } = require("viem/accounts");

  const account = privateKeyToAccount(privateKey);
  const client = new x402Client();
  registerExactEvmScheme(client, { signer: account });
  client.registerPolicy((_version, reqs) => {
    const base = reqs.filter((r) => r.network === BASE_NETWORK);
    return base.length ? base : reqs;
  });
  return { client, httpClient: new x402HTTPClient(client) };
}

function parsePaymentRequired(res, body) {
  const header = res.headers.get("payment-required");
  if (header) {
    return JSON.parse(Buffer.from(header, "base64").toString("utf8"));
  }
  if (body && typeof body === "object" && Array.isArray(body.accepts)) return body;
  throw new Error("missing x402 payment-required challenge");
}

function acceptedAmountUsd(paymentRequired) {
  const accepted = Array.isArray(paymentRequired?.accepts)
    ? paymentRequired.accepts.find((item) => item.network === BASE_NETWORK) || paymentRequired.accepts[0]
    : null;
  if (!accepted?.amount) throw new Error("payment challenge did not include an accepted amount");
  return atomicToUsd(accepted.amount);
}

async function tryBalances(address) {
  try {
    return await getBalances(address);
  } catch (err) {
    return { address, network: "base-mainnet", error: err.message };
  }
}

function printPaymentPreview({ wallet, amountUsd, beforeBalance, url }) {
  console.log("x402 payment preview:");
  console.log(`  wallet: ${wallet.address}`);
  console.log(`  endpoint: ${url}`);
  console.log(`  price: $${amountUsd.toFixed(6)} USDC`);
  if (beforeBalance?.usdc != null) {
    console.log(`  balance before: ${beforeBalance.usdc} USDC`);
  } else if (beforeBalance?.error) {
    console.log(`  balance before: unavailable (${beforeBalance.error})`);
  }
}

function printPaymentFinal({ afterBalance, receipt }) {
  if (afterBalance?.usdc != null) {
    console.log(`x402 final balance: ${afterBalance.usdc} USDC`);
  } else if (afterBalance?.error) {
    console.log(`x402 final balance: unavailable (${afterBalance.error})`);
  }
  if (receipt) console.log(`x402 receipt logged: ${paths.SPEND_LOG_PATH}`);
}

// Calls the hosted ForgeMesh Voice endpoint, paying via x402 if it returns 402.
// confirm(amountUsd, resourceUrl) is awaited before signing when approval is required.
// Returns { ok, engine: "hosted", amountUsd?, error? }. Never throws.
async function hostedSpeak(config, text, outPath, { confirm } = {}) {
  // Tiers: /v1/tts/base (cheapest), /v1/tts/pro, /v1/tts/custom; -long variants for >short-bucket text.
  const tier = config.hostedVoice?.tier || "base";
  const url = `${config.forgemeshVoiceBaseUrl || paths.DEFAULT_BASE_URL}/v1/tts/${tier}`;
  const body = { text };
  if (config.hostedVoice?.voice) body.voice = config.hostedVoice.voice;
  if (config.hostedVoice?.language) body.lang = config.hostedVoice.language;
  if (config.hostedVoice?.preset) body.preset = config.hostedVoice.preset;
  if (config.hostedVoice?.mix) body.mix = config.hostedVoice.mix;
  if (config.hostedVoice?.expression) body.expression = config.hostedVoice.expression;
  if (config.hostedVoice?.expressionLevel != null) body.expressionLevel = config.hostedVoice.expressionLevel;
  if (config.hostedVoice?.expressionControls && Object.keys(config.hostedVoice.expressionControls).length) {
    body.knobs = config.hostedVoice.expressionControls;
  }
  const requestInit = {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(120000),
  };

  try {
    let res = await fetch(url, requestInit);
    let amountUsd = 0;

    if (res.status === 402) {
      const body = await res.json().catch(() => undefined);
      const paymentRequired = parsePaymentRequired(res, body);
      amountUsd = acceptedAmountUsd(paymentRequired);
      const wallet = loadWallet();
      const beforeBalance = await tryBalances(wallet.address);
      printPaymentPreview({ wallet, amountUsd, beforeBalance, url });
      const caps = checkCaps(amountUsd, config.x402Policy);
      if (!caps.ok) return { ok: false, engine: "hosted", error: `blocked by spend cap: ${caps.reason}` };

      if (config.x402Policy?.requireApproval) {
        if (!confirm) return { ok: false, engine: "hosted", error: "approval required but no approver available (use --approve)" };
        const approved = await confirm(amountUsd, url);
        if (!approved) return { ok: false, engine: "hosted", error: "payment declined by user" };
      }

      const { client, httpClient } = buildHttpClient(wallet.privateKey);
      const paymentPayload = await client.createPaymentPayload(paymentRequired);
      const paymentHeaders = httpClient.encodePaymentSignatureHeader(paymentPayload);
      res = await fetch(url, { ...requestInit, headers: { ...requestInit.headers, ...paymentHeaders } });
      res._x402BeforeBalance = beforeBalance;
    }

    if (!res.ok) {
      const detail = (await res.text().catch(() => "")).slice(0, 200);
      return { ok: false, engine: "hosted", error: `hosted voice returned ${res.status}${detail ? `: ${detail}` : ""}` };
    }

    fs.writeFileSync(outPath, Buffer.from(await res.arrayBuffer()));
    if (amountUsd > 0) {
      const wallet = loadWallet();
      const afterBalance = await tryBalances(wallet.address);
      const paymentResponse = res.headers.get("payment-response");
      const receipt = appendReceipt({
        endpoint: url,
        amountUsd,
        network: BASE_NETWORK,
        token: "USDC",
        chars: text.length,
        wallet: wallet.address,
        balanceBefore: res._x402BeforeBalance,
        balanceAfter: afterBalance,
        paymentResponse,
      });
      printPaymentFinal({ afterBalance, receipt });
    }
    return { ok: true, engine: "hosted", amountUsd };
  } catch (err) {
    return { ok: false, engine: "hosted", error: err.message };
  }
}

module.exports = { hostedSpeak };
