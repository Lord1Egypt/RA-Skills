'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { MailboxStore } = require('../src/proxy/mailbox/store');
const { OutboundSync } = require('../src/proxy/sync/outbound');
const hubFetchMod = require('../src/gep/hubFetch');

function tmpDataDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'proxy-outbound-sync-'));
}

function readMessagesJsonl(dataDir) {
  return fs.readFileSync(path.join(dataDir, 'messages.jsonl'), 'utf8');
}

function jsonResponse(body, status = 200) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

function encryptedTrace(ciphertext) {
  return {
    encrypted: true,
    algorithm: 'aes-256-gcm',
    payload_schema: 'prism_trace_row',
    iv: 'aXYxMjM0NTY3ODkw',
    tag: 'dGFnMTIzNDU2Nzg5MA==',
    ciphertext,
  };
}

describe('proxy trace outbound sync', () => {
  let savedOutboundMaxBytes;

  beforeEach(() => {
    savedOutboundMaxBytes = process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES;
    delete process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES;
  });

  afterEach(() => {
    hubFetchMod._setFetchImplForTest(null);
    if (savedOutboundMaxBytes === undefined) delete process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES;
    else process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES = savedOutboundMaxBytes;
  });

  it('uploads pending proxy_trace messages to the Hub mailbox endpoint', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    const requests = [];
    store.setState('node_id', 'node_test_trace_upload');
    const created = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        trace: encryptedTrace('Y2lwaGVydGV4dC1mb3ItdGVzdA=='),
      },
    });

    hubFetchMod._setFetchImplForTest(async (url, opts) => {
      requests.push({
        url,
        method: opts.method,
        headers: opts.headers,
        body: JSON.parse(opts.body),
      });
      return jsonResponse({
        results: [{ id: created.message_id, status: 'accepted' }],
      });
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 1);
      assert.equal(result.synced, 1);
      assert.equal(requests.length, 1);
      const outboundUrl = new URL(requests[0].url);
      assert.equal(outboundUrl.origin + outboundUrl.pathname, 'https://hub.example.test/a2a/mailbox/outbound');
      assert.equal(outboundUrl.searchParams.get('sender_id'), 'node_test_trace_upload');
      assert.equal(requests[0].method, 'POST');
      assert.equal(requests[0].body.sender_id, 'node_test_trace_upload');
      assert.equal(requests[0].body.messages.length, 1);
      assert.equal(requests[0].body.messages[0].id, created.message_id);
      assert.equal(requests[0].body.messages[0].type, 'proxy_trace');
      assert.equal(requests[0].body.messages[0].priority, 'low');
      assert.equal(requests[0].body.messages[0].payload.schema, 'prism_trace_row.v1');
      assert.equal(requests[0].body.messages[0].payload.encrypted, true);
      assert.equal(requests[0].body.messages[0].payload.trace.encrypted, true);
      assert.equal(store.getById(created.message_id).status, 'synced');
      assert.equal(store.countPending({ direction: 'outbound' }), 0);
      assert.match(store.getState('last_sync_at'), /^\d{4}-\d{2}-\d{2}T/);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('drops pending proxy_trace messages when trace upload is disabled before flush', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    const requests = [];
    store.setState('node_id', 'node_test_trace_disabled');
    store.setState('trace_collection_enabled', false);
    const trace = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        trace: encryptedTrace('ZHJvcC1tZQ=='),
      },
    });
    const asset = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { type: 'Gene', summary: 'still send non-trace' },
    });

    hubFetchMod._setFetchImplForTest(async (url, opts) => {
      requests.push({
        url,
        body: JSON.parse(opts.body),
      });
      return jsonResponse({
        results: [{ id: asset.message_id, status: 'accepted' }],
      });
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 1);
      assert.equal(result.synced, 1);
      assert.equal(result.dropped, 1);
      assert.equal(requests.length, 1);
      assert.equal(requests[0].body.messages.length, 1);
      assert.equal(requests[0].body.messages[0].id, asset.message_id);
      assert.equal(requests[0].body.messages[0].type, 'asset_submit');
      assert.equal(store.getById(trace.message_id).status, 'rejected');
      assert.equal(store.getById(trace.message_id).error, 'proxy trace upload disabled');
      assert.equal(store.getById(asset.message_id).status, 'synced');
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('rejects unsafe pending proxy_trace payloads before outbound upload', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    store.setState('node_id', 'node_test_trace_payload_reject');
    const trace = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        trace: {
          ...encryptedTrace('ZmFrZS1lbmNyeXB0ZWQ='),
          requestBody: 'plaintext should not leave pending mailbox',
        },
      },
    });

    hubFetchMod._setFetchImplForTest(async () => {
      throw new Error('unsafe proxy_trace should not be sent');
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 0);
      assert.equal(result.dropped, 1);
      assert.equal(store.getById(trace.message_id).status, 'rejected');
      assert.equal(store.getById(trace.message_id).error, 'proxy trace payload rejected');
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('rejects secret_version-only encrypted proxy_trace payloads before outbound upload by default', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    store.setState('node_id', 'node_test_trace_secret_version_reject');
    const trace = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        node_secret_version: 7,
        trace: {
          ...encryptedTrace('ZmFrZS1lbmNyeXB0ZWQ='),
          secret_version: 7,
        },
      },
    });

    hubFetchMod._setFetchImplForTest(async () => {
      throw new Error('secret_version-only proxy_trace should not be sent');
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 0);
      assert.equal(result.dropped, 1);
      assert.equal(store.getById(trace.message_id).status, 'rejected');
      assert.equal(store.getById(trace.message_id).error, 'proxy trace payload rejected');
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('rejects encrypted proxy_trace payloads with plaintext outside the envelope', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    store.setState('node_id', 'node_test_trace_wrapper_reject');
    const topLevel = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        trace: encryptedTrace('dG9wLWxldmVs'),
        requestBody: 'top-level plaintext should not leave pending mailbox',
      },
    });
    const nested = store.send({
      type: 'proxy_trace',
      priority: 'low',
      payload: {
        schema: 'prism_trace_row.v1',
        encrypted: true,
        trace: {
          ...encryptedTrace('bmVzdGVk'),
          hub_key_envelope: {
            requestBody: 'nested plaintext should not leave pending mailbox',
          },
        },
      },
    });

    hubFetchMod._setFetchImplForTest(async () => {
      throw new Error('unsafe proxy_trace should not be sent');
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 0);
      assert.equal(result.dropped, 2);
      assert.equal(store.getById(topLevel.message_id).status, 'rejected');
      assert.equal(store.getById(nested.message_id).status, 'rejected');
      assert.equal(store.getById(topLevel.message_id).error, 'proxy trace payload rejected');
      assert.equal(store.getById(nested.message_id).error, 'proxy trace payload rejected');
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('splits outbound flush batches by serialized request body size before calling Hub', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    const requests = [];
    store.setState('node_id', 'node_test_body_budget');
    process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES = '900';
    const first = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'a'.repeat(200) },
    });
    const second = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'b'.repeat(200) },
    });
    store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'c'.repeat(200) },
    });

    hubFetchMod._setFetchImplForTest(async (url, opts) => {
      const body = JSON.parse(opts.body);
      requests.push(body);
      return jsonResponse({
        results: body.messages.map((m) => ({ id: m.id, status: 'accepted' })),
      });
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 2);
      assert.equal(result.synced, 2);
      assert.equal(requests.length, 1);
      assert.deepEqual(requests[0].messages.map((m) => m.id), [first.message_id, second.message_id]);
      assert.equal(store.countPending({ direction: 'outbound' }), 1);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('rejects a single outbound message that cannot fit under the body budget', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    store.setState('node_id', 'node_test_single_too_large');
    process.env.EVOMAP_OUTBOUND_SYNC_MAX_BODY_BYTES = '512';
    const created = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'x'.repeat(2000) },
    });

    hubFetchMod._setFetchImplForTest(async () => {
      throw new Error('oversized single message should not be sent');
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.sent, 0);
      assert.equal(result.dropped, 1);
      assert.equal(store.getById(created.message_id).status, 'rejected');
      assert.match(store.getById(created.message_id).error, /exceeds max body bytes/);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('quarantines a single message when Hub still returns 413', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    const fakeToken = 'fake-token-413-abcdefghijklmnopqrstuvwxyz';
    store.setState('node_id', 'node_test_hub_413_single');
    const created = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'hub says too large' },
    });

    hubFetchMod._setFetchImplForTest(async () => jsonResponse({
      error: 'entity too large',
      token: fakeToken,
      authorization: `Bearer ${fakeToken}`,
    }, 413));

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.payloadTooLarge, true);
      assert.equal(result.error, 'hub_payload_too_large');
      assert.equal(result.dropped, 1);
      assert.equal(store.getById(created.message_id).status, 'rejected');
      assert.match(store.getById(created.message_id).error, /Hub 413 outbound payload too large/);
      assert.doesNotMatch(store.getById(created.message_id).error, new RegExp(fakeToken));
      assert.doesNotMatch(readMessagesJsonl(dataDir), new RegExp(fakeToken));
      assert.doesNotMatch(result.error, new RegExp(fakeToken));
      assert.equal(store.countPending({ direction: 'outbound' }), 0);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('sanitizes Hub non-2xx response text before retry persistence and logs', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    const errors = [];
    const fakeToken = 'fake-token-retry-abcdefghijklmnopqrstuvwxyz';
    store.setState('node_id', 'node_test_hub_retry_sanitize');
    const created = store.send({
      type: 'asset_submit',
      priority: 'normal',
      payload: { summary: 'retry without leaking hub response body token' },
    });

    hubFetchMod._setFetchImplForTest(async () => jsonResponse({
      error: 'temporary hub failure',
      token: fakeToken,
      authorization: `Bearer ${fakeToken}`,
    }, 500));

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: (msg) => errors.push(String(msg)), warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();
      const persisted = store.getById(created.message_id);
      const messagesJsonl = readMessagesJsonl(dataDir);
      const loggerOutput = errors.join('\n');

      assert.equal(result.sent, 0);
      assert.equal(persisted.status, 'pending');
      assert.equal(persisted.retry_count, 1);
      assert.match(persisted.error, /Hub returned 500/);
      assert.match(loggerOutput, /Hub returned 500/);
      assert.doesNotMatch(persisted.error, new RegExp(fakeToken));
      assert.doesNotMatch(messagesJsonl, new RegExp(fakeToken));
      assert.doesNotMatch(loggerOutput, new RegExp(fakeToken));
      assert.doesNotMatch(result.error, new RegExp(fakeToken));
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

  it('backs down the outbound batch budget when Hub returns 413 for multiple messages', async () => {
    const dataDir = tmpDataDir();
    const store = new MailboxStore(dataDir);
    let calls = 0;
    store.setState('node_id', 'node_test_hub_413_batch');
    store.send({ type: 'asset_submit', payload: { summary: 'a'.repeat(1000) } });
    store.send({ type: 'asset_submit', payload: { summary: 'b'.repeat(1000) } });

    hubFetchMod._setFetchImplForTest(async () => {
      calls++;
      return jsonResponse({ error: 'entity too large' }, 413);
    });

    try {
      const sync = new OutboundSync({
        store,
        hubUrl: 'https://hub.example.test',
        getHeaders: () => ({ Authorization: 'Bearer test' }),
        logger: { error: () => {}, warn: () => {}, log: () => {} },
      });

      const result = await sync.flush();

      assert.equal(result.payloadTooLarge, true);
      assert.equal(result.error, 'hub_payload_too_large');
      assert.equal(calls, 1);
      assert.equal(store.countPending({ direction: 'outbound' }), 2);
      assert.ok(Number(store.getState('outbound_sync_max_body_bytes')) > 0);
    } finally {
      store.close();
      try { fs.rmSync(dataDir, { recursive: true }); } catch {}
    }
  });

});
