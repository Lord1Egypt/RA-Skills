import assert from 'node:assert/strict';
import test from 'node:test';

import {
  CRAWLEO_CONTRACT_PATH,
  CRAWLEO_MCP_TOOLS,
  CRAWLEO_REST_ENDPOINTS,
  CRAWLEO_SKILL_INSTRUCTIONS_PATH,
  CRAWLEO_SKILL_MANIFEST_PATH,
  createCrawleoClient,
  crawl,
  getScaffoldStatus,
  googleMaps,
  googleSearch,
  headfulBrowser,
  search
} from '../src/index.js';

test('scaffold exports the Crawleo contract location and documented capability names', () => {
  assert.equal(CRAWLEO_CONTRACT_PATH, 'contracts/crawleo-endpoints.json');
  assert.equal(CRAWLEO_SKILL_MANIFEST_PATH, 'skill.json');
  assert.equal(CRAWLEO_SKILL_INSTRUCTIONS_PATH, 'SKILL.md');
  assert.deepEqual(CRAWLEO_REST_ENDPOINTS, ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser']);
  assert.deepEqual(CRAWLEO_MCP_TOOLS, ['search_web', 'google_search', 'google_maps', 'crawl_web', 'headful_browser']);
});

test('scaffold status is explicit that runtime wrappers are implemented and live calls are opt-in', () => {
  assert.deepEqual(getScaffoldStatus(), {
    packageName: 'openclaw-crawleo-skill',
    implementationStatus: 'rest-wrappers-implemented',
    contractPath: 'contracts/crawleo-endpoints.json',
    skillManifestPath: 'skill.json',
    skillInstructionsPath: 'SKILL.md',
    restEndpoints: ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser'],
    mcpTools: ['search_web', 'google_search', 'google_maps', 'crawl_web', 'headful_browser'],
    liveCrawleoCallsEnabledByDefault: false
  });
});

test('public API exports client factory and all endpoint wrapper functions', () => {
  assert.equal(typeof createCrawleoClient, 'function');
  assert.equal(typeof search, 'function');
  assert.equal(typeof googleSearch, 'function');
  assert.equal(typeof googleMaps, 'function');
  assert.equal(typeof crawl, 'function');
  assert.equal(typeof headfulBrowser, 'function');
});
