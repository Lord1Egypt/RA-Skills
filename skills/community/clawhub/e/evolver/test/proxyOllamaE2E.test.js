'use strict';

// Real-socket e2e for the Ollama native ingress (/api/chat, /api/generate). Forwards verbatim to the Ollama
// upstream (no translation). Streaming is NDJSON (not SSE) — the trace tee scans bare JSON lines. Asserts route +
// byte pass-through + per-client trace (client=ollama, usage from prompt_eval_count/eval_count, finishReason from
// done_reason) for both NDJSON stream and non-stream.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildOllamaHandler } = require('../src/proxy/router/ollama_route.js');

const enc = new TextEncoder();
const ndjson = (parts) => new ReadableStream({ start(c) { for (const p of parts) c.enqueue(enc.encode(p)); c.close(); } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function mockOllama(reqPath, body) {
  const stream = !(body && body.stream === false); // ollama streams by default
  if (stream) {
    return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: ndjson([
      '{"model":"llama3.2","message":{"role":"assistant","content":"hi"},"done":false}\n',
      '{"model":"llama3.2","message":{"role":"assistant","content":" there"},"done":true,"done_reason":"stop","prompt_eval_count":10,"eval_count":5}\n',
    ]) });
  }
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({ model: 'llama3.2', message: { role: 'assistant', content: 'hi there' }, done: true, done_reason: 'stop', prompt_eval_count: 10, eval_count: 5 }) });
}

async function withServer(run) {
  const traceFile = path.join(os.tmpdir(), `e2e-ollama-${process.pid}-${(process.hrtime.bigint() % 1000000n).toString()}.jsonl`);
  const saved = { m: process.env.EVOMAP_PROXY_TRACE, f: process.env.EVOMAP_PROXY_TRACE_FILE, e: process.env.EVOMAP_PROXY_TRACE_ENCRYPTION };
  process.env.EVOMAP_PROXY_TRACE = 'full';
  process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;
  process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '0';
  try { fs.unlinkSync(traceFile); } catch { /* fresh */ }

  const silent = { log() {}, warn() {}, error() {} };
  const routes = {
    'POST /api/chat': buildOllamaHandler({ ollamaProxy: mockOllama, apiPath: '/api/chat', logger: silent }),
    'POST /api/generate': buildOllamaHandler({ ollamaProxy: mockOllama, apiPath: '/api/generate', logger: silent }),
  };
  const srv = new ProxyHttpServer(routes, { port: 0, logger: silent });
  srv.token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const call = ({ reqPath, body }) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: reqPath, method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'user-agent': 'ollama/0.5.1' } }, (res) => {
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

const chatBody = (extra = {}) => ({ model: 'llama3.2', messages: [{ role: 'user', content: 'hi' }], ...extra });

test('Ollama /api/chat (non-stream) — native passthrough + usage/finish from eval counts', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: '/api/chat', body: chatBody({ stream: false }) });
    assert.equal(res.status, 200);
    const parsed = JSON.parse(res.bytes.toString('utf8'));
    assert.equal(parsed.message.content, 'hi there');   // body forwarded unchanged
    const rows = await readRows(1);
    const r = rows.find((x) => !x.isStream);
    assert.ok(r, 'ollama non-stream row captured');
    assert.equal(r.client, 'ollama');
    assert.equal(r.upstream, 'ollama');
    assert.equal(r.model, 'llama3.2');
    assert.equal(r.input_tokens, 10);   // prompt_eval_count
    assert.equal(r.output_tokens, 5);   // eval_count
    assert.equal(r.finishReason, 'stop'); // done_reason
  });
});

test('Ollama /api/chat (NDJSON stream) — tee scans bare JSON lines for eval counts + done_reason', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: '/api/chat', body: chatBody() }); // default stream
    assert.equal(res.status, 200);
    assert.ok(res.bytes.length > 0);
    const rows = await readRows(1);
    const r = rows.find((x) => x.isStream);
    assert.ok(r, 'ollama stream row captured');
    assert.equal(r.upstream, 'ollama');
    assert.equal(r.input_tokens, 10);   // from the final NDJSON chunk
    assert.equal(r.output_tokens, 5);
    assert.equal(r.finishReason, 'stop');
  });
});

test('Ollama /api/generate route also works', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ reqPath: '/api/generate', body: { model: 'llama3.2', prompt: 'hi', stream: false } });
    assert.equal(res.status, 200);
    const rows = await readRows(1);
    const r = rows.find((x) => !x.isStream);
    assert.ok(r, 'generate row captured');
    assert.equal(r.path, '/api/generate');
    assert.equal(r.upstream, 'ollama');
    assert.equal(r.output_tokens, 5);
  });
});
