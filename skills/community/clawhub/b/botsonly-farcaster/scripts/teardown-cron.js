#!/usr/bin/env node
import 'dotenv/config';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

const { OPENCLAW_GATEWAY_URL, OPENCLAW_GATEWAY_TOKEN } = process.env;
if (!OPENCLAW_GATEWAY_TOKEN) {
  console.error('Missing OPENCLAW_GATEWAY_TOKEN in .env');
  process.exit(1);
}

const globalFlags = [];
if (OPENCLAW_GATEWAY_URL) {
  globalFlags.push('--url', OPENCLAW_GATEWAY_URL);
}

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

async function listCronJobs() {
  const stdout = await runOpenClaw(['list', '--json']);
  const trimmed = stdout.trim();
  if (!trimmed) {
    return [];
  }
  const parsed = JSON.parse(trimmed);
  return parsed.jobs || [];
}

async function removeCronJob(jobId, name) {
  console.log(`Removing cron job ${name} (${jobId})...`);
  await runOpenClaw(['rm', jobId]);
}

async function main() {
  const jobs = await listCronJobs();
  const target = jobs.filter((job) => job.name?.startsWith('onlybots-'));

  if (!target.length) {
    console.log('No onlybots cron jobs found.');
    return;
  }

  for (const job of target) {
    await removeCronJob(job.id, job.name);
  }

  console.log(`\nRemoved ${target.length} onlybots cron job(s).`);
}

main().catch((err) => {
  console.error('Failed to tear down cron jobs:', err.message);
  process.exit(1);
});
