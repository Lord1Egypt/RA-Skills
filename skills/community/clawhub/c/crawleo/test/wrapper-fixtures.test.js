import assert from 'node:assert/strict';
import test from 'node:test';

import { CRAWLEO_ERROR_CODES, createCrawleoClient } from '../src/index.js';

function createRecordingClient() {
  const calls = [];
  const client = createCrawleoClient({
    apiKey: 'offline-wrapper-fixture-key',
    fetch: async (url, init) => {
      const requestUrl = new URL(url);
      calls.push({ url: requestUrl, init });
      return {
        ok: true,
        status: 200,
        headers: new Map([['content-type', 'application/json']]),
        async text() {
          return JSON.stringify({
            ok: true,
            path: requestUrl.pathname,
            query: Object.fromEntries(requestUrl.searchParams.entries())
          });
        }
      };
    }
  });

  return { client, calls };
}

async function assertSingleRequest(wrapperCall, { path, query }) {
  const { client, calls } = createRecordingClient();
  const result = await wrapperCall(client);

  assert.equal(calls.length, 1);
  assert.equal(calls[0].url.origin, 'https://api.crawleo.dev');
  assert.equal(calls[0].url.pathname, path);
  assert.equal(calls[0].init.method, 'GET');
  assert.equal(calls[0].init.headers['x-api-key'], 'offline-wrapper-fixture-key');
  assert.equal(calls[0].init.headers.accept, 'application/json');

  for (const [key, value] of Object.entries(query)) {
    assert.equal(calls[0].url.searchParams.get(key), String(value));
  }

  assert.equal(result.path, path);
  return calls[0].url;
}

function assertValidationError(fn, { endpoint, field }) {
  assert.throws(
    fn,
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.VALIDATION);
      assert.equal(error.endpoint, endpoint);
      assert.equal(error.field, field);
      return true;
    }
  );
}

test('search wrapper constructs /search URL with documented query params', async () => {
  await assertSingleRequest(
    (client) => client.search({
      query: 'machine learning',
      max_pages: 2,
      device: 'mobile',
      markdown: true,
      auto_crawling: false
    }),
    {
      path: '/search',
      query: {
        query: 'machine learning',
        max_pages: '2',
        device: 'mobile',
        markdown: 'true',
        auto_crawling: 'false'
      }
    }
  );
});

test('googleSearch wrapper constructs /google-search URL with documented query params', async () => {
  await assertSingleRequest(
    (client) => client.googleSearch({
      q: 'best CRM software',
      gl: 'us',
      hl: 'en',
      type: 'shopping',
      tbs: 'qdr:w',
      num: 10,
      page: 2
    }),
    {
      path: '/google-search',
      query: {
        q: 'best CRM software',
        gl: 'us',
        hl: 'en',
        type: 'shopping',
        tbs: 'qdr:w',
        num: '10',
        page: '2'
      }
    }
  );
});

test('googleMaps wrapper constructs /google-maps URL with documented query params', async () => {
  await assertSingleRequest(
    (client) => client.googleMaps({
      q: 'restaurants in Paris',
      hl: 'fr',
      ll: '@48.8566,2.3522,15z',
      placeId: 'ChIJLU7jZClu5kcR4PcOOO6p3I0'
    }),
    {
      path: '/google-maps',
      query: {
        q: 'restaurants in Paris',
        hl: 'fr',
        ll: '@48.8566,2.3522,15z',
        placeId: 'ChIJLU7jZClu5kcR4PcOOO6p3I0'
      }
    }
  );
});

test('crawl wrapper serializes string and array urls as documented comma-separated query values', async () => {
  await assertSingleRequest(
    (client) => client.crawl({ urls: 'https://example.com/a', markdown: true }),
    {
      path: '/crawl',
      query: {
        urls: 'https://example.com/a',
        markdown: 'true'
      }
    }
  );

  await assertSingleRequest(
    (client) => client.crawl({ urls: ['https://example.com/a', 'https://example.com/b'], render_js: true, screenshot: true }),
    {
      path: '/crawl',
      query: {
        urls: 'https://example.com/a,https://example.com/b',
        render_js: 'true',
        screenshot: 'true'
      }
    }
  );
});

