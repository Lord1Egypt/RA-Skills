#!/usr/bin/env node
/**
 * Blink Wallet — Budget Controls CLI
 *
 * Usage:
 *   node budget.js status                         Show current budget status
 *   node budget.js set --hourly <sats> --daily <sats>   Set spending limits
 *   node budget.js set --off                      Remove all spending limits
 *   node budget.js log [--last <n>]               Show recent spending entries
 *   node budget.js reset                          Clear spending history (keeps active reservations)
 *   node budget.js reset --force                  Clear everything, incl. active reservations (unsafe mid-payment)
 *   node budget.js allowlist list                 Show allowed L402 domains
 *   node budget.js allowlist add <domain>         Add domain to allowlist
 *   node budget.js allowlist remove <domain>      Remove domain from allowlist
 *
 * Configuration:
 *   Limits are stored in ~/.blink/budget.json.
 *   Env vars BLINK_BUDGET_HOURLY_SATS, BLINK_BUDGET_DAILY_SATS, and
 *   BLINK_L402_ALLOWED_DOMAINS override the config file at runtime.
 *
 * Output: JSON to stdout. Status messages to stderr.
 * Dependencies: None (Node.js 22+ built-ins only).
 */

'use strict';

const { getConfig, readConfigFile, writeConfig, getStatus, getLog, resetLog, LOG_FILE } = require('./_budget');
const { strictArgv, assertPositionalCount } = require('./_blink_client');

// Every option this script accepts; anything else is refused (v3.0.4 strict sweep).
const ARG_OPTIONS = {
  hourly: { type: 'string' },
  daily: { type: 'string' },
  off: { type: 'boolean' },
  last: { type: 'string' },
  force: { type: 'boolean' },
};

// Maximum positionals (subcommand included); the minimum is left to each
// subcommand's usage message. PR #27 review: extra words were ignored.
const MAX_POSITIONALS = {
  status: 1,
  set: 1,
  log: 1,
  reset: 1,
  'allowlist list': 2,
  'allowlist add': 3,
  'allowlist remove': 3,
};

// Options are scoped per subcommand; a flag meant for another subcommand is
// rejected instead of silently ignored (e.g. `budget status --force`).
const SUBCOMMAND_OPTIONS = {
  status: [],
  set: ['--hourly', '--daily', '--off'],
  log: ['--last'],
  reset: ['--force'],
  allowlist: [],
};

