#!/usr/bin/env node
import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const __dirname = dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(readFileSync(resolve(__dirname, '../references/config.json'), 'utf8'));

const { OPENCLAW_GATEWAY_URL, OPENCLAW_GATEWAY_TOKEN } = process.env;
if (!OPENCLAW_GATEWAY_TOKEN) {
  console.error('Missing OPENCLAW_GATEWAY_TOKEN in .env');
  process.exit(1);
}

const globalFlags = [];
if (OPENCLAW_GATEWAY_URL) {
  globalFlags.push('--url', OPENCLAW_GATEWAY_URL);
}

const skillRoot = process.cwd();

function buildArgs(subcommandArgs) {
  const args = [...globalFlags, 'cron', ...subcommandArgs];
  return args;
}

async function runOpenClaw(subcommandArgs) {
  const args = buildArgs(subcommandArgs);
  args.push('--token', OPENCLAW_GATEWAY_TOKEN);
  const result = await execFileAsync('openclaw', args, { encoding: 'utf8', env: process.env });
  return result.stdout;
}

function commandMessage(scriptPath) {
  return `cd "${skillRoot}" && node ${scriptPath}`;
}

async function createCronJob(name, schedule, scriptPath) {
  const message = commandMessage(scriptPath);
  const args = ['add', '--name', name, '--cron', schedule, '--message', message, '--session', 'isolated', '--wake', 'now'];
  console.log(`Creating cron job ${name} (${schedule})...`);
  const stdout = await runOpenClaw(args);
  console.log(stdout.trim());
}

async function main() {
  await createCronJob('onlybots-post', config.postingSchedule || '0 14 * * *', 'scripts/post-to-onlybots.js');
  await createCronJob('onlybots-engage', config.engagementSchedule || '0 */6 * * *', 'scripts/engage-with-bots.js');
  console.log('\nSetup complete.');
}

main().catch((err) => {
  console.error('Failed to set up cron jobs:', err.message);
  process.exit(1);
});
