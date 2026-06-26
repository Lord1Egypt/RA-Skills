// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/headless-auth.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

/**
 * headless-auth.js — Shared UX helper for RFC 8628 device code flow in
 * headless / remote / no-browser environments.
 *
 * Zero external dependencies. Node builtins only. CommonJS.
 *
 * SSOT — Single Source of Truth.
 * This file lives in sdks/_shared/scripts/ and is automatically synced to
 * sdks/awareness-memory/scripts/ and sdks/claudecode/scripts/ by
 * scripts/sync-shared-scripts.sh. DO NOT edit the copies — edit THIS file.
 *
 * TS variant: sdks/openclaw/src/headless-auth.ts (manually maintained)
 * ESM variant: sdks/setup-cli/src/headless-auth.mjs (manually maintained)
 *
 * See docs/features/f-036/shared-scripts-consolidation.md
 */

const { execSync } = require("child_process");

// ─── Environment detection ───────────────────────────────────────

/**
 * Decide whether the current process is running in a headless environment.
 * See setup-cli/src/headless-auth.mjs for full docs.
 */
function isHeadlessEnv(opts) {
  opts = opts || {};
  const env = opts.env || process.env;
  const platform = opts.platform || process.platform;
  const isTTY = opts.isTTY === undefined
    ? Boolean(process.stdout && process.stdout.isTTY)
    : opts.isTTY;

  const flag = String(env.AWARENESS_HEADLESS || "").toLowerCase();
  if (flag === "1" || flag === "true" || flag === "yes" || flag === "on") return true;
  if (flag === "0" || flag === "false" || flag === "no" || flag === "off") return false;

  if (env.SSH_CONNECTION || env.SSH_CLIENT || env.SSH_TTY) return true;
  if (String(env.CODESPACES || "").toLowerCase() === "true") return true;
  if (env.GITPOD_WORKSPACE_ID) return true;
  if (String(env.CLOUD_SHELL || "").toLowerCase() === "true") return true;

  if (platform === "linux") {
    if (!env.DISPLAY && !env.WAYLAND_DISPLAY) return true;
  }

  if (!isTTY) return true;

  return false;
}

// ─── Browser opener ──────────────────────────────────────────────

function openBrowserSilently(url) {
  try {
    const platform = process.platform;
    if (platform === "darwin") {
      execSync(`open "${url}"`, { stdio: "ignore" });
    } else if (platform === "win32") {
      execSync(`start "" "${url}"`, { stdio: "ignore" });
    } else {
      execSync(`xdg-open "${url}"`, { stdio: "ignore" });
    }
    return true;
  } catch {
    return false;
  }
}

// ─── Box renderer ────────────────────────────────────────────────

function wrap(s, width) {
  const out = [];
  let i = 0;
  while (i < s.length) {
    out.push(s.slice(i, i + width - 3));
    i += width - 3;
  }
  return out.length > 0 ? out : [""];
}

function renderDeviceCodeBox(args) {
  const userCode = args.userCode;
  const verificationUri = args.verificationUri;
  const expiresInSec = args.expiresInSec;
  const headless = !!args.headless;
  const product = args.product || "Awareness";

  const minutes = expiresInSec ? Math.max(1, Math.round(expiresInSec / 60)) : null;
  const ttlLine = minutes
    ? `Code expires in ~${minutes} minute${minutes === 1 ? "" : "s"}.`
    : "";

  const W = 62;
  const pad = (s) => {
    if (s.length >= W) return s.slice(0, W);
    return s + " ".repeat(W - s.length);
  };
  const top = "╔" + "═".repeat(W + 2) + "╗";
  const bot = "╚" + "═".repeat(W + 2) + "╝";
  const mid = (s) => "║ " + pad(s || "") + " ║";

  const lines = [];
  lines.push("");
  lines.push(top);
  lines.push(mid(`${product} Device Authorization`));
  lines.push(mid(""));
  if (headless) {
    lines.push(mid("Headless / remote host detected — no browser will be opened."));
    lines.push(mid(""));
    lines.push(mid("1. Open this URL on any device with a browser"));
    lines.push(mid("   (your phone or laptop works fine):"));
  } else {
    lines.push(mid("1. We tried to open your browser. If nothing happened,"));
    lines.push(mid("   visit this URL manually:"));
  }
  lines.push(mid(""));
  const urlLines = wrap(verificationUri, W);
  for (const line of urlLines) lines.push(mid("   " + line));
  lines.push(mid(""));
  lines.push(mid("2. Sign in (if needed) and enter this code:"));
  lines.push(mid(""));
  lines.push(mid(`       ┌─────────────────┐`));
  lines.push(mid(`       │   ${userCode.padEnd(13)} │`));
  lines.push(mid(`       └─────────────────┘`));
  lines.push(mid(""));
  if (ttlLine) lines.push(mid(ttlLine));
  lines.push(mid("Waiting for approval..."));
  lines.push(bot);
  lines.push("");

  return lines.join("\n");
}

const DEFAULT_POLL_TIMEOUT_SEC = 840;

module.exports = {
  isHeadlessEnv,
  openBrowserSilently,
  renderDeviceCodeBox,
  DEFAULT_POLL_TIMEOUT_SEC,
};
