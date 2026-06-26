const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { captureEnvFingerprint, envFingerprintKey, isSameEnvClass, detectModelName } = require('../src/gep/envFingerprint');

// Env vars detectModelName() reads, in priority order. Saved/restored around
// each model test so the suite never leaks state into other tests.
const MODEL_ENV_VARS = [
  'EVOLVER_MODEL_NAME',
  'ANTHROPIC_MODEL',
  'CLAUDE_MODEL',
  'CLAUDE_CODE_MODEL',
  'OPENAI_MODEL',
  'CODEX_MODEL',
  'CURSOR_MODEL',
];
function withModelEnv(overrides, fn) {
  const saved = {};
  for (const k of MODEL_ENV_VARS) { saved[k] = process.env[k]; delete process.env[k]; }
  try {
    for (const [k, v] of Object.entries(overrides)) process.env[k] = v;
    return fn();
  } finally {
    for (const k of MODEL_ENV_VARS) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
  }
}

describe('captureEnvFingerprint', function () {
  it('returns an object with expected fields', function () {
    const fp = captureEnvFingerprint();
    assert.equal(typeof fp, 'object');
    assert.equal(typeof fp.device_id, 'string');
    assert.equal(typeof fp.node_version, 'string');
    assert.equal(typeof fp.platform, 'string');
    assert.equal(typeof fp.arch, 'string');
    assert.equal(typeof fp.os_release, 'string');
    assert.equal(typeof fp.hostname, 'string');
    assert.equal(typeof fp.container, 'boolean');
    assert.equal(typeof fp.cwd, 'string');
  });

  it('hashes hostname to 12 chars', function () {
    const fp = captureEnvFingerprint();
    assert.equal(fp.hostname.length, 12);
  });

  it('hashes cwd to 12 chars', function () {
    const fp = captureEnvFingerprint();
    assert.equal(fp.cwd.length, 12);
  });

  it('node_version starts with v', function () {
    const fp = captureEnvFingerprint();
    assert.ok(fp.node_version.startsWith('v'));
  });

  it('includes a model field (string, never empty)', function () {
    const fp = captureEnvFingerprint();
    assert.equal(typeof fp.model, 'string');
    assert.ok(fp.model.length > 0);
  });

  it('reports the explicit model when EVOLVER_MODEL_NAME is set', function () {
    withModelEnv({ EVOLVER_MODEL_NAME: 'claude-opus-4-8' }, function () {
      const fp = captureEnvFingerprint();
      assert.equal(fp.model, 'claude-opus-4-8');
    });
  });

  it('falls back to "unknown" when no model env var is set', function () {
    withModelEnv({}, function () {
      const fp = captureEnvFingerprint();
      assert.equal(fp.model, 'unknown');
    });
  });

  it('returns consistent results across calls', function () {
    const fp1 = captureEnvFingerprint();
    const fp2 = captureEnvFingerprint();
    assert.equal(fp1.device_id, fp2.device_id);
    assert.equal(fp1.platform, fp2.platform);
    assert.equal(fp1.hostname, fp2.hostname);
  });
});

describe('envFingerprintKey', function () {
  it('returns a 16-char hex string', function () {
    const fp = captureEnvFingerprint();
    const key = envFingerprintKey(fp);
    assert.equal(typeof key, 'string');
    assert.equal(key.length, 16);
    assert.match(key, /^[0-9a-f]{16}$/);
  });

  it('returns unknown for null input', function () {
    assert.equal(envFingerprintKey(null), 'unknown');
  });

  it('returns unknown for non-object input', function () {
    assert.equal(envFingerprintKey('string'), 'unknown');
  });

  it('same fingerprint produces same key', function () {
    const fp = captureEnvFingerprint();
    assert.equal(envFingerprintKey(fp), envFingerprintKey(fp));
  });

  it('different fingerprints produce different keys', function () {
    const fp1 = captureEnvFingerprint();
    const fp2 = { ...fp1, device_id: 'different_device' };
    assert.notEqual(envFingerprintKey(fp1), envFingerprintKey(fp2));
  });

  it('is model-independent: same env, different model -> same key', function () {
    const fp1 = captureEnvFingerprint();
    const fp2 = { ...fp1, model: 'some-other-model' };
    assert.equal(envFingerprintKey(fp1), envFingerprintKey(fp2));
  });
});

describe('detectModelName', function () {
  it('returns "unknown" when no model env var is set', function () {
    withModelEnv({}, function () {
      assert.equal(detectModelName(), 'unknown');
    });
  });

  it('prefers EVOLVER_MODEL_NAME over host CLI vars', function () {
    withModelEnv({ EVOLVER_MODEL_NAME: 'explicit-model', ANTHROPIC_MODEL: 'host-model' }, function () {
      assert.equal(detectModelName(), 'explicit-model');
    });
  });

  it('falls back to host CLI model vars (ANTHROPIC_MODEL)', function () {
    withModelEnv({ ANTHROPIC_MODEL: 'claude-sonnet-4-6' }, function () {
      assert.equal(detectModelName(), 'claude-sonnet-4-6');
    });
  });

  it('trims whitespace and ignores blank values', function () {
    withModelEnv({ EVOLVER_MODEL_NAME: '   ', OPENAI_MODEL: '  gpt-4o  ' }, function () {
      assert.equal(detectModelName(), 'gpt-4o');
    });
  });

  it('caps model name length at 100 chars', function () {
    withModelEnv({ EVOLVER_MODEL_NAME: 'x'.repeat(250) }, function () {
      assert.equal(detectModelName().length, 100);
    });
  });
});

describe('isSameEnvClass', function () {
  it('returns true for identical fingerprints', function () {
    const fp = captureEnvFingerprint();
    assert.equal(isSameEnvClass(fp, fp), true);
  });

  it('returns true for fingerprints with same key fields', function () {
    const fp1 = captureEnvFingerprint();
    const fp2 = { ...fp1, cwd: 'different_cwd' };
    assert.equal(isSameEnvClass(fp1, fp2), true);
  });

  it('returns false for different environments', function () {
    const fp1 = captureEnvFingerprint();
    const fp2 = { ...fp1, device_id: 'other_device' };
    assert.equal(isSameEnvClass(fp1, fp2), false);
  });
});
