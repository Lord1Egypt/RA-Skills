#!/usr/bin/env node

import { createCrawleoClient, CrawleoError } from '../src/index.js';

const enableLiveExample = process.env.CRAWLEO_ENABLE_LIVE_EXAMPLE === '1';
const apiKey = process.env.CRAWLEO_API_KEY;

if (!enableLiveExample || !apiKey) {
  console.log('Skipping live Crawleo example: set CRAWLEO_ENABLE_LIVE_EXAMPLE=1 and CRAWLEO_API_KEY to run it.');
  process.exit(0);
}

const client = createCrawleoClient({ apiKey });

try {
  const result = await client.search({
    query: 'Crawleo web intelligence',
    max_pages: 1
  });

  console.log(JSON.stringify({
    ok: true,
    endpoint: '/search',
    topLevelFields: Object.keys(result || {})
  }, null, 2));
} catch (error) {
  if (error instanceof CrawleoError) {
    console.error(JSON.stringify(error.toJSON(), null, 2));
    process.exit(1);
  }

  console.error('Unexpected live Crawleo example failure.');
  process.exit(1);
}
