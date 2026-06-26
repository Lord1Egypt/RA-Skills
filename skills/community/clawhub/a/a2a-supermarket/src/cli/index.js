#!/usr/bin/env node

const WELL_KNOWN_PATHS = ['/.well-known/ucp', '/.well-known/ucp.json'];

function parseArgv(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      flags[key] = next;
      i += 1;
    } else {
      flags[key] = true;
    }
  }
  return flags;
}

function toPositiveInt(value, fallback = null) {
  const numeric = Number(value);
  if (!Number.isInteger(numeric) || numeric <= 0) {
    return fallback;
  }
  return numeric;
}

function toBoolean(value, fallback = true) {
  if (value === undefined || value === null || value === '') {
    return fallback;
  }
  if (typeof value === 'boolean') {
    return value;
  }
  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'y'].includes(normalized)) {
    return true;
  }
  if (['false', '0', 'no', 'n'].includes(normalized)) {
    return false;
  }
  return fallback;
}

async function readStdinJson() {
  if (process.stdin.isTTY) {
    return {};
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) {
    return {};
  }
  return JSON.parse(raw);
}

async function fetchJsonOrThrow(url, options = {}) {
  const response = await fetch(url, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.error ?? `HTTP ${response.status} ${url}`);
  }
  return body;
}

function normalizeDomain(domainInput) {
  const raw = String(domainInput ?? '').trim();
  if (!raw) {
    throw new Error('domain is required');
  }
  if (raw.startsWith('http://') || raw.startsWith('https://')) {
    const cleanBaseUrl = raw.replace(/\/+$/, '');
    return {
      cleanDomain: cleanBaseUrl.replace(/^https?:\/\//, ''),
      baseCandidates: [cleanBaseUrl]
    };
  }
  const cleanDomain = raw.replace(/\/+$/, '');
  return {
    cleanDomain,
    baseCandidates: [`https://${cleanDomain}`, `http://${cleanDomain}`]
  };
}

function resolveShoppingRestEndpoint(profile) {
  const services = profile?.ucp?.services ?? {};
  for (const value of Object.values(services)) {
    const list = Array.isArray(value) ? value : [value];
    for (const service of list) {
      const endpoint = service?.rest?.endpoint;
      if (endpoint) {
        return endpoint.replace(/\/+$/, '');
      }
    }
  }
  throw new Error('No UCP REST endpoint found in services');
}

async function discoverUcp(domainInput) {
  const { cleanDomain, baseCandidates } = normalizeDomain(domainInput);

  for (const base of baseCandidates) {
    for (const path of WELL_KNOWN_PATHS) {
      const profileUrl = `${base}${path}`;
      try {
        const response = await fetch(profileUrl);
        if (!response.ok) {
          continue;
        }
        const profile = await response.json();
        if (!profile?.ucp) {
          continue;
        }
        return {
          domain: cleanDomain,
          profile,
          profileUrl,
          endpoint: resolveShoppingRestEndpoint(profile)
        };
      } catch {
      }
    }
  }

  throw new Error(`No UCP profile found for ${domainInput}`);
}

async function runSellerPublish(input, discovery) {
  const name = String(input.name ?? '').trim();
  if (!name) {
    throw new Error('seller publish requires name');
  }

  const amountMinorUnits = toPositiveInt(
    input['price-minor-units'] ?? input.amountMinorUnits ?? input.priceMinorUnits
  );
  if (!amountMinorUnits) {
    throw new Error('seller publish requires positive integer price-minor-units');
  }

  const payload = {
    id: input['product-id'] ?? input.productId,
    name,
    description: String(input.description ?? `${name} listed via a2a-supermarket skill.`).trim(),
    category: String(input.category ?? 'General').trim() || 'General',
    inStock: toBoolean(input['in-stock'] ?? input.inStock, true),
    price: {
      amountMinorUnits,
      currency: String(input.currency ?? 'USD').trim() || 'USD'
    }
  };

  return fetchJsonOrThrow(`${discovery.endpoint}/products`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload)
  });
}

async function runBuyerDiscover(input, discovery) {
  const query = String(input.query ?? '').trim();
  const category = String(input.category ?? '').trim();
  const listAll = toBoolean(input.all ?? input['list-all'] ?? input.listAll, false);
  const limit = listAll ? null : toPositiveInt(input.limit, 10);

  const base = `${discovery.endpoint}/products`;
  const url = query
    ? `${discovery.endpoint}/products/search?q=${encodeURIComponent(query)}`
    : (category ? `${base}?category=${encodeURIComponent(category)}` : base);

  const payload = await fetchJsonOrThrow(url);
  const rawProducts = Array.isArray(payload.products) ? payload.products : [];
  const products = Number.isInteger(limit) ? rawProducts.slice(0, limit) : rawProducts;
  return {
    products,
    total: payload.total ?? products.length,
    returned: products.length,
    listAll,
    query: query || null,
    category: category || null
  };
}

async function main() {
  const flags = parseArgv(process.argv.slice(2));
  const stdinInput = await readStdinJson().catch(() => ({}));
  const input = { ...stdinInput, ...flags };

  const role = String(input.role ?? 'buyer').trim().toLowerCase();
  if (!['buyer', 'seller'].includes(role)) {
    throw new Error('role must be buyer or seller');
  }

  const discovery = await discoverUcp(input.domain);
  if (role === 'seller') {
    const published = await runSellerPublish(input, discovery);
    process.stdout.write(`${JSON.stringify({
      ok: true,
      role,
      mode: 'seller_publish',
      domain: discovery.domain,
      endpoint: discovery.endpoint,
      result: published
    }, null, 2)}\n`);
    return;
  }

  const discovered = await runBuyerDiscover(input, discovery);
  process.stdout.write(`${JSON.stringify({
    ok: true,
    role,
    mode: 'buyer_discover',
    domain: discovery.domain,
    endpoint: discovery.endpoint,
    result: discovered
  }, null, 2)}\n`);
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  process.stdout.write(`${JSON.stringify({
    ok: false,
    error: message,
    hint: 'Provide --domain. seller requires --name and --price-minor-units; buyer may pass --query or --category or --all true.'
  }, null, 2)}\n`);
  process.exitCode = 1;
});
