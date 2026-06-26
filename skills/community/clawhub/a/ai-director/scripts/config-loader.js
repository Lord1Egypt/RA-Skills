#!/usr/bin/env node
/**
 * Multi-User Config Loader for AI Director
 * Loads user-specific config from credentials/{USER_ID}.json
 */

const fs = require("fs");
const path = require("path");

function loadUserConfig() {
  const USER_ID = process.env.USER_ID || process.env.TELEGRAM_USER_ID;

  if (!USER_ID) {
    console.error("❌ USER_ID or TELEGRAM_USER_ID environment variable required");
    console.error("   Set it when calling the script: USER_ID=5470522468 node ad-producer.js ...");
    process.exit(1);
  }

  const credentialsPath = path.join(__dirname, "..", "credentials", `${USER_ID}.json`);

  if (!fs.existsSync(credentialsPath)) {
    console.error(`❌ No config found for user ${USER_ID}`);
    console.error(`   Create: ${credentialsPath}`);
    console.error(`   Copy from: config.example.json`);
    process.exit(1);
  }

  try {
    const config = JSON.parse(fs.readFileSync(credentialsPath, "utf8"));
    return { config, userId: USER_ID, credentialsPath };
  } catch (e) {
    console.error(`❌ Failed to load config for user ${USER_ID}: ${e.message}`);
    process.exit(1);
  }
}

function saveUserConfig(config) {
  const USER_ID = process.env.USER_ID || process.env.TELEGRAM_USER_ID;
  if (!USER_ID) {
    throw new Error("USER_ID not set");
  }

  const credentialsPath = path.join(__dirname, "..", "credentials", `${USER_ID}.json`);
  fs.writeFileSync(credentialsPath, JSON.stringify(config, null, 2));
}

function getStatePath(userId, filename = "state.json") {
  const stateDir = path.join(__dirname, "..", "state");
  if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
  }
  return path.join(stateDir, `${userId}.${filename}`);
}

module.exports = { loadUserConfig, saveUserConfig, getStatePath };
