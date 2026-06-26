#!/usr/bin/env node

import crypto from "crypto";
import fs from "fs";
import path from "path";
import os from "os";
import readline from "readline";
import { DchatBot } from "./bot.js";
import { NknClient } from "./client.js";
import { SafeStorage } from "./storage.js";
import { MessageDb } from "./db.js";
import type { IncomingMessage } from "./types.js";

const DATA_DIR = path.join(os.homedir(), ".dchat-clawhub");

// ── Identity helpers ───────────────────────────────────────

/**
 * Get or create a random passphrase for encrypting the identity at rest.
 *
 * The passkey is stored in a SEPARATE directory from the encrypted identity
 * (OS config dir vs data dir) so the encryption key is not alongside the
 * ciphertext. This means a leak of ~/.dchat-clawhub/identity.enc alone
 * does not expose the seed.
 *
 * Passkey location: ~/.config/dchat-clawhub/.passkey (mode 0600)
 * Identity location: ~/.dchat-clawhub/identity.enc (mode 0600)
 */
function getPassphrase(dataDir: string): string {
  // Use XDG_CONFIG_HOME or platform-appropriate config dir, separate from dataDir
  const configBase = process.env.XDG_CONFIG_HOME ?? path.join(os.homedir(), ".config");
  const configDir = path.join(configBase, "dchat-clawhub");
  const keyFile = path.join(configDir, ".passkey");

  // Migration: move legacy .passkey from dataDir if present
  const legacyKeyFile = path.join(dataDir, ".passkey");
  if (fs.existsSync(legacyKeyFile) && !fs.existsSync(keyFile)) {
    fs.mkdirSync(configDir, { recursive: true });
    fs.renameSync(legacyKeyFile, keyFile);
    fs.chmodSync(keyFile, 0o600);
    return fs.readFileSync(keyFile, "utf-8").trim();
  }

  if (fs.existsSync(keyFile)) {
    return fs.readFileSync(keyFile, "utf-8").trim();
  }

  const passphrase = crypto.randomBytes(32).toString("base64url");
  fs.mkdirSync(configDir, { recursive: true });
  fs.writeFileSync(keyFile, passphrase, { mode: 0o600 });
  return passphrase;
}

function loadOrCreateIdentity(dataDir: string): { seed: string; address: string; isNew: boolean } {
  fs.mkdirSync(dataDir, { recursive: true });
  const storage = new SafeStorage(dataDir);
  const passphrase = getPassphrase(dataDir);

  if (storage.exists()) {
    const identity = storage.load(passphrase);
    if (identity) return { ...identity, isNew: false };
  }

  // Migrate legacy plaintext seed
  const legacySeedFile = path.join(dataDir, "seed");
  if (fs.existsSync(legacySeedFile)) {
    const seed = fs.readFileSync(legacySeedFile, "utf-8").trim();
    const address = NknClient.deriveAddress(seed);
    storage.save({ seed, address }, passphrase);
    fs.unlinkSync(legacySeedFile);
    return { seed, address, isNew: false };
  }

  const seed = NknClient.generateSeed();
  const address = NknClient.deriveAddress(seed);
  storage.save({ seed, address }, passphrase);
  return { seed, address, isNew: true };
}

// ── Sub-command handlers ───────────────────────────────────

function cmdHelp() {
  console.log(`dchat — Decentralized P2P bot communication over NKN

Commands:
  dchat init                          Generate bot identity (no network needed)
  dchat address                       Print bot's NKN address (no network needed)
  dchat send <to> <message>           Send a text message
  dchat send-image <to> <path>        Send an image
  dchat send-audio <to> <path>        Send an audio file
  dchat send-file <to> <path>         Send a file
  dchat history <peer> [limit]        Show message history with a peer
  dchat contacts add <address> <alias>  Add a contact with alias
  dchat contacts remove <alias>         Remove a contact
  dchat contacts list                   List all contacts
  dchat listen                        Listen for incoming messages (daemon)
  dchat interactive                   Start interactive REPL
  dchat help                          Show this help

<to> and <peer> accept either a 64-char NKN address or a contact alias.

Options:
  --seed <hex>          Use specific seed (overrides stored identity)
  --data-dir <path>     Custom data directory (default: ~/.dchat-clawhub)

Data stored in: ${DATA_DIR}`);
}

