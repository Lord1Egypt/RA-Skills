import assert from 'node:assert/strict';
import test from 'node:test';

import { CrawleoError, createCrawleoClient } from '../src/index.js';

const liveEnabled = process.env.CRAWLEO_ENABLE_LIVE_TESTS === '1';
const apiKey = process.env.CRAWLEO_API_KEY;
const skipReason = 'Set CRAWLEO_ENABLE_LIVE_TESTS=1 and CRAWLEO_API_KEY to run live Crawleo tests.';

test('live Crawleo /search smoke test is explicitly gated', { skip: liveEnabled && apiKey ? false : skipReason }, async () => {
  const client = createCrawleoClient({ apiKey });

  try {
    const result = await client.search({
      query: 'Crawleo web intelligence',
      max_pages: 1
    });

    assert.equal(typeof result, 'object');
    assert.notEqual(result, null);
  } catch (error) {
    if (error instanceof CrawleoError) {
      throw new Error(`Live Crawleo smoke test failed: ${JSON.stringify(error.toJSON())}`);
    }

    throw error;
  }
});
