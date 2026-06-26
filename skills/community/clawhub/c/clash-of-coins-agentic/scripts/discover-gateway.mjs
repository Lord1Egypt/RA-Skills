#!/usr/bin/env node

import process from 'node:process';

const DEFAULT_TIMEOUT_MS = 10000;
const MAX_TIMEOUT_MS = 120000;

const HELP_TEXT = `Clash of Coins discovery helper

Usage:
  node scripts/discover-gateway.mjs --origin <https://gateway.example> [options]

Required:
  --origin <url>         Target gateway origin.

Optional:
  --nickname <value>     Shop recipient nickname for personalized catalog probe.
  --address <0x...>      Shop recipient address for personalized catalog probe.
  --timeout-ms <number>  HTTP timeout per request in ms (default: ${DEFAULT_TIMEOUT_MS}).
  --help                 Show this help.

Rules:
  - Use exactly one origin per run.
  - Use either --nickname or --address, never both.
  - Script is non-interactive and always emits structured JSON to stdout.

Exit codes:
  0  success (at least one endpoint returned a response)
  2  invalid arguments
  3  network or connectivity failure (no endpoint returned a response)
`;

function fail(message, code = 2) {
  console.error(`Error: ${message}`);
  console.error("Run with '--help' for usage.");
  process.exit(code);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    switch (token) {
      case '--help':
        args.help = true;
        break;
      case '--origin':
      case '--nickname':
      case '--address':
      case '--timeout-ms': {
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          fail(`Missing value for ${token}.`);
        }
        args[token.slice(2)] = next;
        i += 1;
        break;
      }
      default:
        fail(`Unknown argument: ${token}`);
    }
  }
  return args;
}

function normalizeOrigin(input) {
  let url;
  try {
    url = new URL(input);
  } catch {
    fail(`Invalid --origin URL: ${input}`);
  }

  if (!['http:', 'https:'].includes(url.protocol)) {
    fail(`Origin must use http or https: ${input}`);
  }

  url.pathname = '/';
  url.search = '';
  url.hash = '';
  return url.toString().replace(/\/$/, '');
}

function readTimeout(value) {
  if (value == null) {
    return DEFAULT_TIMEOUT_MS;
  }
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0 || !Number.isInteger(parsed)) {
    fail(`--timeout-ms must be a positive integer, got: ${value}`);
  }
  if (parsed > MAX_TIMEOUT_MS) {
    fail(`--timeout-ms must be <= ${MAX_TIMEOUT_MS}, got: ${value}`);
  }
  return parsed;
}

async function probe(origin, path, timeoutMs) {
  const url = new URL(path, `${origin}/`).toString();
  const startedAt = Date.now();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      method: 'GET',
      redirect: 'follow',
      signal: controller.signal,
    });
    const text = await response.text();
    return {
      path,
      url,
      status: response.status,
      ok: response.ok,
      durationMs: Date.now() - startedAt,
      contentType: response.headers.get('content-type'),
      body: text,
    };
  } catch (error) {
    return {
      path,
      url,
      status: null,
      ok: false,
      durationMs: Date.now() - startedAt,
      contentType: null,
      body: '',
      error: error instanceof Error ? error.message : String(error),
    };
  } finally {
    clearTimeout(timeout);
  }
}

function safePreview(value, max = 180) {
  if (!value) {
    return null;
  }
  const oneLine = value.replace(/\s+/g, ' ').trim();
  if (!oneLine) {
    return null;
  }
  return oneLine.length > max ? `${oneLine.slice(0, max)}...` : oneLine;
}

