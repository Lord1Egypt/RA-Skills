#!/usr/bin/env node
import { createClient, loadWallet, parseArgs, exitError, runMain, jsonStringify } from "./_helpers.js";
import { parseEther } from "atxswap-sdk";

await runMain(async () => {
  const client = await createClient();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command) {
    exitError("Usage: transfer.js <bnb|atx|usdt|token> <to> <amount> [tokenAddress] [--from address] [--password <pwd>]");
  }

  const fromAddress = args.from || client.wallet.list()[0]?.address;
  if (!fromAddress) exitError("No wallet found. Create one first.");

  const wallet = await loadWallet(client, fromAddress, args);

  switch (command) {
    case "bnb": {
      const to = args._[1];
      const amount = args._[2];
      if (!to || !amount) exitError("Usage: transfer.js bnb <to> <amount> [--from address]");
      const result = await client.transfer.sendBnb(wallet, to, parseEther(amount));
      console.log(jsonStringify({ action: "send BNB", to, amount, txHash: result.txHash }, 2));
      break;
    }

    case "atx": {
      const to = args._[1];
      const amount = args._[2];
      if (!to || !amount) exitError("Usage: transfer.js atx <to> <amount> [--from address]");
      const result = await client.transfer.sendAtx(wallet, to, parseEther(amount));
      console.log(jsonStringify({ action: "send ATX", to, amount, txHash: result.txHash }, 2));
      break;
    }

    case "usdt": {
      const to = args._[1];
      const amount = args._[2];
      if (!to || !amount) exitError("Usage: transfer.js usdt <to> <amount> [--from address]");
      const result = await client.transfer.sendUsdt(wallet, to, parseEther(amount));
      console.log(jsonStringify({ action: "send USDT", to, amount, txHash: result.txHash }, 2));
      break;
    }

    case "token": {
      const tokenAddr = args._[1];
      const to = args._[2];
      const amount = args._[3];
      if (!tokenAddr || !to || !amount) {
        exitError("Usage: transfer.js token <tokenAddress> <to> <amount> [--from address]");
      }
      const result = await client.transfer.sendToken(wallet, tokenAddr, to, parseEther(amount));
      console.log(jsonStringify({ action: "send token", token: tokenAddr, to, amount, txHash: result.txHash }, 2));
      break;
    }

    default:
      exitError("Usage: transfer.js <bnb|atx|usdt|token> [args]");
  }
});
