#!/usr/bin/env node

import { z } from "zod";
import { appConfig } from "./config.js";
import { BridgeService } from "./services/bridgeService.js";
import { HyperliquidService } from "./services/hyperliquidService.js";
import { HyperliquidTradingService } from "./services/hyperliquidTradingService.js";
import { RiskService } from "./services/riskService.js";
import { SolanaBalanceService } from "./services/solanaBalanceService.js";
import { SolanaTokenService } from "./services/solanaTokenService.js";
import { SolanaWalletService } from "./services/solanaWalletService.js";
import { SwapService } from "./services/swapService.js";
import { TokenService } from "./services/tokenService.js";
import { WalletService } from "./services/walletService.js";
import { bridgeTokenTool } from "./tools/bridgeToken.js";
import { cancelHyperliquidOrderTool } from "./tools/cancelHyperliquidOrder.js";
import { depositToHyperliquidTool } from "./tools/depositToHyperliquid.js";
import { getBalancesTool } from "./tools/getBalances.js";
import { getHyperliquidAccountStateTool } from "./tools/getHyperliquidAccountState.js";
import { getHyperliquidMarketStateTool } from "./tools/getHyperliquidMarketState.js";
import { placeHyperliquidOrderTool } from "./tools/placeHyperliquidOrder.js";
import { protectHyperliquidPositionTool } from "./tools/protectHyperliquidPosition.js";
import { quoteOperationTool } from "./tools/quoteOperation.js";
import { safetyCheckTool } from "./tools/safetyCheck.js";
import { swapTokenTool } from "./tools/swapToken.js";
import { transferTokenTool } from "./tools/transferToken.js";
import { buildFailure, toErrorMessage } from "./utils/formatting.js";
import { safeParseJsonInput } from "./utils/validation.js";

function readCliArgs(): { action?: string; input?: string } {
  const args = process.argv.slice(2);
  const parsed: { action?: string; input?: string } = {};

  for (let index = 0; index < args.length; index += 1) {
    const current = args[index];
    const next = args[index + 1];

    if (current === "--action" && next) {
      parsed.action = next;
      index += 1;
      continue;
    }

    if (current === "--input" && next) {
      parsed.input = next;
      index += 1;
    }
  }

  return parsed;
}

async function maybeReadStdin(): Promise<string | undefined> {
  if (process.stdin.isTTY) {
    return undefined;
  }

  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.from(chunk));
  }
  const content = Buffer.concat(chunks).toString("utf8").trim();
  return content || undefined;
}

function printJson(value: unknown): void {
  console.log(
    JSON.stringify(
      value,
      (_, currentValue) => (typeof currentValue === "bigint" ? currentValue.toString() : currentValue),
      2
    )
  );
}

async function main(): Promise<void> {
  const cli = readCliArgs();
  const stdinInput = await maybeReadStdin();
  const action = cli.action;
  const rawInput = cli.input ?? stdinInput;

  if (!action) {
    printJson(
      buildFailure("quote_operation", "startup", "error", [
        "Missing --action. Supported actions: get_balances, transfer_token, swap_token, bridge_token, deposit_to_hyperliquid, get_hyperliquid_market_state, get_hyperliquid_account_state, place_hyperliquid_order, protect_hyperliquid_position, cancel_hyperliquid_order, safety_check, quote_operation."
      ])
    );
    process.exitCode = 1;
    return;
  }

  const walletService = new WalletService();
  const solanaWalletService = new SolanaWalletService();
  const solanaTokenService = new SolanaTokenService(solanaWalletService);
  const tokenService = new TokenService(walletService);
  const solanaBalanceService = new SolanaBalanceService();
  const swapService = new SwapService(walletService, tokenService);
  const bridgeService = new BridgeService(walletService, tokenService, solanaWalletService);
  const riskService = new RiskService(walletService);
  const hyperliquidService = new HyperliquidService(walletService, tokenService, bridgeService);
  const hyperliquidTradingService = new HyperliquidTradingService(walletService);

  const input = safeParseJsonInput(rawInput);

  let response;
  switch (action) {
    case "get_balances":
      response = await getBalancesTool(input, tokenService, solanaBalanceService);
      break;
    case "transfer_token":
      response = await transferTokenTool(input, walletService, tokenService, riskService);
      break;
    case "swap_token":
      response = await swapTokenTool(input, walletService, tokenService, swapService, riskService);
      break;
    case "bridge_token":
      response = await bridgeTokenTool(
        input,
        walletService,
        solanaWalletService,
        tokenService,
        solanaTokenService,
        bridgeService,
        riskService
      );
      break;
    case "deposit_to_hyperliquid":
      response = await depositToHyperliquidTool(input, walletService, hyperliquidService, riskService);
      break;
    case "get_hyperliquid_market_state":
      response = await getHyperliquidMarketStateTool(input, hyperliquidTradingService);
      break;
    case "get_hyperliquid_account_state":
      response = await getHyperliquidAccountStateTool(input, hyperliquidTradingService);
      break;
    case "place_hyperliquid_order":
      response = await placeHyperliquidOrderTool(input, hyperliquidTradingService);
      break;
    case "protect_hyperliquid_position":
      response = await protectHyperliquidPositionTool(input, hyperliquidTradingService);
      break;
    case "cancel_hyperliquid_order":
      response = await cancelHyperliquidOrderTool(input, hyperliquidTradingService);
      break;
    case "safety_check":
      response = await safetyCheckTool(input, riskService);
      break;
    case "quote_operation":
      response = await quoteOperationTool(
        input,
        walletService,
        tokenService,
        solanaWalletService,
        solanaTokenService,
        swapService,
        bridgeService,
        hyperliquidService,
        hyperliquidTradingService
      );
      break;
    case "--help":
    case "help":
      printJson({
        name: "crypto-treasury-ops",
        actions: [
          "get_balances",
          "transfer_token",
          "swap_token",
          "bridge_token",
          "deposit_to_hyperliquid",
          "get_hyperliquid_market_state",
          "get_hyperliquid_account_state",
          "place_hyperliquid_order",
          "protect_hyperliquid_position",
          "cancel_hyperliquid_order",
          "safety_check",
          "quote_operation"
        ],
        dryRunDefault: appConfig.safety.dryRunDefault
      });
      return;
    default:
      throw new Error(`Unsupported action "${action}".`);
  }

  printJson(response);
  if (!response.ok) {
    process.exitCode = 1;
  }
}

main().catch((error: unknown) => {
  const failedAction = readCliArgs().action;
  const tool =
    failedAction &&
    [
      "get_balances",
      "transfer_token",
      "swap_token",
      "bridge_token",
      "deposit_to_hyperliquid",
      "get_hyperliquid_market_state",
      "get_hyperliquid_account_state",
      "place_hyperliquid_order",
      "protect_hyperliquid_position",
      "cancel_hyperliquid_order",
      "safety_check",
      "quote_operation"
    ].includes(failedAction)
      ? failedAction
      : "quote_operation";
  const message =
    error instanceof z.ZodError
      ? error.issues.map((issue) => issue.message).join("; ")
      : toErrorMessage(error);

  printJson(buildFailure(tool as Parameters<typeof buildFailure>[0], "runtime", "error", [message]));
  process.exitCode = 1;
});
