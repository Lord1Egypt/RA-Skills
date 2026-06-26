#!/usr/bin/env node
import { install } from '../src/install.js';
import { configure, addNode } from '../src/configure.js';
import { startMihomo, stopMihomo } from '../src/service.js';
import { status, listNodes, switchNode } from '../src/api.js';
import { watch } from '../src/watchdog.js';
import { loadConfig } from '../src/config.js';
import { output, error } from '../src/logger.js';

const HELP = `
mihomod - Network proxy manager and health watchdog for mihomo

USAGE:
    mihomod <command> [options]

COMMANDS:
    install              Download and install mihomo binary
    config <url>         Generate mihomo config from subscription URL
    add <protocol-url>   Add a single proxy node (vmess://, ss://, etc.)
    start                Start mihomo service
    stop                 Stop mihomo service
    status               Show current proxy status
    nodes                List all proxy nodes with delay
    switch [node]        Switch to a specific or best available node
    watch                Start health watchdog daemon
    help                 Show this help

OPTIONS:
    --json               Force JSON output
    --config <path>      Override config file path
    --api <url>          Override mihomo API URL
    --quiet              Suppress non-essential output

EXIT CODES:
    0  Success
    1  Runtime error
    2  Configuration error
    3  Network error
`.trim();

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0] || 'help';
  const flags = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--json') flags.json = true;
    else if (args[i] === '--quiet') flags.quiet = true;
    else if (args[i] === '--config' && args[i + 1]) { flags.configPath = args[++i]; }
    else if (args[i] === '--api' && args[i + 1]) { flags.apiUrl = args[++i]; }
    else positional.push(args[i]);
  }

  try {
    let config;
    if (!['install', 'help', '--help', '-h'].includes(cmd)) {
      config = loadConfig(flags.configPath);
      if (flags.apiUrl) config.mihomo.api = flags.apiUrl;
    }

    switch (cmd) {
      case 'install':
        output(await install(), flags);
        break;
      case 'config':
        if (!positional[0]) { error('Usage: mihomod config <subscription-url>', 2); }
        output(await configure(positional[0], config), flags);
        break;
      case 'add':
        if (!positional[0]) { error('Usage: mihomod add <protocol-url>', 2); }
        output(await addNode(positional[0], config), flags);
        break;
      case 'start':
        output(await startMihomo(config), flags);
        break;
      case 'stop':
        output(await stopMihomo(config), flags);
        break;
      case 'status':
        output(await status(config), flags);
        break;
      case 'nodes':
        output(await listNodes(config), flags);
        break;
      case 'switch':
        output(await switchNode(config, positional[0]), flags);
        break;
      case 'watch':
        await watch(config);
        break;
      case 'help': case '--help': case '-h':
        console.log(HELP);
        break;
      default:
        console.error(`Unknown command: ${cmd}`);
        console.log(HELP);
        process.exit(1);
    }
  } catch (e) {
    const code = e.exitCode || 1;
    if (process.stdout.isTTY && !flags.json) {
      console.error(`Error: ${e.message}`);
    } else {
      console.log(JSON.stringify({ error: true, message: e.message, code }));
    }
    process.exit(code);
  }
}

main();
