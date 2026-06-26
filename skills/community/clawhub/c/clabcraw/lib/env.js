/**
 * Smart environment loader for Clabcraw skill scripts.
 *
 * Merges skill.json env defaults with runtime environment variables.
 * Runtime env vars always take precedence over skill.json defaults.
 */

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let skillDefaults = {};

try {
  const skillPath = join(__dirname, "..", "skill.json");
  const skillJson = JSON.parse(readFileSync(skillPath, "utf-8"));
  skillDefaults = skillJson.env || {};
} catch {
  // skill.json not found — rely on runtime env vars only
}

/**
 * Get environment value with fallback to skill.json defaults.
 * Empty strings in skill.json are treated as unset.
 */
export function getEnv(key) {
  const envVal = process.env[key];
  if (envVal) return envVal;
  const defaultVal = skillDefaults[key];
  return defaultVal || undefined;
}

/**
 * Require a specific env var. Exits with error if missing.
 */
export function requireEnv(key) {
  const value = getEnv(key);
  if (!value) {
    console.error(`ERROR: ${key} not set in env or skill.json`);
    process.exit(1);
  }
  return value;
}

/**
 * Load all Clabcraw config from env + skill.json defaults.
 */
export function loadConfig() {
  return {
    apiUrl: getEnv("CLABCRAW_API_URL"),
    walletPrivateKey: getEnv("CLABCRAW_WALLET_PRIVATE_KEY"),
    contractAddress: getEnv("CLABCRAW_CONTRACT_ADDRESS"),
    rpcUrl: getEnv("CLABCRAW_RPC_URL"),
    chainId: getEnv("CLABCRAW_CHAIN_ID"),
  };
}

/**
 * Get wallet address from env.
 * Prefers CLABCRAW_WALLET_ADDRESS, falls back to deriving from private key.
 */
export async function getWalletAddress() {
  const addr = getEnv("CLABCRAW_WALLET_ADDRESS");
  if (addr) return addr;

  const key = getEnv("CLABCRAW_WALLET_PRIVATE_KEY");
  if (key) {
    // Lazy import to avoid circular dependency with client.js
    const { createSigner } = await import("./client.js");
    return createSigner(key).address;
  }

  console.error(
    "ERROR: Set CLABCRAW_WALLET_ADDRESS or CLABCRAW_WALLET_PRIVATE_KEY",
  );
  process.exit(1);
}

/**
 * Validate all required config on startup. Exits if any are missing.
 */
export function validateConfig() {
  const required = ["CLABCRAW_WALLET_PRIVATE_KEY", "CLABCRAW_API_URL"];
  const missing = required.filter((key) => !getEnv(key));

  if (missing.length > 0) {
    console.error(
      `ERROR: Missing required config: ${missing.join(", ")}\n` +
        `Set them as env vars or ensure skill.json has defaults.`,
    );
    process.exit(1);
  }
}
