import assert from 'node:assert/strict';
import test from 'node:test';

import {
  CRAWLEO_ERROR_CODES,
  crawl,
  createCrawleoClient,
  googleMaps,
  googleSearch,
  headfulBrowser,
  search
} from '../src/index.js';

function makeClient() {
  const calls = [];
  const client = createCrawleoClient({
    apiKey: 'secret-wrapper-key',
    fetch: async (url, init) => {
      calls.push({ url, init });
      return {
        ok: true,
        status: 200,
        headers: new Map([['content-type', 'application/json']]),
        async text() {
          return JSON.stringify({ ok: true, path: new URL(url).pathname });
        }
      };
    }
  });
  return { client, calls };
}

test('client exposes methods for every documented Crawleo endpoint', async () => {
  const { client, calls } = makeClient();

  await client.search({ query: 'ai agents', device: 'desktop' });
  await client.googleSearch({ q: 'best CRM', type: 'news', tbs: 'qdr:d' });
  await client.googleMaps({ q: 'restaurants in Paris', hl: 'fr' });
  await client.crawl({ urls: ['https://example.com/a', 'https://example.com/b'], markdown: true });
  await client.headfulBrowser({ urls: 'https://example.com', output_format: 'markdown' });

  assert.deepEqual(
    calls.map((call) => new URL(call.url).pathname),
    ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser']
  );
  assert.equal(new URL(calls[3].url).searchParams.get('urls'), 'https://example.com/a,https://example.com/b');
});

test('top-level endpoint wrappers accept a client object without accepting secrets', async () => {
  const { client, calls } = makeClient();

  await search(client, { query: 'ai agents' });
  await googleSearch(client, { q: 'ai agents' });
  await googleMaps(client, { q: 'coffee near Paris' });
  await crawl(client, { urls: 'https://example.com' });
  await headfulBrowser(client, { urls: ['https://example.com'], output_format: 'page_text' });

  assert.deepEqual(
    calls.map((call) => new URL(call.url).pathname),
    ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser']
  );
});

test('wrappers reject missing required parameters with endpoint and field diagnostics', () => {
  const { client } = makeClient();

  assert.throws(
    () => client.googleSearch({ type: 'news' }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.VALIDATION);
      assert.equal(error.endpoint, '/google-search');
      assert.equal(error.field, 'q');
      return true;
    }
  );
});

test('wrappers validate only documented enum parameters', () => {
  const { client } = makeClient();

  assert.throws(
    () => client.search({ query: 'ai agents', device: 'watch' }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.VALIDATION);
      assert.equal(error.endpoint, '/search');
      assert.equal(error.field, 'device');
      assert.deepEqual(error.details.allowedValues, ['desktop', 'mobile', 'tablet']);
      return true;
    }
  );

  assert.throws(
    () => client.googleSearch({ q: 'ai agents', type: 'videos' }),
    (error) => {
      assert.equal(error.endpoint, '/google-search');
      assert.equal(error.field, 'type');
      return true;
    }
  );

  assert.throws(
    () => client.googleSearch({ q: 'ai agents', tbs: 'qdr:decade' }),
    (error) => {
      assert.equal(error.endpoint, '/google-search');
      assert.equal(error.field, 'tbs');
      return true;
    }
  );

  assert.throws(
    () => client.headfulBrowser({ urls: 'https://example.com', output_format: 'pdf' }),
    (error) => {
      assert.equal(error.endpoint, '/headful-browser');
      assert.equal(error.field, 'output_format');
      return true;
    }
  );
});

test('wrappers reject an invalid client object before making a request', () => {
  assert.throws(
    () => search({}, { query: 'ai agents' }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.VALIDATION);
      assert.equal(error.endpoint, '/search');
      assert.equal(error.field, 'client');
      return true;
    }
  );
});
