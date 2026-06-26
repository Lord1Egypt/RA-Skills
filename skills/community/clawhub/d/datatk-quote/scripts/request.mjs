#!/usr/bin/env node

import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

function usage() {
  console.error(
    'Usage: request.mjs --path /Api/V1/... --body \'{"instrument":"US|AAPL"}\''
  );
  console.error('Config: datatk-quote-skill/env.json');
  process.exit(2);
}

function getArg(args, name) {
  const index = args.indexOf(name);
  if (index === -1) {
    return '';
  }
  return String(args[index + 1] ?? '').trim();
}

function trimTrailingSlash(value) {
  return value.endsWith('/') ? value.slice(0, -1) : value;
}

async function readConfigFile() {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const configPath = join(scriptDir, '..', 'env.json');

  try {
    const raw = await readFile(configPath, 'utf8');
    const parsed = JSON.parse(raw);
    return {
      endpoint: String(parsed.endpoint ?? '').trim(),
      apiKey: String(parsed.apiKey ?? '').trim(),
    };
  } catch (error) {
    return {
      endpoint: '',
      apiKey: '',
    };
  }
}

export async function resolveConfig() {
  const fileConfig = await readConfigFile();
  return {
    endpoint: String(fileConfig.endpoint || '').trim(),
    ak: String(fileConfig.apiKey || '').trim(),
  };
}

function isPlaceholderValue(value) {
  return value.includes('<') || value.includes('>');
}

function assertSafeEndpoint(endpoint) {
  let url;
  try {
    url = new URL(endpoint);
  } catch {
    throw new Error(`Invalid endpoint URL: ${endpoint}`);
  }

  // Only allow HTTPS
  if (url.protocol !== 'https:') {
    throw new Error('Endpoint must use https');
  }

  const host = url.hostname.toLowerCase();

  // Disallow raw IP endpoints (common exfiltration pattern)
  if (/^\d{1,3}(?:\.\d{1,3}){3}$/.test(host)) {
    throw new Error('Endpoint must be a domain name (IP endpoints are not allowed)');
  }

  // Allowlist known datatk domains. Adjust here if you use a private gateway.
  const allowedHosts = new Set([
    'quote.datatk.com',
    'www.datatk.com',
  ]);

  const allowedSuffixes = ['.datatk.com'];

  const isAllowed =
    allowedHosts.has(host) || allowedSuffixes.some((suffix) => host.endsWith(suffix));

  if (!isAllowed) {
    throw new Error(
      `Endpoint host not allowlisted: ${host}. Edit scripts/request.mjs allowlist if you use a private gateway.`
    );
  }

  return url;
}

function assertSafePath(path) {
  if (!path || typeof path !== 'string') {
    throw new Error('Missing request path');
  }
  if (!path.startsWith('/Api/')) {
    throw new Error('Path must start with /Api/');
  }
  if (path.includes('..')) {
    throw new Error('Path must not include ..');
  }
}

export async function postJson({ endpoint, ak, path, body }) {
  const normalizedEndpoint = trimTrailingSlash(endpoint);
  const safeEndpointUrl = assertSafeEndpoint(normalizedEndpoint);
  assertSafePath(path);

  const url = `${safeEndpointUrl.origin}${path}`;

  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      'X-API-KEY': ak,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const text = await resp.text();
  if (!resp.ok) {
    console.error(`HTTP ${resp.status} ${resp.statusText}`);
    if (text) {
      console.error(text);
    }
    process.exit(1);
  }

  console.log(text);
}

function isDirectExecution() {
  if (!process.argv[1]) {
    return false;
  }
  return fileURLToPath(import.meta.url) === process.argv[1];
}

if (isDirectExecution()) {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    usage();
  }

  const config = await resolveConfig();
  const path = getArg(args, '--path');
  const rawBody = getArg(args, '--body');

  if (!config.endpoint) {
    console.error('Missing endpoint. Configure datatk-quote-skill/env.json');
    process.exit(1);
  }
  if (!config.ak) {
    console.error('Missing API key. Configure datatk-quote-skill/env.json');
    process.exit(1);
  }
  if (isPlaceholderValue(config.endpoint)) {
    console.error('Invalid endpoint config. Replace the placeholder value in datatk-quote-skill/env.json');
    process.exit(1);
  }
  if (isPlaceholderValue(config.ak)) {
    console.error('Invalid API key config. Replace the placeholder value in datatk-quote-skill/env.json');
    process.exit(1);
  }
  if (!path || !rawBody) {
    usage();
  }

  let body;
  try {
    body = JSON.parse(rawBody);
  } catch (error) {
    console.error(`Invalid JSON for --body: ${error.message}`);
    process.exit(1);
  }

  await postJson({ endpoint: config.endpoint, ak: config.ak, path, body });
}
