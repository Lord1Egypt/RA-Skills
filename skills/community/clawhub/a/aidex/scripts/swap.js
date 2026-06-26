#!/usr/bin/env node

// Full swap cycle: createSwap (API) -> sign all (client-side) -> sendSwap (API).
// The API builds a chain of transactions (approve + swap if needed).
// The client only specifies high-level parameters, signs, and sends.

import { keccak256 } from "ethers";

import { createSwap, sendSwap, safeErrorText } from "./lib/api.js";
import { resolveToken } from "./lib/tokens.js";
import {
  parseArgs,
  createDeadline,
  output,
  parseSwapInput,
  normalizeSlippage,
  resolveWallet,
  resultTypeToError,
  unwrap,
  isHash,
} from "./lib/utils.js";

const TEMPORARILY_UNAVAILABLE = "AIDEX is temporarily unavailable. Please try again later.";

const args = parseArgs(process.argv);
const {
  tokenIn: tokenInSymbolOrAddress,
  tokenOut: tokenOutSymbolOrAddress,
  amountIn,
} = parseSwapInput(args);

const tokenIn = resolveToken(tokenInSymbolOrAddress);
if (!tokenIn) {
  output({ success: false, error: `Token "${tokenInSymbolOrAddress}" not found.` });
}

const tokenOut = resolveToken(tokenOutSymbolOrAddress);
if (!tokenOut) {
  output({ success: false, error: `Token "${tokenOutSymbolOrAddress}" not found.` });
}

const wallet = await resolveWallet();
const slippage = normalizeSlippage(args.slippage);
const deadlineMinutesRaw = args["deadline-minutes"] ? parseInt(args["deadline-minutes"], 10) : 20;

if (Number.isNaN(deadlineMinutesRaw)) {
  output({ success: false, error: "Invalid --deadline-minutes: must be a number." });
}

const deadlineMinutes = Math.max(1, Math.min(60, deadlineMinutesRaw));
const deadline = createDeadline(deadlineMinutes);

// Step 1: Get the transaction chain from the API (may include approve + swap)
const swap = unwrap(await createSwap(
  tokenInSymbolOrAddress,
  tokenOutSymbolOrAddress,
  amountIn,
  slippage,
  deadline,
  wallet.address,
));

