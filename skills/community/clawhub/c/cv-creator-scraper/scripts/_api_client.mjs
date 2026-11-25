// Creativault Open API client module.
// Shared request, retry, auth, runtime profile, and response shaping logic.

import { spawnSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { isNavosProfile, loadRuntimeProfile } from './_runtime_profile.mjs';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_META = loadSkillMeta();
const RUNTIME_PROFILE = loadRuntimeProfile({ skillMeta: SKILL_META });

const CV_BASE_PROD = 'https://api.creativault.vip/skill/creativault';

function resolveApiBase() {
  const explicit = (process.env.CV_API_BASE_URL || '').trim();
  if (explicit) return explicit.replace(/\/+$/, '');

  if (SKILL_META.channel === 'stable') {
    return CV_BASE_PROD;
  }

  // 非 stable（staging/dev）走内网地址，不硬编码在源码里，
  // 避免内网域名随仓库 / skill 包分发泄露。仅从环境变量读取。
  const staging = (process.env.CV_API_BASE_STAGING_URL || '').trim();
  if (staging) return staging.replace(/\/+$/, '');

  console.error(JSON.stringify({
    error: 'Staging API base URL is not configured',
    hint: 'Set CV_API_BASE_STAGING_URL (or CV_API_BASE_URL) to the internal API base for non-stable channels.',
    channel: SKILL_META.channel,
  }));
  process.exit(1);
}

const API_BASE = resolveApiBase();
const PARTNER_CODE = (
  process.env.CV_PARTNER_CODE
  || RUNTIME_PROFILE.partner_code
  || (isNavosProfile(RUNTIME_PROFILE) ? 'navos' : '')
).trim();

// Back-fill env so downstream modules can infer the matching environment.
if (!process.env.CV_API_BASE_URL) {
  process.env.CV_API_BASE_URL = API_BASE;
}
if (RUNTIME_PROFILE.navos_base_url && !process.env.NAVOS_BASE_URL) {
  process.env.NAVOS_BASE_URL = String(RUNTIME_PROFILE.navos_base_url).replace(/\/+$/, '');
}
if (RUNTIME_PROFILE.navos_region && !process.env.NAVOS_REGION) {
  process.env.NAVOS_REGION = String(RUNTIME_PROFILE.navos_region).trim();
}
if (RUNTIME_PROFILE.navos_validate_base_url && !process.env.NAVOS_VALIDATE_BASE_URL) {
  process.env.NAVOS_VALIDATE_BASE_URL = String(RUNTIME_PROFILE.navos_validate_base_url).replace(/\/+$/, '');
}
if (RUNTIME_PROFILE.navos_callback_base_url && !process.env.NAVOS_CALLBACK_BASE_URL) {
  process.env.NAVOS_CALLBACK_BASE_URL = String(RUNTIME_PROFILE.navos_callback_base_url).replace(/\/+$/, '');
}

const MAX_RETRIES = 3;
const DEFAULT_RETRY_AFTER = 60;
const PRECHECK_CACHE_TTL_MS = 5 * 60 * 1000;
const _balanceCache = new Map();
let _credsPromise = null;

function isPrecheckDisabled() {
  return (process.env.NAVOS_PRECHECK_DISABLED || '').trim().toLowerCase() === 'true';
}

async function getCachedNavosBalance(uid) {
  if (!uid) return null;
  const now = Date.now();
  const cached = _balanceCache.get(uid);
  if (cached && (now - cached.fetchedAt) < PRECHECK_CACHE_TTL_MS) {
    return cached.balance;
  }

  try {
    const { checkNavosBalance } = await import('./_navos_balance.mjs');
    const balance = await checkNavosBalance({ uid });
    _balanceCache.set(uid, { balance, fetchedAt: now });
    return balance;
  } catch (err) {
    console.error(JSON.stringify({
      navos_precheck_warning: 'Navos balance query failed; skipping pre-check.',
      reason: err.message,
    }));
    return null;
  }
}

function invalidateNavosBalanceCache(uid) {
  if (uid) _balanceCache.delete(uid);
}

function loadSkillMeta() {
  try {
    return JSON.parse(readFileSync(new URL('../skill.json', import.meta.url), 'utf8'));
  } catch {
    const fallback = {
      name: 'creator-scraper-cv',
      version: 'unknown',
      channel: 'stable',
    };
    try {
      const skillMd = readFileSync(new URL('../SKILL.md', import.meta.url), 'utf8');
      const versionMatch = skillMd.match(/version:\s*"?([^"\n]+)"?/);
      if (versionMatch?.[1]) {
        fallback.version = versionMatch[1].trim();
      }
    } catch {
      // Keep default fallback metadata.
    }
    return { ...fallback };
  }
}

