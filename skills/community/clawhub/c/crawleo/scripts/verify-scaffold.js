#!/usr/bin/env node

import fs from 'node:fs';

const requiredFiles = [
  'package.json',
  'README.md',
  'SKILL.md',
  'skill.json',
  'src/index.js',
  'src/client.js',
  'src/contract.js',
  'src/endpoints.js',
  'src/errors.js',
  'test/scaffold.test.js',
  'test/client.test.js',
  'test/endpoints.test.js',
  'test/errors.test.js',
  'test/error-fixtures.test.js',
  'test/live.test.js',
  'test/wrapper-fixtures.test.js',
  'examples/README.md',
  'examples/offline-fake-fetch.js',
  'examples/live-usage-template.js',
  'contracts/crawleo-endpoints.json',
  'contracts/crawleo-endpoints.md',
  'contracts/coverage-checklist.md',
  'scripts/verify-contracts.js',
  'scripts/verify-scaffold.js'
];

const requiredEndpoints = ['/search', '/google-search', '/google-maps', '/crawl', '/headful-browser'];
const requiredTools = ['search_web', 'google_search', 'google_maps', 'crawl_web', 'headful_browser'];
const requiredExports = [
  'createCrawleoClient',
  'requestCrawleo',
  'buildCrawleoUrl',
  'CrawleoError',
  'CRAWLEO_ERROR_CODES',
  'search',
  'googleSearch',
  'googleMaps',
  'crawl',
  'headfulBrowser'
];
const requiredWrapperMentions = ['client.search', 'client.googleSearch', 'client.googleMaps', 'client.crawl', 'client.headfulBrowser'];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function assert(condition, message) {
  if (!condition) fail(message);
}

for (const file of requiredFiles) {
  assert(fs.existsSync(file), `${file} is missing`);
  if (fs.existsSync(file)) {
    assert(fs.statSync(file).size > 0, `${file} is empty`);
  }
}

let packageJson = {};
let skillJson = {};
let contract = {};

try {
  packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
} catch (error) {
  fail(`package.json is invalid JSON: ${error.message}`);
}

try {
  skillJson = JSON.parse(fs.readFileSync('skill.json', 'utf8'));
} catch (error) {
  fail(`skill.json is invalid JSON: ${error.message}`);
}

try {
  contract = JSON.parse(fs.readFileSync('contracts/crawleo-endpoints.json', 'utf8'));
} catch (error) {
  fail(`contracts/crawleo-endpoints.json is invalid JSON: ${error.message}`);
}

assert(packageJson.name === 'openclaw-crawleo-skill', 'package name must be openclaw-crawleo-skill');
assert(packageJson.type === 'module', 'package must use ESM modules');
assert(packageJson.scripts && packageJson.scripts.test === 'node --test', 'package must expose node --test script');
assert(packageJson.scripts && packageJson.scripts['test:live'] === 'node --test test/live.test.js', 'package must expose test:live script');
assert(packageJson.scripts && packageJson.scripts['verify:contracts'] === 'node scripts/verify-contracts.js', 'package must expose verify:contracts script');
assert(packageJson.scripts && packageJson.scripts['verify:examples'] === 'node examples/offline-fake-fetch.js && node examples/live-usage-template.js', 'package must expose verify:examples script');
assert(packageJson.scripts && packageJson.scripts['verify:scaffold'] === 'node scripts/verify-scaffold.js', 'package must expose verify:scaffold script');

assert(skillJson.contract === './contracts/crawleo-endpoints.json', 'skill.json must point at the contract inventory');
assert(skillJson.instructions === './SKILL.md', 'skill.json must point at SKILL.md');
assert(skillJson.entrypoint === './src/index.js', 'skill.json must point at src/index.js');

const readme = fs.readFileSync('README.md', 'utf8');
const skillText = fs.readFileSync('SKILL.md', 'utf8');
const coverageText = fs.readFileSync('contracts/coverage-checklist.md', 'utf8');
const sourceText = fs.readFileSync('src/index.js', 'utf8');
const contractText = JSON.stringify(contract);
const skillJsonText = JSON.stringify(skillJson);

