#!/usr/bin/env node

// Search tokens by substring match in symbol, name, and address.

import { searchTokens } from "./lib/api.js";
import { parseArgs, output, unwrap } from "./lib/utils.js";

const args = parseArgs(process.argv);
const tokens = unwrap(await searchTokens(args.term));

output({ success: true, tokens });
