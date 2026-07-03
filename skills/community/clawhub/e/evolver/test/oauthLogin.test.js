'use strict';

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const NODE_SECRET_A = 'a'.repeat(64);
const NODE_SECRET_B = 'b'.repeat(64);
const HUB_CREDENTIAL_ENV_KEYS = [
  'A2A_NODE_SECRET',
  'EVOMAP_NODE_SECRET',
  'A2A_HUB_TOKEN',
  'A2A_NODE_SECRET_VERSION',
  'EVOMAP_NODE_SECRET_VERSION',
];

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

function loadA2A() {
  delete require.cache[require.resolve('../src/gep/a2aProtocol')];
  const a2a = require('../src/gep/a2aProtocol');
  if (a2a._testing && typeof a2a._testing._resetHubNodeSecretStateForTesting === 'function') {
    a2a._testing._resetHubNodeSecretStateForTesting();
  }
  return a2a;
}

function saveEnv(keys) {
  const saved = {};
  for (const key of keys) saved[key] = process.env[key];
  return saved;
}

function restoreEnv(saved) {
  for (const [key, value] of Object.entries(saved)) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
}

function clearHubCredentialEnv() {
  for (const key of HUB_CREDENTIAL_ENV_KEYS) delete process.env[key];
}

function getNodeScopedHubHeaders(a2a) {
  const fn = a2a.buildNodeScopedHubHeaders
    || a2a.buildNodeHubHeaders
    || a2a.buildNodeScopedHeaders;
  if (typeof fn !== 'function') {
    throw new Error('a2aProtocol must export a node-scoped hub header helper');
  }
  return fn.call(a2a);
}

function loadHubSearch() {
  delete require.cache[require.resolve('../src/gep/hubSearch')];
  return require('../src/gep/hubSearch');
}

function loadPrivacyClient() {
  delete require.cache[require.resolve('../src/gep/privacyClient')];
  return require('../src/gep/privacyClient');
}

function loadDirectoryClient() {
  delete require.cache[require.resolve('../src/gep/directoryClient')];
  return require('../src/gep/directoryClient');
}

function assertBearer(headers, token) {
  if (!headers || headers.Authorization !== 'Bearer ' + token) {
    throw new Error('unexpected Authorization bearer');
  }
}

function assertNotBearer(headers, token) {
  if (headers && headers.Authorization === 'Bearer ' + token) {
    throw new Error('unexpected node-scoped bearer source');
  }
}

function writeLegacyNodeSecret(home, secret, version, source) {
  fs.writeFileSync(path.join(home, 'node_secret'), secret, 'utf8');
  if (version) fs.writeFileSync(path.join(home, 'node_secret_version'), String(version), 'utf8');
  if (source) fs.writeFileSync(path.join(home, 'node_secret_source'), source, 'utf8');
}

function writeMailboxState(home, state) {
  const mailboxDir = path.join(home, 'mailbox');
  fs.mkdirSync(mailboxDir, { recursive: true, mode: 0o700 });
  fs.writeFileSync(
    path.join(mailboxDir, 'state.json'),
    JSON.stringify(Object.assign({ _schema_version: 1 }, state), null, 2) + '\n',
    { encoding: 'utf8', mode: 0o600 },
  );
}