/** Resolve an alias or address to an NKN address using the contacts DB. */
function resolveAddress(dataDir: string, addressOrAlias: string): string {
  if (/^[0-9a-f]{64}$/i.test(addressOrAlias)) return addressOrAlias;
  const db = new MessageDb(dataDir);
  const resolved = db.resolveAlias(addressOrAlias);
  db.close();
  if (!resolved) {
    console.error(`Unknown contact: "${addressOrAlias}". Use 'dchat contacts list' to see contacts.`);
    process.exit(1);
  }
  return resolved;
}

function cmdInit(dataDir: string) {
  const identity = loadOrCreateIdentity(dataDir);
  if (identity.isNew) {
    console.log("Generated new bot identity.");
  } else {
    console.log("Bot identity already exists.");
  }
  console.log(`Address: ${identity.address}`);
  console.log(`Data dir: ${dataDir}`);
}

function cmdAddress(dataDir: string, explicitSeed?: string) {
  if (explicitSeed) {
    console.log(NknClient.deriveAddress(explicitSeed));
    return;
  }
  const identity = loadOrCreateIdentity(dataDir);
  console.log(identity.address);
}

async function cmdSend(dataDir: string, seed: string, target: string, message: string) {
  const bot = new DchatBot({ seed, dataDir });
  console.log("Connecting...");
  await bot.start();
  // Wait for all sub-clients to establish relay routes
  await new Promise((r) => setTimeout(r, 3000));
  const id = await bot.sendTextAwait(target, message);
  console.log(`Sent: ${id}`);
  process.exit(0);
}

async function cmdSendMedia(
  dataDir: string,
  seed: string,
  type: "image" | "audio" | "file",
  target: string,
  filePath: string,
) {
  const bot = new DchatBot({ seed, dataDir });
  console.log("Connecting...");
  await bot.start();
  await new Promise((r) => setTimeout(r, 3000));
  let id: string;
  switch (type) {
    case "image":
      id = await bot.sendImage(target, filePath);
      break;
    case "audio":
      id = await bot.sendAudio(target, filePath);
      break;
    case "file":
      id = await bot.sendFile(target, filePath);
      break;
  }
  console.log(`Sent ${type}: ${id}`);
  process.exit(0);
}

function cmdHistory(dataDir: string, seed: string, peerAddress: string, limit: number) {
  const bot = new DchatBot({ seed, dataDir });
  const msgs = bot.getMessages(peerAddress, limit);
  if (msgs.length === 0) {
    console.log("No messages.");
  } else {
    for (const m of msgs) {
      const dir = m.isOutbound ? "→" : "←";
      const time = new Date(m.createdAt).toISOString().substring(11, 19);
      const preview = m.content.length > 80 ? m.content.substring(0, 80) + "..." : m.content;
      console.log(`${dir} [${time}] (${m.contentType}) ${preview}`);
    }
  }
  bot.stop().catch(() => {});
}

async function cmdListen(dataDir: string, seed: string) {
  const bot = new DchatBot({ seed, dataDir });
  const contactDb = new MessageDb(dataDir);
  const shutdown = async () => {
    console.log("\nShutting down...");
    contactDb.close();
    await bot.stop();
    process.exit(0);
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);

  bot.on("message", (msg: IncomingMessage) => {
    const time = new Date(msg.timestamp).toISOString().substring(11, 19);
    const alias = contactDb.getAlias(msg.from);
    const from = alias ?? msg.from.substring(0, 16) + "...";
    switch (msg.contentType) {
      case "text":
      case "textExtension":
        console.log(`[${time}] ${from}: ${msg.content}`);
        break;
      case "image":
        console.log(`[${time}] ${from}: [image] ${msg.localFilePath ?? msg.content}`);
        break;
      case "audio":
        console.log(`[${time}] ${from}: [audio] ${msg.localFilePath ?? "(inline)"}`);
        break;
      case "file": {
        const fileName = msg.options?.fileName ?? "file";
        console.log(`[${time}] ${from}: [file: ${fileName}] ${msg.localFilePath ?? msg.content}`);
        break;
      }
    }
  });

  console.log("Connecting...");
  const address = await bot.start();
  console.log(`Listening as ${address} (Ctrl+C to exit)`);
}

