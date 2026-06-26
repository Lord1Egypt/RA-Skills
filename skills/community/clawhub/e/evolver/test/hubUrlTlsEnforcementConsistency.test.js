// Multi-module TLS-enforcement consistency.
//
// Pre-fix posture across the codebase:
//
//   src/gep/hubFetch.js          → refused http://... unless EVOMAP_HUB_ALLOW_INSECURE=1
//   src/atp/atpExecute._postJson → silently used `lib = http` for any http:// URL
//   src/atp/hubClient._hubPost   → bare native fetch(), no scheme check
//   src/atp/hubClient._hubGet    → same
//
// An operator override `A2A_HUB_URL=http://...` would let hubFetch-routed
// calls (heartbeat, solidify verify) refuse the URL while the ATP path
// silently sent the Authorization: Bearer <nodeSecret> header in
// cleartext. These tests pin the post-fix contract: all three call sites
// honour the same enforce-or-bypass posture as hubFetch.

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

async function withEnv(overrides, fn) {
  // MUST be async and await fn(): when fn is async, `return fn()` returns
  // the Promise synchronously, and a non-async `finally` would restore env
  // before the async work resumes. `enforceHubScheme` reads
  // `process.env.EVOMAP_HUB_ALLOW_INSECURE` from across `await`s in
  // completeAtpTask / hubClient, so a sync finally lets it observe the
  // ambient value instead of the override — a test running in a shell
  // with EVOMAP_HUB_ALLOW_INSECURE already set (or inherited from a
  // previous test file) would silently bypass the guard and pass for
  // the wrong reason (Bugbot PR #160 Medium).
  const orig = {};
  for (const k of Object.keys(overrides)) {
    orig[k] = process.env[k];
    if (overrides[k] === undefined) delete process.env[k];
    else process.env[k] = overrides[k];
  }
  try { return await fn(); }
  finally {
    for (const k of Object.keys(orig)) {
      if (orig[k] === undefined) delete process.env[k];
      else process.env[k] = orig[k];
    }
  }
}

describe('enforceHubScheme: the shared TLS-posture helper', () => {
  const { enforceHubScheme } = require('../src/gep/hubFetch');

  // withEnv is async (it must `return await fn()` so async callbacks see
  // the override across awaits — see helper comment). These tests below
  // call sync inner fns, but the test bodies still need to `await
  // withEnv(...)` — otherwise withEnv's finally restoration is scheduled
  // in a microtask that runs AFTER the it() body returns, so env vars
  // leak past the test boundary into whatever runs next. In the loop case
  // (last test) the cascade is worse: each iteration's `orig` snapshot
  // captures the previous iteration's still-unrestored override instead
  // of the true ambient, and the restores fire in scrambled order after
  // the loop ends. (Bugbot PR #160 Low.)

  it('refuses http:// when EVOMAP_HUB_ALLOW_INSECURE is unset', async () => {
    await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: undefined }, () => {
      assert.throws(
        () => enforceHubScheme('http://hub.example/api'),
        /must use https/i,
      );
    });
  });

  it('refuses non-URL input when EVOMAP_HUB_ALLOW_INSECURE is unset', async () => {
    await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: undefined }, () => {
      assert.throws(
        () => enforceHubScheme('::::not-a-url'),
        /not a valid URL/i,
      );
    });
  });

  it('accepts https://', async () => {
    await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: undefined }, () => {
      assert.doesNotThrow(() => enforceHubScheme('https://hub.example/api'));
    });
  });

  it('accepts http:// when EVOMAP_HUB_ALLOW_INSECURE=1', async () => {
    await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: '1' }, () => {
      assert.doesNotThrow(() => enforceHubScheme('http://localhost:8080/api'));
    });
  });

  it('treats EVOMAP_HUB_ALLOW_INSECURE values other than exactly "1" as absent', async () => {
    // Match hubFetch's own contract: only the literal "1" disables enforcement.
    // Each iteration awaits withEnv so the previous override is fully
    // restored before the next iteration's `orig` snapshot — otherwise
    // saves cascade and env pollution survives the test.
    for (const val of ['true', 'yes', '0', '', ' 1', '1 ']) {
      await withEnv({ EVOMAP_HUB_ALLOW_INSECURE: val }, () => {
        assert.throws(
          () => enforceHubScheme('http://hub.example/api'),
          /must use https/i,
          'EVOMAP_HUB_ALLOW_INSECURE=' + JSON.stringify(val) + ' must NOT bypass enforcement',
        );
      });
    }
  });
});

