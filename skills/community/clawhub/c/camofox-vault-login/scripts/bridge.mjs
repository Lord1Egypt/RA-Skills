// No page prose, values, raw exceptions, or transport payloads leave this module.
const issuedErrors = new WeakSet();
export class BridgeError extends Error { constructor(code) { super(code); this.code = code; issuedErrors.add(this); } }
export const safeErrorCode = e => issuedErrors.has(e) && /^[A-Z_]{1,60}$/.test(e.code) ? e.code : 'OPERATION_FAILED';
const fail = code => { throw new BridgeError(code); };
export function origin(value) {
  if (typeof value !== 'string' || /[^!-~]/.test(value)) fail('INVALID_ORIGIN');
  let u; try { u = new URL(value); } catch { fail('INVALID_ORIGIN'); }
  if (u.protocol !== 'https:' || u.username || u.password || u.hostname.endsWith('.') || u.hostname.includes('xn--')) fail('INVALID_ORIGIN');
  return u.origin;
}
// Domain/default matching is deliberately narrowed to EXACT HTTPS origin, not eTLD+1.
// Starts-with is accepted only for a stored bare HTTPS origin; paths/regex fail closed per entry.
export function authorized(item, destination) {
  let found = false;
  for (const entry of item.login?.uris || []) {
    if (entry.match === 5) continue; // Never
    if (![null, undefined, 0, 1, 2].includes(entry.match) || typeof entry.uri !== 'string') continue;
    let stored = entry.uri;
    // Only bare DNS hostnames, never schemeless paths/ports/userinfo, imply HTTPS.
    if (/^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i.test(stored)) stored = 'https://' + stored;
    try {
      const storedOrigin = origin(stored);
      const u = new URL(stored);
      // Never erase a starts-with path/query/fragment restriction: exclude the entry.
      if (entry.match === 2 && (u.pathname !== '/' || u.search || u.hash)) continue;
      if (storedOrigin === destination) found = true;
    } catch { /* Invalid entries are not authorization grants. */ }
  }
  return found;
}
const safeFields = new Set(['username', 'password', 'totp']);
export async function bridge(request, deps) {
  let stage = 'request'; const filled = [];
  try {
    const { action = 'fill', tabId, fields = {}, itemId, trustedOrigins = [] } = request;
    if (!['list','inspect','fill','dry-run'].includes(action)) fail('INVALID_REQUEST');
    const expected = origin(request.origin);
    if (!Array.isArray(trustedOrigins) || trustedOrigins.some(x => origin(x) !== x)) fail('INVALID_MAPPING');
    const allowed = new Set([expected, ...trustedOrigins]);
    const keys = Object.keys(fields);
    if (keys.some(k => !safeFields.has(k)) || keys.some(k => typeof fields[k] !== 'string' || !fields[k] || fields[k].length > 1000)) fail('INVALID_FIELDS');
    if (['fill','dry-run'].includes(action) && (!tabId || !keys.length)) fail('INVALID_REQUEST');
    stage = 'vault-status';
    const status = await deps.vault.status();
    if (!deps.profile?.expectedVaultServerUrl || !deps.profile?.expectedVaultEmail) fail('VAULT_IDENTITY_REQUIRED');
    if (status.serverUrl !== deps.profile.expectedVaultServerUrl || status.userEmail !== deps.profile.expectedVaultEmail) fail('VAULT_IDENTITY_MISMATCH');
    if (!['locked','unlocked'].includes(status.status)) fail('VAULT_LOGIN_REQUIRED');
    if (status.status === 'locked') { stage = 'vault-unlock'; await deps.vault.unlock(); }
    stage = 'vault-lookup';
    const all = await deps.vault.items();
    if (!Array.isArray(all)) fail('INVALID_VAULT_RESPONSE');
    const candidates = all.filter(i => i.type === 1 && (!itemId || i.id === itemId)).filter(i => {
      // An unrelated unsupported/invalid entry must not deny discovery of every other item.
      try { return authorized(i, expected); } catch { if (itemId) throw new BridgeError('UNSUPPORTED_URI_RULE'); return false; }
    });
    // Intentionally do not return vault-controlled names, usernames, URLs or arbitrary strings.
    const metadata = i => {
      if (typeof i.id !== 'string' || !/^[a-f0-9-]{36}$/i.test(i.id)) fail('INVALID_ITEM_ID');
      return { id: i.id, hasUsername: !!i.login?.username, hasPassword: !!i.login?.password, hasTotp: !!i.login?.totp };
    };
    if (action === 'list') return { ok: true, stage: 'listed', items: candidates.map(metadata) };
    if (!candidates.length) fail('NO_MATCHING_ITEM');
    if (candidates.length !== 1) fail('AMBIGUOUS_ITEMS');
    const item = candidates[0]; const meta = metadata(item);
    // Explicit mappings may ONLY select additional exact origins already stored on this same item.
    for (const o of allowed) if (!authorized(item, o)) fail('MAPPING_NOT_IN_VAULT');
    if (action === 'inspect') return { ok: true, stage: 'inspected', item: meta };
    for (const kind of keys) {
      stage = 'guard-' + kind;
      const m = await deps.browser.inspect(tabId, fields[kind]);
      const current = origin(m.url);
      // Stay on the caller-selected destination throughout invocation; mappings do not permit navigation.
      if (current !== expected) fail('ORIGIN_CHANGED');
      if (m.top !== true || m.count !== 1 || m.tag !== 'INPUT' || m.visible !== true || m.disabled !== false || m.readOnly !== false) fail('UNSAFE_FIELD');
      const types = { username: ['text','email'], password: ['password'], totp: ['text','tel','number'] };
      if (!types[kind].includes(m.type)) fail('WRONG_FIELD_TYPE');
      if (!Array.isArray(m.actions)) fail('UNSAFE_FORM');
      for (const a of m.actions) if (origin(a) !== expected) fail('UNSAFE_FORM');
      if (action === 'dry-run') continue;
      let secret;
      if (kind === 'totp') { stage = 'totp'; secret = await deps.vault.totp(item); }
      else secret = item.login?.[kind];
      if (kind !== 'totp' && (typeof secret !== 'string' || !secret)) fail('MISSING_FIELD');
      let expiresAt;
      if (kind === 'totp') { expiresAt = secret?.expiresAt; secret = secret?.code; if (!/^[0-9]{6,8}$/.test(secret || '') || !Number.isFinite(expiresAt)) fail('INVALID_TOTP'); }
      // Recheck immediately before dispatch, including after potentially slow TOTP generation.
      stage = 'recheck-' + kind;
      const again = await deps.browser.inspect(tabId, fields[kind]);
      if (JSON.stringify(again) !== JSON.stringify(m)) fail('TARGET_CHANGED');
      if (kind === 'totp' && expiresAt - (deps.now || Date.now)() < 10000) fail('TOTP_TOO_OLD');
      stage = 'type-' + kind;
      await deps.browser.type(tabId, fields[kind], secret);
      secret = undefined; filled.push(kind);
    }
    return { ok: true, stage: action === 'dry-run' ? 'validated' : 'filled', item: meta, filled, submitted: false };
  } catch (e) {
    return { ok: false, stage, code: safeErrorCode(e), filled, outcome: stage.startsWith('type-') ? 'unknown-partial-fill-possible' : 'stopped', submitted: false };
  }
}