if (!API_BASE) {
  console.error(JSON.stringify({
    error: 'API base URL is not configured',
    hint: 'Set CV_API_BASE_URL environment variable, or configure "api_base_url" in skill.json',
    example: 'export CV_API_BASE_URL=https://your-api-host.com',
  }));
  process.exit(1);
}

function resolveEnvCredentials() {
  const apiKey = (process.env.CV_API_KEY || '').trim();
  if (!apiKey) {
    console.error(JSON.stringify({
      error: 'CV_API_KEY environment variable is not set',
      hint: 'Set it via: export CV_API_KEY=cv_live_your_key_here',
    }));
    process.exit(1);
  }

  return {
    apiKey,
    userIdentity: (process.env.CV_USER_IDENTITY || '').trim(),
    partnerCode: PARTNER_CODE || 'common',
    uid: null,
    source: 'env',
  };
}

async function resolveNavosCredentials({ forceRefresh = false } = {}) {
  const { resolveCvCredentials } = await import('./_cv_credentials.mjs');
  return resolveCvCredentials({
    partnerCode: PARTNER_CODE || 'navos',
    cvBase: API_BASE,
    skillChannel: SKILL_META.channel || 'stable',
    navosRegion: RUNTIME_PROFILE.navos_region || '',
    navosValidateBaseUrl: RUNTIME_PROFILE.navos_validate_base_url || '',
    navosCallbackBaseUrl: RUNTIME_PROFILE.navos_callback_base_url || '',
    forceRefresh,
  });
}

async function getCredentials({ forceRefresh = false } = {}) {
  if (forceRefresh) {
    _credsPromise = null;
  }
  if (!_credsPromise) {
    _credsPromise = (
      RUNTIME_PROFILE.auth_mode === 'navos'
        ? resolveNavosCredentials({ forceRefresh })
        : Promise.resolve(resolveEnvCredentials())
    ).catch((err) => {
      _credsPromise = null;
      throw err;
    });
  }
  return _credsPromise;
}

function buildPartnerHeaders(partnerCode) {
  const headers = {
    'Content-Type': 'application/json',
    'X-Partner-Code': partnerCode,
    'X-Timestamp': Math.floor(Date.now() / 1000).toString(),
    'X-Nonce': randomBytes(16).toString('hex'),
  };
  if (RUNTIME_PROFILE.navos_region) {
    headers['X-Navos-Region'] = String(RUNTIME_PROFILE.navos_region);
  }
  return headers;
}

async function createCreatorResultSet({ platform, queryParams, result }) {
  if (!isNavosProfile(RUNTIME_PROFILE)) return null;

  const items = getResultItems(result);
  if (items.length === 0) return null;

  const creds = await getCredentials();
  const { loadNavosIdentity } = await import('./_navos_identity.mjs');
  const identity = loadNavosIdentity();
  const partnerCode = creds.partnerCode || PARTNER_CODE || 'navos-global';
  const url = `${API_BASE}/internal/partners/${encodeURIComponent(partnerCode)}/creator-result-set`;
  const body = {
    uid: identity.uid,
    token: identity.token,
    email: creds.userIdentity || identity.email,
    client_version: SKILL_META.channel || '',
    platform,
    locale: RUNTIME_PROFILE.default_lang === 'en' ? 'en' : 'zh',
    title: `Navos ${platform} creator search`,
    query: queryParams || {},
    items,
    meta: result?.meta || {},
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: buildPartnerHeaders(partnerCode),
    body: JSON.stringify(body),
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok || payload?.code !== 200 || !payload?.data?.list_url) {
    const reason = payload?.en_message || payload?.zh_message || `HTTP ${response.status}`;
    throw new Error(`CV creator result set rejected: ${reason}`);
  }

  return payload.data;
}

