const { describe, it, before, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
if (!process.env.A2A_NODE_SECRET) {
  process.env.A2A_NODE_SECRET = 'a'.repeat(64);
}
const {
  PROTOCOL_NAME,
  PROTOCOL_VERSION,
  VALID_MESSAGE_TYPES,
  buildMessage,
  buildHello,
  buildPublish,
  buildFetch,
  buildReport,
  buildDecision,
  buildRevoke,
  isValidProtocolMessage,
  unwrapAssetFromMessage,
  sendHelloToHub,
  rotateNodeSecret,
  sendHeartbeat,
  hubOpenEventStream,
  getHubNodeSecret,
  getHubNodeSecretVersion,
  mergeAndCap,
  httpTransportSend,
  httpTransportReceive,
} = require('../src/gep/a2aProtocol');
const {
  _resetCachedNodeIdForTesting,
  _resetDryRunWarnedForTesting,
  _resetHubNodeSecretStateForTesting,
} = require('../src/gep/a2aProtocol')._testing;
const { computeAssetId } = require('../src/gep/contentHash');
const { MailboxStore } = require('../src/proxy/mailbox/store');

function suppressionMarker(secret) {
  return 'sha256:' + crypto.createHash('sha256').update(secret.toLowerCase()).digest('hex');
}

function assertNoRawHubResponseSecrets(logText, raw) {
  assert.equal(logText.includes(raw.nodeSecret), false, 'raw node_secret value must not be logged');
  assert.equal(logText.includes(raw.bearer), false, 'raw Bearer token must not be logged');
  assert.equal(logText.includes(raw.token), false, 'raw token field value must not be logged');
  assert.equal(logText.includes(raw.envPath), false, 'raw .env path must not be logged');
  assert.equal(logText.includes(raw.body), false, 'raw Hub response body must not be logged verbatim');
}

describe('protocol constants', () => {
  it('has expected protocol name', () => {
    assert.equal(PROTOCOL_NAME, 'gep-a2a');
  });

  it('has 6 valid message types', () => {
    assert.equal(VALID_MESSAGE_TYPES.length, 6);
    for (const t of ['hello', 'publish', 'fetch', 'report', 'decision', 'revoke']) {
      assert.ok(VALID_MESSAGE_TYPES.includes(t), `missing type: ${t}`);
    }
  });
});

describe('buildMessage', () => {
  it('builds a valid protocol message', () => {
    const msg = buildMessage({ messageType: 'hello', payload: { test: true } });
    assert.equal(msg.protocol, PROTOCOL_NAME);
    assert.equal(msg.message_type, 'hello');
    assert.ok(msg.message_id.startsWith('msg_'));
    assert.ok(msg.timestamp);
    assert.deepEqual(msg.payload, { test: true });
  });

  it('rejects invalid message type', () => {
    assert.throws(() => buildMessage({ messageType: 'invalid' }), /Invalid message type/);
  });
});

describe('typed message builders', () => {
  var _origNodeSecret;
  before(() => {
    _origNodeSecret = process.env.A2A_NODE_SECRET;
    process.env.A2A_NODE_SECRET = 'test-secret-for-signing';
  });
  after(() => {
    if (_origNodeSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = _origNodeSecret;
  });

  it('buildHello includes env_fingerprint', () => {
    const msg = buildHello({});
    assert.equal(msg.message_type, 'hello');
    assert.ok(msg.payload.env_fingerprint);
  });

  it('buildHello includes name when provided', () => {
    const msg = buildHello({ name: 'My Agent' });
    assert.equal(msg.payload.name, 'My Agent');
  });

  it('buildHello omits name when empty or missing', () => {
    const msg1 = buildHello({});
    assert.equal(msg1.payload.name, undefined);
    const msg2 = buildHello({ name: '   ' });
    assert.equal(msg2.payload.name, undefined);
  });

  it('buildHello truncates name to 32 chars', () => {
    const long = 'A'.repeat(50);
    const msg = buildHello({ name: long });
    assert.equal(msg.payload.name.length, 32);
  });

  it('buildPublish requires asset with type and id', () => {
    assert.throws(() => buildPublish({}), /asset must have type and id/);
    assert.throws(() => buildPublish({ asset: { type: 'Gene' } }), /asset must have type and id/);

    const msg = buildPublish({ asset: { type: 'Gene', id: 'g1' } });
    assert.equal(msg.message_type, 'publish');
    assert.equal(msg.payload.asset_type, 'Gene');
    assert.equal(msg.payload.local_id, 'g1');
    assert.ok(msg.payload.signature);
  });

  it('buildFetch creates a fetch message', () => {
    const msg = buildFetch({ assetType: 'Capsule', localId: 'c1' });
    assert.equal(msg.message_type, 'fetch');
    assert.equal(msg.payload.asset_type, 'Capsule');
  });

  // The three optional fields below are not cosmetic: their presence/absence
  // drives Hub-side behavior (search_only / asset_ids select the free vs paid
  // fetch path; signals scope the search). They must be OMITTED — not sent as
  // empty/false — when the input is empty/falsy, so assert with the `in`
  // operator on payload, not on values.
  it('buildFetch omits optional fields when not provided', () => {
    const msg = buildFetch({ assetType: 'Capsule', localId: 'c1' });
    assert.equal('signals' in msg.payload, false);
    assert.equal('search_only' in msg.payload, false);
    assert.equal('asset_ids' in msg.payload, false);
  });

  it('buildFetch includes signals only when a non-empty array', () => {
    assert.equal('signals' in buildFetch({ signals: [] }).payload, false);
    assert.equal('signals' in buildFetch({ signals: null }).payload, false);
    const msg = buildFetch({ signals: ['log_error', 'perf'] });
    assert.deepEqual(msg.payload.signals, ['log_error', 'perf']);
  });

  it('buildFetch sets search_only only for an exact boolean true', () => {
    assert.equal('search_only' in buildFetch({ searchOnly: false }).payload, false);
    assert.equal('search_only' in buildFetch({ searchOnly: 'true' }).payload, false);
    assert.equal(buildFetch({ searchOnly: true }).payload.search_only, true);
  });

  it('buildFetch includes asset_ids only when a non-empty array', () => {
    assert.equal('asset_ids' in buildFetch({ assetIds: [] }).payload, false);
    assert.equal('asset_ids' in buildFetch({ assetIds: null }).payload, false);
    const msg = buildFetch({ assetIds: ['sha256:a', 'sha256:b'] });
    assert.deepEqual(msg.payload.asset_ids, ['sha256:a', 'sha256:b']);
  });

  it('buildReport creates a report message', () => {
    const msg = buildReport({ assetId: 'sha256:abc', validationReport: { ok: true } });
    assert.equal(msg.message_type, 'report');
    assert.equal(msg.payload.target_asset_id, 'sha256:abc');
  });

  it('buildDecision validates decision values', () => {
    assert.throws(() => buildDecision({ decision: 'maybe' }), /decision must be/);

    for (const d of ['accept', 'reject', 'quarantine']) {
      const msg = buildDecision({ decision: d, assetId: 'test' });
      assert.equal(msg.payload.decision, d);
    }
  });

  it('buildRevoke creates a revoke message', () => {
    const msg = buildRevoke({ assetId: 'sha256:abc', reason: 'outdated' });
    assert.equal(msg.message_type, 'revoke');
    assert.equal(msg.payload.reason, 'outdated');
  });
});

describe('isValidProtocolMessage', () => {
  it('returns true for well-formed messages', () => {
    const msg = buildHello({});
    assert.ok(isValidProtocolMessage(msg));
  });

  it('returns false for null/undefined', () => {
    assert.ok(!isValidProtocolMessage(null));
    assert.ok(!isValidProtocolMessage(undefined));
  });

  it('returns false for wrong protocol', () => {
    assert.ok(!isValidProtocolMessage({ protocol: 'other', message_type: 'hello', message_id: 'x', timestamp: 'y' }));
  });

  it('returns false for missing fields', () => {
    assert.ok(!isValidProtocolMessage({ protocol: PROTOCOL_NAME }));
  });
});

describe('unwrapAssetFromMessage', () => {
  var _origNodeSecret;
  before(() => {
    _origNodeSecret = process.env.A2A_NODE_SECRET;
    process.env.A2A_NODE_SECRET = 'test-secret-for-signing';
  });
  after(() => {
    if (_origNodeSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = _origNodeSecret;
  });

  it('extracts asset from publish message', () => {
    const asset = { type: 'Gene', id: 'g1', strategy: ['test'] };
    const msg = buildPublish({ asset });
    const result = unwrapAssetFromMessage(msg);
    assert.equal(result.type, 'Gene');
    assert.equal(result.id, 'g1');
  });

  it('returns plain asset objects as-is', () => {
    const gene = { type: 'Gene', id: 'g1' };
    assert.deepEqual(unwrapAssetFromMessage(gene), gene);

    const capsule = { type: 'Capsule', id: 'c1' };
    assert.deepEqual(unwrapAssetFromMessage(capsule), capsule);
  });

  it('returns null for unrecognized input', () => {
    assert.equal(unwrapAssetFromMessage(null), null);
    assert.equal(unwrapAssetFromMessage({ random: true }), null);
    assert.equal(unwrapAssetFromMessage('string'), null);
  });
});

describe('sendHeartbeat log touch', () => {
  var tmpDir;
  var originalFetch;
  var originalHubUrl;
  var originalLogsDir;
  var originalInsecure;
  var originalEvolverHome;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-hb-test-'));
    originalHubUrl = process.env.A2A_HUB_URL;
    originalLogsDir = process.env.EVOLVER_LOGS_DIR;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    originalEvolverHome = process.env.EVOLVER_HOME;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
    process.env.EVOLVER_HOME = path.join(tmpDir, '.evomap');
    // hubFetch enforces https:// by default; tests use a fake http URL with
    // a stubbed fetch, so opt into insecure mode to bypass URL validation
    // and have hubFetch route through global.fetch (where the stub lives).
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    originalFetch = global.fetch;
  });

  after(() => {
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) {
      delete process.env.A2A_HUB_URL;
    } else {
      process.env.A2A_HUB_URL = originalHubUrl;
    }
    if (originalLogsDir === undefined) {
      delete process.env.EVOLVER_LOGS_DIR;
    } else {
      process.env.EVOLVER_LOGS_DIR = originalLogsDir;
    }
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
    if (originalEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = originalEvolverHome;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    _resetHubNodeSecretStateForTesting();
    fs.mkdirSync(process.env.EVOLVER_HOME, { recursive: true });
  });

  afterEach(() => {
    _resetHubNodeSecretStateForTesting();
  });

  it('updates mtime of existing evolver_loop.log on successful heartbeat', async () => {
    var logPath = path.join(tmpDir, 'evolver_loop.log');
    fs.writeFileSync(logPath, '');
    var oldTime = new Date(Date.now() - 5000);
    fs.utimesSync(logPath, oldTime, oldTime);

    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok, 'heartbeat should succeed');

    var mtime = fs.statSync(logPath).mtimeMs;
    assert.ok(mtime > oldTime.getTime(), 'mtime should be newer than the pre-set old time');
  });

  it('creates evolver_loop.log when it does not exist on successful heartbeat', async () => {
    var logPath = path.join(tmpDir, 'evolver_loop.log');
    if (fs.existsSync(logPath)) fs.unlinkSync(logPath);

    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
      text: async () => '',
    });

    var result = await sendHeartbeat();
    assert.ok(result.ok, 'heartbeat should succeed');
    assert.ok(fs.existsSync(logPath), 'evolver_loop.log should be created when missing');
  });

  it('sends node_secret_version on heartbeat headers and body', async () => {
    var savedVersion = process.env.A2A_NODE_SECRET_VERSION;
    var captured = null;
    try {
      process.env.A2A_NODE_SECRET_VERSION = '9';
      global.fetch = async (url, opts) => {
        captured = { url, opts, body: JSON.parse(opts.body) };
        return {
          ok: true,
          status: 200,
          json: async () => ({ status: 'ok' }),
          text: async () => '',
        };
      };

      var result = await sendHeartbeat();
      assert.ok(result.ok, 'heartbeat should succeed');
      assert.equal(getHubNodeSecretVersion(), 9);
      assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '9');
      assert.equal(captured.body.node_secret_version, 9);
      assert.equal(captured.body.meta.node_secret_version, 9);
    } finally {
      if (savedVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
      else process.env.A2A_NODE_SECRET_VERSION = savedVersion;
    }
  });

  it('does not reuse persisted node_secret_version for a different env secret', async () => {
    var savedSecret = process.env.A2A_NODE_SECRET;
    var savedVersion = process.env.A2A_NODE_SECRET_VERSION;
    var savedEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
    try {
      fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'a'.repeat(64));
      fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '7');
      process.env.A2A_NODE_SECRET = 'b'.repeat(64);
      delete process.env.A2A_NODE_SECRET_VERSION;
      delete process.env.EVOMAP_NODE_SECRET_VERSION;

      assert.equal(getHubNodeSecretVersion(), null);
    } finally {
      if (savedSecret === undefined) delete process.env.A2A_NODE_SECRET;
      else process.env.A2A_NODE_SECRET = savedSecret;
      if (savedVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
      else process.env.A2A_NODE_SECRET_VERSION = savedVersion;
      if (savedEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
      else process.env.EVOMAP_NODE_SECRET_VERSION = savedEvoVersion;
    }
  });

  it('uses rotated secret and version on heartbeat retry when env secret is stale', async () => {
    var savedSecret = process.env.A2A_NODE_SECRET;
    var savedVersion = process.env.A2A_NODE_SECRET_VERSION;
    var savedEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
    var savedNodeId = process.env.A2A_NODE_ID;
    var savedEvolverHome = process.env.EVOLVER_HOME;
    var tempHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-hb-reauth-'));
    try {
      _resetCachedNodeIdForTesting();
      _resetHubNodeSecretStateForTesting();
      process.env.EVOLVER_HOME = path.join(tempHome, '.evomap');
      process.env.A2A_NODE_ID = 'node_aaaaaaaaaaaa';
      process.env.A2A_NODE_SECRET = 'a'.repeat(64);
      process.env.A2A_NODE_SECRET_VERSION = '1';
      delete process.env.EVOMAP_NODE_SECRET_VERSION;
      fs.mkdirSync(process.env.EVOLVER_HOME, { recursive: true });
      fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'a'.repeat(64));
      fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '1');

      var heartbeatCalls = [];
      global.fetch = async (url, opts) => {
        if (String(url).includes('/a2a/heartbeat')) {
          heartbeatCalls.push({
            headers: opts.headers,
            body: JSON.parse(opts.body),
          });
          if (heartbeatCalls.length === 1) {
            return {
              ok: false,
              status: 403,
              json: async () => ({ error: 'node_secret_invalid' }),
              text: async () => JSON.stringify({ error: 'node_secret_invalid' }),
            };
          }
          return {
            ok: true,
            status: 200,
            json: async () => ({ status: 'ok' }),
            text: async () => '',
          };
        }
        if (String(url).includes('/a2a/hello')) {
          return {
            ok: true,
            status: 200,
            json: async () => ({
              payload: {
                status: 'acknowledged',
                node_secret: 'b'.repeat(64),
                node_secret_version: 4,
                your_node_id: 'node_aaaaaaaaaaaa',
              },
            }),
            text: async () => '',
          };
        }
        throw new Error('unexpected fetch URL: ' + url);
      };

      var result = await sendHeartbeat();

      assert.equal(result.ok, true);
      assert.equal(heartbeatCalls.length, 2, 'expected initial heartbeat plus retry');
      assert.equal(heartbeatCalls[0].headers.Authorization, 'Bearer ' + 'a'.repeat(64));
      assert.equal(heartbeatCalls[0].headers['X-EvoMap-Node-Secret-Version'], '1');
      assert.equal(heartbeatCalls[0].body.node_secret_version, 1);
      assert.equal(heartbeatCalls[0].body.meta.node_secret_version, 1);
      assert.equal(heartbeatCalls[1].headers.Authorization, 'Bearer ' + 'b'.repeat(64));
      assert.equal(heartbeatCalls[1].headers['X-EvoMap-Node-Secret-Version'], '4');
      assert.equal(heartbeatCalls[1].body.node_secret_version, 4);
      assert.equal(heartbeatCalls[1].body.meta.node_secret_version, 4);
      assert.equal(getHubNodeSecret(), 'b'.repeat(64));
      assert.equal(getHubNodeSecretVersion(), 4);
    } finally {
      _resetHubNodeSecretStateForTesting();
      _resetCachedNodeIdForTesting();
      fs.rmSync(tempHome, { recursive: true, force: true });
      if (savedSecret === undefined) delete process.env.A2A_NODE_SECRET;
      else process.env.A2A_NODE_SECRET = savedSecret;
      if (savedVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
      else process.env.A2A_NODE_SECRET_VERSION = savedVersion;
      if (savedEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
      else process.env.EVOMAP_NODE_SECRET_VERSION = savedEvoVersion;
      if (savedNodeId === undefined) delete process.env.A2A_NODE_ID;
      else process.env.A2A_NODE_ID = savedNodeId;
      if (savedEvolverHome === undefined) delete process.env.EVOLVER_HOME;
      else process.env.EVOLVER_HOME = savedEvolverHome;
    }
  });

  it('clears diverged local secret on heartbeat 401 followed by rotate hello 401', async () => {
    var savedSecret = process.env.A2A_NODE_SECRET;
    var savedEvoSecret = process.env.EVOMAP_NODE_SECRET;
    var savedVersion = process.env.A2A_NODE_SECRET_VERSION;
    var savedEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
    var savedNodeId = process.env.A2A_NODE_ID;
    var secretFile = path.join(process.env.EVOLVER_HOME, 'node_secret');
    var versionFile = path.join(process.env.EVOLVER_HOME, 'node_secret_version');
    var sourceFile = path.join(process.env.EVOLVER_HOME, 'node_secret_source');
    var suppressionFile = path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed');
    var logPath = path.join(tmpDir, 'evolver_loop.log');
    try {
      _resetCachedNodeIdForTesting();
      _resetHubNodeSecretStateForTesting();
      process.env.A2A_NODE_ID = 'node_aaaaaaaaaaaa';
      process.env.A2A_NODE_SECRET = 'a'.repeat(64);
      process.env.A2A_NODE_SECRET_VERSION = '1';
      delete process.env.EVOMAP_NODE_SECRET;
      delete process.env.EVOMAP_NODE_SECRET_VERSION;
      fs.rmSync(secretFile, { force: true });
      fs.rmSync(versionFile, { force: true });
      fs.rmSync(sourceFile, { force: true });
      fs.rmSync(suppressionFile, { force: true });
      fs.rmSync(logPath, { force: true });
      fs.writeFileSync(secretFile, 'a'.repeat(64));
      fs.writeFileSync(versionFile, '1');
      fs.writeFileSync(sourceFile, 'hub_rotate');

      var calls = [];
      global.fetch = async (url, opts) => {
        var u = String(url);
        var kind = u.includes('/a2a/heartbeat') ? 'heartbeat'
          : u.includes('/a2a/hello') ? 'hello'
            : 'unknown';
        calls.push({
          kind: kind,
          headers: opts.headers,
          body: JSON.parse(opts.body),
        });
        if (kind === 'heartbeat' || kind === 'hello') {
          return {
            ok: false,
            status: 401,
            json: async () => ({ error: 'node_secret_invalid' }),
            text: async () => JSON.stringify({ error: 'node_secret_invalid' }),
          };
        }
        throw new Error('unexpected fetch URL: ' + url);
      };

      var result = await sendHeartbeat();

      assert.deepEqual(calls.map(function (c) { return c.kind; }), ['heartbeat', 'hello']);
      assert.equal(calls[0].headers.Authorization, 'Bearer ' + 'a'.repeat(64));
      assert.equal(calls[0].headers['X-EvoMap-Node-Secret-Version'], '1');
      assert.equal(calls[0].body.node_secret_version, 1);
      assert.equal(calls[0].body.meta.node_secret_version, 1);
      assert.equal(calls[1].headers.Authorization, 'Bearer ' + 'a'.repeat(64));
      assert.equal(calls[1].headers['X-EvoMap-Node-Secret-Version'], '1');
      assert.equal(calls[1].body.payload.rotate_secret, true);
      assert.equal(result.ok, false);
      assert.equal(result.error, 'secret_diverged_cleared');
      assert.equal(fs.existsSync(secretFile), false, 'diverged node_secret must be removed');
      assert.equal(fs.existsSync(versionFile), false, 'diverged node_secret_version must be removed');
      assert.equal(fs.existsSync(sourceFile), false, 'diverged node_secret_source must be removed');
      assert.equal(fs.readFileSync(suppressionFile, 'utf8'), suppressionMarker('a'.repeat(64)));
      assert.equal(getHubNodeSecret(), null);
      assert.equal(getHubNodeSecretVersion(), null);
      if (fs.existsSync(logPath)) {
        assert.equal(fs.readFileSync(logPath, 'utf8').includes('"type":"heartbeat_ok"'), false);
      }
    } finally {
      _resetHubNodeSecretStateForTesting();
      _resetCachedNodeIdForTesting();
      fs.rmSync(secretFile, { force: true });
      fs.rmSync(versionFile, { force: true });
      fs.rmSync(sourceFile, { force: true });
      fs.rmSync(suppressionFile, { force: true });
      if (savedSecret === undefined) delete process.env.A2A_NODE_SECRET;
      else process.env.A2A_NODE_SECRET = savedSecret;
      if (savedEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
      else process.env.EVOMAP_NODE_SECRET = savedEvoSecret;
      if (savedVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
      else process.env.A2A_NODE_SECRET_VERSION = savedVersion;
      if (savedEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
      else process.env.EVOMAP_NODE_SECRET_VERSION = savedEvoVersion;
      if (savedNodeId === undefined) delete process.env.A2A_NODE_ID;
      else process.env.A2A_NODE_ID = savedNodeId;
    }
  });
});

describe('node_secret_version hello compatibility', () => {
  var originalFetch;
  var originalHubUrl;
  var originalInsecure;
  var originalNodeId;
  var originalSecret;
  var originalEvoSecret;
  var originalVersion;
  var originalEvoVersion;
  var originalEvolverHome;
  var tempHome;

  before(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    originalNodeId = process.env.A2A_NODE_ID;
    originalSecret = process.env.A2A_NODE_SECRET;
    originalEvoSecret = process.env.EVOMAP_NODE_SECRET;
    originalVersion = process.env.A2A_NODE_SECRET_VERSION;
    originalEvoVersion = process.env.EVOMAP_NODE_SECRET_VERSION;
    originalEvolverHome = process.env.EVOLVER_HOME;
  });

  after(() => {
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
    if (originalNodeId === undefined) delete process.env.A2A_NODE_ID;
    else process.env.A2A_NODE_ID = originalNodeId;
    if (originalSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalSecret;
    if (originalEvoSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
    else process.env.EVOMAP_NODE_SECRET = originalEvoSecret;
    if (originalVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalVersion;
    if (originalEvoVersion === undefined) delete process.env.EVOMAP_NODE_SECRET_VERSION;
    else process.env.EVOMAP_NODE_SECRET_VERSION = originalEvoVersion;
    if (originalEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = originalEvolverHome;
  });

  beforeEach(() => {
    tempHome = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-hello-version-'));
    process.env.EVOLVER_HOME = path.join(tempHome, '.evomap');
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    process.env.A2A_NODE_ID = 'node_aaaaaaaaaaaa';
    delete process.env.A2A_NODE_SECRET;
    delete process.env.EVOMAP_NODE_SECRET;
    delete process.env.A2A_NODE_SECRET_VERSION;
    delete process.env.EVOMAP_NODE_SECRET_VERSION;
    fs.mkdirSync(process.env.EVOLVER_HOME, { recursive: true });
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'a'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '7');
    _resetHubNodeSecretStateForTesting();
    _resetCachedNodeIdForTesting();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    _resetHubNodeSecretStateForTesting();
    _resetCachedNodeIdForTesting();
    fs.rmSync(tempHome, { recursive: true, force: true });
  });

  function mailboxDir() {
    return path.join(process.env.EVOLVER_HOME, 'mailbox');
  }

  function mailboxStatePath() {
    return path.join(mailboxDir(), 'state.json');
  }

  function readMailboxState() {
    return JSON.parse(fs.readFileSync(mailboxStatePath(), 'utf8'));
  }

  function seedMailboxSecret(secret, version, source) {
    const store = new MailboxStore(mailboxDir());
    store.setState('node_secret', secret);
    store.setState('node_secret_version', version);
    store.setState('node_secret_source', source);
    return store;
  }

  it('clears persisted node_secret_version when hello succeeds without a version', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ payload: { status: 'acknowledged', your_node_id: 'node_aaaaaaaaaaaa' } }),
      text: async () => '',
    });

    assert.equal(getHubNodeSecretVersion(), 7);
    const result = await sendHelloToHub();

    assert.equal(result.ok, true);
    assert.equal(getHubNodeSecretVersion(), null);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version')), false);
  });

  it('prefers hub-rotated persisted secret and version over stale env after restart', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '4');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '1';
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 4);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'b'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '4');
    assert.equal(captured.body.node_secret_version, 4);
    assert.equal(captured.body.meta.node_secret_version, 4);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'hub_rotate');
  });

  it('does not attach stale env version to a hub-rotated persisted secret', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '4');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    process.env.A2A_NODE_SECRET = 'b'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '1';
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 4);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'b'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '4');
    assert.equal(captured.body.node_secret_version, 4);
    assert.equal(captured.body.meta.node_secret_version, 4);
  });

  it('lets env secret and version win when persisted source is env_seed', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '7');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'env_seed');
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '2';
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'a'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 2);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'a'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '2');
    assert.equal(captured.body.node_secret_version, 2);
    assert.equal(captured.body.meta.node_secret_version, 2);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'utf8'), 'a'.repeat(64));
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '2');
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'env_seed');
  });

  it('lets env secret win when persisted source is missing for legacy installs', async () => {
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '7');
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '2';
    _resetHubNodeSecretStateForTesting();

    assert.equal(getHubNodeSecret(), 'a'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 2);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'utf8'), 'a'.repeat(64));
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '2');
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'env_seed');
  });

  it('stores node_secret_version when hello succeeds without rotating the secret', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        payload: {
          status: 'acknowledged',
          node_secret_version: 9,
          your_node_id: 'node_aaaaaaaaaaaa',
        },
      }),
      text: async () => '',
    });

    const result = await sendHelloToHub();

    assert.equal(result.ok, true);
    assert.equal(getHubNodeSecretVersion(), 9);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '9');
  });

  it('uses newer legacy hub_rotate version when mailbox has the same secret at an older version', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '9');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    seedMailboxSecret('a'.repeat(64), '5', 'hub_rotate').close();
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'a'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 9);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'a'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '9');
    assert.equal(captured.body.node_secret_version, 9);
    assert.equal(captured.body.meta.node_secret_version, 9);
  });

  it('uses newer legacy hub_rotate tuple when mailbox has a different older secret', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'c'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '9');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    seedMailboxSecret('b'.repeat(64), '5', 'hub_rotate').close();
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'c'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 9);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'c'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '9');
    assert.equal(captured.body.node_secret_version, 9);
    assert.equal(captured.body.meta.node_secret_version, 9);
  });

  it('syncs hello-only node_secret_version to legacy and mailbox without changing the secret', async () => {
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '4');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    seedMailboxSecret('b'.repeat(64), '4', 'hub_rotate').close();
    _resetHubNodeSecretStateForTesting();
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        payload: {
          status: 'acknowledged',
          node_secret_version: 12,
          your_node_id: 'node_aaaaaaaaaaaa',
        },
      }),
      text: async () => '',
    });

    const result = await sendHelloToHub();
    const state = readMailboxState();

    assert.equal(result.ok, true);
    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 12);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'utf8'), 'b'.repeat(64));
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '12');
    assert.equal(state.node_secret, 'b'.repeat(64));
    assert.equal(state.node_secret_version, '12');
    assert.equal(state.node_secret_source, 'hub_rotate');
  });

  it('sanitizes sendHelloToHub non-2xx Hub response logs', async () => {
    const raw = {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    };
    raw.body = JSON.stringify({
      error: 'auth_failed',
      node_secret: raw.nodeSecret,
      token: raw.token,
      detail: `${raw.bearer} from ${raw.envPath}`,
    });
    global.fetch = async () => ({
      ok: false,
      status: 503,
      json: async () => ({}),
      text: async () => raw.body,
    });

    const warnings = [];
    const origWarn = console.warn;
    console.warn = function () { warnings.push(Array.prototype.join.call(arguments, ' ')); };
    let result;
    try {
      result = await sendHelloToHub();
    } finally {
      console.warn = origWarn;
    }

    assert.equal(result.ok, false);
    assert.equal(result.error, 'http_503');
    const logText = warnings.join('\n');
    assert.match(logText, /\[Hello\] Hub returned 503:/);
    assert.match(logText, /"node_secret":"\[REDACTED\]"/);
    assertNoRawHubResponseSecrets(logText, raw);
  });

  it('clears persisted node_secret_version when rotate hello returns a secret without a version', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        payload: {
          status: 'acknowledged',
          node_secret: 'b'.repeat(64),
          your_node_id: 'node_aaaaaaaaaaaa',
        },
      }),
      text: async () => '',
    });

    assert.equal(getHubNodeSecretVersion(), 7);
    const result = await rotateNodeSecret();

    assert.equal(result.ok, true);
    assert.equal(getHubNodeSecretVersion(), null);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version')), false);
  });

  it('sanitizes rotateNodeSecret non-2xx Hub response logs', async () => {
    const raw = {
      nodeSecret: 'f'.repeat(64),
      bearer: 'Bearer ' + 'g'.repeat(64),
      token: 'tok_' + 'h'.repeat(40),
      envPath: '.env.local',
    };
    raw.body = JSON.stringify({
      error: 'rotate_failed',
      node_secret: raw.nodeSecret,
      credential: {
        token: raw.token,
      },
      detail: `${raw.bearer} from ${raw.envPath}`,
    });
    global.fetch = async () => ({
      ok: false,
      status: 502,
      json: async () => ({}),
      text: async () => raw.body,
    });

    const warnings = [];
    const origWarn = console.warn;
    console.warn = function () { warnings.push(Array.prototype.join.call(arguments, ' ')); };
    let result;
    try {
      result = await rotateNodeSecret();
    } finally {
      console.warn = origWarn;
    }

    assert.equal(result.ok, false);
    assert.equal(result.error, 'http_502');
    const logText = warnings.join('\n');
    assert.match(logText, /rotate_secret hello returned 502:/);
    assert.match(logText, /"node_secret":"\[REDACTED\]"/);
    assertNoRawHubResponseSecrets(logText, raw);
  });

  it('tags rotated node_secret source as hub_rotate', async () => {
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        payload: {
          status: 'acknowledged',
          node_secret: 'b'.repeat(64),
          node_secret_version: 9,
          your_node_id: 'node_aaaaaaaaaaaa',
        },
      }),
      text: async () => '',
    });

    const result = await rotateNodeSecret();

    assert.equal(result.ok, true);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'hub_rotate');
    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 9);
  });

  it('keeps Hub-rotated mailbox secret when an old MailboxStore writes unrelated state', async () => {
    const oldStore = seedMailboxSecret('a'.repeat(64), '1', 'hub_rotate');
    try {
      global.fetch = async () => ({
        ok: true,
        status: 200,
        json: async () => ({
          payload: {
            status: 'acknowledged',
            node_secret: 'b'.repeat(64),
            node_secret_version: 11,
            your_node_id: 'node_aaaaaaaaaaaa',
          },
        }),
        text: async () => '',
      });

      const result = await rotateNodeSecret();
      assert.equal(result.ok, true);

      oldStore.setState('last_sync_error', 'dummy_unrelated_error');
      const state = readMailboxState();

      assert.equal(state.node_secret, 'b'.repeat(64));
      assert.equal(state.node_secret_version, '11');
      assert.equal(state.node_secret_source, 'hub_rotate');
      assert.equal(state.last_sync_error, 'dummy_unrelated_error');
      assert.equal(oldStore.getState('node_secret'), 'b'.repeat(64));
      assert.equal(oldStore.getState('node_secret_version'), '11');
    } finally {
      oldStore.close();
    }
  });

  it('keeps divergence-cleared mailbox secret when an old MailboxStore writes a cursor', async () => {
    const oldStore = seedMailboxSecret('a'.repeat(64), '1', 'hub_rotate');
    try {
      global.fetch = async () => ({
        ok: true,
        status: 200,
        json: async () => ({
          payload: {
            status: 'rejected',
            reason: 'node_secret_invalid',
          },
        }),
        text: async () => '',
      });

      const result = await rotateNodeSecret();
      assert.equal(result.ok, false);
      assert.equal(result.error, 'secret_diverged_cleared');

      oldStore.setCursor('evomap-hub:outbound_cursor', 'cursor_after_clear');
      const state = readMailboxState();

      assert.equal(state.node_secret, '');
      assert.equal(state.node_secret_version, '');
      assert.equal(state.node_secret_source, '');
      assert.equal(state.node_secret_env_suppressed, '');
      assert.equal(state['cursor:evomap-hub:outbound_cursor'], 'cursor_after_clear');
      assert.equal(oldStore.getState('node_secret'), '');
      assert.equal(oldStore.getState('node_secret_version'), '');
    } finally {
      oldStore.close();
    }
  });

  it('clears node_secret_source when divergence clears local secret', async () => {
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        payload: {
          status: 'rejected',
          reason: 'node_secret_invalid',
        },
      }),
      text: async () => '',
    });

    const result = await rotateNodeSecret();

    assert.equal(result.ok, false);
    assert.equal(result.error, 'secret_diverged_cleared');
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret')), false);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version')), false);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source')), false);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')), false);
    assert.equal(getHubNodeSecret(), null);
    assert.equal(getHubNodeSecretVersion(), null);
  });

  it('keeps env node_secret suppressed across restart after divergence clear', async () => {
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '1';
    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ payload: { status: 'rejected', reason: 'node_secret_invalid' } }),
      text: async () => '',
    });

    const result = await rotateNodeSecret();

    assert.equal(result.ok, false);
    assert.equal(result.error, 'secret_diverged_cleared');
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret')), false);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')), true);
    assert.equal(
      fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed'), 'utf8'),
      suppressionMarker('a'.repeat(64))
    );

    const script = `
      const fs = require('fs');
      const path = require('path');
      const { sendHelloToHub } = require('./src/gep/a2aProtocol');
      let hadAuth = null;
      global.fetch = async (url, opts) => {
        hadAuth = Boolean(opts && opts.headers && opts.headers.Authorization);
        return {
          ok: true,
          status: 200,
          json: async () => ({ payload: {
            status: 'acknowledged',
            node_secret: '${'c'.repeat(64)}',
            node_secret_version: 5,
            your_node_id: 'node_aaaaaaaaaaaa'
          } }),
          text: async () => ''
        };
      };
      sendHelloToHub().then((hello) => {
        process.stdout.write(JSON.stringify({
          ok: hello.ok === true,
          hadAuth,
          marker: fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed'))
            ? fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed'), 'utf8')
            : ''
        }));
      }).catch((err) => {
        process.stderr.write(String(err && err.stack || err));
        process.exit(1);
      });
    `;
    const child = spawnSync(process.execPath, ['-e', script], {
      cwd: path.resolve(__dirname, '..'),
      env: {
        ...process.env,
        EVOLVER_HOME: process.env.EVOLVER_HOME,
        A2A_HUB_URL: process.env.A2A_HUB_URL,
        EVOMAP_HUB_ALLOW_INSECURE: '1',
        A2A_NODE_ID: 'node_aaaaaaaaaaaa',
        A2A_NODE_SECRET: 'a'.repeat(64),
        A2A_NODE_SECRET_VERSION: '1',
      },
      encoding: 'utf8',
      timeout: 20_000,
    });

    assert.equal(child.status, 0, child.stderr);
    const childStdoutLines = child.stdout.trim().split('\n').filter(Boolean);
    const childResult = JSON.parse(childStdoutLines[childStdoutLines.length - 1]);
    assert.equal(childResult.ok, true);
    assert.equal(childResult.hadAuth, false, 'restart hello must ignore stale env secret');
    assert.equal(childResult.marker, suppressionMarker('a'.repeat(64)), 'same stale env marker must remain fingerprinted');
  });

  it('adopts changed env node_secret after fingerprinted suppression restart', async () => {
    var captured = null;
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'c'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '5');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed'), suppressionMarker('a'.repeat(64)));
    process.env.A2A_NODE_SECRET = 'd'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '8';
    _resetHubNodeSecretStateForTesting();
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'd'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 8);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'd'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '8');
    assert.equal(captured.body.node_secret_version, 8);
    assert.equal(captured.body.meta.node_secret_version, 8);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')), false);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'utf8'), 'd'.repeat(64));
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '8');
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'env_seed');
  });

  it('preserves hub_rotate source when changed env matches persisted rotated secret', async () => {
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'b'.repeat(64));
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), '5');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'hub_rotate');
    fs.writeFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed'), suppressionMarker('a'.repeat(64)));
    process.env.A2A_NODE_SECRET = 'b'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '8';
    _resetHubNodeSecretStateForTesting();

    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 5);
    assert.equal(fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')), false);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret'), 'utf8'), 'b'.repeat(64));
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_version'), 'utf8'), '5');
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'hub_rotate');

    process.env.A2A_NODE_SECRET = 'c'.repeat(64);
    process.env.A2A_NODE_SECRET_VERSION = '9';
    _resetHubNodeSecretStateForTesting();

    assert.equal(getHubNodeSecret(), 'b'.repeat(64), 'hub-rotated store must still win over later stale env');
    assert.equal(getHubNodeSecretVersion(), 5);
    assert.equal(fs.readFileSync(path.join(process.env.EVOLVER_HOME, 'node_secret_source'), 'utf8'), 'hub_rotate');
  });

  // Regression: a rotate hello that the hub rejects at the app level
  // (status:"rejected", reason:"node_secret_invalid") must unlink the
  // on-disk node_secret so buildHubHeaders() falls back to an
  // unauthenticated hello on the next tick. Pre-fix, the divergence block
  // referenced an undeclared NODE_SECRET_FILE; the resulting ReferenceError
  // was swallowed by the catch, the file was left on disk, and the node
  // reloaded the same diverged secret every tick — a permanent 403 deadlock
  // against the hub. This test fails against that pre-fix code (file stays on
  // disk AND a "Failed to unlink" warning is logged).
  it('unlinks the diverged node_secret + version from disk on a rotate hello rejection', async () => {
    var secretFile = path.join(process.env.EVOLVER_HOME, 'node_secret');
    var versionFile = path.join(process.env.EVOLVER_HOME, 'node_secret_version');
    var sourceFile = path.join(process.env.EVOLVER_HOME, 'node_secret_source');
    fs.writeFileSync(sourceFile, 'hub_rotate');
    assert.equal(fs.existsSync(secretFile), true, 'precondition: persisted node_secret present');
    assert.equal(fs.existsSync(versionFile), true, 'precondition: persisted node_secret_version present');
    assert.equal(fs.existsSync(sourceFile), true, 'precondition: persisted node_secret_source present');

    global.fetch = async () => ({
      ok: true,
      status: 200,
      json: async () => ({ payload: { status: 'rejected', reason: 'node_secret_invalid' } }),
      text: async () => '',
    });

    var warnings = [];
    var origWarn = console.warn;
    console.warn = function () { warnings.push(Array.prototype.join.call(arguments, ' ')); };
    var result;
    try {
      result = await rotateNodeSecret();
    } finally {
      console.warn = origWarn;
    }

    // Caller is signalled to clear (not arm the reauth backoff).
    assert.equal(result.ok, false);
    assert.equal(result.error, 'secret_diverged_cleared');

    // (a) the on-disk secret (and its version sibling) are actually unlinked.
    assert.equal(fs.existsSync(secretFile), false, 'diverged node_secret must be unlinked from disk');
    assert.equal(fs.existsSync(versionFile), false, 'diverged node_secret_version must be unlinked from disk');
    assert.equal(fs.existsSync(sourceFile), false, 'diverged node_secret_source must be unlinked from disk');
    assert.equal(
      fs.existsSync(path.join(process.env.EVOLVER_HOME, 'node_secret_env_suppressed')),
      false,
      'divergence without env must not persist env suppression'
    );

    // (b) the unlink must not have thrown an undefined-variable ReferenceError
    // (the exact failure mode of the original NODE_SECRET_FILE bug).
    var unlinkFail = warnings.find(function (w) { return /Failed to unlink diverged node_secret file/.test(w); });
    assert.equal(unlinkFail, undefined, 'unlink must succeed without a swallowed ReferenceError: ' + (unlinkFail || ''));
  });

  it('ignores orphan env node_secret_version when persisted secret is active', async () => {
    var captured = null;
    process.env.A2A_NODE_SECRET_VERSION = '9';
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecretVersion(), 7);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'a'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '7');
    assert.equal(captured.body.node_secret_version, 7);
    assert.equal(captured.body.meta.node_secret_version, 7);
  });

  it('uses EVOMAP_NODE_SECRET and version as a matched pair', async () => {
    var captured = null;
    process.env.EVOMAP_NODE_SECRET = 'b'.repeat(64);
    process.env.EVOMAP_NODE_SECRET_VERSION = '9';
    global.fetch = async (url, opts) => {
      captured = { url, opts, body: JSON.parse(opts.body) };
      return {
        ok: true,
        status: 200,
        json: async () => ({ status: 'ok' }),
        text: async () => '',
      };
    };

    assert.equal(getHubNodeSecret(), 'b'.repeat(64));
    assert.equal(getHubNodeSecretVersion(), 9);
    var result = await sendHeartbeat();

    assert.equal(result.ok, true);
    assert.equal(captured.opts.headers.Authorization, 'Bearer ' + 'b'.repeat(64));
    assert.equal(captured.opts.headers['X-EvoMap-Node-Secret-Version'], '9');
    assert.equal(captured.body.node_secret_version, 9);
    assert.equal(captured.body.meta.node_secret_version, 9);
  });
});

