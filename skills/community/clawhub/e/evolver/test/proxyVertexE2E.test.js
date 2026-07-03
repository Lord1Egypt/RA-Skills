'use strict';

// Real-socket e2e for the Vertex AI Gemini route + a direct _proxyVertex auth check. Vertex uses the Gemini body
// on a project/location path with a region base + OAuth Bearer. Asserts route parsing (project/location/model:
// action), region-base computation, trace (upstream=vertex, usage from usageMetadata, finishReason from
// candidates) for stream + non-stream; plus _proxyVertex injects the Bearer token and 401s without one.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildVertexHandler, vertexBaseUrl } = require('../src/proxy/router/vertex_route.js');
const { EvoMapProxy } = require('../src/proxy');

const enc = new TextEncoder();
const sse = (parts) => new ReadableStream({ start(c) { for (const p of parts) c.enqueue(enc.encode(p)); c.close(); } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let captured;
function mockVertex(reqPath, body, opts) {
  captured = { reqPath, baseUrl: opts && opts.baseUrl };
  const stream = reqPath.includes(':streamGenerateContent');
  if (stream) {
    return Promise.resolve({ status: 200, headers: { 'content-type': 'text/event-stream' }, stream: sse([
      'data: {"candidates":[{"content":{"parts":[{"text":"hi"}]}}]}\n\n',
      'data: {"candidates":[{"finishReason":"STOP"}],"usageMetadata":{"promptTokenCount":7,"candidatesTokenCount":3}}\n\n',
    ]) });
  }
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({ candidates: [{ content: { parts: [{ text: 'hi' }] }, finishReason: 'STOP' }], usageMetadata: { promptTokenCount: 7, candidatesTokenCount: 3 } }) });
}

async function withServer(run) {
  const traceFile = path.join(os.tmpdir(), `e2e-vertex-${process.pid}-${(process.hrtime.bigint() % 1000000n).toString()}.jsonl`);
  const saved = { m: process.env.EVOMAP_PROXY_TRACE, f: process.env.EVOMAP_PROXY_TRACE_FILE, e: process.env.EVOMAP_PROXY_TRACE_ENCRYPTION };
  process.env.EVOMAP_PROXY_TRACE = 'full';
  process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;
  process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '0';
  try { fs.unlinkSync(traceFile); } catch { /* fresh */ }
  captured = null;

  const silent = { log() {}, warn() {}, error() {} };
  const routes = { 'POST /v1/projects/:project/locations/:location/publishers/google/models/:modelAction': buildVertexHandler({ vertexProxy: mockVertex, logger: silent }) };
  const srv = new ProxyHttpServer(routes, { port: 0, logger: silent });
  srv.token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const call = ({ reqPath, body }) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: reqPath, method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'user-agent': 'google-genai-sdk/1.0' } }, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => resolve({ status: res.statusCode, bytes: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.end(JSON.stringify(body));
  });

  const readRows = async (expected = 1) => {
    let lines = [];
    for (let i = 0; i < 150; i++) {
      if (fs.existsSync(traceFile)) {
        lines = fs.readFileSync(traceFile, 'utf8').trim().split('\n').filter(Boolean);
        if (lines.length >= expected) break;
      }
      await sleep(20);
    }
    return lines.map((l) => JSON.parse(l));
  };

  try {
    await run({ call, readRows });
  } finally {
    await new Promise((r) => srv.server.close(r));
    try { fs.unlinkSync(traceFile); } catch { /* ignore */ }
    process.env.EVOMAP_PROXY_TRACE = saved.m; process.env.EVOMAP_PROXY_TRACE_FILE = saved.f; process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = saved.e;
  }
}

const VPATH = '/v1/projects/my-proj/locations/us-central1/publishers/google/models/gemini-2.0-flash';
const body = { contents: [{ role: 'user', parts: [{ text: 'hi' }] }] };

test('vertexBaseUrl derives the region host (and respects global / override)', () => {
  assert.equal(vertexBaseUrl('us-central1'), 'https://us-central1-aiplatform.googleapis.com');
  assert.equal(vertexBaseUrl('global'), 'https://aiplatform.googleapis.com');
});

test('Vertex route — parses project/location/model, region base, usage/finish trace (non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: `${VPATH}:generateContent`, body });
    assert.equal(res.status, 200);
    assert.equal(captured.reqPath, `${VPATH}:generateContent`);                 // full Vertex path forwarded
    assert.equal(captured.baseUrl, 'https://us-central1-aiplatform.googleapis.com'); // region base from location
    const r = (await readRows(1)).find((x) => !x.isStream);
    assert.ok(r, 'vertex non-stream row captured');
    assert.equal(r.upstream, 'vertex');
    assert.equal(r.model, 'gemini-2.0-flash');
    assert.equal(r.input_tokens, 7);
    assert.equal(r.output_tokens, 3);
    assert.equal(r.finishReason, 'STOP');
  });
});

test('Vertex route — SSE stream tee captures usageMetadata + finishReason', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: `${VPATH}:streamGenerateContent?alt=sse`, body });
    assert.equal(res.status, 200);
    const r = (await readRows(1)).find((x) => x.isStream);
    assert.ok(r, 'vertex stream row captured');
    assert.equal(r.upstream, 'vertex');
    assert.equal(r.input_tokens, 7);
    assert.equal(r.output_tokens, 3);
    assert.equal(r.finishReason, 'STOP');
  });
});

test('_proxyVertex injects the OAuth Bearer token and 401s without one', async () => {
  const savedTok = process.env.EVOMAP_VERTEX_ACCESS_TOKEN;
  let upstreamAuth = null;
  const stub = http.createServer((req, res) => {
    upstreamAuth = req.headers.authorization;
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ candidates: [{ finishReason: 'STOP' }], usageMetadata: { promptTokenCount: 1, candidatesTokenCount: 1 } }));
  });
  const port = await new Promise((r) => stub.listen(0, '127.0.0.1', () => r(stub.address().port)));
  const proxy = new EvoMapProxy({ logger: { log() {}, warn() {}, error() {} } });
  try {
    delete process.env.EVOMAP_VERTEX_ACCESS_TOKEN;
    await assert.rejects(
      () => proxy._proxyVertex('/v1/projects/p/locations/l/publishers/google/models/m:generateContent', body, { baseUrl: `http://127.0.0.1:${port}` }),
      (e) => e.statusCode === 401,
    );
    process.env.EVOMAP_VERTEX_ACCESS_TOKEN = 'ya29.test-token';
    const up = await proxy._proxyVertex('/v1/projects/p/locations/l/publishers/google/models/m:generateContent', body, { baseUrl: `http://127.0.0.1:${port}` });
    assert.equal(up.status, 200);
    assert.equal(upstreamAuth, 'Bearer ya29.test-token'); // proxy injected the access token
  } finally {
    await new Promise((r) => stub.close(r));
    if (savedTok === undefined) delete process.env.EVOMAP_VERTEX_ACCESS_TOKEN; else process.env.EVOMAP_VERTEX_ACCESS_TOKEN = savedTok;
  }
});