test('headfulBrowser wrapper serializes urls and output options for /headful-browser', async () => {
  await assertSingleRequest(
    (client) => client.headfulBrowser({
      urls: ['https://example.com/a', 'https://example.com/b'],
      country: 'gb',
      output_format: 'page_text',
      screenshot: false
    }),
    {
      path: '/headful-browser',
      query: {
        urls: 'https://example.com/a,https://example.com/b',
        country: 'gb',
        output_format: 'page_text',
        screenshot: 'false'
      }
    }
  );
});

test('required parameter validation identifies every documented required field', () => {
  const { client } = createRecordingClient();

  assertValidationError(() => client.search({}), { endpoint: '/search', field: 'query' });
  assertValidationError(() => client.search({ query: '' }), { endpoint: '/search', field: 'query' });
  assertValidationError(() => client.googleSearch({}), { endpoint: '/google-search', field: 'q' });
  assertValidationError(() => client.googleSearch({ q: '' }), { endpoint: '/google-search', field: 'q' });
  assertValidationError(() => client.googleMaps({}), { endpoint: '/google-maps', field: 'q' });
  assertValidationError(() => client.googleMaps({ q: '' }), { endpoint: '/google-maps', field: 'q' });
  assertValidationError(() => client.crawl({}), { endpoint: '/crawl', field: 'urls' });
  assertValidationError(() => client.crawl({ urls: [] }), { endpoint: '/crawl', field: 'urls' });
  assertValidationError(() => client.headfulBrowser({}), { endpoint: '/headful-browser', field: 'urls' });
  assertValidationError(() => client.headfulBrowser({ urls: [] }), { endpoint: '/headful-browser', field: 'urls' });
});

test('documented enum validators accept all allowed values', async () => {
  for (const device of ['desktop', 'mobile', 'tablet']) {
    await assertSingleRequest((client) => client.search({ query: 'ai agents', device }), {
      path: '/search',
      query: { query: 'ai agents', device }
    });
  }

  for (const type of ['search', 'news', 'images', 'places', 'shopping']) {
    await assertSingleRequest((client) => client.googleSearch({ q: 'ai agents', type }), {
      path: '/google-search',
      query: { q: 'ai agents', type }
    });
  }

  for (const tbs of ['qdr:h', 'qdr:d', 'qdr:w', 'qdr:m', 'qdr:y']) {
    await assertSingleRequest((client) => client.googleSearch({ q: 'ai agents', tbs }), {
      path: '/google-search',
      query: { q: 'ai agents', tbs }
    });
  }

  for (const output_format of ['markdown', 'enhanced_html', 'raw_html', 'page_text']) {
    await assertSingleRequest((client) => client.headfulBrowser({ urls: 'https://example.com', output_format }), {
      path: '/headful-browser',
      query: { urls: 'https://example.com', output_format }
    });
  }
});

test('documented enum validators reject invalid values with field diagnostics', () => {
  const { client } = createRecordingClient();

  assertValidationError(() => client.search({ query: 'ai agents', device: 'watch' }), { endpoint: '/search', field: 'device' });
  assertValidationError(() => client.googleSearch({ q: 'ai agents', type: 'videos' }), { endpoint: '/google-search', field: 'type' });
  assertValidationError(() => client.googleSearch({ q: 'ai agents', tbs: 'qdr:decade' }), { endpoint: '/google-search', field: 'tbs' });
  assertValidationError(() => client.headfulBrowser({ urls: 'https://example.com', output_format: 'pdf' }), { endpoint: '/headful-browser', field: 'output_format' });
});