describe('hubOpenEventStream', () => {
  var originalHubUrl;
  var originalNodeId;
  var originalNodeSecret;
  var originalNodeSecretVersion;
  var originalEvolverHome;
  var originalEventSource;
  var tmpDir;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-event-stream-'));
    originalHubUrl = process.env.A2A_HUB_URL;
    originalNodeId = process.env.A2A_NODE_ID;
    originalNodeSecret = process.env.A2A_NODE_SECRET;
    originalNodeSecretVersion = process.env.A2A_NODE_SECRET_VERSION;
    originalEvolverHome = process.env.EVOLVER_HOME;
    originalEventSource = globalThis.EventSource;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.A2A_NODE_ID = 'test-node';
    process.env.EVOLVER_HOME = path.join(tmpDir, '.evomap');
  });

  after(() => {
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalNodeId === undefined) delete process.env.A2A_NODE_ID;
    else process.env.A2A_NODE_ID = originalNodeId;
    if (originalNodeSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalNodeSecret;
    if (originalNodeSecretVersion === undefined) delete process.env.A2A_NODE_SECRET_VERSION;
    else process.env.A2A_NODE_SECRET_VERSION = originalNodeSecretVersion;
    if (originalEvolverHome === undefined) delete process.env.EVOLVER_HOME;
    else process.env.EVOLVER_HOME = originalEvolverHome;
    if (originalEventSource === undefined) delete globalThis.EventSource;
    else globalThis.EventSource = originalEventSource;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    _resetHubNodeSecretStateForTesting();
    fs.mkdirSync(process.env.EVOLVER_HOME, { recursive: true });
  });

  afterEach(() => {
    _resetHubNodeSecretStateForTesting();
  });

  it('returns ok:false with no_hub_url when A2A_HUB_URL is unset', () => {
    var saved = process.env.A2A_HUB_URL;
    delete process.env.A2A_HUB_URL;
    var result = hubOpenEventStream({});
    assert.equal(result.ok, false);
    assert.match(result.error, /no_hub_url/);
    process.env.A2A_HUB_URL = saved;
  });

  it('returns ok:false when no EventSource is available', () => {
    delete globalThis.EventSource;
    var result = hubOpenEventStream({});
    assert.equal(result.ok, false);
    assert.match(result.error, /eventsource_not_available/);
  });

  it('uses globalThis.EventSource when available', () => {
    var calledUrl = null;
    var calledOpts = null;
    globalThis.EventSource = function (url, opts) {
      calledUrl = url;
      calledOpts = opts;
      this.close = function () {};
    };

    var result = hubOpenEventStream({});
    assert.equal(result.ok, true);
    assert.ok(calledUrl.includes('/a2a/events/stream?'), 'URL should contain stream path');
    assert.ok(calledUrl.includes('node_id='), 'URL should contain node_id param');
    delete globalThis.EventSource;
  });

  it('passes Authorization and node secret version headers when set', () => {
    var calledOpts = null;
    globalThis.EventSource = function (url, opts) {
      calledOpts = opts;
      this.close = function () {};
    };
    process.env.A2A_NODE_SECRET = 'secret123';
    process.env.A2A_NODE_SECRET_VERSION = '4';

    var result = hubOpenEventStream({});
    assert.equal(result.ok, true);
    assert.equal(calledOpts.headers['Authorization'], 'Bearer secret123');
    assert.equal(calledOpts.headers['X-EvoMap-Node-Secret-Version'], '4');
    assert.equal(calledOpts.method, undefined);

    delete process.env.A2A_NODE_SECRET;
    delete process.env.A2A_NODE_SECRET_VERSION;
    delete globalThis.EventSource;
  });

  it('close() calls eventSource.close()', () => {
    var closed = false;
    globalThis.EventSource = function () {
      this.close = function () { closed = true; };
    };

    var result = hubOpenEventStream({});
    assert.equal(result.ok, true);
    result.close();
    assert.ok(closed, 'eventSource.close() should have been called');
    delete globalThis.EventSource;
  });

  it('returns ok:false when EventSource constructor throws', () => {
    globalThis.EventSource = function () {
      throw new Error('connection refused');
    };

    var result = hubOpenEventStream({});
    assert.equal(result.ok, false);
    assert.match(result.error, /eventsource_init_failed/);
    assert.match(result.error, /connection refused/);
    delete globalThis.EventSource;
  });
});

