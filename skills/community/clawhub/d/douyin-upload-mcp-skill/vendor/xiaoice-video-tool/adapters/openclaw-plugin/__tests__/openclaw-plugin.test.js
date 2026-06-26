const path = require('path');
const Module = require('node:module');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { describe, test } = require('node:test');

const PLUGIN_PATH = path.resolve(__dirname, '../index.js');
const MANIFEST_PATH = path.resolve(__dirname, '../openclaw.plugin.json');
const SKILL_PATH = path.resolve(__dirname, '../skills/xiaoice-video/SKILL.md');
const CLIENT_PATH = path.resolve(__dirname, '../lib/video-service-client.js');

function loadRegisterWithClientStub(sharedClientStub) {
  const originalLoad = Module._load;

  Module._load = function patchedLoad(request, parent, isMain) {
    const fromPlugin = parent && path.resolve(parent.filename) === PLUGIN_PATH;
    if (fromPlugin && request === './lib/video-service-client') {
      return sharedClientStub;
    }
    return originalLoad.call(this, request, parent, isMain);
  };

  delete require.cache[PLUGIN_PATH];

  try {
    const mod = require(PLUGIN_PATH);
    return mod.default || mod.register || mod;
  } finally {
    Module._load = originalLoad;
  }
}

function createMockApi(configOverrides = {}) {
  const tools = [];
  const config = {
    serviceBaseUrl: 'http://127.0.0.1:3105',
    internalToken: 'video-internal-token',
    requestTimeoutMs: 3200,
    ...configOverrides,
  };

  return {
    config: {
      plugins: {
        entries: {
          'one-click-video': {
            config,
          },
        },
      },
    },
    logger: {
      info() {},
      warn() {},
      error() {},
    },
    registerTool(tool) {
      tools.push(tool);
    },
    getRegisteredTools() {
      return tools.slice();
    },
  };
}

function getSingleRegisteredTool(api) {
  const tools = api.getRegisteredTools();
  assert.equal(tools.length, 1, `Expected exactly one registered tool, got ${tools.length}`);
  return tools[0];
}

function parseResultText(result) {
  const text = result?.content?.[0]?.text;
  assert.equal(typeof text, 'string', `Expected text response, got: ${JSON.stringify(result)}`);
  return text;
}

function parseResultJson(result) {
  return JSON.parse(parseResultText(result));
}

