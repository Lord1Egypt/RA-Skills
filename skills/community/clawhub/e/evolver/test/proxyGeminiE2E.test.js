'use strict';

// Real-socket e2e for the Gemini passthrough route (#format-aware routing, no translation). Drives the native
// Gemini path `/v1beta/models/<model>:generateContent` | `:streamGenerateContent` through the real
// ProxyHttpServer + the real gemini handler + the real trace pipeline, with a mock Gemini upstream that answers
// in Gemini's shape (candidates + usageMetadata). Asserts route matching (model:action in one path segment),
// byte pass-through, and per-client trace extraction (client=gemini, usage from usageMetadata, finishReason
// from candidates[].finishReason) for both streaming and non-streaming.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildGeminiHandler } = require('../src/proxy/router/gemini_route.js');

const enc = new TextEncoder();
const sse = (parts) => new ReadableStream({ start(c) { for (const p of parts) c.enqueue(enc.encode(p)); c.close(); } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Mock Gemini upstream, faithful to Google's behavior:
//  - :streamGenerateContent?alt=sse  -> SSE (text/event-stream)
//  - :streamGenerateContent (default) -> chunked JSON-ARRAY stream served as application/json (NOT non-stream)
//  - :generateContent                 -> single JSON body (application/json, non-stream)
function mockGemini(reqPath, _body) {
  const isStreamAction = reqPath.includes(':streamGenerateContent');
  const sseMode = reqPath.includes('alt=sse');
  if (isStreamAction && sseMode) {
    return Promise.resolve({ status: 200, headers: { 'content-type': 'text/event-stream' }, stream: sse([
      'data: {"candidates":[{"content":{"role":"model","parts":[{"text":"hi"}]}}]}\n\n',
      'data: {"candidates":[{"content":{"role":"model","parts":[{"text":" there"}]},"finishReason":"STOP"}],"usageMetadata":{"promptTokenCount":12,"candidatesTokenCount":4,"totalTokenCount":16}}\n\n',
    ]) });
  }
  if (isStreamAction) {
    // Default array-stream: application/json content-type but a chunked stream body — must NOT be buffered.
    return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: sse([
      '[{"candidates":[{"content":{"role":"model","parts":[{"text":"hi"}]}}]}\r\n',
      ',{"candidates":[{"content":{"role":"model","parts":[{"text":" there"}]},"finishReason":"STOP"}],"usageMetadata":{"promptTokenCount":12,"candidatesTokenCount":4}}\r\n]',
    ]) });
  }
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({
      candidates: [{ content: { role: 'model', parts: [{ text: 'hi there' }] }, finishReason: 'STOP' }],
      usageMetadata: { promptTokenCount: 12, candidatesTokenCount: 4, totalTokenCount: 16 },
    }) });
}

async function withServer(run) {
  const traceFile = path.join(os.tmpdir(), `e2e-gemini-${process.pid}-${(process.hrtime.bigint() % 1000000n).toString()}.jsonl`);
  const saved = { m: process.env.EVOMAP_PROXY_TRACE, f: process.env.EVOMAP_PROXY_TRACE_FILE, e: process.env.EVOMAP_PROXY_TRACE_ENCRYPTION, k: process.env.EVOMAP_GEMINI_API_KEY };
  process.env.EVOMAP_PROXY_TRACE = 'full';
  process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;
  process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '0';
  process.env.EVOMAP_GEMINI_API_KEY = 'gk-test'; // lets the gemini handler accept the request
  try { fs.unlinkSync(traceFile); } catch { /* fresh */ }

  const silent = { log() {}, warn() {}, error() {} };
  const routes = { 'POST /v1beta/models/:modelAction': buildGeminiHandler({ geminiProxy: mockGemini, logger: silent }) };
  const srv = new ProxyHttpServer(routes, { port: 0, logger: silent });
  srv.token = 'e2e-token';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const call = ({ reqPath, body }) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: reqPath, method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer e2e-token', 'x-goog-api-key': 'client-key', 'user-agent': 'google-genai-sdk/1.0' } }, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => resolve({ status: res.statusCode, bytes: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.end(JSON.stringify(body));
  });

  const readRows = async (expected = 2) => {
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
    process.env.EVOMAP_PROXY_TRACE = saved.m; process.env.EVOMAP_PROXY_TRACE_FILE = saved.f;
    process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = saved.e; process.env.EVOMAP_GEMINI_API_KEY = saved.k;
  }
}

const body = { contents: [{ role: 'user', parts: [{ text: 'hi' }] }], generationConfig: { temperature: 0.2 } };

test('Gemini (/v1beta/models/<model>:generateContent) — native passthrough route + usage/finish trace (non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: '/v1beta/models/gemini-2.0-flash:generateContent', body });
    assert.equal(res.status, 200);
    const parsed = JSON.parse(res.bytes.toString('utf8'));
    assert.equal(parsed.candidates[0].content.parts[0].text, 'hi there'); // body forwarded unchanged
    const rows = await readRows(1);
    const r = rows.find((x) => x.client === 'gemini' && !x.isStream);
    assert.ok(r, 'gemini non-stream row captured');
    assert.equal(r.path, '/v1beta/models/gemini-2.0-flash:generateContent'); // native path recorded
    assert.equal(r.model, 'gemini-2.0-flash');                                // model parsed from path
    assert.equal(r.upstream, 'gemini');
    assert.equal(r.input_tokens, 12);   // usageMetadata.promptTokenCount
    assert.equal(r.output_tokens, 4);   // usageMetadata.candidatesTokenCount
    assert.equal(r.finishReason, 'STOP'); // candidates[0].finishReason
  });
});

test('Gemini (:streamGenerateContent default, application/json array-stream) — forwarded as a live stream, not buffered into an error', async () => {
  await withServer(async ({ call, readRows }) => {
    // No ?alt=sse: Google serves a chunked JSON-array stream as application/json. Must be streamed through, not
    // buffered + JSON.parsed into a {error:...} wrapper (the bug Bugbot flagged on the first cut).
    const res = await call({ reqPath: '/v1beta/models/gemini-2.0-flash:streamGenerateContent', body: { ...body } });
    assert.equal(res.status, 200);
    const text = res.bytes.toString('utf8');
    assert.ok(text.startsWith('[') || text.includes('"candidates"'), 'array-stream body forwarded verbatim');
    assert.ok(!/"error"\s*:/.test(text), 'must NOT be wrapped as an upstream error');
    const rows = await readRows(1);
    const r = rows.find((x) => x.client === 'gemini' && x.isStream);
    assert.ok(r, 'default stream recorded as a streamed row');
    assert.equal(r.upstream, 'gemini');
  });
});

test('Gemini (:streamGenerateContent?alt=sse) — SSE tee captures usageMetadata + finishReason from the stream', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: '/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse', body: { ...body } });
    assert.equal(res.status, 200);
    assert.ok(res.bytes.length > 0); // SSE bytes forwarded
    const rows = await readRows(1);
    const r = rows.find((x) => x.client === 'gemini' && x.isStream);
    assert.ok(r, 'gemini stream row captured');
    assert.equal(r.upstream, 'gemini');
    assert.equal(r.input_tokens, 12);   // captured from the final SSE chunk's usageMetadata
    assert.equal(r.output_tokens, 4);
    assert.equal(r.finishReason, 'STOP');
  });
});
