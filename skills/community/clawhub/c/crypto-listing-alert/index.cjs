#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");
const http = require("http");
const https = require("https");

const DEFAULT_API_URL = "https://listingalert.org/api";
//const DEFAULT_API_URL = "http://localhost:8004/api"
const CONFIG_DIR = ".exchange-alerts";
const CONFIG_FILE = "config.json";

// --- Main ---

const [cmd, ...args] = process.argv.slice(2);

if (!cmd) {
  printUsage();
  process.exit(1);
}

switch (cmd) {
  case "check-login":
    handleCheckLogin(args);
    break;
  case "login":
    handleLogin(args);
    break;
  case "plans":
    handlePlans(args);
    break;
  case "subscribe":
    handleSubscribe(args);
    break;
  case "pay":
    handlePay(args);
    break;
  case "check-payment":
    handleCheckPayment(args);
    break;
  case "list-orders":
    handleListOrders(args);
    break;
  case "cancel-order":
    handleCancelOrder(args);
    break;
  case "status":
    handleStatus(args);
    break;
  case "unsubscribe":
    handleUnsubscribe(args);
    break;
  case "help":
  case "--help":
  case "-h":
    printUsage();
    break;
  case "version":
  case "--version":
  case "-v":
    console.log("exchange-alerts v0.3.1");
    break;
  default:
    process.stderr.write(`Unknown command: ${cmd}\n`);
    printUsage();
    process.exit(1);
}

// --- Usage ---

function printUsage() {
  console.log(`exchange-alerts - Subscribe to exchange listing alerts

Usage:
  exchange-alerts <command> [options]

Commands:
  check-login      Check whether API key is already saved locally
  login            Save API key to local config
  plans            List available subscription plans
  subscribe        Create a new subscription (DEPRECATED: use 'pay' instead for paid plans)
  pay              Create payment order and get QR code for crypto payment
  check-payment    Check payment status and wait for confirmation
  list-orders      List payment orders (use --status pending to filter)
  cancel-order     Cancel a pending payment order by --order-id
  status           Check current subscription status
  unsubscribe      Cancel current subscription
  help             Show this help
  version          Show version

Options:
  --json           Output in JSON format (recommended for automation)
  --channel        Notification channel: telegram|discord|email (default: telegram)
  --email          Email address (required when --channel email)
  --telegram       Telegram chat ID (required when --channel telegram)
  --discord-channel Discord channel ID (required when --channel discord)
  --bot-token      User bot token (required for telegram/discord)

Examples:
  exchange-alerts check-login --json
  exchange-alerts login --api-key sk-xxxx
  exchange-alerts plans --json
  exchange-alerts list-orders --status pending --json
  exchange-alerts cancel-order --order-id 123 --json
  exchange-alerts pay --plan basic --exchanges binance,okx --channel telegram --telegram 123456789 --bot-token <TOKEN> --json
  exchange-alerts pay --plan basic --exchanges binance,okx --channel discord --discord-channel 123456789012345678 --bot-token <TOKEN> --json
  exchange-alerts pay --plan basic --exchanges binance,okx --channel email --email user@example.com --json
  exchange-alerts check-payment --order-id 123 --json
  exchange-alerts status --json
  exchange-alerts unsubscribe --json`);
}

// --- Login ---

function handleCheckLogin(args) {
  let loggedIn = false;
  let apiURL = null;

  try {
    const cfg = loadConfig();
    if (cfg && typeof cfg.api_key === "string" && cfg.api_key.trim() !== "") {
      loggedIn = true;
      apiURL = cfg.api_url || DEFAULT_API_URL;
    }
  } catch {
    loggedIn = false;
  }

  if (hasFlag(args, "--json")) {
    outputJSON({
      logged_in: loggedIn,
      api_url: apiURL,
      config_path: getConfigPath(),
    });
  } else {
    if (loggedIn) {
      console.log(`Logged in: yes`);
      console.log(`API URL: ${apiURL}`);
      console.log(`Config: ${getConfigPath()}`);
    } else {
      console.log(`Logged in: no`);
      console.log(`Config: ${getConfigPath()}`);
    }
  }
}