describe('openclaw one-click-video plugin', { concurrency: 1 }, () => {
  test('manifest exposes bundled skills and skill file exists', () => {
    const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));

    assert.deepEqual(manifest.skills, ['./skills']);
    assert.equal(fs.existsSync(SKILL_PATH), true);
    assert.equal(fs.existsSync(CLIENT_PATH), true);
  });

  test('register exactly one tool named xiaoice_video_produce', () => {
    const register = loadRegisterWithClientStub({
      async createTask() {
        return {};
      },
      async getTask() {
        return {};
      },
    });

    const api = createMockApi();
    register(api);

    const tool = getSingleRegisteredTool(api);
    assert.equal(tool.name, 'xiaoice_video_produce');
    assert.equal(typeof tool.execute, 'function');
  });

  test('create/get mapping uses shared client and plugin config path', async () => {
    const createCalls = [];
    const getCalls = [];

    const register = loadRegisterWithClientStub({
      async createTask(params, config) {
        createCalls.push({ params, config });
        return {
          taskId: 'task-create-001',
          status: 'submitted',
        };
      },
      async getTask(taskId, config) {
        getCalls.push({ taskId, config });
        return {
          taskId,
          status: 'processing',
        };
      },
    });

    const api = createMockApi();
    register(api);
    const tool = getSingleRegisteredTool(api);

    const createResult = await tool.execute('call-create', {
      action: 'create',
      topic: 'Generate product launch video',
      sessionId: 'session-1',
      traceId: 'trace-1',
      vhBizId: 'biz-demo',
      title: 'Launch clip',
      materialList: [],
    });

    assert.equal(createResult.isError, false);
    assert.equal(createCalls.length, 1);
    assert.deepEqual(createCalls[0], {
      params: {
        topic: 'Generate product launch video',
        sessionId: 'session-1',
        traceId: 'trace-1',
        vhBizId: 'biz-demo',
        title: 'Launch clip',
        materialList: [],
      },
      config: {
        serviceBaseUrl: 'http://127.0.0.1:3105',
        internalToken: 'video-internal-token',
        requestTimeoutMs: 3200,
      },
    });

    const createPayload = parseResultJson(createResult);
    assert.equal(createPayload.ok, true);
    assert.equal(createPayload.action, 'create');
    assert.equal(createPayload.data.taskId, 'task-create-001');

    const getResult = await tool.execute('call-get', {
      action: 'get',
      taskId: 'task-get-001',
    });

    assert.equal(getResult.isError, false);
    assert.equal(getCalls.length, 1);
    assert.deepEqual(getCalls[0], {
      taskId: 'task-get-001',
      config: {
        serviceBaseUrl: 'http://127.0.0.1:3105',
        internalToken: 'video-internal-token',
        requestTimeoutMs: 3200,
      },
    });

    const getPayload = parseResultJson(getResult);
    assert.equal(getPayload.ok, true);
    assert.equal(getPayload.action, 'get');
    assert.equal(getPayload.data.taskId, 'task-get-001');
  });

  test('missing topic+vhBizId/taskId returns validation error and does not call shared client', async () => {
    let createCallCount = 0;
    let getCallCount = 0;

    const register = loadRegisterWithClientStub({
      async createTask() {
        createCallCount += 1;
        return {};
      },
      async getTask() {
        getCallCount += 1;
        return {};
      },
    });

    const api = createMockApi();
    register(api);
    const tool = getSingleRegisteredTool(api);

    const missingPromptResult = await tool.execute('call-missing-prompt', {
      action: 'create',
    });
    assert.equal(missingPromptResult.isError, true);
    assert.match(parseResultText(missingPromptResult), /(topic|vhBizId)/i);

    const missingTaskResult = await tool.execute('call-missing-task', {
      action: 'get',
    });
    assert.equal(missingTaskResult.isError, true);
    assert.match(parseResultText(missingTaskResult), /taskId/i);

    assert.equal(createCallCount, 0);
    assert.equal(getCallCount, 0);
  });

  test('upstream/network failure maps to isError=true', async () => {
    const register = loadRegisterWithClientStub({
      async createTask() {
        throw new Error('ECONNREFUSED');
      },
      async getTask() {
        return {};
      },
    });

    const api = createMockApi();
    register(api);
    const tool = getSingleRegisteredTool(api);

    const result = await tool.execute('call-network-failure', {
      action: 'create',
      topic: 'Generate network failure case',
      vhBizId: 'biz-network',
    });

    assert.equal(result.isError, true);
    assert.match(parseResultText(result), /ECONNREFUSED/i);
  });

  test('supports vhBizId and rejects vhbizmode', async () => {
    const createCalls = [];

    const register = loadRegisterWithClientStub({
      async createTask(params) {
        createCalls.push(params);
        return { taskId: 'task-vhbizid-001', status: 'submitted' };
      },
      async getTask() {
        return {};
      },
    });

    const api = createMockApi();
    register(api);
    const tool = getSingleRegisteredTool(api);

    const vhBizIdResult = await tool.execute('call-vhBizId', {
      action: 'create',
      topic: 'Generate vhBizId case',
      vhBizId: 'biz-001',
    });
    assert.equal(vhBizIdResult.isError, false);
    assert.equal(createCalls.length, 1);
    assert.equal(createCalls[0].vhBizId, 'biz-001');

    const vhbizmodeResult = await tool.execute('call-vhbizmode', {
      action: 'create',
      topic: 'Generate vhbizmode reject case',
      vhBizId: 'biz-001',
      vhbizmode: 'legacy-field',
    });
    assert.equal(vhbizmodeResult.isError, true);
    assert.match(parseResultText(vhbizmodeResult), /vhbizmode/i);
    assert.match(parseResultText(vhbizmodeResult), /vhBizId/i);
    assert.equal(createCalls.length, 1);
  });
});
