'use strict';

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert/strict');

const { EvoMapProxy } = require('../src/proxy');

// Mock the @aws-sdk/client-bedrock-runtime surface that _proxyBedrock
// uses. We inject this via proxy._bedrockSdk so the real SDK never
// loads — keeps the test hermetic and avoids constructing AWS
// event-stream binary fixtures (which require internal smithy modules
// that are deep transitive deps).
function makeMockSdk(handlers) {
  let lastClientArgs = null;
  let lastCommand = null;

  class MockBedrockRuntimeClient {
    constructor(args) { lastClientArgs = args; }
    async send(command) {
      lastCommand = command;
      const isStream = command instanceof MockInvokeModelWithResponseStreamCommand;
      return isStream
        ? handlers.stream(command.input)
        : handlers.invoke(command.input);
    }
  }
  class MockInvokeModelCommand { constructor(input) { this.input = input; } }
  class MockInvokeModelWithResponseStreamCommand { constructor(input) { this.input = input; } }

  return {
    sdk: {
      BedrockRuntimeClient: MockBedrockRuntimeClient,
      InvokeModelCommand: MockInvokeModelCommand,
      InvokeModelWithResponseStreamCommand: MockInvokeModelWithResponseStreamCommand,
    },
    inspect: () => ({ lastClientArgs, lastCommand }),
  };
}

async function readSseStream(stream) {
  const reader = stream.getReader();
  const dec = new TextDecoder();
  let out = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    out += dec.decode(value);
  }
  return out;
}

