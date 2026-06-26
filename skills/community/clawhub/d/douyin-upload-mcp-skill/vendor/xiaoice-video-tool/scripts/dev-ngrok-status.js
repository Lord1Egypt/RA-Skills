#!/usr/bin/env node

const {
  createContext,
  exitWithError,
  fetchNgrokTunnels,
  getNgrokTunnelInfo,
  logResolvedStateDir,
  writeTextFile,
} = require('./dev-utils');

async function runDevNgrokStatus({ context = createContext() } = {}) {
  logResolvedStateDir('dev:ngrok:status', context);

  const tunnels = await fetchNgrokTunnels(context, { timeoutMs: 2500 });
  const info = getNgrokTunnelInfo(tunnels, context.service.port);

  for (const warning of info.warnings) {
    console.warn(`[dev:ngrok:status] warning: ${warning}`);
  }

  writeTextFile(context.paths.ngrokUrlFile, `${info.publicUrl}\n`);

  const callbackEndpoint = `${info.publicUrl}/v1/callbacks/provider`;
  console.log(`[dev:ngrok:status] public URL: ${info.publicUrl}`);
  console.log(`[dev:ngrok:status] local addr: ${info.localAddr || '(unknown)'}`);
  console.log(`[dev:ngrok:status] callback endpoint: ${callbackEndpoint}`);

  return {
    publicUrl: info.publicUrl,
    localAddr: info.localAddr,
    callbackEndpoint,
    warnings: info.warnings,
  };
}

async function main() {
  await runDevNgrokStatus();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:ngrok:status');
  });
}

module.exports = {
  runDevNgrokStatus,
};
