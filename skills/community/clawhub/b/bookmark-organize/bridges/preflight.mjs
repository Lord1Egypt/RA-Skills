import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { spawn } from "node:child_process";
import { repoRoot } from "./repo-paths.mjs";

const execFileAsync = promisify(execFile);

const BASE_URL = process.env.BOOKMARK_BRIDGE_BASE_URL || "http://127.0.0.1:8787";
const MAX_ATTEMPTS = Number(process.env.BOOKMARK_BRIDGE_PREFLIGHT_ATTEMPTS || 5);
const RETRY_DELAY_MS = Number(process.env.BOOKMARK_BRIDGE_PREFLIGHT_DELAY_MS || 2500);
const REQUEST_TIMEOUT_MS = Number(process.env.BOOKMARK_BRIDGE_REQUEST_TIMEOUT_MS || 5000);

async function main() {
  console.log(`[bridge-preflight] using ${BASE_URL}`);
  console.log(`[bridge-preflight] repo root ${repoRoot}`);

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    console.log(`\n[bridge-preflight] attempt ${attempt}/${MAX_ATTEMPTS}`);

    await ensureBridgeServer();

    const health = await safeRequest("GET", "/health");
    let lastHealth = null;
    if (health.ok) {
      lastHealth = health.data;
      printJson("Health", health.data);
    } else {
      console.log(`[bridge-preflight] health request failed: ${health.error}`);
    }

    const liveContext = await safeRequest("POST", "/context", {
      scope: {
        type: "all",
        label: "All bookmarks"
      }
    });

    if (liveContext.ok) {
      printJson("Context Summary", {
        bookmarkCount: liveContext.data.bookmarks.length,
        folderCount: liveContext.data.folders.length,
        sampleFolders: liveContext.data.folders.slice(0, 5).map((folder) => folder.path.join(" / "))
      });
      console.log("\n[bridge-preflight] bridge and extension are live.");
      return;
    }

    console.log(`[bridge-preflight] live context failed: ${liveContext.error}`);
    printRecoveryHint(lastHealth);
    await attemptChromeReload();

    if (attempt < MAX_ATTEMPTS) {
      await delay(RETRY_DELAY_MS);
    }
  }

  console.log("\n[bridge-preflight] failed to restore a live extension connection.");
  const finalHealth = await safeRequest("GET", "/health");
  if (finalHealth.ok) {
    printFinalRecoveryGuidance(finalHealth.data);
  }
  process.exitCode = 1;
}

function printRecoveryHint(health) {
  const state = classifyExecutorState(health);
  if (state.extensionKnown) {
    console.log("[bridge-preflight] Chrome executor appears installed but is not currently live.");
    console.log("[bridge-preflight] This is usually a sleeping MV3 background worker or a dropped WebSocket, not a first-run install problem.");
    console.log("[bridge-preflight] I will try to wake/reload the existing extension instead of asking to load it again.");
    return;
  }

  console.log("[bridge-preflight] Chrome executor has not checked in yet.");
  console.log("[bridge-preflight] If this is the first run, the user must load the unpacked extension once.");
}

function printFinalRecoveryGuidance(health) {
  const state = classifyExecutorState(health);
  printJson("Recovery Guidance", {
    extensionKnown: state.extensionKnown,
    needsManualInstall: !state.extensionKnown,
    needsExistingExtensionReload: state.extensionKnown,
    extensionVersion: state.extensionVersion,
    lastSeenAt: state.lastSeenAt,
    withinGracePeriod: state.withinGracePeriod,
    message: state.extensionKnown
      ? "The extension was seen before but is not live. Ask the user to reload the existing Bookmark Organize Executor extension card, not to load unpacked again."
      : "The extension has not checked in. Ask the user to load the unpacked Chrome executor extension once."
  });
}

function classifyExecutorState(health) {
  const executor = health?.executor || {};
  const extensionVersion = executor.extensionVersion || null;
  const lastSeenAt = executor.lastSeenAt || null;
  return {
    extensionKnown: Boolean(extensionVersion || lastSeenAt),
    extensionVersion,
    lastSeenAt,
    withinGracePeriod: Boolean(executor.withinGracePeriod)
  };
}

async function attemptChromeReload() {
  console.log("[bridge-preflight] trying to refresh the Chrome extension page.");

  const script = `
    tell application "Google Chrome"
      activate
      open location "chrome://extensions/"
    end tell
    delay 1
    tell application "System Events"
      tell process "Google Chrome"
        set frontmost to true
        repeat with w in windows
          try
            if (name of w) contains "扩展程序 - Google Chrome" then
              perform action "AXRaise" of w
              exit repeat
            end if
          end try
        end repeat
        delay 0.4
        click at {255, 165}
        delay 0.4
        click at {472, 376}
      end tell
    end tell
  `;

  try {
    await execFileAsync("osascript", ["-e", script]);
    console.log("[bridge-preflight] sent update/reload clicks to Chrome.");
  } catch (error) {
    const message = error?.stderr || error?.message || String(error);
    console.log(`[bridge-preflight] Chrome automation failed: ${message.trim()}`);
  }
}

async function ensureBridgeServer() {
  const health = await safeRequest("GET", "/health");
  if (health.ok) {
    return;
  }

  console.log("[bridge-preflight] bridge server is not responding, starting it.");
  const child = spawn("node", ["bridges/local-bridge-server.mjs"], {
    cwd: repoRoot,
    detached: true,
    stdio: "ignore"
  });
  child.unref();
  await delay(1200);
}

async function safeRequest(method, path, body) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      method,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json"
      },
      body: body ? JSON.stringify(body) : undefined
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        ok: false,
        error: data?.error?.message || `HTTP ${response.status}`
      };
    }

    return {
      ok: true,
      data
    };
  } catch (error) {
    return {
      ok: false,
      error: error?.message || String(error)
    };
  } finally {
    clearTimeout(timer);
  }
}

function printJson(title, value) {
  console.log(`\n=== ${title} ===`);
  console.log(JSON.stringify(value, null, 2));
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

main().catch((error) => {
  console.error(`\n[bridge-preflight] ${error.message}`);
  process.exitCode = 1;
});
