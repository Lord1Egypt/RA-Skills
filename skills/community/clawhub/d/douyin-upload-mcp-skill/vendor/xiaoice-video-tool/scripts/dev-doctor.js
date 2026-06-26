#!/usr/bin/env node

const {
  DevCommandError,
  buildCallbackEndpoint,
  createContext,
  exitWithError,
  fetchNgrokTunnels,
  formatErrorMessage,
  getNgrokTunnelInfo,
  getServiceHealth,
  logResolvedStateDir,
  normalizeBaseUrlOptional,
  readJsonFileSafe,
  requestJson,
} = require('./dev-utils');

async function checkCallbackEndpointReachability(endpoint) {
  try {
    const response = await requestJson(endpoint, {
      method: 'POST',
      body: {},
      timeoutMs: 5000,
    });
    return {
      reachable: true,
      status: response.status,
    };
  } catch (error) {
    return {
      reachable: false,
      error,
    };
  }
}

async function runDoctor({
  context,
  env = process.env,
  deps = {},
} = {}) {
  const resolvedContext = context || createContext({ env });
  const checkHealth = typeof deps.checkHealth === 'function'
    ? deps.checkHealth
    : async () => {
      const health = await getServiceHealth(resolvedContext, { timeoutMs: 2000 });
      return {
        ok: health.ok,
        healthUrl: resolvedContext.service.healthUrl,
      };
    };
  const getNgrokStatus = typeof deps.getNgrokStatus === 'function'
    ? deps.getNgrokStatus
    : async () => {
      const tunnels = await fetchNgrokTunnels(resolvedContext, { timeoutMs: 2500 });
      const tunnelInfo = getNgrokTunnelInfo(tunnels, resolvedContext.service.port);
      return {
        publicUrl: tunnelInfo.publicUrl,
        warnings: tunnelInfo.warnings,
      };
    };
  const getSyncedCallbackBaseUrl = typeof deps.getSyncedCallbackBaseUrl === 'function'
    ? deps.getSyncedCallbackBaseUrl
    : async () => {
      const runtimeConfig = readJsonFileSafe(resolvedContext.paths.runtimeConfigFile, {});
      return normalizeBaseUrlOptional(
        runtimeConfig && typeof runtimeConfig === 'object' ? runtimeConfig.callbackPublicBaseUrl : ''
      );
    };
  const checkCallbackEndpoint = typeof deps.checkCallbackEndpoint === 'function'
    ? deps.checkCallbackEndpoint
    : checkCallbackEndpointReachability;

  logResolvedStateDir('dev:doctor', resolvedContext);

  const findings = [];
  let expectedCallbackPublicBaseUrl = '';

  const health = await checkHealth();
  if (!health || !health.ok) {
    findings.push({
      check: 'service_health',
      message: `Service health check failed at ${resolvedContext.service.healthUrl}`,
      fix: `Run npm run dev:service and inspect ${resolvedContext.paths.serviceLogFile}`,
    });
  } else {
    console.log(`[dev:doctor] health OK at ${health.healthUrl || resolvedContext.service.healthUrl}`);
  }

  if (resolvedContext.ngrok.enabled) {
    try {
      const ngrokStatus = await getNgrokStatus();
      expectedCallbackPublicBaseUrl = normalizeBaseUrlOptional(ngrokStatus.publicUrl);
      for (const warning of ngrokStatus.warnings || []) {
        console.warn(`[dev:doctor] warning: ${warning}`);
      }
      console.log(`[dev:doctor] ngrok API OK at ${resolvedContext.ngrok.apiUrl}`);
      console.log(`[dev:doctor] ngrok public URL: ${expectedCallbackPublicBaseUrl}`);
    } catch (error) {
      findings.push({
        check: 'ngrok_api',
        message: `ngrok check failed: ${formatErrorMessage(error)}`,
        fix: `Run npm run dev:ngrok and inspect ${resolvedContext.paths.ngrokLogFile}`,
      });
    }
  } else {
    expectedCallbackPublicBaseUrl = resolvedContext.callbackPublicBaseUrlFromEnv;
    console.log('[dev:doctor] ngrok disabled (VIDEO_USE_NGROK=false), skip ngrok API check');
  }

  const runtimeCallback = normalizeBaseUrlOptional(await getSyncedCallbackBaseUrl());

  if (!runtimeCallback) {
    findings.push({
      check: 'callback_runtime_value',
      message: `runtime callbackPublicBaseUrl is empty in ${resolvedContext.paths.runtimeConfigFile}`,
      fix: 'Run npm run dev:callback:sync',
    });
  } else {
    console.log(`[dev:doctor] runtime callbackPublicBaseUrl: ${runtimeCallback}`);
  }

  if (expectedCallbackPublicBaseUrl && runtimeCallback && expectedCallbackPublicBaseUrl !== runtimeCallback) {
    findings.push({
      check: 'callback_sync',
      message: `callbackPublicBaseUrl mismatch: runtime=${runtimeCallback}, expected=${expectedCallbackPublicBaseUrl}`,
      fix: 'Run npm run dev:callback:sync',
    });
  }

  const reachabilityBaseUrl = runtimeCallback || expectedCallbackPublicBaseUrl;
  if (!reachabilityBaseUrl) {
    findings.push({
      check: 'callback_endpoint',
      message: 'Cannot determine callback endpoint URL',
      fix: 'Run npm run dev:up to bootstrap callback URL',
    });
  } else {
    const callbackEndpoint = buildCallbackEndpoint(reachabilityBaseUrl);
    const callbackReachability = await checkCallbackEndpoint(callbackEndpoint);
    const isReachable = callbackReachability && (callbackReachability.reachable || callbackReachability.ok);
    if (!isReachable) {
      findings.push({
        check: 'callback_endpoint',
        message: `Callback endpoint unreachable: ${callbackEndpoint} (${formatErrorMessage(callbackReachability && callbackReachability.error)})`,
        fix: 'Ensure ngrok tunnel and local service are both running, then rerun npm run dev:doctor',
      });
    } else {
      console.log(
        `[dev:doctor] callback endpoint reachable (HTTP ${callbackReachability.status || 0}) at ${callbackEndpoint}`
      );
    }
  }

  if (findings.length > 0) {
    const hasCallbackMismatch = findings.some((finding) => finding.check === 'callback_sync');
    for (const finding of findings) {
      console.error(`[dev:doctor] FAIL ${finding.check}: ${finding.message}`);
      console.error(`[dev:doctor] fix: ${finding.fix}`);
    }
    throw new DevCommandError(`doctor found ${findings.length} issue(s)`, {
      code: hasCallbackMismatch ? 'CALLBACK_URL_MISMATCH' : 'DOCTOR_FAILED',
    });
  }

  console.log('[dev:doctor] all checks passed');
  return {
    ok: true,
    expectedCallbackPublicBaseUrl,
    runtimeCallbackPublicBaseUrl: runtimeCallback,
  };
}

async function main() {
  await runDoctor();
}

if (require.main === module) {
  main().catch((error) => {
    exitWithError(error, 'dev:doctor');
  });
}

module.exports = {
  checkCallbackEndpointReachability,
  runDoctor,
  runDevDoctor: runDoctor,
};
