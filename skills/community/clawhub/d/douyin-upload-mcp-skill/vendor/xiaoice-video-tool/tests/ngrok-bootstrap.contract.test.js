const { describe, test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  REPO_ROOT,
  loadScriptModule,
  pickFunction,
  invokeFirst,
  invokeFirstAsync,
  createFetchStub,
  parseFetchJsonBody,
  getRequestUrl,
  getRequestMethod,
  getHeaderValue,
  loadJsonFixture,
  runNodeScript,
  collectStringLeaves,
  extractPublicUrl,
} = require('./helpers/ngrok-bootstrap');

const RUNTIME_FILES = [
  'video-service.pid',
  'video-service.log',
  'ngrok.pid',
  'ngrok-url.txt',
  'ngrok.log',
  'bootstrap.last.json',
];

function assertNonZeroAndActionable(result, pattern, context) {
  assert.notEqual(
    result.status,
    0,
    `${context} should exit non-zero. stdout=${result.stdout || ''} stderr=${result.stderr || ''}`
  );
  assert.match(result.output, pattern, `${context} should print actionable error details.`);
}

function loadFirstAvailableModule(relativePaths) {
  const errors = [];
  for (const relativePath of relativePaths) {
    try {
      return loadScriptModule(relativePath);
    } catch (error) {
      errors.push(error?.message || String(error));
    }
  }
  throw new Error(errors.join(' | '));
}