function main() {
  let args;
  try {
    args = strictArgv(process.argv.slice(2), ARG_OPTIONS);
    const positionals = [];
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        if (ARG_OPTIONS[args[i].slice(2)].type === 'string') i++;
      } else positionals.push(args[i]);
    }
    const key = positionals[0] === 'allowlist' ? `allowlist ${positionals[1]}` : positionals[0];
    // Own keys only: `constructor` must reach the unknown-subcommand error.
    if (Object.hasOwn(MAX_POSITIONALS, key)) assertPositionalCount(positionals, 0, MAX_POSITIONALS[key]);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
  const subcommand = args[0];

  if (!subcommand) {
    console.error('Usage:');
    console.error('  blink budget status');
    console.error('  blink budget set --hourly <sats> --daily <sats>');
    console.error('  blink budget set --off');
    console.error('  blink budget log [--last <n>]');
    console.error('  blink budget reset [--force]');
    console.error('  blink budget allowlist list|add|remove <domain>');
    process.exit(1);
  }

  if (Object.hasOwn(SUBCOMMAND_OPTIONS, subcommand)) {
    const bad = args.slice(1).filter((a) => a.startsWith('--') && !SUBCOMMAND_OPTIONS[subcommand].includes(a));
    if (bad.length > 0) {
      console.error(`Error: option(s) ${bad.join(', ')} not valid for 'budget ${subcommand}'.`);
      process.exit(1);
    }
  }

  if (subcommand === 'status') {
    const status = getStatus();
    console.log(JSON.stringify(status, null, 2));
    return;
  }

  if (subcommand === 'set') {
    if (args.includes('--off')) {
      // Preserve allowlist when removing limits. readConfigFile fails closed
      // on corrupt config — do not overwrite a damaged file silently.
      const existing = readConfigFile();
      const preserved = existing.allowlist ? { allowlist: existing.allowlist } : {};
      writeConfig(preserved);
      console.error('Budget limits removed (allowlist preserved).');
      console.log(
        JSON.stringify(
          { message: 'Budget limits removed. No spending limits enforced. Allowlist preserved.' },
          null,
          2,
        ),
      );
      return;
    }

    const config = getConfig();
    let hourly = config.hourlyLimitSats;
    let daily = config.dailyLimitSats;

    // Strict positive-safe-integer parsing: permissive parseInt would round an
    // unsafe magnitude, accept 1000oops, or accept 1e5 — writing a value the
    // validated reader would then reject. (writeConfig also refuses, but the
    // CLI should fail with a clear, flag-level error first.)
    const parseLimitFlag = (flag) => {
      const idx = args.indexOf(flag);
      if (idx === -1) return null;
      const raw = args[idx + 1];
      if (raw === undefined || !/^[0-9]+$/.test(raw)) {
        console.error(
          `Error: ${flag} requires a positive integer value in sats (digits only, no suffixes or exponents).`,
        );
        process.exit(1);
      }
      const n = Number(raw);
      if (!Number.isSafeInteger(n) || n <= 0) {
        console.error(`Error: ${flag} is outside the safe-integer range.`);
        process.exit(1);
      }
      return n;
    };

    const parsedHourly = parseLimitFlag('--hourly');
    if (parsedHourly !== null) hourly = parsedHourly;
    const parsedDaily = parseLimitFlag('--daily');
    if (parsedDaily !== null) daily = parsedDaily;

    if (!args.includes('--hourly') && !args.includes('--daily')) {
      console.error('Error: provide --hourly <sats> and/or --daily <sats>, or --off to remove limits.');
      process.exit(1);
    }

    // Read existing config to preserve allowlist. readConfigFile fails closed
    // on corrupt config — do not overwrite a damaged file silently.
    const existing = readConfigFile();

    const newConfig = { ...existing };
    if (hourly !== null) newConfig.hourlyLimitSats = hourly;
    if (daily !== null) newConfig.dailyLimitSats = daily;

    writeConfig(newConfig);

    const output = {
      hourlyLimitSats: newConfig.hourlyLimitSats ?? null,
      dailyLimitSats: newConfig.dailyLimitSats ?? null,
      message: 'Budget limits updated.',
    };
    console.error('Budget limits updated.');
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (subcommand === 'log') {
    let limit = 20;
    const lastIdx = args.indexOf('--last');
    if (lastIdx !== -1 && args[lastIdx + 1]) {
      const n = parseInt(args[lastIdx + 1], 10);
      if (!isNaN(n) && n > 0) limit = n;
    }

    const entries = getLog(limit);
    const output = {
      logPath: LOG_FILE,
      showing: entries.length,
      entries: entries.map((e) => ({
        ...e,
        date: new Date(e.ts).toISOString(),
      })),
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (subcommand === 'reset') {
    const force = args.includes('--force');
    const { removed, keptReserved, discardedCorrupt } = resetLog({ force });
    const message =
      (force
        ? `Cleared ${removed} spending log entries (including any active reservations — use only while no payments are in flight).`
        : `Cleared ${removed} spending log entries. Kept ${keptReserved} active reservation(s); use --force to clear those too (unsafe while payments run).`) +
      (discardedCorrupt ? ' The previous log was corrupt and was discarded.' : '');
    const output = { removed, keptReserved, discardedCorrupt, force, message };
    console.error(message);
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (subcommand === 'allowlist') {
    const action = args[1];

    if (action === 'list') {
      const config = getConfig();
      const envOverride = process.env.BLINK_L402_ALLOWED_DOMAINS !== undefined;
      const output = {
        allowlist: config.allowlist,
        count: config.allowlist.length,
        source: envOverride ? 'BLINK_L402_ALLOWED_DOMAINS env var' : 'config file',
        message:
          config.allowlist.length === 0
            ? 'No allowlist configured — L402 auto-pay is BLOCKED until a domain is added: blink budget allowlist add <domain>'
            : `${config.allowlist.length} domain(s) allowed for L402 auto-pay.`,
      };
      console.log(JSON.stringify(output, null, 2));
      return;
    }

    if (action === 'add') {
      const domain = args[2];
      if (!domain) {
        console.error('Usage: blink budget allowlist add <domain>');
        process.exit(1);
      }
      const normalized = domain.toLowerCase().trim();

      // Read existing config (fails closed on corruption — do not overwrite).
      const existing = readConfigFile();

      const allowlist = Array.isArray(existing.allowlist) ? existing.allowlist.map((d) => d.toLowerCase().trim()) : [];

      if (allowlist.includes(normalized)) {
        console.error(`Domain ${normalized} is already in the allowlist.`);
        console.log(JSON.stringify({ domain: normalized, action: 'already_exists', allowlist }, null, 2));
        return;
      }

      allowlist.push(normalized);
      existing.allowlist = allowlist;
      writeConfig(existing);

      console.error(`Added ${normalized} to L402 allowlist.`);
      console.log(JSON.stringify({ domain: normalized, action: 'added', allowlist }, null, 2));
      return;
    }

    if (action === 'remove') {
      const domain = args[2];
      if (!domain) {
        console.error('Usage: blink budget allowlist remove <domain>');
        process.exit(1);
      }
      const normalized = domain.toLowerCase().trim();

      // Read existing config (fails closed on corruption — do not overwrite).
      const existing = readConfigFile();

      const allowlist = Array.isArray(existing.allowlist) ? existing.allowlist.map((d) => d.toLowerCase().trim()) : [];

      const idx = allowlist.indexOf(normalized);
      if (idx === -1) {
        console.error(`Domain ${normalized} is not in the allowlist.`);
        console.log(JSON.stringify({ domain: normalized, action: 'not_found', allowlist }, null, 2));
        return;
      }

      allowlist.splice(idx, 1);
      existing.allowlist = allowlist;
      writeConfig(existing);

      console.error(`Removed ${normalized} from L402 allowlist.`);
      console.log(JSON.stringify({ domain: normalized, action: 'removed', allowlist }, null, 2));
      return;
    }

    console.error('Usage: blink budget allowlist list|add|remove <domain>');
    process.exit(1);
    return;
  }

  console.error(`Unknown subcommand: ${subcommand}`);
  console.error('Subcommands: status, set, log, reset, allowlist');
  process.exit(1);
}

if (require.main === module) {
  main();
}

module.exports = { main, ARG_OPTIONS };
