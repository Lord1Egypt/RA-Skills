#!/usr/bin/env node

const {
  DevCommandError,
  createContext,
  ensureRuntimeDir,
  exitWithError,
  fetchNgrokTunnels,
  getNgrokTunnelInfo,
  isProcessRunning,
  killProcess,
  logResolvedStateDir,
  readPidFile,
  removeFileIfExists,
  spawnDetachedProcess,
  verifyCommandAvailable,
  waitFor,
  writePidFile,
  writeTextFile,
} = require('./dev-utils');

async function discoverNgrokTunnel(context, { timeoutMs = 20000 } = {}) {
  return waitFor(
    async () => {
      try {
        const tunnels = await fetchNgrokTunnels(context, { timeoutMs: 1500 });
        const info = getNgrokTunnelInfo(tunnels, context.service.port);
        return info;
      } catch (error) {
        return null;
      }
    },
    {
      timeoutMs,
      intervalMs: 500,
      errorMessage: `Failed to discover ngrok HTTPS tunnel for port ${context.service.port}`,
      hints: [
        `Inspect ngrok logs at ${context.paths.ngrokLogFile}`,
        'If first-time setup, run: ngrok config add-authtoken <your-token>',
        'Check NGROK_API_URL and VIDEO_TASK_SERVICE_PORT in .env',
      ],
    }
  );
}

function buildNgrokArgs(context) {
  const args = ['http'];
  if (context.ngrok.domain) {
    args.push(`--domain=${context.ngrok.domain}`);
  }
  if (context.ngrok.region) {
    args.push(`--region=${context.ngrok.region}`);
  }
  args.push(String(context.service.port));
  return args;
}

async function runDevNgrok({ context = createContext(), timeoutMs = 20000 } = {}) {
  logResolvedStateDir('dev:ngrok', context);
  ensureRuntimeDir(context);

  verifyCommandAvailable(context.ngrok.bin, ['version']);

  const pidFile = context.paths.ngrokPidFile;
  const logFile = context.paths.ngrokLogFile;
  const urlFile = context.paths.ngrokUrlFile;
  const existingPid = readPidFile(pidFile);

  if (existingPid && isProcessRunning(existingPid)) {
    const info = await discoverNgrokTunnel(context, { timeoutMs: 8000 });
    for (const warning of info.warnings) {
      console.warn(`[dev:ngrok] warning: ${warning}`);
    }
    writeTextFile(urlFile, `${info.publicUrl}\n`);
    console.log(`[dev:ngrok] reuse running tunnel pid=${existingPid}`);
    console.log(`[dev:ngrok] public URL: ${info.publicUrl}`);
    return {
      reused: true,
      pid: existingPid,
      publicUrl: info.publicUrl,
      localAddr: info.localAddr,
      callbackEndpoint: `${info.publicUrl}/v1/callbacks/provider`,
      warnings: info.warnings,
    };
  }

  if (existingPid && !isProcessRunning(existingPid)) {
    removeFileIfExists(pidFile);
  }

  const ngrokEnv = { ...process.env };
  if (context.ngrok.authtoken) {
    ngrokEnv.NGROK_AUTHTOKEN = context.ngrok.authtoken;
  }

  const pid = await spawnDetachedProcess({
    command: context.ngrok.bin,
    args: buildNgrokArgs(context),
    cwd: context.repoRoot,
    logFilePath: logFile,
    env: ngrokEnv,
  });
  writePidFile(pidFile, pid);

  console.log(`[dev:ngrok] started pid=${pid}, waiting for tunnel ...`);

  let info;
  try {
    info = await discoverNgrokTunnel(context, { timeoutMs });
  } catch (error) {
    killProcess(pid);
    removeFileIfExists(pidFile);
    throw new DevCommandError('ngrok tunnel startup failed', [
      `Inspect ngrok logs at ${logFile}`,
      'If first-time setup, run: ngrok config add-authtoken <your-token>',
      `Verify NGROK_BIN in .env (current: ${context.ngrok.bin})`,
    ]);
  }

  for (const warning of info.warnings) {
    console.warn(`[dev:ngrok] warning: ${warning}`);
  }

  writeTextFile(urlFile, `${info.publicUrl}\n`);

  console.log(`[dev:ngrok] public URL: ${info.publicUrl}`);
  console.log(`[dev:ngrok] callback endpoint: ${info.publicUrl}/v1/callbacks/provider`);

  return {
    reused: false,
    pid,
    publicUrl: info.publicUrl,
    localAddr: info.localAddr,
    callbackEndpoint: `${info.publicUrl}/v1/callbacks/provider`,
    warnings: info.warnings,
  };
}

async function main() {
  await runDevNgrok();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:ngrok');
  });
}

module.exports = {
  buildNgrokArgs,
  discoverNgrokTunnel,
  runDevNgrok,
};
