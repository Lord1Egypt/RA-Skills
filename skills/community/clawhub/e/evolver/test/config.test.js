const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const config = require('../src/config');
const { envInt, envPositiveInt, envFloat, envStr, resolveHubUrl, antiAbuseTelemetryMode } = config;

// All env accessors read process.env on every call (resolveHubUrl is
// explicitly documented as re-evaluating each call, and the env* helpers
// take an arbitrary key), so these tests drive the real exported functions
// directly — no require-cache juggling needed. We save/restore every env var
// we touch around each test so the suite never leaks state, mirroring
// envFingerprint.test.js.
const TOUCHED_ENV = [
  '__CFG_TEST_KEY__',
  'A2A_HUB_URL',
  'EVOMAP_HUB_URL',
  'EVOLVER_DEFAULT_HUB_URL',
  'EVOMAP_HUB_ALLOW_INSECURE',
  'EVOLVER_ANTI_ABUSE_TELEMETRY',
];
let savedEnv;
beforeEach(function () {
  savedEnv = {};
  for (const k of TOUCHED_ENV) { savedEnv[k] = process.env[k]; delete process.env[k]; }
});
afterEach(function () {
  for (const k of TOUCHED_ENV) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
});

const KEY = '__CFG_TEST_KEY__';

describe('envInt', function () {
  it('falls back when unset', function () {
    assert.equal(envInt(KEY, 42), 42);
  });
  it('falls back on empty string', function () {
    process.env[KEY] = '';
    assert.equal(envInt(KEY, 42), 42);
  });
  it('parses a valid integer', function () {
    process.env[KEY] = '7';
    assert.equal(envInt(KEY, 42), 7);
  });
  it('parses leading integer of a suffixed value (parseInt semantics)', function () {
    process.env[KEY] = '5min';
    assert.equal(envInt(KEY, 42), 5);
  });
  it('falls back on a non-numeric value', function () {
    process.env[KEY] = 'abc';
    assert.equal(envInt(KEY, 42), 42);
  });
  it('accepts 0 and negatives (unlike the positive variant)', function () {
    process.env[KEY] = '0';
    assert.equal(envInt(KEY, 42), 0);
    process.env[KEY] = '-3';
    assert.equal(envInt(KEY, 42), -3);
  });
});

describe('envFloat', function () {
  it('falls back when unset', function () {
    assert.equal(envFloat(KEY, 0.5), 0.5);
  });
  it('falls back on empty string', function () {
    process.env[KEY] = '';
    assert.equal(envFloat(KEY, 0.5), 0.5);
  });
  it('parses a valid float', function () {
    process.env[KEY] = '0.78';
    assert.equal(envFloat(KEY, 0.5), 0.78);
  });
  it('falls back on a non-numeric value', function () {
    process.env[KEY] = 'nope';
    assert.equal(envFloat(KEY, 0.5), 0.5);
  });
});

describe('envStr', function () {
  it('falls back when unset', function () {
    assert.equal(envStr(KEY, 'def'), 'def');
  });
  it('falls back on empty string', function () {
    process.env[KEY] = '';
    assert.equal(envStr(KEY, 'def'), 'def');
  });
  it('returns the set value', function () {
    process.env[KEY] = 'custom';
    assert.equal(envStr(KEY, 'def'), 'custom');
  });
});