function handleLogin(args) {
  const apiKey = getArgValue(args, "--api-key");
  const apiURL = getArgValue(args, "--api-url") || DEFAULT_API_URL;

  if (!apiKey) {
    process.stderr.write("Error: --api-key is required\n");
    process.exit(1);
  }

  const cfg = { api_url: apiURL, api_key: apiKey };

  try {
    saveConfig(cfg);
  } catch (err) {
    outputError(args, "Failed to save config: " + err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    outputJSON({ status: "ok", message: "Login successful. API key saved.", api_url: apiURL });
  } else {
    console.log("Login successful. API key saved.");
    console.log(`API URL: ${apiURL}`);
  }
}

// --- Plans ---

async function handlePlans(args) {
  const cfg = mustLoadConfig(args);
  let body;
  try {
    body = await apiGet(cfg, "/subscriptions/plans");
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    try {
      const resp = JSON.parse(body);
      console.log("Available Plans:");
      console.log("-".repeat(60));
      for (const p of resp.plans || []) {
        const desc = p.description || "";
        console.log(`  [${p.code}] ${p.name} - ${desc}`);
        console.log(`    Price: $${p.price_monthly.toFixed(2)}/month, $${p.price_yearly.toFixed(2)}/year`);
        console.log(`    Exchanges: ${(p.exchanges || []).join(", ")}`);
        console.log(`    Signal Types: ${(p.signal_types || []).join(", ")}`);
        console.log(`    Max Alerts/Day: ${p.max_alerts_per_day}\n`);
      }
    } catch {
      console.log(body);
    }
  }
}

// --- Subscribe ---

async function handleSubscribe(args) {
  const cfg = mustLoadConfig(args);

  const plan = getArgValue(args, "--plan");
  const exchanges = (getArgValue(args, "--exchanges") || "").toLowerCase();
  const channel = (getArgValue(args, "--channel") || "telegram").toLowerCase();
  const email = getArgValue(args, "--email");
  const telegramChatID = getArgValue(args, "--telegram");
  const discordChannelID = getArgValue(args, "--discord-channel");
  const telegramBotToken = getArgValue(args, "--bot-token");
  const discordBotToken = getArgValue(args, "--bot-token");
  const billingCycle = getArgValue(args, "--billing") || "monthly";

  if (!plan || !exchanges) {
    outputError(args, "Missing required flags: --plan, --exchanges");
    process.exit(1);
  }
  if (channel !== "telegram" && channel !== "discord" && channel !== "email") {
    outputError(args, "Invalid --channel. Use telegram, discord or email");
    process.exit(1);
  }
  if ((channel === "telegram" || channel === "discord") && !telegramBotToken) {
    outputError(args, "Missing required flag: --bot-token");
    process.exit(1);
  }
  if (channel === "telegram" && !telegramChatID) {
    outputError(args, "Missing required flag for telegram channel: --telegram");
    process.exit(1);
  }
  if (channel === "discord" && !discordChannelID) {
    outputError(args, "Missing required flag for discord channel: --discord-channel");
    process.exit(1);
  }
  if (channel === "email" && !email) {
    outputError(args, "Missing required flag for email channel: --email");
    process.exit(1);
  }
  if (channel === "email" && !isValidEmail(email)) {
    outputError(args, "Invalid email format for --email");
    process.exit(1);
  }

  const reqBody = {
    plan_code: plan,
    exchanges,
    notify_channel: channel,
    email: channel === "email" ? email : undefined,
    telegram_chat_id: telegramChatID,
    discord_channel_id: discordChannelID,
    billing_cycle: billingCycle,
    telegram_bot_token: channel === "telegram" ? telegramBotToken : undefined,
    discord_bot_token: channel === "discord" ? discordBotToken : undefined,
  };

  let body;
  try {
    body = await apiPost(cfg, "/subscriptions", reqBody);
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    try {
      const resp = JSON.parse(body);
      const s = resp.subscription;
      console.log("Subscription created successfully!");
      console.log(`  Plan: ${s.plan_code}`);
      console.log(`  Status: ${s.status}`);
      console.log(`  Exchanges: ${(s.exchanges || []).join(", ")}`);
      console.log(`  Channel: ${s.notify_channel || "telegram"}`);
      if ((s.notify_channel || "telegram") === "discord") {
        console.log(`  Discord: ${s.discord_channel_id || "-"}`);
      } else if ((s.notify_channel || "telegram") === "email") {
        console.log(`  Email: ${s.email || "-"}`);
      } else {
        console.log(`  Telegram: ${s.telegram_chat_id || "-"}`);
      }
      console.log(`  Expires: ${s.expires_at}`);
    } catch {
      console.log(body);
    }
  }
}

// --- Pay (Create Payment Order) ---

async function handlePay(args) {
  const cfg = mustLoadConfig(args);

  const plan = getArgValue(args, "--plan");
  const exchanges = (getArgValue(args, "--exchanges") || "").toLowerCase();
  const channel = (getArgValue(args, "--channel") || "telegram").toLowerCase();
  const email = getArgValue(args, "--email");
  const telegramChatID = getArgValue(args, "--telegram");
  const discordChannelID = getArgValue(args, "--discord-channel");
  const telegramBotToken = getArgValue(args, "--bot-token");
  const discordBotToken = getArgValue(args, "--bot-token");
  const billingCycle = getArgValue(args, "--billing") || "monthly";

  if (!plan || !exchanges) {
    outputError(args, "Missing required flags: --plan, --exchanges");
    process.exit(1);
  }
  if (channel !== "telegram" && channel !== "discord" && channel !== "email") {
    outputError(args, "Invalid --channel. Use telegram, discord or email");
    process.exit(1);
  }
  if ((channel === "telegram" || channel === "discord") && !telegramBotToken) {
    outputError(args, "Missing required flag: --bot-token");
    process.exit(1);
  }
  if (channel === "telegram" && !telegramChatID) {
    outputError(args, "Missing required flag for telegram channel: --telegram");
    process.exit(1);
  }
  if (channel === "discord" && !discordChannelID) {
    outputError(args, "Missing required flag for discord channel: --discord-channel");
    process.exit(1);
  }
  if (channel === "email" && !email) {
    outputError(args, "Missing required flag for email channel: --email");
    process.exit(1);
  }
  if (channel === "email" && !isValidEmail(email)) {
    outputError(args, "Invalid email format for --email");
    process.exit(1);
  }

  const reqBody = {
    plan_code: plan,
    exchanges,
    notify_channel: channel,
    email: channel === "email" ? email : undefined,
    telegram_chat_id: telegramChatID,
    discord_channel_id: discordChannelID,
    billing_cycle: billingCycle,
    telegram_bot_token: channel === "telegram" ? telegramBotToken : undefined,
    discord_bot_token: channel === "discord" ? discordBotToken : undefined,
  };

  let body;
  try {
    body = await apiPost(cfg, "/payments", reqBody);
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    // Inject qr_url into the response
    try {
      const resp = JSON.parse(body);
      if (resp.order) {
        resp.order.qr_url = `${cfg.api_url}/payments/${resp.order.id}/qr`;
      }
      console.log(JSON.stringify(resp, null, 2));
    } catch {
      console.log(body);
    }
  } else {
    try {
      const resp = JSON.parse(body);
      const order = resp.order;
      const qrUrl = `${cfg.api_url}/payments/${order.id}/qr`;
      console.log("Payment order created successfully!");
      console.log(`  Order ID: ${order.id}`);
      console.log(`  Amount: ${order.amount_usdt} USDT (BEP-20, BSC)`);
      console.log(`  Wallet: ${order.wallet_address}`);
      console.log(`  QR Code: ${qrUrl}`);
      console.log(`  Expires: ${order.expires_at}`);
      console.log(`\n  ⚠️  IMPORTANT: Transfer the EXACT amount shown above.`);
      console.log(`  The system identifies your payment by the unique amount.`);
    } catch {
      console.log(body);
    }
  }
}


// --- Check Payment Status ---

async function handleCheckPayment(args) {
  const cfg = mustLoadConfig(args);

  const orderID = getArgValue(args, "--order-id");
  if (!orderID) {
    outputError(args, "Missing required flag: --order-id");
    process.exit(1);
  }

  const maxWaitSeconds = parseInt(getArgValue(args, "--wait") || "300", 10); // Default 5 min
  const pollInterval = 10000; // 10 seconds
  const startTime = Date.now();

  let body;
  let order;

  while (true) {
    try {
      body = await apiGet(cfg, `/payments/${orderID}`);
      const resp = JSON.parse(body);
      order = resp.order;

      if (order.status === "paid") {
        if (hasFlag(args, "--json")) {
          console.log(body);
        } else {
          console.log("✅ Payment confirmed!");
          console.log(`  Transaction: ${order.tx_hash}`);
          console.log(`  Paid at: ${order.paid_at}`);
          console.log(`  Your subscription is now active.`);
        }
        return;
      }

      if (order.status === "expired") {
        if (hasFlag(args, "--json")) {
          outputJSON({ error: "Payment order expired", order });
        } else {
          console.log("❌ Payment order expired. Please create a new order.");
        }
        process.exit(1);
      }

      // Still pending
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      if (elapsed >= maxWaitSeconds) {
        if (hasFlag(args, "--json")) {
          outputJSON({ status: "timeout", message: "Payment not confirmed within timeout", order });
        } else {
          console.log("⏱️  Timeout: Payment not confirmed yet.");
          console.log(`  Order status: ${order.status}`);
          console.log(`  You can check again later with:`);
          console.log(`  exchange-alerts check-payment --order-id ${orderID} --json`);
        }
        process.exit(0);
      }

      if (!hasFlag(args, "--json")) {
        const remaining = maxWaitSeconds - elapsed;
        process.stdout.write(`\r⏳ Waiting for payment... (${remaining}s remaining)  `);
      }

      await sleep(pollInterval);
    } catch (err) {
      outputError(args, err.message);
      process.exit(1);
    }
  }
}

// --- List Orders ---

async function handleListOrders(args) {
  const cfg = mustLoadConfig(args);

  const status = getArgValue(args, "--status");
  const urlPath = status ? `/payments?status=${encodeURIComponent(status)}` : "/payments";

  let body;
  try {
    body = await apiGet(cfg, urlPath);
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    try {
      const resp = JSON.parse(body);
      const orders = resp.orders || [];
      if (orders.length === 0) {
        console.log("No orders found.");
        return;
      }
      console.log(`Orders (${orders.length}):`);
      console.log("-".repeat(60));
      for (const o of orders) {
        console.log(`  ID: ${o.id}  Plan: ${o.plan_code}  Amount: ${o.amount_usdt} USDT  Status: ${o.status}`);
        console.log(`  Expires: ${o.expires_at}\n`);
      }
    } catch {
      console.log(body);
    }
  }
}

// --- Cancel Order ---

async function handleCancelOrder(args) {
  const cfg = mustLoadConfig(args);

  const orderID = getArgValue(args, "--order-id");
  if (!orderID) {
    outputError(args, "Missing required flag: --order-id");
    process.exit(1);
  }

  let body;
  try {
    body = await apiDelete(cfg, `/payments/${orderID}`);
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    console.log(`Order ${orderID} cancelled successfully.`);
  }
}

// --- Status ---

async function handleStatus(args) {
  const cfg = mustLoadConfig(args);
  let body;
  try {
    body = await apiGet(cfg, "/subscriptions/me");
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    try {
      const resp = JSON.parse(body);
      if (!resp.subscription) {
        console.log("No active subscription.");
        return;
      }
      const s = resp.subscription;
      console.log("Current Subscription:");
      console.log(`  Plan: ${s.plan_code}`);
      console.log(`  Status: ${s.status}`);
      console.log(`  Exchanges: ${(s.exchanges || []).join(", ")}`);
      console.log(`  Channel: ${s.notify_channel || "telegram"}`);
      if ((s.notify_channel || "telegram") === "discord") {
        console.log(`  Discord: ${s.discord_channel_id || "-"}`);
      } else if ((s.notify_channel || "telegram") === "email") {
        console.log(`  Email: ${s.email || "-"}`);
      } else {
        console.log(`  Telegram: ${s.telegram_chat_id || "-"}`);
      }
      console.log(`  Bot Token: configured`);
      console.log(`  Alerts Today: ${s.alerts_sent_today}`);
      console.log(`  Started: ${s.started_at}`);
      console.log(`  Expires: ${s.expires_at}`);
    } catch {
      console.log(body);
    }
  }
}

// --- Unsubscribe ---

async function handleUnsubscribe(args) {
  const cfg = mustLoadConfig(args);
  let body;
  try {
    body = await apiDelete(cfg, "/subscriptions/me");
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }

  if (hasFlag(args, "--json")) {
    console.log(body);
  } else {
    console.log("Subscription cancelled successfully.");
  }
}

// --- HTTP helpers ---

function apiGet(cfg, urlPath) {
  return apiRequest(cfg, "GET", urlPath, null);
}

function apiPost(cfg, urlPath, body) {
  return apiRequest(cfg, "POST", urlPath, body);
}

function apiDelete(cfg, urlPath) {
  return apiRequest(cfg, "DELETE", urlPath, null);
}

function apiRequest(cfg, method, urlPath, body) {
  return new Promise((resolve, reject) => {
    // Ensure api_url ends with / for proper URL joining
    let baseUrl = cfg.api_url;
    if (!baseUrl.endsWith("/")) {
      baseUrl += "/";
    }
    const fullURL = new URL(urlPath.replace(/^\//, ""), baseUrl);
    const mod = fullURL.protocol === "https:" ? https : http;

    const jsonData = body ? JSON.stringify(body) : null;

    const options = {
      method,
      hostname: fullURL.hostname,
      port: fullURL.port,
      path: fullURL.pathname + fullURL.search,
      headers: {
        "Content-Type": "application/json",
      },
      timeout: 15000,
    };

    if (cfg.api_key) {
      options.headers["X-API-Key"] = cfg.api_key;
    }

    if (jsonData) {
      options.headers["Content-Length"] = Buffer.byteLength(jsonData);
    }

    const req = mod.request(options, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const respBody = Buffer.concat(chunks).toString();
        if (res.statusCode >= 400) {
          try {
            const errResp = JSON.parse(respBody);
            if (errResp.error) {
              return reject(new Error(`API error (${res.statusCode}): ${errResp.error}`));
            }
          } catch {}
          return reject(new Error(`API error (${res.statusCode}): ${respBody}`));
        }
        resolve(respBody);
      });
    });

    req.on("error", (err) => reject(new Error("request failed: " + err.message)));
    req.on("timeout", () => {
      req.destroy();
      reject(new Error("request timed out"));
    });

    if (jsonData) {
      req.write(jsonData);
    }
    req.end();
  });
}

