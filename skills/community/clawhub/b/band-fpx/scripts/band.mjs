#!/usr/bin/env node
// band-fpx helper: signed, read-only calls to BAND's web API (api-us.band.us).
//
//   node band.mjs get <endpoint> [key=value ...]   e.g. get /v2.1.0/get_band_list_with_filter
//   node band.mjs refresh                           re-capture the session from the browser
//
// Session bootstrap: the band.us cookies are read ONCE from the signed-in tab via
// `fpx cookies -p band`; the per-session HMAC secret comes from auth.band.us getKey.
// Both are cached in ~/.band-fpx/session.json (mode 600) — this skill's own file,
// never the band-mcp server's store. Every API call is then plain Node fetch.
//
// stdout = the API's JSON only. Exit codes: 0 ok · 2 fpx/bridge failure ·
// 4 signed out / API error (result_code != 1) · 64 usage.
import { createHmac } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

process.stdout.on('error', (e) => { if (e.code === 'EPIPE') process.exit(0); throw e; });

const API = process.env.BAND_API_BASE || 'https://api-us.band.us';
const AUTH = 'https://auth.band.us';
const AKEY = 'bbc59b0b5f7a1c6efe950f6236ccda35'; // static key of the band.us web app
const DIR = process.env.BAND_FPX_HOME || join(homedir(), '.band-fpx');
const FILE = join(DIR, 'session.json');
const PROFILE = process.env.BAND_FPX_PROFILE || 'band';
const TZ = Intl.DateTimeFormat().resolvedOptions().timeZone;

function die(code, msg) { process.stderr.write(`band-fpx: ${msg}\n`); process.exit(code); }

function jwtExpMs(token) {
  try { return JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString()).exp * 1000; }
  catch { return 0; }
}

async function capture() {
  let raw;
  try {
    raw = execFileSync('fpx', ['cookies', '-p', PROFILE], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'inherit'] });
  } catch (e) {
    die(2, `fpx cookies failed (exit ${e.status ?? '?'}) — is ContextMint Bridge paired and a band.us tab open?`);
  }
  let jar;
  try { jar = JSON.parse(raw); } catch { die(2, 'fpx cookies returned non-JSON'); }
  if (Array.isArray(jar)) jar = Object.fromEntries(jar.map((c) => [c.name, c.value]));
  if (!jar.band_session) die(4, 'no band_session cookie — sign in at https://www.band.us/ in the paired browser');
  const cookie = Object.entries(jar).map(([k, v]) => `${k}=${v}`).join('; ');

  // getKey must come from the browser tab: called from Node it answers a
  // signed-in state with an EMPTY secretKey. The callback name must be
  // authCallBack_<_t> or the body is empty.
  const t = Date.now();
  let body;
  try {
    body = execFileSync('fpx', ['get', `${AUTH}/s/login/getKey?_t=${t}&callback=authCallBack_${t}`,
      '-p', PROFILE, '--via-tab', 'https://www.band.us/'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'inherit'] });
  } catch (e) {
    die(2, `fpx getKey failed (exit ${e.status ?? '?'}) — is a band.us tab open in the paired browser?`);
  }
  const secretKey = body.match(/secretKey\s*:\s*'([^']+)'/)?.[1];
  if (!secretKey || !/authenticateState\s*:\s*"USER"/.test(body)) {
    die(4, 'getKey did not return a signed-in session — sign in at https://www.band.us/ and retry');
  }
  const jwt = /isJwtType\s*:\s*true/.test(body);
  const serverMs = Number(body.match(/timeCorrection:\s*(\d+)/)?.[1] ?? Date.now());
  const s = { cookie, secretKey, jwt, clockSkewMs: serverMs - Date.now(), expMs: jwtExpMs(jar.band_session) };
  mkdirSync(DIR, { recursive: true, mode: 0o700 });
  writeFileSync(FILE, JSON.stringify(s), { mode: 0o600 });
  return s;
}

async function session(force) {
  if (!force) {
    try {
      const s = JSON.parse(readFileSync(FILE, 'utf8'));
      if (s.expMs - Date.now() > 10 * 60_000) return s;
    } catch { /* no cache yet */ }
  }
  return capture();
}

function sign(s, endpoint, params) {
  const qs = new URLSearchParams({ ts: String(Date.now() + (s.clockSkewMs || 0)), ...params })
    .toString().replace(/'/g, '%27');
  const path = `${endpoint}?${qs}`;
  const key = s.jwt ? Buffer.from(s.secretKey, 'base64url') : Buffer.from(s.secretKey, 'utf8');
  return { path, md: createHmac('sha256', key).update(path).digest('base64') };
}

async function call(s, endpoint, params) {
  const { path, md } = sign(s, endpoint, params);
  const res = await fetch(API + path, {
    headers: {
      cookie: s.cookie, akey: AKEY, md, language: 'en',
      'DEVICE-TIME-ZONE-ID': TZ,
      'DEVICE-TIME-ZONE-MS-OFFSET': String(-new Date().getTimezoneOffset() * 60_000),
      origin: 'https://www.band.us', referer: 'https://www.band.us/',
    },
  });
  const text = await res.text();
  try { return JSON.parse(text); } catch { return { result_code: -res.status, result_data: { message: text.slice(0, 200) } }; }
}

const [cmd, endpoint, ...kv] = process.argv.slice(2);
if (cmd === 'refresh') {
  await session(true);
  process.stderr.write('band-fpx: session captured\n');
  process.exit(0);
}
if (cmd !== 'get' || !endpoint?.startsWith('/v')) {
  die(64, 'usage: band.mjs get </vX.Y.Z/endpoint> [key=value ...] | band.mjs refresh');
}
const params = Object.fromEntries(kv.map((p) => { const i = p.indexOf('='); return i < 0 ? [p, ''] : [p.slice(0, i), p.slice(i + 1)]; }));

let s = await session(false);
let out = await call(s, endpoint, params);
if (out.result_code === 300) { // expired session or stale secret: re-capture once
  s = await session(true);
  out = await call(s, endpoint, params);
}
process.stdout.write(JSON.stringify(out) + '\n');
if (out.result_code !== 1) {
  die(4, out.result_code === 300
    ? 'not authorized (300) — open https://www.band.us/ in the paired browser so it renews the session, then retry'
    : `result_code ${out.result_code}: ${out.result_data?.message ?? ''}`);
}