function buildOutreachWorkspaceRedirectPath(context = {}) {
  const locale = RUNTIME_PROFILE.default_lang === 'en' ? 'en' : 'zh';
  const query = new URLSearchParams({
    view: 'email',
    source: 'navos',
    layout: 'compact',
  });
  if (context.task_id) query.set('task_id', String(context.task_id));
  if (context.email) query.set('email', String(context.email));
  return `/${locale}/asset/studio/influencer-submission?${query.toString()}`;
}

async function createPartnerWebLink({ redirectPath }) {
  if (!isNavosProfile(RUNTIME_PROFILE) || !redirectPath) return null;

  const creds = await getCredentials();
  const { loadNavosIdentity } = await import('./_navos_identity.mjs');
  const identity = loadNavosIdentity();
  const partnerCode = creds.partnerCode || PARTNER_CODE || 'navos-global';
  const url = `${API_BASE}/internal/partners/${encodeURIComponent(partnerCode)}/web-link-ticket`;
  const body = {
    uid: identity.uid,
    token: identity.token,
    email: creds.userIdentity || identity.email,
    client_version: SKILL_META.channel || '',
    redirect_path: redirectPath,
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: buildPartnerHeaders(partnerCode),
    body: JSON.stringify(body),
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok || payload?.code !== 200 || !payload?.data?.url) {
    const reason = payload?.en_message || payload?.zh_message || `HTTP ${response.status}`;
    throw new Error(`CV web link ticket rejected: ${reason}`);
  }

  return payload.data;
}

function getResultItems(result) {
  if (Array.isArray(result?.data)) return result.data;
  if (Array.isArray(result?.data?.items)) return result.data.items;
  if (Array.isArray(result?.data?.list)) return result.data.list;
  if (Array.isArray(result?.data?.records)) return result.data.records;
  return [];
}

export async function attachCreatorResultSetUrl(result, platform, queryParams = {}) {
  if (!isNavosProfile(RUNTIME_PROFILE)) return result;

  try {
    const snapshot = await createCreatorResultSet({ platform, queryParams, result });
    if (snapshot?.list_url) {
      const separator = snapshot.list_url.includes('?') ? '&' : '?';
      // Keep the browser entry aligned with the Navos language captured for this run.
      // Navos can replace this parameter at click time for links in historical chats.
      result.cv_list_url = `${snapshot.list_url}${separator}navos_locale=${encodeURIComponent(
        RUNTIME_PROFILE.navos_language || 'en-US'
      )}`;
      result.cv_result_set_id = snapshot.result_set_id || null;
      result.cv_result_set_expires_at = snapshot.result_set_expires_at || null;
      result.cv_list_ticket_expires_at = snapshot.ticket_expires_at || null;
    }
  } catch (err) {
    console.error(JSON.stringify({
      cv_list_url_warning: 'Failed to create creator result list link; keeping chat result only.',
      reason: err.message,
    }));
  }

  return result;
}

export async function attachOutreachWorkspaceUrl(result, context = {}) {
  if (!isNavosProfile(RUNTIME_PROFILE)) return result;

  try {
    const redirectPath = buildOutreachWorkspaceRedirectPath(context);
    const ticket = await createPartnerWebLink({ redirectPath });
    if (ticket?.url) {
      result.cv_outreach_url = ticket.url;
      result.cv_outreach_redirect_path = ticket.redirect_path || redirectPath;
      result.cv_outreach_expires_at = ticket.expires_at || null;
    }
  } catch (err) {
    console.error(JSON.stringify({
      cv_outreach_url_warning: 'Failed to create CreatiVault outreach workspace link; keeping chat result only.',
      reason: err.message,
    }));
  }

  return result;
}

