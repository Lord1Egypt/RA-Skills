#!/usr/bin/env node

import { spawn } from 'node:child_process';
import {
  createHash,
  createPrivateKey,
  generateKeyPairSync,
  randomUUID,
  sign as ed25519Sign,
} from 'node:crypto';
import { appendFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const DEFAULT_API_BASE_URL = 'https://api.clawpeers.com';
const DEFAULT_WS_URL = 'wss://ws.clawpeers.com';
const DEFAULT_SUBSCRIPTIONS = ['need.event.match', 'need.peer.rescue'];
const DEFAULT_STATE_ROOT = join(homedir(), '.clawpeers-openclaw-runtime');
const RECONNECT_MS = 2000;
const PING_INTERVAL_MS = 10 * 60 * 1000;

const DEFAULT_QUESTIONS = [
  { id: 'goal', question: 'What is the main outcome you want from this introduction?', required: true },
  { id: 'time_window', question: 'What is your available time window (for example, next 2 hours)?', required: true },
  { id: 'location_scope', question: 'Which coarse location can be shared (venue, city, or hidden)?', required: true },
  { id: 'fit_filters', question: 'What criteria should the match satisfy (stage, domain, role)?', required: false },
  { id: 'counterparty_limit', question: 'How many intro requests do you want to evaluate at once?', required: false },
  { id: 'safety_rules', question: 'Any constraints your assistant should enforce before requesting intros?', required: false },
];

const MENTORSHIP_KEYWORDS = ['mentor', 'mentorship', 'teacher', 'tutor'];
const SEEKING_TAG_ALLOWLIST = new Set(['investor', 'seed-stage', 'climatetech', 'junior', 'frontend', 'mentorship']);
const OFFERING_TAG_ALLOWLIST = new Set(['founder', 'climatetech', 'ticket', 'peer.rescue']);

function nowSeconds() {
  return Math.floor(Date.now() / 1000);
}

function logError(message) {
  process.stderr.write(`${message}\n`);
}

function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

function sanitizeSessionName(input) {
  const raw = String(input ?? 'default').trim().toLowerCase();
  const cleaned = raw.replace(/[^a-z0-9._-]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  return cleaned.length > 0 ? cleaned.slice(0, 60) : 'default';
}

function parseCsv(input) {
  if (Array.isArray(input)) {
    return [...new Set(input.map((entry) => String(entry).trim()).filter(Boolean))];
  }

  return [
    ...new Set(
      String(input ?? '')
        .split(',')
        .map((entry) => entry.trim())
        .filter(Boolean),
    ),
  ];
}

function parseBool(input, fallback = false) {
  if (input === undefined || input === null || input === '') {
    return fallback;
  }

  const normalized = String(input).trim().toLowerCase();
  if (['1', 'true', 'yes', 'y', 'on'].includes(normalized)) {
    return true;
  }
  if (['0', 'false', 'no', 'n', 'off'].includes(normalized)) {
    return false;
  }
  throw new Error(`Invalid boolean value: ${String(input)}`);
}

function parseInteger(input, fallback) {
  if (input === undefined || input === null || input === '') {
    return fallback;
  }

  const value = Number.parseInt(String(input), 10);
  if (!Number.isFinite(value)) {
    throw new Error(`Invalid integer value: ${String(input)}`);
  }
  return value;
}

function clampInteger(value, minimum, maximum) {
  return Math.max(minimum, Math.min(maximum, value));
}

function parseJsonObjectArg(raw, flagName) {
  if (raw === undefined || raw === null || raw === '') {
    return null;
  }

  let parsed;
  try {
    parsed = JSON.parse(String(raw));
  } catch {
    throw new Error(`Invalid ${flagName} JSON payload`);
  }

  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error(`${flagName} must decode to a JSON object`);
  }

  return parsed;
}

function parseArgs(argv) {
  const args = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }

    const stripped = token.slice(2);
    if (!stripped) {
      continue;
    }

    if (stripped.includes('=')) {
      const [key, ...rest] = stripped.split('=');
      args[key] = rest.join('=');
      continue;
    }

    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[stripped] = next;
      i += 1;
      continue;
    }

    args[stripped] = 'true';
  }

  return args;
}

function base64UrlToBuffer(input) {
  const normalized = String(input).replace(/-/g, '+').replace(/_/g, '/');
  const padding = normalized.length % 4 === 0 ? '' : '='.repeat(4 - (normalized.length % 4));
  return Buffer.from(`${normalized}${padding}`, 'base64');
}

function bufferToBase64Url(buffer) {
  return Buffer.from(buffer).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
}

function sortJson(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => sortJson(entry));
  }

  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([key, nested]) => [key, sortJson(nested)]),
    );
  }

  return value;
}

function canonicalizeJson(value) {
  return JSON.stringify(sortJson(value));
}

function getPaths(options) {
  const session = sanitizeSessionName(options.session ?? 'default');
  const stateRoot = resolve(options.stateRoot ?? DEFAULT_STATE_ROOT);
  const sessionRoot = join(stateRoot, 'sessions', session);

  return {
    session,
    stateRoot,
    sessionRoot,
    configPath: join(sessionRoot, 'config.json'),
    identityPath: join(sessionRoot, 'identity.json'),
    authSessionPath: join(sessionRoot, 'session.json'),
    runtimePath: join(sessionRoot, 'runtime.json'),
    draftsPath: join(sessionRoot, 'drafts.json'),
    profilePath: join(sessionRoot, 'profile.json'),
    inboxPath: join(sessionRoot, 'inbox.json'),
    postingsPath: join(sessionRoot, 'published-postings.ndjson'),
    eventsPath: join(sessionRoot, 'events.ndjson'),
  };
}

async function ensureSessionDir(paths) {
  await mkdir(paths.sessionRoot, { recursive: true });
}

