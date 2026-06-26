'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { EvoMapProxy } = require('../src/proxy');
const { PUBLIC_DEFAULT_HUB_URL } = require('../src/config');

// Save/restore every env var resolveHubUrl() consults so cases don't leak.
const HUB_ENV = ['A2A_HUB_URL', 'EVOMAP_HUB_URL', 'EVOLVER_DEFAULT_HUB_URL', 'EVOMAP_HUB_ALLOW_INSECURE'];
function withHubEnv(overrides, fn) {
  const saved = {};
  for (const k of HUB_ENV) saved[k] = process.env[k];
  for (const k of HUB_ENV) delete process.env[k];
  for (const [k, v] of Object.entries(overrides)) process.env[k] = v;
  try {
    return fn();
  } finally {
    for (const k of HUB_ENV) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
  }
}

// evolver#567: a freshly-constructed proxy with no explicit Hub URL must default
// to the canonical public Hub instead of '' (hub-less/offline). Previously the
// proxy read `process.env.A2A_HUB_URL || ''` directly, so running `evolver`
// without exporting A2A_HUB_URL left the proxy in offline mode even after a
// successful `evolver login` — MCP Hub tools returned 503 "Hub not configured"
// and evolver_status reported node_id: null.
describe('EvoMapProxy hubUrl default (evolver#567)', () => {
  it('defaults to the canonical Hub when no Hub env is set', () => {
    withHubEnv({}, () => {
      const proxy = new EvoMapProxy();
      assert.equal(proxy.hubUrl, PUBLIC_DEFAULT_HUB_URL);
      assert.equal(proxy.hubUrl, 'https://evomap.ai');
    });
  });

  it('honours A2A_HUB_URL when set (and trims trailing slash)', () => {
    withHubEnv({ A2A_HUB_URL: 'https://hub.example.test/' }, () => {
      const proxy = new EvoMapProxy();
      assert.equal(proxy.hubUrl, 'https://hub.example.test');
    });
  });

  it('lets opts.hubUrl win over env', () => {
    withHubEnv({ A2A_HUB_URL: 'https://hub.example.test' }, () => {
      const proxy = new EvoMapProxy({ hubUrl: 'https://explicit.example.test' });
      assert.equal(proxy.hubUrl, 'https://explicit.example.test');
    });
  });

  it('still allows an http hub for local/mock dev via EVOMAP_HUB_ALLOW_INSECURE=1', () => {
    withHubEnv({ A2A_HUB_URL: 'http://127.0.0.1:19999', EVOMAP_HUB_ALLOW_INSECURE: '1' }, () => {
      const proxy = new EvoMapProxy();
      assert.equal(proxy.hubUrl, 'http://127.0.0.1:19999');
    });
  });
});