function ensureUserIdentity(creds) {
  if (!creds?.userIdentity) {
    const hint = RUNTIME_PROFILE.auth_mode === 'navos'
      ? 'Ensure Navos identity contains an email field, or set CV_USER_IDENTITY for debugging.'
      : 'Set CV_USER_IDENTITY to the email associated with your API Key account.';
    console.error(JSON.stringify({
      error: 'User identity is missing',
      hint,
      profile: RUNTIME_PROFILE.profile,
      partner_code: PARTNER_CODE || null,
    }));
    process.exit(1);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function applyDefaultServiceLevel(body) {
  const serviceLevel = RUNTIME_PROFILE.default_service_level;
  if (!serviceLevel || !body || body.service_level) {
    return body;
  }
  return { ...body, service_level: serviceLevel };
}

function applyDefaultLang(body) {
  const lang = RUNTIME_PROFILE.default_lang;
  if (!lang || !body || body.lang) {
    return body;
  }
  return { ...body, lang };
}

async function runBalancePrecheck(creds, options) {
  if (
    !RUNTIME_PROFILE.balance_precheck
    || isPrecheckDisabled()
    || creds.source === 'env'
    || !creds.uid
    || !isNavosProfile(RUNTIME_PROFILE)
  ) {
    return;
  }

  const balance = await getCachedNavosBalance(creds.uid);
  if (balance === null) return;

  const required = options.estimatedCredits ?? 0;
  if (balance.available_balance <= 0) {
    console.error(JSON.stringify({
      error: 'Navos balance insufficient',
      code: 'NAVOS_INSUFFICIENT_BALANCE',
      available_balance: balance.available_balance,
      total_balance: balance.total_balance,
      hint: 'Top up your Navos credits to continue using CreatiVault Skill.',
    }));
    process.exit(1);
  }
  if (required > 0 && balance.available_balance < required) {
    console.error(JSON.stringify({
      error: 'Navos balance insufficient for this operation',
      code: 'NAVOS_INSUFFICIENT_BALANCE',
      required,
      available_balance: balance.available_balance,
      total_balance: balance.total_balance,
    }));
    process.exit(1);
  }
}

function buildErrorOutput(data) {
  const errorOutput = {
    error: data.error?.message || 'Request failed',
    code: data.error?.code,
  };

  if (!RUNTIME_PROFILE.hide_cv_meta) {
    errorOutput.request_id = data.meta?.request_id;
  }
  if (data.error?.code === 40201) {
    errorOutput.insufficient_credits = true;
    if (!RUNTIME_PROFILE.hide_cv_meta) {
      errorOutput.credits_remaining = data.meta?.credits_remaining;
    }
  }
  if (data.error?.code === 42902) {
    errorOutput.daily_quota_exhausted = true;
    if (!RUNTIME_PROFILE.hide_cv_meta) {
      errorOutput.daily_quota_remaining = data.meta?.quota_remaining;
    }
  }

  return errorOutput;
}

function stripHiddenMeta(data) {
  if (!RUNTIME_PROFILE.hide_cv_meta || !data.meta) {
    return data;
  }

  const {
    credits_remaining,
    credits_consumed,
    quota_remaining,
    service_level,
    request_id,
    ...restMeta
  } = data.meta;
  data.meta = restMeta;
  return data;
}

function maybeHandleSkillUpdateMeta(meta = {}) {
  if (!RUNTIME_PROFILE.enable_skill_update) {
    return;
  }

  const latestVersion = meta?.skill_latest_version;
  const updateRequired = Boolean(meta?.skill_update_required);
  const updateAvailable = updateRequired || Boolean(meta?.skill_update_available);
  if (!latestVersion && !updateAvailable) {
    return;
  }

  const message = meta?.skill_update_message
    || `creator-scraper-cv has a newer version: current=${SKILL_META.version}, latest=${latestVersion || 'unknown'}`;

  console.error(JSON.stringify({
    skill_update: {
      required: updateRequired,
      current_version: SKILL_META.version,
      latest_version: latestVersion || null,
      min_supported_version: meta?.skill_min_supported_version || null,
      message,
      update_command: 'node scripts/skill_update.mjs --yes',
    },
  }, null, 2));

  if (process.env.CV_SKILL_AUTO_UPDATE === 'true') {
    const result = spawnSync(process.execPath, [join(SCRIPT_DIR, 'skill_update.mjs'), '--yes'], {
      encoding: 'utf8',
      stdio: 'inherit',
    });
    if (result.status !== 0) {
      console.error(JSON.stringify({
        skill_update_error: 'Auto update failed. Please run node scripts/skill_update.mjs --yes manually.',
        exit_code: result.status,
      }));
    }
  }
}

/**
 * Call Creativault Open API with auto-retry on 429.
 * @param {string} path
 * @param {object} body
 * @param {string | null} platform
 * @param {object} options
 * @returns {Promise<object>}
 */
export async function callAPI(path, body = {}, platform = null, options = {}) {
  let processedBody = body;
  if (platform) {
    processedBody = await preprocessIndustryParams(platform, body);
  }
  if (!options.skipProfileBodyDefaults) {
    processedBody = applyDefaultServiceLevel(processedBody);
    processedBody = applyDefaultLang(processedBody);
  }

  const url = `${API_BASE}${path}`;
  let precheckDone = false;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    let creds;
    try {
      creds = await getCredentials();
    } catch (err) {
      const hint = RUNTIME_PROFILE.auth_mode === 'navos'
        ? 'Ensure Navos desktop is logged in (NAVOS_UID/NAVOS_TOKEN env or ~/.navos/identity/navos-userinfo.json).'
        : 'Set CV_API_KEY and CV_USER_IDENTITY for common profile usage.';
      console.error(JSON.stringify({
        error: 'Failed to resolve CV credentials',
        reason: err.message,
        profile: RUNTIME_PROFILE.profile,
        hint,
      }));
      process.exit(1);
    }

    if (!precheckDone) {
      precheckDone = true;
      await runBalancePrecheck(creds, options);
    }

    let response;
    try {
      if (!options.skipUserIdentity) {
        ensureUserIdentity(creds);
      }
      const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': creds.apiKey,
        'X-CV-Skill-Name': SKILL_META.name || 'creator-scraper-cv',
        'X-CV-Skill-Version': SKILL_META.version || 'unknown',
        'X-CV-Skill-Channel': SKILL_META.channel || 'unknown',
        'X-CV-Skill-Profile': RUNTIME_PROFILE.profile || 'common',
      };
      if (isNavosProfile(RUNTIME_PROFILE) && (creds.partnerCode || PARTNER_CODE)) {
        headers['X-Source'] = creds.partnerCode || PARTNER_CODE;
      }
      if (RUNTIME_PROFILE.navos_region) {
        headers['X-Navos-Region'] = String(RUNTIME_PROFILE.navos_region);
      }
      if (!options.skipUserIdentity) {
        headers['X-User-Identity'] = creds.userIdentity;
      }
      response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(processedBody),
      });
    } catch (err) {
      console.error(JSON.stringify({ error: `Network request failed: ${err.message}`, url }));
      process.exit(1);
    }

    if (response.status === 429 && attempt < MAX_RETRIES) {
      const retryAfter = parseInt(response.headers.get('Retry-After') || DEFAULT_RETRY_AFTER, 10);
      console.error(`[retry] Rate limited (429). Waiting ${retryAfter}s before retry ${attempt + 1}/${MAX_RETRIES}...`);
      await sleep(retryAfter * 1000);
      continue;
    }

    let data;
    try {
      data = await response.json();
    } catch {
      console.error(JSON.stringify({ error: `Failed to parse response, HTTP status: ${response.status}`, url }));
      process.exit(1);
    }

    if (!data.success) {
      const errorOutput = buildErrorOutput(data);
      // 失败原因必须同时出现在 stdout。只写 stderr 时，按非 0 退出码判定「脚本执行失败」
      // 的宿主会丢弃输出，调用方拿不到 error.message，用户只看到一句「失败」而不知原因。
      // stderr 保留原样，便于终端排查和日志采集。
      console.log(JSON.stringify({ success: false, ...errorOutput }, null, 2));
      console.error(JSON.stringify(errorOutput, null, 2));
      process.exit(1);
    }

    if (RUNTIME_PROFILE.balance_precheck && creds?.uid) {
      invalidateNavosBalanceCache(creds.uid);
    }
    maybeHandleSkillUpdateMeta(data.meta);
    return stripHiddenMeta(data);
  }

  console.error(JSON.stringify({ error: `Rate limit: max retries (${MAX_RETRIES}) exhausted`, url }));
  process.exit(1);
}

