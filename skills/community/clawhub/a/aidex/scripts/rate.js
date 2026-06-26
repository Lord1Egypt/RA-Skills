#!/usr/bin/env node

// Get exchange rate for a token pair (read-only).

import { getRate } from "./lib/api.js";
import { isAmount, parseArgs, output, parseSwapInput, resultTypeToError, unwrap } from "./lib/utils.js";

const args = parseArgs(process.argv);
const { tokenIn, tokenOut, amountIn } = parseSwapInput(args);

const data = unwrap(await getRate(tokenIn, tokenOut, amountIn));

const resultError = resultTypeToError(data.resultType);
if (resultError) {
  output({ success: false, error: resultError });
}

if (!isAmount(data.rate)
    || !isAmount(data.amountOut)
    || typeof data.estimatedGasPriceUsd !== "number") {
  output({ success: false, error: "AIDEX is temporarily unavailable. Please try again later." });
}

output({
  success: true,
  rate: data.rate,
  amountOut: data.amountOut,
  estimatedGasPriceUsd: data.estimatedGasPriceUsd,
});
