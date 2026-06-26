#!/usr/bin/env node

const {
  DevCommandError,
  buildCallbackEndpoint,
  createContext,
  exitWithError,
  logResolvedStateDir,
  saveBootstrapState,
} = require('./dev-utils');
const { runDevService } = require('./dev-service');
const { runDevNgrok } = require('./dev-ngrok');
const { runDevCallbackSync } = require('./dev-callback-sync');

async function runDevUp({
  context,
  env = process.env,
  deps = {},
} = {}) {
  const resolvedContext = context || createContext({ env });
  const ensureService = typeof deps.ensureService === 'function'
    ? deps.ensureService
    : async ({ context: serviceContext }) => runDevService({ context: serviceContext });
  const ensureNgrok = typeof deps.ensureNgrok === 'function'
    ? deps.ensureNgrok
    : async ({ context: ngrokContext }) => runDevNgrok({ context: ngrokContext });
  const syncCallback = typeof deps.syncCallback === 'function'
    ? deps.syncCallback
    : async ({ context: callbackContext, callbackPublicBaseUrl }) => runDevCallbackSync({
      context: callbackContext,
      callbackPublicBaseUrl,
    });
  const persistBootstrapState = typeof deps.saveBootstrapState === 'function'
    ? deps.saveBootstrapState
    : saveBootstrapState;

  if (resolvedContext.ngrok.enabled && !resolvedContext.tokens.admin) {
    throw new DevCommandError('VIDEO_SERVICE_ADMIN_TOKEN is required', {
      code: 'MISSING_ADMIN_TOKEN',
      hints: ['Set VIDEO_SERVICE_ADMIN_TOKEN in .env'],
    });
  }
  if (resolvedContext.ngrok.enabled && !resolvedContext.tokens.callback) {
    throw new DevCommandError('VIDEO_SERVICE_CALLBACK_TOKEN is required', {
      code: 'MISSING_CALLBACK_TOKEN',
      hints: ['Set VIDEO_SERVICE_CALLBACK_TOKEN in .env'],
    });
  }

  logResolvedStateDir('dev:up', resolvedContext);
  const service = await ensureService({ context: resolvedContext });

  let ngrok = null;
  let callbackPublicBaseUrl = resolvedContext.callbackPublicBaseUrlFromEnv;

  if (resolvedContext.ngrok.enabled) {
    ngrok = await ensureNgrok({ context: resolvedContext });
    callbackPublicBaseUrl = ngrok.publicUrl;
  } else if (!callbackPublicBaseUrl) {
    throw new DevCommandError('VIDEO_CALLBACK_PUBLIC_BASE_URL is required when VIDEO_USE_NGROK=false', {
      code: 'MISSING_CALLBACK_BASE_URL',
      hints: ['Set VIDEO_CALLBACK_PUBLIC_BASE_URL in .env, or set VIDEO_USE_NGROK=true'],
    });
  }

  const synced = await syncCallback({
    context: resolvedContext,
    callbackPublicBaseUrl,
  });

  persistBootstrapState(resolvedContext, {
    ngrokEnabled: resolvedContext.ngrok.enabled,
    serviceHealthUrl: resolvedContext.service.healthUrl,
    callbackPublicBaseUrl: synced.callbackPublicBaseUrl,
    callbackEndpoint: synced.callbackEndpoint,
  });

  console.log('[dev:up] bootstrap complete');
  console.log(`[dev:up] health URL: ${service.healthUrl}`);
  console.log(`[dev:up] callback URL: ${buildCallbackEndpoint(synced.callbackPublicBaseUrl)}`);

  return {
    service,
    ngrok,
    callbackPublicBaseUrl: synced.callbackPublicBaseUrl,
    callbackEndpoint: synced.callbackEndpoint,
  };
}

async function main() {
  await runDevUp();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:up');
  });
}

module.exports = {
  runDevUp,
};