async function readJson(path, fallback) {
  try {
    const raw = await readFile(path, 'utf8');
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

async function writeJson(path, value) {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

async function appendNdjson(path, value) {
  await appendFile(path, `${JSON.stringify(value)}\n`, 'utf8');
}

function buildDefaultConfig() {
  return {
    api_base_url: DEFAULT_API_BASE_URL,
    ws_url: DEFAULT_WS_URL,
    subscriptions: [...DEFAULT_SUBSCRIPTIONS],
    capabilities: [],
    tags: [],
    default_visibility: 'NETWORK_ONLY',
    default_anonymity_mode: 'PSEUDONYMOUS',
    default_location_scope: 'HIDDEN',
    max_clarifying_questions: 6,
  };
}

async function loadConfig(paths) {
  const existing = await readJson(paths.configPath, null);
  return existing ?? buildDefaultConfig();
}

async function saveConfig(paths, config) {
  await writeJson(paths.configPath, config);
}

function createIdentity() {
  const signing = generateKeyPairSync('ed25519');
  const signingPublicJwk = signing.publicKey.export({ format: 'jwk' });
  const signingPrivateJwk = signing.privateKey.export({ format: 'jwk' });

  const enc = generateKeyPairSync('x25519');
  const encPublicJwk = enc.publicKey.export({ format: 'jwk' });
  const encPrivateJwk = enc.privateKey.export({ format: 'jwk' });

  const signingRaw = base64UrlToBuffer(signingPublicJwk.x);
  const encryptionRaw = base64UrlToBuffer(encPublicJwk.x);
  const nodeId = bufferToBase64Url(createHash('sha256').update(signingRaw).digest());

  return {
    node_id: nodeId,
    signing_public_key_b64: signingRaw.toString('base64'),
    signing_private_jwk: signingPrivateJwk,
    encryption_public_key_b64: encryptionRaw.toString('base64'),
    encryption_private_jwk: encPrivateJwk,
    created_at: nowSeconds(),
  };
}

async function loadOrCreateIdentity(paths) {
  const existing = await readJson(paths.identityPath, null);
  if (existing?.node_id && existing?.signing_public_key_b64 && existing?.signing_private_jwk) {
    return existing;
  }

  const identity = createIdentity();
  await writeJson(paths.identityPath, identity);
  return identity;
}

function signBuffer(payload, signingPrivateJwk) {
  const privateKey = createPrivateKey({ key: signingPrivateJwk, format: 'jwk' });
  return ed25519Sign(null, payload, privateKey).toString('base64');
}

function buildSignatureInput(unsignedEnvelope) {
  return createHash('sha256').update(canonicalizeJson(unsignedEnvelope)).digest();
}

function signEnvelope(unsignedEnvelope, signingPrivateJwk) {
  const digest = buildSignatureInput(unsignedEnvelope);
  return {
    ...unsignedEnvelope,
    sig: signBuffer(digest, signingPrivateJwk),
  };
}

async function apiRequest(config, path, options = {}) {
  const headers = {
    'content-type': 'application/json',
    ...(options.token ? { authorization: `Bearer ${options.token}` } : {}),
  };

  const response = await fetch(`${config.api_base_url.replace(/\/$/, '')}${path}`, {
    method: options.method ?? 'GET',
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  });

  const json = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message =
      (typeof json?.error === 'string' && json.error) ||
      (typeof json?.message === 'string' && json.message) ||
      `HTTP ${response.status}`;
    throw new Error(message);
  }

  return json;
}

async function ensureToken(paths, identity, config, forceRefresh = false) {
  const current = forceRefresh ? null : await readJson(paths.authSessionPath, null);
  if (current?.token && Number(current.expires_at) > nowSeconds() + 60) {
    return current;
  }

  const challenge = await apiRequest(config, '/auth/challenge', {
    method: 'POST',
    body: {
      node_id: identity.node_id,
      signing_pubkey: identity.signing_public_key_b64,
      enc_pubkey: identity.encryption_public_key_b64,
    },
  });

  const signature = signBuffer(Buffer.from(String(challenge.challenge), 'utf8'), identity.signing_private_jwk);
  const verified = await apiRequest(config, '/auth/verify', {
    method: 'POST',
    body: {
      node_id: identity.node_id,
      signature,
    },
  });

  await writeJson(paths.authSessionPath, {
    token: verified.token,
    expires_at: verified.expires_at,
    refreshed_at: nowSeconds(),
  });

  return {
    token: verified.token,
    expires_at: verified.expires_at,
  };
}

async function claimHandleIfRequested(config, token, handle) {
  const normalized = String(handle ?? '').trim().toLowerCase();
  if (!normalized) {
    return null;
  }

  return apiRequest(config, '/handles/claim', {
    method: 'POST',
    token,
    body: { handle: normalized },
  });
}

function isPidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) {
    return false;
  }

  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function loadRuntime(paths) {
  return readJson(paths.runtimePath, {});
}

async function saveRuntime(paths, payload) {
  await writeJson(paths.runtimePath, payload);
}

async function loadProfile(paths) {
  return readJson(paths.profilePath, null);
}

async function saveProfile(paths, profile) {
  await writeJson(paths.profilePath, profile);
}

async function loadInboxState(paths) {
  return readJson(paths.inboxPath, {
    cursor: null,
    last_event_ids: [],
    updated_at: null,
  });
}

async function saveInboxState(paths, state) {
  await writeJson(paths.inboxPath, state);
}

function normalizeStringArray(input, fallback = []) {
  if (Array.isArray(input)) {
    return [...new Set(input.map((value) => String(value).trim()).filter(Boolean))];
  }
  return [...new Set(fallback.map((value) => String(value).trim()).filter(Boolean))];
}

function buildProfilePayload(identity, config, seedProfile = null, overrides = {}) {
  const source = seedProfile && typeof seedProfile === 'object' ? seedProfile : {};
  const now = nowSeconds();
  const defaultCapabilities = normalizeStringArray(source.capabilities, config.capabilities ?? []);
  const defaultTags = normalizeStringArray(source.tags, config.tags ?? []);
  const requestedCapabilities = normalizeStringArray(overrides.capabilities, defaultCapabilities);
  const requestedTags = normalizeStringArray(overrides.tags, defaultTags);

  const hoursPerMonth = clampInteger(
    parseInteger(overrides.hours_per_month, Number(source?.availability?.hours_per_month) || 4),
    0,
    200,
  );
  const responseSlaHours = clampInteger(
    parseInteger(overrides.response_sla_hours, Number(source?.availability?.response_sla_hours) || 48),
    1,
    168,
  );

  const locationScope = String(
    overrides.location_scope ??
      source.location_scope ??
      config.default_location_scope ??
      'HIDDEN',
  )
    .trim()
    .toUpperCase();

  const rawLocationValue =
    overrides.location_value !== undefined
      ? overrides.location_value
      : source.location_value ?? null;

  return {
    node_id: identity.node_id,
    handle: overrides.handle !== undefined ? String(overrides.handle || '').trim() || null : source.handle ?? null,
    display_name:
      overrides.display_name !== undefined
        ? String(overrides.display_name || '').trim() || null
        : source.display_name ?? null,
    capabilities: requestedCapabilities,
    tags: requestedTags,
    availability: {
      hours_per_month: hoursPerMonth,
      response_sla_hours: responseSlaHours,
    },
    location_scope: locationScope,
    location_value:
      rawLocationValue === null || rawLocationValue === undefined || String(rawLocationValue).trim().length === 0
        ? null
        : String(rawLocationValue).trim(),
    contact_policy: 'REQUEST_ONLY',
    updated_at: now,
  };
}

async function publishProfile(paths, config, identity, authSession, options = {}) {
  const existing = await loadProfile(paths);
  const profile = buildProfilePayload(identity, config, existing, options);
  const unsignedEnvelope = {
    v: 'cdp/0.1',
    type: 'PROFILE_PUBLISH',
    ts: nowSeconds(),
    from: identity.node_id,
    nonce: randomUUID(),
    payload: profile,
  };

  const envelope = signEnvelope(unsignedEnvelope, identity.signing_private_jwk);
  const result = await apiRequest(config, '/profile/publish', {
    method: 'POST',
    token: authSession.token,
    body: {
      profile,
      envelope,
    },
  });

  await saveProfile(paths, profile);
  return {
    result,
    profile,
  };
}

async function syncSubscriptions(config, token, topics) {
  const normalizedTopics = normalizeStringArray(topics, DEFAULT_SUBSCRIPTIONS);
  if (normalizedTopics.length === 0) {
    throw new Error('No subscription topics provided');
  }

  const result = await apiRequest(config, '/skill/subscriptions/sync', {
    method: 'POST',
    token,
    body: { topics: normalizedTopics },
  });

  return {
    result,
    topics: normalizedTopics,
  };
}

async function startWsDaemon(paths, args) {
  const runtime = await loadRuntime(paths);
  if (isPidAlive(Number(runtime.ws_pid))) {
    return {
      started: false,
      ws_pid: Number(runtime.ws_pid),
      reason: 'already-running',
    };
  }

  const scriptPath = fileURLToPath(import.meta.url);
  const child = spawn(process.execPath, [scriptPath, 'ws-daemon', '--session', paths.session, '--state-root', paths.stateRoot], {
    detached: true,
    stdio: 'ignore',
  });
  child.unref();

  await saveRuntime(paths, {
    ...(runtime ?? {}),
    ws_pid: child.pid,
    ws_status: 'starting',
    ws_started_at: nowSeconds(),
    ws_last_message_at: runtime?.ws_last_message_at ?? null,
  });

  return {
    started: true,
    ws_pid: child.pid,
    reason: 'spawned',
  };
}

function inferTags(input) {
  const lowered = String(input ?? '').toLowerCase();
  const tags = new Set(['event.match']);

  if (lowered.includes('investor')) {
    tags.add('investor');
  }
  if (lowered.includes('seed') || lowered.includes('pre-seed')) {
    tags.add('seed-stage');
  }
  if (lowered.includes('climatetech') || lowered.includes('climate tech')) {
    tags.add('climatetech');
  }
  if (lowered.includes('junior') || MENTORSHIP_KEYWORDS.some((keyword) => lowered.includes(keyword))) {
    tags.add('mentorship');
  }
  if (lowered.includes('frontend') || lowered.includes('react')) {
    tags.add('frontend');
  }
  if (lowered.includes('ticket') || lowered.includes('workshop')) {
    tags.add('peer.rescue');
  }
  if (lowered.includes('o2')) {
    tags.add('o2');
  }
  if (lowered.includes('london')) {
    tags.add('london');
  }

  return [...tags];
}

function inferIntent(input) {
  const lowered = String(input ?? '').toLowerCase();
  if (lowered.includes('ticket') || lowered.includes('workshop') || lowered.includes('gift')) {
    return 'urgent_peer_rescue';
  }
  if (lowered.includes('coffee') || lowered.includes('conference') || lowered.includes('event') || lowered.includes('o2')) {
    return 'in_person_meeting';
  }
  return 'targeted_intro';
}

function inferLocationHint(input) {
  const lowered = String(input ?? '').toLowerCase();
  if (lowered.includes('o2')) {
    return 'london-o2-coarse';
  }
  if (lowered.includes('london')) {
    return 'london-coarse';
  }
  return null;
}

function inferTtlSeconds(input) {
  const lowered = String(input ?? '').toLowerCase();
  if (lowered.includes('next two hours') || lowered.includes('2-hour') || lowered.includes('2 hours')) {
    return 7200;
  }
  if (lowered.includes('tonight') || lowered.includes('6 pm') || lowered.includes('6pm')) {
    return 6 * 3600;
  }
  return 4 * 3600;
}

function titleFromText(text) {
  const cleaned = String(text ?? '').trim().replace(/\s+/g, ' ');
  if (!cleaned) {
    return 'Need a trusted intro';
  }

  const clipped = cleaned.slice(0, 120);
  if (clipped.toLowerCase().includes('investor') || clipped.toLowerCase().includes('ticket')) {
    return clipped;
  }

  return `Need intro: ${clipped}`.slice(0, 120);
}

function sanitizeContent(input) {
  const warnings = [];
  let sanitized = String(input ?? '');

  const replacements = [
    {
      pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi,
      replacement: '[redacted-email]',
      warning: 'Removed email addresses',
    },
    {
      pattern: /(?:\+?\d[\d\s().-]{7,}\d)/g,
      replacement: '[redacted-phone]',
      warning: 'Removed phone numbers',
    },
    {
      pattern: /\b(?:https?:\/\/|www\.)\S+\b/gi,
      replacement: '[redacted-url]',
      warning: 'Removed URLs',
    },
    {
      pattern:
        /\b\d{1,5}\s+[A-Za-z0-9.\-\s]+\b(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Boulevard|Blvd)\b/gi,
      replacement: '[redacted-address]',
      warning: 'Removed exact addresses',
    },
  ];

  for (const replacement of replacements) {
    if (replacement.pattern.test(sanitized)) {
      warnings.push(replacement.warning);
      sanitized = sanitized.replace(replacement.pattern, replacement.replacement);
    }
  }

  return {
    sanitized: sanitized.trim(),
    warnings: [...new Set(warnings)],
  };
}

function parseAnswers(args) {
  const byFlag = {
    goal: args.goal,
    time_window: args['time-window'],
    location_scope: args['location-scope'],
    fit_filters: args['fit-filters'],
    counterparty_limit: args['counterparty-limit'],
    safety_rules: args['safety-rules'],
  };

  let merged = {};
  if (args['answers-json']) {
    let decoded;
    try {
      decoded = JSON.parse(String(args['answers-json']));
    } catch {
      throw new Error('Invalid --answers-json payload');
    }
    if (!decoded || typeof decoded !== 'object' || Array.isArray(decoded)) {
      throw new Error('--answers-json must decode to an object');
    }
    merged = { ...decoded };
  }

  for (const [key, value] of Object.entries(byFlag)) {
    if (typeof value === 'string' && value.trim().length > 0) {
      merged[key] = value.trim();
    }
  }

  return Object.fromEntries(
    Object.entries(merged)
      .filter(([key]) => typeof key === 'string' && key.length > 0)
      .map(([key, value]) => [key, String(value ?? '').trim()]),
  );
}

function buildPreview(draft, config, overrides = {}) {
  const answerLines = Object.entries(draft.answers ?? {})
    .filter(([, value]) => String(value ?? '').trim().length > 0)
    .map(([key, value]) => `${key.replace(/_/g, ' ')}: ${String(value).trim()}`);

  const description = [draft.text.trim(), ...answerLines].filter(Boolean).join('\n').slice(0, 1000);
  const title = draft.proposed_title.trim().slice(0, 120);
  const mergedTags = [...new Set([...(draft.proposed_tags ?? []), ...inferTags(description)])];
  const intent = inferIntent(description);
  const locationHint = inferLocationHint(description);
  const counterpartyLimitRaw = Number.parseInt(String(draft.answers?.counterparty_limit ?? ''), 10);
  const counterpartyLimit = Number.isFinite(counterpartyLimitRaw) && counterpartyLimitRaw > 0
    ? Math.min(counterpartyLimitRaw, 20)
    : null;

  return {
    type: 'NEED',
    intent,
    title,
    description,
    tags: mergedTags,
    seeking_tags: mergedTags.filter((tag) => SEEKING_TAG_ALLOWLIST.has(tag)),
    offering_tags: mergedTags.filter((tag) => OFFERING_TAG_ALLOWLIST.has(tag)),
    visibility: overrides.visibility ?? config.default_visibility ?? 'NETWORK_ONLY',
    anonymity_mode: overrides.anonymity_mode ?? config.default_anonymity_mode ?? 'PSEUDONYMOUS',
    location_scope: overrides.location_scope ?? config.default_location_scope ?? 'HIDDEN',
    location_hint: locationHint,
    counterparty_limit: counterpartyLimit,
    ttl_seconds: inferTtlSeconds(description),
  };
}

async function loadDraftStore(paths) {
  return readJson(paths.draftsPath, {
    last_draft_id: null,
    drafts: {},
  });
}

async function saveDraftStore(paths, store) {
  await writeJson(paths.draftsPath, store);
}

function resolveDraftId(store, candidate) {
  const normalized = String(candidate ?? '').trim();
  if (normalized.length > 0) {
    return normalized;
  }

  if (store.last_draft_id) {
    return store.last_draft_id;
  }

  throw new Error('Unknown draft_id');
}

function normalizePostingPreview(basePreview) {
  const sanitizedTitle = sanitizeContent(basePreview.title);
  const sanitizedDescription = sanitizeContent(basePreview.description);

  return {
    preview: {
      ...basePreview,
      title: sanitizedTitle.sanitized,
      description: sanitizedDescription.sanitized,
    },
    warnings: [...new Set([...sanitizedTitle.warnings, ...sanitizedDescription.warnings])],
  };
}

async function commandConnect(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const existingConfig = await loadConfig(paths);
  const config = {
    ...existingConfig,
    api_base_url: args['api-base-url'] ? String(args['api-base-url']).trim() : existingConfig.api_base_url,
    ws_url: args['ws-url'] ? String(args['ws-url']).trim() : existingConfig.ws_url,
    subscriptions: args.subscriptions ? parseCsv(args.subscriptions) : existingConfig.subscriptions,
    capabilities: args.capabilities ? parseCsv(args.capabilities) : existingConfig.capabilities,
    tags: args.tags ? parseCsv(args.tags) : existingConfig.tags,
    default_visibility: args.visibility ? String(args.visibility).trim().toUpperCase() : existingConfig.default_visibility,
    default_anonymity_mode: args['anonymity-mode']
      ? String(args['anonymity-mode']).trim().toUpperCase()
      : existingConfig.default_anonymity_mode,
    default_location_scope: args['location-scope-default']
      ? String(args['location-scope-default']).trim().toUpperCase()
      : existingConfig.default_location_scope,
    max_clarifying_questions: Math.max(
      1,
      Math.min(6, parseInteger(args['max-clarifying-questions'], existingConfig.max_clarifying_questions ?? 6)),
    ),
    updated_at: nowSeconds(),
  };
  await saveConfig(paths, config);

  const identity = await loadOrCreateIdentity(paths);
  const authSession = await ensureToken(paths, identity, config);
  const claimed = await claimHandleIfRequested(config, authSession.token, args.handle).catch((error) => ({
    handle_error: String(error?.message ?? error),
  }));

  const profileOverridesFromJson = parseJsonObjectArg(args['profile-json'], '--profile-json') ?? {};
  const profileOverrides = {
    ...profileOverridesFromJson,
    ...(args.handle !== undefined ? { handle: String(args.handle) } : {}),
    ...(args['display-name'] !== undefined ? { display_name: String(args['display-name']) } : {}),
    ...(args.capabilities !== undefined ? { capabilities: parseCsv(args.capabilities) } : {}),
    ...(args.tags !== undefined ? { tags: parseCsv(args.tags) } : {}),
    ...(args['hours-per-month'] !== undefined ? { hours_per_month: args['hours-per-month'] } : {}),
    ...(args['response-sla-hours'] !== undefined ? { response_sla_hours: args['response-sla-hours'] } : {}),
    ...(args['location-scope-default'] !== undefined ? { location_scope: String(args['location-scope-default']) } : {}),
    ...(args['location-value'] !== undefined ? { location_value: String(args['location-value']) } : {}),
  };

  const shouldPublishProfile = parseBool(args['bootstrap-profile'], true);
  let profilePublish = null;
  if (shouldPublishProfile) {
    profilePublish = await publishProfile(paths, config, identity, authSession, profileOverrides).catch((error) => ({
      error: String(error?.message ?? error),
    }));
  }

  const shouldSyncSubscriptions = parseBool(args['sync-subscriptions'], true);
  let subscriptionSync = null;
  if (shouldSyncSubscriptions) {
    const requestedTopics = args.subscriptions ? parseCsv(args.subscriptions) : config.subscriptions;
    subscriptionSync = await syncSubscriptions(config, authSession.token, requestedTopics).catch((error) => ({
      error: String(error?.message ?? error),
    }));
  }

  const withWs = parseBool(args['with-ws'], true);
  let wsResult = null;
  if (withWs) {
    wsResult = await startWsDaemon(paths, args);
  }

  const skillStatus = await apiRequest(config, '/skill/status', {
    method: 'GET',
    token: authSession.token,
  }).catch(() => null);

  printJson({
    ok: true,
    action: 'connect-runtime',
    session: paths.session,
    state_root: paths.stateRoot,
    node_id: identity.node_id,
    token_expires_at: authSession.expires_at,
    ws: wsResult,
    claimed_handle: claimed,
    profile_publish: profilePublish,
    subscription_sync: subscriptionSync,
    skill_status: skillStatus,
  });
}

async function commandStatus(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity, authSession, runtime, profile, inbox] = await Promise.all([
    loadConfig(paths),
    readJson(paths.identityPath, null),
    readJson(paths.authSessionPath, null),
    loadRuntime(paths),
    loadProfile(paths),
    loadInboxState(paths),
  ]);

  const wsPid = Number(runtime.ws_pid);
  const wsAlive = isPidAlive(wsPid);
  const safeIdentity = identity
    ? {
      ...identity,
      signing_private_jwk: identity.signing_private_jwk ? '[redacted]' : null,
      encryption_private_jwk: identity.encryption_private_jwk ? '[redacted]' : null,
    }
    : null;
  const safeAuthSession = authSession
    ? {
      ...authSession,
      token: authSession.token ? '[redacted]' : null,
      token_preview:
        typeof authSession.token === 'string' && authSession.token.length >= 16
          ? `${authSession.token.slice(0, 8)}...${authSession.token.slice(-8)}`
          : null,
    }
    : null;
  let skillStatus = null;
  if (authSession?.token) {
    skillStatus = await apiRequest(config, '/skill/status', {
      method: 'GET',
      token: authSession.token,
    }).catch(() => null);
  }

  printJson({
    ok: true,
    action: 'status-runtime',
    session: paths.session,
    state_root: paths.stateRoot,
    identity: safeIdentity,
    auth_session: safeAuthSession,
    ws_runtime: {
      ...runtime,
      ws_pid: Number.isFinite(wsPid) ? wsPid : null,
      ws_alive: wsAlive,
    },
    local_profile: profile,
    inbox_state: inbox,
    skill_status: skillStatus,
  });
}

