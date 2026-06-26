#!/usr/bin/env node

import fs from 'node:fs';

const requiredFiles = [
  'README.md',
  'LICENSE',
  'SKILL.md',
  'skill.json',
  'package.json',
  'contracts/crawleo-endpoints.json',
  'contracts/crawleo-endpoints.md',
  'contracts/coverage-checklist.md',
  'contracts/final-assembly-report.md',
  'examples/README.md',
  'examples/offline-fake-fetch.js',
  'examples/live-usage-template.js',
  'src/index.js',
  'src/client.js',
  'src/contract.js',
  'src/endpoints.js',
  'src/errors.js',
  'test/client.test.js',
  'test/endpoints.test.js',
  'test/error-fixtures.test.js',
  'test/errors.test.js',
  'test/live.test.js',
  'test/scaffold.test.js',
  'test/wrapper-fixtures.test.js',
  'scripts/verify-contracts.js',
  'scripts/verify-final.js',
  'scripts/verify-scaffold.js'
];

const requiredEndpoints = ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser'];
const requiredTools = ['search_web', 'google_search', 'google_maps', 'crawl_web', 'headful_browser'];
const requiredWrappers = ['client.search', 'client.googleSearch', 'client.googleMaps', 'client.crawl', 'client.headfulBrowser'];
const requiredScripts = ['test', 'test:live', 'verify:contracts', 'verify:examples', 'verify:scaffold', 'verify:final'];
const deliverableFilesForBranding = [
  'README.md',
  'SKILL.md',
  'skill.json',
  'package.json',
  'contracts/crawleo-endpoints.md',
  'contracts/coverage-checklist.md',
  'contracts/final-assembly-report.md',
  'examples/README.md',
  'examples/offline-fake-fetch.js',
  'examples/live-usage-template.js',
  'src/index.js',
  'src/client.js',
  'src/contract.js',
  'src/endpoints.js',
  'src/errors.js'
];
const disallowedBrandTerms = ['Firecrawl', 'firecrawl', 'Apify', 'apify', 'Tavily', 'tavily', 'SerpAPI', 'serpapi', 'Browserbase', 'browserbase'];

const failures = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

function readText(path) {
  return fs.readFileSync(path, 'utf8');
}

for (const file of requiredFiles) {
  check(fs.existsSync(file), `${file} is missing`);
  if (fs.existsSync(file)) check(fs.statSync(file).size > 0, `${file} is empty`);
}

let packageJson = {};
let skillJson = {};
let contract = {};
try {
  packageJson = JSON.parse(readText('package.json'));
} catch (error) {
  failures.push(`package.json is invalid JSON: ${error.message}`);
}
try {
  skillJson = JSON.parse(readText('skill.json'));
} catch (error) {
  failures.push(`skill.json is invalid JSON: ${error.message}`);
}
try {
  contract = JSON.parse(readText('contracts/crawleo-endpoints.json'));
} catch (error) {
  failures.push(`contracts/crawleo-endpoints.json is invalid JSON: ${error.message}`);
}

const textFiles = Object.fromEntries(
  requiredFiles.filter((file) => fs.existsSync(file)).map((file) => [file, readText(file)])
);
const combined = Object.values(textFiles).join('\n');

check(packageJson.name === 'openclaw-crawleo-skill', 'package name must be openclaw-crawleo-skill');
check(packageJson.type === 'module', 'package type must be module');
check(packageJson.private === false, 'package must be publishable with private=false');
check(packageJson.license === 'MIT', 'package license must be MIT');
check(Array.isArray(packageJson.files) && packageJson.files.includes('LICENSE'), 'package files must include LICENSE');
check(Array.isArray(packageJson.files) && packageJson.files.includes('scripts/'), 'package files must include scripts/ for verifier scripts');
check(skillJson.name === 'crawleo', 'skill.json name must be crawleo');
check(skillJson.brand === 'Crawleo', 'skill.json brand must be Crawleo');
check(skillJson.contract === './contracts/crawleo-endpoints.json', 'skill.json must point to contract JSON');
check(skillJson.instructions === './SKILL.md', 'skill.json must point to SKILL.md');

for (const scriptName of requiredScripts) {
  check(Boolean(packageJson.scripts?.[scriptName]), `package.json missing ${scriptName} script`);
}

const contractEndpoints = Array.isArray(contract.endpoints) ? contract.endpoints : [];
const contractPaths = contractEndpoints.map((endpoint) => endpoint.path);
const contractTools = contractEndpoints.map((endpoint) => endpoint.mcp_tool).filter(Boolean);
const mcpTools = Array.isArray(contract.mcp?.tools) ? contract.mcp.tools.map((tool) => tool.name) : [];

for (const endpoint of requiredEndpoints) {
  check(contractPaths.filter((path) => path === endpoint).length === 1, `contract must contain exactly one ${endpoint}`);
  for (const file of ['README.md', 'SKILL.md', 'contracts/crawleo-endpoints.md', 'contracts/coverage-checklist.md', 'contracts/final-assembly-report.md', 'examples/offline-fake-fetch.js']) {
    check(textFiles[file]?.includes(endpoint), `${file} must mention ${endpoint}`);
  }
}

for (const tool of requiredTools) {
  check(contractTools.includes(tool) || mcpTools.includes(tool), `contract must include MCP tool ${tool}`);
  for (const file of ['README.md', 'SKILL.md', 'contracts/crawleo-endpoints.md', 'contracts/coverage-checklist.md', 'contracts/final-assembly-report.md', 'skill.json']) {
    check(textFiles[file]?.includes(tool), `${file} must mention ${tool}`);
  }
}

for (const wrapper of requiredWrappers) {
  for (const file of ['README.md', 'contracts/coverage-checklist.md', 'test/wrapper-fixtures.test.js']) {
    check(textFiles[file]?.includes(wrapper), `${file} must mention ${wrapper}`);
  }
}

for (const file of ['README.md', 'SKILL.md', 'contracts/coverage-checklist.md', 'contracts/final-assembly-report.md', 'test/live.test.js']) {
  check(textFiles[file]?.includes('CRAWLEO_ENABLE_LIVE_TESTS'), `${file} must document or enforce CRAWLEO_ENABLE_LIVE_TESTS`);
  check(textFiles[file]?.includes('CRAWLEO_API_KEY'), `${file} must document or enforce CRAWLEO_API_KEY`);
}

check(textFiles['README.md']?.includes('contracts/final-assembly-report.md'), 'README.md must point to final assembly report');
check(textFiles['README.md']?.includes('npm run test:live'), 'README.md must document npm run test:live');
check(textFiles['SKILL.md']?.includes('npm run test:live'), 'SKILL.md must document npm run test:live');
check(textFiles['contracts/coverage-checklist.md']?.includes('npm run test:live'), 'coverage checklist must document npm run test:live');
check(combined.includes('not specified in Crawleo docs'), 'deliverables must preserve the Crawleo ambiguity phrase');
check(combined.includes('https://api.crawleo.dev/mcp'), 'deliverables must mention the optional Crawleo MCP endpoint');

for (const file of deliverableFilesForBranding) {
  const text = textFiles[file] || '';
  for (const term of disallowedBrandTerms) {
    check(!text.includes(term), `${file} contains non-Crawleo brand/reference ${term}`);
  }
}

if (failures.length > 0) {
  console.error('Crawleo final assembly verification failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Crawleo final assembly verification passed: ${requiredFiles.length} files, ${requiredEndpoints.length} endpoints, ${requiredTools.length} MCP tools, ${requiredWrappers.length} wrapper methods, ${requiredScripts.length} scripts.`);
