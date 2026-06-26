#!/usr/bin/env node
/**
 * claude-session-warmer — align your Claude Pro/Max usage window to your working hours.
 *
 * Claude meters usage in a rolling 5-hour window ANCHORED to your first message of a
 * session. If your first real prompt lands at 09:40, your window is 09:40–14:40 and
 * every reset that day is stuck on that clock. Send a tiny "primer" at 05:00 instead
 * and the window opens 05:00–10:00 — a fresh window is already waiting when you start,
 * and the day's resets line up with your working hours.
 *
 * This runs on your ALWAYS-ON box — the same VPS where you already run OpenClaw and an
 * authenticated Claude Code — and fires the primer through the OFFICIAL `claude` CLI on
 * YOUR subscription. It does not exceed any quota (you can't beat the 5h or weekly cap);
 * it only shifts WHEN the window opens. See references/tos.md for why the official-CLI
 * path is the ToS-sanctioned mechanism (Consumer Terms §3 item-7 automation exemption).
 *
 * Subcommands:
 *   check               Verify the `claude` CLI is installed AND logged in on this box
 *   schedule            Print today's primer times for the current config (no side effects)
 *   warm                Fire ONE primer now via `claude -p` (respects enabled + dry_run)
 *   install [--cron-only]  Print cron / scheduled-task lines (--cron-only = pipeable, no comments)
 *   status              Show config + the next primer time
 *
 * Config: ./config.json (copy from config.example.json). All times in the configured tz.
 */

import { readFileSync, existsSync } from "node:fs";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

// ---------- config ----------
const DEFAULTS = {
  enabled: false, // OFF by default — you must opt in. Honest, conservative default.
  dry_run: false, // when true, `warm` prints what it would do but sends nothing
  timezone: "UTC", // IANA tz used for ALL clock math — set this to YOUR timezone
  anchor: "05:00", // first primer of the day (HH:MM, 24h, in `timezone`)
  day_end: "22:00", // stop priming after this local time
  window_minutes: 300, // Claude's window length (5h). Don't change unless Anthropic does.
  buffer_minutes: 5, // fire this many min AFTER a window closes, so the next message
  // starts a genuinely fresh window rather than counting inside the old one
  prompt: "ping — session warm-up, no action needed", // the trivial primer text
  claude_bin: "claude", // path to the official Claude Code CLI on this box
  claude_args: ["-p"], // print mode: one prompt, one response, non-interactive
};

function loadConfig() {
  const path = join(ROOT, "config.json");
  if (!existsSync(path)) return { ...DEFAULTS, _usingDefaults: true };
  try {
    const user = JSON.parse(readFileSync(path, "utf8"));
    return { ...DEFAULTS, ...user };
  } catch (e) {
    console.error(`! Could not parse config.json: ${e.message}\n  Falling back to defaults.`);
    return { ...DEFAULTS, _usingDefaults: true };
  }
}

// ---------- time helpers (tz-aware via Intl, no deps) ----------
function partsInTz(date, timezone) {
  const fmt = new Intl.DateTimeFormat("en-GB", {
    timeZone: timezone, hour12: false, hour: "2-digit", minute: "2-digit",
  });
  const [h, m] = fmt.format(date).split(":").map(Number);
  return { h, m };
}
function minutesNowInTz(timezone) {
  const { h, m } = partsInTz(new Date(), timezone);
  return h * 60 + m;
}
function hhmmToMinutes(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
}
function minutesToHHMM(mins) {
  const m = ((mins % 1440) + 1440) % 1440;
  return `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
}

// ---------- the schedule ----------
// Primers are spaced (window + buffer) apart, from anchor to day_end. The buffer ensures
// the previous window has fully closed before the next primer, so each primer opens a
// brand-new window instead of landing inside the old one.
function computeSchedule(cfg) {
  const start = hhmmToMinutes(cfg.anchor);
  const end = hhmmToMinutes(cfg.day_end);
  const step = cfg.window_minutes + cfg.buffer_minutes;
  const times = [];
  for (let t = start; t <= end; t += step) times.push(t);
  return times; // minutes-of-day, in cfg.timezone
}
function nextPrimer(cfg) {
  const now = minutesNowInTz(cfg.timezone);
  const upcoming = computeSchedule(cfg).find((t) => t > now);
  if (upcoming != null) return { when: minutesToHHMM(upcoming), day: "today" };
  return { when: cfg.anchor, day: "tomorrow" };
}

// ---------- subcommands ----------
function cmdSchedule(cfg) {
  const times = computeSchedule(cfg).map(minutesToHHMM);
  console.log(`claude-session-warmer — primer schedule (${cfg.timezone})`);
  console.log(`  anchor ${cfg.anchor} · window ${cfg.window_minutes}m · buffer ${cfg.buffer_minutes}m · until ${cfg.day_end}`);
  console.log(`  primers: ${times.join("  ")}`);
  if (cfg._usingDefaults) console.log("  (using built-in defaults — no config.json found; copy config.example.json)");
  if (cfg.timezone === "UTC") console.log("  ⚠ timezone is UTC — set your real IANA timezone in config.json");
  if (!cfg.enabled) console.log("  NOTE: enabled=false — `warm` will NOT send until you set enabled=true");
}

function cmdStatus(cfg) {
  const n = nextPrimer(cfg);
  console.log(`claude-session-warmer status`);
  console.log(`  enabled : ${cfg.enabled}${cfg.dry_run ? "  (dry_run)" : ""}`);
  console.log(`  tz      : ${cfg.timezone}`);
  console.log(`  next    : ${n.when} (${n.day})`);
  console.log(`  cli     : ${cfg.claude_bin} ${cfg.claude_args.join(" ")}`);
}

function cmdInstall(cfg, cronOnly) {
  const times = computeSchedule(cfg);
  const self = join(ROOT, "bin", "session-warmer.mjs");
  const cronLines = times.map((t) => {
    const hh = Math.floor(t / 60), mm = t % 60;
    return `${mm} ${hh} * * *  node ${self} warm >> ${join(ROOT, "warmer.log")} 2>&1`;
  });
  if (cronOnly) {
    // pipeable: just the crontab lines (plus CRON_TZ), nothing else
    console.log(`CRON_TZ=${cfg.timezone}`);
    cronLines.forEach((l) => console.log(l));
    return;
  }
  console.log("# --- Option A: cron on this VPS (recommended) ---");
  console.log("# Open your crontab with:  crontab -e   then paste the block below.");
  console.log("# (CRON_TZ makes the times use YOUR timezone regardless of the server's.)");
  console.log(`CRON_TZ=${cfg.timezone}`);
  cronLines.forEach((l) => console.log(l));
  console.log("");
  console.log("# One-liner to append it automatically (review first!):");
  console.log(`#   ( crontab -l 2>/dev/null; node ${self} install --cron-only ) | crontab -`);
  console.log("");
  console.log("# --- Option B: OpenClaw / Cowork scheduled task ---");
  console.log("# Create one scheduled task per primer time above, each running:");
  console.log(`#   node ${self} warm`);
}

