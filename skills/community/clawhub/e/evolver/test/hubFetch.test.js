// Tests for src/gep/hubFetch.js
//
// hubFetch is the single chokepoint for every Hub-facing HTTP call.
// It enforces two guarantees, both bypassable only via
// EVOMAP_HUB_ALLOW_INSECURE=1:
//
//   1. URL schema: must parse and use https://.
//   2. TLS: dispatcher carries an explicit rejectUnauthorized:true that
//      overrides NODE_TLS_REJECT_UNAUTHORIZED=0.
//
// The unit tests below verify the wiring (URL rejection paths + dispatcher
// injection).  The integration suite at the bottom spins up a real HTTPS
// server with a self-signed cert and verifies hubFetch actually refuses
// it even with NODE_TLS_REJECT_UNAUTHORIZED=0 — the only test that proves
// the documented attack is blocked end-to-end.

const { describe, it, before, after, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const { Agent } = require('undici');

function freshHubFetch() {
  delete require.cache[require.resolve('../src/gep/hubFetch')];
  return require('../src/gep/hubFetch');
}

describe('hubFetch — unit', () => {
  let savedEnv;
  let capturedUrl;
  let capturedOptions;
  let hubFetchMod;

  beforeEach(() => {
    savedEnv = {
      EVOMAP_HUB_ALLOW_INSECURE: process.env.EVOMAP_HUB_ALLOW_INSECURE,
      EVOMAP_HUB_IP_FAMILY: process.env.EVOMAP_HUB_IP_FAMILY,
    };
    delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    delete process.env.EVOMAP_HUB_IP_FAMILY;

    capturedUrl = null;
    capturedOptions = null;
    hubFetchMod = freshHubFetch();
    hubFetchMod._setFetchImplForTest((url, opts) => {
      capturedUrl = url;
      capturedOptions = opts;
      return Promise.resolve({ ok: true });
    });
  });

  afterEach(() => {
    if (hubFetchMod) hubFetchMod._setFetchImplForTest(null);
    if (savedEnv.EVOMAP_HUB_ALLOW_INSECURE === undefined) {
      delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    } else {
      process.env.EVOMAP_HUB_ALLOW_INSECURE = savedEnv.EVOMAP_HUB_ALLOW_INSECURE;
    }
    if (savedEnv.EVOMAP_HUB_IP_FAMILY === undefined) {
      delete process.env.EVOMAP_HUB_IP_FAMILY;
    } else {
      process.env.EVOMAP_HUB_IP_FAMILY = savedEnv.EVOMAP_HUB_IP_FAMILY;
    }
  });

  // --- happy path ---

  it('passes the url through unchanged', async () => {
    const { hubFetch } = hubFetchMod;
    await hubFetch('https://hub.example.com/a2a/publish', { method: 'POST' });
    assert.equal(capturedUrl, 'https://hub.example.com/a2a/publish');
  });

  it('injects an undici Agent dispatcher when insecure mode is off', async () => {
    const { hubFetch } = hubFetchMod;
    await hubFetch('https://hub.example.com/a2a/heartbeat', { method: 'POST' });
    assert.ok(capturedOptions.dispatcher instanceof Agent,
      'dispatcher must be an undici Agent (overrides NODE_TLS_REJECT_UNAUTHORIZED=0)');
  });

  it('defaults Hub connections to IPv4-first fallback to avoid IPv6 VPN leaks', () => {
    const cfg = hubFetchMod._getHubFetchConfigForTest();
    assert.equal(cfg.hubIpFamily, 'ipv4first');
    assert.equal(cfg.connectOpts.family, 4);
    assert.equal(cfg.connectOpts.autoSelectFamily, false);
    assert.equal(cfg.primaryConnectOpts.family, 4);
    assert.equal(cfg.primaryConnectOpts.timeout, cfg.ipv4FirstPrimaryConnectTimeoutMs);
    assert.ok(
      cfg.primaryConnectOpts.timeout < cfg.connectTimeoutMs,
      'ipv4first primary probe must leave connect budget for fallback before heartbeat aborts',
    );
    assert.equal(cfg.fallbackConnectOpts.timeout, cfg.connectTimeoutMs);
    assert.equal(cfg.fallbackConnectOpts.autoSelectFamily, true);
    assert.equal(cfg.fallbackConnectOpts.autoSelectFamilyAttemptTimeout, 250);
  });

  it('EVOMAP_HUB_IP_FAMILY=ipv4-only disables dual-stack fallback', () => {
    hubFetchMod._setFetchImplForTest(null);
    process.env.EVOMAP_HUB_IP_FAMILY = 'ipv4-only';
    hubFetchMod = freshHubFetch();

    const cfg = hubFetchMod._getHubFetchConfigForTest();
    assert.equal(cfg.hubIpFamily, 'ipv4only');
    assert.equal(cfg.connectOpts.family, 4);
    assert.equal(cfg.connectOpts.autoSelectFamily, false);
    assert.equal(cfg.primaryConnectOpts.timeout, cfg.connectTimeoutMs);
    assert.equal(cfg.fallbackConnectOpts, null);
  });

  it('EVOMAP_HUB_IP_FAMILY=auto restores dual-stack Happy Eyeballs', () => {
    hubFetchMod._setFetchImplForTest(null);
    process.env.EVOMAP_HUB_IP_FAMILY = 'auto';
    hubFetchMod = freshHubFetch();

    const cfg = hubFetchMod._getHubFetchConfigForTest();
    assert.equal(cfg.hubIpFamily, 'auto');
    assert.equal(cfg.connectOpts.timeout, cfg.connectTimeoutMs);
    assert.equal(cfg.connectOpts.autoSelectFamily, true);
    assert.equal(cfg.connectOpts.autoSelectFamilyAttemptTimeout, 250);
    assert.equal('family' in cfg.connectOpts, false);
    assert.equal(cfg.fallbackConnectOpts, null);
  });

  it('rejects unknown EVOMAP_HUB_IP_FAMILY values at module load', () => {
    hubFetchMod._setFetchImplForTest(null);
    process.env.EVOMAP_HUB_IP_FAMILY = 'ipv6';
    assert.throws(
      () => freshHubFetch(),
      /EVOMAP_HUB_IP_FAMILY must be "ipv4", "ipv4-only", or "auto"/,
    );
  });

  it('preserves existing options fields alongside dispatcher', async () => {
    const { hubFetch } = hubFetchMod;
    const signal = AbortSignal.timeout(1000);
    await hubFetch('https://hub.example.com/a2a/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
      signal,
    });
    assert.equal(capturedOptions.method, 'POST');
    assert.deepEqual(capturedOptions.headers, { 'Content-Type': 'application/json' });
    assert.equal(capturedOptions.body, '{}');
    assert.equal(capturedOptions.signal, signal);
    assert.ok(capturedOptions.dispatcher instanceof Agent);
  });

  it('does not mutate the original options object', async () => {
    const { hubFetch } = hubFetchMod;
    const original = { method: 'GET' };
    await hubFetch('https://hub.example.com/a2a/fetch', original);
    assert.ok(!('dispatcher' in original), 'original options must not be mutated');
  });

  // --- URL schema enforcement (the chokepoint that catches what resolveHubUrl misses) ---

  it('throws on http:// URL — even when caller bypassed resolveHubUrl', async () => {
    const { hubFetch } = hubFetchMod;
    await assert.rejects(
      () => hubFetch('http://attacker.example.com/a2a/heartbeat', { method: 'POST' }),
      (err) => {
        assert.ok(err.message.includes('https://'), 'error should mention https://');
        assert.ok(err.message.includes('EVOMAP_HUB_ALLOW_INSECURE'), 'error should name escape hatch');
        return true;
      }
    );
    assert.equal(capturedUrl, null, 'fetch must not be called when URL is rejected');
  });

  it('throws on ws:// URL', async () => {
    const { hubFetch } = hubFetchMod;
    await assert.rejects(() => hubFetch('ws://attacker.example.com/a2a/heartbeat', {}), /https:\/\//);
  });

  it('throws on unparseable URL', async () => {
    const { hubFetch } = hubFetchMod;
    await assert.rejects(() => hubFetch('not-a-url', {}), /not a valid URL/);
  });

  // --- escape hatch ---

  it('EVOMAP_HUB_ALLOW_INSECURE=1 disables URL check (lets http:// pass)', async () => {
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    const { hubFetch } = hubFetchMod;
    await hubFetch('http://localhost:4000/a2a/heartbeat', { method: 'POST' });
    assert.equal(capturedUrl, 'http://localhost:4000/a2a/heartbeat');
  });

  it('EVOMAP_HUB_ALLOW_INSECURE=1 disables dispatcher injection', async () => {
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    const { hubFetch } = hubFetchMod;
    await hubFetch('http://localhost:4000/a2a/heartbeat', {});
    assert.ok(!capturedOptions || !capturedOptions.dispatcher,
      'no dispatcher should be injected in insecure mode');
  });

  it('EVOMAP_HUB_ALLOW_INSECURE values other than "1" do not bypass', async () => {
    process.env.EVOMAP_HUB_ALLOW_INSECURE = 'true';
    const { hubFetch } = hubFetchMod;
    await assert.rejects(() => hubFetch('http://hub.example.com', {}), /https:\/\//);
  });

  it('classifies non-JSON Hub 403 responses as hub unreachable, not auth', async () => {
    const { throwIfHubUnreachableResponse } = hubFetchMod;
    let textCalls = 0;
    const res = {
      status: 403,
      ok: false,
      headers: new Headers({ 'content-type': 'text/html; charset=utf-8' }),
      text: async () => {
        textCalls++;
        return '<!DOCTYPE html><title>Cloudflare</title><body>Forbidden</body>';
      },
    };

    await assert.rejects(
      () => throwIfHubUnreachableResponse(res, 'heartbeat'),
      (err) => {
        assert.equal(err.name, 'HubUnreachableError');
        assert.equal(err.code, 'HUB_UNREACHABLE');
        assert.equal(err.statusCode, 403);
        assert.match(err.bodySnippet, /Cloudflare/);
        return true;
      },
    );
    assert.equal(textCalls, 1);
  });

  it('classifies successful HTML Hub responses as hub unreachable', async () => {
    const { throwIfHubUnreachableResponse } = hubFetchMod;
    let textCalls = 0;
    const res = {
      status: 200,
      ok: true,
      headers: new Headers({ 'content-type': 'text/html; charset=utf-8' }),
      text: async () => {
        textCalls++;
        return '<!DOCTYPE html><title>Captive portal</title><body>Sign in</body>';
      },
    };

    await assert.rejects(
      () => throwIfHubUnreachableResponse(res, 'mailbox outbound'),
      (err) => {
        assert.equal(err.name, 'HubUnreachableError');
        assert.equal(err.code, 'HUB_UNREACHABLE');
        assert.equal(err.statusCode, 200);
        assert.match(err.bodySnippet, /Captive portal/);
        return true;
      },
    );
    assert.equal(textCalls, 1);
  });

  it('classifies successful non-JSON non-HTML Hub responses as hub unreachable', async () => {
    const { throwIfHubUnreachableResponse } = hubFetchMod;
    const statuses = [200, 201, 204, 299];

    for (const status of statuses) {
      let textCalls = 0;
      const res = {
        status,
        ok: true,
        headers: new Headers({ 'content-type': 'text/plain; charset=utf-8' }),
        text: async () => {
          textCalls++;
          return 'temporary proxy maintenance page';
        },
      };

      await assert.rejects(
        () => throwIfHubUnreachableResponse(res, 'mailbox outbound'),
        (err) => {
          assert.equal(err.name, 'HubUnreachableError');
          assert.equal(err.code, 'HUB_UNREACHABLE');
          assert.equal(err.statusCode, status);
          assert.match(err.bodySnippet, /temporary proxy maintenance/);
          return true;
        },
      );
      assert.equal(textCalls, 1, `status ${status} body should be consumed once`);
    }
  });

  it('does not classify JSON auth or JSON server errors as hub unreachable', async () => {
    const { throwIfHubUnreachableResponse } = hubFetchMod;
    for (const status of [403, 500, 503]) {
      let textCalls = 0;
      const res = {
        status,
        ok: false,
        headers: new Headers({ 'content-type': 'application/json' }),
        text: async () => {
          textCalls++;
          return '{"error":"hub_api_error"}';
        },
      };
      await assert.doesNotReject(() => throwIfHubUnreachableResponse(res, 'json api'));
      assert.equal(textCalls, 0, `JSON status ${status} should not consume the body`);
    }
  });

  it('readHubResponseText truncates and cancels long response streams', async () => {
    const { readHubResponseText } = hubFetchMod;
    const encoder = new TextEncoder();
    let cancelled = false;
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(encoder.encode('x'.repeat(64)));
      },
      cancel() {
        cancelled = true;
      },
    });

    const text = await readHubResponseText({ body: stream }, { maxBytes: 8 });
    assert.equal(text, 'xxxxxxxx\n...[truncated]');
    assert.equal(cancelled, true);
  });

  it('readHubResponseText does NOT truncate a stream that exactly fills maxBytes', async () => {
    const { readHubResponseText } = hubFetchMod;
    const encoder = new TextEncoder();
    let cancelled = false;
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(encoder.encode('x'.repeat(8)));
        controller.close();
      },
      cancel() {
        cancelled = true;
      },
    });

    const text = await readHubResponseText({ body: stream }, { maxBytes: 8 });
    assert.equal(text, 'xxxxxxxx', 'a body equal to the cap is complete, not truncated');
    assert.equal(cancelled, false, 'a cleanly-ended stream must not be cancelled');
  });

  it('readHubResponseJson parses a JSON body sitting exactly on the byte cap', async () => {
    const { readHubResponseJson } = hubFetchMod;
    const json = '{"ok":true}';
    const bytes = Buffer.byteLength(json, 'utf8');
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(encoder.encode(json));
        controller.close();
      },
    });

    const data = await readHubResponseJson({ body: stream }, { maxBytes: bytes });
    assert.deepEqual(data, { ok: true });
  });

  it('readHubResponseJson rejects empty response bodies as invalid JSON', async () => {
    const { readHubResponseJson } = hubFetchMod;
    let textCalls = 0;
    const res = {
      status: 200,
      ok: true,
      headers: new Headers({ 'content-type': 'application/json' }),
      text: async () => {
        textCalls++;
        return '';
      },
    };

    await assert.rejects(
      () => readHubResponseJson(res),
      (err) => {
        assert.equal(err instanceof SyntaxError, true);
        assert.match(err.message, /Unexpected end of JSON input/);
        return true;
      },
    );
    assert.equal(textCalls, 1);
  });
});

