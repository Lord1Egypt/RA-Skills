// Utility functions for skill scripts.

import { getAddress, Wallet } from "ethers";

/**
 * Normalizes an Ethereum address to checksummed format.
 * Returns null if the address is invalid.
 */
export function normalizeAddress(address) {
  try {
    return getAddress(address);
  } catch {
    return null;
  }
}

/**
 * Normalizes a token identifier (address or symbol).
 * Accepts an Ethereum address ("0x...") or a token symbol ("USDC", "ETH").
 * - Address: validates via ethers.js (also converts to checksummed format).
 *   If invalid, falls back to original and lets the API handle the error.
 * - Symbol: returns trimmed string as-is.
 * Returns null if the value is missing or empty.
 */
export function normalizeToken(value) {
  if (value == null) return null;

  const normalized = String(value).trim();
  if (normalized === "") return null;

  // Address — validate via ethers.js (also converts to checksummed format).
  // If invalid, fall back to original and let the API handle the error.
  if (normalized.startsWith("0x")) {
    return normalizeAddress(normalized) ?? normalized;
  }

  // Symbol — return as-is
  return normalized;
}

/**
 * Normalizes a token amount to a decimal string.
 * Accepts a number (0.5) or a string ("0.5", " 0.5 ").
 * Returns the trimmed string representation, or null if the value is not a valid decimal number.
 */
export function normalizeAmount(value) {
  if (value == null) return null;

  const normalized = String(value).trim();
  if (normalized === "") return null;
  if (!/^\d+(\.\d+)?$/.test(normalized)) return null;

  return normalized;
}

/**
 * Normalizes slippage to a number within 0–50 range.
 * Returns the default (0.5) if the value is missing, not a number, or out of range.
 */
export function normalizeSlippage(value, defaultValue = 0.5) {
  if (value == null) return defaultValue;

  const num = Number(value);
  if (Number.isNaN(num) || num < 0 || num > 50) return defaultValue;

  return num;
}

/**
 * Normalizes a transaction hash to lowercase hex format (0x + 64 hex characters).
 * Returns null if the value is not a valid transaction hash.
 */
export function normalizeTxHash(value) {
  if (value == null) return null;

  const normalized = String(value).trim().toLowerCase();
  if (!/^0x[0-9a-f]{64}$/.test(normalized)) return null;

  return normalized;
}

/**
 * Normalizes a private key: trims whitespace, adds 0x prefix if missing,
 * validates length (64 hex characters) and hex format.
 * Returns the normalized key with 0x prefix, or null if invalid.
 */
export function normalizePrivateKey(value) {
  if (value == null) return null;

  let normalized = String(value).trim();
  if (normalized === "") return null;

  if (!normalized.startsWith("0x")) {
    normalized = "0x" + normalized;
  }

  if (!/^0x[0-9a-fA-F]{64}$/.test(normalized)) return null;

  return normalized;
}

/**
 * Checks if the value is a valid Ethereum address (0x + 40 hex characters).
 */
export function isAddress(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]{40}$/.test(value);
}

/**
 * Checks if the value is a valid decimal amount string (e.g., "0.5", "100").
 */
export function isAmount(value) {
  return typeof value === "string" && value !== "" && /^\d+(\.\d+)?$/.test(value);
}

/**
 * Checks if the value is a finite number.
 */
export function isNumber(value) {
  return typeof value === "number" && !Number.isNaN(value);
}

/**
 * Checks if the value is a valid transaction hash (0x + 64 hex characters).
 */
export function isHash(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]{64}$/.test(value);
}

/**
 * Checks if the value is a non-empty trimmed string.
 */
export function isNonEmptyString(value) {
  return typeof value === "string" && value.trim() !== "";
}

/**
 * Checks if the value is a hex-encoded string (0x + at least one hex character).
 */
export function isHex(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]+$/.test(value);
}

/**
 * Maps API resultType to an error message.
 * Returns the error string, or null if resultType indicates success.
 */
export function resultTypeToError(resultType) {
  switch (resultType) {
    case 1: return null;
    case -1: return "Route not found.";
    case -2: return "AIDEX is temporarily unavailable. Please try again later.";
    default: return "AIDEX is temporarily unavailable. Please try again later.";
  }
}

/**
 * Creates a Unix timestamp deadline (current time + minutesFromNow minutes).
 */
export function createDeadline(minutesFromNow = 20) {
  return Math.floor(Date.now() / 1000) + minutesFromNow * 60;
}

/**
 * Parses command-line arguments in --key value format.
 */
export function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const value = argv[i + 1];
      args[key] = value;
      i++;
    }
  }
  return args;
}

/**
 * Returns the value of a required CLI argument.
 * If the argument is missing or empty, prints an error via output() and terminates the process.
 */
export function requireArg(args, name) {
  if (!args[name]) {
    output({ success: false, error: `Missing required argument: --${name}.` });
  }
  return args[name];
}

/**
 * Parses and validates swap-related arguments (--token-in, --token-out, --amount-in).
 * On any missing or invalid argument, prints an error via output() and terminates the process.
 */
export function parseSwapInput(args) {
  const tokenIn = normalizeToken(requireArg(args, "token-in"));
  const tokenOut = normalizeToken(requireArg(args, "token-out"));

  const amountIn = normalizeAmount(requireArg(args, "amount-in"));
  if (!amountIn) {
    output({ success: false, error: "Invalid --amount-in: must be a valid decimal number." });
  }

  return { tokenIn, tokenOut, amountIn };
}

/**
 * Resolves the private key from available sources.
 * Priority: environment variable > system keyring > null.
 */
export async function resolvePrivateKey() {
  const fromEnv = normalizePrivateKey(process.env.AIDEX_PRIVATE_KEY);
  if (fromEnv) return fromEnv;

  try {
    const { Entry } = await import("@napi-rs/keyring");
    const entry = new Entry("aidex", "AIDEX_PRIVATE_KEY");
    const secret = entry.getPassword();
    return normalizePrivateKey(secret);
  } catch {
    return null;
  }
}

/**
 * Resolves the private key and constructs a Wallet.
 * On missing key or invalid key, prints an error via output() and terminates the process.
 */
export async function resolveWallet() {
  const privateKey = await resolvePrivateKey();
  if (!privateKey) {
    output({ success: false, error: "Private key is not configured. If you just configured it, you may need to restart the OpenClaw gateway and try again. See the Setup section in the Documentation." });
  }

  try {
    return new Wallet(privateKey);
  } catch (err) {
    output({ success: false, error: `Invalid private key: ${err.message}.` });
  }
}

/**
 * Outputs a JSON result to stdout and exits the process.
 */
export function output(data) {
  console.log(JSON.stringify(data));
  process.exit(data.success === false ? 1 : 0);
}

/**
 * Unwraps a {success, data, error} result from api.js.
 * Returns result.data on success. On failure, prints the error via output() and terminates the process.
 */
export function unwrap(result) {
  if (result.success) {
    return result.data;
  }
  output({ success: false, error: result.error });
}
