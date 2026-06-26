// HTTP client for AIDEX Agent API.
// All functions return {success: true, data} or {success: false, error}.

import { isAddress, isAmount, isHash, isHex, isNonEmptyString, isNumber } from "./utils.js";
import { SKILL_VERSION } from "./version.js";

const BASE_URL = "https://api.ai-dex.io/api/v1/agent";

const ERROR_CODE = {
  TEMPORARILY_UNAVAILABLE: 0,
  UNSUPPORTED_SKILL_VERSION: 1,
  INVALID_ARGUMENT: 2,
};

const ERROR_TEXT = {
  [ERROR_CODE.TEMPORARILY_UNAVAILABLE]: "AIDEX is temporarily unavailable. Please try again later.",
  [ERROR_CODE.UNSUPPORTED_SKILL_VERSION]: `Skill version ${SKILL_VERSION} is outdated, please update: openclaw skills update aidex`,
  [ERROR_CODE.INVALID_ARGUMENT]: "Request rejected. Double-check the arguments. If they look fine, try updating the skill to the latest version: openclaw skills update aidex",
};

// Returns a fixed user-facing message for the given server error.
// Selection is based solely on the numeric `code` field; `message`
// from the server is not used. Any unrecognized shape (non-object,
// missing or unknown code, null) resolves to the generic
// "temporarily unavailable" text.
export function safeErrorText(error) {
  if (error && typeof error === "object" && typeof error.code === "number") {
    return ERROR_TEXT[error.code] ?? ERROR_TEXT[ERROR_CODE.TEMPORARILY_UNAVAILABLE];
  }
  return ERROR_TEXT[ERROR_CODE.TEMPORARILY_UNAVAILABLE];
}

async function request(method, path, body) {
  try {
    const options = {
      method,
      signal: AbortSignal.timeout(10_000),
      headers: {
        "Content-Type": "application/json",
        "User-Agent": `AIDEX-OpenClaw/${SKILL_VERSION}`,
      },
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const url = `${BASE_URL.replace(/\/+$/, "")}${path}`;
    const response = await fetch(url, options);

    const text = await response.text();
    let data;

    try {
      data = JSON.parse(text);
    } catch {
      data = null;
    }

    if (!response.ok) {
      return { success: false, error: safeErrorText(data?.error) };
    }

    return { success: true, data };
  } catch (err) {
    if (err.name === "TimeoutError") {
      return { success: false, error: "API request timed out." };
    }
    return { success: false, error: `API request failed: ${err.message}.` };
  }
}

export async function searchTokens(term) {
  const params = isNonEmptyString(term) ? `?term=${encodeURIComponent(term)}` : "";
  return request("GET", `/tokens${params}`);
}

export async function getRate(tokenIn, tokenOut, amountIn) {
  if (!isNonEmptyString(tokenIn))
    return { success: false, error: "tokenIn must be a non-empty string." };
  if (!isNonEmptyString(tokenOut))
    return { success: false, error: "tokenOut must be a non-empty string." };
  if (!isAmount(amountIn))
    return { success: false, error: "amountIn must be a valid decimal number string." };
  return request("POST", "/rate", { tokenIn, tokenOut, amountIn });
}

export async function getBalances(address, tokens) {
  if (!isAddress(address))
    return { success: false, error: "address must be a valid Ethereum address." };
  if (!Array.isArray(tokens) || !tokens.every(isNonEmptyString))
    return { success: false, error: "tokens must be an array of non-empty strings." };
  const params = new URLSearchParams({ address, tokens: tokens.join(",") });
  return request("GET", `/balances?${params}`);
}

export async function getSwapStatus(hashes) {
  if (!Array.isArray(hashes) || !hashes.every(isHash))
    return { success: false, error: "hashes must be an array of valid transaction hashes." };
  const params = new URLSearchParams({ hashes: hashes.join(",") });
  return request("GET", `/swap/status?${params}`);
}

export async function createSwap(tokenIn, tokenOut, amountIn, slippage, deadline, from) {
  if (!isNonEmptyString(tokenIn))
    return { success: false, error: "tokenIn must be a non-empty string." };
  if (!isNonEmptyString(tokenOut))
    return { success: false, error: "tokenOut must be a non-empty string." };
  if (!isAmount(amountIn))
    return { success: false, error: "amountIn must be a valid decimal number string." };
  if (!isNumber(slippage) || slippage < 0 || slippage > 50)
    return { success: false, error: "slippage must be a number between 0 and 50." };
  if (!isNumber(deadline) || !Number.isInteger(deadline) || deadline <= 0)
    return { success: false, error: "deadline must be a positive integer (Unix timestamp)." };
  if (!isAddress(from))
    return { success: false, error: "from must be a valid Ethereum address." };
  return request("POST", "/swap/create", {
    tokenIn,
    tokenOut,
    amountIn,
    slippage,
    deadline,
    from,
  });
}

export async function sendSwap(signedTransactions) {
  if (!Array.isArray(signedTransactions) || !signedTransactions.every(isHex))
    return { success: false, error: "signedTransactions must be an array of hex-encoded strings." };
  return request("POST", "/swap/send", { signedTransactions });
}
