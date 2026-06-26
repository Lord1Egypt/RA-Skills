const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

describe('hubVerify', function () {
  const { isSolidifyVerifyEnabled, requestSolidifyPermit } = require('../src/gep/hubVerify');

  it('isSolidifyVerifyEnabled returns false when no hub URL', function () {
    const original = process.env.A2A_HUB_URL;
    delete process.env.A2A_HUB_URL;
    assert.strictEqual(isSolidifyVerifyEnabled(), false);
    if (original !== undefined) process.env.A2A_HUB_URL = original;
  });

  it('isSolidifyVerifyEnabled returns false when explicitly disabled', function () {
    const origUrl = process.env.A2A_HUB_URL;
    const origVerify = process.env.EVOLVER_SOLIDIFY_VERIFY;
    const origNodeEnv = process.env.NODE_ENV;
    process.env.A2A_HUB_URL = 'https://example.com';
    process.env.EVOLVER_SOLIDIFY_VERIFY = 'false';
    process.env.NODE_ENV = 'test';
    assert.strictEqual(isSolidifyVerifyEnabled(), false);
    if (origUrl !== undefined) process.env.A2A_HUB_URL = origUrl; else delete process.env.A2A_HUB_URL;
    if (origVerify !== undefined) process.env.EVOLVER_SOLIDIFY_VERIFY = origVerify; else delete process.env.EVOLVER_SOLIDIFY_VERIFY;
    if (origNodeEnv !== undefined) process.env.NODE_ENV = origNodeEnv; else delete process.env.NODE_ENV;
  });

  it('isSolidifyVerifyEnabled returns true when hub URL is set', function () {
    const origUrl = process.env.A2A_HUB_URL;
    const origVerify = process.env.EVOLVER_SOLIDIFY_VERIFY;
    process.env.A2A_HUB_URL = 'https://evomap.ai';
    delete process.env.EVOLVER_SOLIDIFY_VERIFY;
    assert.strictEqual(isSolidifyVerifyEnabled(), true);
    if (origUrl !== undefined) process.env.A2A_HUB_URL = origUrl; else delete process.env.A2A_HUB_URL;
    if (origVerify !== undefined) process.env.EVOLVER_SOLIDIFY_VERIFY = origVerify; else delete process.env.EVOLVER_SOLIDIFY_VERIFY;
  });

  it('requestSolidifyPermit returns offline error when no hub URL', async function () {
    const origUrl = process.env.A2A_HUB_URL;
    delete process.env.A2A_HUB_URL;
    try {
      const result = await requestSolidifyPermit({ geneId: 'test_gene', signals: ['a'], mutation: {} });
      assert.strictEqual(result.ok, false);
      assert.strictEqual(result.offline, true);
    } finally {
      if (origUrl !== undefined) process.env.A2A_HUB_URL = origUrl;
    }
  });

  it('consumeOfflinePermit returns error with offline flag when no token cached', function () {
    // Hermetic: a host that runs the evolver daemon exports A2A_* hub creds,
    // which would flip this case "online" and fail the assertion. Clear them so
    // the test exercises the genuine no-hub/offline path regardless of ambient
    // env (the inherited-env trap).
    const saved = {};
    for (const k of ['A2A_HUB_URL', 'A2A_NODE_ID', 'A2A_NODE_SECRET']) { saved[k] = process.env[k]; delete process.env[k]; }
    try {
      const { consumeOfflinePermit } = require('../src/gep/hubVerify');
      const result = consumeOfflinePermit();
      assert.strictEqual(result.ok, false);
      assert.strictEqual(result.offline, true);
    } finally {
      for (const k of Object.keys(saved)) { if (saved[k] !== undefined) process.env[k] = saved[k]; }
    }
  });

  it('isSolidifyVerifyEnabled ignores env var disable in non-test env', function () {
    const origUrl = process.env.A2A_HUB_URL;
    const origVerify = process.env.EVOLVER_SOLIDIFY_VERIFY;
    const origNodeEnv = process.env.NODE_ENV;
    process.env.A2A_HUB_URL = 'https://example.com';
    process.env.EVOLVER_SOLIDIFY_VERIFY = 'false';
    process.env.NODE_ENV = 'production';
    assert.strictEqual(isSolidifyVerifyEnabled(), true);
    if (origUrl !== undefined) process.env.A2A_HUB_URL = origUrl; else delete process.env.A2A_HUB_URL;
    if (origVerify !== undefined) process.env.EVOLVER_SOLIDIFY_VERIFY = origVerify; else delete process.env.EVOLVER_SOLIDIFY_VERIFY;
    if (origNodeEnv !== undefined) process.env.NODE_ENV = origNodeEnv; else delete process.env.NODE_ENV;
  });
});

