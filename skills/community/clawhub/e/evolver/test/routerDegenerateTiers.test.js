'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { buildMessagesHandler } = require('../src/proxy/router/messages_route');

// Stubs an _proxyAnthropic-shaped function (status 200 JSON envelope).
function makeStubProxy() {
  const calls = [];
  const fn = async (reqPath, body, opts) => {
    calls.push({ reqPath, body, opts });
    return {
      status: 200,
      headers: { 'content-type': 'application/json' },
      stream: null,
      json: async () => ({ id: 'msg_1', model: body && body.model, content: [] }),
      text: async () => '',
    };
  };
  return { fn, calls };
}

function makeLogger() {
  const lines = [];
  return {
    log: (s) => lines.push({ stream: 'log', s }),
    warn: (s) => lines.push({ stream: 'warn', s }),
    error: () => {},
    lines,
  };
}

// Helper: snapshot + restore the three per-tier env vars around a body so the
// suite never leaks tier config into sibling test files.
function withTierEnv(env, fn) {
  const keys = ['EVOMAP_MODEL_CHEAP', 'EVOMAP_MODEL_MID', 'EVOMAP_MODEL_EXPENSIVE'];
  const prev = {};
  for (const k of keys) prev[k] = process.env[k];
  try {
    for (const k of keys) {
      if (env[k] === undefined) delete process.env[k];
      else process.env[k] = env[k];
    }
    return fn();
  } finally {
    for (const k of keys) {
      if (prev[k] === undefined) delete process.env[k];
      else process.env[k] = prev[k];
    }
  }
}

function degenerateWarns(logger) {
  return logger.lines
    .filter((l) => l.stream === 'warn')
    .map((l) => { try { return JSON.parse(l.s); } catch { return null; } })
    .filter((o) => o && o.event === 'router_degenerate_tiers');
}

describe('router degenerate-tier boot WARN (#152)', () => {
  it('emits one router_degenerate_tiers WARN when enabled and all tiers collapse to one model', () => {
    const { fn } = makeStubProxy();
    const logger = makeLogger();
    withTierEnv(
      {
        EVOMAP_MODEL_CHEAP: 'global.anthropic.claude-opus-4-7',
        EVOMAP_MODEL_MID: 'global.anthropic.claude-opus-4-7',
        EVOMAP_MODEL_EXPENSIVE: 'global.anthropic.claude-opus-4-7',
      },
      () => buildMessagesHandler({ anthropicProxy: fn, logger, routerEnabled: true }),
    );
    const warns = degenerateWarns(logger);
    assert.equal(warns.length, 1, 'exactly one degenerate-tier WARN at construction');
    assert.equal(warns[0].model, 'global.anthropic.claude-opus-4-7');
    assert.match(warns[0].message, /no .*cost-saving/i);
    assert.match(warns[0].message, /EVOMAP_MODEL_CHEAP/);
  });

  it('does NOT warn when tiers are distinct (real cost-saving config)', () => {
    const { fn } = makeStubProxy();
    const logger = makeLogger();
    withTierEnv(
      {
        EVOMAP_MODEL_CHEAP: 'global.anthropic.claude-haiku-4-5-20251001-v1:0',
        EVOMAP_MODEL_MID: 'global.anthropic.claude-sonnet-4-6',
        EVOMAP_MODEL_EXPENSIVE: 'global.anthropic.claude-opus-4-7',
      },
      () => buildMessagesHandler({ anthropicProxy: fn, logger, routerEnabled: true }),
    );
    assert.equal(degenerateWarns(logger).length, 0, 'distinct tiers must not warn');
  });

  it('does NOT warn when the router is disabled, even if tiers are degenerate', () => {
    const { fn } = makeStubProxy();
    const logger = makeLogger();
    withTierEnv(
      {
        EVOMAP_MODEL_CHEAP: 'global.anthropic.claude-opus-4-7',
        EVOMAP_MODEL_MID: 'global.anthropic.claude-opus-4-7',
        EVOMAP_MODEL_EXPENSIVE: 'global.anthropic.claude-opus-4-7',
      },
      () => buildMessagesHandler({ anthropicProxy: fn, logger, routerEnabled: false }),
    );
    assert.equal(degenerateWarns(logger).length, 0, 'disabled router must not warn');
  });

  it('warns when only two of three tiers collapse is NOT degenerate (partial override)', () => {
    // cheap overridden, mid+expensive still equal -> 2 distinct -> not degenerate.
    const { fn } = makeStubProxy();
    const logger = makeLogger();
    withTierEnv(
      {
        EVOMAP_MODEL_CHEAP: 'global.anthropic.claude-haiku-4-5-20251001-v1:0',
        EVOMAP_MODEL_MID: 'global.anthropic.claude-opus-4-7',
        EVOMAP_MODEL_EXPENSIVE: 'global.anthropic.claude-opus-4-7',
      },
      () => buildMessagesHandler({ anthropicProxy: fn, logger, routerEnabled: true }),
    );
    assert.equal(degenerateWarns(logger).length, 0, 'two distinct tiers is a real routing config');
  });
});
