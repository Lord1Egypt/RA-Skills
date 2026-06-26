/**
 * Parse various proxy protocol URLs into mihomo proxy format
 */

import { parse as parseYaml } from 'yaml';

const SUBSCRIPTION_TIMEOUT_MS = 30000;
const MAX_SUBSCRIPTION_BYTES = 10 * 1024 * 1024;

function normalizeBase64(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/').replace(/\s+/g, '');
  const padding = normalized.length % 4;
  return padding ? normalized + '='.repeat(4 - padding) : normalized;
}

function decodeBase64(value) {
  return Buffer.from(normalizeBase64(value), 'base64').toString('utf8');
}

function splitAtFirst(value, delimiter) {
  const index = value.indexOf(delimiter);
  if (index === -1) return [value, ''];
  return [value.slice(0, index), value.slice(index + delimiter.length)];
}

function splitAtLast(value, delimiter) {
  const index = value.lastIndexOf(delimiter);
  if (index === -1) return [value, ''];
  return [value.slice(0, index), value.slice(index + delimiter.length)];
}

function parseHostPort(value) {
  if (!value) throw new Error('Invalid SS host: missing server');

  if (value.startsWith('[')) {
    const closing = value.indexOf(']');
    const portStart = value.lastIndexOf(':');
    if (closing === -1 || portStart <= closing) {
      throw new Error('Invalid SS host: missing port');
    }
    return {
      server: value.slice(1, closing),
      port: value.slice(portStart + 1)
    };
  }

  const portStart = value.lastIndexOf(':');
  if (portStart === -1) throw new Error('Invalid SS host: missing port');

  return {
    server: value.slice(0, portStart),
    port: value.slice(portStart + 1)
  };
}

function parseMethodPassword(value) {
  const separator = value.indexOf(':');
  if (separator === -1) {
    throw new Error('Invalid SS credentials');
  }

  return {
    method: value.slice(0, separator),
    password: value.slice(separator + 1)
  };
}

async function readResponseText(response, maxBytes) {
  const contentLength = Number(response.headers.get('content-length') || 0);
  if (contentLength > maxBytes) {
    throw new Error(`Subscription too large: ${contentLength} bytes exceeds ${maxBytes} bytes`);
  }

  if (!response.body) {
    return response.text();
  }

  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    total += value.byteLength;
    if (total > maxBytes) {
      reader.releaseLock();
      throw new Error(`Subscription too large: exceeds ${maxBytes} bytes`);
    }

    chunks.push(Buffer.from(value));
  }

  return Buffer.concat(chunks).toString('utf8');
}

export function parseProxyUrl(url) {
  if (url.startsWith('vmess://')) return parseVmess(url);
  if (url.startsWith('ss://')) return parseSS(url);
  if (url.startsWith('trojan://')) return parseTrojan(url);
  if (url.startsWith('vless://')) return parseVless(url);
  throw new Error(`Unsupported protocol: ${url.split('://')[0]}`);
}

function parseVmess(url) {
  const b64 = url.replace('vmess://', '');
  const data = JSON.parse(decodeBase64(b64));
  return {
    name: data.ps || `vmess-${data.add}`,
    type: 'vmess',
    server: data.add,
    port: parseInt(data.port),
    uuid: data.id,
    alterId: parseInt(data.aid || 0),
    cipher: data.scy || 'auto',
    udp: true,
    ...(data.net === 'ws' ? {
      network: 'ws',
      'ws-opts': {
        path: data.path || '/',
        ...(data.host ? { headers: { Host: data.host } } : {})
      }
    } : {}),
    ...(data.tls === 'tls' ? { tls: true, servername: data.sni || data.host || data.add } : {})
  };
}

function parseSS(url) {
  // ss://base64(method:password)@server:port#name
  // or ss://base64(method:password@server:port)#name
  const cleaned = url.replace('ss://', '');
  const [mainWithQuery, fragment] = splitAtFirst(cleaned, '#');
  const [main] = splitAtFirst(mainWithQuery, '?');
  const name = fragment ? decodeURIComponent(fragment) : undefined;

  let method;
  let password;
  let server;
  let port;

  if (main.includes('@')) {
    const [userinfoEncoded, hostport] = splitAtLast(main, '@');
    const decodedUserinfo = (() => {
      try {
        return decodeBase64(userinfoEncoded);
      } catch {
        return decodeURIComponent(userinfoEncoded);
      }
    })();

    ({ method, password } = parseMethodPassword(decodedUserinfo));
    ({ server, port } = parseHostPort(hostport));
  } else {
    const decoded = decodeBase64(main);
    const [userinfo, hostport] = splitAtLast(decoded, '@');
    ({ method, password } = parseMethodPassword(userinfo));
    ({ server, port } = parseHostPort(hostport));
  }

  return {
    name: name || `ss-${server}`,
    type: 'ss',
    server,
    port: parseInt(port),
    cipher: method,
    password,
    udp: true
  };
}

function parseTrojan(url) {
  const u = new URL(url);
  return {
    name: u.hash ? decodeURIComponent(u.hash.slice(1)) : `trojan-${u.hostname}`,
    type: 'trojan',
    server: u.hostname,
    port: parseInt(u.port),
    password: u.username,
    udp: true,
    sni: u.searchParams.get('sni') || u.hostname,
    'skip-cert-verify': u.searchParams.get('allowInsecure') === '1'
  };
}

function parseVless(url) {
  const u = new URL(url);
  return {
    name: u.hash ? decodeURIComponent(u.hash.slice(1)) : `vless-${u.hostname}`,
    type: 'vless',
    server: u.hostname,
    port: parseInt(u.port),
    uuid: u.username,
    udp: true,
    tls: u.searchParams.get('security') === 'tls',
    servername: u.searchParams.get('sni') || u.hostname,
    flow: u.searchParams.get('flow') || '',
    ...(u.searchParams.get('type') === 'ws' ? {
      network: 'ws',
      'ws-opts': {
        path: u.searchParams.get('path') || '/',
        headers: { Host: u.searchParams.get('host') || u.hostname }
      }
    } : {})
  };
}

export async function fetchSubscription(url) {
  const res = await fetch(url, { signal: AbortSignal.timeout(SUBSCRIPTION_TIMEOUT_MS) });
  if (!res.ok) throw new Error(`Subscription fetch failed: ${res.status}`);
  const text = await readResponseText(res, MAX_SUBSCRIPTION_BYTES);

  // Try YAML (clash/mihomo format)
  try {
    const parsed = parseYaml(text);
    if (parsed && Array.isArray(parsed.proxies) && parsed.proxies.length > 0) {
      return { format: 'clash', raw: text, config: parsed };
    }
  } catch {}

  const trimmed = text.trim();

  // Try base64 encoded list
  try {
    const decoded = decodeBase64(trimmed);
    const lines = decoded
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.match(/^(vmess|ss|trojan|vless):\/\//));

    if (lines.length > 0) {
      const proxies = lines.map(line => parseProxyUrl(line));
      return { format: 'base64', proxies };
    }
  } catch {}

  // Try line-by-line URLs
  const lines = text
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.match(/^(vmess|ss|trojan|vless):\/\//));

  if (lines.length) {
    const proxies = lines.map(line => parseProxyUrl(line));
    return { format: 'urls', proxies };
  }

  throw new Error('Unable to parse subscription format');
}
