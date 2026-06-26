const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

const savedEnv = {};
const envKeys = [
  'EVOLVER_ATP', 'EVOLVER_ATP_SERVICES', 'EVOLVER_AGENT_NAME', 'EVOLVER_MODEL_NAME',
];

beforeEach(() => {
  for (const k of envKeys) { savedEnv[k] = process.env[k]; delete process.env[k]; }
});

afterEach(() => {
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
});

describe('defaultHandler', () => {
  const { defaultOrderHandler, resolveAtpServices, getAtpMode } = require('../src/atp/defaultHandler');

  describe('getAtpMode', () => {
    it('defaults to auto', () => {
      assert.equal(getAtpMode(), 'auto');
    });

    it('returns off for EVOLVER_ATP=off', () => {
      process.env.EVOLVER_ATP = 'off';
      assert.equal(getAtpMode(), 'off');
    });

    it('returns off for EVOLVER_ATP=false', () => {
      process.env.EVOLVER_ATP = 'false';
      assert.equal(getAtpMode(), 'off');
    });

    it('returns off for EVOLVER_ATP=0', () => {
      process.env.EVOLVER_ATP = '0';
      assert.equal(getAtpMode(), 'off');
    });

    it('returns on for EVOLVER_ATP=on', () => {
      process.env.EVOLVER_ATP = 'on';
      assert.equal(getAtpMode(), 'on');
    });

    it('returns on for EVOLVER_ATP=true', () => {
      process.env.EVOLVER_ATP = 'true';
      assert.equal(getAtpMode(), 'on');
    });

    it('returns auto for unknown value', () => {
      process.env.EVOLVER_ATP = 'maybe';
      assert.equal(getAtpMode(), 'auto');
    });
  });

  describe('resolveAtpServices', () => {
    it('returns default service when no env set', () => {
      const services = resolveAtpServices();
      assert.equal(services.length, 1);
      assert.ok(services[0].title.includes('Evolver Agent'));
      assert.ok(services[0].capabilities.includes('code_evolution'));
      assert.equal(services[0].pricePerTask, 5);
    });

    it('uses EVOLVER_AGENT_NAME in title', () => {
      process.env.EVOLVER_AGENT_NAME = 'TestBot';
      const services = resolveAtpServices();
      assert.ok(services[0].title.startsWith('TestBot'));
    });

    it('parses EVOLVER_ATP_SERVICES JSON', () => {
      process.env.EVOLVER_ATP_SERVICES = JSON.stringify([
        { title: 'Custom Service', capabilities: ['custom'], pricePerTask: 99 },
      ]);
      const services = resolveAtpServices();
      assert.equal(services.length, 1);
      assert.equal(services[0].title, 'Custom Service');
      assert.equal(services[0].pricePerTask, 99);
    });

    it('falls back to default on invalid JSON', () => {
      process.env.EVOLVER_ATP_SERVICES = 'not-json';
      const services = resolveAtpServices();
      assert.equal(services.length, 1);
      assert.ok(services[0].title.includes('Evolver Agent'));
    });

    it('falls back to default on empty array', () => {
      process.env.EVOLVER_ATP_SERVICES = '[]';
      const services = resolveAtpServices();
      assert.equal(services.length, 1);
    });
  });

  describe('defaultOrderHandler', () => {
    it('returns code review result for review signal', () => {
      const result = defaultOrderHandler({ title: '', signals: 'code_review,javascript' });
      assert.ok(result.result.includes('review'));
      assert.equal(result.pass_rate, 1.0);
      assert.equal(result.processor, 'evolver-default');
    });

    it('returns translation result for translation title', () => {
      const result = defaultOrderHandler({ title: 'Translate this document', signals: '' });
      assert.ok(result.result.includes('Translation'));
    });

    it('returns summary result for summarization signal', () => {
      const result = defaultOrderHandler({ title: '', signals: 'summarization' });
      assert.ok(result.result.includes('Summarization'));
    });

    it('returns generic result for unknown task', () => {
      const result = defaultOrderHandler({ title: 'Unknown task', signals: 'random' });
      assert.ok(result.result.includes('processed by evolver'));
    });

    it('handles missing title/signals', () => {
      const result = defaultOrderHandler({});
      assert.ok(result.result);
      assert.equal(result.pass_rate, 1.0);
    });
  });
});

describe('merchantAgent idempotency', () => {
  const merchantAgent = require('../src/atp/merchantAgent');

  it('isRunning returns false initially', () => {
    assert.equal(merchantAgent.isRunning(), false);
  });
});
