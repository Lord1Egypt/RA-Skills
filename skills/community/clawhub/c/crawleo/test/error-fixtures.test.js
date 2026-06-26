import assert from 'node:assert/strict';
import test from 'node:test';

import {
  CRAWLEO_ERROR_CODES,
  CrawleoError,
  createCrawleoClient,
  redactSecret,
  requestCrawleo
} from '../src/index.js';

const FIXTURE_SECRET = 'fixture-secret-key-never-real';

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

async function getErrorFromClient(fetchImpl, apiKey = FIXTURE_SECRET) {
  const client = createCrawleoClient({ apiKey, fetch: fetchImpl });

  try {
    await client.search({ query: 'fixture query' });
  } catch (error) {
    return error;
  }

  throw new Error('Expected Crawleo client call to fail');
}

test('HTTP error fixture table maps status codes to stable Crawleo error codes', async () => {
  const fixtures = [
    [400, CRAWLEO_ERROR_CODES.HTTP_BAD_REQUEST, 'Bad request fixture'],
    [401, CRAWLEO_ERROR_CODES.HTTP_AUTH, 'Invalid API key fixture'],
    [402, CRAWLEO_ERROR_CODES.HTTP_PAYMENT_REQUIRED, 'Insufficient credits fixture'],
    [403, CRAWLEO_ERROR_CODES.HTTP_FORBIDDEN, 'Inactive subscription fixture'],
    [429, CRAWLEO_ERROR_CODES.HTTP_RATE_LIMIT, 'Rate limit fixture'],
    [500, CRAWLEO_ERROR_CODES.HTTP_UPSTREAM, 'Internal server fixture']
  ];

  for (const [status, expectedCode, message] of fixtures) {
    const error = await getErrorFromClient(async () => response({
      status,
      body: {
        error: message,
        code: `fixture_${status}`,
        details: { endpoint: '/search', status }
      }
    }));

    assert.ok(error instanceof CrawleoError);
    assert.equal(error.code, expectedCode);
    assert.equal(error.endpoint, '/search');
    assert.equal(error.status, status);
    assert.equal(error.details.error, message);
    assert.equal(error.details.code, `fixture_${status}`);
  }
});

test('missing API key and missing fetch produce distinct configuration diagnostics', async () => {
  await assert.rejects(
    () => requestCrawleo({ apiKey: '', fetchImpl: async () => response({ status: 200, body: {} }), endpointPath: '/search', params: { query: 'fixture' } }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.MISSING_API_KEY);
      assert.equal(error.endpoint, '/search');
      assert.equal(error.status, undefined);
      return true;
    }
  );

  await assert.rejects(
    () => requestCrawleo({ apiKey: FIXTURE_SECRET, fetchImpl: undefined, endpointPath: '/search', params: { query: 'fixture' } }),
    (error) => {
      assert.equal(error.code, CRAWLEO_ERROR_CODES.MISSING_FETCH);
      assert.equal(error.endpoint, '/search');
      assert.equal(JSON.stringify(error).includes(FIXTURE_SECRET), false);
      return true;
    }
  );
});

test('malformed successful JSON response carries redacted bounded body preview', async () => {
  const error = await getErrorFromClient(async () => response({
    status: 200,
    body: `{ "message": "token ${FIXTURE_SECRET}"`,
    contentType: 'application/json'
  }));

  assert.equal(error.code, CRAWLEO_ERROR_CODES.RESPONSE_MALFORMED_JSON);
  assert.equal(error.status, 200);
  assert.equal(error.details.contentType, 'application/json');
  assert.equal(error.details.bodyPreview.includes(FIXTURE_SECRET), false);
  assert.match(error.details.bodyPreview, /\[REDACTED\]/);
});

test('text HTTP error bodies are summarized and redacted without becoming malformed JSON errors', async () => {
  const error = await getErrorFromClient(async () => response({
    status: 500,
    body: `upstream failure x-api-key: ${FIXTURE_SECRET}`,
    contentType: 'text/plain'
  }));

  assert.equal(error.code, CRAWLEO_ERROR_CODES.HTTP_UPSTREAM);
  assert.equal(error.details.contentType, 'text/plain');
  assert.equal(error.details.bodyPreview.includes(FIXTURE_SECRET), false);
  assert.match(error.details.bodyPreview, /x-api-key: \[REDACTED\]/);
});

test('transport error fixture preserves transport classification and redacts thrown messages', async () => {
  const error = await getErrorFromClient(async () => {
    throw new Error(`socket closed with Authorization: Bearer ${FIXTURE_SECRET}`);
  });

  assert.equal(error.code, CRAWLEO_ERROR_CODES.TRANSPORT);
  assert.equal(error.status, undefined);
  assert.equal(error.details.cause.includes(FIXTURE_SECRET), false);
  assert.match(error.details.cause, /Authorization: \[REDACTED\]/i);
});

test('CrawleoError serialization redacts nested details and explicit secret values', () => {
  const error = new CrawleoError(`top-level message ${FIXTURE_SECRET}`, {
    code: CRAWLEO_ERROR_CODES.HTTP_AUTH,
    endpoint: '/search',
    status: 401,
    secrets: [FIXTURE_SECRET],
    details: {
      header: `x-api-key=${FIXTURE_SECRET}`,
      nested: [{ authorization: `Authorization: Bearer ${FIXTURE_SECRET}` }]
    }
  });

  const serialized = JSON.stringify(error);

  assert.equal(serialized.includes(FIXTURE_SECRET), false);
  assert.match(error.message, /\[REDACTED\]/);
  assert.match(error.details.header, /x-api-key= \[REDACTED\]/);
  assert.match(error.details.nested[0].authorization, /Authorization: \[REDACTED\]/i);
});

test('redactSecret handles common API key spellings without explicit secret input', () => {
  assert.equal(redactSecret('apiKey=abc123'), 'apiKey= [REDACTED]');
  assert.equal(redactSecret('api-key: abc123'), 'api-key: [REDACTED]');
  assert.equal(redactSecret('x-api-key: abc123'), 'x-api-key: [REDACTED]');
  assert.equal(redactSecret('Authorization: Bearer abc123'), 'Authorization: [REDACTED]');
});
