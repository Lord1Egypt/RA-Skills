"use strict";

const fs = require("fs");
const paths = require("./paths");
const { ensureDir, readJson, writePrivateJson } = require("./fsutil");

async function ensureWallet() {
  ensureDir(paths.APP_DIR);
  if (fs.existsSync(paths.WALLET_PATH)) {
    return { wallet: readJson(paths.WALLET_PATH), created: false };
  }
  const { generatePrivateKey, privateKeyToAccount } = require("viem/accounts");
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  const wallet = {
    address: account.address,
    privateKey,
    chain: "base",
    network: "base-mainnet",
    createdAt: new Date().toISOString(),
  };
  writePrivateJson(paths.WALLET_PATH, wallet);
  return { wallet, created: true };
}

function loadWallet() {
  if (!fs.existsSync(paths.WALLET_PATH)) {
    console.error("Wallet not found. Run: x402-agent-voice init");
    process.exit(1);
  }
  return readJson(paths.WALLET_PATH);
}

module.exports = { ensureWallet, loadWallet };
