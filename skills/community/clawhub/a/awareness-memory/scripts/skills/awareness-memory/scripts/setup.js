#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/setup.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// One-click setup: browser login → auto API key → select memory → write config
// Zero external dependencies — uses only Node.js builtins.
//
// Usage: node setup.js
//        node setup.js --logout
//        node setup.js --status
// ---------------------------------------------------------------------------

const fs = require("fs");
const https = require("https");
const http = require("http");
const os = require("os");
const path = require("path");
const { execSync } = require("child_process");
const readline = require("readline");

const {
  isHeadlessEnv,
  openBrowserSilently,
  renderDeviceCodeBox,
  DEFAULT_POLL_TIMEOUT_SEC,
} = require("./headless-auth.js");

const API_BASE = process.env.AWARENESS_BASE_URL || "https://awareness.market/api/v1";
const CREDS_DIR = path.join(os.homedir(), ".awareness");
const CREDS_FILE = path.join(CREDS_DIR, "credentials.json");

// ---------------------------------------------------------------------------
// HTTP helper (zero deps)
// ---------------------------------------------------------------------------

function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const mod = parsed.protocol === "https:" ? https : http;
    const body = options.body ? JSON.stringify(options.body) : undefined;
    const req = mod.request(parsed, {
      method: options.method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
        ...(body ? { "Content-Length": Buffer.byteLength(body) } : {}),
      },
      timeout: options.timeout || 15000,
    }, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, data: {} }); }
      });
    });
    req.on("error", reject);
    req.on("timeout", () => { req.destroy(); reject(new Error("Request timed out")); });
    if (body) req.write(body);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Browser opener (delegated to shared headless-auth helper)
// ---------------------------------------------------------------------------

function openBrowser(url) {
  return openBrowserSilently(url);
}

// ---------------------------------------------------------------------------
// Credentials
// ---------------------------------------------------------------------------

function saveCreds(apiKey, memoryId, apiBase = API_BASE) {
  if (!fs.existsSync(CREDS_DIR)) fs.mkdirSync(CREDS_DIR, { recursive: true, mode: 0o700 });
  const data = JSON.stringify({ api_key: apiKey, memory_id: memoryId, api_base: apiBase }, null, 2) + "\n";
  fs.writeFileSync(CREDS_FILE, data, { mode: 0o600 });
}

function loadCreds() {
  try {
    if (!fs.existsSync(CREDS_FILE)) return null;
    const raw = JSON.parse(fs.readFileSync(CREDS_FILE, "utf-8"));
    return raw.api_key ? raw : null;
  } catch { return null; }
}

// ---------------------------------------------------------------------------
// Interactive prompt
// ---------------------------------------------------------------------------

function ask(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => { rl.close(); resolve(answer.trim()); });
  });
}

// ---------------------------------------------------------------------------
// Write environment variables to shell profile
// ---------------------------------------------------------------------------

function writeEnvToProfile(apiKey, memoryId) {
  const shell = process.env.SHELL || "";
  const home = os.homedir();

  // Determine profile file
  let profilePath;
  if (shell.includes("zsh")) profilePath = path.join(home, ".zshrc");
  else if (shell.includes("bash")) profilePath = path.join(home, ".bashrc");
  else if (process.platform === "win32") profilePath = null; // Windows uses different mechanism
  else profilePath = path.join(home, ".profile");

  const envBlock = [
    "",
    "# Awareness Cloud Memory",
    `export AWARENESS_API_KEY="${apiKey}"`,
    `export AWARENESS_MEMORY_ID="${memoryId}"`,
    "",
  ].join("\n");

  if (profilePath) {
    try {
      // Check if already configured
      const existing = fs.existsSync(profilePath) ? fs.readFileSync(profilePath, "utf-8") : "";
      if (existing.includes("AWARENESS_API_KEY")) {
        // Replace existing block
        const updated = existing.replace(
          /# Awareness Cloud Memory\nexport AWARENESS_API_KEY="[^"]*"\nexport AWARENESS_MEMORY_ID="[^"]*"/,
          `# Awareness Cloud Memory\nexport AWARENESS_API_KEY="${apiKey}"\nexport AWARENESS_MEMORY_ID="${memoryId}"`
        );
        if (updated !== existing) {
          fs.writeFileSync(profilePath, updated);
          console.log(`  Updated ${profilePath}`);
        } else {
          // Couldn't find exact pattern, append
          fs.appendFileSync(profilePath, envBlock);
          console.log(`  Appended to ${profilePath}`);
        }
      } else {
        fs.appendFileSync(profilePath, envBlock);
        console.log(`  Written to ${profilePath}`);
      }
      return profilePath;
    } catch (e) {
      console.log(`  Could not write to ${profilePath}: ${e.message}`);
    }
  }

  // Windows: show manual instructions
  if (process.platform === "win32") {
    console.log("\n  On Windows, set these environment variables:");
    console.log(`    setx AWARENESS_API_KEY "${apiKey}"`);
    console.log(`    setx AWARENESS_MEMORY_ID "${memoryId}"`);
    console.log("  Or add them in System Properties > Environment Variables.\n");
  }

  return null;
}

