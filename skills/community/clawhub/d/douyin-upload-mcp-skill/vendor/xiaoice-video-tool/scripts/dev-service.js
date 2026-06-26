#!/usr/bin/env node

const path = require('node:path');

const {
  DevCommandError,
  createContext,
  ensureRuntimeDir,
  exitWithError,
  getServiceHealth,
  isProcessRunning,
  killProcess,
  logResolvedStateDir,
  readPidFile,
  removeFileIfExists,
  spawnDetachedProcess,
  validateServiceTokens,
  waitForServiceHealth,
  writePidFile,
} = require('./dev-utils');

async function runDevService({ context = createContext(), timeoutMs = 20000 } = {}) {
  logResolvedStateDir('dev:service', context);
  validateServiceTokens(context, {
    requireAdmin: true,
    requireInternal: true,
    requireCallback: true,
  });
  ensureRuntimeDir(context);

  const pidFile = context.paths.servicePidFile;
  const logFile = context.paths.serviceLogFile;
  const existingPid = readPidFile(pidFile);
  const existingHealth = await getServiceHealth(context, { timeoutMs: 1200 });

  if (existingHealth.ok) {
    if (existingPid && isProcessRunning(existingPid)) {
      console.log(`[dev:service] reuse running service pid=${existingPid}`);
      return {
        reused: true,
        pid: existingPid,
        healthUrl: context.service.healthUrl,
        logFile,
      };
    }
    console.log(`[dev:service] reuse healthy service at ${context.service.baseUrl}`);
    return {
      reused: true,
      pid: null,
      healthUrl: context.service.healthUrl,
      logFile,
    };
  }

  if (existingPid && isProcessRunning(existingPid)) {
    throw new DevCommandError(
      `Found running service process pid=${existingPid}, but /health is not ready`,
      [
        `Inspect logs at ${logFile}`,
        `Stop the stale process manually, then rerun npm run dev:service`,
      ]
    );
  }

  if (existingPid && !isProcessRunning(existingPid)) {
    removeFileIfExists(pidFile);
  }

  const serviceCliPath = path.join(context.repoRoot, 'src/service/cli.js');
  const pid = await spawnDetachedProcess({
    command: process.execPath,
    args: [serviceCliPath],
    cwd: context.repoRoot,
    logFilePath: logFile,
  });

  writePidFile(pidFile, pid);
  console.log(`[dev:service] started pid=${pid}, waiting for /health ...`);

  try {
    await waitForServiceHealth(context, { timeoutMs });
  } catch (error) {
    killProcess(pid);
    removeFileIfExists(pidFile);
    throw new DevCommandError('Service failed to become healthy', [
      `Inspect logs at ${logFile}`,
      'Verify .env tokens and provider settings',
    ]);
  }

  console.log(`[dev:service] healthy at ${context.service.healthUrl}`);
  return {
    reused: false,
    pid,
    healthUrl: context.service.healthUrl,
    logFile,
  };
}

async function main() {
  await runDevService();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:service');
  });
}

module.exports = {
  runDevService,
};
