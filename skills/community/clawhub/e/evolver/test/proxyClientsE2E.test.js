'use strict';

// Real end-to-end coverage for the three agent clients that drive the proxy, each over a real socket through
// the real ProxyHttpServer + the real route handler + the real trace pipeline, with format-aware mock upstreams:
//   - Claude Code  -> POST /v1/messages  (native Anthropic Messages)
//   - cursor       -> POST /v1/messages  (Anthropic mode + x-cursor-session-id)
//   - codex        -> POST /v1/responses (OpenAI Responses: input / previous_response_id / response.completed)
// Asserts byte pass-through and per-client trace-row extraction (client detect, session/threading keys, usage,
// finish) for BOTH streaming and non-streaming. codex exercises the real /v1/responses route, not /v1/messages.

const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { ProxyHttpServer } = require('../src/proxy/server/http.js');
const { buildMessagesHandler } = require('../src/proxy/router/messages_route.js');
const { buildResponsesHandler } = require('../src/proxy/router/responses_route.js');

const enc = new TextEncoder();
const sse = (parts) => new ReadableStream({ start(c) { for (const p of parts) c.enqueue(enc.encode(p)); c.close(); } });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Anthropic upstream (claude code / cursor-anthropic-mode).
function mockAnthropic(_p, body) {
  const stream = body && body.stream === true;
  return Promise.resolve(stream
    ? { status: 200, headers: { 'content-type': 'text/event-stream' }, stream: sse([
        'event: message_start\ndata: {"type":"message_start","message":{"id":"msg_live9","usage":{"input_tokens":40,"cache_read_input_tokens":5}}}\n\n',
        'event: content_block_delta\ndata: {"type":"content_block_delta","delta":{"text":"hi"}}\n\n',
        'event: message_delta\ndata: {"type":"message_delta","usage":{"output_tokens":12},"delta":{"stop_reason":"end_turn"}}\n\n',
      ]) }
    : { status: 200, headers: { 'content-type': 'application/json' }, stream: null,
        text: () => JSON.stringify({ id: 'msg_live9', stop_reason: 'end_turn', usage: { input_tokens: 40, output_tokens: 12, cache_read_input_tokens: 5 } }) });
}

// OpenAI Responses upstream (codex).
function mockOpenAI(_p, body) {
  const stream = body && body.stream === true;
  return Promise.resolve(stream
    ? { status: 200, headers: { 'content-type': 'text/event-stream' }, stream: sse([
        'event: response.created\ndata: {"type":"response.created","response":{"id":"resp_live123","status":"in_progress"}}\n\n',
        'event: response.output_text.delta\ndata: {"type":"response.output_text.delta","delta":"hi"}\n\n',
        'event: response.completed\ndata: {"type":"response.completed","response":{"id":"resp_live123","status":"completed","usage":{"input_tokens":33,"output_tokens":7}}}\n\n',
      ]) }
    : { status: 200, headers: { 'content-type': 'application/json' }, stream: null,
        text: () => JSON.stringify({ id: 'resp_live123', status: 'completed', usage: { input_tokens: 33, output_tokens: 7 } }) });
}

async function withServer(run) {
  const traceFile = path.join(os.tmpdir(), `e2e-clients-${process.pid}-${(process.hrtime.bigint() % 1000000n).toString()}.jsonl`);
  const saved = {
    m: process.env.EVOMAP_PROXY_TRACE, f: process.env.EVOMAP_PROXY_TRACE_FILE, e: process.env.EVOMAP_PROXY_TRACE_ENCRYPTION,
    k: process.env.EVOMAP_OPENAI_API_KEY,
  };
  process.env.EVOMAP_PROXY_TRACE = 'full';
  process.env.EVOMAP_PROXY_TRACE_FILE = traceFile;
  process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = '0';
  process.env.EVOMAP_OPENAI_API_KEY = 'sk-openai-test'; // lets the /v1/responses handler accept codex
  try { fs.unlinkSync(traceFile); } catch { /* fresh */ }

  const silent = { log() {}, warn() {}, error() {} };
  const routes = {
    'POST /v1/messages': buildMessagesHandler({ anthropicProxy: mockAnthropic, routerEnabled: false, logger: silent }),
    'POST /v1/responses': buildResponsesHandler({ openAIProxy: mockOpenAI, logger: silent }),
  };
  // Bypass start() so we never write the operator's real settings.json; wire token + port by hand (read-only auth).
  const srv = new ProxyHttpServer(routes, { port: 0, logger: silent });
  srv.token = 'e2e-token';
  srv.server = http.createServer((req, res) => srv._handleRequest(req, res));
  const port = await new Promise((resolve) => srv.server.listen(0, '127.0.0.1', () => resolve(srv.server.address().port)));
  srv.actualPort = port;

  const call = ({ path: reqPath = '/v1/messages', headers, body }) => new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port, path: reqPath, method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer e2e-token', 'x-api-key': 'sk-client', ...headers } }, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => resolve({ status: res.statusCode, bytes: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.end(JSON.stringify(body));
  });

  // Each test issues a non-stream + a stream call; the streamed row emits only once its SSE body is drained,
  // so wait for the expected count (not just the first line) before asserting.
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
    process.env.EVOMAP_PROXY_TRACE_ENCRYPTION = saved.e; process.env.EVOMAP_OPENAI_API_KEY = saved.k;
  }
}

