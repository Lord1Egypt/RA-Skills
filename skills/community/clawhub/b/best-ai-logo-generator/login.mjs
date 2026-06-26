#!/usr/bin/env node
/**
 * AI Logo Generator — CLI Login
 * Opens browser OAuth flow and saves token to ~/.config/ailogogenerator.online/auth.json
 * Zero external dependencies — uses only Node.js built-ins.
 */

import http from "http";
import fs from "fs";
import path from "path";
import os from "os";
import { execSync, spawn } from "child_process";

const CONFIG_DIR = path.join(os.homedir(), ".config", "ailogogenerator.online");
const AUTH_FILE = path.join(CONFIG_DIR, "auth.json");
const CALLBACK_PORT = 19876;
const CALLBACK_HOST = "127.0.0.1";
const CALLBACK_URL = `http://${CALLBACK_HOST}:${CALLBACK_PORT}/callback`;
const LOGIN_URL = `https://ailogogenerator.online/login?cli_redirect=${encodeURIComponent(CALLBACK_URL)}`;
const TIMEOUT_MS = 120_000;

// ── helpers ──────────────────────────────────────────────────────────────────

function readAuth() {
  try {
    const raw = fs.readFileSync(AUTH_FILE, "utf8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function saveAuth(token, email) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  const data = {
    token,
    email: email || "",
    loginAt: new Date().toISOString(),
  };
  fs.writeFileSync(AUTH_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
  return data;
}

function openBrowser(url) {
  const platform = process.platform;
  try {
    if (platform === "darwin") {
      execSync(`open "${url}"`, { stdio: "ignore" });
    } else if (platform === "win32") {
      // Windows: start command needs cmd /c
      spawn("cmd", ["/c", "start", "", url], { detached: true, stdio: "ignore" }).unref();
    } else {
      // Linux / other Unix
      spawn("xdg-open", [url], { detached: true, stdio: "ignore" }).unref();
    }
  } catch {
    // Silently ignore — we already printed the URL below
  }
}

function parseQuery(queryString) {
  const params = {};
  if (!queryString) return params;
  for (const part of queryString.split("&")) {
    const [k, v] = part.split("=");
    if (k) params[decodeURIComponent(k)] = v ? decodeURIComponent(v) : "";
  }
  return params;
}

const SUCCESS_HTML = (email) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Login successful — AI Logo Generator</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d0e14;
    color: #f0f0f5;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }
  .card {
    text-align: center;
    padding: 2.5rem 3rem;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 1rem;
    background: rgba(255,255,255,0.03);
    max-width: 420px;
    width: 90%;
  }
  .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  h1 {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
  }
  p {
    color: rgba(240,240,245,0.55);
    font-size: 0.9rem;
    line-height: 1.6;
  }
  .email {
    color: #a78bfa;
    font-weight: 500;
  }
  .hint {
    margin-top: 1.5rem;
    font-size: 0.8rem;
    color: rgba(240,240,245,0.3);
  }
</style>
</head>
<body>
<div class="card">
  <div class="icon">&#10003;</div>
  <h1>Login successful</h1>
  <p>You're now authenticated${email ? ` as <span class="email">${email}</span>` : ""}.<br>You can close this tab and return to your terminal.</p>
  <p class="hint">Token saved to ~/.config/ailogogenerator.online/auth.json</p>
</div>
</body>
</html>`;

const ERROR_HTML = (msg) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Login failed — AI Logo Generator</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d0e14;
    color: #f0f0f5;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }
  .card {
    text-align: center;
    padding: 2.5rem 3rem;
    border: 1px solid rgba(255,80,80,0.2);
    border-radius: 1rem;
    background: rgba(255,80,80,0.05);
    max-width: 420px;
    width: 90%;
  }
  h1 { font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem; color: #f87171; }
  p { color: rgba(240,240,245,0.55); font-size: 0.9rem; }
</style>
</head>
<body>
<div class="card">
  <h1>Login failed</h1>
  <p>${msg || "No token received. Please try again."}</p>
</div>
</body>
</html>`;

// ── main ──────────────────────────────────────────────────────────────────────

// Check if already logged in
const existing = readAuth();
if (existing && existing.token) {
  const who = existing.email ? ` (${existing.email})` : "";
  console.log(`Already logged in${who}. Token stored at:\n  ${AUTH_FILE}`);
  console.log("To re-login, delete that file and run this script again.");
  process.exit(0);
}

console.log("Opening browser for login...");
console.log(`If your browser doesn't open automatically, visit:\n  ${LOGIN_URL}\n`);

let server;
let timeoutHandle;

const cleanup = () => {
  if (timeoutHandle) clearTimeout(timeoutHandle);
  if (server && server.listening) {
    server.close();
  }
};

server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${CALLBACK_HOST}`);

  if (url.pathname !== "/callback") {
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  const params = parseQuery(url.search.slice(1));
  const token = params.token;
  const email = params.email || "";

  if (!token) {
    res.writeHead(400, { "Content-Type": "text/html; charset=utf-8" });
    res.end(ERROR_HTML("No token received from the server."));
    cleanup();
    console.error("Login failed: no token in callback.");
    process.exit(1);
    return;
  }

  const authData = saveAuth(token, email);

  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(SUCCESS_HTML(email));

  cleanup();

  const who = authData.email ? ` as ${authData.email}` : "";
  console.log(`\nLogin successful${who}.`);
  console.log(`Token saved to:\n  ${AUTH_FILE}`);
  process.exit(0);
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(
      `Port ${CALLBACK_PORT} is already in use.\n` +
      `Another login process may be running, or a previous one didn't clean up.\n` +
      `Try: kill $(lsof -ti:${CALLBACK_PORT}) and run again.`
    );
  } else {
    console.error("Server error:", err.message);
  }
  process.exit(1);
});

server.listen(CALLBACK_PORT, CALLBACK_HOST, () => {
  openBrowser(LOGIN_URL);

  timeoutHandle = setTimeout(() => {
    console.error(`\nTimeout: no login received within ${TIMEOUT_MS / 1000}s.`);
    cleanup();
    process.exit(1);
  }, TIMEOUT_MS);
});
