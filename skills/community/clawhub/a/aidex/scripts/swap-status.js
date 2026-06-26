#!/usr/bin/env node

// Check swap operation status by transaction hashes (1-3 hashes: approve + swap).
// Returns high-level status (pending/completed/failed) and details per step.

import { getSwapStatus } from "./lib/api.js";
import { parseArgs, output, normalizeTxHash, requireArg, unwrap } from "./lib/utils.js";

const args = parseArgs(process.argv);

const rawHashes = requireArg(args, "hashes").split(",").map((h) => h.trim()).filter(Boolean);

if (rawHashes.length === 0 || rawHashes.length > 3) {
  output({ success: false, error: "Expected 1 to 3 transaction hashes, comma-separated." });
}

const hashes = rawHashes.map((h) => {
  const normalized = normalizeTxHash(h);
  if (!normalized) {
    output({ success: false, error: `Invalid hash: ${h}. Must be 0x followed by 64 hex characters.` });
  }
  return normalized;
});

const data = unwrap(await getSwapStatus(hashes));

output({ success: true, ...data });