describe('atpExecute._postJson: TLS enforcement', () => {
  let _postJson;

  beforeEach(() => {
    // Force a fresh require so the module observes whatever env we set up.
    for (const k of Object.keys(require.cache)) {
      // Match both POSIX `/` and Windows `\` separators in require.cache keys.
      if (/[\\/]src[\\/]atp[\\/]atpExecute/.test(k) || /[\\/]src[\\/]gep[\\/]hubFetch/.test(k)) {
        delete require.cache[k];
      }
    }
    // _postJson is module-internal; reach it via the require evaluation.
    // It is intentionally not exported, so we rebuild it by re-requiring
    // and digging into the same fn the public completeAtpTask uses.
    // Simplest stable approach: re-export it by patching __get__ — but
    // atpExecute does not expose that. Instead, exercise enforcement by
    // calling completeAtpTask with a stubbed answer file and asserting
    // the `publish` stage surfaces the TLS error.
  });

  it('_publishBundle (via completeAtpTask) refuses http:// hub URL with no insecure bypass', async () => {
    await withEnv({
      A2A_HUB_URL: 'http://hub.example',
      EVOMAP_HUB_ALLOW_INSECURE: undefined,
      A2A_NODE_SECRET: 'a'.repeat(64),
      A2A_NODE_ID: 'node_aaa',
    }, async () => {
      for (const k of Object.keys(require.cache)) {
        if (/[\\/]src[\\/](atp|gep)[\\/]/.test(k)) {
          delete require.cache[k];
        }
      }
      // Stub a2aProtocol so completeAtpTask doesn't try to hit a real hub
      // for /hello. We just need _publishBundle to reach _postJson and
      // bounce off the TLS guard.
      const a2aPath = require.resolve('../src/gep/a2aProtocol');
      require.cache[a2aPath] = {
        id: a2aPath, filename: a2aPath, loaded: true,
        exports: {
          getNodeId: () => 'node_aaa',
          getHubUrl: () => 'http://hub.example',
          getHubNodeSecret: () => 'a'.repeat(64),
          buildHubHeaders: () => ({}),
          sendHelloToHub: async () => ({ ok: true }),
        },
      };

      const fs = require('fs');
      const os = require('os');
      const path = require('path');
      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'atp-tls-'));
      const answerFile = path.join(tmpDir, 'answer.txt');
      fs.writeFileSync(answerFile, 'minimal answer body');

      try {
        const { completeAtpTask } = require('../src/atp/atpExecute');
        const res = await completeAtpTask({
          taskId: 'task_1',
          orderId: 'order_1',
          answerFile,
          summary: 'test',
          capabilities: ['x'],
          signals: ['y'],
        });

        assert.equal(res.ok, false, 'must NOT publish over http://');
        assert.equal(res.stage, 'publish', 'must fail at the publish stage, not at hello');
        // Require TLS-specific signal. Pre-tighten the regex also accepted
        // `publish_failed`, which `_publishBundle` returns on ANY network
        // error — so a guard-bypassed run that simply failed because
        // hub.example does not exist would still satisfy the assertion
        // (false positive). Insist on the actual TLS refusal message.
        assert.match(String(res.error || ''), /tls_refused|must use https/i,
          'error must signal TLS refusal specifically — got ' + JSON.stringify(res.error));
      } finally {
        try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
      }
    });
  });
});

