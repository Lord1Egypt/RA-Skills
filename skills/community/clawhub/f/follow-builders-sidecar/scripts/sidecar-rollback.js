#!/usr/bin/env node

import { fileURLToPath } from 'url';

import {
  disableCronJob,
  enableCronJob,
  findOriginalCronJob,
  findSidecarCronJob,
  listCronJobs,
  loadSidecarState,
  log,
  nowIso,
  saveSidecarState
} from './sidecar-common.js';

function parseArgs(argv) {
  const args = argv.slice(2);
  return {
    reenableOriginal: args.includes('--reenable-original')
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const state = await loadSidecarState();
  const cronJobs = await listCronJobs();
  const originalJob = findOriginalCronJob(cronJobs, state.originalJobId);
  const sidecarJob = findSidecarCronJob(cronJobs, state.sidecarJobId);

  if (sidecarJob?.enabled) {
    await disableCronJob(sidecarJob.id);
  }

  if (args.reenableOriginal && originalJob && !originalJob.enabled) {
    await enableCronJob(originalJob.id);
  }

  state.lastCheckedAt = nowIso();
  await saveSidecarState(state);

  process.stdout.write(`${JSON.stringify({
    status: 'ok',
    disabledSidecarJob: Boolean(sidecarJob?.enabled),
    reenabledOriginalJob: Boolean(args.reenableOriginal && originalJob && !originalJob.enabled),
    originalJobId: originalJob?.id || null,
    sidecarJobId: sidecarJob?.id || null
  })}\n`);
}

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    log('error', 'Sidecar rollback failed', {
      error: error.message,
      stack: error.stack
    });
    process.exit(1);
  });
}
