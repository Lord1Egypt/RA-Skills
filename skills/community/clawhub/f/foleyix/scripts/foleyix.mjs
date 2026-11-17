#!/usr/bin/env node
/** Foleyix 1.4.1 — zero-dependency CLI; Node.js 22.20 or newer. */
import { constants as fsConstants } from 'node:fs';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createHash, randomUUID } from 'node:crypto';

const VERSION = '1.4.1';
const CLIENT_ID = 'foleyix-cli';
const DEFAULT_ORIGIN = 'https://foleyix.com';
const MODES = ['free', 'narration', 'dialogue', 'podcast', 'scene', 'sfx', 'ambience'];
const STATES = ['queued', 'running', 'succeeded', 'failed', 'unknown'];
const WAV_MIMES = ['audio/wav', 'audio/wave', 'audio/x-wav', 'audio/vnd.wave'];
const MAX_AUDIO_BYTES = 128 * 1024 * 1024;
const MAX_REFERENCE_VOICES = 3;
const secrets = new Set();
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const hash = (value) => createHash('sha256').update(value).digest('hex');
const noFollow = fsConstants.O_NOFOLLOW || 0;
let jsonOutput = process.argv.includes('--json');
let origin;
let config;

class CliError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.code = code;
    this.details = details;
  }
}
const fail = (code, message, details) => { throw new CliError(code, message, details); };
function redact(value) {
  if (typeof value === 'string') {
    for (const secret of secrets) if (secret) value = value.split(secret).join('[redacted]');
    return value;
  }
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, redact(v)]));
  return value;
}
function output(value) {
  const safe = redact(value);
  if (jsonOutput) process.stdout.write(JSON.stringify(safe) + '\n');
  else if (safe.help) process.stdout.write(safe.help + '\n');
  else process.stdout.write(JSON.stringify(safe, null, 2) + '\n');
}
function note(message) { process.stderr.write(redact(message) + '\n'); }
function parseArgs() {
  const args = process.argv.slice(2), options = {}, positional = [];
  const booleans = new Set(['json', 'no-browser', 'no-wait', 'force', 'active', 'help', 'version']);
  const values = new Set(['origin', 'mode', 'prompt', 'input', 'out', 'request-id', 'timeout', 'cursor', 'limit', 'voice-id']);
  for (let i = 0; i < args.length; i++) {
    const argument = args[i];
    if (!argument.startsWith('--')) { positional.push(argument); continue; }
    const separator = argument.indexOf('=');
    const name = argument.slice(2, separator < 0 ? undefined : separator);
    if (name !== 'voice-id' && Object.hasOwn(options, name)) fail('invalid_argument', 'An option was provided more than once.');
    if (booleans.has(name)) {
      if (separator >= 0) fail('invalid_argument', 'Boolean options do not take a value.');
      options[name] = true;
    } else if (values.has(name)) {
      const value = separator >= 0 ? argument.slice(separator + 1) : args[++i];
      if (value === undefined || value.startsWith('--')) fail('invalid_argument', 'An option is missing its value.');
      if (name === 'voice-id') (options[name] ||= []).push(value);
      else options[name] = value;
    } else fail('invalid_argument', 'An unsupported option was provided. Run help to see supported options.');
  }
  const command = options.help ? 'help' : options.version ? 'version' : positional.shift() || 'help';
  jsonOutput = !!options.json;
  const permitted = {
    help: [], version: [], capabilities: [], login: ['no-browser', 'timeout'], whoami: [], logout: [], quota: [], voices: [],
    generate: ['mode', 'prompt', 'input', 'out', 'force', 'no-wait', 'request-id', 'timeout', 'voice-id'],
    jobs: ['active', 'cursor', 'limit'], status: [], download: ['out', 'force'],
  };
  if (!Object.hasOwn(permitted, command)) fail('invalid_command', 'Unknown command. Run help for available commands.');
  for (const name of Object.keys(options)) {
    if (!['origin', 'json', 'help', 'version'].includes(name) && !permitted[command].includes(name)) fail('invalid_argument', 'This option is not available for the selected command.');
  }
  if (positional.length !== (['status', 'download'].includes(command) ? 1 : 0)) fail('invalid_argument', 'This command has missing or unexpected positional arguments.');
  return { command, options, positional };
}
function serviceOrigin(value, explicit) {
  let url;
  try { url = new URL(value); } catch { fail('invalid_origin', 'Use an HTTPS origin without a path, credentials, or query.'); }
  if (url.username || url.password || url.search || url.hash || url.pathname !== '/') fail('invalid_origin', 'Use an origin without credentials, a path, query, or fragment.');
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname);
  const domain = url.hostname.includes('.') && url.hostname.split('.').every((label) => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label)) && !/^\d+(?:\.\d+){3}$/.test(url.hostname);
  if (!(url.protocol === 'https:' && (domain || (explicit && local))) && !(explicit && local && url.protocol === 'http:')) fail('invalid_origin', 'Use HTTPS with a valid domain. HTTP is allowed only with an explicit localhost origin.');
  return url.origin;
}
function apiUrl(relative) {
  const url = new URL(relative, origin);
  if (url.origin !== origin || url.username || url.password || url.hash || !url.pathname.startsWith('/api/')) fail('unsafe_url', 'The server returned an unsafe API URL.');
  return url.href;
}
function identifier(value, label = 'identifier') {
  if (typeof value !== 'string' || !/^[A-Za-z0-9_.:-]{1,128}$/.test(value)) fail('invalid_argument', 'Use a valid ' + label + '.');
  return value;
}
function integerOption(value, fallback, maximum = 3600) {
  if (value === undefined) return fallback;
  if (!/^\d+$/.test(value) || Number(value) < 1 || Number(value) > maximum) fail('invalid_argument', 'Use a positive whole number within the supported limit.');
  return Number(value);
}
function safeString(value, limit = 256) { return typeof value === 'string' ? value.slice(0, limit) : null; }
function publicUser(value) {
  if (!value || typeof value !== 'object') fail('invalid_response', 'The account response is incomplete.');
  return { id: safeString(value.id), email: safeString(value.email), name: safeString(value.name) };
}
function publicVoice(value) {
  if (!value || typeof value !== 'object' || typeof value.id !== 'string' || !/^[A-Za-z0-9_.:-]{1,128}$/.test(value.id)
    || typeof value.name !== 'string' || typeof value.status !== 'string') fail('invalid_response', 'The reference voice response is incomplete.');
  const audio = value.referenceAudio;
  return { id: value.id, name: safeString(value.name, 48), description: safeString(value.description, 2048),
    status: safeString(value.status, 32), source: ['catalog', 'upload', 'design'].includes(value.source) ? value.source : null,
    assetId: safeString(value.assetId, 128), referenceAudio: audio && Number.isFinite(audio.duration) && Number.isSafeInteger(audio.bytes)
      ? { duration: audio.duration, bytes: audio.bytes } : null };
}
function publicJob(value) {
  if (!value || typeof value !== 'object' || !STATES.includes(value.status)) fail('invalid_response', 'The task response is incomplete.');
  identifier(value.id, 'task ID');
  const result = {
    id: value.id, kind: safeString(value.kind), status: value.status,
    projectName: safeString(value.projectName), segmentTitle: safeString(value.segmentTitle),
    createdAt: safeString(value.createdAt), updatedAt: safeString(value.updatedAt),
    quotaUnits: Number.isFinite(value.quotaUnits) ? value.quotaUnits : null,
    quotaUnit: value.quotaUnit === 'seconds' ? 'seconds' : null,
    resultAvailable: value.resultAvailable === true, resultExpiresAt: safeString(value.resultExpiresAt),
  };
  if (value.asset && value.resultAvailable === true) {
    const asset = value.asset;
    identifier(asset.id, 'asset ID');
    const parsed = new URL(apiUrl(asset.url));
    if (parsed.pathname !== '/api/assets/' + encodeURIComponent(asset.id) || parsed.search) fail('unsafe_url', 'The audio URL does not match its private asset.');
    result.asset = { id: asset.id, mime: safeString(asset.mime, 80), bytes: asset.bytes, duration: asset.duration, url: parsed.pathname };
  }
  return result;
}
function serverError(status, data) {
  const raw = typeof data?.code === 'string' && /^[a-z][a-z0-9_]{0,63}$/.test(data.code) ? data.code : typeof data?.error === 'string' ? data.error : data?.error?.code;
  const code = typeof raw === 'string' && /^[a-z][a-z0-9_]{0,63}$/.test(raw) ? raw : 'http_error';
  const messages = {
    authorization_pending: 'Waiting for website authorization.', slow_down: 'The authorization server requested slower polling.',
    expired_token: 'The authorization code expired. Run login again.', access_denied: 'Website authorization was declined.',
    invalid_grant: 'The login can no longer be refreshed. Run login again.', queue_full: 'Your account queue is full. Wait for an existing task to finish.',
    model_disabled: 'Audio generation is currently unavailable on this service.', service_not_ready: 'Audio generation is currently unavailable on this service.',
    quota_exceeded: 'Your account does not have enough available audio time.', invalid_input: 'The service rejected this input. Check its length and selected mode.',
    idempotency_conflict: 'This request ID has already been used with different input.', request_key_conflict: 'This request ID has already been used with different input.',
    invalid_voices: 'Select up to three distinct saved reference voices.', voice_not_ready: 'A reference is missing, not owned by this account, or has no completed preview. Run voices and check it on the website.',
    reference_audio_too_long: 'Each reference must be at most 30 seconds.', reference_audio_too_large: 'Each reference must be at most 10 MB.',
    invalid_reference_audio: 'A reference has invalid audio metadata. Check or replace it on the website.',
    invalid_prompt: 'The final prompt, including reference descriptions, must contain 1–3,000 Unicode characters.',
  };
  return new CliError(code, messages[code] || (status === 401 ? 'Website login is required. Run login again.' : 'Foleyix rejected this request.'), { status });
}
async function fetchJSON(relative, { method = 'GET', body, token, headers = {} } = {}) {
  if (token) secrets.add(token);
  const controller = new AbortController(), timeout = setTimeout(() => controller.abort(), 30000);
  try {
    const response = await fetch(apiUrl(relative), {
      method, signal: controller.signal, redirect: 'error', cache: 'no-store',
      headers: { Accept: 'application/json', ...(body ? { 'Content-Type': 'application/json' } : {}), ...(token ? { Authorization: 'Bearer ' + token } : {}), ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });
    const raw = await response.text();
    if (raw.length > 1024 * 1024) fail('invalid_response', 'The service response is too large.');
    let data;
    try { data = JSON.parse(raw); } catch { fail('invalid_response', 'The service did not return JSON.', { status: response.status }); }
    if (!response.ok) throw serverError(response.status, data);
    return data;
  } catch (error) {
    if (error instanceof CliError) throw error;
    fail('network_error', 'The service response could not be confirmed. Check your connection.');
  } finally { clearTimeout(timeout); }
}
async function privateDirectory(directory) {
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  const stat = await fs.lstat(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink() || (process.getuid && stat.uid !== process.getuid())) fail('unsafe_config', 'Use a private configuration directory owned by your user.');
  if (process.platform !== 'win32' && (stat.mode & 0o777) !== 0o700) await fs.chmod(directory, 0o700);
}
async function initializeConfig() {
  const root = path.resolve(process.env.FOLEYIX_CONFIG_DIR || path.join(os.homedir(), '.config', 'foleyix'));
  await privateDirectory(root);
  const directory = path.join(root, hash(origin));
  await privateDirectory(directory);
  config = { root, directory, credentials: path.join(directory, 'credentials.json'), journal: path.join(directory, 'requests.json'), lock: path.join(directory, '.lock') };
}
async function readPrivate(file, optional = true) {
  let handle;
  try {
    const stat = await fs.lstat(file);
    if (!stat.isFile() || stat.isSymbolicLink() || (process.getuid && stat.uid !== process.getuid())) fail('unsafe_config', 'A private configuration file has unsafe ownership or type.');
    handle = await fs.open(file, fsConstants.O_RDONLY | noFollow);
    const opened = await handle.stat();
    if (opened.ino !== stat.ino || opened.dev !== stat.dev || opened.size > 1024 * 1024) fail('unsafe_config', 'The private configuration changed while it was being read.');
    if (process.platform !== 'win32' && (opened.mode & 0o777) !== 0o600) await handle.chmod(0o600);
    return JSON.parse(await handle.readFile('utf8'));
  } catch (error) {
    if (optional && error.code === 'ENOENT') return null;
    if (error instanceof CliError) throw error;
    fail('invalid_config', 'The private configuration could not be read. Run login again or repair its permissions.');
  } finally { await handle?.close(); }
}
async function syncDirectory(directory) {
  if (process.platform === 'win32') return;
  const handle = await fs.open(directory, fsConstants.O_RDONLY);
  try { await handle.sync(); } catch (error) { if (!['EINVAL', 'ENOTSUP'].includes(error.code)) throw error; } finally { await handle.close(); }
}
async function savePrivate(file, value) {
  await privateDirectory(config.directory);
  try { const stat = await fs.lstat(file); if (!stat.isFile() || stat.isSymbolicLink()) fail('unsafe_config', 'Refusing to replace an unsafe private configuration file.'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  const temporary = file + '.' + randomUUID() + '.tmp';
  let handle;
  try {
    handle = await fs.open(temporary, fsConstants.O_WRONLY | fsConstants.O_CREAT | fsConstants.O_EXCL | noFollow, 0o600);
    await handle.writeFile(JSON.stringify(value) + '\n');
    await handle.sync(); await handle.close(); handle = null;
    await fs.rename(temporary, file);
    await syncDirectory(config.directory);
  } finally { await handle?.close(); await fs.unlink(temporary).catch(() => {}); }
}
async function withLock(operation) {
  const nonce = randomUUID(), ownerFile = path.join(config.lock, 'owner.json'), started = Date.now();
  for (;;) {
    try {
      await fs.mkdir(config.lock, { mode: 0o700 });
      await fs.writeFile(ownerFile, JSON.stringify({ pid: process.pid, nonce }), { flag: 'wx', mode: 0o600 });
      break;
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      const stat = await fs.lstat(config.lock);
      if (!stat.isDirectory() || stat.isSymbolicLink() || (process.getuid && stat.uid !== process.getuid())) fail('unsafe_config', 'The configuration lock is unsafe.');
      const owner = await readPrivate(ownerFile);
      let dead = false;
      if (owner && Number.isInteger(owner.pid) && owner.pid > 0) {
        try { process.kill(owner.pid, 0); } catch (error) { dead = error.code === 'ESRCH'; }
      } else dead = Date.now() - stat.mtimeMs > 35000;
      // Never remove a lock after a read: another process could replace it in between.
      if (dead) fail('cli_busy', 'A previous command left a lock. Confirm no Foleyix command is running, remove this private lock directory, then retry. Run login again if a refresh was interrupted.', { lockPath: config.lock });
      if (Date.now() - started > 35000) fail('cli_busy', 'Another Foleyix command is still updating the login. Retry after it finishes.');
      await sleep(100);
    }
  }
  try { return await operation(); }
  finally {
    const owner = await readPrivate(ownerFile);
    if (owner?.nonce === nonce) await fs.rm(config.lock, { recursive: true });
  }
}
function tokenData(data) {
  const refreshExpiresAt = typeof data?.refresh_expires_at === 'string' ? Date.parse(data.refresh_expires_at) : NaN;
  if (!data || data.token_type?.toLowerCase() !== 'bearer' || typeof data.access_token !== 'string' || data.access_token.length < 16 || typeof data.refresh_token !== 'string' || data.refresh_token.length < 16 || !Number.isFinite(data.expires_in) || data.expires_in <= 0 || !Number.isFinite(refreshExpiresAt) || refreshExpiresAt <= Date.now()) fail('invalid_response', 'The login response is incomplete. Run login again.');
  secrets.add(data.access_token); secrets.add(data.refresh_token);
  return { origin, accessToken: data.access_token, refreshToken: data.refresh_token, expiresAt: Math.min(Date.now() + data.expires_in * 1000, refreshExpiresAt), refreshExpiresAt, refreshPending: false };
}
async function credentials(allowPending = false) {
  const value = await readPrivate(config.credentials);
  if (!value) fail('not_logged_in', 'Run login and approve access on the Foleyix website.');
  if (typeof value.accessToken === 'string') secrets.add(value.accessToken);
  if (typeof value.refreshToken === 'string') secrets.add(value.refreshToken);
  if (value.origin !== origin || typeof value.accessToken !== 'string' || typeof value.refreshToken !== 'string' || !Number.isFinite(value.expiresAt) || !Number.isFinite(value.refreshExpiresAt)) fail('invalid_config', 'The saved login does not match this service. Run login again.');
  if (value.refreshPending && !allowPending) fail('login_required', 'A refresh response was not confirmed. Run login again; the old refresh credential cannot be reused.');
  return value;
}
async function refreshLocked(current, rejected) {
    if (current.expiresAt > Date.now() + 30000 && (!rejected || current.accessToken !== rejected)) return current.accessToken;
    if (current.refreshExpiresAt <= Date.now()) fail('login_required', 'Your CLI login has expired. Run login again.');
    // Persist before sending: if a rotated response is lost, never replay this refresh token.
    await savePrivate(config.credentials, { ...current, refreshPending: true });
    let refreshed;
    try { refreshed = await fetchJSON('/api/cli/auth/token', { method: 'POST', body: { grant_type: 'refresh_token', refresh_token: current.refreshToken, client_id: CLIENT_ID } }); }
    catch { fail('login_required', 'The refresh response was not confirmed. Run login again; the old refresh credential cannot be reused.'); }
    const next = tokenData(refreshed);
    await savePrivate(config.credentials, next);
    return next.accessToken;
}
async function accessToken(rejected) {
  return withLock(async () => refreshLocked(await credentials(), rejected));
}
async function authenticated(relative, options = {}) {
  let token = await accessToken();
  try { return await fetchJSON(relative, { ...options, token }); }
  catch (error) {
    if (!(error instanceof CliError) || error.details.status !== 401) throw error;
    token = await accessToken(token);
    return fetchJSON(relative, { ...options, token });
  }
}
async function login(options) {
  const device = await fetchJSON('/api/cli/auth/device-code', { method: 'POST', body: { client_id: CLIENT_ID } });
  if (typeof device.device_code === 'string') secrets.add(device.device_code);
  if (typeof device.device_code !== 'string' || device.device_code.length < 16 || typeof device.user_code !== 'string' || !/^[A-Z0-9-]{4,32}$/.test(device.user_code) || !Number.isFinite(device.expires_in) || device.expires_in < 1 || device.expires_in > 600) fail('invalid_response', 'The device authorization response is incomplete.');
  let verification;
  try { verification = new URL(device.verification_uri); } catch { fail('unsafe_url', 'The authorization URL is invalid.'); }
  if (verification.origin !== origin || verification.pathname !== '/activate' || verification.username || verification.password || verification.search || verification.hash) fail('unsafe_url', 'The authorization URL does not belong to this Foleyix service.');
  verification.searchParams.set('user_code', device.user_code);
  const authorizationUrl = verification.href;
  note('Open ' + authorizationUrl + '\nAuthorization code: ' + device.user_code + '\nLog in on the website, check the account and code, and approve this CLI.');
  const until = Date.now() + Math.min(device.expires_in, integerOption(options.timeout, device.expires_in, 600)) * 1000;
  let interval = Number.isFinite(device.interval) ? Math.max(1, device.interval) : 5;
  for (;;) {
    if (Date.now() >= until) fail('login_timeout', 'Authorization was not completed before the deadline. Run login again.');
    await sleep(Math.min(interval * 1000, until - Date.now()));
    if (Date.now() >= until) fail('login_timeout', 'Authorization was not completed before the deadline. Run login again.');
    try {
      const tokens = await fetchJSON('/api/cli/auth/token', { method: 'POST', body: { grant_type: 'urn:ietf:params:oauth:grant-type:device_code', device_code: device.device_code, client_id: CLIENT_ID } });
      const value = tokenData(tokens);
      await withLock(() => savePrivate(config.credentials, value));
      const identity = await authenticated('/api/cli/auth/whoami');
      return output({ ok: true, authenticated: true, origin, user: publicUser(identity.user), modelEnabled: identity.modelEnabled === true });
    } catch (error) {
      if (error.code === 'authorization_pending') continue;
      if (error.code === 'slow_down') { interval += 5; continue; }
      throw error;
    }
  }
}
async function logout() {
  await withLock(async () => {
    const value = await credentials(true);
    // A failed revoke retains the login so the user can retry and actually revoke it.
    // Consumed refresh tokens are accepted only for revocation, never replayed for refresh.
    const result = await fetchJSON('/api/cli/auth/revoke', { method: 'POST', body: { client_id: CLIENT_ID, refresh_token: value.refreshToken } });
    if (result.success !== true) fail('revoke_unconfirmed', 'The server did not confirm revocation. Your local login was retained; retry logout.');
    await fs.unlink(config.credentials);
    await syncDirectory(config.directory);
  });
  output({ ok: true, authenticated: false, origin, revoked: true });
}
async function getJob(id) {
  return publicJob((await authenticated('/api/jobs/' + encodeURIComponent(identifier(id, 'task ID')))).job);
}
async function requestRecord(prompt, mode, requestedId, voiceIds) {
  // Keep historical no-reference fingerprints; reference order defines @voiceN.
  const inputHash = hash(JSON.stringify({ mode, prompt, ...(voiceIds.length ? { voiceIds } : {}) }));
  return withLock(async () => {
    const journal = await readPrivate(config.journal) || { origin, requests: {} };
    if (journal.origin !== origin || !journal.requests || typeof journal.requests !== 'object' || Array.isArray(journal.requests)) fail('invalid_config', 'The saved request journal is invalid.');
    let requestId = requestedId ? identifier(requestedId, 'request ID') : null;
    if (!requestId) requestId = Object.keys(journal.requests).find((id) => journal.requests[id].inputHash === inputHash && ['pending', 'uncertain'].includes(journal.requests[id].state)) || randomUUID();
    const previous = journal.requests[requestId];
    if (previous && previous.inputHash !== inputHash) fail('idempotency_conflict', 'This request ID was already saved for different input.', { requestId });
    const record = previous || { inputHash, createdAt: new Date().toISOString(), state: 'pending' };
    journal.requests[requestId] = record;
    // Keep unresolved requests; cap successful history to avoid unbounded local growth.
    const resolved = Object.entries(journal.requests).filter(([, r]) => r.state === 'resolved').sort((a, b) => a[1].createdAt.localeCompare(b[1].createdAt));
    for (const [id] of resolved.slice(0, Math.max(0, resolved.length - 500))) if (id !== requestId) delete journal.requests[id];
    await savePrivate(config.journal, journal);
    return { requestId, ...record };
  });
}
async function updateRecord(requestId, patch) {
  await withLock(async () => {
    const journal = await readPrivate(config.journal, false);
    if (journal.origin !== origin || !journal.requests?.[requestId]) fail('invalid_config', 'The saved request journal changed unexpectedly.');
    journal.requests[requestId] = { ...journal.requests[requestId], ...patch };
    await savePrivate(config.journal, journal);
  });
}
async function waitForJob(job, timeout) {
  const until = Date.now() + timeout * 1000;
  while (['queued', 'running'].includes(job.status)) {
    if (Date.now() >= until) return { job, timedOut: true };
    await sleep(Math.min(5000, until - Date.now()));
    job = await getJob(job.id);
  }
  return { job, timedOut: false };
}
async function generate(options) {
  if ((options.prompt === undefined) === (options.input === undefined)) fail('invalid_argument', 'Provide exactly one of --prompt or --input.');
  const mode = options.mode || 'narration';
  if (!MODES.includes(mode)) fail('invalid_argument', 'Use ' + MODES.join(', ') + '.');
  if (options['no-wait'] && options.out) fail('invalid_argument', '--out requires waiting for the task; remove --no-wait.');
  if (options.force && !options.out) fail('invalid_argument', '--force requires --out.');
  const timeout = integerOption(options.timeout, 600, 3600);
  let prompt = options.prompt;
  if (options.input !== undefined) {
    const file = path.resolve(options.input), stat = await fs.stat(file);
    if (!stat.isFile() || stat.size > 64 * 1024) fail('invalid_input', 'Use a UTF-8 text file no larger than 64 KiB.');
    const bytes = await fs.readFile(file);
    try { prompt = new TextDecoder('utf-8', { fatal: true }).decode(bytes); } catch { fail('invalid_input', 'The input file must contain valid UTF-8 text.'); }
  }
  if (typeof prompt !== 'string' || !prompt.trim() || Buffer.byteLength(prompt, 'utf8') > 64 * 1024) fail('invalid_input', 'Provide nonempty text no larger than 64 KiB; the service also enforces mode limits.');
  prompt = prompt.trim();
  if (Array.from(prompt).length > 3000) fail('invalid_input', 'Use no more than 3,000 Unicode characters.');
  const voiceIds = (options['voice-id'] || []).map(id => identifier(id, 'saved reference voice ID'));
  if (voiceIds.length > MAX_REFERENCE_VOICES || new Set(voiceIds).size !== voiceIds.length) fail('invalid_argument', 'Select up to three distinct saved reference voices with --voice-id, in @voice1–@voice3 order.');
  // Check login before creating an unresolved journal entry.
  await accessToken();
  const record = await requestRecord(prompt, mode, options['request-id'], voiceIds);
  let job;
  if (record.jobId) job = await getJob(record.jobId);
  else {
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        job = publicJob((await authenticated('/api/generations', { method: 'POST', body: { mode, prompt, ...(voiceIds.length ? { voiceIds } : {}) }, headers: { 'Idempotency-Key': record.requestId } })).job);
        await updateRecord(record.requestId, { state: ['succeeded', 'failed'].includes(job.status) ? 'resolved' : job.status === 'unknown' ? 'uncertain' : 'pending', jobId: job.id });
        break;
      } catch (error) {
        const retryable = error.code === 'network_error' || error.details?.status >= 500;
        const confirmedRejection = error.details?.status >= 400 && error.details?.status < 500 && !['invalid_response', 'unsafe_url'].includes(error.code);
        await updateRecord(record.requestId, { state: confirmedRejection ? 'rejected' : 'uncertain' });
        if (retryable) {
          if (attempt < 2) { await sleep(1000 * (attempt + 1)); continue; }
        }
        error.details = { ...error.details, requestId: record.requestId };
        throw error;
      }
    }
  }
  let result;
  try { result = options['no-wait'] ? { job, timedOut: false } : await waitForJob(job, timeout); }
  catch (error) { error.details = { ...error.details, jobId: job.id, requestId: record.requestId }; throw error; }
  await updateRecord(record.requestId, { state: ['succeeded', 'failed'].includes(result.job.status) ? 'resolved' : result.job.status === 'unknown' ? 'uncertain' : 'pending', jobId: job.id });
  if (['failed', 'unknown'].includes(result.job.status)) fail(result.job.status === 'unknown' ? 'generation_unknown' : 'generation_failed', result.job.status === 'unknown' ? 'The model result is unknown. Check this task; do not start a replacement automatically.' : 'The audio task failed. Check its status on Foleyix.', { jobId: job.id, requestId: record.requestId });
  let delivery = {};
  try { if (options.out && !result.timedOut) delivery = await downloadJob(result.job, options); }
  catch (error) { error.details = { ...error.details, jobId: job.id, requestId: record.requestId }; throw error; }
  output({ ok: true, requestId: record.requestId, jobId: job.id, status: result.job.status, timedOut: result.timedOut, job: result.job, ...delivery });
}
function validateWav(bytes) {
  if (bytes.length < 44 || bytes.toString('ascii', 0, 4) !== 'RIFF' || bytes.toString('ascii', 8, 12) !== 'WAVE' || bytes.readUInt32LE(4) + 8 !== bytes.length) fail('invalid_audio', 'The download is not a complete RIFF/WAVE audio file.');
  let position = 12, format = false, data = false;
  while (position + 8 <= bytes.length) {
    const kind = bytes.toString('ascii', position, position + 4), size = bytes.readUInt32LE(position + 4);
    if (position + 8 + size > bytes.length) fail('invalid_audio', 'The WAV download contains a truncated chunk.');
    if (kind === 'fmt ') {
      if (size < 16) fail('invalid_audio', 'The WAV format chunk is incomplete.');
      const encoding = bytes.readUInt16LE(position + 8), channels = bytes.readUInt16LE(position + 10), rate = bytes.readUInt32LE(position + 12), alignment = bytes.readUInt16LE(position + 20);
      if (![1, 3, 0xfffe].includes(encoding) || channels < 1 || channels > 32 || rate < 8000 || rate > 384000 || alignment < 1) fail('invalid_audio', 'The WAV format is unsupported or invalid.');
      format = true;
    }
    if (kind === 'data' && size > 0) data = true;
    position += 8 + size + (size % 2);
  }
  if (!format || !data || position !== bytes.length) fail('invalid_audio', 'The WAV download is missing complete audio data.');
}
async function audioBytes(asset, rejected) {
  const token = await accessToken(rejected);
  const controller = new AbortController(), timeout = setTimeout(() => controller.abort(), 30000);
  try {
    const response = await fetch(apiUrl(asset.url), { headers: { Accept: 'audio/wav', Authorization: 'Bearer ' + token }, redirect: 'error', cache: 'no-store', signal: controller.signal });
    if (response.status === 401 && !rejected) { clearTimeout(timeout); return audioBytes(asset, token); }
    if (!response.ok) throw serverError(response.status, null);
    const mime = (response.headers.get('content-type') || '').split(';')[0].trim().toLowerCase();
    if (!WAV_MIMES.includes(mime)) fail('invalid_audio', 'The private asset download did not return WAV audio.');
    const declared = response.headers.get('content-length');
    if (declared && (!/^\d+$/.test(declared) || Number(declared) !== asset.bytes)) fail('invalid_audio', 'The audio size does not match its task metadata.');
    const chunks = [], reader = response.body?.getReader();
    if (!reader) fail('invalid_audio', 'The audio response has no content.');
    let length = 0;
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > asset.bytes || length > MAX_AUDIO_BYTES) { await reader.cancel(); fail('invalid_audio', 'The audio download exceeds its expected size.'); }
      chunks.push(Buffer.from(value));
    }
    if (length !== asset.bytes) fail('invalid_audio', 'The audio download is incomplete.');
    const bytes = Buffer.concat(chunks, length);
    validateWav(bytes);
    return bytes;
  } catch (error) {
    if (error instanceof CliError) throw error;
    fail('network_error', 'The audio download could not be confirmed. No output file was saved.');
  } finally { clearTimeout(timeout); }
}
async function downloadJob(job, options) {
  if (job.status !== 'succeeded' || !job.resultAvailable || !job.asset) fail('result_unavailable', 'This task has no available audio result.', { jobId: job.id });
  const asset = job.asset;
  if (!WAV_MIMES.includes((asset.mime || '').toLowerCase()) || !Number.isInteger(asset.bytes) || asset.bytes < 44 || asset.bytes > MAX_AUDIO_BYTES) fail('invalid_audio', 'The audio metadata does not describe a supported WAV file.');
  const destination = path.resolve(options.out || 'foleyix-' + job.id + '.wav');
  if (path.extname(destination).toLowerCase() !== '.wav') fail('invalid_argument', 'Save WAV audio to a filename ending in .wav.');
  const directory = path.dirname(destination);
  const parent = await fs.stat(directory);
  if (!parent.isDirectory()) fail('invalid_output', 'The output directory must already exist.');
  try {
    const existing = await fs.lstat(destination);
    if (!existing.isFile() || existing.isSymbolicLink()) fail('unsafe_output', 'Refusing to replace a link or non-file output path.');
    if (!options.force) fail('output_exists', 'The output file already exists. Choose another filename or use --force.');
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  const bytes = await audioBytes(asset), temporary = path.join(directory, '.' + path.basename(destination) + '.' + randomUUID() + '.part');
  let handle;
  try {
    handle = await fs.open(temporary, fsConstants.O_WRONLY | fsConstants.O_CREAT | fsConstants.O_EXCL | noFollow, 0o600);
    await handle.writeFile(bytes); await handle.sync(); await handle.close(); handle = null;
    if (options.force) {
      try { const current = await fs.lstat(destination); if (!current.isFile() || current.isSymbolicLink()) fail('unsafe_output', 'Refusing to replace a link or non-file output path.'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
      await fs.rename(temporary, destination);
    } else {
      try { await fs.link(temporary, destination); } catch (error) { if (error.code === 'EEXIST') fail('output_exists', 'Another command created the output file. Choose another filename.'); throw error; }
      await fs.unlink(temporary);
    }
    await syncDirectory(directory);
  } finally { await handle?.close(); await fs.unlink(temporary).catch(() => {}); }
  return { path: destination, bytes: bytes.length, mime: 'audio/wav' };
}
const HELP = [
  'Foleyix ' + VERSION + ' — Node.js 22.20+',
  'Usage: node scripts/foleyix.mjs <command> [options]',
  'capabilities                            List bundled website-aligned audio types (no login)',
  'login [--no-browser] [--timeout seconds]  Open the displayed website URL manually and approve',
  'whoami                                  Show the connected account',
  'logout                                  Revoke this CLI connection',
  'quota                                   Show shared audio-time quota and queue',
  'voices                                  List your saved reference voices and audio metadata',
  'generate --prompt text | --input file [--mode free|narration|dialogue|podcast|scene|sfx|ambience]',
  '         [--voice-id id (repeat up to 3)] [--out audio.wav] [--force] [--no-wait] [--request-id id] [--timeout seconds]',
  'jobs [--active] [--cursor cursor] [--limit 1..100]',
  'status <jobId>',
  'download <jobId> [--out audio.wav] [--force]',
  'Global: --json, --origin https://foleyix.com',
  'Login always displays the authorization URL; --no-browser is retained for compatibility.',
  'Generation waits up to 600 seconds by default. A timeout retains the task and request IDs.',
  'Input: up to 3,000 Unicode characters. Default mode: narration; modes do not rewrite the prompt.',
  'Reference IDs come from voices; their order maps to @voice1, @voice2, @voice3. Typing a marker alone does not attach audio.',
  'Create/import/upload references on the website first. Each reference: at most 30 seconds and 10 MB.',
  'Credentials stay in a private, per-origin directory; do not copy them into a project.',
].join('\n');
async function main() {
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (major < 22 || (major === 22 && minor < 20)) fail('unsupported_node', 'Foleyix requires Node.js 22.20 or newer.');
  const { command, options, positional } = parseArgs();
  if (command === 'help') return output({ ok: true, help: HELP });
  if (command === 'version') return output({ ok: true, version: VERSION });
  if (command === 'capabilities') {
    const capabilities = JSON.parse(await fs.readFile(new URL('../references/audio-capabilities.json', import.meta.url), 'utf8'));
    if (capabilities.schemaVersion !== 1 || !Array.isArray(capabilities.types) || !Array.isArray(capabilities.creationModes)
      || capabilities.creationModes.length !== MODES.length || capabilities.creationModes.some((mode, index) => mode !== MODES[index])) fail('invalid_capabilities', 'The bundled audio capabilities do not match this CLI. Reinstall the complete skill.');
    return output({ ok: true, version: VERSION, capabilities });
  }
  origin = serviceOrigin(options.origin || DEFAULT_ORIGIN, options.origin !== undefined);
  await initializeConfig();
  if (command === 'login') return login(options);
  if (command === 'logout') return logout();
  if (command === 'whoami') {
    const value = await authenticated('/api/cli/auth/whoami');
    return output({ ok: true, origin, user: publicUser(value.user), scopes: Array.isArray(value.scopes) ? value.scopes.filter((scope) => ['audio:generate', 'audio:read'].includes(scope)) : [], expiresAt: safeString(value.expiresAt), modelEnabled: value.modelEnabled === true });
  }
  if (command === 'quota') {
    const value = (await authenticated('/api/quota')).quota;
    if (!value || typeof value !== 'object') fail('invalid_response', 'The quota response is incomplete.');
    const quota = Object.fromEntries(['plan', 'generationUnit', 'generationLimit', 'generationUsed', 'generationReserved', 'exportLimit', 'exportUsed', 'exportReserved', 'projectLimit', 'storageLimit', 'storageUsed', 'queueLimit', 'queueUsed', 'periodEnd'].filter((key) => typeof value[key] === 'string' || Number.isFinite(value[key]) || value[key] === null).map((key) => [key, value[key]]));
    return output({ ok: true, quota });
  }
  if (command === 'voices') {
    const value = await authenticated('/api/voices');
    if (!Array.isArray(value.voices)) fail('invalid_response', 'The reference voice response is incomplete.');
    return output({ ok: true, voices: value.voices.map(publicVoice) });
  }
  if (command === 'jobs') {
    const query = new URLSearchParams();
    if (options.active) query.set('active', '1');
    if (options.cursor) query.set('cursor', options.cursor);
    if (options.limit) query.set('limit', String(integerOption(options.limit, 50, 100)));
    const value = await authenticated('/api/jobs' + (query.size ? '?' + query : ''));
    if (!Array.isArray(value.jobs)) fail('invalid_response', 'The task history response is incomplete.');
    return output({ ok: true, jobs: value.jobs.map(publicJob), nextCursor: safeString(value.nextCursor, 1000) });
  }
  if (command === 'status') return output({ ok: true, job: await getJob(positional[0]) });
  if (command === 'download') { const job = await getJob(positional[0]); return output({ ok: true, jobId: job.id, ...await downloadJob(job, options) }); }
  return generate(options);
}
main().catch((error) => {
  const known = error instanceof CliError ? error : new CliError('local_error', 'The command could not complete. Check the input path and private directory permissions.');
  output({ ok: false, error: { code: known.code, message: known.message, ...known.details } });
  process.exitCode = 1;
});
