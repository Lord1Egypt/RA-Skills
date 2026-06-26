'use strict';

// Real-socket e2e for the OpenAI Chat Completions ingress (/v1/chat/completions) — cursor's OpenAI mode + generic
// OpenAI Chat clients. Format-aware passthrough (no translation): an OpenAI-Chat-shaped request goes to the
// OpenAI /chat/completions upstream verbatim. Drives the real ProxyHttpServer + the real handler (built from the
// generalized buildChatCompletionsHandler) + the trace pipeline with a mock OpenAI upstream; asserts the upstream
// path (/chat/completions), byte pass-through, and trace extraction (usage from prompt/completion_tokens,
// finishReason from choices[].finish_reason) for stream + non-stream.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildChatCompletionsHandler } = require('../src/proxy/router/responses_route.js');

const enc = new TextEncoder();
const sse = (parts) => new ReadableStream({ start(c) { for (const p of parts) c.enqueue(enc.encode(p)); c.close(); } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let lastReqPath = null;
function mockOpenAI(reqPath, body) {
  lastReqPath = reqPath; // assert the handler forwarded to /chat/completions
  const stream = body && body.stream === true;
  if (stream) {
    return Promise.resolve({ status: 200, headers: { 'content-type': 'text/event-stream' }, stream: sse([
      'data: {"id":"chatcmpl-1","choices":[{"delta":{"content":"hi"},"index":0}]}\n\n',
      'data: {"id":"chatcmpl-1","choices":[{"delta":{},"finish_reason":"stop","index":0}],"usage":{"prompt_tokens":21,"completion_tokens":4}}\n\n',
      'data: [DONE]\n\n',
    ]) });
  }
  return Promise.resolve({ status: 200, headers: { 'content-type': 'application/json' }, stream: null,
    text: () => JSON.stringify({ id: 'chatcmpl-1', choices: [{ message: { role: 'assistant', content: 'hi' }, finish_reason: 'stop', index: 0 }], usage: { prompt_tokens: 21, completion_tokens: 4 } }) });
}

async function withServer(run) {
  const traceFile = path.join(os.tmpdir(), `e2e-chat-${process.pid}-${(process.hrtime.bigint() % 1000000n).toString()}.jsonl`);
  const saved = { m: process.env.EVOMAP_PROXY_TRACE, f: process.env.EVOMAP_PROXY_TRACE_FILE, e: process.env.EVOMAP_PROXY_TRACE_ENCRYPTION, k: process.env.EVOMAP_OPENAI_API_KEY };
  process.env.EVOMAP_PROXY_TRACE = 'full';
  process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;
  process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '0';
  process.env.EVOMAP_OPENAI_API_KEY = 'sk-test'; // lets the handler accept the request
  lastReqPath = null;
  try { fs.unlinkSync(traceFile); } catch { /* fresh */ }

  const silent = { log() {}, warn() {}, error() {} };
  const routes = { 'POST /v1/chat/completions': buildChatCompletionsHandler({ openAIProxy: mockOpenAI, logger: silent }) };
  const srv = new ProxyHttpServer(routes, { port: 0, logger: silent });
  srv.token = 'e2e-token';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const call = ({ headers, body }) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: '/v1/chat/completions', method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer e2e-token', 'x-api-key': 'sk-client', ...headers } }, (res) => {
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
    process.env.EVOMAP_PROXY_TRACE = saved.m; process.env.EVOMAP_PROXY_TRACE_FILE = saved.f;
    process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = saved.e; process.env.EVOMAP_OPENAI_API_KEY = saved.k;
  }
}

const chatBody = (extra = {}) => ({ model: 'gpt-4o', messages: [{ role: 'user', content: 'hi' }], ...extra });

test('OpenAI Chat (/v1/chat/completions) — forwards to /chat/completions + usage/finish trace (non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ headers: { 'user-agent': 'cursor/0.42' }, body: chatBody() });
    assert.equal(res.status, 200);
    assert.equal(lastReqPath, '/chat/completions');            // forwarded to the chat endpoint, not /responses
    const parsed = JSON.parse(res.bytes.toString('utf8'));
    assert.equal(parsed.choices[0].message.content, 'hi');     // body forwarded unchanged
    const rows = await readRows(1);
    const r = rows.find((x) => !x.isStream);
    assert.ok(r, 'chat non-stream row captured');
    assert.equal(r.path, '/v1/chat/completions');
    assert.equal(r.upstream, 'openai');
    assert.equal(r.input_tokens, 21);   // usage.prompt_tokens
    assert.equal(r.output_tokens, 4);   // usage.completion_tokens
    assert.equal(r.finishReason, 'stop'); // choices[0].finish_reason
  });
});

test('OpenAI Chat (/v1/chat/completions, stream) — SSE tee captures final usage + finish_reason', async () => {
  await withServer(async ({ call, readRows }) => {
    const res = await call({ headers: { 'user-agent': 'cursor/0.42' }, body: chatBody({ stream: true }) });
    assert.equal(res.status, 200);
    assert.equal(lastReqPath, '/chat/completions');
    assert.ok(res.bytes.length > 0);
    const rows = await readRows(1);
    const r = rows.find((x) => x.isStream);
    assert.ok(r, 'chat stream row captured');
    assert.equal(r.upstream, 'openai');
    assert.equal(r.input_tokens, 21);   // from the final SSE chunk's usage
    assert.equal(r.output_tokens, 4);
    assert.equal(r.finishReason, 'stop');
  });
});