async function cmdInteractive(dataDir: string, seed: string) {
  const bot = new DchatBot({ seed, dataDir });
  const contactDb = new MessageDb(dataDir);
  const shutdown = async () => {
    console.log("\nShutting down...");
    contactDb.close();
    await bot.stop();
    process.exit(0);
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);

  bot.on("message", (msg: IncomingMessage) => {
    const time = new Date(msg.timestamp).toISOString().substring(11, 19);
    const alias = contactDb.getAlias(msg.from);
    const from = alias ?? msg.from.substring(0, 16) + "...";
    switch (msg.contentType) {
      case "text":
      case "textExtension":
        console.log(`\n[${time}] ${from}: ${msg.content}`);
        break;
      case "image":
        console.log(`\n[${time}] ${from}: [image] ${msg.localFilePath ?? msg.content}`);
        break;
      case "audio":
        console.log(`\n[${time}] ${from}: [audio] ${msg.localFilePath ?? "(inline)"}`);
        break;
      case "file": {
        const fileName = msg.options?.fileName ?? "file";
        console.log(`\n[${time}] ${from}: [file: ${fileName}] ${msg.localFilePath ?? msg.content}`);
        break;
      }
    }
    rl.prompt();
  });

  console.log("Connecting...");
  const address = await bot.start();
  console.log(`Bot address: ${address}\n`);
  console.log("Commands: /send /image /audio /file /history /address /quit\n");

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  rl.setPrompt("> ");
  rl.prompt();

  rl.on("line", async (line: string) => {
    const trimmed = line.trim();
    if (!trimmed) { rl.prompt(); return; }
    const parts = trimmed.split(/\s+/);
    const cmd = parts[0];
    try {
      switch (cmd) {
        case "/send": {
          const [, addr, ...rest] = parts;
          if (!addr || rest.length === 0) { console.log("Usage: /send <address> <message>"); break; }
          console.log(`Sent: ${bot.sendText(addr, rest.join(" "))}`);
          break;
        }
        case "/image": {
          if (!parts[1] || !parts[2]) { console.log("Usage: /image <address> <path>"); break; }
          console.log(`Sent image: ${await bot.sendImage(parts[1], parts[2])}`);
          break;
        }
        case "/audio": {
          if (!parts[1] || !parts[2]) { console.log("Usage: /audio <address> <path>"); break; }
          console.log(`Sent audio: ${await bot.sendAudio(parts[1], parts[2])}`);
          break;
        }
        case "/file": {
          if (!parts[1] || !parts[2]) { console.log("Usage: /file <address> <path>"); break; }
          console.log(`Sent file: ${await bot.sendFile(parts[1], parts[2])}`);
          break;
        }
        case "/history": {
          if (!parts[1]) { console.log("Usage: /history <address>"); break; }
          const msgs = bot.getMessages(parts[1]);
          if (msgs.length === 0) { console.log("No messages."); }
          else {
            for (const m of msgs) {
              const dir = m.isOutbound ? "→" : "←";
              const t = new Date(m.createdAt).toISOString().substring(11, 19);
              const p = m.content.length > 80 ? m.content.substring(0, 80) + "..." : m.content;
              console.log(`  ${dir} [${t}] (${m.contentType}) ${p}`);
            }
          }
          break;
        }
        case "/address":
          console.log(bot.address);
          break;
        case "/quit":
        case "/exit":
          await shutdown();
          break;
        default:
          console.log(`Unknown command: ${cmd}`);
      }
    } catch (err) {
      console.error("Error:", err instanceof Error ? err.message : err);
    }
    rl.prompt();
  });

  rl.on("close", shutdown);
}

// ── Main: parse args and dispatch ──────────────────────────