function parseJsonIfPossible(text) {
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function collectPayableProtocolsFromOpenApi(resultEntry) {
  const openApi = parseJsonIfPossible(resultEntry?.body ?? '');
  const discovered = new Set();

  if (!openApi || typeof openApi !== 'object') {
    return discovered;
  }

  for (const [routePath, pathItem] of Object.entries(openApi.paths ?? {})) {
    if (!pathItem || typeof pathItem !== 'object') {
      continue;
    }
    for (const operation of Object.values(pathItem)) {
      if (!operation || typeof operation !== 'object') {
        continue;
      }
      const paymentInfo = operation['x-payment-info'];
      if (!paymentInfo || typeof paymentInfo !== 'object') {
        continue;
      }

      const declaredProtocols = Array.isArray(paymentInfo.protocols) ? paymentInfo.protocols : [];
      for (const protocol of declaredProtocols) {
        if (protocol === 'x402' || protocol === 'mpp') {
          discovered.add(protocol);
        }
      }

      // Fallback for legacy OpenAPI docs that omitted explicit protocols.
      if (declaredProtocols.length === 0) {
        if (routePath.includes('/x402/')) {
          discovered.add('x402');
        }
        if (routePath.includes('/mpp/')) {
          discovered.add('mpp');
        }
      }
    }
  }

  return discovered;
}

function protocolsFromStatus(results) {
  const getByPath = (path) => results.find((entry) => entry.path === path) ?? null;
  const has200 = (path) => results.find((entry) => entry.path === path)?.status === 200;
  const root = Array.from(collectPayableProtocolsFromOpenApi(getByPath('/openapi.json')));
  const shop = Array.from(collectPayableProtocolsFromOpenApi(getByPath('/shop/openapi.json')));

  if (root.length === 0) {
    const x402Document = parseJsonIfPossible(getByPath('/.well-known/x402')?.body ?? '');
    const x402Resources = Array.isArray(x402Document?.resources) ? x402Document.resources : [];
    if (x402Resources.length > 0) {
      root.push('x402');
    }
    if (has200('/.well-known/mpp')) {
      root.push('mpp');
    }
  }

  if (shop.length === 0) {
    if (has200('/shop/.well-known/x402')) {
      shop.push('x402');
    }
    if (has200('/shop/.well-known/mpp')) {
      shop.push('mpp');
    }
  }

  return {
    root: Array.from(new Set(root)),
    shop: Array.from(new Set(shop)),
  };
}

function summarizeCatalog(catalogResult) {
  const summary = {
    status: catalogResult?.status ?? null,
    totalItems: null,
    saleItems: null,
    shopItems: null,
    mismatchedPurchaseUrls: [],
  };

  const catalog = parseJsonIfPossible(catalogResult?.body ?? '');
  const items = Array.isArray(catalog?.items) ? catalog.items : null;
  if (!items) {
    return summary;
  }

  let saleItems = 0;
  let shopItems = 0;
  for (const item of items) {
    if (item?.surface === 'sale') {
      saleItems += 1;
    }
    if (item?.surface === 'shop') {
      shopItems += 1;
    }

    const purchaseUrl = typeof item?.purchaseUrl === 'string' ? item.purchaseUrl : '';
    if (!purchaseUrl) {
      continue;
    }

    const looksLikeShop = purchaseUrl.includes('/shop/');
    const looksLikeSale = purchaseUrl.includes('/agentic/');
    if (item?.surface === 'sale' && looksLikeShop) {
      summary.mismatchedPurchaseUrls.push({
        catalogId: item.catalogId ?? null,
        surface: item.surface,
        purchaseUrl,
      });
    }
    if (item?.surface === 'shop' && looksLikeSale) {
      summary.mismatchedPurchaseUrls.push({
        catalogId: item.catalogId ?? null,
        surface: item.surface,
        purchaseUrl,
      });
    }
  }

  summary.totalItems = items.length;
  summary.saleItems = saleItems;
  summary.shopItems = shopItems;
  return summary;
}

function buildRecommendations(protocols, catalog, recipient) {
  const recommendations = [];

  if (protocols.root.length === 0 && protocols.shop.length === 0) {
    recommendations.push(
      'No payable protocol was discovered from OpenAPI or well-known docs. Re-check origin and deployment runtime config.'
    );
  }

  if (catalog.mismatchedPurchaseUrls.length > 0) {
    recommendations.push(
      'Catalog purchaseUrl mapping contains surface mismatches. Route by surface and protocol metadata, not assumptions.'
    );
  }

  if ((catalog.shopItems ?? 0) > 0 && !recipient.nickname && !recipient.address) {
    recommendations.push(
      'Shop items detected. Provide --nickname or --address before quote/buy validation for recipient-scoped checks.'
    );
  }

  if (recommendations.length === 0) {
    recommendations.push(
      'Discovery is consistent. Continue with quote/buy flow using catalog purchaseUrl and protocol metadata.'
    );
  }

  return recommendations;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(HELP_TEXT);
    return;
  }

  if (!args.origin) {
    fail('Missing required --origin.');
  }
  if (args.nickname && args.address) {
    fail('Use either --nickname or --address, not both.');
  }

  const timeoutMs = readTimeout(args['timeout-ms']);
  const origin = normalizeOrigin(args.origin);
  const recipient = {
    nickname: args.nickname ?? null,
    address: args.address ?? null,
  };

  const recipientQuery = recipient.nickname
    ? `nickname=${encodeURIComponent(recipient.nickname)}`
    : recipient.address
      ? `address=${encodeURIComponent(recipient.address)}`
      : null;

  const paths = [
    '/',
    '/health',
    '/openapi.json',
    '/openapi.full.json',
    '/mcp.json',
    '/skills/index.json',
    '/catalog',
    '/.well-known/agent.json',
    '/.well-known/agents.json',
    '/.well-known/x402',
    '/.well-known/mpp',
    '/llms.txt',
    '/skill.md',
    '/shop',
    '/shop/health',
    '/shop/openapi.json',
    '/shop/openapi.full.json',
    '/shop/llms.txt',
    '/shop/skill.md',
    '/shop/api/shop/items',
    '/shop/.well-known/agent.json',
    '/shop/.well-known/agents.json',
    '/shop/.well-known/x402',
    '/shop/.well-known/mpp',
  ];
  if (recipientQuery) {
    paths.push(`/shop/api/shop/items?${recipientQuery}`);
  }

  const results = [];
  for (const path of paths) {
    results.push(await probe(origin, path, timeoutMs));
  }

  const protocols = protocolsFromStatus(results);
  const catalogSummary = summarizeCatalog(results.find((entry) => entry.path === '/catalog'));
  const recommendations = buildRecommendations(protocols, catalogSummary, recipient);

  const summary = {
    origin,
    generatedAt: new Date().toISOString(),
    timeoutMs,
    recipient,
    protocols,
    catalog: catalogSummary,
    endpoints: results.map((entry) => ({
      path: entry.path,
      url: entry.url,
      status: entry.status,
      ok: entry.ok,
      durationMs: entry.durationMs,
      contentType: entry.contentType,
      bodyPreview: safePreview(entry.body),
      error: entry.error ?? null,
    })),
    recommendations,
  };

  console.log(JSON.stringify(summary, null, 2));

  const allUnreachable = results.every((entry) => entry.status === null);
  if (allUnreachable) {
    process.exit(3);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(3);
});
