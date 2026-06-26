'use strict';

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');

const { buildMessagesHandler } = require('../src/proxy/router/messages_route');

// Stubs an _proxyAnthropic-shaped function that records what it received
// and returns a fixed 200 JSON envelope.
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

describe('Phase C slice 6 — EVOMAP_ROUTER_ENABLED gating + router_decision log', () => {
  // Hermetic tier-model env: pin the per-tier env vars so this suite stays
  // green regardless of what DEFAULT_TIER_MODELS happens to be on main.
  // Operators sometimes run "all tiers point to one model" while tuning;
  // those are valid daemon configs but break tier-distinguishing tests.
  let prevCheap, prevMid, prevExpensive;
  before(() => {
    prevCheap = process.env.EVOMAP_MODEL_CHEAP;
    prevMid = process.env.EVOMAP_MODEL_MID;
    prevExpensive = process.env.EVOMAP_MODEL_EXPENSIVE;
    process.env.EVOMAP_MODEL_CHEAP = 'global.anthropic.claude-haiku-4-5-20251001-v1:0';
    process.env.EVOMAP_MODEL_MID = 'global.anthropic.claude-sonnet-4-6';
    process.env.EVOMAP_MODEL_EXPENSIVE = 'global.anthropic.claude-opus-4-7';
  });
  after(() => {
    if (prevCheap === undefined) delete process.env.EVOMAP_MODEL_CHEAP;
    else process.env.EVOMAP_MODEL_CHEAP = prevCheap;
    if (prevMid === undefined) delete process.env.EVOMAP_MODEL_MID;
    else process.env.EVOMAP_MODEL_MID = prevMid;
    if (prevExpensive === undefined) delete process.env.EVOMAP_MODEL_EXPENSIVE;
    else process.env.EVOMAP_MODEL_EXPENSIVE = prevExpensive;
  });

  it('forwards body unmodified when routerEnabled=false (default)', async () => {
    const { fn, calls } = makeStubProxy();
    const logger = makeLogger();
    const handler = buildMessagesHandler({
      anthropicProxy: fn,
      logger,
      routerEnabled: false,
    });

    const body = {
      model: 'global.anthropic.claude-opus-4-7',
      messages: [{ role: 'user', content: 'what is npm?' }],
    };
    const res = await handler({
      body,
      headers: { 'x-api-key': 'sk-test' },
    });
    assert.equal(res.status, 200);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].body.model, 'global.anthropic.claude-opus-4-7', 'model must not be rewritten when disabled');
    assert.equal(calls[0].body, body, 'body identity preserved on the off-path');
    assert.equal(logger.lines.length, 0, 'no log lines emitted when disabled');
  });

  it('emits a router_decision JSON log line when routerEnabled=true', async () => {
    const { fn } = makeStubProxy();
    const logger = makeLogger();
    const handler = buildMessagesHandler({
      anthropicProxy: fn,
      logger,
      routerEnabled: true,
    });

    await handler({
      body: {
        model: 'global.anthropic.claude-opus-4-7',
        messages: [{ role: 'user', content: 'what is npm?' }],
      },
      headers: { 'x-api-key': 'sk-test' },
    });

    const decisionLines = logger.lines
      .filter((l) => l.stream === 'log')
      .map((l) => JSON.parse(l.s));
    assert.equal(decisionLines.length, 1, 'exactly one router_decision log per request');
    const d = decisionLines[0];
    assert.equal(d.event, 'router_decision');
    assert.equal(d.tier, 'cheap');
    assert.equal(d.reason, 'trivial_lookup');
    assert.equal(d.original_model, 'global.anthropic.claude-opus-4-7');
    assert.equal(d.chosen_model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0');
    assert.equal(d.escalation_skipped, false);
    assert.equal(d.fallback, null);
  });

  it('records fallback=classifier_error in the log when classifier throws', async () => {
    const { fn, calls } = makeStubProxy();
    const logger = makeLogger();
    // Pollute body with a recursive reference so extractFeatures crashes when
    // it tries to walk messages — simulates a runtime classifier failure
    // without mocking the classifier module.
    const handler = buildMessagesHandler({
      anthropicProxy: fn,
      logger,
      routerEnabled: true,
    });

    const body = { model: 'global.anthropic.claude-opus-4-7' };
    Object.defineProperty(body, 'messages', {
      get() { throw new Error('boom'); },
    });

    const res = await handler({ body, headers: { 'x-api-key': 'sk-test' } });
    assert.equal(res.status, 200);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].body, body, 'body forwarded unmodified on classifier_error');

    const warnLines = logger.lines.filter((l) => l.stream === 'warn').map((l) => JSON.parse(l.s));
    const decisionLines = logger.lines.filter((l) => l.stream === 'log').map((l) => JSON.parse(l.s));
    assert.equal(warnLines.length, 1);
    assert.equal(warnLines[0].event, 'router_fallback');
    assert.equal(warnLines[0].reason, 'classifier_error');
    assert.equal(decisionLines.length, 1);
    assert.equal(decisionLines[0].fallback, 'classifier_error');
    assert.equal(decisionLines[0].tier, null, 'no tier when classifier failed');
    assert.equal(decisionLines[0].chosen_model, 'global.anthropic.claude-opus-4-7', 'falls back to original model');
  });

  it('honors EVOMAP_ROUTER_ENABLED=1 from the environment when option omitted', async () => {
    const prev = process.env.EVOMAP_ROUTER_ENABLED;
    process.env.EVOMAP_ROUTER_ENABLED = '1';
    try {
      const { fn, calls } = makeStubProxy();
      const logger = makeLogger();
      const handler = buildMessagesHandler({ anthropicProxy: fn, logger });
      await handler({
        body: { model: 'global.anthropic.claude-opus-4-7', messages: [{ role: 'user', content: 'what is npm?' }] },
        headers: { 'x-api-key': 'sk-test' },
      });
      assert.equal(calls[0].body.model, 'global.anthropic.claude-haiku-4-5-20251001-v1:0', 'env flag enables rewrite');
      const decisionLines = logger.lines.filter((l) => l.stream === 'log');
      assert.equal(decisionLines.length, 1);
    } finally {
      if (prev === undefined) delete process.env.EVOMAP_ROUTER_ENABLED;
      else process.env.EVOMAP_ROUTER_ENABLED = prev;
    }
  });

  it('defaults to disabled when env var is unset or not exactly "1"', async () => {
    const prev = process.env.EVOMAP_ROUTER_ENABLED;
    for (const val of [undefined, '', '0', 'true', 'yes']) {
      if (val === undefined) delete process.env.EVOMAP_ROUTER_ENABLED;
      else process.env.EVOMAP_ROUTER_ENABLED = val;
      const { fn, calls } = makeStubProxy();
      const logger = makeLogger();
      const handler = buildMessagesHandler({ anthropicProxy: fn, logger });
      await handler({
        body: { model: 'global.anthropic.claude-opus-4-7', messages: [{ role: 'user', content: 'what is npm?' }] },
        headers: { 'x-api-key': 'sk-test' },
      });
      assert.equal(calls[0].body.model, 'global.anthropic.claude-opus-4-7',
        `value ${JSON.stringify(val)} must not enable rewrite`);
      assert.equal(logger.lines.length, 0);
    }
    if (prev === undefined) delete process.env.EVOMAP_ROUTER_ENABLED;
    else process.env.EVOMAP_ROUTER_ENABLED = prev;
  });
});