describe('mergeAndCap', () => {
  it('concatenates without dropping when total is under cap', () => {
    var result = mergeAndCap([1, 2, 3], [4, 5], 10);
    assert.deepEqual(result, [1, 2, 3, 4, 5]);
  });

  it('keeps exactly cap entries when total exceeds cap', () => {
    var prev = Array.from({ length: 80 }, function (_, i) { return { id: i }; });
    var incoming = Array.from({ length: 30 }, function (_, i) { return { id: 80 + i }; });
    var result = mergeAndCap(prev, incoming, 100);
    assert.equal(result.length, 100);
  });

  it('keeps the LAST (newest) entries, not the first', () => {
    var prev = Array.from({ length: 80 }, function (_, i) { return { id: i }; });
    var incoming = Array.from({ length: 30 }, function (_, i) { return { id: 80 + i }; });
    var result = mergeAndCap(prev, incoming, 100);
    // First 10 (oldest: id 0-9) should be dropped; last 100 start at id 10
    assert.equal(result[0].id, 10);
    assert.equal(result[99].id, 109);
  });

  it('simulates 5 successive merges of 30 entries and stays bounded at 100', () => {
    var acc = [];
    for (var round = 0; round < 5; round++) {
      var batch = Array.from({ length: 30 }, function (_, i) { return { id: round * 30 + i }; });
      acc = mergeAndCap(acc, batch, 100);
    }
    assert.equal(acc.length, 100);
    // After 150 total entries, oldest 50 should be gone (id 0-49 dropped)
    assert.equal(acc[0].id, 50);
    assert.equal(acc[99].id, 149);
  });
});