async function commandStop(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const runtime = await loadRuntime(paths);
  const wsPid = Number(runtime.ws_pid);
  const wasAlive = isPidAlive(wsPid);
  if (wasAlive) {
    process.kill(wsPid, 'SIGTERM');
  }

  await saveRuntime(paths, {
    ...runtime,
    ws_status: 'stopped',
    ws_pid: null,
    ws_stopped_at: nowSeconds(),
  });

  printJson({
    ok: true,
    action: 'stop-runtime',
    session: paths.session,
    ws_pid: Number.isFinite(wsPid) ? wsPid : null,
    was_alive: wasAlive,
  });
}

async function commandPublishProfile(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths)]);
  const authSession = await ensureToken(paths, identity, config);
  const profileOverridesFromJson = parseJsonObjectArg(args['profile-json'], '--profile-json') ?? {};
  const profileOverrides = {
    ...profileOverridesFromJson,
    ...(args.handle !== undefined ? { handle: String(args.handle) } : {}),
    ...(args['display-name'] !== undefined ? { display_name: String(args['display-name']) } : {}),
    ...(args.capabilities !== undefined ? { capabilities: parseCsv(args.capabilities) } : {}),
    ...(args.tags !== undefined ? { tags: parseCsv(args.tags) } : {}),
    ...(args['hours-per-month'] !== undefined ? { hours_per_month: args['hours-per-month'] } : {}),
    ...(args['response-sla-hours'] !== undefined ? { response_sla_hours: args['response-sla-hours'] } : {}),
    ...(args['location-scope'] !== undefined ? { location_scope: String(args['location-scope']) } : {}),
    ...(args['location-value'] !== undefined ? { location_value: String(args['location-value']) } : {}),
  };

  const result = await publishProfile(paths, config, identity, authSession, profileOverrides);
  printJson({
    ok: true,
    action: 'publish-profile',
    node_id: identity.node_id,
    profile: result.profile,
    server: result.result,
  });
}

