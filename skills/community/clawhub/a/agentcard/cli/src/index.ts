#!/usr/bin/env node

/**
 * @asgcard/cli — ASG Card command line interface
 *
 * Manage virtual cards for AI agents from your terminal.
 * Authenticates via Stellar wallet signature (no API keys needed).
 *
 * Usage:
 *   asgcard login              — Set your Stellar private key
 *   asgcard cards              — List your cards
 *   asgcard card <id>          — Get card details
 *   asgcard card:details <id>  — Get sensitive card info (PAN, CVV)
 *   asgcard card:create        — Create a new card (x402 payment)
 *   asgcard card:fund <id>     — Fund a card (x402 payment)
 *   asgcard card:freeze <id>   — Freeze a card
 *   asgcard card:unfreeze <id> — Unfreeze a card
 *   asgcard pricing            — View pricing tiers
 *   asgcard health             — API health check
 */

import { Command } from "commander";
import chalk from "chalk";
import ora from "ora";
import { ASGCardClient } from "@asgcard/sdk";
import { WalletClient } from "./wallet-client.js";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// ── Config persistence ──────────────────────────────────────

const CONFIG_DIR = join(homedir(), ".asgcard");
const CONFIG_FILE = join(CONFIG_DIR, "config.json");

interface Config {
  privateKey?: string;
  apiUrl?: string;
  rpcUrl?: string;
}

function loadConfig(): Config {
  try {
    if (existsSync(CONFIG_FILE)) {
      return JSON.parse(readFileSync(CONFIG_FILE, "utf-8"));
    }
  } catch {
    // ignore
  }
  return {};
}

function saveConfig(config: Config): void {
  mkdirSync(CONFIG_DIR, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), { mode: 0o600 });
}

function requireKey(): string {
  const config = loadConfig();
  const key = process.env.STELLAR_PRIVATE_KEY || config.privateKey;
  if (!key) {
    console.error(
      chalk.red("❌ No Stellar private key configured.\n") +
        chalk.dim("Run: ") +
        chalk.cyan("asgcard login") +
        chalk.dim(" or set ") +
        chalk.cyan("STELLAR_PRIVATE_KEY") +
        chalk.dim(" env var.")
    );
    process.exit(1);
  }
  return key;
}

function getApiUrl(): string {
  return process.env.ASGCARD_API_URL || loadConfig().apiUrl || "https://api.asgcard.dev";
}

function getRpcUrl(): string | undefined {
  return process.env.STELLAR_RPC_URL || loadConfig().rpcUrl;
}

// ── Formatters ──────────────────────────────────────────────

function formatCard(card: Record<string, unknown>): string {
  const status = card.status === "active"
    ? chalk.green("● active")
    : card.status === "frozen"
      ? chalk.blue("❄ frozen")
      : chalk.dim(String(card.status));

  return [
    `  ${chalk.bold(String(card.cardId || card.id || ""))}`,
    `  Name:    ${card.nameOnCard || card.name || "—"}`,
    `  Balance: ${chalk.green("$" + (card.balance ?? "?"))}`,
    `  Status:  ${status}`,
    `  Created: ${card.createdAt || "—"}`,
  ].join("\n");
}

// ── CLI ─────────────────────────────────────────────────────

const program = new Command();

program
  .name("asgcard")
  .description("ASG Card CLI — virtual cards for AI agents, powered by x402")
  .version("0.1.0");

// ── login ───────────────────────────────────────────────────

program
  .command("login")
  .description("Configure your Stellar private key for wallet authentication")
  .argument("[key]", "Stellar secret key (S...). Omit to enter interactively")
  .option("--api-url <url>", "Custom API URL")
  .option("--rpc-url <url>", "Custom Stellar RPC URL")
  .action(async (key?: string, options?: { apiUrl?: string; rpcUrl?: string }) => {
    let privateKey = key;

    if (!privateKey) {
      // Read from stdin
      const readline = await import("node:readline");
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      privateKey = await new Promise<string>((resolve) => {
        rl.question(chalk.cyan("Enter Stellar secret key (S...): "), (answer) => {
          rl.close();
          resolve(answer.trim());
        });
      });
    }

    if (!privateKey?.startsWith("S")) {
      console.error(chalk.red("❌ Invalid key. Must start with S (Stellar secret key)."));
      process.exit(1);
    }

    const config: Config = {
      ...loadConfig(),
      privateKey,
      ...(options?.apiUrl && { apiUrl: options.apiUrl }),
      ...(options?.rpcUrl && { rpcUrl: options.rpcUrl }),
    };
    saveConfig(config);

    // Derive and display the public key
    const { Keypair } = await import("@stellar/stellar-sdk");
    const kp = Keypair.fromSecret(privateKey);

    console.log(chalk.green("✅ Key saved to ~/.asgcard/config.json"));
    console.log(chalk.dim("   Wallet: ") + chalk.cyan(kp.publicKey()));
    console.log(chalk.dim("   API:    ") + chalk.cyan(config.apiUrl || "https://api.asgcard.dev"));
  });