describe('httpTransportReceive asset_id filter', () => {
  var originalFetch;
  var originalHubUrl;
  var originalInsecure;

  before(() => {
    originalFetch = global.fetch;
    originalHubUrl = process.env.A2A_HUB_URL;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
  });

  after(() => {
    global.fetch = originalFetch;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalInsecure === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = originalInsecure;
  });

  it('discards assets with no asset_id (tamper bypass prevention)', async () => {
    global.fetch = async function () {
      return { ok: true, json: async function () { return { payload: { results: [{ type: 'Gene', id: 'g1' }] } }; } };
    };
    var result = await httpTransportReceive({});
    assert.equal(result.length, 0);
  });

  it('passes through assets whose asset_id matches content hash', async () => {
    var asset = { type: 'Gene', id: 'g2', strategy: ['x'] };
    asset.asset_id = computeAssetId(asset);
    global.fetch = async function () {
      return { ok: true, json: async function () { return { payload: { results: [asset] } }; } };
    };
    var result = await httpTransportReceive({});
    assert.equal(result.length, 1);
    assert.equal(result[0].id, 'g2');
  });

  it('discards assets whose asset_id does not match content hash', async () => {
    var asset = { type: 'Gene', id: 'g3', asset_id: 'sha256:deadbeef' };
    global.fetch = async function () {
      return { ok: true, json: async function () { return { payload: { results: [asset] } }; } };
    };
    var result = await httpTransportReceive({});
    assert.equal(result.length, 0);
  });

  it('keeps valid assets and discards tampered or missing-asset_id ones in a mixed batch', async () => {
    var good = { type: 'Gene', id: 'g4', strategy: ['y'] };
    good.asset_id = computeAssetId(good);
    var bad = { type: 'Capsule', id: 'c1', asset_id: 'sha256:bad' };
    var noId = { type: 'Gene', id: 'g5' };
    global.fetch = async function () {
      return { ok: true, json: async function () { return { payload: { results: [good, bad, noId] } }; } };
    };
    var result = await httpTransportReceive({});
    // noId is discarded (missing asset_id treated as untrusted, same as tampered)
    assert.equal(result.length, 1);
    assert.equal(result[0].id, 'g4');
  });
});