const claudeMeta = JSON.stringify({ session_id: 'sess-CC-uuid-1', device_id: 'a'.repeat(64) });

test('Claude Code (/v1/messages) — session, usage, finish, response id over real HTTP (stream + non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const n = await call({ headers: { 'user-agent': 'claude-cli/2.1.169' }, body: { model: 'claude-opus-4-8', metadata: { user_id: claudeMeta }, messages: [{ role: 'user', content: 'hi' }] } });
    const s = await call({ headers: { 'user-agent': 'claude-cli/2.1.169' }, body: { model: 'claude-opus-4-8', stream: true, metadata: { user_id: claudeMeta }, messages: [{ role: 'user', content: 'hi' }] } });
    assert.equal(n.status, 200); assert.ok(n.bytes.length > 0);
    assert.equal(s.status, 200); assert.ok(s.bytes.length > 0);
    const rows = await readRows();
    const ccN = rows.find((r) => r.client === 'claude-code' && !r.isStream);
    const ccS = rows.find((r) => r.client === 'claude-code' && r.isStream);
    assert.ok(ccN && ccS, 'both claude rows captured');
    assert.equal(ccN.sessionId, 'sess-CC-uuid-1');     // inner session_id, not the whole user_id blob
    assert.equal(ccN.input_tokens, 40); assert.equal(ccN.output_tokens, 12);
    assert.equal(ccN.cacheReadTokens, 5);
    assert.equal(ccN.finishReason, 'end_turn');
    assert.equal(ccN.responseId, 'msg_live9');
    assert.ok(ccN.id, 'trace id populated (was null)');
    assert.equal(ccS.input_tokens, 40); assert.equal(ccS.output_tokens, 12); // streamed usage (deferred emit)
    assert.equal(ccS.finishReason, 'end_turn');
    assert.equal(ccS.responseId, 'msg_live9');
  });
});

test('cursor (/v1/messages, Anthropic mode) — x-cursor-session-id + usage over real HTTP (stream + non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const hdr = { 'user-agent': 'cursor/0.42', 'x-cursor-session-id': 'cur-sess-9' };
    const n = await call({ headers: hdr, body: { model: 'claude-opus-4-8', messages: [{ role: 'user', content: 'hi' }] } });
    const s = await call({ headers: hdr, body: { model: 'claude-opus-4-8', stream: true, messages: [{ role: 'user', content: 'hi' }] } });
    assert.equal(n.status, 200); assert.equal(s.status, 200);
    const rows = await readRows();
    const cN = rows.find((r) => r.client === 'cursor' && !r.isStream);
    const cS = rows.find((r) => r.client === 'cursor' && r.isStream);
    assert.ok(cN && cS, 'both cursor rows captured');
    assert.equal(cN.sessionId, 'cur-sess-9');
    assert.equal(cN.input_tokens, 40); assert.equal(cN.output_tokens, 12);
    assert.equal(cS.input_tokens, 40); assert.equal(cS.output_tokens, 12);
  });
});

test('codex (/v1/responses) — previous_response_id threading + usage over real HTTP (stream + non-stream)', async () => {
  await withServer(async ({ call, readRows }) => {
    const hdr = { 'user-agent': 'codex_cli/1.0' };
    const n = await call({ path: '/v1/responses', headers: hdr, body: { model: 'gpt-5-codex', input: 'hi', previous_response_id: 'resp_prev_codex' } });
    const s = await call({ path: '/v1/responses', headers: hdr, body: { model: 'gpt-5-codex', stream: true, input: 'hi', previous_response_id: 'resp_prev_codex' } });
    assert.equal(n.status, 200); assert.equal(s.status, 200);
    const rows = await readRows();
    const cN = rows.find((r) => r.client === 'codex' && !r.isStream);
    const cS = rows.find((r) => r.client === 'codex' && r.isStream);
    assert.ok(cN && cS, 'both codex rows captured');
    assert.equal(cN.path, '/v1/responses');                 // real codex route, not /v1/messages
    assert.equal(cN.previousResponseId, 'resp_prev_codex'); // chains to the prior codex turn
    assert.equal(cN.responseId, 'resp_live123');
    assert.equal(cN.input_tokens, 33); assert.equal(cN.output_tokens, 7);
    assert.equal(cN.finishReason, 'completed');             // Responses status -> finishReason
    assert.equal(cS.previousResponseId, 'resp_prev_codex');
    assert.equal(cS.responseId, 'resp_live123');            // from response.completed SSE
    assert.equal(cS.input_tokens, 33); assert.equal(cS.output_tokens, 7);
  });
});
