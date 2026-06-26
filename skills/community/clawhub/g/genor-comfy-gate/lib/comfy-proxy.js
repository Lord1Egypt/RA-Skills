import crypto from 'crypto';
import { fetchJson, SERVERS, queryAllServers, pickServer, recordSuccess, recordFailure } from './load-balancer.js';

/** Maps proxy prompt_id → { serverId, serverPromptId, server } */
export const promptMap = new Map();

const AUDIO_EXT = new Set(['mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac']);
const IMAGE_EXT = new Set(['png', 'jpg', 'jpeg', 'webp', 'gif']);

function contentTypeFromFilename(filename) {
  const ext = (filename || '').split('.').pop()?.toLowerCase() || '';
  if (AUDIO_EXT.has(ext)) {
    if (ext === 'wav') return 'audio/wav';
    if (ext === 'flac') return 'audio/flac';
    if (ext === 'ogg') return 'audio/ogg';
    return 'audio/mpeg';
  }
  if (IMAGE_EXT.has(ext)) {
    if (ext === 'jpg' || ext === 'jpeg') return 'image/jpeg';
    if (ext === 'webp') return 'image/webp';
    if (ext === 'gif') return 'image/gif';
    return 'image/png';
  }
  return null;
}

export function registerPrompt(ourPromptId, server, upstreamPromptId, extra = {}) {
  promptMap.set(ourPromptId, {
    serverId: server.id,
    serverPromptId: upstreamPromptId,
    server,
    ...extra,
  });
  promptMap.set(upstreamPromptId, {
    serverId: server.id,
    serverPromptId: upstreamPromptId,
    server,
    aliased: true,
    ...extra,
  });
}

/**
 * @param {typeof SERVERS} servers
 * @param {object} body
 */
export async function submitPrompt(servers, body) {
  const results = await queryAllServers(servers);
  const server = pickServer(servers, results);
  if (!server) {
    return { error: 'All ComfyUI servers offline or unreachable', status: 503 };
  }

  const payload = { ...body };
  if (!payload.client_id) payload.client_id = crypto.randomUUID();

  try {
    const upstream = await fetch(`${server.url}/prompt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(30000),
    });
    const upstreamData = await upstream.json();
    if (!upstream.ok) {
      recordFailure(server.id);
      return { status: upstream.status, data: upstreamData };
    }
    recordSuccess(server.id);
    const upstreamPromptId = upstreamData.prompt_id;
    const ourPromptId = crypto.randomUUID();
    registerPrompt(ourPromptId, server, upstreamPromptId);
    return {
      status: 200,
      data: {
        prompt_id: ourPromptId,
        number: upstreamData.number,
        node_errors: upstreamData.node_errors,
        upstream_prompt_id: upstreamPromptId,
        server: server.id,
      },
    };
  } catch (err) {
    recordFailure(server.id);
    return { status: 502, data: { error: `Failed to forward to server ${server.id}: ${err.message}` } };
  }
}

export async function getHistoryForPrompt(promptId) {
  const mapEntry = promptMap.get(promptId);
  if (!mapEntry) return { status: 404, data: { error: 'Unknown prompt_id' } };
  try {
    const upstream = await fetch(`${mapEntry.server.url}/history/${mapEntry.serverPromptId}`, {
      signal: AbortSignal.timeout(10000),
    });
    const data = await upstream.json();
    return { status: upstream.status, data };
  } catch (err) {
    return {
      status: 502,
      data: { error: `Failed to fetch history from server ${mapEntry.serverId}: ${err.message}` },
    };
  }
}

export async function getAggregatedHistory(maxItems = 200) {
  const results = {};
  await Promise.all(
    SERVERS.map(async (server) => {
      try {
        const { data } = await fetchJson(`${server.url}/history?max_items=${maxItems}`, {
          signal: AbortSignal.timeout(10000),
        });
        if (data && typeof data === 'object') {
          for (const [id, entry] of Object.entries(data)) {
            results[`${server.id}--${id}`] = entry;
          }
        }
      } catch {
        /* skip offline server */
      }
    }),
  );
  return results;
}

export async function getAggregatedQueue() {
  const results = await queryAllServers(SERVERS);
  const running = [];
  const pending = [];
  for (const server of SERVERS) {
    const q = results.get(server.id);
    if (!q) continue;
    const prefix = `${server.id}--`;
    for (const item of q.queue_running || []) {
      if (Array.isArray(item) && item[1]) item[1] = prefix + item[1];
      running.push(item);
    }
    for (const item of q.queue_pending || []) {
      if (Array.isArray(item) && item[1]) item[1] = prefix + item[1];
      pending.push(item);
    }
  }
  return { queue_running: running, queue_pending: pending };
}

export async function proxyView(query) {
  const filename = query.filename;
  const subfolder = query.subfolder || '';
  const type = query.type || 'output';
  const accept =
    'image/*,audio/*,application/octet-stream,*/*';

  for (const server of SERVERS) {
    try {
      const url = new URL(`${server.url}/view`);
      url.searchParams.set('filename', filename);
      url.searchParams.set('subfolder', subfolder);
      url.searchParams.set('type', type);

      const upstream = await fetch(url.toString(), {
        signal: AbortSignal.timeout(30000),
        headers: { Accept: accept },
      });
      if (upstream.ok) {
        const guessed = contentTypeFromFilename(filename);
        const contentType =
          upstream.headers.get('content-type') || guessed || 'application/octet-stream';
        const buffer = Buffer.from(await upstream.arrayBuffer());
        return { ok: true, contentType, buffer };
      }
      console.error(`/view fail on ${server.id}: ${upstream.status}`);
    } catch (err) {
      console.error(`/view error on ${server.id}: ${err.message}`);
    }
  }
  return { ok: false };
}

export async function proxyFirstServer(path, options = {}) {
  for (const server of SERVERS) {
    try {
      const url = `${server.url}${path}`;
      const upstream = await fetch(url, {
        ...options,
        signal: options.signal || AbortSignal.timeout(30000),
      });
      const text = await upstream.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch {
        data = text;
      }
      if (upstream.ok || upstream.status < 500) {
        recordSuccess(server.id);
        return { status: upstream.status, data, headers: upstream.headers };
      }
    } catch {
      recordFailure(server.id);
    }
  }
  return { status: 502, data: { error: 'No servers available' } };
}

export async function proxyGetPath(reqPath, query = {}) {
  const qs = new URLSearchParams(query).toString();
  const suffix = qs ? `?${qs}` : '';
  for (const server of SERVERS) {
    try {
      const { status, data } = await fetchJson(`${server.url}${reqPath}${suffix}`, {
        signal: AbortSignal.timeout(5000),
      });
      if (data !== undefined && data !== null && data !== '') {
        recordSuccess(server.id);
        return { status, data };
      }
    } catch {
      recordFailure(server.id);
    }
  }
  return { status: 503, data: { error: 'All servers offline' } };
}