describe('EvoMapProxy._proxyBedrock', () => {
  let proxy;

  before(() => {
    proxy = new EvoMapProxy({
      logger: { log: () => {}, error: () => {}, warn: () => {} },
    });
  });

  it('non-stream: rewrites body, strips model, injects anthropic_version, returns Anthropic-shaped JSON', async () => {
    const mock = makeMockSdk({
      invoke: () => ({
        body: Buffer.from(JSON.stringify({ id: 'msg_1', content: [{ type: 'text', text: 'hi' }] })),
      }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      max_tokens: 16,
    }, {
      bedrockRegion: 'us-east-1',
      bedrockCredentials: { accessKeyId: 'test', secretAccessKey: 'test' },
    });

    assert.equal(result.status, 200);
    assert.equal(result.headers['content-type'], 'application/json');
    assert.equal(result.stream, null);
    const json = result.json();
    assert.equal(json.id, 'msg_1');
    assert.equal(json.content[0].text, 'hi');

    const { lastCommand } = mock.inspect();
    assert.equal(lastCommand.input.modelId, 'anthropic.claude-3-5-haiku-20241022-v1:0');
    const sentBody = JSON.parse(lastCommand.input.body);
    assert.equal(sentBody.model, undefined, 'top-level model must be stripped (Bedrock 400s on unknown fields)');
    assert.equal(sentBody.anthropic_version, 'bedrock-2023-05-31');
    assert.deepEqual(sentBody.messages, [{ role: 'user', content: 'hi' }]);
    assert.equal(sentBody.max_tokens, 16);
  });

  it('normalizes Claude Code bare model aliases before sending to Bedrock', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;

    await proxy._proxyBedrock('/v1/messages', {
      model: 'claude-haiku-4-5-20251001',
      messages: [{ role: 'user', content: 'hi' }],
      max_tokens: 16,
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    assert.equal(
      mock.inspect().lastCommand.input.modelId,
      'global.anthropic.claude-haiku-4-5-20251001-v1:0'
    );
  });

  it('non-stream: missing body.model returns 400 Anthropic-shaped error', async () => {
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw new Error('should not be called'); },
      stream: () => { throw new Error('should not be called'); },
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      messages: [{ role: 'user', content: 'hi' }],
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    assert.equal(result.status, 400);
    const json = result.json();
    assert.equal(json.type, 'error');
    assert.match(json.error.message, /model required/i);
  });

  it('streaming: re-emits Bedrock chunks as standard SSE data: ... \\n\\n', async () => {
    const chunks = [
      { type: 'message_start', message: { id: 'msg_1' } },
      { type: 'content_block_delta', delta: { type: 'text_delta', text: 'hi' } },
      { type: 'message_stop' },
    ];
    async function* fakeStream() {
      for (const c of chunks) {
        yield { chunk: { bytes: Buffer.from(JSON.stringify(c)) } };
      }
    }
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw new Error('should not be called'); },
      stream: () => ({ body: fakeStream() }),
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    assert.equal(result.status, 200);
    assert.equal(result.headers['content-type'], 'text/event-stream');
    assert.notEqual(result.stream, null);

    const sse = await readSseStream(result.stream);
    // Each chunk must become exactly one `data: <json>\n\n` frame.
    assert.match(sse, /^data: \{"type":"message_start"/m);
    assert.match(sse, /data: \{"type":"content_block_delta".*"text":"hi"/);
    assert.match(sse, /data: \{"type":"message_stop"\}\n\n$/);
    // Three chunks -> three frames -> three `\n\n` separators.
    const frameSeparators = sse.split('\n\n').length - 1;
    assert.equal(frameSeparators, 3);
  });

  it('streaming: error events become Anthropic-shaped error frames', async () => {
    async function* fakeStream() {
      yield { chunk: { bytes: Buffer.from(JSON.stringify({ type: 'message_start' })) } };
      yield { throttlingException: { name: 'ThrottlingException', message: 'slow down' } };
    }
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw new Error('should not be called'); },
      stream: () => ({ body: fakeStream() }),
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sse = await readSseStream(result.stream);
    assert.match(sse, /event: error\ndata: \{"type":"error".*"ThrottlingException"/);
  });

  // Bedrock InvokeModelWithResponseStream documents six exception envelope
  // shapes; missing one silently drops the error (stream closes clean,
  // client sees a truncated response with no signal). These two had been
  // missed in the initial cut.
  for (const exKey of ['modelTimeoutException', 'serviceUnavailableException']) {
    it(`streaming: ${exKey} also surfaces as Anthropic-shaped error frame`, async () => {
      const exName = exKey === 'modelTimeoutException' ? 'ModelTimeoutException' : 'ServiceUnavailableException';
      async function* fakeStream() {
        yield { chunk: { bytes: Buffer.from(JSON.stringify({ type: 'message_start' })) } };
        yield { [exKey]: { name: exName, message: 'upstream went sideways' } };
      }
      proxy._bedrockSdk = makeMockSdk({
        invoke: () => { throw new Error('should not be called'); },
        stream: () => ({ body: fakeStream() }),
      }).sdk;

      const result = await proxy._proxyBedrock('/v1/messages', {
        model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
        messages: [{ role: 'user', content: 'hi' }],
        stream: true,
      }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

      const sse = await readSseStream(result.stream);
      assert.match(sse, new RegExp(`event: error\\ndata: \\{"type":"error".*"${exName}"`));
    });
  }

  it('error relay: SDK ServiceException becomes Anthropic-shaped error envelope with httpStatusCode', async () => {
    const err = Object.assign(new Error('access denied'), {
      name: 'AccessDeniedException',
      $metadata: { httpStatusCode: 403 },
    });
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw err; },
      stream: () => { throw new Error('should not be called'); },
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    assert.equal(result.status, 403);
    const json = result.json();
    assert.equal(json.type, 'error');
    assert.equal(json.error.type, 'AccessDeniedException');
    assert.match(json.error.message, /access denied/);
  });

  it('error with no $metadata defaults to status 500', async () => {
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw new Error('boom'); },
      stream: () => { throw new Error('should not be called'); },
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    assert.equal(result.status, 500);
  });

  it('us.* dated Bedrock IDs canonicalize to the global.* equivalent at proxy boundary', async () => {
    // PR #135 made `canonicalizeForBedrock` rewrite `us.*` → `global.*` so a
    // client carrying a regional inference profile doesn't end up pinned to
    // it. That canonicalize is now applied at the proxy boundary as well so
    // the rewrite is consistent whether or not the router-decision step is
    // enabled (defense-in-depth for EVOMAP_ROUTER_ENABLED=0 deployments).
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from(JSON.stringify({ ok: true })) }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;

    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const { lastCommand } = mock.inspect();
    assert.equal(lastCommand.input.modelId, 'global.anthropic.claude-haiku-4-5-20251001-v1:0');
  });

  it('client constructor receives region + endpoint + credentials from opts', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('nope'); },
    });
    proxy._bedrockSdk = mock.sdk;

    await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [],
    }, {
      bedrockRegion: 'us-west-2',
      bedrockEndpoint: 'http://127.0.0.1:9999',
      bedrockCredentials: { accessKeyId: 'AK', secretAccessKey: 'SK' },
    });

    const { lastClientArgs } = mock.inspect();
    assert.equal(lastClientArgs.region, 'us-west-2');
    assert.equal(lastClientArgs.endpoint, 'http://127.0.0.1:9999');
    assert.deepEqual(lastClientArgs.credentials, { accessKeyId: 'AK', secretAccessKey: 'SK' });
  });

  it('streaming: cancel() on the ReadableStream closes the upstream AsyncIterable', async () => {
    let returnCalled = false;
    const fakeStream = {
      [Symbol.asyncIterator]() {
        return {
          async next() {
            return { value: { chunk: { bytes: Buffer.from(JSON.stringify({ type: 'message_start' })) } }, done: false };
          },
          async return() { returnCalled = true; return { value: undefined, done: true }; },
        };
      },
    };
    proxy._bedrockSdk = makeMockSdk({
      invoke: () => { throw new Error('should not be called'); },
      stream: () => ({ body: fakeStream }),
    }).sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const reader = result.stream.getReader();
    await reader.read();
    await reader.cancel();
    // Give the cancel hook a tick to run.
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(returnCalled, true, 'cancel() must invoke AsyncIterator.return() to release the upstream');
  });

  it('reuses BedrockRuntimeClient across calls with the same constructor args', async () => {
    const constructed = [];
    function makeMockSdkInstrumented() {
      class MockBedrockRuntimeClient {
        constructor(args) { constructed.push(args); }
        async send() { return { body: Buffer.from('{}') }; }
      }
      class MockInvokeModelCommand { constructor(input) { this.input = input; } }
      class MockInvokeModelWithResponseStreamCommand { constructor(input) { this.input = input; } }
      return {
        BedrockRuntimeClient: MockBedrockRuntimeClient,
        InvokeModelCommand: MockInvokeModelCommand,
        InvokeModelWithResponseStreamCommand: MockInvokeModelWithResponseStreamCommand,
      };
    }
    proxy._bedrockSdk = makeMockSdkInstrumented();
    proxy._bedrockClient = null;
    proxy._bedrockClientKey = null;
    proxy._bedrockClientSdk = null;

    const opts = { bedrockRegion: 'us-east-1', bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } };
    const body = { model: 'anthropic.claude-3-5-haiku-20241022-v1:0', messages: [] };

    await proxy._proxyBedrock('/v1/messages', body, opts);
    await proxy._proxyBedrock('/v1/messages', body, opts);
    await proxy._proxyBedrock('/v1/messages', body, opts);
    assert.equal(constructed.length, 1, 'client must be reused across same-args calls');

    // Different region → new client.
    await proxy._proxyBedrock('/v1/messages', body, { ...opts, bedrockRegion: 'us-west-2' });
    assert.equal(constructed.length, 2, 'changing region must rebuild the client');
  });

  // Claude Code v2.1.150+ sends thinking:{type:'adaptive'} for Opus 4.7+;
  // Bedrock InvokeModel on the 4.5/4.1-gen profiles 400s on it. Normalize.
  it('thinking: type="adaptive" with explicit budget_tokens is folded to "enabled" preserving budget', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      max_tokens: 8192,
      messages: [{ role: 'user', content: 'hi' }],
      thinking: { type: 'adaptive', budget_tokens: 4096 },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.equal(sent.thinking.type, 'enabled');
    assert.equal(sent.thinking.budget_tokens, 4096, 'explicit budget_tokens preserved');
  });

  // CC omits budget_tokens in adaptive mode (model decides). Bedrock 'enabled'
  // requires it, so we default to max_tokens/2.
  it('thinking: type="adaptive" without budget_tokens defaults to max_tokens/2', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      max_tokens: 8192,
      messages: [{ role: 'user', content: 'hi' }],
      thinking: { type: 'adaptive' },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.equal(sent.thinking.type, 'enabled');
    assert.equal(sent.thinking.budget_tokens, 4096, 'should default to max_tokens/2');
  });

  // Anthropic: budget_tokens >= 1024. Bedrock: budget_tokens < max_tokens.
  // For max_tokens <= 1024 the constraints are incompatible — the only
  // valid action is to drop thinking entirely.
  it('thinking: adaptive with max_tokens <= 1024 folds to disabled (constraints incompatible)', async () => {
    for (const maxTokens of [256, 512, 1024]) {
      const mock = makeMockSdk({
        invoke: () => ({ body: Buffer.from('{}') }),
        stream: () => { throw new Error('should not be called'); },
      });
      proxy._bedrockSdk = mock.sdk;
      proxy._bedrockClient = null;
      await proxy._proxyBedrock('/v1/messages', {
        model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
        max_tokens: maxTokens,
        messages: [{ role: 'user', content: 'hi' }],
        thinking: { type: 'adaptive' },
      }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

      const sent = JSON.parse(mock.inspect().lastCommand.input.body);
      assert.deepEqual(sent.thinking, { type: 'disabled' }, `max_tokens=${maxTokens} should disable thinking`);
    }
  });

  // Above 1024 the 1024 floor is safe (1024 < max_tokens).
  it('thinking: adaptive with max_tokens just above 1024 keeps 1024 floor', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      max_tokens: 2000,
      messages: [{ role: 'user', content: 'hi' }],
      thinking: { type: 'adaptive' },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.equal(sent.thinking.type, 'enabled');
    assert.equal(sent.thinking.budget_tokens, 1024, 'floor 1024 < max_tokens 2000 is valid');
  });

  // Caller's explicit budget_tokens is honored even when max_tokens is small —
  // they've taken responsibility for the relationship; we don't second-guess.
  it('thinking: adaptive with explicit small budget_tokens passes through even at small max_tokens', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      max_tokens: 1024,
      messages: [{ role: 'user', content: 'hi' }],
      thinking: { type: 'adaptive', budget_tokens: 800 },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.equal(sent.thinking.type, 'enabled');
    assert.equal(sent.thinking.budget_tokens, 800);
  });

  it('thinking: adaptive and output_config pass through for Opus 4.7', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'global.anthropic.claude-opus-4-7',
      max_tokens: 8192,
      messages: [{ role: 'user', content: 'compact this session' }],
      thinking: { type: 'adaptive' },
      output_config: { effort: 'xhigh' },
      context_management: { edits: [] },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.deepEqual(sent.thinking, { type: 'adaptive' });
    assert.deepEqual(sent.output_config, { effort: 'xhigh' });
    assert.equal('context_management' in sent, false, 'context_management must still be stripped');
  });

  it('thinking: adaptive and output_config pass through for Opus 4.8', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'global.anthropic.claude-opus-4-8',
      max_tokens: 8192,
      messages: [{ role: 'user', content: 'compact this session' }],
      thinking: { type: 'adaptive' },
      output_config: { effort: 'xhigh' },
      context_management: { edits: [] },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.deepEqual(sent.thinking, { type: 'adaptive' });
    assert.deepEqual(sent.output_config, { effort: 'xhigh' });
    assert.equal('context_management' in sent, false, 'context_management must still be stripped');
  });

  // CC v2.1.150+ adds top-level fields Bedrock InvokeModel doesn't accept;
  // unknown top-level keys cause it to 400 the whole call.
  it('strips CC-specific top-level fields (output_config, context_management) before forwarding to Bedrock', async () => {
    const mock = makeMockSdk({
      invoke: () => ({ body: Buffer.from('{}') }),
      stream: () => { throw new Error('should not be called'); },
    });
    proxy._bedrockSdk = mock.sdk;
    await proxy._proxyBedrock('/v1/messages', {
      model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      output_config: { effort: 'xhigh' },
      context_management: { edits: [] },
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

    const sent = JSON.parse(mock.inspect().lastCommand.input.body);
    assert.equal('output_config' in sent, false, 'output_config must not be forwarded');
    assert.equal('context_management' in sent, false, 'context_management must not be forwarded');
  });

  it('thinking: "enabled" / "disabled" / undefined pass through untouched', async () => {
    for (const value of [{ type: 'enabled', budget_tokens: 1024 }, { type: 'disabled' }, undefined]) {
      const mock = makeMockSdk({
        invoke: () => ({ body: Buffer.from('{}') }),
        stream: () => { throw new Error('should not be called'); },
      });
      proxy._bedrockSdk = mock.sdk;
      proxy._bedrockClient = null;  // force rebuild so mock.inspect tracks this call
      await proxy._proxyBedrock('/v1/messages', {
        model: 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
        messages: [{ role: 'user', content: 'hi' }],
        ...(value ? { thinking: value } : {}),
      }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });

      const sent = JSON.parse(mock.inspect().lastCommand.input.body);
      assert.deepEqual(sent.thinking, value);
    }
  });

  it('strips body.stream before forwarding (Bedrock infers from command type)', async () => {
    const mock = makeMockSdk({
      invoke: () => { throw new Error('should not be called'); },
      stream: () => ({ body: (async function*(){ yield { chunk: { bytes: Buffer.from('{}') } }; })() }),
    });
    proxy._bedrockSdk = mock.sdk;

    const result = await proxy._proxyBedrock('/v1/messages', {
      model: 'anthropic.claude-3-5-haiku-20241022-v1:0',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
    }, { bedrockCredentials: { accessKeyId: 't', secretAccessKey: 't' } });
    // drain so the async generator is awaited
    await readSseStream(result.stream);

    const { lastCommand } = mock.inspect();
    const sent = JSON.parse(lastCommand.input.body);
    assert.equal(sent.stream, undefined, 'body.stream must be removed before forwarding');
  });
});