async function main() {
  const args = process.argv.slice(2);

  // Extract global options first
  let dataDir = DATA_DIR;
  let explicitSeed: string | undefined;
  const positional: string[] = [];

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--data-dir":
        dataDir = args[++i];
        break;
      case "--seed":
        explicitSeed = args[++i];
        break;
      default:
        positional.push(args[i]);
    }
  }

  const subcommand = positional[0] ?? "help";

  // Resolve seed for commands that need it
  const resolveSeed = (): string => {
    if (explicitSeed) return explicitSeed;
    return loadOrCreateIdentity(dataDir).seed;
  };

  switch (subcommand) {
    case "help":
    case "--help":
    case "-h":
      cmdHelp();
      break;

    case "init":
      cmdInit(dataDir);
      break;

    case "address":
      cmdAddress(dataDir, explicitSeed);
      break;

    case "contacts": {
      const action = positional[1];
      const db = new MessageDb(dataDir);
      switch (action) {
        case "add": {
          const addr = positional[2];
          const alias = positional[3];
          if (!addr || !alias) {
            console.error("Usage: dchat contacts add <address> <alias>");
            process.exit(1);
          }
          if (!/^[0-9a-f]{64}$/i.test(addr)) {
            console.error("Address must be a 64-character hex string.");
            process.exit(1);
          }
          db.addContact(addr, alias);
          console.log(`Added contact: ${alias} → ${addr}`);
          break;
        }
        case "remove": {
          const target = positional[2];
          if (!target) {
            console.error("Usage: dchat contacts remove <alias|address>");
            process.exit(1);
          }
          if (db.removeContact(target)) {
            console.log(`Removed contact: ${target}`);
          } else {
            console.error(`Contact not found: ${target}`);
          }
          break;
        }
        case "list": {
          const contacts = db.listContacts();
          if (contacts.length === 0) {
            console.log("No contacts.");
          } else {
            for (const c of contacts) {
              const alias = c.name ? `${c.name} ` : "";
              console.log(`  ${alias}${c.address}`);
            }
          }
          break;
        }
        default:
          console.error("Usage: dchat contacts <add|remove|list>");
          process.exit(1);
      }
      db.close();
      break;
    }

    case "send": {
      const target = positional[1];
      const message = positional.slice(2).join(" ");
      if (!target || !message) {
        console.error("Usage: dchat send <address|alias> <message>");
        process.exit(1);
      }
      await cmdSend(dataDir, resolveSeed(), resolveAddress(dataDir, target), message);
      break;
    }

    case "send-image": {
      if (!positional[1] || !positional[2]) {
        console.error("Usage: dchat send-image <address|alias> <path>");
        process.exit(1);
      }
      await cmdSendMedia(dataDir, resolveSeed(), "image", resolveAddress(dataDir, positional[1]), positional[2]);
      break;
    }

    case "send-audio": {
      if (!positional[1] || !positional[2]) {
        console.error("Usage: dchat send-audio <address|alias> <path>");
        process.exit(1);
      }
      await cmdSendMedia(dataDir, resolveSeed(), "audio", resolveAddress(dataDir, positional[1]), positional[2]);
      break;
    }

    case "send-file": {
      if (!positional[1] || !positional[2]) {
        console.error("Usage: dchat send-file <address|alias> <path>");
        process.exit(1);
      }
      await cmdSendMedia(dataDir, resolveSeed(), "file", resolveAddress(dataDir, positional[1]), positional[2]);
      break;
    }

    case "history": {
      if (!positional[1]) {
        console.error("Usage: dchat history <address|alias> [limit]");
        process.exit(1);
      }
      const limit = positional[2] ? parseInt(positional[2], 10) : 50;
      cmdHistory(dataDir, resolveSeed(), resolveAddress(dataDir, positional[1]), limit);
      break;
    }

    case "listen":
      await cmdListen(dataDir, resolveSeed());
      break;

    case "interactive":
      await cmdInteractive(dataDir, resolveSeed());
      break;

    default:
      console.error(`Unknown command: ${subcommand}\nRun 'dchat help' for usage.`);
      process.exit(1);
  }
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
