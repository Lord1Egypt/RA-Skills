#!/usr/bin/env node
'use strict';

/**
 * Unified Clawprint API CLI — discovery via GET /api/products, then any documented route.
 *
 * Usage:
 *   node scripts/clawprint.js
 *   node scripts/clawprint.js --path /api/users --method POST --body '{"email":"a@b.com","display_name":"x"}'
 *   node scripts/clawprint.js --product create_user --body '{"email":"a@b.com","display_name":"x"}'
 *   node scripts/clawprint.js --path /api/businesses/biz_123/status --public-key 'public_…' --secret-key 'secret_…'
 */

const fs = require('fs');
const { buildClawprintUrl, clawprintRequest } = require('../lib/clawprint-http');

function printHelp() {
  console.log(`Clawprint API CLI

Default (no args): GET /api/products — fetch the products list (no auth).

Options:
  --method METHOD     HTTP method (default: GET)
  --path PATH         Path as listed in the products response, e.g. /api/users or /api/products
  --product ID        Resolve method + path from the products list entry with this id (GET /api/products first)
  --query STRING      Query string without "?", appended to path
  --body JSON         JSON body (string). Use @file.json to read from file
  --no-auth           Do not send X-Public-Key / X-Secret-Key
  --public-key KEY    Override CLAWPRINT_PUBLIC_KEY for this request
  --secret-key KEY    Override CLAWPRINT_SECRET_KEY for this request
  -h, --help          Show this help

Environment:
  CLAWPRINT_SITE_URL — deployment origin (e.g. Convex); paths use /api/…
  CLAWPRINT_API_URL — API root including /api (default: https://clawprintai.com/api)
  CLAWPRINT_PUBLIC_KEY — from POST /api/users response \`public_key\`
  CLAWPRINT_SECRET_KEY — from POST /api/users response \`secret_key\`

Examples:
  node scripts/clawprint
  node scripts/clawprint --path /api/users --method POST --no-auth \\
    --body '{"email":"you@example.com","display_name":"Agent"}'
`);
}

function parseArgs(argv) {
  const opts = {
    method: 'GET',
    methodExplicit: false,
    path: null,
    product: null,
    query: '',
    body: undefined,
    auth: true,
    publicKey: null,
    secretKey: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      opts.help = true;
      continue;
    }
    if (a === '--no-auth') {
      opts.auth = false;
      continue;
    }
    const take = (key) => {
      const v = argv[++i];
      if (v === undefined) throw new Error(`Missing value for ${a}`);
      opts[key] = v;
    };
    switch (a) {
      case '--method':
        opts.methodExplicit = true;
        take('method');
        break;
      case '--path':
        take('path');
        break;
      case '--product':
        take('product');
        break;
      case '--query':
        take('query');
        break;
      case '--body':
        take('bodyRaw');
        break;
      case '--public-key':
        take('publicKey');
        break;
      case '--secret-key':
        take('secretKey');
        break;
      default:
        throw new Error(`Unknown argument: ${a}`);
    }
  }

  if (opts.bodyRaw !== undefined) {
    let raw = opts.bodyRaw;
    if (raw.startsWith('@')) {
      const fp = raw.slice(1);
      raw = fs.readFileSync(fp, 'utf8');
    }
    try {
      opts.body = JSON.parse(raw);
    } catch (e) {
      throw new Error(`Invalid JSON in --body: ${e.message}`);
    }
  }

  return opts;
}

async function loadProducts() {
  const url = buildClawprintUrl('/api/products');
  const res = await clawprintRequest({
    method: 'GET',
    url,
    auth: false,
  });
  return res.body;
}

function main() {
  let opts;
  try {
    opts = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(e.message);
    console.error('Try: node scripts/clawprint --help');
    process.exit(1);
  }

  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  run(opts).catch((err) => {
    console.error(err.message || String(err));
    if (err.response) {
      console.error(JSON.stringify(err.response, null, 2));
    }
    process.exit(1);
  });
}

async function run(opts) {
  let method = (opts.method || 'GET').toUpperCase();
  let path = opts.path;

  if (opts.product) {
    const products = await loadProducts();
    if (!Array.isArray(products)) {
      throw new Error('GET /api/products did not return an array');
    }
    const entry = products.find((e) => e && e.id === opts.product);
    if (!entry) {
      const ids = products.map((e) => e.id).filter(Boolean);
      throw new Error(
        `Unknown product id "${opts.product}". Known ids: ${ids.join(', ') || '(none)'}`,
      );
    }
    if (!path) path = entry.path;
    if (!opts.methodExplicit) method = String(entry.method || 'GET').toUpperCase();
    else method = (opts.method || 'GET').toUpperCase();
  }

  if (!path) {
    path = '/api/products';
    method = 'GET';
    opts.auth = false;
  }

  let fullPath = path;
  if (opts.query) {
    const q = opts.query.startsWith('?') ? opts.query.slice(1) : opts.query;
    fullPath += (fullPath.includes('?') ? '&' : '?') + q;
  }

  const url = buildClawprintUrl(fullPath);

  const res = await clawprintRequest({
    method,
    url,
    body: method === 'GET' || method === 'HEAD' ? null : opts.body,
    auth: opts.auth,
    publicKey: opts.publicKey,
    secretKey: opts.secretKey,
  });

  console.log(JSON.stringify(res.body, null, 2));
}

main();
