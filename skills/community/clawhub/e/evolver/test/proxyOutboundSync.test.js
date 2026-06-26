'use strict';

const { describe, it, afterEach } = require('node:test');
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
  afterEach(() => {
    hubFetchMod._setFetchImplForTest(null);
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
      assert.equal(requests[0].url, 'https://hub.example.test/a2a/mailbox/outbound');
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
});
