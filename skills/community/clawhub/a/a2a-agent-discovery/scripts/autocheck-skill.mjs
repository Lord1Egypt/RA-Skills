#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const errors = [];
const warnings = [];

function fail(message) { errors.push(message); }
function warn(message) { warnings.push(message); }
function read(file) { return fs.readFileSync(path.join(root, file), 'utf8'); }

if (!fs.existsSync(path.join(root, 'SKILL.md'))) {
  fail('SKILL.md is missing');
} else {
  const skill = read('SKILL.md');
  const match = skill.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) {
    fail('SKILL.md frontmatter is missing');
  } else {
    const fm = match[1];
    const name = fm.match(/^name:\s*(.+)$/m)?.[1]?.trim();
    const description = fm.match(/^description:\s*(.+)$/m)?.[1]?.trim();
    if (!name) fail('frontmatter.name is missing');
    if (name && !/^[a-z0-9-]+$/.test(name)) fail('frontmatter.name must be lowercase/digit/hyphen slug');
    if (name && name !== 'a2a-agent-discovery') warn(`expected skill name a2a-agent-discovery, got ${name}`);
    if (!description) fail('frontmatter.description is missing');
    if (description && description.length > 160) fail('frontmatter.description must be <=160 chars');
    if (description && /\n/.test(description)) fail('frontmatter.description must be one line');
    if (!/homepage:\s*https:\/\/github\.com\/aihlp\/itinai/m.test(fm)) warn('homepage should point to canonical ITINAI repository');
    if (!/requires:/m.test(fm)) warn('metadata.openclaw.requires is not declared');
  }

  const body = skill.replace(/^---\n[\s\S]*?\n---\n/, '');
  for (const phrase of [
    'explicit user approval',
    'Do not create a new registry',
    'Never send secrets',
    'ITINAI is the board. Remote agents provide the services.',
    '{baseDir}/delegate-task.md'
  ]) {
    if (!body.includes(phrase)) warn(`SKILL.md missing expected guardrail: ${phrase}`);
  }
  const vagueTriggerPatterns = [
    /find, search, list, inspect, compare, buy through agents/i,
    /get another agent service/i,
    /another agent to do something, sell something, quote something/i,
    /post their own agent, publish an agent, register an offer/i,
    /create a service listing such as/i
  ];
  for (const pattern of vagueTriggerPatterns) {
    if (pattern.test(body)) fail(`SKILL.md contains vague trigger language: ${pattern}`);
  }
  if (!/Use this workflow only when the request explicitly mentions at least one activation term/.test(body)) {
    fail('SKILL.md search workflow must require explicit ITINAI/A2A activation terms');
  }
  if (!/Do not use this workflow for ordinary web search, shopping, local search, product comparison/.test(body)) {
    fail('SKILL.md search workflow must exclude ordinary non-A2A requests');
  }
  if (!/Use this workflow only after a specific remote agent has been selected/.test(body)) {
    fail('SKILL.md service-request workflow must require selected agent or explicit Agent Card endpoint');
  }
  if (!/Do not use this workflow for ordinary classified ads, social posts, marketplace listings/.test(body)) {
    fail('SKILL.md publish workflow must exclude ordinary listing/drafting tasks');
  }
  if (/\/mnt\/|C:\\|\/Users\//.test(body)) fail('SKILL.md contains hardcoded local absolute paths');
}

const textFiles = ['SKILL.md', 'README.md', 'publish-agent.md', 'search-agent.md', 'delegate-task.md', 'src/index.ts'];
for (const file of textFiles) {
  if (!fs.existsSync(path.join(root, file))) continue;
  const text = read(file);
  if (/itinai-submit-agent-card\.json/.test(text)) fail(`${file} references legacy itinai-submit-agent-card.json`);
  if (/curl\s+[^\n|]+\|\s*(bash|sh)|wget\s+[^\n|]+\|\s*(bash|sh)|eval\s*\(|base64\s+-d/.test(text)) fail(`${file} contains dangerous install/execution pattern`);
  if (/(api[_-]?key|token|password|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-.]{16,}/i.test(text)) fail(`${file} may contain a hardcoded secret`);
}

const src = fs.existsSync(path.join(root, 'src/index.ts')) ? read('src/index.ts') : '';
if (src) {
  for (const required of ['requireHttpsUrl(url, "request URL")', 'redirect: "manual"', 'MAX_JSON_BYTES', 'confirm_external_submission', 'request_agent_service', 'confirm_external_request']) {
    if (!src.includes(required)) fail(`src/index.ts missing ${required}`);
  }
  if (/data\s*=\s*\{ raw: text \}/.test(src)) fail('src/index.ts must reject invalid JSON instead of returning raw text');
}

if (errors.length || warnings.length) {
  console.log(JSON.stringify({ ok: errors.length === 0, errors, warnings }, null, 2));
} else {
  console.log(JSON.stringify({ ok: true, errors: [], warnings: [] }, null, 2));
}
process.exit(errors.length ? 1 : 0);