if (!swap || typeof swap !== "object" || !Array.isArray(swap.transactions)) {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

const resultError = resultTypeToError(swap.resultType);

if (resultError) {
  output({ success: false, error: resultError });
}

// Protocol values referenced by both validation passes below.

const ROUTER_ADDRESS = "0x1208d02aac7d247eb79b71ce23c792441457e7b3";
const WETH_ADDRESS = resolveToken("WETH").address.toLowerCase();
const NATIVE_ADDRESS = "0x0000000000000000000000000000000000000000";
const APPROVE_SELECTOR = "0x095ea7b3";
const WRAP_SELECTOR = "0xd0e30db0";
const UNWRAP_SELECTOR = "0x2e1a7d4d";

// #region Transaction validation

// Every transaction returned by the AIDEX API is checked against this
// hardcoded whitelist before signing. The whitelist is in-source: updating
// the AIDEX router requires publishing a new skill version (signed by the
// publisher on ClawHub), which an API-only attacker cannot do.

const KNOWN_TRANSACTION_DESTINATIONS = new Set([ROUTER_ADDRESS, WETH_ADDRESS]);
const KNOWN_APPROVE_SPENDERS = new Set([ROUTER_ADDRESS]);

for (const tx of swap.transactions) {
  const to = (tx.to || "").toLowerCase();
  const data = (tx.data || "").toLowerCase();

  if (KNOWN_TRANSACTION_DESTINATIONS.has(to)) {
    continue;
  }

  if (data.startsWith(APPROVE_SELECTOR)) {
    // approve(spender, amount): 4-byte selector + 32-byte spender word + 32-byte amount.
    // The address is the last 20 bytes of the spender word -> hex chars 34..73.
    const spender = "0x" + data.slice(34, 74);

    if (KNOWN_APPROVE_SPENDERS.has(spender)) {
      continue;
    }

    output({
      success: false,
      error: `Approve spender ${spender} is not whitelisted. ` +
        `This may indicate an outdated skill version. ` +
        `Please update: openclaw skills update aidex.`,
    });
  }

  output({
    success: false,
    error: `Transaction destination ${to} is not whitelisted. ` +
      `This may indicate an outdated skill version. ` +
      `Please update: openclaw skills update aidex.`,
  });
}

// #endregion

// #region Main transaction validation

// Independent semantic check of every transaction the AIDEX API returned.
// Compares each field against locally-known values (tokens from the bundled
// registry, user-supplied amount/slippage/deadline) so a malicious or
// compromised API cannot trick the user into signing a different swap.

const AMOUNT_REGEX = /^\d+(\.\d+)?$/;

function fail() {
  throw new Error("Validation failed");
}

function toBaseUnits(decimalString, decimals) {
  if (typeof decimalString !== "string" || !AMOUNT_REGEX.test(decimalString)) fail();
  const [intPart, fracPart = ""] = decimalString.split(".");
  if (fracPart.length > decimals) fail();
  const padded = (fracPart + "0".repeat(decimals)).slice(0, decimals);
  return BigInt(intPart + padded);
}

function applySlippage(amountOutBaseUnits, slippagePercent) {
  const slippageScaled = BigInt(Math.trunc(slippagePercent * 100));
  return (amountOutBaseUnits * (10000n - slippageScaled)) / 10000n;
}

function isApproveTx(tx) {
  return tx.to.toLowerCase() === tokenIn.address.toLowerCase()
    && tx.data.toLowerCase().startsWith(APPROVE_SELECTOR);
}

function isWrapTx(tx) {
  return tx.to.toLowerCase() === WETH_ADDRESS
    && tx.data.toLowerCase().startsWith(WRAP_SELECTOR);
}

function isUnwrapTx(tx) {
  return tx.to.toLowerCase() === WETH_ADDRESS
    && tx.data.toLowerCase().startsWith(UNWRAP_SELECTOR);
}

function validateWrap(tx) {
  if (tokenIn.address.toLowerCase() !== NATIVE_ADDRESS) fail();
  if (tokenOut.address.toLowerCase() !== WETH_ADDRESS) fail();

  const expectedValue = toBaseUnits(amountIn, tokenIn.decimals);

  if (tx.to.toLowerCase() !== WETH_ADDRESS) fail();
  if (tx.data.toLowerCase() !== WRAP_SELECTOR) fail();
  if (BigInt(tx.value) !== expectedValue) fail();
}

function validateUnwrap(tx) {
  if (tokenIn.address.toLowerCase() !== WETH_ADDRESS) fail();
  if (tokenOut.address.toLowerCase() !== NATIVE_ADDRESS) fail();

  const amountInBaseUnits = toBaseUnits(amountIn, tokenIn.decimals);
  const expectedData = UNWRAP_SELECTOR + amountInBaseUnits.toString(16).padStart(64, "0");

  if (tx.to.toLowerCase() !== WETH_ADDRESS) fail();
  if (tx.data.toLowerCase() !== expectedData) fail();
  if (BigInt(tx.value) !== 0n) fail();
}

function validateRegularSwap(tx) {
  if (tx.to.toLowerCase() !== ROUTER_ADDRESS) fail();

  const data = tx.data.toLowerCase();
  const dataByteLength = (data.length - 2) / 2;
  if (dataByteLength < 79) fail();

  // Header layout (79 bytes): requestType(1) + routeFlags(1) + tokenIn(20) +
  // tokenOut(20) + amountIn(16) + minAmountOut(16) + deadline(4) + operationCount(1).
  const requestType = data.slice(2, 4);
  const routeFlags = parseInt(data.slice(4, 6), 16);
  const tokenInInData = "0x" + data.slice(6, 46);
  const tokenOutInData = "0x" + data.slice(46, 86);
  const amountInInData = BigInt("0x" + data.slice(86, 118));
  const minAmountOutInData = BigInt("0x" + data.slice(118, 150));
  const deadlineInData = parseInt(data.slice(150, 158), 16);
  const operationCount = parseInt(data.slice(158, 160), 16);

  if (dataByteLength < 79 + operationCount) fail();

  const tokenInLower = tokenIn.address.toLowerCase();
  const tokenOutLower = tokenOut.address.toLowerCase();
  const amountInBaseUnits = toBaseUnits(amountIn, tokenIn.decimals);

  // Native quirks: the on-chain router operates on WETH; native ETH on either
  // side is signaled via tx.value (input) and routeFlags bit 0 / IsNativeOut
  // (output). Both sides being native is impossible: that case routes through
  // wrap/unwrap, not regular swap.
  let expectedTokenIn;
  let expectedTokenOut;
  let expectedNativeOutBit;
  let expectedTxValue;
  if (tokenInLower === NATIVE_ADDRESS) {
    expectedTokenIn = WETH_ADDRESS;
    expectedTokenOut = tokenOutLower;
    expectedNativeOutBit = 0;
    expectedTxValue = amountInBaseUnits;
  } else if (tokenOutLower === NATIVE_ADDRESS) {
    expectedTokenIn = tokenInLower;
    expectedTokenOut = WETH_ADDRESS;
    expectedNativeOutBit = 1;
    expectedTxValue = 0n;
  } else {
    expectedTokenIn = tokenInLower;
    expectedTokenOut = tokenOutLower;
    expectedNativeOutBit = 0;
    expectedTxValue = 0n;
  }

  if (requestType !== "00") fail();
  if ((routeFlags & 0x01) !== expectedNativeOutBit) fail();
  if ((routeFlags & 0xfc) !== 0) fail();
  if (tokenInInData !== expectedTokenIn) fail();
  if (tokenOutInData !== expectedTokenOut) fail();
  if (amountInInData !== amountInBaseUnits) fail();
  if (deadlineInData !== deadline) fail();
  if (operationCount < 1) fail();
  if (BigInt(tx.value) !== expectedTxValue) fail();

  // minAmountOut must be strictly positive: a backend that supplies
  // tokenToReceiveAmount = "0" would otherwise pass with minAmountOut = 0,
  // letting MEV/front-running drain the pool.
  const amountOutBaseUnits = toBaseUnits(swap.tokenToReceiveAmount, tokenOut.decimals);
  const expectedMinAmountOut = applySlippage(amountOutBaseUnits, slippage);
  if (expectedMinAmountOut <= 0n) fail();
  if (minAmountOutInData !== expectedMinAmountOut) fail();
}

function validateApprove(tx, isFirstOfPair) {
  if (tx.to.toLowerCase() !== tokenIn.address.toLowerCase()) fail();

  const data = tx.data.toLowerCase();
  if (data.length !== 138) fail();
  if (!data.startsWith(APPROVE_SELECTOR)) fail();

  // approve(spender, amount): selector(4B) + spender word(32B) + amount(32B).
  // Spender address = last 20 bytes of spender word -> hex chars 34..74.
  const spender = "0x" + data.slice(34, 74);
  if (spender !== ROUTER_ADDRESS) fail();

  // USDT-style reset pattern: a pair of approves where the first sets allowance
  // to 0 (required by tokens that disallow direct allowance change) and the
  // second sets the new non-zero allowance. A solo approve must be non-zero.
  const amount = BigInt("0x" + data.slice(74, 138));
  if (isFirstOfPair) {
    if (amount !== 0n) fail();
  } else {
    if (amount === 0n) fail();
  }

  if (BigInt(tx.value) !== 0n) fail();
}

try {
  if (swap.transactions.length < 1 || swap.transactions.length > 3) fail();

  for (const tx of swap.transactions) {
    for (const field of ["to", "data", "value", "gasPrice"]) {
      if (typeof tx[field] !== "string" || tx[field].length === 0) fail();
    }
    for (const field of ["gasLimit", "nonce"]) {
      if (typeof tx[field] !== "number" || !Number.isFinite(tx[field])) fail();
    }
  }

  // Position-based classification: the main transaction (wrap, unwrap, or
  // regular swap) must be last; all preceding transactions must be approves.
  for (let i = 0; i < swap.transactions.length; i++) {
    const tx = swap.transactions[i];
    const isLast = i === swap.transactions.length - 1;

    if (isLast) {
      if (isWrapTx(tx)) validateWrap(tx);
      else if (isUnwrapTx(tx)) validateUnwrap(tx);
      else if (tx.to.toLowerCase() === ROUTER_ADDRESS) validateRegularSwap(tx);
      else fail();
    } else {
      if (!isApproveTx(tx)) fail();
      const isFirstOfPair = isApproveTx(swap.transactions[i + 1]);
      validateApprove(tx, isFirstOfPair);
    }
  }
} catch {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

// #endregion

// Step 2: Sign each transaction in the chain
const signedTransactions = [];

try {
  for (const tx of swap.transactions) {
    const signed = await wallet.signTransaction({
      to: tx.to,
      data: tx.data,
      value: tx.value,
      gasPrice: tx.gasPrice,
      gasLimit: tx.gasLimit,
      nonce: tx.nonce,
      chainId: 1,
      type: 0,
    });
    signedTransactions.push(signed);
  }
} catch {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

// Local transaction hashes: keccak256 of each signed payload. The server's
// reported hashes are checked against these before any user-facing output, so
// a malicious or compromised API cannot fabricate hashes that do not exist
// on-chain.
const localHashes = signedTransactions.map(keccak256);

// Step 3: Send all signed transactions
const sendData = unwrap(await sendSwap(signedTransactions));

if (!sendData || typeof sendData !== "object") {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

if (!Array.isArray(sendData.transactionHashes)
    || sendData.transactionHashes.length !== localHashes.length) {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

for (let i = 0; i < localHashes.length; i++) {
  const serverHash = sendData.transactionHashes[i];
  if (!isHash(serverHash)) {
    output({ success: false, error: TEMPORARILY_UNAVAILABLE });
  }
  if (serverHash.toLowerCase() !== localHashes[i].toLowerCase()) {
    output({ success: false, error: TEMPORARILY_UNAVAILABLE });
  }
}

if (sendData.error) {
  if (!Number.isInteger(sendData.failedAtStep)
      || sendData.failedAtStep < 0
      || sendData.failedAtStep > localHashes.length) {
    output({ success: false, error: TEMPORARILY_UNAVAILABLE });
  }
  output({
    success: false,
    error: safeErrorText(sendData.error),
    transactionHashes: localHashes.slice(0, sendData.failedAtStep),
    failedAtStep: sendData.failedAtStep,
  });
}

if (typeof swap.estimatedGasPriceUsd !== "number") {
  output({ success: false, error: TEMPORARILY_UNAVAILABLE });
}

output({
  success: true,
  transactionHashes: localHashes,
  fromAddress: wallet.address,
  amountOut: swap.tokenToReceiveAmount,
  estimatedGasPriceUsd: swap.estimatedGasPriceUsd,
});
