#!/usr/bin/env node
/**
 * claude-usage-companion — keep your Claude usage on a VPS healthy after the
 * June 2026 split of programmatic usage into a separate monthly credit pool.
 *
 * Two clean, ToS-safe jobs (no automation of the model, no limit circumvention):
 *   A) MONITOR the programmatic credit pool — month-to-date burn, projection to
 *      month end, and an alert when you're on track to run dry.
 *   B) REMIND you (a human) at your anchor time to start your interactive
 *      session, so your 5-hour window aligns to your day.
 *
 * Usage data comes from `ccusage` (local parse of ~/.claude, no model calls,
 * no window side effects). Cost is USD at API rates — the same basis as the
 * programmatic credit pool.
 *
 * Commands:
 *   check     verify node + ccusage are available and config is valid
 *   report    print month-to-date burn, projection, top models (no side effects)
 *   guard     evaluate thresholds and alert if over (this is what cron runs)
 *   remind    emit the anchor-time "start your session" nudge (cron runs this)
 *   status    show config + the next scheduled actions
 *   install   print a ready-to-paste cron block
 *
 * Node 18+. The only external tool is `ccusage` (configurable).
 */
import { spawnSync } from "node:child_process";
import { readFileSync, existsSync, appendFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const CONFIG_PATH = join(ROOT, "config.json");
const LOG_PATH = join(ROOT, "companion.log");

const PLAN_CREDITS = { pro: 20, max5x: 100, max20x: 200 };

const DEFAULTS = {
  timezone: "UTC",
  plan: "max5x",                 // pro | max5x | max20x — sets the default cap
  monthly_credit_usd: null,      // override the plan cap if your number differs
  warn_pct: 80,
  critical_pct: 95,
  reminder_enabled: true,
  anchor: "08:00",               // local time you start work
  reminder_text: "Your Claude 5-hour interactive window resets to your day when you send your first prompt. Open Claude Code / Cowork and send one now to align it.",
  alert_command: null,           // shell command; receives the message on stdin. null = print to stdout
  ccusage_cmd: ["npx", "-y", "ccusage@latest"],
  currency_symbol: "$",
};

// ---------- config ----------
function loadConfig() {
  let cfg = { ...DEFAULTS };
  if (existsSync(CONFIG_PATH)) {
    try { cfg = { ...cfg, ...JSON.parse(readFileSync(CONFIG_PATH, "utf8")) }; }
    catch (e) { console.error(`! Could not parse config.json: ${e.message}\n  Using defaults.`); cfg._broken = true; }
  } else { cfg._usingDefaults = true; }
  cfg.cap = cfg.monthly_credit_usd ?? PLAN_CREDITS[cfg.plan] ?? 100;
  return cfg;
}

// ---------- timezone-aware date helpers ----------
function tzParts(tz, d = new Date()) {
  const f = new Intl.DateTimeFormat("en-CA", {
    timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", hour12: false,
  });
  const p = Object.fromEntries(f.formatToParts(d).map(o => [o.type, o.value]));
  return { y: +p.year, m: +p.month, d: +p.day, hh: +p.hour, mm: +p.minute };
}
const pad = n => String(n).padStart(2, "0");
const daysInMonth = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate(); // m is 1-based

// ---------- ccusage ----------
function runCcusage(cfg, args) {
  const [bin, ...base] = cfg.ccusage_cmd;
  const r = spawnSync(bin, [...base, ...args], { encoding: "utf8", timeout: 120000 });
  return r;
}

function collectClaudeBurn(cfg) {
  const now = tzParts(cfg.timezone);
  const since = `${now.y}${pad(now.m)}01`;
  const r = runCcusage(cfg, ["daily", "--json", "--since", since]);
  if (r.status !== 0 || !r.stdout) {
    throw new Error(`ccusage failed: ${(r.stderr || r.error?.message || "no output").toString().trim().slice(0, 200)}`);
  }
  const data = JSON.parse(r.stdout);
  const rows = data.daily || [];
  const monthPrefix = `${now.y}-${pad(now.m)}`;
  let mtd = 0;
  const perDay = [];
  const modelTotals = {};
  for (const row of rows) {
    if (!String(row.period).startsWith(monthPrefix)) continue;
    let dayClaude = 0;
    for (const mb of row.modelBreakdowns || []) {
      const name = String(mb.modelName || "");
      if (/^claude/i.test(name)) {              // Anthropic models only (exclude "[openclaw] ...")
        dayClaude += mb.cost || 0;
        modelTotals[name] = (modelTotals[name] || 0) + (mb.cost || 0);
      }
    }
    mtd += dayClaude;
    perDay.push({ date: row.period, cost: dayClaude });
  }
  const dim = daysInMonth(now.y, now.m);
  const dayOfMonth = now.d;
  const avgDaily = dayOfMonth > 0 ? mtd / dayOfMonth : 0;
  const projected = avgDaily * dim;
  return { now, mtd, avgDaily, projected, dim, dayOfMonth, daysLeft: dim - dayOfMonth, perDay, modelTotals };
}

function fmt(cfg, n) { return `${cfg.currency_symbol}${n.toFixed(2)}`; }
function bar(pct, width = 30) {
  const f = Math.max(0, Math.min(width, Math.round(pct / 100 * width)));
  return "█".repeat(f) + " ".repeat(width - f);
}

// ---------- commands ----------
function cmdReport(cfg) {
  const b = collectClaudeBurn(cfg);
  const pct = cfg.cap ? (b.mtd / cfg.cap) * 100 : 0;
  const projPct = cfg.cap ? (b.projected / cfg.cap) * 100 : 0;
  console.log(`claude-usage-companion — programmatic credit pool (${cfg.timezone})`);
  console.log(`  month ${b.now.y}-${pad(b.now.m)} · day ${b.dayOfMonth}/${b.dim} · cap ${fmt(cfg, cfg.cap)} (${cfg.monthly_credit_usd != null ? "custom" : cfg.plan})`);
  console.log("");
  console.log(`  spent so far   ${bar(pct)}  ${pct.toFixed(0)}%   ${fmt(cfg, b.mtd)}`);
  console.log(`  projected EOM  ${bar(projPct)}  ${projPct.toFixed(0)}%   ${fmt(cfg, b.projected)}`);
  console.log("");
  console.log(`  avg/day ${fmt(cfg, b.avgDaily)} · ${b.daysLeft} days left`);
  const verdict = projPct >= cfg.critical_pct ? "⛔ on track to run dry — slow automated jobs or raise credits"
    : projPct >= cfg.warn_pct ? "⚠ trending high — keep an eye on it"
    : "✓ comfortably within budget";
  console.log(`  outlook: ${verdict}`);
  const models = Object.entries(b.modelTotals).sort((a, c) => c[1] - a[1]).slice(0, 5);
  if (models.length) {
    console.log("\n  top models this month:");
    for (const [m, c] of models) console.log(`    ${fmt(cfg, c).padStart(9)}  ${m}`);
  }
  console.log("\n  (Cost = API-rate spend on Anthropic models, from ccusage. On an always-on");
  console.log("   automation box this ≈ your programmatic credit-pool burn. For the exact");
  console.log("   remaining balance, see the 'Usage credits' line in `/usage` inside Claude Code.)");
  return { b, pct, projPct };
}

function deliver(cfg, message) {
  const stamp = new Date().toISOString();
  const line = `[${stamp}] ${message.replace(/\n/g, " ")}`;
  try { appendFileSync(LOG_PATH, line + "\n"); } catch {}
  if (cfg.alert_command) {
    const r = spawnSync(cfg.alert_command, { shell: true, input: message, encoding: "utf8", timeout: 30000 });
    if (r.status !== 0) console.error(`! alert_command exited ${r.status}: ${(r.stderr || "").trim().slice(0, 200)}`);
  } else {
    console.log(message);
  }
}

function cmdGuard(cfg, { verbose }) {
  let r;
  try { r = collectClaudeBurn(cfg); }
  catch (e) {
    deliver(cfg, `claude-usage-companion: could not read usage — ${e.message}. Run \`check\`.`);
    process.exit(1);
  }
  const pct = cfg.cap ? (r.mtd / cfg.cap) * 100 : 0;
  const projPct = cfg.cap ? (r.projected / cfg.cap) * 100 : 0;
  const head = `Claude credit pool: ${fmt(cfg, r.mtd)} of ${fmt(cfg, cfg.cap)} (${pct.toFixed(0)}%) spent, projected ${fmt(cfg, r.projected)} (${projPct.toFixed(0)}%) by month end. ${r.daysLeft} days left.`;
  if (pct >= cfg.critical_pct || projPct >= 100) {
    deliver(cfg, `⛔ CRITICAL — ${head} Automations will stop when the pool is exhausted (no rollover). Slow non-interactive jobs or add usage credits.`);
  } else if (pct >= cfg.warn_pct || projPct >= cfg.warn_pct) {
    deliver(cfg, `⚠ WARNING — ${head}`);
  } else if (verbose) {
    deliver(cfg, `✓ OK — ${head}`);
  }
}

function cmdRemind(cfg) {
  if (!cfg.reminder_enabled) { console.log("reminder disabled (reminder_enabled=false)"); return; }
  let credit = "";
  try {
    const r = collectClaudeBurn(cfg);
    const pct = cfg.cap ? (r.mtd / cfg.cap) * 100 : 0;
    credit = ` (credit pool ${pct.toFixed(0)}% used this month)`;
  } catch {}
  deliver(cfg, `⏰ ${cfg.reminder_text}${credit}`);
}

function nextAnchor(cfg) {
  const [h, m] = cfg.anchor.split(":").map(Number);
  const now = tzParts(cfg.timezone);
  const nowMin = now.hh * 60 + now.mm, anchorMin = h * 60 + m;
  return anchorMin > nowMin ? `${cfg.anchor} (today)` : `${cfg.anchor} (tomorrow)`;
}

function cmdStatus(cfg) {
  console.log("claude-usage-companion status");
  console.log(`  timezone : ${cfg.timezone}`);
  console.log(`  cap      : ${fmt(cfg, cfg.cap)} (${cfg.monthly_credit_usd != null ? "custom monthly_credit_usd" : "plan " + cfg.plan})`);
  console.log(`  thresholds: warn ${cfg.warn_pct}% · critical ${cfg.critical_pct}%`);
  console.log(`  reminder : ${cfg.reminder_enabled ? "on, next at " + nextAnchor(cfg) : "off"}`);
  console.log(`  alerts   : ${cfg.alert_command ? "via alert_command" : "stdout + companion.log"}`);
  console.log(`  ccusage  : ${cfg.ccusage_cmd.join(" ")}`);
  if (cfg._usingDefaults) console.log("  NOTE: no config.json — copy config.example.json and set your timezone/plan.");
  if (cfg.timezone === "UTC") console.log("  ⚠ timezone is UTC — set your real IANA timezone in config.json");
}

function cmdCheck(cfg) {
  console.log("claude-usage-companion check");
  console.log(`  node ${process.version} ✓`);
  process.stdout.write(`  ccusage (${cfg.ccusage_cmd.join(" ")}) … `);
  const r = runCcusage(cfg, ["--version"]);
  if (r.status !== 0) {
    console.log("✗");
    console.error("    Could not run ccusage. Install it (fast path): npm i -g ccusage");
    console.error("    then set \"ccusage_cmd\": [\"ccusage\"] in config.json. Or keep the npx default.");
    process.exit(1);
  }
  console.log(`✓ (${(r.stdout || "").trim()})`);
  process.stdout.write("  reading usage data … ");
  try { const b = collectClaudeBurn(cfg); console.log(`✓ ${b.perDay.length} day(s) this month, ${fmt(cfg, b.mtd)} so far`); }
  catch (e) { console.log("✗"); console.error(`    ${e.message}`); process.exit(1); }
  console.log(`  cap ${fmt(cfg, cfg.cap)} · tz ${cfg.timezone} ✓`);
  console.log("  Ready. Try `report`, then `install` to schedule guard + remind.");
}

function cmdInstall(cfg) {
  const self = join(ROOT, "bin", "usage-companion.mjs");
  const [ah, am] = cfg.anchor.split(":").map(Number);
  const log = `>> ${LOG_PATH} 2>&1`;
  const lines = [
    `CRON_TZ=${cfg.timezone}`,
    `# monitor the programmatic credit pool 3x/day`,
    `0 9,14,19 * * *  node ${self} guard ${log}`,
    `# remind you to start your interactive session at your anchor time`,
    `${am} ${ah} * * *  node ${self} remind ${log}`,
  ];
  console.log("# claude-usage-companion — paste into `crontab -e`");
  console.log("# (CRON_TZ pins these to YOUR timezone regardless of the server's.)");
  lines.forEach(l => console.log(l));
  console.log("");
  console.log("# one-liner to append (review first):");
  console.log(`#   ( crontab -l 2>/dev/null; node ${self} install --cron-only ) | crontab -`);
}
function cmdInstallCronOnly(cfg) {
  const self = join(ROOT, "bin", "usage-companion.mjs");
  const [ah, am] = cfg.anchor.split(":").map(Number);
  const log = `>> ${LOG_PATH} 2>&1`;
  console.log(`CRON_TZ=${cfg.timezone}`);
  console.log(`0 9,14,19 * * *  node ${self} guard ${log}`);
  console.log(`${am} ${ah} * * *  node ${self} remind ${log}`);
}

// ---------- main ----------
const cmd = process.argv[2];
const flags = new Set(process.argv.slice(3));
const cfg = loadConfig();
try {
  switch (cmd) {
    case "report": cmdReport(cfg); break;
    case "guard": cmdGuard(cfg, { verbose: flags.has("--verbose") || flags.has("-v") }); break;
    case "remind": cmdRemind(cfg); break;
    case "status": cmdStatus(cfg); break;
    case "check": cmdCheck(cfg); break;
    case "install": flags.has("--cron-only") ? cmdInstallCronOnly(cfg) : cmdInstall(cfg); break;
    default:
      console.log("claude-usage-companion — commands: check | report | guard | remind | status | install [--cron-only]");
      if (!cmd) process.exit(0);
      process.exit(2);
  }
} catch (e) {
  console.error(`! ${e.message}`);
  process.exit(1);
}
