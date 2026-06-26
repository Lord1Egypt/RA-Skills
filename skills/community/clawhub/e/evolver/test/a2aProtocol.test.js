const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
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
  sendHeartbeat,
  hubOpenEventStream,
  mergeAndCap,
  httpTransportSend,
  httpTransportReceive,
} = require('../src/gep/a2aProtocol');
const { _resetDryRunWarnedForTesting } = require('../src/gep/a2aProtocol')._testing;
const { computeAssetId } = require('../src/gep/contentHash');

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

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-hb-test-'));
    originalHubUrl = process.env.A2A_HUB_URL;
    originalLogsDir = process.env.EVOLVER_LOGS_DIR;
    originalInsecure = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.EVOLVER_LOGS_DIR = tmpDir;
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
    fs.rmSync(tmpDir, { recursive: true, force: true });
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
});

describe('hubOpenEventStream', () => {
  var originalHubUrl;
  var originalNodeId;
  var originalNodeSecret;
  var originalEventSource;

  before(() => {
    originalHubUrl = process.env.A2A_HUB_URL;
    originalNodeId = process.env.A2A_NODE_ID;
    originalNodeSecret = process.env.A2A_NODE_SECRET;
    originalEventSource = globalThis.EventSource;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.A2A_NODE_ID = 'test-node';
  });

  after(() => {
    if (originalHubUrl === undefined) delete process.env.A2A_HUB_URL;
    else process.env.A2A_HUB_URL = originalHubUrl;
    if (originalNodeId === undefined) delete process.env.A2A_NODE_ID;
    else process.env.A2A_NODE_ID = originalNodeId;
    if (originalNodeSecret === undefined) delete process.env.A2A_NODE_SECRET;
    else process.env.A2A_NODE_SECRET = originalNodeSecret;
    if (originalEventSource === undefined) delete globalThis.EventSource;
    else globalThis.EventSource = originalEventSource;
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

  it('passes Authorization header when A2A_NODE_SECRET is set', () => {
    var calledOpts = null;
    globalThis.EventSource = function (url, opts) {
      calledOpts = opts;
      this.close = function () {};
    };
    process.env.A2A_NODE_SECRET = 'secret123';

    var result = hubOpenEventStream({});
    assert.equal(result.ok, true);
    assert.equal(calledOpts.headers['Authorization'], 'Bearer secret123');

    delete process.env.A2A_NODE_SECRET;
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
