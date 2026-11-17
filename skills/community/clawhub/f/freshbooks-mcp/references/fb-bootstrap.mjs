#!/usr/bin/env node
// FreshBooks OAuth2 bootstrap — authorize URL + code exchange + identity probe.
// Usage:
//   node fb-bootstrap.mjs url      <client_id> [redirect_uri]
//   node fb-bootstrap.mjs exchange <client_id> <client_secret> <redirect_uri> <code|full_redirect_url>
//   node fb-bootstrap.mjs refresh  <client_id> <client_secret> <redirect_uri> <refresh_token>
//   node fb-bootstrap.mjs me       <access_token>
process.stdout.on('error', (e) => { if (e.code === 'EPIPE') process.exit(0); throw e; });

const AUTHORIZE = 'https://auth.freshbooks.com/oauth/authorize/';
const TOKEN = 'https://api.freshbooks.com/auth/oauth/token';
const ME = 'https://api.freshbooks.com/auth/api/v1/users/me';
const DEFAULT_REDIRECT = 'https://localhost';

const die = (msg) => { console.error(`error: ${msg}`); process.exit(1); };

// Accept either a bare code or the whole pasted redirect URL.
function extractCode(input) {
  if (!input) die('no code supplied');
  if (!input.includes('://')) return input.trim();
  let u;
  try { u = new URL(input); } catch { return input.trim(); }
  const code = u.searchParams.get('code');
  if (!code) die(`no ?code= found in the pasted URL. Got: ${u.origin}${u.pathname}${u.search}`);
  return code;
}

async function tokenCall(grantType, codeField, codeValue, clientId, clientSecret, redirectUri) {
  // The official SDK posts this FORM-ENCODED, not JSON.
  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    grant_type: grantType,
    redirect_uri: redirectUri,
    [codeField]: codeValue,
  });
  const res = await fetch(TOKEN, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/json' },
    body,
  });
  const raw = await res.text();
  let json;
  try { json = JSON.parse(raw); } catch { die(`non-JSON token response (HTTP ${res.status}): ${raw.slice(0, 400)}`); }
  if (!res.ok || !json.access_token) {
    die(`token exchange failed (HTTP ${res.status}): ${json.error ?? ''} ${json.error_description ?? raw.slice(0, 300)}`);
  }
  return json;
}

function reportTokens(t) {
  const expiresAt = new Date((t.created_at + t.expires_in) * 1000).toISOString();
  console.error(`access_token expires_in=${t.expires_in}s (at ${expiresAt})`);
  // stdout = data only
  console.log(JSON.stringify({
    access_token: t.access_token,
    refresh_token: t.refresh_token,
    created_at: t.created_at,
    expires_in: t.expires_in,
    expires_at: expiresAt,
  }, null, 2));
}

async function me(accessToken) {
  const res = await fetch(ME, {
    headers: { Authorization: `Bearer ${accessToken}`, 'Api-Version': 'alpha', Accept: 'application/json' },
  });
  const raw = await res.text();
  if (!res.ok) die(`/users/me failed (HTTP ${res.status}): ${raw.slice(0, 400)}`);
  console.log(raw);
}

const [cmd, ...rest] = process.argv.slice(2);
switch (cmd) {
  case 'url': {
    const [clientId, redirectUri = DEFAULT_REDIRECT] = rest;
    if (!clientId) die('usage: url <client_id> [redirect_uri]');
    const p = new URLSearchParams({ client_id: clientId, response_type: 'code', redirect_uri: redirectUri });
    console.log(`${AUTHORIZE}?${p}`);
    break;
  }
  case 'exchange': {
    const [clientId, clientSecret, redirectUri, codeOrUrl] = rest;
    if (!clientId || !clientSecret || !redirectUri || !codeOrUrl) {
      die('usage: exchange <client_id> <client_secret> <redirect_uri> <code|full_redirect_url>');
    }
    reportTokens(await tokenCall('authorization_code', 'code', extractCode(codeOrUrl), clientId, clientSecret, redirectUri));
    break;
  }
  case 'refresh': {
    const [clientId, clientSecret, redirectUri, refreshToken] = rest;
    if (!clientId || !clientSecret || !redirectUri || !refreshToken) {
      die('usage: refresh <client_id> <client_secret> <redirect_uri> <refresh_token>');
    }
    reportTokens(await tokenCall('refresh_token', 'refresh_token', refreshToken, clientId, clientSecret, redirectUri));
    break;
  }
  case 'me': {
    const [accessToken] = rest;
    if (!accessToken) die('usage: me <access_token>');
    await me(accessToken);
    break;
  }
  default:
    die('usage: url | exchange | refresh | me   (see header comment)');
}