function stubHubFetch(routes) {
  const hubFetchMod = require('../src/gep/hubFetch');
  hubFetchMod._setFetchImplForTest(async (url, init) => {
    const body = routes(url, init || {});
    const status = body.status || 200;
    return {
      ok: status >= 200 && status < 300,
      status,
      json: async () => body.json,
      text: async () => (typeof body.text === 'string' ? body.text : JSON.stringify(body.json || {})),
    };
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

test('hub header helpers keep user-scoped OAuth separate from node-scoped node_secret', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS);
  const m = load();
  try {
    clearHubCredentialEnv();
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    const a2a = loadA2A();

    assert.equal(a2a.buildHubHeaders().Authorization, 'Bearer OAUTH_AT');
    assertBearer(getNodeScopedHubHeaders(a2a), NODE_SECRET_A);
  } finally {
    restoreEnv(savedEnv);
  }
});

test('http transport send uses node-scoped auth when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL']));
  const m = load();
  let sentHeaders = null;
  const restoreFetch = stubHubFetch((_url, init) => {
    sentHeaders = init.headers || {};
    return { status: 200, json: { status: 'ok' } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    const a2a = loadA2A();
    const msg = a2a.buildMessage({ messageType: 'hello', payload: {} });

    const result = await a2a.httpTransportSend(msg, {});
    assert.equal(result.ok, true);
    assertBearer(sentHeaders, NODE_SECRET_A);
    assertNotBearer(sentHeaders, 'OAUTH_AT');
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('agent audit GET uses node-scoped auth when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const m = load();
  let sentUrl = null;
  let sentHeaders = null;
  const restoreFetch = stubHubFetch((url, init) => {
    sentUrl = url;
    sentHeaders = init.headers || {};
    return { status: 200, json: { entries: [] } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    const a2a = loadA2A();

    const result = await a2a.hubGetAuditLogs({});
    assert.equal(result.ok, true);
    assertBearer(sentHeaders, NODE_SECRET_A);
    assertNotBearer(sentHeaders, 'OAUTH_AT');
    assert.equal(new URL(sentUrl).searchParams.get('node_id'), 'node_abcdef123456');
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('agent work report GET uses node-scoped auth and node identity when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const m = load();
  let sentUrl = null;
  let sentHeaders = null;
  const restoreFetch = stubHubFetch((url, init) => {
    sentUrl = url;
    sentHeaders = init.headers || {};
    return { status: 200, json: { report: {} } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    const a2a = loadA2A();

    const result = await a2a.hubGetWorkReport({ days: 3 });

    assert.equal(result.ok, true);
    assertBearer(sentHeaders, NODE_SECRET_A);
    assertNotBearer(sentHeaders, 'OAUTH_AT');
    const parsed = new URL(sentUrl);
    assert.equal(parsed.searchParams.get('node_id'), 'node_abcdef123456');
    assert.equal(parsed.searchParams.get('days'), '3');
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('directory search uses node-scoped auth and node identity when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const m = load();
  const calls = [];
  const restoreFetch = stubHubFetch((url, init) => {
    calls.push({ url, headers: init.headers || {} });
    return { status: 200, json: { results: [] } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    loadA2A();
    const directoryClient = loadDirectoryClient();

    await directoryClient.searchByQuery('planner', { limit: 2 });
    await directoryClient.searchBySignals(['planning', 'agent'], { limit: 4 });

    assert.equal(calls.length, 2);
    assert.equal(new URL(calls[0].url).searchParams.get('node_id'), 'node_abcdef123456');
    assert.equal(new URL(calls[1].url).searchParams.get('node_id'), 'node_abcdef123456');
    assert.equal(new URL(calls[0].url).searchParams.get('limit'), '2');
    assert.equal(new URL(calls[1].url).searchParams.get('limit'), '4');
    for (const call of calls) {
      assertBearer(call.headers, NODE_SECRET_A);
      assertNotBearer(call.headers, 'OAUTH_AT');
    }
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('graft GET requests use node-scoped auth and node identity when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const m = load();
  const calls = [];
  const restoreFetch = stubHubFetch((url, init) => {
    calls.push({ url, headers: init.headers || {}, method: init.method });
    if (url.includes('/a2a/graft/task/')) {
      return { status: 200, json: { status: 'ok', best: null, snapshots: [] } };
    }
    return {
      status: 200,
      json: {
        status: 'ok',
        snapshot: { id: 'snap_1', task_id: 'task_1', source_node_id: 'node_source', score: 0.9 },
      },
    };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    loadA2A();
    const hubSearch = loadHubSearch();

    const graft = await hubSearch.graftFromBreakthrough('snap_1');
    const list = await hubSearch.listGraftSnapshots('task_1');

    assert.equal(graft.ok, true);
    assert.equal(list.ok, true);
    assert.equal(calls.length, 2);
    for (const call of calls) {
      assert.equal(call.method, 'GET');
      assertBearer(call.headers, NODE_SECRET_A);
      assertNotBearer(call.headers, 'OAUTH_AT');
      assert.equal(new URL(call.url).searchParams.get('node_id'), 'node_abcdef123456');
    }
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('privacy tool templates use node-scoped auth and node identity when OAuth token exists', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const m = load();
  let sentUrl = null;
  let sentHeaders = null;
  const restoreFetch = stubHubFetch((url, init) => {
    sentUrl = url;
    sentHeaders = init.headers || {};
    return { status: 200, json: { templates: [] } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    m.saveOAuthToken({ access_token: 'OAUTH_AT', expires_at: Date.now() + 3600_000 });
    writeLegacyNodeSecret(home, NODE_SECRET_A);
    loadA2A();
    const privacyClient = loadPrivacyClient();

    const templates = await privacyClient.getToolTemplates();

    assert.deepEqual(templates, []);
    assertBearer(sentHeaders, NODE_SECRET_A);
    assertNotBearer(sentHeaders, 'OAUTH_AT');
    assert.equal(new URL(sentUrl).searchParams.get('node_id'), 'node_abcdef123456');
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('diverged mailbox node_secret is cleared before unauthenticated re-hello', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const calls = [];
  const restoreFetch = stubHubFetch((_url, init) => {
    const msg = JSON.parse(init.body || '{}');
    calls.push({
      rotate: Boolean(msg && msg.payload && msg.payload.rotate_secret),
      authorization: init.headers && init.headers.Authorization,
    });
    if (msg && msg.payload && msg.payload.rotate_secret) {
      return { status: 401, text: '{"error":"node_secret_invalid"}' };
    }
    if (init.headers && init.headers.Authorization) {
      return { status: 401, text: '{"error":"node_secret_invalid"}' };
    }
    return { status: 200, json: { payload: { node_secret: NODE_SECRET_B, node_secret_version: 9 } } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    writeMailboxState(home, {
      node_secret: NODE_SECRET_A,
      node_secret_version: '4',
      node_secret_source: 'hub_rotate',
    });
    const a2a = loadA2A();

    const rotate = await a2a.rotateNodeSecret();
    const clearedState = JSON.parse(fs.readFileSync(path.join(home, 'mailbox', 'state.json'), 'utf8'));
    const hello = await a2a.sendHelloToHub();

    assert.equal(rotate.ok, false);
    assert.equal(rotate.error, 'secret_diverged_cleared');
    assert.equal(clearedState.node_secret, '');
    assert.equal(clearedState.node_secret_version, '');
    assert.equal(clearedState.node_secret_source, '');
    assert.equal(hello.ok, true);
    assert.equal(calls.length, 2);
    assert.equal(calls[0].authorization, 'Bearer ' + NODE_SECRET_A);
    assert.equal(calls[1].authorization, undefined);
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('hub-rotated mailbox state is updated when rotate returns a new node_secret', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS.concat(['A2A_HUB_URL', 'A2A_NODE_ID']));
  const restoreFetch = stubHubFetch((_url, init) => {
    const msg = JSON.parse(init.body || '{}');
    assert.equal(Boolean(msg && msg.payload && msg.payload.rotate_secret), true);
    assert.equal(init.headers.Authorization, 'Bearer ' + NODE_SECRET_A);
    return { status: 200, json: { payload: { node_secret: NODE_SECRET_B, node_secret_version: 11 } } };
  });
  try {
    clearHubCredentialEnv();
    process.env.A2A_HUB_URL = 'https://hub.test';
    process.env.A2A_NODE_ID = 'node_abcdef123456';
    writeMailboxState(home, {
      node_secret: NODE_SECRET_A,
      node_secret_version: '10',
      node_secret_source: 'hub_rotate',
    });
    writeLegacyNodeSecret(home, NODE_SECRET_A, '10', 'hub_rotate');
    const a2a = loadA2A();

    const rotate = await a2a.rotateNodeSecret();
    const storedState = JSON.parse(fs.readFileSync(path.join(home, 'mailbox', 'state.json'), 'utf8'));
    const freshA2a = loadA2A();
    const headers = getNodeScopedHubHeaders(freshA2a);

    assert.equal(rotate.ok, true);
    assert.equal(storedState.node_secret, NODE_SECRET_B);
    assert.equal(storedState.node_secret_version, '11');
    assert.equal(storedState.node_secret_source, 'hub_rotate');
    assertBearer(headers, NODE_SECRET_B);
    assert.equal(headers['X-EvoMap-Node-Secret-Version'], '11');
  } finally {
    restoreFetch();
    restoreEnv(savedEnv);
  }
});

test('node-scoped hub headers read node_secret from mailbox state', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS);
  try {
    clearHubCredentialEnv();
    writeMailboxState(home, {
      node_secret: NODE_SECRET_A,
      node_secret_version: '3',
    });
    const a2a = loadA2A();

    const headers = getNodeScopedHubHeaders(a2a);
    assertBearer(headers, NODE_SECRET_A);
    assert.equal(headers['X-EvoMap-Node-Secret-Version'], '3');
  } finally {
    restoreEnv(savedEnv);
  }
});

test('node-scoped hub headers prefer hub-rotated mailbox state over stale env', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS);
  try {
    clearHubCredentialEnv();
    process.env.A2A_NODE_SECRET = NODE_SECRET_A;
    process.env.A2A_NODE_SECRET_VERSION = '1';
    writeMailboxState(home, {
      node_secret: NODE_SECRET_B,
      node_secret_version: '4',
      node_secret_source: 'hub_rotate',
    });
    const a2a = loadA2A();

    const headers = getNodeScopedHubHeaders(a2a);
    assertBearer(headers, NODE_SECRET_B);
    assertNotBearer(headers, NODE_SECRET_A);
    assert.equal(headers['X-EvoMap-Node-Secret-Version'], '4');
  } finally {
    restoreEnv(savedEnv);
  }
});

test('node-scoped hub headers keep env fallback when mailbox source is not hub_rotate', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS);
  try {
    clearHubCredentialEnv();
    process.env.A2A_NODE_SECRET = NODE_SECRET_A;
    process.env.A2A_NODE_SECRET_VERSION = '2';
    writeMailboxState(home, {
      node_secret: NODE_SECRET_B,
      node_secret_version: '4',
      node_secret_source: 'env_seed',
    });
    const a2a = loadA2A();

    const headers = getNodeScopedHubHeaders(a2a);
    assertBearer(headers, NODE_SECRET_A);
    assertNotBearer(headers, NODE_SECRET_B);
    assert.equal(headers['X-EvoMap-Node-Secret-Version'], '2');
  } finally {
    restoreEnv(savedEnv);
  }
});

test('node-scoped hub headers keep legacy node_secret fallback when mailbox state is absent', async () => {
  const home = tmpHome();
  const savedEnv = saveEnv(HUB_CREDENTIAL_ENV_KEYS);
  try {
    clearHubCredentialEnv();
    writeLegacyNodeSecret(home, NODE_SECRET_B, '5', 'hub_rotate');
    const a2a = loadA2A();

    const headers = getNodeScopedHubHeaders(a2a);
    assertBearer(headers, NODE_SECRET_B);
    assert.equal(headers['X-EvoMap-Node-Secret-Version'], '5');
  } finally {
    restoreEnv(savedEnv);
  }
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
