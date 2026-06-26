const { describe, test, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { requestJson } = require('./helpers/http-json');

const MODEL_ID = 'CVHPZJ4LCGBMNIZULS0';
const TOKENS = {
  internal: 'internal-token',
  admin: 'admin-token',
  callback: 'callback-token',
};

function loadStartVideoTaskService() {
  try {
    const exported = require('../src/service/server').startVideoTaskService;
    if (typeof exported === 'function') {
      return exported;
    }
  } catch (serverModuleError) {
    // fall through to secondary source lookup.
    void serverModuleError;
  }

  const serviceModule = require('../src/service');
  if (typeof serviceModule.startVideoTaskService === 'function') {
    return serviceModule.startVideoTaskService;
  }

  throw new Error(
    'Missing startVideoTaskService export. Expected ../src/service/server or ../src/service to export function startVideoTaskService().'
  );
}

const startVideoTaskService = loadStartVideoTaskService();

function createTempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'video-task-service-'));
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitFor(predicate, { timeoutMs = 2000, intervalMs = 25 } = {}) {
  const startedAt = Date.now();
  let lastValue = null;

  while (Date.now() - startedAt <= timeoutMs) {
    lastValue = await predicate();
    if (lastValue) {
      return lastValue;
    }
    await wait(intervalMs);
  }

  throw new Error(`waitFor timeout after ${timeoutMs}ms`);
}

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
        return next.body ?? {};
      },
    };
  }

  fetchStub.calls = calls;
  fetchStub.queueResponse = (response) => {
    queue.push(response);
  };

  return fetchStub;
}

function parseFetchJsonBody(call) {
  assert.equal(typeof call?.init?.body, 'string');
  return JSON.parse(call.init.body);
}

