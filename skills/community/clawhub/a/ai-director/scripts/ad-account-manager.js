#!/usr/bin/env node
/**
 * Ad Account Manager - X2C 账号管理模块
 *
 * 使用 X2C Open API 进行账号认证和管理。
 *
 * Usage:
 *   node ad-account-manager.js <command> [options]
 *
 * Commands:
 *   send-code <email>    发送验证码到邮箱
 *   verify <email> <code>  验证并获取 API Key
 *   check-binding        检查账号绑定状态
 *   balance              查询余额（通过 config/get-options）
 *   unbind               解绑账号
 *   help                 显示帮助
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Multi-user config loader
const configLoader = require("./config-loader");

// Configuration
const X2C_API_BASE =
  process.env.X2C_API_BASE_URL || "https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api";

// Load config (multi-user aware)
function loadConfig() {
  try {
    const result = configLoader.loadUserConfig();
    return result.config;
  } catch (e) {
    // If USER_ID not set or config missing, return empty (for initial setup)
    return {};
  }
}

function saveConfig(config) {
  try {
    configLoader.saveUserConfig(config);
  } catch (e) {
    console.error(`Failed to save config: ${e.message}`);
    throw e;
  }
}

// Update unified account.json and sync to all skills
function updateAccountAndSync(x2cData) {
  try {
    let account = {};
    if (fs.existsSync(ACCOUNT_PATH)) {
      account = JSON.parse(fs.readFileSync(ACCOUNT_PATH, "utf8"));
    }
    if (!account.x2c) account.x2c = {};
    if (x2cData.apiKey) account.x2c.apiKey = x2cData.apiKey;
    if (x2cData.userId) account.x2c.userId = x2cData.userId;
    if (x2cData.email) account.x2c.email = x2cData.email;
    fs.writeFileSync(ACCOUNT_PATH, JSON.stringify(account, null, 2) + "\n");

    // Run sync script
    if (fs.existsSync(SYNC_SCRIPT)) {
      require("child_process").execSync(`node "${SYNC_SCRIPT}"`, { stdio: "inherit" });
    }
  } catch (e) {
    console.error(`Warning: Could not sync account.json: ${e.message}`);
  }
}

// HTTP Request helper
function request(action, data = {}, apiKey = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(X2C_API_BASE);

    const payload = JSON.stringify({ action, ...data });

    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(payload),
      },
    };

    if (apiKey) {
      options.headers["X-API-Key"] = apiKey;
    }

    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          if (json.success) {
            resolve(json);
          } else {
            reject(new Error(json.error || json.message || "API Error"));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${body.substring(0, 200)}`));
        }
      });
    });

    req.on("error", reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error("Request timeout"));
    });

    req.write(payload);
    req.end();
  });
}

// Mask API key for display
function maskApiKey(key) {
  if (!key || key.length < 12) return "***";
  return key.substring(0, 10) + "..." + key.substring(key.length - 6);
}

// Commands
const commands = {
  // Send verification code
  async "send-code"(email) {
    if (!email) {
      console.log("Usage: node ad-account-manager.js send-code <email>");
      return { success: false, error: "Email required" };
    }

    console.log(`📧 Sending verification code to ${email}...`);

    try {
      const res = await request("auth/send-code", { email });
      console.log("✅ Verification code sent!");
      console.log("   Check your email and run:");
      console.log(`   node ad-account-manager.js verify ${email} <code>`);
      return { success: true };
    } catch (e) {
      console.log(`❌ Failed: ${e.message}`);
      return { success: false, error: e.message };
    }
  },

  // Verify code and get API key
  async verify(email, code) {
    if (!email || !code) {
      console.log("Usage: node ad-account-manager.js verify <email> <code>");
      return { success: false, error: "Email and code required" };
    }

    console.log(`🔐 Verifying code for ${email}...`);

    try {
      const res = await request("auth/verify", { email, code });

      // Save to config
      const config = loadConfig();
      config.x2cApiKey = res.api_key;
      config.x2cUserId = res.user_id;
      config.x2cEmail = email;
      saveConfig(config);

      // Sync to unified account.json and all skills
      updateAccountAndSync({ apiKey: res.api_key, userId: res.user_id, email });

      console.log("✅ Account verified and bound!");
      console.log(`   API Key: ${maskApiKey(res.api_key)}`);
      console.log(`   User ID: ${res.user_id}`);

      return { success: true, apiKey: res.api_key };
    } catch (e) {
      console.log(`❌ Verification failed: ${e.message}`);
      return { success: false, error: e.message };
    }
  },

  // Check binding status
  async "check-binding"() {
    const config = loadConfig();
    const apiKey = config.x2cApiKey;

    if (!apiKey) {
      console.log("❌ No X2C account bound");
      console.log("");
      console.log("To bind your account:");
      console.log("  1. node ad-account-manager.js send-code your@email.com");
      console.log("  2. Check email for verification code");
      console.log("  3. node ad-account-manager.js verify your@email.com 123456");
      return { bound: false };
    }

    console.log("✅ X2C account is bound");
    console.log(`   Email: ${config.x2cEmail || "N/A"}`);
    console.log(`   API Key: ${maskApiKey(apiKey)}`);
    return { bound: true, apiKey, email: config.x2cEmail };
  },

  // Bind with existing API key (direct)
  async bind(options = {}) {
    const apiKey = options.key;

    if (!apiKey) {
      console.log("");
      console.log("X2C Account Binding");
      console.log("══════════════════════════════════════════════════════════");
      console.log("");
      console.log("Option 1: Email verification (recommended)");
      console.log("  node ad-account-manager.js send-code your@email.com");
      console.log("  node ad-account-manager.js verify your@email.com <code>");
      console.log("");
      console.log("Option 2: Direct API key (if you already have one)");
      console.log('  node ad-account-manager.js bind --key "x2c_sk_xxx"');
      console.log("");
      return { success: false };
    }

    // Validate key format
    if (!apiKey.startsWith("x2c_sk_")) {
      console.log("❌ Invalid API key format");
      console.log('   API key should start with "x2c_sk_"');
      return { success: false, error: "Invalid key format" };
    }

    // Test the key
    console.log("🔐 Validating API key...");
    try {
      await request("config/get-options", {}, apiKey);

      // Save to config
      const config = loadConfig();
      config.x2cApiKey = apiKey;
      saveConfig(config);

      // Sync to unified account.json and all skills
      updateAccountAndSync({ apiKey });

      console.log("✅ Account bound successfully!");
      console.log(`   API Key: ${maskApiKey(apiKey)}`);
      return { success: true };
    } catch (e) {
      console.log(`❌ Invalid API key: ${e.message}`);
      return { success: false, error: e.message };
    }
  },

  // Get configuration (includes pricing info)
  async config() {
    const config = loadConfig();
    const apiKey = config.x2cApiKey;

    if (!apiKey) {
      console.log("❌ No X2C account bound");
      return { error: "Not bound" };
    }

    console.log("📋 Fetching configuration...");

    try {
      const res = await request("config/get-options", {}, apiKey);

      console.log("");
      console.log("Available Options:");
      console.log("══════════════════════════════════════════════════════════");

      console.log("\n📹 Modes:");
      res.modes?.forEach((m) => console.log(`   - ${m}`));

      console.log("\n📐 Ratios:");
      res.ratios?.forEach((r) => console.log(`   - ${r}`));

      console.log("\n⏱️  Durations:");
      res.durations?.forEach((d) => {
        console.log(`   - ${d.label}: ${d.credits} credits ($${d.usd})`);
      });

      console.log("\n📝 Script Pricing:");
      res.script_pricing?.forEach((p) => {
        console.log(`   - ${p.mode}: ${p.credits} credits ($${p.usd})`);
      });

      console.log("\n🎨 Styles:");
      res.styles?.slice(0, 5).forEach((s) => console.log(`   - ${s.name}`));
      if (res.styles?.length > 5) console.log(`   ... and ${res.styles.length - 5} more`);

      return res;
    } catch (e) {
      console.log(`❌ Failed: ${e.message}`);
      return { error: e.message };
    }
  },

  // Unbind account
  async unbind() {
    const config = loadConfig();

    if (!config.x2cApiKey) {
      console.log("❌ No X2C account bound");
      return { success: false };
    }

    delete config.x2cApiKey;
    delete config.x2cUserId;
    delete config.x2cEmail;
    saveConfig(config);

    // Clear unified account.json x2c section and sync
    updateAccountAndSync({ apiKey: "", userId: "", email: "" });

    console.log("✅ X2C account unbound");
    return { success: true };
  },

  // Help
  async help() {
    console.log(`
Ad Account Manager - X2C Account Management

Authentication:
  send-code <email>
      Send verification code to email

  verify <email> <code>
      Verify code and get API key

  bind --key <api_key>
      Bind with existing API key (if you already have one)

Account Management:
  check-binding
      Check if X2C account is bound

  config
      Get available options (styles, durations, pricing)

  unbind
      Remove X2C account binding

  help
      Show this help

Examples:
  # New user registration
  node ad-account-manager.js send-code user@example.com
  node ad-account-manager.js verify user@example.com 123456

  # Check binding
  node ad-account-manager.js check-binding

  # View pricing and options
  node ad-account-manager.js config

  # Unbind
  node ad-account-manager.js unbind

API Key Format: x2c_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
`);
  },
};

// Module exports for programmatic use
module.exports = {
  checkBinding: async () => {
    const config = loadConfig();
    return {
      bound: !!config.x2cApiKey,
      apiKey: config.x2cApiKey || null,
      email: config.x2cEmail || null,
    };
  },

  getApiKey: () => {
    const config = loadConfig();
    return config.x2cApiKey || null;
  },

  request: request,
};

// CLI entry point
if (require.main === module) {
  async function main() {
    const args = process.argv.slice(2);
    const cmd = args[0];

    if (!cmd || !commands[cmd]) {
      await commands.help();
      process.exit(cmd ? 1 : 0);
    }

    // Parse options
    const options = {};
    const positional = [];

    for (let i = 1; i < args.length; i++) {
      if (args[i].startsWith("--")) {
        const key = args[i].slice(2);
        const value = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
        options[key] = value;
      } else {
        positional.push(args[i]);
      }
    }

    try {
      const result = await commands[cmd](...positional, options);
      if (result && result.error) {
        process.exit(1);
      }
    } catch (error) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  }

  main();
}
