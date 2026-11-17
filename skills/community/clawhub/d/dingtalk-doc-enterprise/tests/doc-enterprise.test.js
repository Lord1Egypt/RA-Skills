'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const client = require('../doc-enterprise');
const originalFetch = global.fetch;

function mockResponse(data, options = {}) {
  return {
    ok: options.ok ?? true,
    status: options.status ?? 200,
    async text() {
      return data === undefined ? '' : JSON.stringify(data);
    }
  };
}

test.afterEach(() => {
  delete process.env.DINGTALK_CLIENTID;
  delete process.env.DINGTALK_CLIENTSECRET;
  delete process.env.OPENCLAW_SENDER_ID;
  delete process.env.DINGTALK_SENDER_ID;
  delete process.env.DINGTALK_OPERATOR_ID;
  delete process.env.DINGTALK_DEBUG;
  global.fetch = originalFetch;
});

test('command whitelist exposes existing-document operations only', () => {
  assert.deepEqual(Object.keys(client.COMMAND_HANDLERS).sort(), [
    'blocks', 'delete', 'insert', 'modify', 'read', 'update'
  ]);
  assert.equal(client.COMMAND_HANDLERS.create, undefined);
  assert.equal(client.COMMAND_HANDLERS['create-doc'], undefined);
  assert.equal(client.COMMAND_HANDLERS['append-text'], undefined);
  assert.equal(client.callAPI, undefined);
  assert.rejects(() => client.runCommand('create', []), /未知或不允许/);
});

test('OpenClaw frontmatter uses single-line metadata and valid core fields', () => {
  const skillPath = path.join(__dirname, '..', 'SKILL.md');
  const lines = fs.readFileSync(skillPath, 'utf8').split(/\r?\n/);
  assert.equal(lines[0], '---');
  assert.match(lines[1], /^name: [a-z0-9-]+$/);
  assert.match(lines[2], /^description: .{1,1024}$/u);
  assert.match(lines[3], /^metadata: \{.*\}$/);
  assert.doesNotThrow(() => JSON.parse(lines[3].slice('metadata: '.length)));
  assert.equal(lines[4], '---');
});

test('extractDocId accepts DingTalk URL and rejects unknown URL', () => {
  assert.equal(
    client.extractDocId('https://alidocs.dingtalk.com/i/nodes/Abc_123-x?utm_scene=person_space'),
    'Abc_123-x'
  );
  assert.equal(client.extractDocId('alidocs.dingtalk.com/i/nodes/Abc123'), 'Abc123');
  assert.throws(() => client.extractDocId('https://example.com/document/123'), /只允许/);
  assert.throws(() => client.extractDocId('https://example.com/i/nodes/Abc123'), /只允许/);
});

test('all commands validate the document URL before credentials and identity', async () => {
  let fetchCalls = 0;
  global.fetch = async () => {
    fetchCalls += 1;
    throw new Error('network must not be called for an invalid URL');
  };

  const invalidUrl = 'https://example.com/i/nodes/abc';
  const cases = [
    ['read', [invalidUrl]],
    ['blocks', [invalidUrl]],
    ['insert', [invalidUrl, '0', 'text']],
    ['modify', [invalidUrl, 'block1', 'text']],
    ['delete', [invalidUrl, 'block1']],
    ['update', [invalidUrl, '# content']]
  ];

  for (const [command, args] of cases) {
    await assert.rejects(() => client.runCommand(command, args), /只允许 alidocs\.dingtalk\.com/);
  }
  assert.equal(fetchCalls, 0);
});

test('sender identity takes precedence over local operator fallback', async () => {
  process.env.DINGTALK_CLIENTID = 'app-key';
  process.env.DINGTALK_CLIENTSECRET = 'app-secret';
  process.env.OPENCLAW_SENDER_ID = 'sender-123';
  process.env.DINGTALK_OPERATOR_ID = 'local-operator';
  const requests = [];
  global.fetch = async (url, options) => {
    requests.push({ url, options });
    if (url.includes('/oauth2/accessToken')) return mockResponse({ accessToken: 'token-123' });
    if (url.includes('oapi.dingtalk.com/user/get')) return mockResponse({ errcode: 0, unionid: 'sender-union-id' });
    throw new Error(`unexpected URL: ${url}`);
  };

  assert.equal(await client.getCurrentOperatorId(), 'sender-union-id');
  assert.equal(requests.length, 2);
  assert.match(requests[1].url, /userid=sender-123/);
});

test('insert preserves position zero and never calls a document creation endpoint', async () => {
  let request;
  global.fetch = async (url, options) => {
    request = { url, options };
    return mockResponse({ success: true });
  };

  await client.insertBlock('https://alidocs.dingtalk.com/i/nodes/doc123', 'first', 0, 'operator', 'token');
  assert.match(request.url, /\/v1\.0\/doc\/suites\/documents\/doc123\/blocks\?operatorId=operator$/);
  assert.deepEqual(JSON.parse(request.options.body), {
    element: { blockType: 'paragraph', paragraph: { text: 'first' } },
    position: 0
  });
  assert.doesNotMatch(request.url, /\/workspaces\/[^/]+\/docs(?:\?|$)/);
});

test('modify and delete target content blocks on an existing document', async () => {
  const requests = [];
  global.fetch = async (url, options) => {
    requests.push({ url, options });
    return mockResponse(undefined);
  };

  await client.modifyBlock('doc123', 'block456', 'replacement', 'operator', 'token');
  await client.deleteBlock('doc123', 'block456', 'operator', 'token');

  assert.equal(requests[0].options.method, 'PUT');
  assert.match(requests[0].url, /\/documents\/doc123\/blocks\/block456\?/);
  assert.deepEqual(JSON.parse(requests[0].options.body), {
    element: { blockType: 'paragraph', paragraph: { text: 'replacement' } }
  });
  assert.equal(requests[1].options.method, 'DELETE');
  assert.match(requests[1].url, /\/documents\/doc123\/blocks\/block456\?/);
});

test('extractBlocks supports response shapes observed by both skills', () => {
  assert.deepEqual(client.extractBlocks({ blocks: [{ blockId: 'a' }] }), [{ blockId: 'a' }]);
  assert.deepEqual(client.extractBlocks({ result: { data: [{ id: 'b' }] } }), [{ id: 'b' }]);
  assert.deepEqual(client.extractBlocks({ data: { result: { data: [{ id: 'c' }] } } }), [{ id: 'c' }]);
});