describe('hubVerify offline token integrity (C2)', function () {
  // Reset cached module so MEMORY_DIR takes effect on each test
  function freshHubVerify(memDir) {
    process.env.MEMORY_DIR = memDir;
    delete require.cache[require.resolve('../src/gep/hubVerify')];
    return require('../src/gep/hubVerify');
  }

  function makeTokenFile(otPath, token, signingSecret) {
    const data = JSON.stringify(token);
    const hmac = crypto.createHmac('sha256', signingSecret).update(data).digest('hex');
    fs.writeFileSync(otPath, JSON.stringify({ data: token, hmac }), 'utf8');
  }

  function withEnv(overrides, fn) {
    const orig = {};
    for (const k of Object.keys(overrides)) {
      orig[k] = process.env[k];
      if (overrides[k] === undefined) delete process.env[k];
      else process.env[k] = overrides[k];
    }
    try { return fn(); }
    finally {
      for (const k of Object.keys(orig)) {
        if (orig[k] === undefined) delete process.env[k];
        else process.env[k] = orig[k];
      }
      delete require.cache[require.resolve('../src/gep/hubVerify')];
    }
  }

  it('consumeOfflinePermit accepts a token signed with the current nodeSecret', function () {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: 'a'.repeat(64), MEMORY_DIR: tmpDir }, () => {
        const token = { usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 10 };
        makeTokenFile(path.join(tmpDir, '.ot'), token, 'a'.repeat(64));
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, true, 'token with matching HMAC should be accepted');
        assert.strictEqual(res.offline, true);
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('rejects token when nodeSecret rotates (clone detection)', function () {
    // A cloned install reuses the .ot file but rotates nodeSecret on first
    // online verify. HMAC verification fails and the token is rejected.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: 'b'.repeat(64), MEMORY_DIR: tmpDir }, () => {
        const token = { usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 10 };
        // Sign with secret A but the running install has secret B.
        makeTokenFile(path.join(tmpDir, '.ot'), token, 'a'.repeat(64));
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, false);
        assert.strictEqual(res.error, 'no_offline_token');
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('rejects tampered token data even when HMAC field is present', function () {
    // Attacker forges usedCount=0 to bypass quota, but the HMAC is over the
    // original usedCount=5 payload. Verification fails.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: 'c'.repeat(64), MEMORY_DIR: tmpDir }, () => {
        const realToken = { usedCount: 5, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 10 };
        const realHmac = crypto.createHmac('sha256', 'c'.repeat(64)).update(JSON.stringify(realToken)).digest('hex');
        const forgedToken = { usedCount: 0, expiresAt: realToken.expiresAt, maxOfflineSolidifies: 10 };
        fs.writeFileSync(path.join(tmpDir, '.ot'), JSON.stringify({ data: forgedToken, hmac: realHmac }), 'utf8');
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, false);
        assert.strictEqual(res.error, 'no_offline_token');
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('rejects legacy binary .ot file (pre-HMAC format) on upgrade', function () {
    // Pre-HMAC versions wrote an AES-CBC ciphertext blob to .ot. After upgrade,
    // loadOfflineToken's JSON.parse throws → catch returns null → consume
    // returns no_offline_token. Next online verify rewrites in JSON+HMAC form.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: 'd'.repeat(64), MEMORY_DIR: tmpDir }, () => {
        // Raw bytes — not valid JSON.
        fs.writeFileSync(path.join(tmpDir, '.ot'), Buffer.from([0x00, 0xff, 0xab, 0xcd, 0xef, 0x12, 0x34]));
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, false);
        assert.strictEqual(res.error, 'no_offline_token');
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('rejects token when nodeSecret is unavailable (misconfig path)', function () {
    // No A2A_NODE_SECRET env var and a2aProtocol can't supply one
    // (require fails in this env). loadOfflineToken returns null rather
    // than accepting an unverifiable token.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: undefined, MEMORY_DIR: tmpDir }, () => {
        // Token file present, signed by some secret — but the running install
        // has no way to fetch a secret to verify against.
        const token = { usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 10 };
        makeTokenFile(path.join(tmpDir, '.ot'), token, 'e'.repeat(64));
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, false);
        assert.strictEqual(res.error, 'no_offline_token');
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });

  it('rejects token when HMAC field has wrong length (length-mismatch guard)', function () {
    // The length pre-check in loadOfflineToken guards crypto.timingSafeEqual,
    // which throws on mismatched lengths. Truncated/padded HMACs must be
    // rejected before reaching timingSafeEqual.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ot-hmac-'));
    try {
      withEnv({ A2A_NODE_SECRET: 'f'.repeat(64), MEMORY_DIR: tmpDir }, () => {
        const token = { usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 10 };
        // Truncated HMAC: 30 hex chars → 15 bytes vs expected 32 bytes.
        const truncatedHmac = 'a'.repeat(30);
        fs.writeFileSync(path.join(tmpDir, '.ot'), JSON.stringify({ data: token, hmac: truncatedHmac }), 'utf8');
        const hv = freshHubVerify(tmpDir);
        const res = hv.consumeOfflinePermit();
        assert.strictEqual(res.ok, false);
        assert.strictEqual(res.error, 'no_offline_token');
      });
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  });
});

describe('hubVerify: recordLastOnlineVerify trigger window', function () {
  // Pre-fix: lastOnlineVerify only advanced on {ok:true} envelopes. A streak
  // of envelope-error responses (quota_exceeded, rate_limited, ...) or any
  // 4xx (bad creds, forbidden) left the offline-duration counter stuck at
  // the moment of the last good envelope, so after MAX_OFFLINE_DURATION_MS
  // (7 days) consumeOfflinePermit would refuse to issue offline permits with
  // offline_duration_exceeded even though the daemon was talking to the hub
  // the whole time.

  function freshHubVerify(memDir) {
    process.env.MEMORY_DIR = memDir;
    delete require.cache[require.resolve('../src/gep/hubVerify')];
    // Do NOT clear hubFetch / a2aProtocol caches here — the caller installed
    // stubs there and re-requiring hubVerify must pick those stubs up.
    return require('../src/gep/hubVerify');
  }

  function stubA2aProtocol(nodeId, nodeSecret) {
    const a2aPath = require.resolve('../src/gep/a2aProtocol');
    require.cache[a2aPath] = {
      id: a2aPath, filename: a2aPath, loaded: true,
      exports: {
        getHubNodeSecret: () => nodeSecret,
        getNodeId: () => nodeId,
      },
    };
  }

  function stubHubFetch(fakeRes) {
    const hubFetchPath = require.resolve('../src/gep/hubFetch');
    require.cache[hubFetchPath] = {
      id: hubFetchPath, filename: hubFetchPath, loaded: true,
      exports: { hubFetch: async () => fakeRes },
    };
  }

  function makeRes(status, bodyObj) {
    return {
      ok: status >= 200 && status < 300,
      status,
      json: async () => bodyObj,
      text: async () => JSON.stringify(bodyObj),
    };
  }

  async function withFullEnv(memDir, fn) {
    const origUrl = process.env.A2A_HUB_URL;
    const origSecret = process.env.A2A_NODE_SECRET;
    const origMem = process.env.MEMORY_DIR;
    process.env.A2A_HUB_URL = 'http://localhost:19999';
    process.env.A2A_NODE_SECRET = 'a'.repeat(64);
    process.env.MEMORY_DIR = memDir;
    try { return await fn(); }
    finally {
      if (origUrl === undefined) delete process.env.A2A_HUB_URL; else process.env.A2A_HUB_URL = origUrl;
      if (origSecret === undefined) delete process.env.A2A_NODE_SECRET; else process.env.A2A_NODE_SECRET = origSecret;
      if (origMem === undefined) delete process.env.MEMORY_DIR; else process.env.MEMORY_DIR = origMem;
      delete require.cache[require.resolve('../src/gep/hubVerify')];
      delete require.cache[require.resolve('../src/gep/hubFetch')];
      delete require.cache[require.resolve('../src/gep/a2aProtocol')];
    }
  }

  it('records lastOnlineVerify on 2xx with envelope {ok:true}', async function () {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hv-online-'));
    try {
      await withFullEnv(tmpDir, async () => {
        stubA2aProtocol('node_aaa', 'a'.repeat(64));
        stubHubFetch(makeRes(200, { ok: true }));
        const hv = freshHubVerify(tmpDir);
        await hv.requestSolidifyPermit({ geneId: 'g1', signals: [], mutation: {} });
        const lvPath = path.join(tmpDir, '.lv');
        assert.ok(fs.existsSync(lvPath), '.lv file must be written on a healthy {ok:true} reply');
      });
    } finally { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} }
  });

  it('records lastOnlineVerify on 2xx envelope-error responses (e.g. quota_exceeded)', async function () {
    // The fix: connection is healthy, hub answered, but the envelope reports
    // an application-level error. lastOnlineVerify must still advance so a
    // streak of these does not falsely trip offline_duration_exceeded.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hv-online-'));
    try {
      await withFullEnv(tmpDir, async () => {
        stubA2aProtocol('node_bbb', 'a'.repeat(64));
        stubHubFetch(makeRes(200, { ok: false, error: 'quota_exceeded' }));
        const hv = freshHubVerify(tmpDir);
        const result = await hv.requestSolidifyPermit({ geneId: 'g2', signals: [], mutation: {} });
        assert.equal(result.ok, false, 'envelope-level error must still surface to the caller');
        assert.equal(result.error, 'quota_exceeded');
        const lvPath = path.join(tmpDir, '.lv');
        assert.ok(fs.existsSync(lvPath), '.lv file must be written even when envelope ok=false');
        const ts = parseInt(fs.readFileSync(lvPath, 'utf8'), 10);
        assert.ok(Math.abs(Date.now() - ts) < 5000, 'recorded ts must be recent');
      });
    } finally { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} }
  });

  it('records lastOnlineVerify on 4xx responses (hub explicitly rejected — still reachable)', async function () {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hv-online-'));
    try {
      await withFullEnv(tmpDir, async () => {
        stubA2aProtocol('node_ccc', 'a'.repeat(64));
        stubHubFetch(makeRes(401, { error: 'unauthorized' }));
        const hv = freshHubVerify(tmpDir);
        const result = await hv.requestSolidifyPermit({ geneId: 'g3', signals: [], mutation: {} });
        assert.equal(result.ok, false);
        assert.equal(result.offline, false, '4xx is not offline — hub answered');
        const lvPath = path.join(tmpDir, '.lv');
        assert.ok(fs.existsSync(lvPath), '.lv file must be written even on 4xx');
      });
    } finally { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} }
  });

  it('does NOT record lastOnlineVerify on 5xx (treated as infra down / offline)', async function () {
    // 5xx is ambiguous (CDN/LB up but hub down), conservatively keep the
    // pre-fix behaviour of NOT advancing lastOnlineVerify so the offline
    // counter still trips after MAX_OFFLINE_DURATION_MS if hub stays broken.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hv-online-'));
    try {
      await withFullEnv(tmpDir, async () => {
        stubA2aProtocol('node_ddd', 'a'.repeat(64));
        stubHubFetch(makeRes(503, { error: 'service_unavailable' }));
        const hv = freshHubVerify(tmpDir);
        const result = await hv.requestSolidifyPermit({ geneId: 'g4', signals: [], mutation: {} });
        assert.equal(result.ok, false);
        assert.equal(result.offline, true, '5xx must keep treating the call as offline');
        const lvPath = path.join(tmpDir, '.lv');
        assert.ok(!fs.existsSync(lvPath), '.lv file must NOT be written on 5xx');
      });
    } finally { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} }
  });

  it('does NOT cache offline_token on envelope-error responses', async function () {
    // Guard against an over-eager rewrite: even though we now record online
    // on envelope errors, we MUST NOT pick up an offline_token field from a
    // {ok:false} envelope — that token could be stale or invalid.
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hv-online-'));
    try {
      await withFullEnv(tmpDir, async () => {
        stubA2aProtocol('node_eee', 'a'.repeat(64));
        stubHubFetch(makeRes(200, {
          ok: false,
          error: 'rate_limited',
          offline_token: { usedCount: 0, expiresAt: Date.now() + 86400000, maxOfflineSolidifies: 99 },
        }));
        const hv = freshHubVerify(tmpDir);
        await hv.requestSolidifyPermit({ geneId: 'g5', signals: [], mutation: {} });
        const otPath = path.join(tmpDir, '.ot');
        assert.ok(!fs.existsSync(otPath), 'offline_token from a {ok:false} envelope must be ignored');
      });
    } finally { try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {} }
  });
});
