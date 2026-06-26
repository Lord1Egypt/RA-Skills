#!/usr/bin/env node

// Derives wallet address from the private key.
// Does not call the API — purely client-side operation.

import { output, resolveWallet } from "./lib/utils.js";

const wallet = await resolveWallet();
output({ success: true, address: wallet.address });