describe('envPositiveInt', function () {
  it('falls back when unset', function () {
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('falls back on empty string', function () {
    process.env[KEY] = '';
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('parses a valid positive integer', function () {
    process.env[KEY] = '250';
    assert.equal(envPositiveInt(KEY, 1000), 250);
  });
  it('accepts the leading positive integer of a suffixed value', function () {
    process.env[KEY] = '5min';
    assert.equal(envPositiveInt(KEY, 1000), 5);
  });
  it('rejects 0 (would hot-loop / zero a timeout) and falls back', function () {
    process.env[KEY] = '0';
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('rejects negatives and falls back', function () {
    process.env[KEY] = '-5';
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('rejects a suffix-only NaN value and falls back', function () {
    process.env[KEY] = 'ms';
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('rejects values >= 2^31 (setTimeout downgrades them to 1ms) and falls back', function () {
    process.env[KEY] = String(2 ** 31);
    assert.equal(envPositiveInt(KEY, 1000), 1000);
  });
  it('accepts the largest valid value just below 2^31', function () {
    process.env[KEY] = String(2 ** 31 - 1);
    assert.equal(envPositiveInt(KEY, 1000), 2 ** 31 - 1);
  });
  it('warns at most once per key on invalid input', function () {
    const origWarn = console.warn;
    const calls = [];
    console.warn = (...args) => calls.push(args);
    try {
      // Use a key never warned before in this process so the one-time Set is clean.
      const uniqueKey = '__CFG_TEST_WARN_ONCE__';
      const savedUnique = process.env[uniqueKey];
      try {
        process.env[uniqueKey] = 'not-a-number';
        envPositiveInt(uniqueKey, 1000);
        envPositiveInt(uniqueKey, 1000);
        envPositiveInt(uniqueKey, 1000);
      } finally {
        if (savedUnique === undefined) delete process.env[uniqueKey];
        else process.env[uniqueKey] = savedUnique;
      }
      assert.equal(calls.length, 1, 'expected exactly one warning for repeated invalid reads of the same key');
      assert.match(calls[0][0], /\[config\] __CFG_TEST_WARN_ONCE__=/);
    } finally {
      console.warn = origWarn;
    }
  });
});

describe('antiAbuseTelemetryMode', function () {
  it('defaults to heartbeat mode', function () {
    delete process.env.EVOLVER_ANTI_ABUSE_TELEMETRY;
    assert.equal(antiAbuseTelemetryMode(), 'heartbeat');
  });
  it('allows explicit opt-out', function () {
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'off';
    assert.equal(antiAbuseTelemetryMode(), 'off');
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'false';
    assert.equal(antiAbuseTelemetryMode(), 'off');
  });
  it('enables heartbeat mode for explicit truthy values', function () {
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'heartbeat';
    assert.equal(antiAbuseTelemetryMode(), 'heartbeat');
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'true';
    assert.equal(antiAbuseTelemetryMode(), 'heartbeat');
  });
  it('keeps unknown values off', function () {
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = 'full';
    assert.equal(antiAbuseTelemetryMode(), 'off');
  });
  it('treats an empty / blank env value as unset (default-on), not as opt-out', function () {
    // A bare `EVOLVER_ANTI_ABUSE_TELEMETRY=` line in a .env file must not
    // silently disable the documented default-on behavior (Bugbot, PR #216).
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = '';
    assert.equal(antiAbuseTelemetryMode(), 'heartbeat');
    process.env.EVOLVER_ANTI_ABUSE_TELEMETRY = '   ';
    assert.equal(antiAbuseTelemetryMode(), 'heartbeat');
  });
});

describe('resolveHubUrl', function () {
  it('returns the compile-time default when no env override is set', function () {
    assert.equal(resolveHubUrl(), config.PUBLIC_DEFAULT_HUB_URL);
    assert.equal(resolveHubUrl(), 'https://evomap.ai');
  });
  it('prefers A2A_HUB_URL over all other sources', function () {
    process.env.A2A_HUB_URL = 'https://a2a.example';
    process.env.EVOMAP_HUB_URL = 'https://evomap2.example';
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://deploy.example';
    assert.equal(resolveHubUrl(), 'https://a2a.example');
  });
  it('falls back to EVOMAP_HUB_URL when A2A_HUB_URL is unset', function () {
    process.env.EVOMAP_HUB_URL = 'https://evomap2.example';
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://deploy.example';
    assert.equal(resolveHubUrl(), 'https://evomap2.example');
  });
  it('falls back to EVOLVER_DEFAULT_HUB_URL when the higher tiers are unset', function () {
    process.env.EVOLVER_DEFAULT_HUB_URL = 'https://deploy.example';
    assert.equal(resolveHubUrl(), 'https://deploy.example');
  });
  it('re-evaluates on every call (no module-load caching)', function () {
    assert.equal(resolveHubUrl(), 'https://evomap.ai');
    process.env.A2A_HUB_URL = 'https://later.example';
    assert.equal(resolveHubUrl(), 'https://later.example');
  });
  it('throws on a non-https hub URL by default', function () {
    process.env.A2A_HUB_URL = 'http://insecure.example';
    assert.throws(() => resolveHubUrl(), /must use https/);
  });
  it('throws on a syntactically invalid hub URL by default', function () {
    process.env.A2A_HUB_URL = 'not a url';
    assert.throws(() => resolveHubUrl(), /not a valid URL/);
  });
  it('allows a non-https hub URL when EVOMAP_HUB_ALLOW_INSECURE=1', function () {
    process.env.A2A_HUB_URL = 'http://insecure.example';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = '1';
    assert.equal(resolveHubUrl(), 'http://insecure.example');
  });
  it('does not bypass the https check for ALLOW_INSECURE values other than exactly "1"', function () {
    process.env.A2A_HUB_URL = 'http://insecure.example';
    process.env.EVOMAP_HUB_ALLOW_INSECURE = 'true';
    assert.throws(() => resolveHubUrl(), /must use https/);
  });
});
