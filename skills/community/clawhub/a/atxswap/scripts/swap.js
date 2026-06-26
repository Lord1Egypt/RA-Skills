#!/usr/bin/env node
import { createClient, loadWallet, parseArgs, fmt, exitError, runMain, jsonStringify } from "./_helpers.js";
import { parseEther } from "atxswap-sdk";

await runMain(async () => {
  const client = await createClient();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  const amount = args._[1];

  if (!command || !amount || !["buy", "sell"].includes(command)) {
    exitError("Usage: swap.js <buy|sell> <amount> [--from address] [--slippage bps] [--password <pwd>]");
  }

  const fromAddress = args.from || client.wallet.list()[0]?.address;
  if (!fromAddress) exitError("No wallet found. Create one first.");

  const wallet = await loadWallet(client, fromAddress, args);
  const amountWei = parseEther(amount);
  const slippage = args.slippage ? parseInt(args.slippage) : undefined;

  if (command === "buy") {
    const result = await client.swap.buy(wallet, amountWei, slippage);
    console.log(jsonStringify({
      action: "buy ATX",
      txHash: result.txHash,
      usdtSpent: fmt(result.amountIn),
      atxReceived: fmt(result.amountOut),
    }, 2));
  } else {
    const result = await client.swap.sell(wallet, amountWei, slippage);
    console.log(jsonStringify({
      action: "sell ATX",
      txHash: result.txHash,
      atxSold: fmt(result.amountIn),
      usdtReceived: fmt(result.amountOut),
    }, 2));
  }
});