describe('strict TLS dispatcher / agent — defence against NODE_TLS_REJECT_UNAUTHORIZED=0', () => {
  // Cursor Security Reviewer #160 Medium: enforceHubScheme alone only
  // guards the URL scheme. If a caller built its own HTTP transport
  // and did not pin cert verification at the dispatcher / agent layer,
  // a globally-disabled NODE_TLS_REJECT_UNAUTHORIZED=0 could still
  // weaken the Hub channel. Mirror hubFetch by passing the strict
  // dispatcher / agent in secure mode, and skip it when the documented
  // EVOMAP_HUB_ALLOW_INSECURE=1 escape hatch is set.

  it('hubFetch exports strictHttpsAgent with rejectUnauthorized:true', () => {
    // Only `strictHttpsAgent` is exported now. The undici Agent stays
    // private to hubFetch — handing it out to fetch-based callers would
    // tempt them to pair it with `global.fetch`, which crashes with
    // UND_ERR_INVALID_ARG because global.fetch is the *internal* undici
    // copy (Bugbot PR #160 HIGH). Fetch-based callers route through
    // `hubFetch()` itself.
    const { strictHttpsAgent } = require('../src/gep/hubFetch');
    assert.ok(strictHttpsAgent, 'strictHttpsAgent must be exported');
    assert.equal(strictHttpsAgent.options && strictHttpsAgent.options.rejectUnauthorized, true,
      'strictHttpsAgent must pin rejectUnauthorized=true so NODE_TLS_REJECT_UNAUTHORIZED=0 cannot weaken');
  });

  it('atpExecute._postJson routes through hubFetch with strict dispatcher in secure mode', async () => {
    const hubFetchMod = require('../src/gep/hubFetch');
    let capturedOpts = null;
    hubFetchMod._setFetchImplForTest(async (_url, opts) => {
      capturedOpts = opts;
      return {
        ok: true,
        status: 200,
        text: async () => '{"payload":{"decision":"accept"}}',
        json: async () => ({ ok: true }),
      };
    });
    try {
      await withEnv({
        EVOMAP_HUB_ALLOW_INSECURE: undefined,
        EVOMAP_PROXY: undefined,
        A2A_TRANSPORT: undefined,
      }, async () => {
        for (const k of Object.keys(require.cache)) {
          if (/[\\/]src[\\/]atp[\\/]/.test(k) ||
              /[\\/]src[\\/]gep[\\/](?!hubFetch)/.test(k)) {
            delete require.cache[k];
          }
        }
        const a2aPath = require.resolve('../src/gep/a2aProtocol');
        require.cache[a2aPath] = {
          id: a2aPath, filename: a2aPath, loaded: true,
          exports: {
            getNodeId: () => 'node_aaa',
            getHubUrl: () => 'https://hub.example',
            getHubNodeSecret: () => 'a'.repeat(64),
            buildHubHeaders: () => ({}),
            sendHelloToHub: async () => ({ ok: true }),
          },
        };
        const settingsPath = require.resolve('../src/proxy/server/settings');
        require.cache[settingsPath] = {
          id: settingsPath, filename: settingsPath, loaded: true,
          exports: { getProxyUrl: () => null, getProxyToken: () => null },
        };
        const fs = require('fs');
        const os = require('os');
        const path = require('path');
        const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'atp-strict-'));
        const answerFile = path.join(tmpDir, 'answer.txt');
        fs.writeFileSync(answerFile, 'a');
        try {
          const { completeAtpTask } = require('../src/atp/atpExecute');
          await completeAtpTask({
            taskId: 't_1', orderId: 'o_1', answerFile, summary: 's',
            capabilities: ['x'], signals: ['y'],
          });
        } finally {
          try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
        }
      });

      assert.ok(capturedOpts, 'hubFetch must have invoked the (stubbed) undici fetch');
      assert.ok(capturedOpts.dispatcher, 'hubFetch must attach a dispatcher in secure mode');
      assert.equal(
        capturedOpts.dispatcher[Object.getOwnPropertySymbols(capturedOpts.dispatcher)
          .find((s) => s.toString() === 'Symbol(options)')]
          .connect.rejectUnauthorized,
        true,
        'dispatcher must pin connect.rejectUnauthorized=true',
      );
    } finally {
      hubFetchMod._setFetchImplForTest(null);
    }
  });

  it('atpExecute._postJson does NOT attach a dispatcher under EVOMAP_HUB_ALLOW_INSECURE=1', async () => {
    const hubFetchMod = require('../src/gep/hubFetch');
    let capturedOpts = null;
    hubFetchMod._setFetchImplForTest(async (_url, opts) => {
      capturedOpts = opts;
      return {
        ok: true,
        status: 200,
        text: async () => '{"payload":{"decision":"accept"}}',
        json: async () => ({ ok: true }),
      };
    });
    try {
      await withEnv({
        EVOMAP_HUB_ALLOW_INSECURE: '1',
        EVOMAP_PROXY: undefined,
        A2A_TRANSPORT: undefined,
      }, async () => {
        for (const k of Object.keys(require.cache)) {
          if (/[\\/]src[\\/]atp[\\/]/.test(k) ||
              /[\\/]src[\\/]gep[\\/](?!hubFetch)/.test(k)) {
            delete require.cache[k];
          }
        }
        const a2aPath = require.resolve('../src/gep/a2aProtocol');
        require.cache[a2aPath] = {
          id: a2aPath, filename: a2aPath, loaded: true,
          exports: {
            getNodeId: () => 'node_aaa',
            getHubUrl: () => 'https://hub.example',
            getHubNodeSecret: () => 'a'.repeat(64),
            buildHubHeaders: () => ({}),
            sendHelloToHub: async () => ({ ok: true }),
          },
        };
        const settingsPath = require.resolve('../src/proxy/server/settings');
        require.cache[settingsPath] = {
          id: settingsPath, filename: settingsPath, loaded: true,
          exports: { getProxyUrl: () => null, getProxyToken: () => null },
        };
        const fs = require('fs');
        const os = require('os');
        const path = require('path');
        const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'atp-strict-bypass-'));
        const answerFile = path.join(tmpDir, 'answer.txt');
        fs.writeFileSync(answerFile, 'a');
        try {
          const { completeAtpTask } = require('../src/atp/atpExecute');
          await completeAtpTask({
            taskId: 't_1', orderId: 'o_1', answerFile, summary: 's',
            capabilities: ['x'], signals: ['y'],
          });
        } finally {
          try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
        }
      });

      assert.ok(capturedOpts, 'fetch seam must have been called');
      assert.equal(capturedOpts.dispatcher, undefined,
        'under EVOMAP_HUB_ALLOW_INSECURE=1 hubFetch must NOT add the strict dispatcher');
    } finally {
      hubFetchMod._setFetchImplForTest(null);
    }
  });

  it('hubClient._hubPost routes through hubFetch with strict dispatcher in secure mode', async () => {
    // After PR #160 R3: hubClient no longer touches the global fetch
    // directly — it routes through hubFetch(), which itself uses
    // undici.fetch (same package as the strict Agent) and adds the
    // dispatcher. Stub via hubFetch's test seam so we observe what
    // hubFetch actually hands to undici.fetch.
    const hubFetchMod = require('../src/gep/hubFetch');
    let capturedOpts = null;
    hubFetchMod._setFetchImplForTest(async (_url, opts) => {
      capturedOpts = opts;
      return {
        ok: true, status: 200,
        json: async () => ({ ok: true }),
        text: async () => '',
      };
    });
    try {
      await withEnv({
        EVOMAP_HUB_ALLOW_INSECURE: undefined,
        EVOMAP_PROXY: undefined,
        A2A_TRANSPORT: undefined,
      }, async () => {
        for (const k of Object.keys(require.cache)) {
          // Do NOT clear hubFetch — we just installed a stub on it.
          if (/[\\/]src[\\/](atp[\\/]hubClient|gep[\\/]a2aProtocol|proxy[\\/]server[\\/]settings)\b/.test(k)) {
            delete require.cache[k];
          }
        }
        const a2aPath = require.resolve('../src/gep/a2aProtocol');
        require.cache[a2aPath] = {
          id: a2aPath, filename: a2aPath, loaded: true,
          exports: {
            getNodeId: () => 'node_test',
            getHubUrl: () => 'https://hub.example',
            buildHubHeaders: () => ({}),
          },
        };
        const settingsPath = require.resolve('../src/proxy/server/settings');
        require.cache[settingsPath] = {
          id: settingsPath, filename: settingsPath, loaded: true,
          exports: { getProxyUrl: () => null, getProxyToken: () => null },
        };
        const hubClient = require('../src/atp/hubClient');
        await hubClient.placeOrder({ capabilities: ['x'], budget: 1 });
      });

      assert.ok(capturedOpts, 'hubFetch must have invoked the (stubbed) undici fetch');
      assert.ok(capturedOpts.dispatcher,
        'hubFetch must attach a dispatcher in secure mode');
      // Verify the contract (rejectUnauthorized=true) without an
      // identity check — cache resets across describes hand out fresh
      // Agent instances.
      const opts = capturedOpts.dispatcher[Object.getOwnPropertySymbols(capturedOpts.dispatcher)
        .find((s) => s.toString() === 'Symbol(options)')];
      assert.equal(opts && opts.connect && opts.connect.rejectUnauthorized, true,
        'dispatcher must pin connect.rejectUnauthorized=true. opts=' + JSON.stringify(opts));
    } finally {
      hubFetchMod._setFetchImplForTest(null);
    }
  });

  it('hubClient._hubPost does NOT attach a dispatcher under EVOMAP_HUB_ALLOW_INSECURE=1', async () => {
    // In insecure mode hubFetch uses the platform global.fetch (or the
    // test seam if installed) and does NOT add a dispatcher, so the
    // documented EVOMAP_HUB_ALLOW_INSECURE=1 escape hatch keeps local
    // mock hubs that rely on NODE_TLS_REJECT_UNAUTHORIZED=0 working.
    const hubFetchMod = require('../src/gep/hubFetch');
    let capturedOpts = null;
    hubFetchMod._setFetchImplForTest(async (_url, opts) => {
      capturedOpts = opts;
      return {
        ok: true, status: 200,
        json: async () => ({ ok: true }),
        text: async () => '',
      };
    });
    try {
      await withEnv({
        EVOMAP_HUB_ALLOW_INSECURE: '1',
        EVOMAP_PROXY: undefined,
        A2A_TRANSPORT: undefined,
      }, async () => {
        for (const k of Object.keys(require.cache)) {
          if (/[\\/]src[\\/](atp[\\/]hubClient|gep[\\/]a2aProtocol|proxy[\\/]server[\\/]settings)\b/.test(k)) {
            delete require.cache[k];
          }
        }
        const a2aPath = require.resolve('../src/gep/a2aProtocol');
        require.cache[a2aPath] = {
          id: a2aPath, filename: a2aPath, loaded: true,
          exports: {
            getNodeId: () => 'node_test',
            getHubUrl: () => 'http://localhost:8080',
            buildHubHeaders: () => ({}),
          },
        };
        const settingsPath = require.resolve('../src/proxy/server/settings');
        require.cache[settingsPath] = {
          id: settingsPath, filename: settingsPath, loaded: true,
          exports: { getProxyUrl: () => null, getProxyToken: () => null },
        };
        const hubClient = require('../src/atp/hubClient');
        await hubClient.placeOrder({ capabilities: ['x'], budget: 1 });
      });

      assert.ok(capturedOpts, 'fetch seam must have been called');
      assert.equal(capturedOpts.dispatcher, undefined,
        'under EVOMAP_HUB_ALLOW_INSECURE=1 hubFetch must NOT add the strict dispatcher');
    } finally {
      hubFetchMod._setFetchImplForTest(null);
    }
  });
});

