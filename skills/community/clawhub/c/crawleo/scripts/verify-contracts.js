#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const contractPath = path.join('contracts', 'crawleo-endpoints.json');
const markdownPath = path.join('contracts', 'crawleo-endpoints.md');

const requiredEndpoints = ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser'];
const requiredTools = ['search_web', 'google_search', 'google_maps', 'crawl_web', 'headful_browser'];
const requiredEndpointFields = [
  'id',
  'name',
  'method',
  'path',
  'url',
  'mcp_tool',
  'description',
  'sources',
  'cost',
  'parameters',
  'examples',
  'response_shape',
  'errors',
  'ambiguities'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function assert(condition, message) {
  if (!condition) fail(message);
}

function countValues(values) {
  return values.reduce((counts, value) => {
    counts[value] = (counts[value] || 0) + 1;
    return counts;
  }, {});
}

assert(fs.existsSync(contractPath), `${contractPath} does not exist`);
assert(fs.existsSync(markdownPath), `${markdownPath} does not exist`);

let contract;
try {
  contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
} catch (error) {
  fail(`${contractPath} is not valid JSON: ${error.message}`);
  contract = { endpoints: [] };
}

const markdown = fs.existsSync(markdownPath) ? fs.readFileSync(markdownPath, 'utf8') : '';
const endpoints = Array.isArray(contract.endpoints) ? contract.endpoints : [];
const endpointPaths = endpoints.map((endpoint) => endpoint.path);
const endpointPathCounts = countValues(endpointPaths);

for (const endpointPath of requiredEndpoints) {
  assert(endpointPathCounts[endpointPath] === 1, `expected exactly one contract for ${endpointPath}, found ${endpointPathCounts[endpointPath] || 0}`);
  assert(markdown.includes(endpointPath), `${markdownPath} does not mention ${endpointPath}`);
}

const toolNames = endpoints.map((endpoint) => endpoint.mcp_tool).filter(Boolean);
const mcpTools = contract.mcp && Array.isArray(contract.mcp.tools) ? contract.mcp.tools.map((tool) => tool.name) : [];
const allTools = [...toolNames, ...mcpTools];

for (const toolName of requiredTools) {
  assert(allTools.includes(toolName), `missing MCP tool ${toolName}`);
  assert(markdown.includes(toolName), `${markdownPath} does not mention MCP tool ${toolName}`);
}

for (const endpoint of endpoints) {
  for (const field of requiredEndpointFields) {
    assert(Object.prototype.hasOwnProperty.call(endpoint, field), `${endpoint.path || endpoint.id || 'unknown endpoint'} missing field ${field}`);
  }

  assert(endpoint.method === 'GET', `${endpoint.path} method must be GET per Crawleo docs`);
  assert(typeof endpoint.url === 'string' && endpoint.url.startsWith('https://api.crawleo.dev/'), `${endpoint.path} url must use Crawleo API base URL`);
  assert(Array.isArray(endpoint.sources) && endpoint.sources.length > 0, `${endpoint.path} must include source links`);
  assert(Array.isArray(endpoint.parameters) && endpoint.parameters.length > 0, `${endpoint.path} must include parameters`);
  assert(endpoint.parameters.some((parameter) => parameter.name === 'x-api-key' && parameter.in === 'header'), `${endpoint.path} must include x-api-key header parameter`);
  assert(Array.isArray(endpoint.examples) && endpoint.examples.length > 0, `${endpoint.path} must include examples`);
  assert(endpoint.response_shape && Array.isArray(endpoint.response_shape.top_level_fields) && endpoint.response_shape.top_level_fields.length > 0, `${endpoint.path} must include response top-level fields`);
  assert(Array.isArray(endpoint.ambiguities) && endpoint.ambiguities.length > 0, `${endpoint.path} must include ambiguity notes, even if only to say no ambiguity is known`);
}

assert(markdown.includes('not specified in Crawleo docs'), `${markdownPath} must preserve required ambiguity phrase`);
assert(JSON.stringify(contract).includes('not specified in Crawleo docs'), `${contractPath} must preserve required ambiguity phrase`);

if (process.exitCode) {
  console.error('Crawleo contract verification failed.');
  process.exit(process.exitCode);
}

console.log(`Crawleo contract verification passed: ${requiredEndpoints.length} endpoints and ${requiredTools.length} MCP tools covered.`);
