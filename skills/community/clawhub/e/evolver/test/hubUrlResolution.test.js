// Tests for config.resolveHubUrl() introduced in v1.69.7.
//
// Before v1.69.7, several modules bound their HUB_URL at require()-time from
// process.env.A2A_HUB_URL || process.env.EVOMAP_HUB_URL || 'https://evomap.ai'.
// That meant setting A2A_HUB_URL at runtime (e.g. in tests or wrappers) did
// nothing. The new resolveHubUrl() re-reads env on every call.
//
// Since v1.84.x: resolveHubUrl() rejects non-https URLs by default.
// Set EVOMAP_HUB_ALLOW_INSECURE=1 to bypass (local dev / mock hub only).

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

function freshConfig() {
  const resolved = require.resolve('../src/config');
  delete require.cache[resolved];
  return require(resolved);
}

function freshModule(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
  return require(resolved);
}

describe('config.resolveHubUrl', () => {
  const savedEnv = {};
  const envKeys = [
    'A2A_HUB_URL',
    'EVOMAP_HUB_URL',
    'EVOLVER_DEFAULT_HUB_URL',
    'EVOMAP_HUB_ALLOW_INSECURE',
  ];

  beforeEach(() => {
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) {
        delete process.env[k];
      } else {
        process.env[k] = savedEnv[k];
      }
    }
  });

  it('falls back to PUBLIC_DEFAULT_HUB_URL when no env is set', () => {
    const { resolveHubUrl, PUBLIC_DEFAULT_HUB_URL } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://evomap.ai');
    assert.equal(PUBLIC_DEFAULT_HUB_URL, 'https://evomap.ai');
  });

  it('A2A_HUB_URL takes highest priority', () => {
    process.env.A2A_HUB_URL = 'https://primary.example.com';
    process.env.EVOMAP_HUB_URL = 'https://secondary.example.com';
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://deployment.example.com';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://primary.example.com');
  });

  it('EVOMAP_HUB_URL wins when A2A_HUB_URL is empty', () => {
    process.env.EVOMAP_HUB_URL = 'https://legacy.example.com';
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://deployment.example.com';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://legacy.example.com');
  });

  it('EVOLVER_DEFAULT_HUB_URL is honored for air-gapped deployments', () => {
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://private-hub.internal';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://private-hub.internal');
  });

  it('re-reads env on every call (lazy)', () => {
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://evomap.ai');

    process.env.A2A_HUB_URL = 'https://first.example.com';
    assert.equal(resolveHubUrl(), 'https://first.example.com');

    process.env.A2A_HUB_URL = 'https://second.example.com';
    assert.equal(resolveHubUrl(), 'https://second.example.com');

    delete process.env.A2A_HUB_URL;
    assert.equal(resolveHubUrl(), 'https://evomap.ai');
  });

  it('treats empty-string env vars the same as unset', () => {
    process.env.A2A_HUB_URL = '';
    process.env.EVOMAP_HUB_URL = '';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'https://evomap.ai');
  });

  // #580 Bug 1: a `.env` value with surrounding whitespace (common with a
  // quoted entry like A2A_HUB_URL="https://evomap.ai ") must be trimmed.
  // Otherwise the trailing space survives `hubUrl.replace(/\/+$/, '')` at
  // endpoint construction and produces "https://evomap.ai /a2a/events/poll",
  // which fails hubFetch URL validation.
  it('trims surrounding whitespace from the hub URL (#580)', () => {
    process.env.A2A_HUB_URL = '  https://evomap.ai  ';
    const { resolveHubUrl } = freshConfig();
    const url = resolveHubUrl();
    assert.equal(url, 'https://evomap.ai');
    // The exact failure mode from the issue: base + path must not contain a space.
    assert.equal(url.replace(/\/+$/, '') + '/a2a/events/poll',
      'https://evomap.ai/a2a/events/poll');
  });

  it('treats a whitespace-only env var the same as unset (#580)', () => {
    process.env.A2A_HUB_URL = '   ';
    process.env.EVOMAP_HUB_URL = 'https://fallback.example.com';
    const { resolveHubUrl } = freshConfig();
    // Whitespace-only A2A_HUB_URL must fall through to EVOMAP_HUB_URL, not be
    // picked as a "truthy" value.
    assert.equal(resolveHubUrl(), 'https://fallback.example.com');
  });

  // --- https-only enforcement (C1 PR-2 Step 1) ---

  it('throws on http:// URL by default (MITM guard)', () => {
    process.env.A2A_HUB_URL = 'http://hub.example.com';
    const { resolveHubUrl } = freshConfig();
    assert.throws(
      () => resolveHubUrl(),
      (err) => {
        assert.ok(err.message.includes('https://'), 'error should mention https://');
        assert.ok(err.message.includes('EVOMAP_HUB_ALLOW_INSECURE'), 'error should name the escape hatch');
        return true;
      }
    );
  });

  it('throws on ws:// URL by default', () => {
    process.env.A2A_HUB_URL = 'ws://hub.example.com';
    const { resolveHubUrl } = freshConfig();
    assert.throws(() => resolveHubUrl(), /https:\/\//);
  });

  it('throws on unparseable URL', () => {
    process.env.A2A_HUB_URL = 'not-a-url';
    const { resolveHubUrl } = freshConfig();
    assert.throws(() => resolveHubUrl(), /not a valid URL/);
  });

  it('EVOMAP_HUB_ALLOW_INSECURE=1 bypasses https check (local dev / mock hub)', () => {
    process.env.A2A_HUB_URL = 'http://localhost:4000';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'http://localhost:4000');
  });

  it('EVOMAP_HUB_ALLOW_INSECURE=1 also allows unparseable URL', () => {
    process.env.A2A_HUB_URL = 'not-a-url';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    const { resolveHubUrl } = freshConfig();
    assert.equal(resolveHubUrl(), 'not-a-url');
  });

  it('EVOMAP_HUB_ALLOW_INSECURE values other than "1" do not bypass', () => {
    process.env.A2A_HUB_URL = 'http://hub.example.com';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = 'true';
    const { resolveHubUrl } = freshConfig();
    assert.throws(() => resolveHubUrl(), /https:\/\//);
  });
});

describe('Search-First hub URL helpers', () => {
  const savedEnv = {};
  const envKeys = [
    'A2A_HUB_URL',
    'EVOMAP_HUB_URL',
  ];

  beforeEach(() => {
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) {
        delete process.env[k];
      } else {
        process.env[k] = savedEnv[k];
      }
    }
  });

  for (const [label, modulePath] of [
    ['hubSearch.getHubUrl', '../src/gep/hubSearch'],
    ['hubReview.getHubUrl', '../src/gep/hubReview'],
  ]) {
    it(label + ' trims surrounding whitespace before endpoint construction', () => {
      process.env.A2A_HUB_URL = '  https://evomap.ai/  ';
      const { getHubUrl } = freshModule(modulePath);
      const url = getHubUrl();
      assert.equal(url, 'https://evomap.ai');
      assert.equal(url.replace(/\/+$/, '') + '/a2a/fetch', 'https://evomap.ai/a2a/fetch');
    });

    it(label + ' falls back to EVOMAP_HUB_URL when A2A_HUB_URL is whitespace-only', () => {
      process.env.A2A_HUB_URL = '   ';
      process.env.EVOMAP_HUB_URL = 'https://fallback.example.com';
      const { getHubUrl } = freshModule(modulePath);
      assert.equal(getHubUrl(), 'https://fallback.example.com');
    });
  }
});