describe('ngrok bootstrap contracts from docs/08', { concurrency: 1 }, () => {
  test('relative state dir resolves against repo root and runtime paths are generated', () => {
    const devUtils = loadScriptModule('scripts/dev-utils.js');
    const createContext = pickFunction(devUtils, ['createContext'], 'dev context builder');

    const relativeStateDir = 'tmp/contracts-ngrok-state';
    const context = createContext({
      env: {
        ...process.env,
        XIAOICE_VIDEO_STATE_DIR: relativeStateDir,
      },
    });
    const resolvedStateDir = context.stateDir;

    assert.equal(
      path.normalize(resolvedStateDir),
      path.join(REPO_ROOT, relativeStateDir),
      'relative XIAOICE_VIDEO_STATE_DIR must resolve against repository root'
    );

    const runtimeDir = path.join(resolvedStateDir, 'runtime');
    const allPathValues = new Set(collectStringLeaves(context.paths));
    assert.ok(
      allPathValues.has(path.normalize(runtimeDir)),
      'runtime path map should include `${stateDir}/runtime`'
    );

    for (const fileName of RUNTIME_FILES) {
      const expected = path.normalize(path.join(runtimeDir, fileName));
      assert.ok(
        allPathValues.has(expected),
        `runtime path map should include ${fileName} under ${runtimeDir}`
      );
    }
  });

  test('ngrok tunnel selection picks HTTPS and prefers exact target-port entries', () => {
    const ngrokModule = loadFirstAvailableModule(['scripts/dev-utils.js', 'scripts/dev-ngrok.js']);
    const selectTunnel = pickFunction(
      ngrokModule,
      [
        'getNgrokTunnelInfo',
        'pickBestNgrokTunnel',
        'selectTargetHttpsTunnel',
        'selectHttpsTunnelUrl',
        'pickHttpsTunnelForPort',
        'resolveNgrokPublicUrl',
      ],
      'ngrok tunnel selector'
    );

    const fixture = loadJsonFixture('ngrok-tunnels.multi.json');
    const selected = invokeFirst(
      [
        () => selectTunnel({ tunnels: fixture.tunnels, targetPort: 3105 }),
        () => selectTunnel({ tunnels: fixture.tunnels, port: 3105 }),
        () => selectTunnel(fixture.tunnels, 3105),
        () => selectTunnel(fixture, 3105),
      ],
      'selectTargetHttpsTunnel'
    );

    const selectedUrl = extractPublicUrl(selected);
    assert.equal(selectedUrl, 'https://exact-first.ngrok-free.app');
    assert.match(selectedUrl, /^https:\/\//, 'selected ngrok URL must be HTTPS');
  });

  test('callback sync sends PUT /v1/admin/config with X-Admin-Token and minimal JSON body', async () => {
    const callbackSyncModule = loadScriptModule('scripts/dev-callback-sync.js');
    const syncCallback = pickFunction(
      callbackSyncModule,
      ['runDevCallbackSync', 'runCallbackSync', 'syncCallbackPublicBaseUrl', 'syncCallbackConfig'],
      'callback sync function'
    );

    const fetchStub = createFetchStub();
    fetchStub.queueResponse({
      status: 200,
      body: { data: { callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app' } },
    });

    const originalFetch = global.fetch;
    global.fetch = fetchStub;
    try {
      const context = {
        stateDir: path.join(REPO_ROOT, 'tmp/contracts-dev-callback-sync'),
        service: {
          baseUrl: 'http://127.0.0.1:3105',
          healthUrl: 'http://127.0.0.1:3105/health',
        },
        ngrok: {
          enabled: true,
        },
        paths: {
          ngrokUrlFile: path.join(REPO_ROOT, 'tmp/contracts-dev-callback-sync/runtime/ngrok-url.txt'),
        },
        tokens: {
          admin: 'admin-token-test',
        },
      };

      await invokeFirstAsync(
        [
          () =>
            syncCallback({
              context,
              callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app',
            }),
          () =>
            syncCallback({
              serviceBaseUrl: 'http://127.0.0.1:3105',
              callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app',
              adminToken: 'admin-token-test',
              fetch: fetchStub,
            }),
          () =>
            syncCallback({
              baseUrl: 'http://127.0.0.1:3105',
              callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app',
              adminToken: 'admin-token-test',
              fetch: fetchStub,
            }),
          () =>
            syncCallback(
              'http://127.0.0.1:3105',
              'https://exact-first.ngrok-free.app',
              'admin-token-test',
              fetchStub
            ),
          () =>
            syncCallback({
              serviceBaseUrl: 'http://127.0.0.1:3105',
              callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app',
              adminToken: 'admin-token-test',
            }),
        ],
        'syncCallbackPublicBaseUrl'
      );
    } finally {
      global.fetch = originalFetch;
    }

    assert.equal(fetchStub.calls.length, 1);
    const call = fetchStub.calls[0];
    assert.equal(getRequestUrl(call), 'http://127.0.0.1:3105/v1/admin/config');
    assert.equal(getRequestMethod(call), 'PUT');
    assert.equal(getHeaderValue(call.init.headers, 'X-Admin-Token'), 'admin-token-test');
    assert.deepEqual(parseFetchJsonBody(call), {
      callbackPublicBaseUrl: 'https://exact-first.ngrok-free.app',
    });
  });

  test('dev:up fails with actionable errors when admin/callback token is missing', () => {
    const scenarios = [
      {
        label: 'missing admin token',
        env: {
          VIDEO_SERVICE_ADMIN_TOKEN: '',
          VIDEO_SERVICE_CALLBACK_TOKEN: 'callback-token-test',
        },
        pattern: /(VIDEO_SERVICE_ADMIN_TOKEN|E_MISSING_ADMIN_TOKEN|admin token)/i,
      },
      {
        label: 'missing callback token',
        env: {
          VIDEO_SERVICE_ADMIN_TOKEN: 'admin-token-test',
          VIDEO_SERVICE_CALLBACK_TOKEN: '',
        },
        pattern: /(VIDEO_SERVICE_CALLBACK_TOKEN|E_MISSING_CALLBACK_TOKEN|callback token)/i,
      },
    ];

    for (const scenario of scenarios) {
      const result = runNodeScript('scripts/dev-up.js', {
        timeoutMs: 5000,
        env: {
          NODE_ENV: 'test',
          VIDEO_USE_NGROK: 'true',
          VIDEO_TASK_SERVICE_HOST: '127.0.0.1',
          VIDEO_TASK_SERVICE_PORT: '3105',
          VIDEO_SERVICE_INTERNAL_TOKEN: 'internal-token-test',
          XIAOICE_VIDEO_STATE_DIR: 'tmp/contracts-dev-up',
          ...scenario.env,
        },
      });

      assertNonZeroAndActionable(result, scenario.pattern, `dev:up ${scenario.label}`);
    }
  });

  test('dev:up fails with actionable error when ngrok startup fails', () => {
    const result = runNodeScript('scripts/dev-up.js', {
      timeoutMs: 5000,
      env: {
        NODE_ENV: 'test',
        VIDEO_USE_NGROK: 'true',
        VIDEO_TASK_SERVICE_HOST: '127.0.0.1',
        VIDEO_TASK_SERVICE_PORT: '3105',
        VIDEO_SERVICE_INTERNAL_TOKEN: 'internal-token-test',
        VIDEO_SERVICE_ADMIN_TOKEN: 'admin-token-test',
        VIDEO_SERVICE_CALLBACK_TOKEN: 'callback-token-test',
        NGROK_BIN: '__missing_ngrok_binary__',
        XIAOICE_VIDEO_STATE_DIR: 'tmp/contracts-dev-up',
      },
    });

    assertNonZeroAndActionable(
      result,
      /(E_NGROK_START_FAILED|ngrok|NGROK_BIN|add-authtoken|failed to start)/i,
      'dev:up ngrok startup failure'
    );
  });

  test('dev:doctor fails when callbackPublicBaseUrl does not match ngrok URL', async () => {
    const doctorModule = loadScriptModule('scripts/dev-doctor.js');
    const runDevDoctor = pickFunction(doctorModule, ['runDevDoctor'], 'dev:doctor runner');
    const ngrokFixture = loadJsonFixture('ngrok-tunnels.single.json');

    const fetchCalls = [];
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ngrok-doctor-contract-'));
    const runtimeConfigFile = path.join(tempDir, 'runtime-config.json');
    fs.writeFileSync(
      runtimeConfigFile,
      `${JSON.stringify({ callbackPublicBaseUrl: 'https://stale-public.ngrok-free.app' }, null, 2)}\n`,
      'utf8'
    );

    const context = {
      stateDir: tempDir,
      service: {
        port: 3105,
        healthUrl: 'http://127.0.0.1:3105/health',
      },
      ngrok: {
        enabled: true,
        apiUrl: 'http://127.0.0.1:4040',
      },
      callbackPublicBaseUrlFromEnv: '',
      paths: {
        runtimeConfigFile,
        serviceLogFile: path.join(tempDir, 'video-service.log'),
        ngrokLogFile: path.join(tempDir, 'ngrok.log'),
      },
    };

    const fetchStub = async (input, init = {}) => {
      const url = typeof input === 'string' ? input : input?.url || '';
      fetchCalls.push({ input, init, url });

      if (url.endsWith('/api/tunnels')) {
        return {
          ok: true,
          status: 200,
          async json() {
            return ngrokFixture;
          },
        };
      }
      if (url.endsWith('/health')) {
        return {
          ok: true,
          status: 200,
          async json() {
            return { status: 'ok' };
          },
        };
      }
      if (url.endsWith('/v1/admin/config')) {
        return {
          ok: true,
          status: 200,
          async json() {
            return { data: { callbackPublicBaseUrl: 'https://stale-public.ngrok-free.app' } };
          },
        };
      }

      return {
        ok: false,
        status: 404,
        async json() {
          return { error: { code: 'not_found', message: url } };
        },
      };
    };

    const originalFetch = global.fetch;
    const originalConsoleError = console.error;
    const errorLines = [];
    global.fetch = fetchStub;
    console.error = (...args) => {
      errorLines.push(args.map((item) => String(item)).join(' '));
    };
    try {
      await assert.rejects(() => runDevDoctor({ context }), /doctor found/i);
      assert.ok(
        errorLines.some((line) => /callbackPublicBaseUrl mismatch/i.test(line)),
        'dev:doctor should report callbackPublicBaseUrl mismatch'
      );
      assert.ok(fetchCalls.length >= 3, 'dev:doctor should check health, ngrok tunnels, and callback endpoint');
    } finally {
      global.fetch = originalFetch;
      console.error = originalConsoleError;
    }
  });
});