describe('httpTransportSend HUB_DRY_RUN', () => {
  var originalDryRun;
  var originalHubUrl;

  before(() => {
    originalDryRun = process.env.HUB_DRY_RUN;
    originalHubUrl = process.env.A2A_HUB_URL;
    _resetDryRunWarnedForTesting();
  });

  after(() => {
    if (originalDryRun === undefined) delete process.env.HUB_DRY_RUN;
    else process.env.HUB_DRY_RUN = originalDryRun;
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    _resetDryRunWarnedForTesting();
  });

  it('returns ok:true with dry_run:true when HUB_DRY_RUN=1', async () => {
    process.env.HUB_DRY_RUN = '1';
    var msg = buildMessage({ messageType: 'hello', payload: {} });
    var result = await httpTransportSend(msg, {});
    assert.equal(result.ok, true);
    assert.equal(result.dry_run, true);
  });

  it('accepts yes/on/true as truthy HUB_DRY_RUN values', async () => {
    var msg = buildMessage({ messageType: 'hello', payload: {} });
    // 'Yes' and 'On' exercise the .toLowerCase() path; 'true' and '1' are canonical forms.
    for (var val of ['yes', 'on', 'true', 'Yes']) {
      process.env.HUB_DRY_RUN = val;
      _resetDryRunWarnedForTesting();
      var result = await httpTransportSend(msg, {});
      assert.equal(result.dry_run, true, 'expected dry_run for HUB_DRY_RUN=' + val);
      delete process.env.HUB_DRY_RUN;
    }
  });

  it('warning fires exactly once per process lifecycle', async () => {
    process.env.HUB_DRY_RUN = '1';
    _resetDryRunWarnedForTesting();
    var warnCount = 0;
    var origWarn = console.warn;
    console.warn = function () {
      if (String(arguments[0]).includes('HUB_DRY_RUN')) warnCount++;
      origWarn.apply(console, arguments);
    };
    try {
      var msg = buildMessage({ messageType: 'hello', payload: {} });
      await httpTransportSend(msg, {});
      await httpTransportSend(msg, {});
      assert.equal(warnCount, 1, 'warning should fire exactly once');
    } finally {
      console.warn = origWarn;
    }
  });

  it('returns {ok:false} when A2A_HUB_URL unset and HUB_DRY_RUN off', async () => {
    delete process.env.HUB_DRY_RUN;
    var savedUrl = process.env.A2A_HUB_URL;
    delete process.env.A2A_HUB_URL;
    try {
      var msg = buildMessage({ messageType: 'hello', payload: {} });
      var result = await httpTransportSend(msg, {});
      assert.equal(result.ok, false);
      assert.equal(result.error, 'A2A_HUB_URL not set');
    } finally {
      if (savedUrl === undefined) delete process.env.A2A_HUB_URL;
      else process.env.A2A_HUB_URL = savedUrl;
    }
  });

  it('_resetDryRunWarnedForTesting allows warning to fire again', async () => {
    process.env.HUB_DRY_RUN = '1';
    _resetDryRunWarnedForTesting();
    var warnCount = 0;
    var origWarn = console.warn;
    console.warn = function () {
      if (String(arguments[0]).includes('HUB_DRY_RUN')) warnCount++;
      origWarn.apply(console, arguments);
    };
    try {
      var msg = buildMessage({ messageType: 'hello', payload: {} });
      await httpTransportSend(msg, {});
      _resetDryRunWarnedForTesting();
      await httpTransportSend(msg, {});
      assert.equal(warnCount, 2, 'warning should fire again after reset');
    } finally {
      console.warn = origWarn;
      _resetDryRunWarnedForTesting();
    }
  });
});