function isIdentifierStart(ch) {
  return /[A-Za-z_]/.test(ch || '');
}

function isIdentifierChar(ch) {
  return /[A-Za-z0-9_]/.test(ch || '');
}

function stripMatchingQuotes(value) {
  const trimmed = value.trim();
  if (trimmed.length < 2) return trimmed;
  const first = trimmed[0];
  const last = trimmed[trimmed.length - 1];
  if ((first === '"' && last === '"') || (first === "'" && last === "'")) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function hasMatchingQuotes(value) {
  const trimmed = value.trim();
  if (trimmed.length < 2) return false;
  const first = trimmed[0];
  const last = trimmed[trimmed.length - 1];
  return (first === '"' && last === '"') || (first === "'" && last === "'");
}

function findQuotedEnd(source, start) {
  const quote = source[start];
  let escaped = false;
  for (let index = start + 1; index < source.length; index++) {
    const ch = source[index];
    if (escaped) {
      escaped = false;
      continue;
    }
    if (ch === '\\') {
      escaped = true;
      continue;
    }
    if (ch === quote) return index;
  }
  return -1;
}

function readLooseKey(source, start) {
  let index = start;
  while (/\s/.test(source[index] || '')) index++;

  const quote = source[index];
  if (quote === '"' || quote === "'") {
    const end = findQuotedEnd(source, index);
    if (end < 0) return null;
    return { key: source.slice(index + 1, end), next: end + 1 };
  }

  if (!isIdentifierStart(source[index])) return null;
  const keyStart = index;
  index++;
  while (isIdentifierChar(source[index])) index++;
  return { key: source.slice(keyStart, index), next: index };
}

function looksLikeNextField(source, start) {
  const key = readLooseKey(source, start);
  if (!key) return false;
  let index = key.next;
  while (/\s/.test(source[index] || '')) index++;
  return source[index] === ':';
}

function findNextFieldBoundary(source, start) {
  let quote = null;
  let escaped = false;
  let depth = 0;

  for (let index = start; index < source.length; index++) {
    const ch = source[index];
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === '\\') {
        escaped = true;
      } else if (ch === quote) {
        quote = null;
      }
      continue;
    }

    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (ch === '[' || ch === '{') {
      depth++;
      continue;
    }
    if ((ch === ']' || ch === '}') && depth > 0) {
      depth--;
      continue;
    }
    if (ch === ',' && depth === 0 && looksLikeNextField(source, index + 1)) {
      return index;
    }
  }

  return source.length;
}