for (const endpoint of requiredEndpoints) {
  assert(readme.includes(endpoint), `README.md must mention ${endpoint}`);
  assert(skillText.includes(endpoint), `SKILL.md must mention ${endpoint}`);
  assert(coverageText.includes(endpoint), `coverage checklist must mention ${endpoint}`);
  assert(sourceText.includes(endpoint), `src/index.js must mention ${endpoint}`);
  assert(contractText.includes(endpoint), `contract must mention ${endpoint}`);
  assert(skillJsonText.includes(endpoint), `skill.json must mention ${endpoint}`);
}

for (const tool of requiredTools) {
  assert(readme.includes(tool), `README.md must mention ${tool}`);
  assert(skillText.includes(tool), `SKILL.md must mention ${tool}`);
  assert(coverageText.includes(tool), `coverage checklist must mention ${tool}`);
  assert(sourceText.includes(tool), `src/index.js must mention ${tool}`);
  assert(contractText.includes(tool), `contract must mention ${tool}`);
  assert(skillJsonText.includes(tool), `skill.json must mention ${tool}`);
}

assert(readme.includes('CRAWLEO_API_KEY'), 'README.md must document CRAWLEO_API_KEY');
assert(readme.includes('CRAWLEO_ENABLE_LIVE_TESTS'), 'README.md must document CRAWLEO_ENABLE_LIVE_TESTS');
assert(readme.includes('npm run test:live'), 'README.md must document test:live');
assert(skillText.includes('CRAWLEO_ENABLE_LIVE_TESTS'), 'SKILL.md must document CRAWLEO_ENABLE_LIVE_TESTS');
assert(skillText.includes('npm run test:live'), 'SKILL.md must document test:live');
assert(coverageText.includes('npm run test:live'), 'coverage checklist must document test:live');
assert(readme.includes('offline'), 'README.md must document offline verification posture');
assert(readme.includes('createCrawleoClient'), 'README.md must document createCrawleoClient');
assert(readme.includes('client.search'), 'README.md must document runtime wrapper methods');
assert(readme.includes('contracts/crawleo-endpoints.json'), 'README.md must point to contract JSON');
assert(readme.includes('contracts/coverage-checklist.md'), 'README.md must point to coverage checklist');
assert(skillText.includes('contracts/coverage-checklist.md'), 'SKILL.md must point to coverage checklist');
assert(readme.includes('https://api.crawleo.dev/mcp'), 'README.md must mention optional Crawleo MCP endpoint');
assert(skillText.includes('not specified in Crawleo docs'), 'SKILL.md must include ambiguity policy');
assert(skillText.includes('createCrawleoClient'), 'SKILL.md must document the client factory');

let publicApi = {};
try {
  publicApi = await import(new URL('../src/index.js', import.meta.url));
} catch (error) {
  fail(`src/index.js could not be imported: ${error.message}`);
}

for (const exportName of requiredExports) {
  assert(typeof publicApi[exportName] !== 'undefined', `src/index.js must export ${exportName}`);
}

for (const wrapperName of ['search', 'googleSearch', 'googleMaps', 'crawl', 'headfulBrowser']) {
  assert(typeof publicApi[wrapperName] === 'function', `${wrapperName} export must be a function`);
}

assert(typeof publicApi.createCrawleoClient === 'function', 'createCrawleoClient export must be a function');

for (const wrapperMention of requiredWrapperMentions) {
  assert(readme.includes(wrapperMention), `README.md must mention ${wrapperMention}`);
  assert(coverageText.includes(wrapperMention), `coverage checklist must mention ${wrapperMention}`);
}

if (process.exitCode) {
  console.error('Crawleo scaffold verification failed.');
  process.exit(process.exitCode);
}

console.log(`Crawleo scaffold verification passed: ${requiredFiles.length} files, ${requiredEndpoints.length} endpoints, ${requiredTools.length} MCP tools, ${requiredExports.length} public exports.`);
