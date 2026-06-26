import type { RequestHandler } from "express";
import { StrKey } from "@stellar/stellar-sdk";
import nacl from "tweetnacl";
import { query } from "../db/db";

/** Lightweight DAA tracking — upsert one row per wallet per day */
async function trackApiActivity(walletAddress: string): Promise<void> {
    await query(
        `INSERT INTO api_activity (wallet_address, request_date, request_count)
         VALUES ($1, CURRENT_DATE, 1)
         ON CONFLICT (wallet_address, request_date)
         DO UPDATE SET request_count = api_activity.request_count + 1,
                       last_seen_at = NOW()`,
        [walletAddress]
    );
}

const MAX_CLOCK_DRIFT_SECONDS = 300;

/**
 * Try base64 first (canonical), fall back to base58 for backward compat.
 * Per P0 decision: base64 is the canonical format going forward.
 */
const decodeSignature = (signatureStr: string): Uint8Array => {
  // Try base64 first (canonical)
  try {
    const buf = Buffer.from(signatureStr, "base64");
    if (buf.length === 64) return new Uint8Array(buf);
  } catch {
    // not base64
  }

  // Fallback: base58 (legacy Solana-era format)
  try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const bs58Default = require("bs58").default as { decode: (input: string) => Uint8Array };
    const decoded = bs58Default.decode(signatureStr);
    if (decoded.length === 64) return new Uint8Array(decoded);
  } catch {
    // not base58 either
  }

  throw new Error("Signature must be base64 (preferred) or base58 encoded");
};

export const requireWalletAuth: RequestHandler = (req, res, next) => {
  const address = req.header("X-WALLET-ADDRESS");
  const signatureEncoded = req.header("X-WALLET-SIGNATURE");
  const timestampHeader = req.header("X-WALLET-TIMESTAMP");

  if (!address || !signatureEncoded || !timestampHeader) {
    res.status(401).json({ error: "Missing wallet authentication headers" });
    return;
  }

  const timestamp = Number(timestampHeader);
  if (!Number.isFinite(timestamp)) {
    res.status(401).json({ error: "Invalid wallet timestamp" });
    return;
  }

  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - timestamp) > MAX_CLOCK_DRIFT_SECONDS) {
    res.status(401).json({ error: "Wallet timestamp outside accepted window" });
    return;
  }

  try {
    // Validate Stellar address with full checksum + version byte check
    if (!StrKey.isValidEd25519PublicKey(address)) {
      res.status(401).json({ error: "Invalid Stellar public key" });
      return;
    }

    const pubkeyBytes = StrKey.decodeEd25519PublicKey(address);
    const signature = decodeSignature(signatureEncoded);
    const message = new TextEncoder().encode(`asgcard-auth:${timestamp}`);
    const verified = nacl.sign.detached.verify(message, signature, pubkeyBytes);

    if (!verified) {
      res.status(401).json({ error: "Invalid wallet signature" });
      return;
    }

    req.walletContext = {
      address,
      timestamp
    };

    // Track DAA (Daily Active Agents) — fire-and-forget
    trackApiActivity(address).catch(() => {});

    next();
  } catch {
    res.status(401).json({ error: "Invalid wallet authentication payload" });
  }
};
