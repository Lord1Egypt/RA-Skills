import { CRAWLEO_ENDPOINTS } from './contract.js';
import { CrawleoError, CRAWLEO_ERROR_CODES } from './errors.js';

export function search(client, params = {}) {
  return callEndpoint(client, CRAWLEO_ENDPOINTS.search, params);
}

export function googleSearch(client, params = {}) {
  return callEndpoint(client, CRAWLEO_ENDPOINTS.googleSearch, params);
}

export function googleMaps(client, params = {}) {
  return callEndpoint(client, CRAWLEO_ENDPOINTS.googleMaps, params);
}

export function crawl(client, params = {}) {
  return callEndpoint(client, CRAWLEO_ENDPOINTS.crawl, normalizeUrlListParams(params));
}

export function headfulBrowser(client, params = {}) {
  return callEndpoint(client, CRAWLEO_ENDPOINTS.headfulBrowser, normalizeUrlListParams(params));
}

export function validateEndpointParams(endpoint, params = {}) {
  for (const field of endpoint.requiredQuery) {
    const value = params[field];
    if (value === undefined || value === null || value === '' || (Array.isArray(value) && value.length === 0)) {
      throw new CrawleoError(`Missing required Crawleo parameter: ${field}`, {
        code: CRAWLEO_ERROR_CODES.VALIDATION,
        endpoint: endpoint.path,
        field
      });
    }
  }

  for (const [field, allowedValues] of Object.entries(endpoint.enumQuery)) {
    const value = params[field];
    if (value !== undefined && value !== null && !allowedValues.includes(value)) {
      throw new CrawleoError(`Invalid Crawleo parameter ${field}: expected one of ${allowedValues.join(', ')}`, {
        code: CRAWLEO_ERROR_CODES.VALIDATION,
        endpoint: endpoint.path,
        field,
        details: { allowedValues, received: value }
      });
    }
  }
}

export function createEndpointMethods(client) {
  return Object.freeze({
    search: (params) => search(client, params),
    googleSearch: (params) => googleSearch(client, params),
    googleMaps: (params) => googleMaps(client, params),
    crawl: (params) => crawl(client, params),
    headfulBrowser: (params) => headfulBrowser(client, params)
  });
}

function callEndpoint(client, endpoint, params) {
  if (!client || typeof client.request !== 'function') {
    throw new CrawleoError('A Crawleo client with a request method is required.', {
      code: CRAWLEO_ERROR_CODES.VALIDATION,
      endpoint: endpoint.path,
      field: 'client'
    });
  }

  validateEndpointParams(endpoint, params);
  return client.request(endpoint.path, params);
}

function normalizeUrlListParams(params) {
  if (!Object.prototype.hasOwnProperty.call(params, 'urls')) return params;
  return {
    ...params,
    urls: Array.isArray(params.urls) ? params.urls.join(',') : params.urls
  };
}
