import { log } from './logger.js';

const API_TIMEOUT_MS = 5000;

function apiUrl(config, path) {
  return `${config.mihomo.api}${path}`;
}

function headers(config) {
  const h = { 'Content-Type': 'application/json' };
  if (config.mihomo.secret) h['Authorization'] = `Bearer ${config.mihomo.secret}`;
  return h;
}

function fetchWithTimeout(url, options = {}) {
  return fetch(url, {
    signal: AbortSignal.timeout(API_TIMEOUT_MS),
    ...options,
  });
}

export async function status(config) {
  try {
    const [proxyRes, versionRes] = await Promise.all([
      fetchWithTimeout(apiUrl(config, `/proxies/${encodeURIComponent(config.selector)}`), { headers: headers(config) }),
      fetchWithTimeout(apiUrl(config, '/version'), { headers: headers(config) })
    ]);

    if (!proxyRes.ok) throw new Error(`API error: ${proxyRes.status}`);

    const proxy = await proxyRes.json();
    const version = versionRes.ok ? await versionRes.json() : {};

    const allRes = await fetchWithTimeout(apiUrl(config, '/proxies'), { headers: headers(config) });
    const all = await allRes.json();
    const skipTypes = new Set(['Selector', 'URLTest', 'Fallback', 'Direct', 'Reject', 'Compatible', 'Pass']);
    const proxies = Object.values(all.proxies || {});
    const alive = proxies.filter(p => p.alive && !skipTypes.has(p.type)).length;
    const total = proxies.filter(p => !skipTypes.has(p.type)).length;

    const hist = proxy.history || [];
    const delay = hist.length ? hist[hist.length - 1].delay : 0;

    return {
      running: true,
      node: proxy.now || '',
      delay,
      version: version.version || '',
      selector: config.selector,
      alive,
      total
    };
  } catch (e) {
    if (e.cause?.code === 'ECONNREFUSED') {
      return { running: false, error: 'mihomo not running' };
    }
    throw e;
  }
}

export async function listNodes(config) {
  const res = await fetchWithTimeout(apiUrl(config, '/proxies'), { headers: headers(config) });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  const data = await res.json();
  const skipTypes = new Set(['Selector', 'URLTest', 'Fallback', 'Direct', 'Reject', 'Compatible', 'Pass']);

  return Object.entries(data.proxies || {})
    .filter(([_, v]) => !skipTypes.has(v.type))
    .map(([name, v]) => {
      const hist = v.history || [];
      return {
        name,
        type: v.type,
        alive: v.alive || false,
        delay: hist.length ? hist[hist.length - 1].delay : 0
      };
    })
    .sort((a, b) => (a.alive === b.alive ? a.delay - b.delay : a.alive ? -1 : 1));
}

export async function switchNode(config, nodeName) {
  const currentStatus = await status(config);
  const from = currentStatus.node;

  if (!nodeName) {
    const nodes = await listNodes(config);
    const priorities = config.watchdog.nodePriority || [];
    const maxDelay = config.watchdog.maxDelay || 3000;

    const candidates = nodes
      .filter(n => n.alive && n.delay > 0 && n.delay < maxDelay && n.name !== from)
      .map(n => {
        let pri = priorities.length;
        for (let i = 0; i < priorities.length; i++) {
          if (n.name.includes(priorities[i])) { pri = i; break; }
        }
        return { ...n, pri };
      })
      .sort((a, b) => a.pri - b.pri || a.delay - b.delay);

    if (!candidates.length) throw new Error('No suitable node found');
    nodeName = candidates[0].name;
  }

  const res = await fetchWithTimeout(
    apiUrl(config, `/proxies/${encodeURIComponent(config.selector)}`),
    {
      method: 'PUT',
      headers: headers(config),
      body: JSON.stringify({ name: nodeName })
    }
  );

  if (!res.ok) throw new Error(`Switch failed: ${res.status} ${await res.text()}`);

  return { switched: true, from, to: nodeName };
}

export async function testEndpoints(config) {
  const endpoints = config.watchdog.endpoints || [];
  for (const ep of endpoints) {
    try {
      const res = await fetch(ep.url, { signal: AbortSignal.timeout(8000) });
      if (res.status === ep.expect) return { ok: true, url: ep.url, status: res.status };
    } catch {}
  }
  return { ok: false };
}
