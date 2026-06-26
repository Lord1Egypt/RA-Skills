const { describe, test, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

const SERVICE_BASE_URL = 'http://127.0.0.1:3105';
const INTERNAL_TOKEN = 'internal-token-for-mcp-test';
const REQUEST_TIMEOUT_MS = 2000;

const ENV_KEYS = [
  'XIAOICE_VIDEO_SERVICE_BASE_URL',
  'VIDEO_SERVICE_BASE_URL',
  'VIDEO_SERVICE_INTERNAL_TOKEN',
  'XIAOICE_VIDEO_INTERNAL_TOKEN',
  'VIDEO_SERVICE_REQUEST_TIMEOUT_MS',
];

function createFetchStub() {
  const queue = [];
  const calls = [];

  async function fetchStub(input, init = {}) {
    calls.push({ input, init });

    if (queue.length === 0) {
      throw new Error('Unexpected fetch call: no mock response queued');
    }

    const next = queue.shift();
    if (next instanceof Error) {
      throw next;
    }

    const status = next.status ?? 200;
    return {
      ok: next.ok ?? (status >= 200 && status < 300),
      status,
      statusText: next.statusText || '',
      async json() {
        if (next.jsonError) {
          throw next.jsonError;
        }
        return next.body ?? {};
      },
      async text() {
        return next.text ?? JSON.stringify(next.body ?? {});
      },
    };
  }

  fetchStub.calls = calls;
  fetchStub.queueResponse = (response) => {
    queue.push(response);
  };

  return fetchStub;
}

function getRequestUrl(call) {
  const input = call?.input;
  if (typeof input === 'string') {
    return input;
  }
  if (input && typeof input.url === 'string') {
    return input.url;
  }
  return String(input || '');
}

function getRequestMethod(call) {
  const explicitMethod = call?.init?.method;
  if (explicitMethod) {
    return String(explicitMethod).toUpperCase();
  }

  const inputMethod = call?.input?.method;
  if (inputMethod) {
    return String(inputMethod).toUpperCase();
  }

  return 'GET';
}

function getHeaderValue(headers, name) {
  if (!headers) {
    return '';
  }

  if (typeof headers.get === 'function') {
    const value = headers.get(name);
    return value == null ? '' : String(value);
  }

  for (const [key, value] of Object.entries(headers)) {
    if (String(key).toLowerCase() === String(name).toLowerCase()) {
      return value == null ? '' : String(value);
    }
  }
  return '';
}

async function getRequestBodyJson(call) {
  if (typeof call?.init?.body === 'string' && call.init.body) {
    return JSON.parse(call.init.body);
  }

  if (call?.input && typeof call.input.text === 'function') {
    const text = await call.input.text();
    if (text) {
      return JSON.parse(text);
    }
  }

  return null;
}

function assertErrorResult(result) {
  assert.equal(
    result?.isError,
    true,
    `Expected tool result to set isError=true, got: ${JSON.stringify(result)}`
  );
}

function assertSuccessResult(result) {
  assert.equal(
    result?.isError,
    false,
    `Expected tool result to set isError=false, got: ${JSON.stringify(result)}`
  );
}

function tryCreateTool(factory, runtimeConfig) {
  const attempts = [[runtimeConfig], []];
  for (const args of attempts) {
    try {
      const candidate = factory(...args);
      if (candidate && typeof candidate.execute === 'function') {
        return candidate;
      }
    } catch (error) {
      void error;
    }
  }
  return null;
}

function wrapDirectExecutor(execute, runtimeConfig) {
  return async (params) => {
    if (execute.length >= 2) {
      return execute(params, runtimeConfig);
    }
    return execute(params);
  };
}

function wrapToolExecute(execute, runtimeConfig) {
  return async (params) => {
    if (execute.length >= 3) {
      return execute('test-call-id', params, runtimeConfig);
    }
    if (execute.length >= 2) {
      return execute('test-call-id', params);
    }
    return execute(params);
  };
}

function loadToolExecutor() {
  let modulePath = '';
  try {
    modulePath = require.resolve('../src/mcp/tool');
  } catch (error) {
    throw new Error(
      'Missing src/mcp/tool.js. Expected a reusable MCP tool module exporting xiaoice_video_produce execute logic.'
    );
  }

  delete require.cache[modulePath];
  const mod = require(modulePath);
  const runtimeConfig = {
    serviceBaseUrl: SERVICE_BASE_URL,
    internalToken: INTERNAL_TOKEN,
    requestTimeoutMs: REQUEST_TIMEOUT_MS,
  };

  const directExportNames = [
    'executeXiaoiceVideoProduce',
    'executeVideoProduce',
    'handleXiaoiceVideoProduce',
    'runXiaoiceVideoProduce',
  ];

  for (const key of directExportNames) {
    if (typeof mod?.[key] === 'function') {
      return wrapDirectExecutor(mod[key], runtimeConfig);
    }
  }

  const factoryExportNames = [
    'createXiaoiceVideoProduceTool',
    'createVideoProduceTool',
    'createMcpTool',
    'createTool',
    'buildXiaoiceVideoProduceTool',
  ];

  for (const key of factoryExportNames) {
    if (typeof mod?.[key] === 'function') {
      const tool = tryCreateTool(mod[key], runtimeConfig);
      if (tool) {
        return wrapToolExecute(tool.execute.bind(tool), runtimeConfig);
      }
    }
  }

  if (mod?.tool && typeof mod.tool.execute === 'function') {
    return wrapToolExecute(mod.tool.execute.bind(mod.tool), runtimeConfig);
  }

  if (mod?.xiaoiceVideoProduceTool && typeof mod.xiaoiceVideoProduceTool.execute === 'function') {
    return wrapToolExecute(mod.xiaoiceVideoProduceTool.execute.bind(mod.xiaoiceVideoProduceTool), runtimeConfig);
  }

  if (typeof mod?.execute === 'function') {
    return wrapToolExecute(mod.execute, runtimeConfig);
  }

  if (typeof mod === 'function') {
    const tool = tryCreateTool(mod, runtimeConfig);
    if (tool) {
      return wrapToolExecute(tool.execute.bind(tool), runtimeConfig);
    }
    return wrapDirectExecutor(mod, runtimeConfig);
  }

  if (typeof mod?.default === 'function') {
    const tool = tryCreateTool(mod.default, runtimeConfig);
    if (tool) {
      return wrapToolExecute(tool.execute.bind(tool), runtimeConfig);
    }
    return wrapDirectExecutor(mod.default, runtimeConfig);
  }

  throw new Error(
    'Cannot resolve xiaoice_video_produce execute function from src/mcp/tool.js exports.'
  );
}

describe('xiaoice_video_produce reusable executor', { concurrency: 1 }, () => {
  let fetchStub;
  let originalFetch;
  const previousEnv = {};

  beforeEach(() => {
    originalFetch = global.fetch;
    fetchStub = createFetchStub();
    global.fetch = fetchStub;

    for (const key of ENV_KEYS) {
      previousEnv[key] = process.env[key];
    }
    process.env.XIAOICE_VIDEO_SERVICE_BASE_URL = SERVICE_BASE_URL;
    process.env.VIDEO_SERVICE_BASE_URL = SERVICE_BASE_URL;
    process.env.VIDEO_SERVICE_INTERNAL_TOKEN = INTERNAL_TOKEN;
    process.env.XIAOICE_VIDEO_INTERNAL_TOKEN = INTERNAL_TOKEN;
    process.env.VIDEO_SERVICE_REQUEST_TIMEOUT_MS = String(REQUEST_TIMEOUT_MS);
  });

  afterEach(() => {
    global.fetch = originalFetch;
    for (const key of ENV_KEYS) {
      if (previousEnv[key] == null) {
        delete process.env[key];
      } else {
        process.env[key] = previousEnv[key];
      }
    }
  });

  test('validates create parameters (topic + vhBizId required)', async () => {
    const execute = loadToolExecutor();

    const result = await execute({ action: 'create' });
    assertErrorResult(result);
    assert.equal(fetchStub.calls.length, 0);
  });

  test('validates get parameters (taskId required)', async () => {
    const execute = loadToolExecutor();

    const result = await execute({ action: 'get' });
    assertErrorResult(result);
    assert.equal(fetchStub.calls.length, 0);
  });

  test('maps create to POST /v1/tasks with internal token', async () => {
    fetchStub.queueResponse({
      status: 202,
      body: {
        data: {
          taskId: 'task-create-001',
          status: 'submitted',
        },
      },
    });

    const execute = loadToolExecutor();
    const result = await execute({
      action: 'create',
      topic: 'Generate a launch video',
      sessionId: 'session-create-001',
      traceId: 'trace-create-001',
      vhBizId: 'biz-create-001',
      title: 'Launch video',
      materialList: [],
      aigcWatermark: true,
    });

    assertSuccessResult(result);
    assert.equal(fetchStub.calls.length, 1);

    const call = fetchStub.calls[0];
    assert.equal(getRequestUrl(call), `${SERVICE_BASE_URL}/v1/tasks`);
    assert.equal(getRequestMethod(call), 'POST');

    const headers = call.init?.headers || call.input?.headers;
    assert.equal(getHeaderValue(headers, 'X-Internal-Token'), INTERNAL_TOKEN);

    const body = await getRequestBodyJson(call);
    assert.equal(body?.topic, 'Generate a launch video');
    assert.equal(body?.sessionId, 'session-create-001');
    assert.equal(body?.traceId, 'trace-create-001');
    assert.equal(body?.vhBizId, 'biz-create-001');
    assert.equal(body?.title, 'Launch video');
    assert.deepEqual(body?.materialList, []);
    assert.equal(body?.aigcWatermark, true);
  });

  test('rejects legacy vhbizmode argument with validation error', async () => {
    const execute = loadToolExecutor();

    const result = await execute({
      action: 'create',
      topic: 'Generate legacy input rejection test video',
      vhBizId: 'biz-legacy',
      vhbizmode: 'legacy-biz',
    });

    assertErrorResult(result);
    assert.equal(fetchStub.calls.length, 0);
  });

  test('maps get to GET /v1/tasks/:taskId with internal token', async () => {
    fetchStub.queueResponse({
      status: 200,
      body: {
        data: {
          taskId: 'task-get-001',
          status: 'processing',
        },
      },
    });

    const execute = loadToolExecutor();
    const result = await execute({
      action: 'get',
      taskId: 'task-get-001',
    });

    assertSuccessResult(result);
    assert.equal(fetchStub.calls.length, 1);

    const call = fetchStub.calls[0];
    assert.equal(getRequestUrl(call), `${SERVICE_BASE_URL}/v1/tasks/task-get-001`);
    assert.equal(getRequestMethod(call), 'GET');

    const headers = call.init?.headers || call.input?.headers;
    assert.equal(getHeaderValue(headers, 'X-Internal-Token'), INTERNAL_TOKEN);
  });

  test('maps upstream 4xx HTTP response to isError=true', async () => {
    fetchStub.queueResponse({
      status: 422,
      ok: false,
      body: {
        error: {
          code: 'VALIDATION_FAILED',
          message: 'invalid topic',
        },
      },
    });

    const execute = loadToolExecutor();
    const result = await execute({
      action: 'create',
      topic: 'Generate a 4xx mapping test video',
      vhBizId: 'biz-4xx',
    });

    assertErrorResult(result);
  });

  test('maps upstream 5xx HTTP response to isError=true', async () => {
    fetchStub.queueResponse({
      status: 503,
      ok: false,
      body: {
        error: {
          code: 'UPSTREAM_DOWN',
          message: 'provider unavailable',
        },
      },
    });

    const execute = loadToolExecutor();
    const result = await execute({
      action: 'get',
      taskId: 'task-upstream-5xx',
    });

    assertErrorResult(result);
  });

  test('maps network errors to isError=true', async () => {
    fetchStub.queueResponse(new Error('ECONNREFUSED'));

    const execute = loadToolExecutor();
    const result = await execute({
      action: 'create',
      topic: 'Generate a network-error mapping test video',
      vhBizId: 'biz-network',
    });

    assertErrorResult(result);
  });
});
