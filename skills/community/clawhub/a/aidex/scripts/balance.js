#!/usr/bin/env node

// Get token balances for a wallet address.
// Zero address (0x0000...0) = native ETH balance.
// Maximum 9 tokens per request.

import { getBalances } from "./lib/api.js";
import { parseArgs, output, normalizeAddress, normalizeToken, requireArg, unwrap } from "./lib/utils.js";

const args = parseArgs(process.argv);

const address = normalizeAddress(requireArg(args, "address"));
if (!address) {
  output({ success: false, error: "Invalid --address: must be a valid Ethereum address." });
}

const tokens = requireArg(args, "tokens").split(",").map(normalizeToken).filter(Boolean);

if (tokens.length === 0) {
  output({ success: false, error: "At least one token address is required." });
}

if (tokens.length > 9) {
  output({ success: false, error: "Too many tokens. Maximum is 9 per request." });
}

const balances = unwrap(await getBalances(address, tokens));

output({ success: true, balances });
