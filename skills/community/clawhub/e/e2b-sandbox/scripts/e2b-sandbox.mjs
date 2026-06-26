#!/usr/bin/env node
import process from 'node:process';
import {
  createSandbox,
  listSandboxes,
  getSandboxInfo,
  execInSandbox,
  getSandboxHost,
  setSandboxTimeout,
  snapshotSandbox,
  killSandbox,
} from './e2b-core.mjs';

function usage() {
  console.log(`Usage:
  run-e2b.sh create [--label NAME] [--template TEMPLATE] [--timeout-ms MS] [--env KEY=VAL]... [--metadata KEY=VAL]...
  run-e2b.sh list
  run-e2b.sh info --sandbox ID_OR_LABEL
  run-e2b.sh exec --sandbox ID_OR_LABEL --cmd COMMAND [--cwd DIR] [--env KEY=VAL]... [--timeout-ms MS]
  run-e2b.sh host --sandbox ID_OR_LABEL --port PORT
  run-e2b.sh set-timeout --sandbox ID_OR_LABEL --timeout-ms MS
  run-e2b.sh snapshot --sandbox ID_OR_LABEL
  run-e2b.sh kill --sandbox ID_OR_LABEL
`);
}

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const out = { command, positionals: [], flags: {} };
  for (let i = 0; i < rest.length; i += 1) {
    const token = rest[i];
    if (!token.startsWith('--')) {
      out.positionals.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = rest[i + 1];
    if (next !== undefined && !next.startsWith('--')) {
      const prev = out.flags[key];
      if (prev === undefined) out.flags[key] = next;
      else if (Array.isArray(prev)) prev.push(next);
      else out.flags[key] = [prev, next];
      i += 1;
    } else {
      out.flags[key] = true;
    }
  }
  return out;
}

function asArray(value) {
  if (value === undefined) return [];
  return Array.isArray(value) ? value : [value];
}

function parseIntFlag(value, label) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) fail(`Invalid ${label}: ${value}`);
  return n;
}

function parseKeyValue(list, label) {
  const out = {};
  for (const item of list) {
    const idx = String(item).indexOf('=');
    if (idx <= 0) fail(`Expected ${label} in KEY=VALUE form, got: ${item}`);
    out[String(item).slice(0, idx)] = String(item).slice(idx + 1);
  }
  return out;
}

function print(data) {
  console.log(JSON.stringify(data, null, 2));
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));
  if (!command || command === 'help' || flags.help) {
    usage();
    return;
  }
  if (!process.env.E2B_API_KEY?.trim()) fail('Missing E2B_API_KEY.');

  switch (command) {
    case 'create':
      print(await createSandbox({
        label: typeof flags.label === 'string' ? flags.label : null,
        template: typeof flags.template === 'string' ? flags.template : 'base',
        timeoutMs: flags['timeout-ms'] ? parseIntFlag(flags['timeout-ms'], '--timeout-ms') : 3_600_000,
        envs: parseKeyValue(asArray(flags.env), '--env'),
        metadata: parseKeyValue(asArray(flags.metadata), '--metadata'),
      }));
      break;
    case 'list':
      print(await listSandboxes());
      break;
    case 'info':
      print(await getSandboxInfo({ sandbox: flags.sandbox }));
      break;
    case 'exec':
      print(await execInSandbox({
        sandbox: flags.sandbox,
        cmd: typeof flags.cmd === 'string' ? flags.cmd : null,
        cwd: typeof flags.cwd === 'string' ? flags.cwd : undefined,
        envs: parseKeyValue(asArray(flags.env), '--env'),
        timeoutMs: flags['timeout-ms'] ? parseIntFlag(flags['timeout-ms'], '--timeout-ms') : undefined,
      }));
      break;
    case 'host':
      print(await getSandboxHost({ sandbox: flags.sandbox, port: parseIntFlag(flags.port, '--port') }));
      break;
    case 'set-timeout':
      print(await setSandboxTimeout({ sandbox: flags.sandbox, timeoutMs: parseIntFlag(flags['timeout-ms'], '--timeout-ms') }));
      break;
    case 'snapshot':
      print(await snapshotSandbox({ sandbox: flags.sandbox }));
      break;
    case 'kill':
      print(await killSandbox({ sandbox: flags.sandbox }));
      break;
    default:
      fail(`Unknown command: ${command}`);
  }
}

main().catch((error) => {
  console.error(error?.stack || String(error));
  process.exit(1);
});
