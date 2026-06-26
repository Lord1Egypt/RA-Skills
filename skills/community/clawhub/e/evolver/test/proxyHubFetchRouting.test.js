'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');

function jsonResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

function loadProxyWithHubFetch(hubFetchImpl) {
  const hubFetchPath = require.resolve('../src/gep/hubFetch');
  const proxyPath = require.resolve('../src/proxy/index.js');
  const oldHubFetch = require.cache[hubFetchPath];
  const oldProxy = require.cache[proxyPath];

  delete require.cache[proxyPath];
  require.cache[hubFetchPath] = {
    id: hubFetchPath,
    filename: hubFetchPath,
    loaded: true,
    exports: { hubFetch: hubFetchImpl },
  };

  const proxyModule = require('../src/proxy/index.js');
  return {
    proxyModule,
    restore() {
      if (oldProxy) require.cache[proxyPath] = oldProxy;
      else delete require.cache[proxyPath];
      if (oldHubFetch) require.cache[hubFetchPath] = oldHubFetch;
      else delete require.cache[hubFetchPath];
    },
  };
}

test('EvoMapProxy._proxyHttp routes Hub passthrough through hubFetch', async () => {
  const calls = [];
  const { proxyModule, restore } = loadProxyWithHubFetch(async (url, opts) => {
    calls.push({ url, opts });
    return jsonResponse({ via: 'hubFetch' });
  });

  try {
    const proxy = new proxyModule.EvoMapProxy({ hubUrl: 'https://hub.example.com' });
    proxy.lifecycle = {
      _buildHeaders: () => ({ authorization: 'Bearer test-secret' }),
      reAuthenticate: async () => false,
    };

    const result = await proxy._proxyHttp('/a2a/assets/search', null, {
      method: 'GET',
      query: { signals: 'cloudflare_block', limit: 1 },
    });

    assert.deepEqual(result, { via: 'hubFetch' });
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, 'https://hub.example.com/a2a/assets/search?signals=cloudflare_block&limit=1');
    assert.equal(calls[0].opts.method, 'GET');
    assert.deepEqual(calls[0].opts.headers, { authorization: 'Bearer test-secret' });
    assert.equal('body' in calls[0].opts, false);
  } finally {
    restore();
  }
});

test('EvoMapProxy._proxyHttp retries auth failures through hubFetch', async () => {
  const calls = [];
  const { proxyModule, restore } = loadProxyWithHubFetch(async (url, opts) => {
    calls.push({ url, opts });
    return calls.length === 1
      ? jsonResponse({ error: 'node_secret_required' }, 401)
      : jsonResponse({ ok: true });
  });

  try {
    let reauthCalls = 0;
    const proxy = new proxyModule.EvoMapProxy({ hubUrl: 'https://hub.example.com' });
    proxy.lifecycle = {
      _buildHeaders: () => ({ authorization: 'Bearer refreshed-secret' }),
      reAuthenticate: async () => { reauthCalls += 1; return true; },
    };

    const result = await proxy._proxyHttp('/a2a/fetch', { search_only: true });

    assert.deepEqual(result, { ok: true });
    assert.equal(reauthCalls, 1);
    assert.equal(calls.length, 2);
    assert.equal(calls[0].url, 'https://hub.example.com/a2a/fetch');
    assert.equal(calls[1].url, 'https://hub.example.com/a2a/fetch');
  } finally {
    restore();
  }
});

test('EvoMapProxy._getHubMailboxStatus also uses hubFetch', async () => {
  const calls = [];
  const { proxyModule, restore } = loadProxyWithHubFetch(async (url, opts) => {
    calls.push({ url, opts });
    return jsonResponse({ synced: true });
  });

  try {
    const proxy = new proxyModule.EvoMapProxy({ hubUrl: 'https://hub.example.com' });
    proxy.lifecycle = {
      nodeId: 'node_test',
      _buildHeaders: () => ({ authorization: 'Bearer test-secret' }),
    };

    const result = await proxy._getHubMailboxStatus();

    assert.deepEqual(result, { synced: true });
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, 'https://hub.example.com/a2a/mailbox/status?node_id=node_test');
    assert.equal(calls[0].opts.method, 'GET');
  } finally {
    restore();
  }
});
