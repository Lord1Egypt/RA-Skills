import assert from 'node:assert/strict';
import test from 'node:test';

import { CRAWLEO_ERROR_CODES, CrawleoError, createCrawleoClient } from '../src/index.js';

function response({ status, body, contentType = 'application/json' }) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: new Map([['content-type', contentType]]),
    async text() {
      return typeof body === 'string' ? body : JSON.stringify(body);
    }
  };
}

async function captureError(status, body, contentType, apiKey = `secret-key-${status}`) {
  const client = createCrawleoClient({
    apiKey,
    fetch: async () => response({ status, body, contentType })
  });

  try {
    await client.search({ query: 'ai agents' });
  } catch (error) {
    return { error, apiKey };
  }

  throw new Error('Expected request to fail');
}

test('HTTP 400 bad requests map to a stable Crawleo error code', async () => {
  const { error } = await captureError(400, { error: 'Missing required parameter q' });

  assert.ok(error instanceof CrawleoError);
  assert.equal(error.code, CRAWLEO_ERROR_CODES.HTTP_BAD_REQUEST);
  assert.equal(error.endpoint, '/search');
  assert.equal(error.status, 400);
  assert.deepEqual(error.details, { error: 'Missing required parameter q' });
});

test('HTTP 401 auth failures are normalized without leaking the API key', async () => {
  const apiKey = 'secret-key-401';
  const { error } = await captureError(401, {
    error: `Invalid x-api-key: ${apiKey}`,
    code: 'invalid_key'
  }, undefined, apiKey);

  assert.equal(error.code, CRAWLEO_ERROR_CODES.HTTP_AUTH);
  assert.equal(JSON.stringify(error).includes(apiKey), false);
  assert.match(JSON.stringify(error), /\[REDACTED\]/);
});

test('HTTP 402 quota failures and HTTP 429 rate limits get distinct codes', async () => {
  const quota = await captureError(402, { error: 'Insufficient credits' });
  const rateLimit = await captureError(429, { error: 'Rate limit exceeded' });

  assert.equal(quota.error.code, CRAWLEO_ERROR_CODES.HTTP_PAYMENT_REQUIRED);
  assert.equal(rateLimit.error.code, CRAWLEO_ERROR_CODES.HTTP_RATE_LIMIT);
});

test('HTTP 403 forbidden and 5xx upstream failures get stable codes', async () => {
  const forbidden = await captureError(403, { error: 'Inactive account or expired subscription' });
  const upstream = await captureError(500, { error: 'Internal server error' });

  assert.equal(forbidden.error.code, CRAWLEO_ERROR_CODES.HTTP_FORBIDDEN);
  assert.equal(upstream.error.code, CRAWLEO_ERROR_CODES.HTTP_UPSTREAM);
});

test('non-JSON HTTP errors preserve a bounded redacted body preview', async () => {
  const apiKey = 'secret-key-500-text';
  const { error } = await captureError(500, `server failed with api_key=${apiKey}`, 'text/plain', apiKey);

  assert.equal(error.code, CRAWLEO_ERROR_CODES.HTTP_UPSTREAM);
  assert.equal(error.details.contentType, 'text/plain');
  assert.equal(error.details.bodyPreview.includes(apiKey), false);
  assert.match(error.details.bodyPreview, /\[REDACTED\]/);
});

test('successful malformed JSON responses are response diagnostics, not HTTP errors', async () => {
  const apiKey = 'secret-malformed-key';
  const client = createCrawleoClient({
    apiKey,
    fetch: async () => response({ status: 200, body: `{ "token": "${apiKey}"`, contentType: 'application/json' })
  });

  await assert.rejects(
    () => client.search({ query: 'ai agents' }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.RESPONSE_MALFORMED_JSON);
      assert.equal(error.status, 200);
      assert.equal(JSON.stringify(error).includes(apiKey), false);
      return true;
    }
  );
});

test('transport failures remain distinct from HTTP failures and are redacted', async () => {
  const apiKey = 'secret-network-key';
  const client = createCrawleoClient({
    apiKey,
    fetch: async () => {
      throw new Error(`socket closed for ${apiKey}`);
    }
  });

  await assert.rejects(
    () => client.search({ query: 'ai agents' }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.TRANSPORT);
      assert.equal(error.status, undefined);
      assert.equal(JSON.stringify(error).includes(apiKey), false);
      return true;
    }
  );
});
