'use strict';

// Real-socket e2e for GET /v1/models routing. The probe is routed by the `anthropic-version` header to the
// Anthropic or OpenAI upstream's model list (so codex/opencode/cursor/SDK startup probes never 404). Mocks the
// provider callables to assert: correct provider chosen, GET method + no body, native path (/v1/models vs
// /models), and the model list forwarded back.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildModelsHandler } = require('../src/proxy/router/models_route.js');

let calls;
function mockAnthropic(reqPath, body, opts) {
  calls.push({ provider: 'anthropic', reqPath, body, method: opts && opts.method });
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({ data: [{ id: 'claude-opus-4-8', type: 'model' }] }) });
}
function mockOpenAI(reqPath, body, opts) {
  calls.push({ provider: 'openai', reqPath, body, method: opts && opts.method });
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({ object: 'list', data: [{ id: 'gpt-4o', object: 'model' }] }) });
}

async function withServer(run) {
  calls = [];
  const silent = { log() {}, warn() {}, error() {} };
  const handler = buildModelsHandler({ anthropicProxy: mockAnthropic, openAIProxy: mockOpenAI, logger: silent });
  const srv = new ProxyHttpServer({ 'GET /v1/models': handler }, { port: 0, logger: silent });
  srv.token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const get = (headers) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: '/v1/models', method: 'GET',
      headers: { authorization: 'Bearer aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', ...headers } }, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => resolve({ status: res.statusCode, bytes: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.end();
  });

  try {
    await run({ get });
  } finally {
    await new Promise((r) => srv.server.close(r));
  }
}

test('GET /v1/models with anthropic-version header → Anthropic /v1/models (GET, no body)', async () => {
  await withServer(async ({ get }) => {
    const res = await get({ 'anthropic-version': '2023-06-01' });
    assert.equal(res.status, 200);
    const body = JSON.parse(res.bytes.toString('utf8'));
    assert.equal(body.data[0].id, 'claude-opus-4-8');         // anthropic list forwarded
    assert.equal(calls.length, 1);
    assert.equal(calls[0].provider, 'anthropic');
    assert.equal(calls[0].reqPath, '/v1/models');
    assert.equal(calls[0].method, 'GET');
    assert.equal(calls[0].body, null);                        // GET sends no body
  });
});

test('GET /v1/models without anthropic-version → OpenAI /models (default; codex/opencode/cursor)', async () => {
  await withServer(async ({ get }) => {
    const res = await get({ 'user-agent': 'opencode/1.0' });
    assert.equal(res.status, 200);
    const body = JSON.parse(res.bytes.toString('utf8'));
    assert.equal(body.data[0].id, 'gpt-4o');                  // openai list forwarded
    assert.equal(calls[0].provider, 'openai');
    assert.equal(calls[0].reqPath, '/models');                // OpenAI base already ends in /v1 → /models
    assert.equal(calls[0].method, 'GET');
    assert.equal(calls[0].body, null);
  });
});

test('GET /v1/models surfaces an upstream 401 (no key) instead of 404', async () => {
  await withServer(async ({ get }) => {
    // openAIProxy that throws like _proxyOpenAIResponses does with no key
    const handler = buildModelsHandler({
      anthropicProxy: mockAnthropic,
      openAIProxy: () => Promise.reject(Object.assign(new Error('openai api key required'), { statusCode: 401 })),
      logger: { log() {}, warn() {}, error() {} },
    });
    // swap in a one-off server for this case
    const srv = new ProxyHttpServer({ 'GET /v1/models': handler }, { port: 0, logger: { log() {}, warn() {}, error() {} } });
    srv.token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
    srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
    const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
    srv.actualPort = port;
    const res = await new Promise((resolve, reject) => {
      const req = http.request({ host: '127.0.0.1', port, path: '/v1/models', method: 'GET', headers: { authorization: 'Bearer aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' } }, (r) => {
        const ch = []; r.on('data', (d) => ch.push(d)); r.on('end', () => resolve({ status: r.statusCode, bytes: Buffer.concat(ch) }));
      });
      req.on('error', reject); req.end();
    });
    await new Promise((r) => srv.server.close(r));
    assert.equal(res.status, 401);
    assert.match(res.bytes.toString('utf8'), /api key required/);
  });
});
