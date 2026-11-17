#!/usr/bin/env node
import { bridge, BridgeError, safeErrorCode } from './bridge.mjs';
import { createVault, createBrowser, loadProfile } from './runtime.mjs';
// Read NONSECRET request JSON on stdin. Never pass credentials to this interface.
let result;
try {
  if (process.argv.length !== 2) throw new BridgeError('STDIN_ONLY');
  let input = '';
  for await (const chunk of process.stdin) { input += chunk; if (input.length > 32768) throw new BridgeError('REQUEST_TOO_LARGE'); }
  const request = JSON.parse(input);
  const permitted = ['action','origin','itemId','tabId','fields','trustedOrigins','userId','sessionKey'];
  if (!request || typeof request !== 'object' || Array.isArray(request)) throw new BridgeError('INVALID_REQUEST');
  if (Object.keys(request).some(k => !permitted.includes(k))) throw new BridgeError('UNKNOWN_REQUEST_KEY');
  if (typeof request.userId !== 'string' || !request.userId || typeof request.sessionKey !== 'string' || !request.sessionKey) throw new BridgeError('CALLER_IDENTITY_REQUIRED');
  const profile = await loadProfile();
  const browser = ['list','inspect'].includes(request.action) ? {} : await createBrowser({ ...profile, userId: request.userId, sessionKey: request.sessionKey });
  result = await bridge(request, { vault: createVault({ profile }), browser, profile });
} catch (e) { result = { ok: false, stage: 'setup', code: safeErrorCode(e) }; }
process.stdout.write(JSON.stringify(result) + '\n');
// Force process termination: installed contract cannot cancel in-flight fetch on timeout.
process.exit(result.ok ? 0 : 1);
