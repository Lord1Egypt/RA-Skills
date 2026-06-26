import { createEndpointMethods } from './endpoints.js';
import { CRAWLEO_BASE_URL, getEndpointByPath } from './contract.js';
import { CrawleoError, CRAWLEO_ERROR_CODES, errorCodeForStatus, redactSecret } from './errors.js';

export function createCrawleoClient(options = {}) {
  const apiKey = options.apiKey ?? process.env.CRAWLEO_API_KEY;
  const fetchImpl = options.fetch ?? globalThis.fetch;
  const baseUrl = normalizeBaseUrl(options.baseUrl ?? CRAWLEO_BASE_URL);

  const client = {
    baseUrl,
    request(endpointPath, params = {}) {
      return requestCrawleo({ apiKey, fetchImpl, baseUrl, endpointPath, params });
    }
  };

  return Object.freeze({
    ...client,
    ...createEndpointMethods(client)
  });
}

export async function requestCrawleo({ apiKey, fetchImpl, baseUrl = CRAWLEO_BASE_URL, endpointPath, params = {} }) {
  const endpoint = getEndpointByPath(endpointPath);
  if (!endpoint) {
    throw new CrawleoError(`Unknown Crawleo endpoint: ${endpointPath}`, {
      code: CRAWLEO_ERROR_CODES.VALIDATION,
      endpoint: endpointPath,
      field: 'endpointPath'
    });
  }

  if (!apiKey) {
    throw new CrawleoError('CRAWLEO_API_KEY is required for live Crawleo REST calls.', {
      code: CRAWLEO_ERROR_CODES.MISSING_API_KEY,
      endpoint: endpointPath
    });
  }

  if (typeof fetchImpl !== 'function') {
    throw new CrawleoError('A fetch implementation is required for Crawleo REST calls.', {
      code: CRAWLEO_ERROR_CODES.MISSING_FETCH,
      endpoint: endpointPath,
      secrets: [apiKey]
    });
  }

  const url = buildCrawleoUrl(baseUrl, endpoint.path, params);
  let response;

  try {
    response = await fetchImpl(url, {
      method: endpoint.method,
      headers: {
        'x-api-key': apiKey,
        accept: 'application/json'
      }
    });
  } catch (error) {
    throw new CrawleoError('Crawleo request failed before receiving a response.', {
      code: CRAWLEO_ERROR_CODES.TRANSPORT,
      endpoint: endpoint.path,
      details: { cause: error instanceof Error ? error.message : String(error) },
      secrets: [apiKey]
    });
  }

  return parseCrawleoResponse(response, { endpointPath: endpoint.path, apiKey });
}

export function buildCrawleoUrl(baseUrl, endpointPath, params = {}) {
  const url = new URL(endpointPath, `${normalizeBaseUrl(baseUrl)}/`);

  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null) continue;
    const encodedValue = Array.isArray(value) ? value.join(',') : String(value);
    url.searchParams.set(key, encodedValue);
  }

  return url;
}

async function parseCrawleoResponse(response, { endpointPath, apiKey }) {
  const status = response.status;
  const ok = response.ok ?? (status >= 200 && status < 300);
  const rawBody = await readResponseBody(response);
  const contentType = typeof response.headers?.get === 'function' ? response.headers.get('content-type') || '' : '';
  const expectsJson = contentType.includes('application/json') || rawBody.trim().startsWith('{') || rawBody.trim().startsWith('[');

  let parsedBody = null;
  let malformedJson = false;

  if (rawBody && expectsJson) {
    try {
      parsedBody = JSON.parse(rawBody);
    } catch {
      malformedJson = true;
    }
  }

  if (!ok) {
    throw new CrawleoError(`Crawleo request failed with HTTP ${status}.`, {
      code: errorCodeForStatus(status),
      endpoint: endpointPath,
      status,
      details: summarizeResponseBody(parsedBody, rawBody, contentType, apiKey),
      secrets: [apiKey]
    });
  }

  if (malformedJson) {
    throw new CrawleoError('Crawleo returned malformed JSON.', {
      code: CRAWLEO_ERROR_CODES.RESPONSE_MALFORMED_JSON,
      endpoint: endpointPath,
      status,
      details: {
        contentType,
        bodyPreview: redactSecret(rawBody.slice(0, 500), [apiKey])
      },
      secrets: [apiKey]
    });
  }

  return parsedBody;
}

async function readResponseBody(response) {
  if (typeof response.text === 'function') return response.text();
  if (typeof response.json === 'function') return JSON.stringify(await response.json());
  return '';
}

function summarizeResponseBody(body, rawBody, contentType, apiKey) {
  if (body == null) {
    if (!rawBody) return null;
    return {
      contentType,
      bodyPreview: redactSecret(rawBody.slice(0, 500), [apiKey])
    };
  }
  if (typeof body !== 'object') return { body };

  const summary = {};
  for (const key of ['error', 'message', 'code', 'details']) {
    if (Object.prototype.hasOwnProperty.call(body, key)) {
      summary[key] = body[key];
    }
  }

  return Object.keys(summary).length > 0 ? summary : { body };
}

function normalizeBaseUrl(baseUrl) {
  return String(baseUrl).replace(/\/+$/, '');
}