// ── cards (list) ────────────────────────────────────────────

program
  .command("cards")
  .description("List all your virtual cards")
  .action(async () => {
    const key = requireKey();
    const spinner = ora("Fetching cards...").start();

    try {
      const client = new WalletClient({ privateKey: key, baseUrl: getApiUrl() });
      const result = await client.listCards();
      spinner.stop();

      if (!result.cards || result.cards.length === 0) {
        console.log(chalk.dim("No cards found. Create one with: asgcard card:create"));
        return;
      }

      console.log(chalk.bold(`\n📇 ${result.cards.length} card(s):\n`));
      for (const card of result.cards) {
        console.log(formatCard(card as unknown as Record<string, unknown>));
        console.log();
      }
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── card (get) ──────────────────────────────────────────────

program
  .command("card")
  .description("Get summary for a specific card")
  .argument("<id>", "Card ID")
  .action(async (id: string) => {
    const key = requireKey();
    const spinner = ora("Fetching card...").start();

    try {
      const client = new WalletClient({ privateKey: key, baseUrl: getApiUrl() });
      const result = await client.getCard(id);
      spinner.stop();
      console.log(formatCard(result as unknown as Record<string, unknown>));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── card:details ────────────────────────────────────────────

program
  .command("card:details")
  .description("Get sensitive card details (PAN, CVV, expiry)")
  .argument("<id>", "Card ID")
  .action(async (id: string) => {
    const key = requireKey();
    const spinner = ora("Fetching card details...").start();

    try {
      const client = new WalletClient({ privateKey: key, baseUrl: getApiUrl() });
      const result = await client.getCardDetails(id);
      spinner.stop();

      console.log(chalk.bold("\n🔒 Sensitive Card Details:\n"));
      const details = result as unknown as Record<string, unknown>;
      console.log(`  Card Number:  ${chalk.cyan(String(details.cardNumber || ""))}`);
      console.log(`  CVV:          ${chalk.cyan(String(details.cvv || ""))}`);
      console.log(`  Expiry:       ${chalk.cyan(`${details.expiryMonth}/${details.expiryYear}`)}`);

      const addr = details.billingAddress as Record<string, unknown> | undefined;
      if (addr) {
        console.log(`  Address:      ${addr.street}, ${addr.city}, ${addr.state} ${addr.zip}, ${addr.country}`);
      }
      console.log(chalk.dim("\n  ⚠ Store securely. Rate-limited to 5/hour."));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── card:create ─────────────────────────────────────────────

const VALID_AMOUNTS = ["10", "25", "50", "100", "200", "500"];

program
  .command("card:create")
  .description("Create a new virtual card (pays on-chain via x402)")
  .requiredOption("-a, --amount <amount>", `Card load amount (${VALID_AMOUNTS.join(", ")})`)
  .requiredOption("-n, --name <name>", "Name on card")
  .requiredOption("-e, --email <email>", "Email for notifications")
  .action(async (options: { amount: string; name: string; email: string }) => {
    if (!VALID_AMOUNTS.includes(options.amount)) {
      console.error(chalk.red(`❌ Invalid amount. Choose from: ${VALID_AMOUNTS.join(", ")}`));
      process.exit(1);
    }

    const key = requireKey();
    const spinner = ora(`Creating $${options.amount} card...`).start();

    try {
      const client = new ASGCardClient({
        privateKey: key,
        baseUrl: getApiUrl(),
        rpcUrl: getRpcUrl(),
      });

      const result = await client.createCard({
        amount: Number(options.amount) as 10 | 25 | 50 | 100 | 200 | 500,
        nameOnCard: options.name,
        email: options.email,
      });

      spinner.succeed(chalk.green("Card created!"));
      console.log(formatCard(result.card as unknown as Record<string, unknown>));

      if (result.detailsEnvelope) {
        console.log(chalk.bold("\n🔒 Card Details (one-time):"));
        console.log(`  Number: ${chalk.cyan(result.detailsEnvelope.cardNumber)}`);
        console.log(`  CVV:    ${chalk.cyan(result.detailsEnvelope.cvv)}`);
        console.log(`  Expiry: ${chalk.cyan(`${result.detailsEnvelope.expiryMonth}/${result.detailsEnvelope.expiryYear}`)}`);
      }

      console.log(chalk.dim(`\n  TX: ${result.payment.txHash}`));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── card:fund ───────────────────────────────────────────────

program
  .command("card:fund")
  .description("Fund an existing card (pays on-chain via x402)")
  .argument("<id>", "Card ID to fund")
  .requiredOption("-a, --amount <amount>", `Fund amount (${VALID_AMOUNTS.join(", ")})`)
  .action(async (id: string, options: { amount: string }) => {
    if (!VALID_AMOUNTS.includes(options.amount)) {
      console.error(chalk.red(`❌ Invalid amount. Choose from: ${VALID_AMOUNTS.join(", ")}`));
      process.exit(1);
    }

    const key = requireKey();
    const spinner = ora(`Funding $${options.amount}...`).start();

    try {
      const client = new ASGCardClient({
        privateKey: key,
        baseUrl: getApiUrl(),
        rpcUrl: getRpcUrl(),
      });

      const result = await client.fundCard({
        amount: Number(options.amount) as 10 | 25 | 50 | 100 | 200 | 500,
        cardId: id,
      });

      spinner.succeed(chalk.green(`Funded $${result.fundedAmount}!`));
      console.log(`  Card:        ${result.cardId}`);
      console.log(`  New balance: ${chalk.green("$" + result.newBalance)}`);
      console.log(chalk.dim(`  TX: ${result.payment.txHash}`));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── card:freeze / card:unfreeze ─────────────────────────────

program
  .command("card:freeze")
  .description("Temporarily freeze a card")
  .argument("<id>", "Card ID")
  .action(async (id: string) => {
    const key = requireKey();
    const spinner = ora("Freezing card...").start();

    try {
      const client = new WalletClient({ privateKey: key, baseUrl: getApiUrl() });
      await client.freezeCard(id);
      spinner.succeed(chalk.blue(`❄ Card ${id} frozen`));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

program
  .command("card:unfreeze")
  .description("Unfreeze a frozen card")
  .argument("<id>", "Card ID")
  .action(async (id: string) => {
    const key = requireKey();
    const spinner = ora("Unfreezing card...").start();

    try {
      const client = new WalletClient({ privateKey: key, baseUrl: getApiUrl() });
      await client.unfreezeCard(id);
      spinner.succeed(chalk.green(`🔓 Card ${id} unfrozen`));
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── pricing ─────────────────────────────────────────────────

program
  .command("pricing")
  .description("View current pricing tiers")
  .action(async () => {
    const spinner = ora("Fetching pricing...").start();

    try {
      const client = new ASGCardClient({
        privateKey: "SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVID", // dummy for public endpoint
        baseUrl: getApiUrl(),
      });
      const tiers = await client.getTiers();
      spinner.stop();

      console.log(chalk.bold("\n💰 Card Creation Tiers:\n"));
      console.log(
        chalk.dim("  Load Amount   Total Cost   Endpoint")
      );
      for (const t of tiers.creation) {
        console.log(
          `  ${chalk.green("$" + String(t.loadAmount || "?").padEnd(11))} ${chalk.cyan("$" + String(t.totalCost).padEnd(11))} ${chalk.dim(t.endpoint)}`
        );
      }

      console.log(chalk.bold("\n💰 Card Funding Tiers:\n"));
      console.log(
        chalk.dim("  Fund Amount   Total Cost   Endpoint")
      );
      for (const t of tiers.funding) {
        console.log(
          `  ${chalk.green("$" + String(t.fundAmount || "?").padEnd(11))} ${chalk.cyan("$" + String(t.totalCost).padEnd(11))} ${chalk.dim(t.endpoint)}`
        );
      }
      console.log();
    } catch (error) {
      spinner.fail(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── health ──────────────────────────────────────────────────

program
  .command("health")
  .description("Check API health")
  .action(async () => {
    const spinner = ora("Checking API...").start();

    try {
      const res = await fetch(`${getApiUrl()}/health`);
      const data = await res.json() as Record<string, unknown>;
      spinner.succeed(
        chalk.green("API is healthy ") +
          chalk.dim(`v${data.version} — ${data.timestamp}`)
      );
    } catch (error) {
      spinner.fail(chalk.red(`API unreachable: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

// ── whoami ──────────────────────────────────────────────────

program
  .command("whoami")
  .description("Show your configured wallet address")
  .action(async () => {
    const key = requireKey();
    const { Keypair } = await import("@stellar/stellar-sdk");
    const kp = Keypair.fromSecret(key);
    console.log(chalk.cyan(kp.publicKey()));
  });

program.parse();