// --- Config helpers ---

function getConfigPath() {
  const home = os.homedir();
  return path.join(home, CONFIG_DIR, CONFIG_FILE);
}

function loadConfig() {
  const configPath = getConfigPath();
  let data;
  try {
    data = fs.readFileSync(configPath, "utf-8");
  } catch {
    throw new Error("not logged in. Run: exchange-alerts login --api-key <YOUR_KEY>");
  }
  return JSON.parse(data);
}

function mustLoadConfig(args) {
  try {
    return loadConfig();
  } catch (err) {
    outputError(args, err.message);
    process.exit(1);
  }
}

function saveConfig(cfg) {
  const configPath = getConfigPath();
  const dir = path.dirname(configPath);
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  fs.writeFileSync(configPath, JSON.stringify(cfg, null, 2), { mode: 0o600 });
}

// --- Output helpers ---

function hasFlag(args, flag) {
  return args.includes(flag);
}

function getArgValue(args, flag) {
  const idx = args.indexOf(flag);
  if (idx !== -1 && idx + 1 < args.length) {
    return args[idx + 1];
  }
  return null;
}

function outputJSON(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

function outputError(args, msg) {
  if (hasFlag(args, "--json")) {
    outputJSON({ error: msg });
  } else {
    process.stderr.write(`Error: ${msg}\n`);
  }
}

function isValidEmail(value) {
  if (!value || typeof value !== "string") return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