function splitLooseArrayItems(source) {
  const items = [];
  let quote = null;
  let escaped = false;
  let depth = 0;
  let start = 0;

  for (let index = 0; index < source.length; index++) {
    const ch = source[index];
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === '\\') {
        escaped = true;
      } else if (ch === quote) {
        quote = null;
      }
      continue;
    }

    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (ch === '[' || ch === '{') {
      depth++;
      continue;
    }
    if ((ch === ']' || ch === '}') && depth > 0) {
      depth--;
      continue;
    }
    if (ch === ',' && depth === 0) {
      items.push(source.slice(start, index));
      start = index + 1;
    }
  }

  items.push(source.slice(start));
  return items;
}

function parseLooseScalar(value) {
  const trimmed = value.trim();
  if (!trimmed) return '';
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    return splitLooseArrayItems(trimmed.slice(1, -1))
      .filter(item => item.trim() !== '')
      .map(parseLooseScalar);
  }

  if (hasMatchingQuotes(trimmed)) return stripMatchingQuotes(trimmed);
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  if (trimmed === 'null') return null;
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) return Number(trimmed);
  return trimmed;
}

function parseLooseObjectArg(raw) {
  const source = raw.trim();
  if (!source.startsWith('{') || !source.endsWith('}')) return null;

  const body = source.slice(1, -1).trim();
  if (!body) return {};

  const result = {};
  let index = 0;

  while (index < body.length) {
    while (/[\s,]/.test(body[index] || '')) index++;
    if (index >= body.length) break;

    const key = readLooseKey(body, index);
    if (!key) return null;

    index = key.next;
    while (/\s/.test(body[index] || '')) index++;
    if (body[index] !== ':') return null;

    index++;
    const boundary = findNextFieldBoundary(body, index);
    result[key.key] = parseLooseScalar(body.slice(index, boundary));
    index = boundary < body.length ? boundary + 1 : body.length;
  }

  return result;
}