describe('EvoMapProxy provider dispatch via opts.upstreamMode', () => {
  const { buildMessagesHandler } = require('../src/proxy/router/messages_route');
  // Dispatch reads opts.upstreamMode (set by messages_route.js once per
  // request), NOT process.env directly — that's the whole point of the
  // single-source-of-truth fix. Both tests here exercise the dispatch
  // closure with opts.upstreamMode rather than env, mirroring how the
  // closure is actually called in production.
  function makeDispatch(proxy) {
    return (reqPath, body, opts) => {
      const mode = opts?.upstreamMode || 'anthropic';
      return mode === 'bedrock'
        ? proxy._proxyBedrock(reqPath, body, opts)
        : proxy._proxyAnthropic(reqPath, body, opts);
    };
  }

  it('opts.upstreamMode unset → _proxyAnthropic', async () => {
    const proxy = new EvoMapProxy({ logger: { log: () => {}, error: () => {}, warn: () => {} } });
    let anthropicCalled = false;
    let bedrockCalled = false;
    proxy._proxyAnthropic = async () => { anthropicCalled = true; return { status: 200, headers: {}, stream: null, json: () => ({}), text: () => '{}' }; };
    proxy._proxyBedrock = async () => { bedrockCalled = true; return { status: 200, headers: {}, stream: null, json: () => ({}), text: () => '{}' }; };

    await makeDispatch(proxy)('/v1/messages', {}, {});
    assert.equal(anthropicCalled, true);
    assert.equal(bedrockCalled, false);
  });

  it('opts.upstreamMode="bedrock" → _proxyBedrock', async () => {
    const proxy = new EvoMapProxy({ logger: { log: () => {}, error: () => {}, warn: () => {} } });
    let anthropicCalled = false;
    let bedrockCalled = false;
    proxy._proxyAnthropic = async () => { anthropicCalled = true; return { status: 200, headers: {}, stream: null, json: () => ({}), text: () => '{}' }; };
    proxy._proxyBedrock = async () => { bedrockCalled = true; return { status: 200, headers: {}, stream: null, json: () => ({}), text: () => '{}' }; };

    await makeDispatch(proxy)('/v1/messages', {}, { upstreamMode: 'bedrock' });
    assert.equal(bedrockCalled, true);
    assert.equal(anthropicCalled, false);
  });

  it('messages_route.js threads upstreamMode through to anthropicProxy', async () => {
    // End-to-end: hand the handler a mock anthropicProxy and verify that
    // when EVOMAP_UPSTREAM=bedrock the gate is skipped AND the call reaches
    // anthropicProxy with opts.upstreamMode='bedrock' (one env read, two
    // consumers). This is the regression guard for the TOCTOU bug.
    const prev = process.env.EVOMAP_UPSTREAM;
    process.env.EVOMAP_UPSTREAM = 'bedrock';
    try {
      let receivedOpts = null;
      const handler = buildMessagesHandler({
        anthropicProxy: async (_p, _b, opts) => {
          receivedOpts = opts;
          return { status: 200, headers: {}, stream: null, json: () => ({}), text: () => '{}' };
        },
        logger: { log: () => {}, warn: () => {}, error: () => {} },
        routerEnabled: false,
      });
      await handler({ body: { messages: [] }, headers: {} });
      assert.equal(receivedOpts.upstreamMode, 'bedrock');
    } finally {
      if (prev === undefined) delete process.env.EVOMAP_UPSTREAM;
      else process.env.EVOMAP_UPSTREAM = prev;
    }
  });
});

