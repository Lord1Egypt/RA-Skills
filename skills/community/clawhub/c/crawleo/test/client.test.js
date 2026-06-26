import assert from 'node:assert/strict';
import test from 'node:test';

import { CrawleoError, CRAWLEO_ERROR_CODES, buildCrawleoUrl, createCrawleoClient } from '../src/index.js';

function jsonResponse(body, init = {}) {
  return {
    ok: init.ok ?? true,
    status: init.status ?? 200,
    headers: new Map([['content-type', 'application/json']]),
    async text() {
      return JSON.stringify(body);
    }
  };
}

test('buildCrawleoUrl constructs Crawleo URLs and comma-encodes array values', () => {
  const url = buildCrawleoUrl('https://api.crawleo.dev/', '/crawl', {
    urls: ['https://example.com/a', 'https://example.com/b'],
    markdown: true,
    empty: null
  });

  assert.equal(url.toString(), 'https://api.crawleo.dev/crawl?urls=https%3A%2F%2Fexample.com%2Fa%2Chttps%3A%2F%2Fexample.com%2Fb&markdown=true');
});

test('client request injects x-api-key and returns parsed JSON through an injected fetch', async () => {
  const calls = [];
  const client = createCrawleoClient({
    apiKey: 'secret-test-key',
    fetch: async (url, init) => {
      calls.push({ url, init });
      return jsonResponse({ ok: true, query: 'ai agents' });
    }
  });

  const result = await client.request('/search', { query: 'ai agents', max_pages: 1 });

  assert.deepEqual(result, { ok: true, query: 'ai agents' });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url.toString(), 'https://api.crawleo.dev/search?query=ai+agents&max_pages=1');
  assert.equal(calls[0].init.method, 'GET');
  assert.equal(calls[0].init.headers['x-api-key'], 'secret-test-key');
  assert.equal(calls[0].init.headers.accept, 'application/json');
});

test('client request reports missing API key as a structured CrawleoError', async () => {
  const client = createCrawleoClient({ apiKey: '', fetch: async () => jsonResponse({}) });

  await assert.rejects(
    () => client.request('/search', { query: 'ai agents' }),
    (error) => {
      assert.ok(error instanceof CrawleoError);
      assert.equal(error.code, CRAWLEO_ERROR_CODES.MISSING_API_KEY);
      assert.equal(error.endpoint, '/search');
      assert.deepEqual(error.toJSON(), {
        name: 'CrawleoError',
        code: CRAWLEO_ERROR_CODES.MISSING_API_KEY,
        message: 'CRAWLEO_API_KEY is required for live Crawleo REST calls.',
        endpoint: '/search',
        status: undefined,
        field: undefined,
        details: undefined
      });
      return true;
    }
  );
});

test('transport failures are redacted before serialization', async () => {
  const apiKey = 'secret-transport-key';
  const client = createCrawleoClient({
    apiKey,
    fetch: async () => {
      throw new Error(`network failed with apiKey=${apiKey}`);
    }
  });

  await assert.rejects(
    () => client.request('/search', { query: 'ai agents' }),
    (error) => {
      const serialized = JSON.stringify(error);
      assert.ok(error instanceof CrawleoError);
      assert.equal(error.code, CRAWLEO_ERROR_CODES.TRANSPORT);
      assert.equal(error.endpoint, '/search');
      assert.equal(serialized.includes(apiKey), false);
      assert.match(serialized, /\[REDACTED\]/);
      return true;
    }
  );
});

test('unknown endpoint paths are validation errors', async () => {
  const client = createCrawleoClient({ apiKey: 'secret-test-key', fetch: async () => jsonResponse({}) });

  await assert.rejects(
    () => client.request('/not-crawleo', {}),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.VALIDATION);
      assert.equal(error.field, 'endpointPath');
      return true;
    }
  );
});