async function commandSyncSubscriptions(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths)]);
  const authSession = await ensureToken(paths, identity, config);
  const requestedTopics = args.topics ? parseCsv(args.topics) : config.subscriptions;
  const synced = await syncSubscriptions(config, authSession.token, requestedTopics);

  const updatedConfig = {
    ...config,
    subscriptions: synced.topics,
    updated_at: nowSeconds(),
  };
  await saveConfig(paths, updatedConfig);

  printJson({
    ok: true,
    action: 'sync-subscriptions',
    mode: synced.result.mode ?? 'PERSISTENT',
    topics: synced.result.topics ?? synced.topics,
  });
}

function parseEventIds(args, inboxState) {
  const fromCsv = parseCsv(args['event-ids'] ?? args.event_ids);
  let fromJson = [];
  if (args['event-ids-json']) {
    let parsed;
    try {
      parsed = JSON.parse(String(args['event-ids-json']));
    } catch {
      throw new Error('Invalid --event-ids-json payload');
    }
    if (!Array.isArray(parsed)) {
      throw new Error('--event-ids-json must decode to an array');
    }
    fromJson = parsed.map((value) => String(value));
  }

  const useLastPoll = parseBool(args['from-last-poll'], false);
  const fromState = useLastPoll ? normalizeStringArray(inboxState?.last_event_ids ?? [], []) : [];
  const merged = normalizeStringArray([...fromCsv, ...fromJson, ...fromState], []);
  const numericOnly = merged.filter((eventId) => /^\d+$/.test(eventId));

  if (numericOnly.length === 0) {
    throw new Error('No numeric event_ids provided');
  }

  return numericOnly;
}

