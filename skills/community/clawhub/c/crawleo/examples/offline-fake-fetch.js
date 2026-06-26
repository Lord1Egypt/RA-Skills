#!/usr/bin/env node

import { createCrawleoClient } from '../src/index.js';

const calls = [];

const client = createCrawleoClient({
  apiKey: 'offline-example-key',
  fetch: async (url, init) => {
    const requestUrl = new URL(url);
    calls.push({ path: requestUrl.pathname, method: init.method });

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

await client.search({ query: 'ai agents', max_pages: 1, markdown: true });
await client.googleSearch({ q: 'best CRM software', type: 'news', tbs: 'qdr:d' });
await client.googleMaps({ q: 'restaurants in Paris', hl: 'fr' });
await client.crawl({ urls: ['https://example.com'], markdown: true });
await client.headfulBrowser({ urls: 'https://example.com', output_format: 'markdown' });

const expectedPaths = ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser'];
const actualPaths = calls.map((call) => call.path);

if (JSON.stringify(actualPaths) !== JSON.stringify(expectedPaths)) {
  throw new Error(`Unexpected wrapper paths: ${actualPaths.join(', ')}`);
}

console.log(`Offline Crawleo wrapper example passed for ${calls.length} endpoints.`);