/**
 * Parse command-line JSON argument.
 * @returns {object}
 */
export function parseArgs() {
  const raw = process.argv[2];
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    const loose = parseLooseObjectArg(raw);
    if (loose) return loose;

    console.error(JSON.stringify({
      error: 'Argument must be a valid JSON string',
      received: raw,
      hint: 'Pass JSON with quoted keys and string values. A loose object fallback is supported only for Navos/PowerShell argument escaping issues.',
    }));
    process.exit(1);
  }
}

/**
 * Validate required parameters.
 * @param {object} params
 * @param {string[]} required
 */
export function validateRequired(params, required) {
  const missing = required.filter(key => params[key] === undefined || params[key] === null);
  if (missing.length > 0) {
    console.error(JSON.stringify({ error: `Missing required parameters: ${missing.join(', ')}` }));
    process.exit(1);
  }
}

const VALID_PLATFORMS = ['tiktok', 'youtube', 'instagram'];

/**
 * Validate platform parameter.
 * @param {string} platform
 */
export function validatePlatform(platform) {
  if (!platform || !VALID_PLATFORMS.includes(platform)) {
    console.error(JSON.stringify({ error: `platform must be one of: ${VALID_PLATFORMS.join(' / ')}`, received: platform }));
    process.exit(1);
  }
}

/**
 * Preprocess industry category parameters based on platform.
 * @param {string} platform
 * @param {object} params
 * @returns {Promise<object>}
 */
export async function preprocessIndustryParams(platform, params) {
  const { convertToLeafIds, suggestIndustryMatches } = await import('./_industry_mapper.mjs');
  const processed = { ...params };

  if (processed.industry) {
    const input = processed.industry;
    const leafIds = convertToLeafIds(input);
    if (leafIds.length > 0) {
      processed.industry = leafIds.join(',');
    } else {
      const suggestions = suggestIndustryMatches(input);
      console.error(JSON.stringify({
        error: `Unknown or invalid industry category: "${input}". Every value must be a known category ID or supported name.`,
        hint: 'Use one exact category, a known alias, or choose from the suggested categories below. If the user intent is ambiguous, ask for confirmation before searching.',
        suggestions,
        reference: 'See references/industry-categories.md for full list',
      }));
      process.exit(1);
    }
  }

  return processed;
}