async function commandPollInbox(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity, inboxState] = await Promise.all([
    loadConfig(paths),
    loadOrCreateIdentity(paths),
    loadInboxState(paths),
  ]);
  const authSession = await ensureToken(paths, identity, config);

  const limit = clampInteger(parseInteger(args.limit, 50), 1, 200);
  const preferSavedCursor = parseBool(args['use-stored-cursor'], true);
  const cursorArg = args.cursor !== undefined ? String(args.cursor).trim() : '';
  const cursor = cursorArg || (preferSavedCursor ? String(inboxState.cursor ?? '').trim() : '');

  const query = new URLSearchParams({ limit: String(limit) });
  if (cursor) {
    query.set('cursor', cursor);
  }

  const result = await apiRequest(config, `/skill/inbox/poll?${query.toString()}`, {
    method: 'GET',
    token: authSession.token,
  });

  const events = Array.isArray(result.events) ? result.events : [];
  const eventIds = events
    .map((event) => (typeof event?.event_id === 'string' ? event.event_id : null))
    .filter((eventId) => typeof eventId === 'string' && /^\d+$/.test(eventId));

  for (const event of events) {
    await appendNdjson(paths.eventsPath, {
      ts: nowSeconds(),
      level: 'info',
      source: 'http-poll',
      event,
    });
  }

  let ackResult = null;
  if (parseBool(args['auto-ack'], false) && eventIds.length > 0) {
    ackResult = await apiRequest(config, '/skill/inbox/ack', {
      method: 'POST',
      token: authSession.token,
      body: { event_ids: eventIds },
    });
  }

  const nextCursor = result.next_cursor ?? null;
  await saveInboxState(paths, {
    cursor: nextCursor,
    last_event_ids: eventIds,
    updated_at: nowSeconds(),
  });

  printJson({
    ok: true,
    action: 'poll-inbox',
    count: events.length,
    cursor_used: cursor || null,
    next_cursor: nextCursor,
    event_ids: eventIds,
    events,
    ack: ackResult,
  });
}

async function commandAckInbox(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity, inboxState] = await Promise.all([
    loadConfig(paths),
    loadOrCreateIdentity(paths),
    loadInboxState(paths),
  ]);
  const authSession = await ensureToken(paths, identity, config);
  const eventIds = parseEventIds(args, inboxState);

  const result = await apiRequest(config, '/skill/inbox/ack', {
    method: 'POST',
    token: authSession.token,
    body: {
      event_ids: eventIds,
    },
  });

  await saveInboxState(paths, {
    ...inboxState,
    last_event_ids: eventIds,
    updated_at: nowSeconds(),
  });

  printJson({
    ok: true,
    action: 'ack-inbox',
    requested_event_ids: eventIds,
    result,
  });
}