describe('hubClient._hubPost / _hubGet: TLS enforcement', () => {
  // hubClient now routes through hubFetch (PR #160 R3 — dispatcher mixing
  // would otherwise crash with UND_ERR_INVALID_ARG, see hubFetch.js
  // header comment). Stub via hubFetch's `_setFetchImplForTest` seam
  // rather than `global.fetch`; the latter is no longer on the code
  // path the production calls take, so any test that stubbed it would
  // either bypass the strict transport contract or accidentally let a
  // real DNS request through.
  let hubFetchMod;

  beforeEach(() => {
    hubFetchMod = require('../src/gep/hubFetch');
    // Default seam: refuse to be called. Tests that expect the post-
    // guard fetch path override this with a success stub.
    hubFetchMod._setFetchImplForTest(async () => {
      throw new Error('hubFetch fetch seam must NOT be reached — the URL-scheme guard must short-circuit');
    });
  });

  afterEach(() => {
    if (hubFetchMod) hubFetchMod._setFetchImplForTest(null);
  });

  function freshHubClient(hubUrl) {
    // Do NOT clear hubFetch from the cache — its module-level seam
    // (`_setFetchImplForTest`) is what these tests rely on. Clearing
    // would tear out the stub installed in beforeEach.
    const pat = /[\\/]src[\\/](atp[\\/]hubClient|gep[\\/]a2aProtocol|proxy[\\/]server[\\/]settings)\b/;
    for (const k of Object.keys(require.cache)) {
      if (pat.test(k)) delete require.cache[k];
    }
    const a2aPath = require.resolve('../src/gep/a2aProtocol');
    require.cache[a2aPath] = {
      id: a2aPath, filename: a2aPath, loaded: true,
      exports: {
        getNodeId: () => 'node_test',
        getHubUrl: () => hubUrl,
        buildHubHeaders: () => ({ 'Authorization': 'Bearer SECRET_VALUE' }),
      },
    };
    const settingsPath = require.resolve('../src/proxy/server/settings');
    require.cache[settingsPath] = {
      id: settingsPath, filename: settingsPath, loaded: true,
      exports: {
        getProxyUrl: () => null,    // force direct hub path, skip _proxyRequest
        getProxyToken: () => null,
      },
    };
    return require('../src/atp/hubClient');
  }

  it('placeOrder refuses to POST to http:// hub when EVOMAP_HUB_ALLOW_INSECURE unset', async () => {
    await withEnv({
      EVOMAP_HUB_ALLOW_INSECURE: undefined,
      EVOMAP_PROXY: undefined,
      A2A_TRANSPORT: undefined,
    }, async () => {
      const hubClient = freshHubClient('http://hub.example');
      const res = await hubClient.placeOrder({
        capabilities: ['x'],
        budget: 10,
      });
      assert.equal(res.ok, false);
      assert.match(String(res.error || ''), /tls_refused|must use https/i,
        'POST must refuse http:// — got ' + JSON.stringify(res.error));
    });
  });

  it('listProofs refuses to GET from http:// hub when EVOMAP_HUB_ALLOW_INSECURE unset', async () => {
    await withEnv({
      EVOMAP_HUB_ALLOW_INSECURE: undefined,
      EVOMAP_PROXY: undefined,
      A2A_TRANSPORT: undefined,
    }, async () => {
      const hubClient = freshHubClient('http://hub.example');
      const res = await hubClient.listProofs({ role: 'consumer', limit: 5 });
      assert.equal(res.ok, false);
      assert.match(String(res.error || ''), /tls_refused|must use https/i,
        'GET must refuse http:// — got ' + JSON.stringify(res.error));
    });
  });

  it('https:// hub URL passes the guard (fetch seam is reached)', async () => {
    await withEnv({
      EVOMAP_HUB_ALLOW_INSECURE: undefined,
      EVOMAP_PROXY: undefined,
      A2A_TRANSPORT: undefined,
    }, async () => {
      // Override the default throw stub with success so we can observe
      // that the post-guard fetch path runs.
      let fetchCalled = 0;
      hubFetchMod._setFetchImplForTest(async () => {
        fetchCalled++;
        return {
          ok: true, status: 200,
          json: async () => ({ ok: true }),
          text: async () => '',
        };
      });
      const hubClient = freshHubClient('https://hub.example');
      const res = await hubClient.placeOrder({ capabilities: ['x'], budget: 1 });
      assert.equal(res.ok, true, 'https URL must pass the guard');
      assert.equal(fetchCalled, 1, 'undici fetch seam must be called exactly once');
    });
  });

  it('EVOMAP_HUB_ALLOW_INSECURE=1 lets http:// through to fetch', async () => {
    await withEnv({
      EVOMAP_HUB_ALLOW_INSECURE: '1',
      EVOMAP_PROXY: undefined,
      A2A_TRANSPORT: undefined,
    }, async () => {
      let fetchCalled = 0;
      hubFetchMod._setFetchImplForTest(async () => {
        fetchCalled++;
        return {
          ok: true, status: 200,
          json: async () => ({ ok: true }),
          text: async () => '',
        };
      });
      const hubClient = freshHubClient('http://localhost:8080');
      const res = await hubClient.placeOrder({ capabilities: ['x'], budget: 1 });
      assert.equal(res.ok, true);
      assert.equal(fetchCalled, 1, 'insecure bypass must allow http through to fetch');
    });
  });
});
