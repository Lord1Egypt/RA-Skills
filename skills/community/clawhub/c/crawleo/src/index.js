export { createCrawleoClient, requestCrawleo, buildCrawleoUrl } from './client.js';
export { search, googleSearch, googleMaps, crawl, headfulBrowser, validateEndpointParams } from './endpoints.js';
export { CRAWLEO_BASE_URL, CRAWLEO_ENDPOINTS, CRAWLEO_ENDPOINTS_BY_PATH, getEndpointByPath } from './contract.js';
export { CrawleoError, CRAWLEO_ERROR_CODES, redactSecret } from './errors.js';

export const CRAWLEO_CONTRACT_PATH = 'contracts/crawleo-endpoints.json';
export const CRAWLEO_SKILL_MANIFEST_PATH = 'skill.json';
export const CRAWLEO_SKILL_INSTRUCTIONS_PATH = 'SKILL.md';

export const CRAWLEO_REST_ENDPOINTS = Object.freeze([
  '/search',
  '/google-search',
  '/google-maps',
  '/crawl',
  '/headful-browser'
]);

export const CRAWLEO_MCP_TOOLS = Object.freeze([
  'search_web',
  'google_search',
  'google_maps',
  'crawl_web',
  'headful_browser'
]);

export function getScaffoldStatus() {
  return Object.freeze({
    packageName: 'openclaw-crawleo-skill',
    implementationStatus: 'rest-wrappers-implemented',
    contractPath: CRAWLEO_CONTRACT_PATH,
    skillManifestPath: CRAWLEO_SKILL_MANIFEST_PATH,
    skillInstructionsPath: CRAWLEO_SKILL_INSTRUCTIONS_PATH,
    restEndpoints: CRAWLEO_REST_ENDPOINTS,
    mcpTools: CRAWLEO_MCP_TOOLS,
    liveCrawleoCallsEnabledByDefault: false
  });
}