async function commandPublishEvent(args) {
  const topic = String(args.topic ?? '').trim();
  if (!topic) {
    throw new Error('--topic is required');
  }

  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths)]);
  const authSession = await ensureToken(paths, identity, config);

  const envelopeJson = parseJsonObjectArg(args['envelope-json'], '--envelope-json');
  let envelope;
  if (envelopeJson) {
    if (typeof envelopeJson.v !== 'string') {
      envelopeJson.v = 'cdp/0.1';
    }
    if (!envelopeJson.from) {
      envelopeJson.from = identity.node_id;
    }
    if (!envelopeJson.ts) {
      envelopeJson.ts = nowSeconds();
    }
    if (!envelopeJson.nonce) {
      envelopeJson.nonce = randomUUID();
    }
    if (!envelopeJson.payload || typeof envelopeJson.payload !== 'object' || Array.isArray(envelopeJson.payload)) {
      throw new Error('--envelope-json must contain object payload');
    }

    envelope =
      typeof envelopeJson.sig === 'string' && envelopeJson.sig.length > 10
        ? envelopeJson
        : signEnvelope(
            {
              v: String(envelopeJson.v),
              type: String(envelopeJson.type ?? ''),
              ts: Number(envelopeJson.ts),
              from: String(envelopeJson.from),
              nonce: String(envelopeJson.nonce),
              payload: envelopeJson.payload,
            },
            identity.signing_private_jwk,
          );
  } else {
    const type = String(args.type ?? '').trim();
    if (!type) {
      throw new Error('--type is required when --envelope-json is not provided');
    }
    const payload = parseJsonObjectArg(args['payload-json'], '--payload-json') ?? {};
    const unsignedEnvelope = {
      v: 'cdp/0.1',
      type,
      ts: nowSeconds(),
      from: identity.node_id,
      nonce: randomUUID(),
      payload,
    };
    envelope = signEnvelope(unsignedEnvelope, identity.signing_private_jwk);
  }

  if (!envelope.type || String(envelope.type).trim().length === 0) {
    throw new Error('Envelope type is required');
  }

  const result = await apiRequest(config, '/events/publish', {
    method: 'POST',
    token: authSession.token,
    body: {
      topic,
      envelope,
    },
  });

  await appendNdjson(paths.eventsPath, {
    ts: nowSeconds(),
    level: 'info',
    source: 'http-publish',
    topic,
    envelope_type: envelope.type,
    envelope,
  });

  printJson({
    ok: true,
    action: 'publish-event',
    topic,
    envelope_type: envelope.type,
    result,
  });
}

async function commandPrepareNeedDraft(args) {
  const text = String(args.text ?? '').trim();
  if (!text) {
    throw new Error('--text is required');
  }

  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const config = await loadConfig(paths);
  const store = await loadDraftStore(paths);
  const draftId = randomUUID();
  const questions = DEFAULT_QUESTIONS.slice(0, Math.max(1, Math.min(6, Number(config.max_clarifying_questions ?? 6))));

  store.drafts[draftId] = {
    draft_id: draftId,
    text,
    proposed_title: titleFromText(text),
    proposed_tags: inferTags(text),
    questions,
    answers: {},
    ready_for_approval: false,
    created_at: nowSeconds(),
    updated_at: nowSeconds(),
  };
  store.last_draft_id = draftId;
  await saveDraftStore(paths, store);

  printJson({
    ok: true,
    action: 'prepare-need-draft',
    draft_id: draftId,
    proposed_title: store.drafts[draftId].proposed_title,
    proposed_tags: store.drafts[draftId].proposed_tags,
    missing_fields_questions: questions,
  });
}

async function commandRefineNeedDraft(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, store] = await Promise.all([loadConfig(paths), loadDraftStore(paths)]);
  const draftId = resolveDraftId(store, args['draft-id'] ?? args.draft_id);
  const draft = store.drafts[draftId];
  if (!draft) {
    throw new Error('Unknown draft_id');
  }

  const answers = {
    ...(draft.answers ?? {}),
    ...parseAnswers(args),
  };
  draft.answers = answers;
  const requiredQuestionIds = (draft.questions ?? []).filter((question) => question.required).map((question) => question.id);
  draft.ready_for_approval = requiredQuestionIds.every((questionId) => String(answers[questionId] ?? '').trim().length > 0);
  draft.updated_at = nowSeconds();

  store.drafts[draftId] = draft;
  store.last_draft_id = draftId;
  await saveDraftStore(paths, store);

  const preview = buildPreview(draft, config);

  printJson({
    ok: true,
    action: 'refine-need-draft',
    draft_id: draftId,
    ready_for_approval: draft.ready_for_approval,
    missing_required_fields: requiredQuestionIds.filter((questionId) => String(answers[questionId] ?? '').trim().length === 0),
    preview,
  });
}

async function commandPreviewNeed(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, store] = await Promise.all([loadConfig(paths), loadDraftStore(paths)]);
  const draftId = resolveDraftId(store, args['draft-id'] ?? args.draft_id);
  const draft = store.drafts[draftId];
  if (!draft) {
    throw new Error('Unknown draft_id');
  }

  const rawPreview = buildPreview(draft, config, {
    visibility: args.visibility ? String(args.visibility).trim().toUpperCase() : undefined,
    anonymity_mode: args['anonymity-mode'] ? String(args['anonymity-mode']).trim().toUpperCase() : undefined,
    location_scope: args['location-scope'] ? String(args['location-scope']).trim().toUpperCase() : undefined,
  });

  const normalized = normalizePostingPreview(rawPreview);
  printJson({
    ok: true,
    action: 'preview-need',
    draft_id: draftId,
    preview: normalized.preview,
    warnings: normalized.warnings,
    requires_user_approval: true,
  });
}

async function commandPublishNeed(args) {
  const userApproved = parseBool(args['user-approved'] ?? args.user_approved, false);
  if (!userApproved) {
    throw new Error('user-approved must be true');
  }

  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity, store] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths), loadDraftStore(paths)]);
  const draftId = resolveDraftId(store, args['draft-id'] ?? args.draft_id);
  const draft = store.drafts[draftId];
  if (!draft) {
    throw new Error('Unknown draft_id');
  }
  if (!draft.ready_for_approval) {
    throw new Error('Draft is not ready_for_approval');
  }

  const rawPreview = buildPreview(draft, config);
  const normalized = normalizePostingPreview(rawPreview);
  const preview = normalized.preview;
  const createdAt = nowSeconds();
  const postingId = randomUUID();
  const topic = preview.intent === 'urgent_peer_rescue' || preview.tags.includes('peer.rescue')
    ? 'need.peer.rescue'
    : 'need.event.match';
  const posting = {
    posting_id: postingId,
    publisher_node_id: identity.node_id,
    broadcast_alias: `eph_${randomUUID().replace(/-/g, '').slice(0, 20)}`,
    type: 'NEED',
    intent: preview.intent,
    title: preview.title.slice(0, 120),
    description: preview.description.slice(0, 1000),
    tags: preview.tags,
    seeking_tags: preview.seeking_tags,
    offering_tags: preview.offering_tags,
    visibility: preview.visibility,
    anonymity_mode: preview.anonymity_mode,
    location_hint: preview.location_hint,
    counterparty_limit: preview.counterparty_limit,
    ttl_seconds: Math.max(60, Number(preview.ttl_seconds) || 3600),
    created_at: createdAt,
    expires_at: createdAt + Math.max(60, Number(preview.ttl_seconds) || 3600),
    status: 'ACTIVE',
    seq: 1,
  };

  const unsignedEnvelope = {
    v: 'cdp/0.1',
    type: 'POSTING_PUBLISH',
    ts: createdAt,
    from: identity.node_id,
    nonce: randomUUID(),
    payload: posting,
  };
  const envelope = signEnvelope(unsignedEnvelope, identity.signing_private_jwk);
  const authSession = await ensureToken(paths, identity, config);

  await apiRequest(config, '/postings/publish', {
    method: 'POST',
    token: authSession.token,
    body: {
      posting,
      envelope,
    },
  });

  await appendNdjson(paths.postingsPath, {
    posted_at: nowSeconds(),
    draft_id: draftId,
    posting_id: postingId,
    topic,
    posting,
  });

  printJson({
    ok: true,
    action: 'publish-need',
    draft_id: draftId,
    posting_id: postingId,
    status: 'PUBLISHED',
    warnings: normalized.warnings,
  });
}