describe('messages_route auth gate softens under EVOMAP_UPSTREAM=bedrock', () => {
  const { buildMessagesHandler } = require('../src/proxy/router/messages_route');

  it('throws 401 when neither inbound x-api-key nor proxy env creds (default mode)', async () => {
    const prevMode = process.env.EVOMAP_UPSTREAM;
    const prevKey = process.env.ANTHROPIC_API_KEY;
    const prevTok = process.env.ANTHROPIC_AUTH_TOKEN;
    delete process.env.EVOMAP_UPSTREAM;
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.ANTHROPIC_AUTH_TOKEN;
    try {
      const handler = buildMessagesHandler({
        anthropicProxy: async () => { throw new Error('should not reach upstream'); },
        logger: { log: () => {}, warn: () => {}, error: () => {} },
        routerEnabled: false,
      });
      await assert.rejects(
        () => handler({ body: { messages: [] }, headers: {} }),
        (err) => err.statusCode === 401 && /x-api-key required/.test(err.message),
      );
    } finally {
      if (prevMode !== undefined) process.env.EVOMAP_UPSTREAM = prevMode;
      if (prevKey !== undefined) process.env.ANTHROPIC_API_KEY = prevKey;
      if (prevTok !== undefined) process.env.ANTHROPIC_AUTH_TOKEN = prevTok;
    }
  });

  it('skips the credential check when EVOMAP_UPSTREAM=bedrock (proxy_token gate is upstream of this handler)', async () => {
    const prevMode = process.env.EVOMAP_UPSTREAM;
    const prevKey = process.env.ANTHROPIC_API_KEY;
    const prevTok = process.env.ANTHROPIC_AUTH_TOKEN;
    process.env.EVOMAP_UPSTREAM = 'bedrock';
    delete process.env.ANTHROPIC_API_KEY;
    delete process.env.ANTHROPIC_AUTH_TOKEN;
    try {
      let called = false;
      const handler = buildMessagesHandler({
        anthropicProxy: async () => {
          called = true;
          return { status: 200, headers: {}, stream: null, json: () => ({ ok: true }), text: () => '{"ok":true}' };
        },
        logger: { log: () => {}, warn: () => {}, error: () => {} },
        routerEnabled: false,
      });
      const result = await handler({ body: { messages: [] }, headers: {} });
      assert.equal(called, true, 'handler must reach upstream without 401');
      assert.equal(result.status, 200);
    } finally {
      if (prevMode === undefined) delete process.env.EVOMAP_UPSTREAM;
      else process.env.EVOMAP_UPSTREAM = prevMode;
      if (prevKey !== undefined) process.env.ANTHROPIC_API_KEY = prevKey;
      if (prevTok !== undefined) process.env.ANTHROPIC_AUTH_TOKEN = prevTok;
    }
  });
});