function cmdCheck(cfg) {
  // Verifies the box can actually warm the window: binary present + logged in.
  // This sends ONE tiny real prompt (which also warms the window — harmless/desired).
  console.log("claude-session-warmer check — verifying this box can warm your window…");
  console.log(`  1/2 locating CLI: ${cfg.claude_bin}`);
  execFile(cfg.claude_bin, ["--version"], { timeout: 30000 }, (verr, vout) => {
    if (verr) {
      console.error(`  ✗ '${cfg.claude_bin}' not found or not runnable on this box.`);
      console.error(`    Fix: install the official Claude Code CLI here, or set claude_bin in config.json.`);
      process.exitCode = 1;
      return;
    }
    console.log(`      ✓ found (${(vout || "").trim() || "version ok"})`);
    console.log(`  2/2 testing auth with a one-line prompt…`);
    execFile(cfg.claude_bin, [...cfg.claude_args, "reply with exactly: ok"], { timeout: 120000 }, (aerr, aout, astderr) => {
      if (aerr) {
        const tail = (astderr || aerr.message || "").trim().split("\n").slice(-2).join(" ");
        console.error(`      ✗ the prompt failed: ${tail}`);
        console.error(`    Most likely this box is not logged in. Fix: run \`claude\` once interactively`);
        console.error(`    here and complete the official login, then re-run this check.`);
        process.exitCode = 1;
        return;
      }
      console.log(`      ✓ Claude replied — auth works. This box can warm your window.`);
      console.log(`  Ready. Set enabled=true in config.json, then \`install\` to schedule it.`);
    });
  });
}

function cmdWarm(cfg) {
  const stamp = new Date().toISOString();
  if (!cfg.enabled) {
    console.log(`[${stamp}] skipped — enabled=false (set it true in config.json to arm)`);
    return;
  }
  if (cfg.dry_run) {
    console.log(`[${stamp}] DRY RUN — would send: ${cfg.claude_bin} ${cfg.claude_args.join(" ")} ${JSON.stringify(cfg.prompt)}`);
    return;
  }
  execFile(cfg.claude_bin, [...cfg.claude_args, cfg.prompt], { timeout: 120000 }, (err, stdout, stderr) => {
    if (err) {
      console.error(`[${stamp}] primer FAILED: ${err.message}`);
      if (stderr) console.error(stderr.trim().split("\n").slice(-3).join("\n"));
      console.error(`[${stamp}] hint: run \`node bin/session-warmer.mjs check\` — the box may need re-login.`);
      process.exitCode = 1;
      return;
    }
    const preview = (stdout || "").trim().slice(0, 80).replace(/\s+/g, " ");
    console.log(`[${stamp}] primer sent — session window warmed. reply: "${preview}"`);
  });
}

// ---------- main ----------
const cmd = process.argv[2] || "status";
const flags = process.argv.slice(3);
const cfg = loadConfig();
switch (cmd) {
  case "check": cmdCheck(cfg); break;
  case "schedule": cmdSchedule(cfg); break;
  case "warm": cmdWarm(cfg); break;
  case "install": cmdInstall(cfg, flags.includes("--cron-only")); break;
  case "status": cmdStatus(cfg); break;
  default:
    console.error(`Unknown command: ${cmd}\nUsage: session-warmer.mjs [check|schedule|warm|install|status]`);
    process.exitCode = 2;
}
