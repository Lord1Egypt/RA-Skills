#!/usr/bin/env node

const {
  DevCommandError,
  buildCallbackEndpoint,
  createContext,
  exitWithError,
  isHttpsPublicUrl,
  logResolvedStateDir,
  normalizeBaseUrlOptional,
  readTextFileSafe,
  toTrimmedString,
} = require('./dev-utils');

function resolveCallbackPublicBaseUrl(context, { callbackPublicBaseUrl } = {}) {
  if (callbackPublicBaseUrl) {
    return normalizeBaseUrlOptional(callbackPublicBaseUrl);
  }

  const ngrokUrl = normalizeBaseUrlOptional(readTextFileSafe(context.paths.ngrokUrlFile, '').trim());
  if (ngrokUrl) {
    return ngrokUrl;
  }

  if (!context.ngrok.enabled && context.callbackPublicBaseUrlFromEnv) {
    return context.callbackPublicBaseUrlFromEnv;
  }

  throw new DevCommandError('Cannot resolve callbackPublicBaseUrl', [
    `Run npm run dev:ngrok first, or set VIDEO_CALLBACK_PUBLIC_BASE_URL in .env when VIDEO_USE_NGROK=false`,
  ]);
}

async function runDevCallbackSync({ context = createContext(), callbackPublicBaseUrl } = {}) {
  logResolvedStateDir('dev:callback:sync', context);

  if (!context.tokens.admin) {
    throw new DevCommandError('VIDEO_SERVICE_ADMIN_TOKEN is required', [
      'Set VIDEO_SERVICE_ADMIN_TOKEN in .env',
    ]);
  }

  const callbackBaseUrl = resolveCallbackPublicBaseUrl(context, { callbackPublicBaseUrl });
  if (context.ngrok.enabled && !isHttpsPublicUrl(callbackBaseUrl)) {
    throw new DevCommandError(`ngrok callback URL must be HTTPS: ${callbackBaseUrl}`, [
      'Use ngrok HTTPS public URL, then rerun npm run dev:callback:sync',
    ]);
  }

  await syncCallbackPublicBaseUrl({
    serviceBaseUrl: context.service.baseUrl,
    adminToken: context.tokens.admin,
    callbackPublicBaseUrl: callbackBaseUrl,
  });

  const callbackEndpoint = buildCallbackEndpoint(callbackBaseUrl);
  console.log(`[dev:callback:sync] synced callbackPublicBaseUrl=${callbackBaseUrl}`);
  console.log(`[dev:callback:sync] callback endpoint: ${callbackEndpoint}`);

  return {
    callbackPublicBaseUrl: callbackBaseUrl,
    callbackEndpoint,
  };
}

async function syncCallbackPublicBaseUrl({
  serviceBaseUrl,
  adminToken,
  callbackPublicBaseUrl,
  fetchImpl = global.fetch,
  timeoutMs = 5000,
} = {}) {
  const normalizedServiceBaseUrl = normalizeBaseUrlOptional(serviceBaseUrl);
  const normalizedCallbackPublicBaseUrl = normalizeBaseUrlOptional(callbackPublicBaseUrl);
  const trimmedAdminToken = toTrimmedString(adminToken);

  if (!normalizedServiceBaseUrl) {
    throw new DevCommandError('serviceBaseUrl is required', {
      code: 'MISSING_SERVICE_BASE_URL',
    });
  }
  if (!trimmedAdminToken) {
    throw new DevCommandError('adminToken is required', {
      code: 'MISSING_ADMIN_TOKEN',
    });
  }
  if (!normalizedCallbackPublicBaseUrl) {
    throw new DevCommandError('callbackPublicBaseUrl is required', {
      code: 'MISSING_CALLBACK_BASE_URL',
    });
  }
  if (typeof fetchImpl !== 'function') {
    throw new DevCommandError('fetch implementation is required', {
      code: 'MISSING_FETCH_IMPL',
    });
  }

  const endpoint = `${normalizedServiceBaseUrl}/v1/admin/config`;

  let response;
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      response = await fetchImpl(endpoint, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Token': trimmedAdminToken,
        },
        body: JSON.stringify({
          callbackPublicBaseUrl: normalizedCallbackPublicBaseUrl,
        }),
        signal: controller.signal,
      });
    } finally {
      clearTimeout(timer);
    }
  } catch (error) {
    throw new DevCommandError(`Failed to call ${endpoint}`, {
      code: 'ADMIN_CONFIG_SYNC_UNREACHABLE',
      hints: [
        'Run npm run dev:service to ensure service is online',
      ],
    });
  }

  let rawText = '';
  try {
    rawText = await response.text();
  } catch (error) {
    rawText = '';
  }

  if (!response.ok) {
    throw new DevCommandError(`Admin config sync failed with HTTP ${response.status}`, {
      code: 'ADMIN_CONFIG_SYNC_HTTP_ERROR',
      hints: [
        'Verify VIDEO_SERVICE_ADMIN_TOKEN in .env',
      ],
    });
  }

  let responseData = null;
  if (rawText) {
    try {
      responseData = JSON.parse(rawText);
    } catch (error) {
      responseData = null;
    }
  }

  return {
    endpoint,
    callbackPublicBaseUrl: normalizedCallbackPublicBaseUrl,
    responseStatus: response.status,
    responseData,
  };
}

async function main() {
  await runDevCallbackSync();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:callback:sync');
  });
}

module.exports = {
  resolveCallbackPublicBaseUrl,
  syncCallbackPublicBaseUrl,
  runDevCallbackSync,
};