// --- integration: real HTTPS server with a self-signed cert ---
//
// Proves hubFetch actually refuses an untrusted cert at the wire level
// even when NODE_TLS_REJECT_UNAUTHORIZED=0 is set globally.  Uses Node's
// crypto.X509Certificate / PKI primitives to generate a fresh cert+key
// at test setup so we don't need a fixture committed to the repo.
describe('hubFetch — integration (real TLS rejection)', () => {
  const https = require('node:https');
  const crypto = require('node:crypto');

  let server;
  let port;
  let savedTlsEnv;
  let savedInsecureEnv;
  let skipReason = null;

  before(async () => {
    savedTlsEnv = process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    savedInsecureEnv = process.env.EVOMAP_HUB_ALLOW_INSECURE;
    delete process.env.EVOMAP_HUB_ALLOW_INSECURE;

    // selfsigned cert generation requires either openssl on PATH or a
    // dedicated lib.  We try child_process.spawnSync('openssl', ...) and
    // skip if unavailable — the unit suite above still proves wiring.
    const { spawnSync } = require('node:child_process');
    const os = require('node:os');
    const fs = require('node:fs');
    const path = require('node:path');

    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'hubfetch-tls-'));
    const keyPath = path.join(tmp, 'key.pem');
    const certPath = path.join(tmp, 'cert.pem');
    const result = spawnSync('openssl', [
      'req', '-x509', '-newkey', 'rsa:2048',
      '-keyout', keyPath, '-out', certPath,
      '-days', '1', '-nodes',
      '-subj', '/CN=localhost',
    ], { encoding: 'utf8' });

    if (result.status !== 0 || !fs.existsSync(certPath)) {
      skipReason = 'openssl not available on PATH — integration test skipped';
      return;
    }

    const key = fs.readFileSync(keyPath);
    const cert = fs.readFileSync(certPath);

    server = https.createServer({ key, cert }, (_req, res) => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('{"ok":true}');
    });
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    port = server.address().port;
  });

  after(() => {
    if (server) server.close();
    if (savedTlsEnv === undefined) delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    else process.env.NODE_TLS_REJECT_UNAUTHORIZED = savedTlsEnv;
    if (savedInsecureEnv === undefined) delete process.env.EVOMAP_HUB_ALLOW_INSECURE;
    else process.env.EVOMAP_HUB_ALLOW_INSECURE = savedInsecureEnv;
  });

  it('hubFetch rejects self-signed cert even when NODE_TLS_REJECT_UNAUTHORIZED=0', async (t) => {
    if (skipReason) { t.skip(skipReason); return; }
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

    const { hubFetch } = freshHubFetch();
    await assert.rejects(
      () => hubFetch(`https://127.0.0.1:${port}/probe`, {}),
      (err) => {
        // undici surfaces TLS errors with code SELF_SIGNED_CERT_IN_CHAIN /
        // UNABLE_TO_VERIFY_LEAF_SIGNATURE / DEPTH_ZERO_SELF_SIGNED_CERT
        // depending on chain.  Just assert it's a connection/TLS error.
        const msg = String(err && (err.cause && err.cause.code || err.code || err.message));
        assert.ok(/self.signed|UNABLE_TO_VERIFY|SELF_SIGNED|certificate|TLS/i.test(msg),
          'expected TLS rejection, got: ' + msg);
        return true;
      }
    );
  });

  it('bare fetch with NODE_TLS_REJECT_UNAUTHORIZED=0 ACCEPTS the same cert (control)', async (t) => {
    if (skipReason) { t.skip(skipReason); return; }
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

    // Sanity check: without hubFetch, the env var bypass DOES work.
    // This proves the attack is real and hubFetch is what blocks it.
    const res = await fetch(`https://127.0.0.1:${port}/probe`, {});
    assert.equal(res.ok, true, 'bare fetch should succeed with TLS verification disabled');
  });
});
