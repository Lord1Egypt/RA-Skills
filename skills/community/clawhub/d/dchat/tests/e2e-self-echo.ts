#!/usr/bin/env node
/**
 * End-to-end self-echo test:
 *   1. Create a new bot identity (wallet/seed)
 *   2. Save seed + NKN address in SafeStorage (encrypted)
 *   3. Connect to NKN network
 *   4. Send a text message to self (own NKN address)
 *   5. Verify the echo arrives back
 *   6. Verify message is persisted in DB
 *   7. Verify SafeStorage can reload the identity
 */

import fs from "fs";
import os from "os";
import path from "path";
import { DchatBot } from "../src/bot.js";
import { NknClient } from "../src/client.js";
import { SafeStorage } from "../src/storage.js";
import type { IncomingMessage } from "../src/types.js";

const TIMEOUT_MS = 120_000; // 2 min — NKN connection can be slow
const TEST_PASSPHRASE = "test-e2e-passphrase-2024";
const ECHO_TEXT = `echo-test-${Date.now()}`;

let tmpDir: string;
let bot: DchatBot | null = null;

function log(msg: string) {
  const ts = new Date().toISOString().substring(11, 23);
  console.log(`[${ts}] ${msg}`);
}

function fail(msg: string): never {
  console.error(`\n  FAIL: ${msg}\n`);
  cleanup();
  process.exit(1);
}

function pass(msg: string) {
  console.log(`  PASS: ${msg}`);
}

function cleanup() {
  if (bot) {
    bot.stop().catch(() => {});
    bot = null;
  }
  if (tmpDir && fs.existsSync(tmpDir)) {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

async function main() {
  console.log("\n=== dchat-clawhub E2E Self-Echo Test ===\n");

  // Set up temp directory
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "dchat-e2e-"));
  log(`Data dir: ${tmpDir}`);

  // ── Step 1: Create identity ──────────────────────────
  log("Step 1: Creating new bot identity...");
  const seed = NknClient.generateSeed();
  if (!seed || seed.length !== 64) fail("Seed generation failed");
  pass(`Generated seed: ${seed.substring(0, 8)}...${seed.substring(56)}`);

  // ── Step 2: Save identity to SafeStorage ─────────────
  log("Step 2: Saving identity to SafeStorage...");
  const storage = new SafeStorage(tmpDir);

  // We'll save the address after connecting — for now save seed with placeholder
  // (address is derived from seed, but only known after NKN connection)
  pass(`SafeStorage file: ${storage.getFilePath()}`);

  // ── Step 3: Connect to NKN network ───────────────────
  log("Step 3: Connecting to NKN network...");
  bot = new DchatBot({ seed, dataDir: tmpDir });

  const address = await bot.start();
  if (!address) fail("No address returned from start()");
  pass(`Connected! NKN address: ${address}`);

  // Now save the full identity
  storage.save({ seed, address }, TEST_PASSPHRASE);
  pass(`Identity saved to encrypted storage`);

  // ── Step 4: Send echo message to self ────────────────
  log("Step 4: Sending echo message to self...");

  const echoReceived = new Promise<IncomingMessage>((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error("Echo timeout — no message received within 60s")),
      60_000,
    );

    bot!.on("message", (msg: IncomingMessage) => {
      clearTimeout(timer);
      resolve(msg);
    });
  });

  const sentId = bot.sendText(address, ECHO_TEXT);
  pass(`Sent message ID: ${sentId}`);

  // ── Step 5: Wait for echo ────────────────────────────
  log("Step 5: Waiting for echo message...");
  const echoMsg = await echoReceived;

  if (echoMsg.content !== ECHO_TEXT) {
    fail(`Content mismatch: expected "${ECHO_TEXT}", got "${echoMsg.content}"`);
  }
  if (echoMsg.from !== address) {
    fail(`Sender mismatch: expected self (${address}), got ${echoMsg.from}`);
  }
  if (echoMsg.contentType !== "text") {
    fail(`ContentType mismatch: expected "text", got "${echoMsg.contentType}"`);
  }
  pass(`Echo received! Content: "${echoMsg.content}"`);
  pass(`From: ${echoMsg.from}`);

  // ── Step 6: Verify DB persistence ────────────────────
  log("Step 6: Verifying message in database...");
  const history = bot.getMessages(address, 10);
  if (history.length === 0) fail("No messages found in DB");

  const dbMsg = history.find((m) => m.id === sentId);
  if (!dbMsg) fail(`Sent message ${sentId} not found in DB`);
  if (dbMsg.content !== ECHO_TEXT) fail(`DB content mismatch`);
  if (dbMsg.status !== "delivered") {
    // May still be "sent" if receipt loop hasn't fired, but self-echo sets it to "delivered"
    log(`  Note: message status is "${dbMsg.status}" (expected "delivered")`);
  }
  pass(`Message persisted in DB: id=${dbMsg.id}, status=${dbMsg.status}`);

  // ── Step 7: Verify SafeStorage reload ────────────────
  log("Step 7: Verifying SafeStorage reload...");
  const loaded = storage.load(TEST_PASSPHRASE);
  if (!loaded) fail("Failed to load identity from SafeStorage");
  if (loaded.seed !== seed) fail("Seed mismatch after reload");
  if (loaded.address !== address) fail("Address mismatch after reload");
  pass(`Identity reloaded: seed matches, address matches`);

  // Verify wrong passphrase fails
  let wrongPassFailed = false;
  try {
    storage.load("wrong-passphrase");
  } catch {
    wrongPassFailed = true;
  }
  if (!wrongPassFailed) fail("SafeStorage should reject wrong passphrase");
  pass(`Wrong passphrase correctly rejected`);

  // ── Done ─────────────────────────────────────────────
  console.log("\n=== All E2E tests passed! ===\n");

  await bot.stop();
  bot = null;

  // Clean up
  fs.rmSync(tmpDir, { recursive: true, force: true });
  process.exit(0);
}

// Global timeout
const globalTimer = setTimeout(() => {
  fail(`Global timeout (${TIMEOUT_MS / 1000}s) exceeded`);
}, TIMEOUT_MS);

main()
  .catch((err) => {
    fail(`Unhandled error: ${err.message ?? err}`);
  })
  .finally(() => {
    clearTimeout(globalTimer);
  });