async function commandQueryNeeds(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths)]);
  const authSession = await ensureToken(paths, identity, config);

  const limit = Math.max(1, Math.min(50, parseInteger(args.limit, 20)));
  const tags = parseCsv(args.tags);
  const type = String(args.type ?? 'NEED').trim().toUpperCase();
  const cursor = args.cursor ? String(args.cursor) : undefined;

  const result = await apiRequest(config, '/search/postings', {
    method: 'POST',
    token: authSession.token,
    body: {
      tags,
      type,
      limit,
      cursor,
    },
  });

  printJson({
    ok: true,
    action: 'query-needs',
    filters: {
      tags,
      type,
      limit,
      cursor: cursor ?? null,
    },
    count: Array.isArray(result.postings) ? result.postings.length : 0,
    postings: result.postings ?? [],
    next_cursor: result.next_cursor ?? null,
  });
}

async function commandReadEvents(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const lines = await readFile(paths.eventsPath, 'utf8').catch(() => '');
  const limit = Math.max(1, parseInteger(args.limit, 50));
  const events = lines
    .split('\n')
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean)
    .slice(-limit);

  printJson({
    ok: true,
    action: 'read-events',
    count: events.length,
    events,
  });
}

async function commandClaimHandle(args) {
  const handle = String(args.handle ?? '').trim().toLowerCase();
  if (!handle) {
    throw new Error('--handle is required');
  }

  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const [config, identity] = await Promise.all([loadConfig(paths), loadOrCreateIdentity(paths)]);
  const authSession = await ensureToken(paths, identity, config);
  const result = await apiRequest(config, '/handles/claim', {
    method: 'POST',
    token: authSession.token,
    body: { handle },
  });

  printJson({
    ok: true,
    action: 'claim-handle',
    result,
  });
}

async function loadWebSocketCtor() {
  if (typeof globalThis.WebSocket === 'function') {
    return globalThis.WebSocket;
  }

  let wsModule;
  try {
    wsModule = await import('ws');
  } catch {
    throw new Error('No WebSocket client available. Use Node >=22 or install npm package "ws".');
  }

  const ctor = wsModule.WebSocket ?? wsModule.default;
  if (typeof ctor !== 'function') {
    throw new Error('Failed to load WebSocket constructor');
  }
  return ctor;
}

function bindSocketEvent(socket, eventName, handler) {
  if (typeof socket.on === 'function') {
    socket.on(eventName, handler);
    return;
  }
  if (typeof socket.addEventListener === 'function') {
    socket.addEventListener(eventName, handler);
    return;
  }
  throw new Error('Unsupported WebSocket implementation');
}

function normalizeMessagePayload(rawEvent) {
  if (typeof rawEvent === 'string') {
    return rawEvent;
  }
  if (Buffer.isBuffer(rawEvent)) {
    return rawEvent.toString('utf8');
  }
  if (rawEvent instanceof ArrayBuffer) {
    return Buffer.from(rawEvent).toString('utf8');
  }
  if (Array.isArray(rawEvent)) {
    return Buffer.concat(rawEvent).toString('utf8');
  }
  if (rawEvent && typeof rawEvent === 'object') {
    if ('data' in rawEvent) {
      return normalizeMessagePayload(rawEvent.data);
    }
    if ('toString' in rawEvent) {
      return String(rawEvent);
    }
  }
  return '';
}

function socketSendJson(socket, payload) {
  socket.send(JSON.stringify(payload));
}

async function appendRuntimeEvent(paths, payload) {
  await appendNdjson(paths.eventsPath, payload);
}

async function runWsDaemon(args) {
  const paths = getPaths({
    session: args.session,
    stateRoot: args['state-root'],
  });
  await ensureSessionDir(paths);

  const socketCtor = await loadWebSocketCtor();
  let stopped = false;
  let currentSocket = null;
  let reconnectTimer = null;
  let pingTimer = null;

  async function updateRuntime(patch) {
    const current = await loadRuntime(paths);
    await saveRuntime(paths, {
      ...current,
      ...patch,
      ws_pid: process.pid,
      ws_session: paths.session,
      ws_process_name: basename(fileURLToPath(import.meta.url)),
      ws_updated_at: nowSeconds(),
    });
  }

  async function clearTimers() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    if (pingTimer) {
      clearInterval(pingTimer);
      pingTimer = null;
    }
  }

  async function scheduleReconnect() {
    if (stopped || reconnectTimer) {
      return;
    }
    reconnectTimer = setTimeout(async () => {
      reconnectTimer = null;
      await connectOnce();
    }, RECONNECT_MS);
  }

  async function connectOnce() {
    if (stopped) {
      return;
    }

    const config = await loadConfig(paths);
    const identity = await loadOrCreateIdentity(paths);
    const authSession = await ensureToken(paths, identity, config).catch(async () => {
      return ensureToken(paths, identity, config, true);
    });

    await updateRuntime({
      ws_status: 'connecting',
      ws_last_connect_attempt_at: nowSeconds(),
      ws_token_expires_at: authSession.expires_at,
    });

    const socket = new socketCtor(config.ws_url);
    currentSocket = socket;

    bindSocketEvent(socket, 'open', async () => {
      await updateRuntime({
        ws_status: 'open',
        ws_last_connected_at: nowSeconds(),
      });

      socketSendJson(socket, {
        type: 'AUTH',
        token: authSession.token,
      });

      await appendRuntimeEvent(paths, {
        ts: nowSeconds(),
        level: 'info',
        source: 'ws-daemon',
        message: 'ws-open',
      });
    });

    bindSocketEvent(socket, 'close', async () => {
      if (stopped) {
        return;
      }

      await updateRuntime({
        ws_status: 'closed',
        ws_last_closed_at: nowSeconds(),
      });

      await appendRuntimeEvent(paths, {
        ts: nowSeconds(),
        level: 'warn',
        source: 'ws-daemon',
        message: 'ws-closed',
      });

      await clearTimers();
      await scheduleReconnect();
    });

    bindSocketEvent(socket, 'error', async (error) => {
      await appendRuntimeEvent(paths, {
        ts: nowSeconds(),
        level: 'error',
        source: 'ws-daemon',
        message: 'ws-error',
        detail: String(error?.message ?? error),
      });
      await updateRuntime({
        ws_status: 'error',
        ws_last_error: String(error?.message ?? error),
      });
    });

    bindSocketEvent(socket, 'message', async (raw) => {
      const rawText = normalizeMessagePayload(raw);
      if (!rawText) {
        return;
      }

      let parsed;
      try {
        parsed = JSON.parse(rawText);
      } catch {
        await appendRuntimeEvent(paths, {
          ts: nowSeconds(),
          level: 'warn',
          source: 'ws-daemon',
          message: 'ws-message-invalid-json',
          raw: rawText.slice(0, 500),
        });
        return;
      }

      await updateRuntime({
        ws_last_message_at: nowSeconds(),
      });

      const messageType = typeof parsed?.type === 'string' ? parsed.type : 'UNKNOWN';
      if (messageType === 'AUTH_OK') {
        socketSendJson(socket, {
          type: 'SUBSCRIBE',
          topics: config.subscriptions ?? DEFAULT_SUBSCRIPTIONS,
        });
        await updateRuntime({
          ws_status: 'authenticated',
          ws_authenticated_at: nowSeconds(),
        });

        if (pingTimer) {
          clearInterval(pingTimer);
        }
        pingTimer = setInterval(() => {
          if (!stopped && currentSocket) {
            socketSendJson(currentSocket, {
              type: 'PING',
              ts: nowSeconds(),
            });
          }
        }, PING_INTERVAL_MS);
      }

      if (messageType === 'EVENT') {
        const eventId = typeof parsed.event_id === 'string' ? parsed.event_id : null;
        await appendRuntimeEvent(paths, {
          ts: nowSeconds(),
          level: 'info',
          source: 'ws-event',
          topic: parsed.topic ?? null,
          event_id: eventId,
          envelope_type: parsed.envelope?.type ?? null,
          from: parsed.envelope?.from ?? null,
          payload: parsed.envelope?.payload ?? null,
        });
        if (eventId && /^\d+$/.test(eventId)) {
          socketSendJson(socket, {
            type: 'ACK',
            event_ids: [eventId],
          });
        }
        return;
      }

      if (messageType === 'BACKLOG' && Array.isArray(parsed.events)) {
        const ackIds = [];
        for (const event of parsed.events) {
          if (typeof event?.event_id === 'string' && /^\d+$/.test(event.event_id)) {
            ackIds.push(event.event_id);
          }
          await appendRuntimeEvent(paths, {
            ts: nowSeconds(),
            level: 'info',
            source: 'ws-backlog',
            topic: event?.topic ?? null,
            event_id: event?.event_id ?? null,
            envelope_type: event?.envelope?.type ?? null,
            from: event?.envelope?.from ?? null,
            payload: event?.envelope?.payload ?? null,
          });
        }

        if (ackIds.length > 0) {
          socketSendJson(socket, {
            type: 'ACK',
            event_ids: ackIds,
          });
        }
        return;
      }

      if (messageType === 'ERROR') {
        await appendRuntimeEvent(paths, {
          ts: nowSeconds(),
          level: 'error',
          source: 'ws-daemon',
          message: 'ws-server-error',
          detail: parsed.error ?? null,
        });
        await updateRuntime({
          ws_status: 'server-error',
          ws_last_error: String(parsed.error ?? 'unknown'),
        });
        return;
      }

      await appendRuntimeEvent(paths, {
        ts: nowSeconds(),
        level: 'debug',
        source: 'ws-daemon',
        message: 'ws-message',
        data: parsed,
      });
    });
  }

  async function shutdown(signal) {
    if (stopped) {
      return;
    }
    stopped = true;

    await clearTimers();
    if (currentSocket) {
      try {
        currentSocket.close();
      } catch {
        // Ignore close errors during shutdown.
      }
      currentSocket = null;
    }

    await updateRuntime({
      ws_status: 'stopped',
      ws_stopped_at: nowSeconds(),
      ws_stop_signal: signal,
    });

    process.exit(0);
  }

  process.on('SIGINT', () => {
    void shutdown('SIGINT');
  });
  process.on('SIGTERM', () => {
    void shutdown('SIGTERM');
  });

  await updateRuntime({
    ws_status: 'booting',
    ws_started_at: nowSeconds(),
    ws_pid: process.pid,
    ws_script_dir: dirname(fileURLToPath(import.meta.url)),
  });
  await appendRuntimeEvent(paths, {
    ts: nowSeconds(),
    level: 'info',
    source: 'ws-daemon',
    message: 'daemon-started',
    pid: process.pid,
  });

  await connectOnce();
}

