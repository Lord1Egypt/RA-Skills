'use strict';

// Direct tests for EvoMapProxy._proxyGemini against a real local upstream (mirrors proxyOpenAIResponses.test.js).
// Guards the stream-detection contract: `:streamGenerateContent` is a STREAM even when the upstream serves it as
// application/json (Google's default array-stream, no ?alt=sse) — it must be forwarded as a live stream, never
// buffered + JSON.parsed into an {error} wrapper. Also checks x-goog-api-key injection + non-stream parsing.

const { describe, it, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');

const { EvoMapProxy } = require('../src/proxy');

function startStub(handler) {
  return new Promise((resolve) => {
    const server = http.createServer(handler);
    server.listen(0, '127.0.0.1', () => resolve({ server, baseUrl: `http://127.0.0.1:${server.address().port}` }));
  });
}

describe('EvoMapProxy._proxyGemini', () => {
  let stub, proxy, captured;
  let saved;

  before(async () => {
    captured = [];
    saved = { g: process.env.EVOMAP_GEMINI_API_KEY, gg: process.env.GEMINI_API_KEY, go: process.env.GOOGLE_API_KEY };
    stub = await startStub((req, res) => {
      const chunks = [];
      req.on('data', (c) => chunks.push(c));
      req.on('end', () => {
        captured.push({ url: req.url, headers: req.headers });
        if (req.url.includes(':streamGenerateContent')) {
          // Default array-stream: application/json + a chunked body (NOT text/event-stream).
          res.writeHead(200, { 'content-type': 'application/json' });
          res.write('[{"candidates":[{"content":{"parts":[{"text":"hi"}]}}]}\r\n');
          res.end(',{"candidates":[{"finishReason":"STOP"}],"usageMetadata":{"promptTokenCount":5,"candidatesTokenCount":2}}\r\n]');
          return;
        }
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ candidates: [{ finishReason: 'STOP' }], usageMetadata: { promptTokenCount: 5, candidatesTokenCount: 2 } }));
      });
    });
    proxy = new EvoMapProxy({ geminiBaseUrl: stub.baseUrl, logger: { log() {}, warn() {}, error() {} } });
  });

  after(async () => {
    await new Promise((r) => stub.server.close(r));
    for (const [k, env] of [['g', 'EVOMAP_GEMINI_API_KEY'], ['gg', 'GEMINI_API_KEY'], ['go', 'GOOGLE_API_KEY']]) {
      if (saved[k] === undefined) delete process.env[env]; else process.env[env] = saved[k];
    }
  });

  beforeEach(() => {
    captured.length = 0;
    delete process.env.EVOMAP_GEMINI_API_KEY; delete process.env.GEMINI_API_KEY; delete process.env.GOOGLE_API_KEY;
    process.env.EVOMAP_GEMINI_API_KEY = 'gk-upstream';
  });

  it('treats :streamGenerateContent as a STREAM even when served application/json (default array-stream)', async () => {
    const res = await proxy._proxyGemini('/v1beta/models/gemini-2.0-flash:streamGenerateContent', { contents: [] }, { inboundHeaders: {} });
    assert.equal(res.status, 200);
    assert.ok(res.stream, 'must expose a live stream, not buffer it');
    assert.equal(res.text, null, 'must NOT buffer-and-parse the array-stream');
    assert.equal(res.json, null);
  });

  it('treats :generateContent (application/json) as non-stream and parses the body', async () => {
    const res = await proxy._proxyGemini('/v1beta/models/gemini-2.0-flash:generateContent', { contents: [] }, { inboundHeaders: {} });
    assert.equal(res.status, 200);
    assert.equal(res.stream, null);
    const body = await res.json();
    assert.equal(body.candidates[0].finishReason, 'STOP');
    assert.equal(body.usageMetadata.promptTokenCount, 5);
  });

  it('injects the upstream x-goog-api-key (proxy-mediated, never trusts inbound)', async () => {
    await proxy._proxyGemini('/v1beta/models/gemini-2.0-flash:generateContent', { contents: [] }, {
      inboundHeaders: { 'x-goog-api-key': 'client-should-be-ignored', authorization: 'Bearer proxy-token' },
    });
    assert.equal(captured[0].headers['x-goog-api-key'], 'gk-upstream');
    assert.equal(captured[0].headers.authorization, undefined); // proxy auth header dropped
  });

  it('401s when no upstream Gemini key is configured', async () => {
    delete process.env.EVOMAP_GEMINI_API_KEY;
    await assert.rejects(
      () => proxy._proxyGemini('/v1beta/models/gemini-2.0-flash:generateContent', { contents: [] }, { inboundHeaders: {} }),
      (e) => e.statusCode === 401,
    );
  });
});