// ---------------------------------------------------------------------------
// Main setup flow
// ---------------------------------------------------------------------------

async function main() {
  const args = process.argv.slice(2);

  // --status: show current config
  if (args.includes("--status")) {
    const creds = loadCreds();
    if (creds) {
      console.log(`Logged in: ${creds.api_key.slice(0, 10)}...`);
      if (creds.memory_id) console.log(`Memory: ${creds.memory_id}`);
      console.log(`API: ${creds.api_base || API_BASE}`);
    } else {
      console.log("Not configured. Run: node setup.js");
    }
    const envKey = process.env.AWARENESS_API_KEY;
    const envMem = process.env.AWARENESS_MEMORY_ID;
    if (envKey) console.log(`Env AWARENESS_API_KEY: ${envKey.slice(0, 10)}...`);
    if (envMem) console.log(`Env AWARENESS_MEMORY_ID: ${envMem}`);
    return;
  }

  // --logout: clear credentials
  if (args.includes("--logout")) {
    try { if (fs.existsSync(CREDS_FILE)) fs.unlinkSync(CREDS_FILE); } catch {}
    console.log("Logged out. Credentials cleared.");
    return;
  }

  console.log("\n  Awareness Cloud Memory — Setup\n");

  // Step 1: Check existing credentials
  const existing = loadCreds();
  if (existing) {
    console.log(`  Already configured (key: ${existing.api_key.slice(0, 10)}...)`);
    const redo = await ask("  Reconfigure? (y/N): ");
    if (redo.toLowerCase() !== "y") {
      console.log("  Setup complete. Your memory is ready.\n");
      return;
    }
  }

  // Step 2: Device code authentication
  console.log("  Authenticating with Awareness...\n");

  let authData;
  try {
    const { status, data } = await request(`${API_BASE}/auth/device/init`, {
      method: "POST", body: {},
    });
    if (status !== 200 || !data.device_code) throw new Error(data.detail || "Init failed");
    authData = data;
  } catch (e) {
    console.error(`  Auth failed: ${e.message}`);
    console.log("\n  Manual setup: set AWARENESS_API_KEY and AWARENESS_MEMORY_ID environment variables.");
    console.log("  Get your credentials at https://awareness.market\n");
    process.exit(1);
  }

  const verifyUrl = `${authData.verification_uri || "https://awareness.market/cli-auth"}?code=${encodeURIComponent(authData.user_code)}`;

  // Headless-aware UX: on SSH/Docker/Codespaces/no-TTY hosts, skip the
  // browser attempt and just show a prominent box with the URL + code.
  const headless = isHeadlessEnv();
  let opened = false;
  if (!headless) {
    opened = openBrowser(verifyUrl);
  }

  console.log(renderDeviceCodeBox({
    userCode: authData.user_code,
    verificationUri: verifyUrl,
    expiresInSec: authData.expires_in || 900,
    headless: headless || !opened,
  }));

  // Poll for approval — align with backend Redis TTL (900s).
  const pollTimeout = authData.expires_in || DEFAULT_POLL_TIMEOUT_SEC;
  const deadline = Date.now() + pollTimeout * 1000;
  let apiKey = null;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, (authData.interval || 5) * 1000));
    try {
      const { data } = await request(`${API_BASE}/auth/device/poll`, {
        method: "POST", body: { device_code: authData.device_code },
      });
      if (data.status === "approved" && data.api_key) {
        apiKey = data.api_key;
        break;
      }
      if (data.status === "expired") { console.error("  Code expired. Run setup again."); process.exit(1); }
      process.stdout.write(".");
    } catch { process.stdout.write("."); }
  }

  if (!apiKey) { console.error("\n  Authorization timed out. Run setup again."); process.exit(1); }

  console.log("\n  Authorized!\n");

  // Step 3: Select or create memory
  let memoryId, memoryName;

  try {
    const { status, data } = await request(`${API_BASE}/memories`, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    const memories = Array.isArray(data) ? data : data.items || data.memories || [];

    if (memories.length === 0) {
      console.log("  No memories found. Creating one...\n");
      const desc = await ask("  What is this memory for? (e.g., 'my coding projects'): ") || "General development workflow";

      const { data: wizData } = await request(`${API_BASE}/wizard/memory_designer`, {
        method: "POST",
        headers: { Authorization: `Bearer ${apiKey}` },
        body: { owner_id: "", locale: "en", messages: [{ role: "user", content: desc }], draft: {} },
        timeout: 30000,
      });

      if (wizData.plan?.create_payload) {
        const { data: mem } = await request(`${API_BASE}/memories`, {
          method: "POST",
          headers: { Authorization: `Bearer ${apiKey}` },
          body: wizData.plan.create_payload,
        });
        memoryId = mem.id;
        memoryName = mem.name || wizData.plan.name || "New Memory";
        console.log(`  Created: ${memoryName}\n`);
      }
    } else {
      console.log("  Your memories:");
      memories.forEach((m, i) => console.log(`    ${i + 1}. ${m.name || "Unnamed"} (${m.id})`));
      console.log(`    ${memories.length + 1}. Create new memory`);
      const choice = await ask(`\n  Select (1-${memories.length + 1}) [1]: `) || "1";
      const num = Number(choice);

      if (num === memories.length + 1) {
        // Create new
        const desc = await ask("  Describe this memory: ") || "General development workflow";
        const { data: wizData } = await request(`${API_BASE}/wizard/memory_designer`, {
          method: "POST",
          headers: { Authorization: `Bearer ${apiKey}` },
          body: { owner_id: "", locale: "en", messages: [{ role: "user", content: desc }], draft: {} },
          timeout: 30000,
        });
        if (wizData.plan?.create_payload) {
          const { data: mem } = await request(`${API_BASE}/memories`, {
            method: "POST",
            headers: { Authorization: `Bearer ${apiKey}` },
            body: wizData.plan.create_payload,
          });
          memoryId = mem.id;
          memoryName = mem.name || "New Memory";
          console.log(`  Created: ${memoryName}\n`);
        }
      } else {
        const idx = Math.max(0, Math.min(num - 1, memories.length - 1));
        memoryId = memories[idx].id;
        memoryName = memories[idx].name || "Unnamed";
      }
    }
  } catch (e) {
    console.error(`  Memory selection failed: ${e.message}`);
    memoryId = await ask("  Enter your Memory ID manually: ");
    memoryName = "Manual";
  }

  if (!memoryId) { console.error("  No memory selected. Run setup again."); process.exit(1); }

  // Step 4: Save credentials + write env vars
  console.log(`  Selected memory: ${memoryName} (${memoryId})\n`);
  console.log("  Saving configuration...");

  saveCreds(apiKey, memoryId, API_BASE);
  console.log(`  Saved to ${CREDS_FILE}`);

  writeEnvToProfile(apiKey, memoryId);

  // Step 5: Set env vars for current session
  process.env.AWARENESS_API_KEY = apiKey;
  process.env.AWARENESS_MEMORY_ID = memoryId;

  console.log("\n  Setup complete!\n");
  console.log("  Your memory is now active. The skill will automatically:");
  console.log("    - Load relevant context before each request");
  console.log("    - Save summaries after each session\n");

  // Show key info (masked)
  console.log(`  API Key:   ${apiKey.slice(0, 10)}...`);
  console.log(`  Memory:    ${memoryName} (${memoryId})`);
  console.log(`  Dashboard: https://awareness.market\n`);

  // Hint to restart shell
  console.log("  Note: Restart your terminal or run 'source ~/.bashrc' to activate env vars.\n");
}

main().catch((e) => { console.error(`Setup failed: ${e.message}`); process.exit(1); });