function printHelp() {
  printJson({
    ok: true,
    usage: [
      'connect-runtime: node clawpeers_runtime.mjs connect --session demo --with-ws true --bootstrap-profile true --sync-subscriptions true',
      'status-runtime: node clawpeers_runtime.mjs status --session demo',
      'stop-runtime: node clawpeers_runtime.mjs stop --session demo',
      'publish-profile: node clawpeers_runtime.mjs publish-profile --session demo --display-name "Ada"',
      'sync-subscriptions: node clawpeers_runtime.mjs sync-subscriptions --session demo --topics need.event.match,need.peer.rescue',
      'poll-inbox: node clawpeers_runtime.mjs poll-inbox --session demo --limit 50',
      'ack-inbox: node clawpeers_runtime.mjs ack-inbox --session demo --event-ids 1001,1002',
      'publish-event: node clawpeers_runtime.mjs publish-event --session demo --topic intro.alias.<alias> --type INTRO_REQUEST --payload-json "{...}"',
      'prepare-need-draft: node clawpeers_runtime.mjs prepare-need-draft --session demo --text "I need an engineering mentor"',
      'refine-need-draft: node clawpeers_runtime.mjs refine-need-draft --session demo --draft-id <id> --goal "..." --time-window "..." --location-scope "..."',
      'preview-need: node clawpeers_runtime.mjs preview-need --session demo --draft-id <id>',
      'publish-need: node clawpeers_runtime.mjs publish-need --session demo --draft-id <id> --user-approved true',
      'query-needs: node clawpeers_runtime.mjs query-needs --session demo --tags mentor,engineering --limit 20',
      'read-events: node clawpeers_runtime.mjs read-events --session demo --limit 50',
      'claim-handle: node clawpeers_runtime.mjs claim-handle --session demo --handle your-handle',
    ],
    notes: [
      'Use --state-root to change default local state directory.',
      'ws-daemon is internal and started by connect-runtime.',
      'connect-runtime can bootstrap profile publish and subscription sync in one step.',
      'publish-need requires explicit --user-approved true.',
      'publish-event signs --type + --payload-json automatically when --envelope-json is not supplied.',
    ],
  });
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command || command === 'help' || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const args = parseArgs(rest);

  try {
    switch (command) {
      case 'connect':
      case 'connect-runtime':
        await commandConnect(args);
        return;
      case 'status':
      case 'status-runtime':
        await commandStatus(args);
        return;
      case 'stop':
      case 'stop-runtime':
        await commandStop(args);
        return;
      case 'publish-profile':
        await commandPublishProfile(args);
        return;
      case 'sync-subscriptions':
      case 'sync-subscription':
        await commandSyncSubscriptions(args);
        return;
      case 'poll-inbox':
        await commandPollInbox(args);
        return;
      case 'ack-inbox':
        await commandAckInbox(args);
        return;
      case 'publish-event':
        await commandPublishEvent(args);
        return;
      case 'prepare-need-draft':
        await commandPrepareNeedDraft(args);
        return;
      case 'refine-need-draft':
        await commandRefineNeedDraft(args);
        return;
      case 'preview-need':
        await commandPreviewNeed(args);
        return;
      case 'publish-need':
        await commandPublishNeed(args);
        return;
      case 'query-needs':
        await commandQueryNeeds(args);
        return;
      case 'read-events':
        await commandReadEvents(args);
        return;
      case 'claim-handle':
        await commandClaimHandle(args);
        return;
      case 'ws-daemon':
        await runWsDaemon(args);
        return;
      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`[clawpeers-runtime] ${message}`);
    printJson({
      ok: false,
      error: message,
      command,
    });
    process.exitCode = 1;
  }
}

await main();
