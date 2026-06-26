'use strict';

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

function tmpHome() {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-oauth-'));
  process.env.EVOLVER_HOME = d;
  return d;
}

// Fresh require of the module each test (it caches nothing path-related, but
// EVOLVER_HOME is read lazily so this is just for clarity).
function load() {
  delete require.cache[require.resolve('../src/gep/oauthLogin')];
  return require('../src/gep/oauthLogin');
}

function stubHubFetch(routes) {
  const hubFetchMod = require('../src/gep/hubFetch');
  hubFetchMod._setFetchImplForTest(async (url, init) => {
    const body = routes(url, init || {});
    return { status: body.status || 200, json: async () => body.json };
  });
  return () => { hubFetchMod._setFetchImplForTest(null); };
}

test('deviceLogin: device_authorization -> poll (pending then token) -> persists', async () => {
  tmpHome();
  const m = load();
  let polls = 0;
  const restore = stubHubFetch((url) => {
    if (url.endsWith('/oauth/device_authorization')) {
      return { status: 200, json: { device_code: 'DC', user_code: 'AB12-CD34', verification_uri: 'https://evomap.ai/device', interval: 1 } };
    }
    // /oauth/token: pending twice, then success
    polls += 1;
    if (polls < 3) return { status: 400, json: { error: 'authorization_pending' } };
    return { status: 200, json: { access_token: 'AT', refresh_token: 'RT', expires_in: 3600, scope: 'a2a' } };
  });
  try {
    let shown = null;
    const tok = await m.deviceLogin({ hubUrl: 'https://hub.test', sleep: async () => {}, onCode: (c) => { shown = c; } });
    assert.equal(tok.access_token, 'AT');
    assert.equal(tok.refresh_token, 'RT');
    assert.ok(tok.expires_at > Date.now());
    assert.equal(shown.userCode, 'AB12-CD34');
    assert.equal(polls, 3); // 2 pending + 1 success
    assert.equal(m.loadValidAccessToken(), 'AT'); // persisted + valid
  } finally {
    restore();
  }
});

test('loadValidAccessToken: returns null when expired', async () => {
  tmpHome();
  const m = load();
  m.saveOAuthToken({ access_token: 'OLD', expires_at: Date.now() - 1000 });
  assert.equal(m.loadValidAccessToken(), null);
  m.saveOAuthToken({ access_token: 'FRESH', expires_at: Date.now() + 3600_000 });
  assert.equal(m.loadValidAccessToken(), 'FRESH');
});

test('refreshOAuthToken: uses refresh_token grant, updates stored token', async () => {
  tmpHome();
  const m = load();
  m.saveOAuthToken({ access_token: 'AT1', refresh_token: 'RT1', expires_at: Date.now() + 1000 });
  let sentGrant = null;
  let sentRefresh = null;
  const restore = stubHubFetch((_url, init) => {
    const b = JSON.parse(init.body);
    sentGrant = b.grant_type;
    sentRefresh = b.refresh_token;
    return { status: 200, json: { access_token: 'AT2', refresh_token: 'RT2', expires_in: 3600 } };
  });
  try {
    const at = await m.refreshOAuthToken({ hubUrl: 'https://hub.test' });
    assert.equal(at, 'AT2');
    assert.equal(sentGrant, 'refresh_token');
    assert.equal(sentRefresh, 'RT1');
    assert.equal(m.loadOAuthToken().access_token, 'AT2');
  } finally {
    restore();
  }
});

test('refreshOAuthToken: refuses http hub URL before sending refresh token', async () => {
  tmpHome();
  const origInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
  delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
  const m = load();
  m.saveOAuthToken({ access_token: 'AT1', refresh_token: 'RT1', expires_at: Date.now() + 1000 });
  let called = false;
  const restore = stubHubFetch(() => {
    called = true;
    return { status: 200, json: { access_token: 'AT2', expires_in: 3600 } };
  });
  try {
    await assert.rejects(
      () => m.refreshOAuthToken({ hubUrl: 'http://hub.test' }),
      /must use https/i,
    );
    assert.equal(called, false, 'refresh token must not be sent after URL-scheme refusal');
  } finally {
    restore();
    if (origInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = origInsecure;
  }
});

test('buildHubHeaders prefers a valid OAuth token over node_secret', async () => {
  const home = tmpHome();
  const m = load();
  m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
  // node_secret also present in the same EVOLVER_HOME
  fs.writeFileSync(path.join(home, 'node_secret'), 'a'.repeat(64), 'utf8');
  delete require.cache[require.resolve('../src/gep/a2aProtocol')];
  const a2a = require('../src/gep/a2aProtocol');
  const headers = a2a.buildHubHeaders();
  assert.equal(headers.Authorization, 'Bearer OAUTH_AT');
});

test('startTokenAutoRefresh: schedules ~2min before expiry, refreshes, reschedules', async () => {
  tmpHome();
  const m = load();
  const now = Date.now();
  m.saveOAuthToken({ access_token: 'AT1', refresh_token: 'RT1', expires_at: now + 3600_000 });
  let scheduledDelay = null;
  let firedFn = null;
  const fakeSetTimer = (fn, ms) => { scheduledDelay = ms; firedFn = fn; return { unref() {} }; };
  const restore = stubHubFetch(() => ({ status: 200, json: { access_token: 'AT2', refresh_token: 'RT2', expires_in: 3600 } }));
  try {
    const stop = m.startTokenAutoRefresh({ setTimer: fakeSetTimer, clearTimer: () => {}, now: () => now });
    // ~ (3600_000 - 2*60_000) = 3_480_000 ms before expiry
    assert.equal(scheduledDelay, 3_480_000);
    await firedFn(); // simulate the timer firing -> refresh + reschedule
    assert.equal(m.loadOAuthToken().access_token, 'AT2');
    stop();
  } finally {
    restore();
  }
});

test('startTokenAutoRefresh: no-op when there is no refresh token', () => {
  tmpHome();
  const m = load();
  m.saveOAuthToken({ access_token: 'AT', expires_at: Date.now() + 3600_000 }); // no refresh_token
  let scheduled = false;
  m.startTokenAutoRefresh({ setTimer: () => { scheduled = true; return {}; } });
  assert.equal(scheduled, false);
});
