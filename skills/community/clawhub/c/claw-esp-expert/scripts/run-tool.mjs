#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import process from 'node:process';

const require = createRequire(import.meta.url);
const { skillTools } = require('../dist/index.js');
const ALLOWED_TOOLS = new Set(['manage_env', 'explore_demo', 'resolve_component', 'analyze_partitions', 'decode_panic', 'analyze_monitor', 'flash_and_monitor', 'execute_project', 'safe_build']);

function usage() {
  console.log(`run-tool usage:
  node scripts/run-tool.mjs <manage_env|explore_demo|resolve_component|analyze_partitions|decode_panic|analyze_monitor|flash_and_monitor|execute_project|safe_build> --stdin

Examples:
  printf '%s' '{"action":"check"}' | node scripts/run-tool.mjs manage_env --stdin
  printf '%s' '{"query":"gpio"}' | node scripts/run-tool.mjs explore_demo --stdin
  printf '%s' '{"query":"led_strip","target":"esp32s3"}' | node scripts/run-tool.mjs resolve_component --stdin
  printf '%s' '{"projectPath":"/path/to/project","rawLog":"overflow 0x20000"}' | node scripts/run-tool.mjs analyze_partitions --stdin
  printf '%s' '{"chip":"esp32s3","elfPath":"/path/to/app.elf","log":"Guru Meditation Error..."}' | node scripts/run-tool.mjs decode_panic --stdin
  printf '%s' '{"chip":"esp32s3","elfPath":"/path/to/app.elf","log":"...monitor output..."}' | node scripts/run-tool.mjs analyze_monitor --stdin
  printf '%s' '{"projectPath":"/path/to/project","chip":"esp32s3","port":"/dev/ttyUSB0"}' | node scripts/run-tool.mjs flash_and_monitor --stdin
  printf '%s' '{"projectPath":"/path/to/project","chip":"esp32s3","port":"/dev/ttyUSB0"}' | node scripts/run-tool.mjs execute_project --stdin
  printf '%s' '{"projectPath":"/path/to/project","chip":"esp32"}' | node scripts/run-tool.mjs safe_build --stdin`);
}

function parseArgs(argv) {
  const [toolName, ...rest] = argv;
  const useStdin = rest.includes('--stdin');

  return { toolName, useStdin };
}

function readJsonFromStdin() {
  const input = readFileSync(0, 'utf8').trim();
  if (!input) return {};

  try {
    return JSON.parse(input);
  } catch (error) {
    throw new Error(`Invalid JSON input: ${error instanceof Error ? error.message : String(error)}`);
  }
}

async function main() {
  const { toolName, useStdin } = parseArgs(process.argv.slice(2));

  if (!toolName || toolName === '--help' || toolName === '-h' || toolName === 'help') {
    usage();
    process.exit(toolName ? 0 : 1);
  }

  if (!ALLOWED_TOOLS.has(toolName)) {
    throw new Error(`Unsupported tool: ${toolName}`);
  }

  if (!useStdin) {
    throw new Error('Use --stdin and pass JSON input through stdin.');
  }

  const payload = readJsonFromStdin();
  const result = await skillTools[toolName](payload);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  usage();
  process.exit(1);
});