describe('video-task-service integration (node:test)', { concurrency: 1 }, () => {
  let tempDir;
  let service;
  let baseUrl;
  let nowMs;
  let originalFetch;
  let fetchStub;

  beforeEach(async () => {
    tempDir = createTempDir();
    nowMs = Date.now();

    originalFetch = global.fetch;
    fetchStub = createFetchStub();
    global.fetch = fetchStub;

    service = await startVideoTaskService({
      port: 0,
      dbPath: path.join(tempDir, 'video-tasks.db'),
      secretsPath: path.join(tempDir, 'video-secrets.json'),
      internalToken: TOKENS.internal,
      adminToken: TOKENS.admin,
      callbackToken: TOKENS.callback,
      providerModelId: MODEL_ID,
      taskTimeoutMs: 100,
      providerSubmitMaxRetries: 1,
      providerSubmitRetryDelaysMs: [1],
      now: () => nowMs,
    });
    baseUrl = `http://127.0.0.1:${service.port}`;
  });

  afterEach(async () => {
    if (service && typeof service.close === 'function') {
      await service.close();
    }
    global.fetch = originalFetch;
  });

  test('POST /v1/tasks: internal auth and create field validation', async () => {
    const unauthorized = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      body: { topic: 'hello world', vhBizId: 'biz-unauthorized' },
    });
    assert.equal(unauthorized.statusCode, 401);

    const invalidTopic = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: { topic: '   ', vhBizId: 'biz-1', sessionId: 'sess-1' },
    });
    assert.equal(invalidTopic.statusCode, 422);

    const missingVhBizId = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: { topic: 'Generate missing vhBizId validation test' },
    });
    assert.equal(missingVhBizId.statusCode, 422);

    assert.equal(fetchStub.calls.length, 0);
  });

  test('POST /v1/tasks rejects legacy vhbizmode field', async () => {
    const legacyFieldResp = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate a legacy field rejection test video',
        vhBizId: 'biz-legacy',
        vhbizmode: 'legacy-biz',
      },
    });

    assert.equal(legacyFieldResp.statusCode, 422);
    assert.equal(legacyFieldResp.body?.error?.code, 'validation_error');
    assert.equal(legacyFieldResp.body?.error?.message, 'vhbizmode is no longer supported; use vhBizId');
    assert.equal(fetchStub.calls.length, 0);
  });

  test('POST /v1/tasks then GET /v1/tasks/:taskId can query created task', async () => {
    fetchStub.queueResponse({
      status: 200,
      body: { taskId: 'provider-query-001' },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate a product intro video',
        vhBizId: 'biz-query-001',
        sessionId: 'session-query',
        traceId: 'trace-query',
      },
    });

    assert.equal(created.statusCode, 202);
    assert.equal(created.body?.data?.status, 'submitted');
    assert.ok(created.body?.data?.taskId);

    const queried = await requestJson({
      baseUrl,
      method: 'GET',
      route: `/v1/tasks/${created.body.data.taskId}`,
      headers: { 'X-Internal-Token': TOKENS.internal },
    });

    assert.equal(queried.statusCode, 200);
    assert.equal(queried.body?.data?.taskId, created.body.data.taskId);
    assert.ok(queried.body?.data?.status);
  });

  test('POST /v1/tasks maps request fields into the provider payload contract', async () => {
    fetchStub.queueResponse({
      status: 200,
      body: { taskId: 'provider-contract-001' },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate a contract coverage video',
        vhBizId: 'biz-request-001',
        sessionId: 'session-contract',
        traceId: 'trace-contract',
        title: 'Contract test title',
        content: 'Contract test content',
        materialList: [{ url: 'https://example.com/material.jpg' }],
        ttsConf: {
          voice: 'female',
        },
        aigcWatermark: true,
      },
    });

    assert.equal(created.statusCode, 202);

    const providerCall = await waitFor(() => fetchStub.calls[0] || null);
    assert.equal(providerCall.input, 'http://127.0.0.1:3999/openapi/aivideo/create');
    assert.equal(providerCall.init?.method, 'POST');
    assert.equal(providerCall.init?.headers?.['Content-Type'], 'application/json');

    const providerPayload = parseFetchJsonBody(providerCall);
    assert.equal(providerPayload.topic, 'Generate a contract coverage video');
    assert.equal(providerPayload.vhBizId, 'biz-request-001');
    assert.equal(providerPayload.modelId, MODEL_ID);
    assert.equal(providerPayload.title, 'Contract test title');
    assert.equal(providerPayload.content, 'Contract test content');
    assert.deepEqual(providerPayload.materialList, [{ url: 'https://example.com/material.jpg' }]);
    assert.deepEqual(providerPayload.ttsConf, { voice: 'female' });
    assert.equal(providerPayload.aigcWatermark, true);

    const callbackUrl = new URL(providerPayload.callbackUrl);
    assert.equal(callbackUrl.origin, baseUrl);
    assert.equal(callbackUrl.pathname, '/v1/callbacks/provider');
    assert.equal(callbackUrl.searchParams.get('token'), TOKENS.callback);
  });

  test('POST /v1/callbacks/provider success updates status and videoUrl', async () => {
    const providerTaskId = 'provider-callback-001';
    const videoUrl = 'https://cdn.example.com/provider-callback-001.mp4';

    fetchStub.queueResponse({
      status: 200,
      body: { taskId: providerTaskId },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate callback update test video',
        vhBizId: 'biz-callback-001',
        sessionId: 'session-callback',
        traceId: 'trace-callback',
      },
    });
    assert.equal(created.statusCode, 202);
    const taskId = created.body.data.taskId;

    await waitFor(async () => {
      const statusResp = await requestJson({
        baseUrl,
        method: 'GET',
        route: `/v1/tasks/${taskId}`,
        headers: { 'X-Internal-Token': TOKENS.internal },
      });
      return statusResp.body?.data?.providerTaskId ? statusResp : null;
    });

    const callbackResp = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/callbacks/provider',
      headers: { 'X-Callback-Token': TOKENS.callback },
      body: {
        providerTaskId,
        videoUrl,
      },
    });
    assert.equal(callbackResp.statusCode, 200);

    const finalResp = await requestJson({
      baseUrl,
      method: 'GET',
      route: `/v1/tasks/${taskId}`,
      headers: { 'X-Internal-Token': TOKENS.internal },
    });

    assert.equal(finalResp.statusCode, 200);
    assert.equal(finalResp.body?.data?.status, 'succeeded');
    assert.equal(finalResp.body?.data?.videoUrl, videoUrl);
  });

  test('POST /v1/callbacks/provider accepts query token auth and failure payloads', async () => {
    const providerTaskId = 'provider-callback-failed-001';

    fetchStub.queueResponse({
      status: 200,
      body: { taskId: providerTaskId },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate callback failure test video',
        vhBizId: 'biz-callback-failed-001',
        sessionId: 'session-callback-failed',
        traceId: 'trace-callback-failed',
      },
    });
    assert.equal(created.statusCode, 202);
    const taskId = created.body.data.taskId;

    await waitFor(async () => {
      const statusResp = await requestJson({
        baseUrl,
        method: 'GET',
        route: `/v1/tasks/${taskId}`,
        headers: { 'X-Internal-Token': TOKENS.internal },
      });
      return statusResp.body?.data?.providerTaskId ? statusResp : null;
    });

    const callbackResp = await requestJson({
      baseUrl,
      method: 'POST',
      route: `/v1/callbacks/provider?token=${encodeURIComponent(TOKENS.callback)}`,
      body: {
        providerTaskId,
        status: 'failed',
      },
    });
    assert.equal(callbackResp.statusCode, 200);

    const finalResp = await requestJson({
      baseUrl,
      method: 'GET',
      route: `/v1/tasks/${taskId}`,
      headers: { 'X-Internal-Token': TOKENS.internal },
    });

    assert.equal(finalResp.statusCode, 200);
    assert.equal(finalResp.body?.data?.status, 'failed');
    assert.equal(finalResp.body?.data?.errorMessage, 'PROVIDER_CALLBACK_FAILED');
  });

  test('PUT /v1/admin/config updates runtime config used by later submissions', async () => {
    const unauthorized = await requestJson({
      baseUrl,
      method: 'PUT',
      route: '/v1/admin/config',
      body: { apiBaseUrl: 'https://provider.example.com' },
    });
    assert.equal(unauthorized.statusCode, 401);

    const legacyFieldResp = await requestJson({
      baseUrl,
      method: 'PUT',
      route: '/v1/admin/config',
      headers: { 'X-Admin-Token': TOKENS.admin },
      body: { vhbizmode: 'legacy-biz-config' },
    });
    assert.equal(legacyFieldResp.statusCode, 422);
    assert.equal(legacyFieldResp.body?.error?.code, 'validation_error');
    assert.equal(legacyFieldResp.body?.error?.message, 'vhbizmode is no longer supported; use vhBizId');

    const updated = await requestJson({
      baseUrl,
      method: 'PUT',
      route: '/v1/admin/config',
      headers: { 'X-Admin-Token': TOKENS.admin },
      body: {
        apiBaseUrl: 'https://provider.example.com',
        apiKey: 'abcdefghi',
        providerAuthHeader: 'Authorization',
        providerAuthScheme: 'Bearer',
        providerPath: 'custom/create',
        vhBizId: 'biz-config-001',
      },
    });

    assert.equal(updated.statusCode, 200);
    assert.equal(updated.body?.data?.apiBaseUrl, 'https://provider.example.com');
    assert.equal(updated.body?.data?.apiKey, 'abc***ghi');
    assert.equal(updated.body?.data?.providerPath, '/custom/create');
    assert.equal(updated.body?.data?.vhBizId, 'biz-config-001');
    assert.equal(
      Object.prototype.hasOwnProperty.call(updated.body?.data || {}, 'vhbizmode'),
      false
    );

    fetchStub.queueResponse({
      status: 200,
      body: { taskId: 'provider-config-001' },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate config-updated video',
        vhBizId: 'biz-config-request-001',
      },
    });
    assert.equal(created.statusCode, 202);

    const providerCall = await waitFor(() => fetchStub.calls[0] || null);
    assert.equal(providerCall.input, 'https://provider.example.com/custom/create');
    assert.equal(providerCall.init?.headers?.Authorization, 'Bearer abcdefghi');

    const providerPayload = parseFetchJsonBody(providerCall);
    assert.equal(providerPayload.vhBizId, 'biz-config-request-001');
  });

  test('protected routes return 401 without token', async () => {
    const createResp = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      body: { topic: 'unauthorized create', vhBizId: 'biz-unauthorized' },
    });
    assert.equal(createResp.statusCode, 401);

    const getResp = await requestJson({
      baseUrl,
      method: 'GET',
      route: '/v1/tasks/any-task-id',
    });
    assert.equal(getResp.statusCode, 401);

    const callbackResp = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/callbacks/provider',
      body: {
        providerTaskId: 'provider-unauthorized',
        videoUrl: 'https://cdn.example.com/unauthorized.mp4',
      },
    });
    assert.equal(callbackResp.statusCode, 401);
  });

  test('POST /v1/tasks validates materialList and ttsConf field types', async () => {
    const invalidMaterialList = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate invalid materialList test video',
        vhBizId: 'biz-invalid-materials',
        materialList: {},
      },
    });
    assert.equal(invalidMaterialList.statusCode, 422);

    const invalidTtsConf = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Generate invalid ttsConf test video',
        vhBizId: 'biz-invalid-tts',
        ttsConf: [],
      },
    });
    assert.equal(invalidTtsConf.statusCode, 422);
    assert.equal(fetchStub.calls.length, 0);
  });

  test('timeout materialize: stale processing task becomes timeout on query', async () => {
    fetchStub.queueResponse({
      status: 200,
      body: { taskId: 'provider-timeout-001' },
    });

    const created = await requestJson({
      baseUrl,
      method: 'POST',
      route: '/v1/tasks',
      headers: { 'X-Internal-Token': TOKENS.internal },
      body: {
        topic: 'Timeout materialize behavior test',
        vhBizId: 'biz-timeout-001',
        sessionId: 'session-timeout',
        traceId: 'trace-timeout',
      },
    });
    assert.equal(created.statusCode, 202);
    const taskId = created.body.data.taskId;

    await waitFor(async () => {
      const statusResp = await requestJson({
        baseUrl,
        method: 'GET',
        route: `/v1/tasks/${taskId}`,
        headers: { 'X-Internal-Token': TOKENS.internal },
      });
      return statusResp.body?.data?.status === 'processing' ? statusResp : null;
    });

    nowMs += 1000;
    const timedOut = await requestJson({
      baseUrl,
      method: 'GET',
      route: `/v1/tasks/${taskId}`,
      headers: { 'X-Internal-Token': TOKENS.internal },
    });

    assert.equal(timedOut.statusCode, 200);
    assert.equal(timedOut.body?.data?.status, 'timeout');
  });
});
