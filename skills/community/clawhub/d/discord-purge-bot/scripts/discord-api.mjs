import * as http from 'node:http';

import { normalizeToken, sanitizeObject, sleep } from './common.mjs';

const API_BASE = 'https://discord.com/api/v10';

function enableProxyFromEnvironment() {
  const hasProxyEnv = [
    'HTTP_PROXY',
    'http_proxy',
    'HTTPS_PROXY',
    'https_proxy',
    'NO_PROXY',
    'no_proxy',
  ].some((name) => Boolean(process.env[name]));

  if (!hasProxyEnv || typeof http.setGlobalProxyFromEnv !== 'function') {
    return;
  }

  try {
    http.setGlobalProxyFromEnv();
  } catch (error) {
    process.emitWarning(`Failed to configure proxy from environment: ${error.message}`);
  }
}

enableProxyFromEnvironment();

function buildUrl(pathname, query) {
  const url = new URL(pathname, API_BASE);
  const queryValues = sanitizeObject(query ?? {});
  for (const [key, value] of Object.entries(queryValues)) {
    url.searchParams.set(key, String(value));
  }
  return url;
}

async function parseResponseBody(response) {
  const contentType = response.headers.get('content-type') ?? '';
  if (response.status === 204) return null;
  if (contentType.includes('application/json')) return response.json();
  return response.text();
}

async function parseRetryAfter(response) {
  const retryHeader = response.headers.get('retry-after');
  if (retryHeader) {
    const retryHeaderNumber = Number.parseFloat(retryHeader);
    if (!Number.isNaN(retryHeaderNumber)) return retryHeaderNumber * 1000;
  }

  try {
    const data = await response.clone().json();
    const retryAfter = Number(data.retry_after);
    if (!Number.isNaN(retryAfter)) return retryAfter * 1000;
  } catch {
    return 1000;
  }

  return 1000;
}

export async function discordRequest({ token, method = 'GET', path, query, body, reason, retryLimit = 8 }) {
  const requestUrl = buildUrl(path, query);
  const headers = {
    Authorization: normalizeToken(token),
  };

  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }

  if (reason) {
    headers['X-Audit-Log-Reason'] = encodeURIComponent(reason);
  }

  let attempts = 0;
  while (true) {
    let response;
    try {
      response = await fetch(requestUrl, {
        method,
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
      });
    } catch (error) {
      attempts += 1;
      if (attempts > retryLimit) throw error;
      await sleep(750 * attempts);
      continue;
    }

    if (response.status === 429) {
      attempts += 1;
      if (attempts > retryLimit) {
        const bodyText = await response.text();
        throw new Error(`Discord API 429 after retries: ${bodyText}`);
      }
      const waitMs = await parseRetryAfter(response);
      await sleep(waitMs + 100);
      continue;
    }

    if (response.status >= 500 && response.status <= 504) {
      attempts += 1;
      if (attempts > retryLimit) {
        const bodyText = await response.text();
        throw new Error(`Discord API ${response.status} after retries: ${bodyText}`);
      }
      await sleep(500 * attempts);
      continue;
    }

    const remaining = Number.parseInt(response.headers.get('x-ratelimit-remaining') ?? '', 10);
    const resetAfter = Number.parseFloat(response.headers.get('x-ratelimit-reset-after') ?? '');

    if (!response.ok) {
      const failedBody = await parseResponseBody(response);
      const error = new Error(`Discord API ${response.status} ${method} ${requestUrl.pathname}`);
      error.status = response.status;
      error.body = failedBody;
      throw error;
    }

    const payload = await parseResponseBody(response);

    if (!Number.isNaN(remaining) && remaining === 0 && !Number.isNaN(resetAfter) && resetAfter > 0) {
      await sleep(resetAfter * 1000);
    }

    return payload;
  }
}

export async function fetchMessagesPage({ token, channelId, before, after, around, limit = 100 }) {
  return discordRequest({
    token,
    method: 'GET',
    path: `/channels/${channelId}/messages`,
    query: {
      before,
      after,
      around,
      limit,
    },
  });
}

export async function bulkDeleteMessages({ token, channelId, messageIds, reason }) {
  return discordRequest({
    token,
    method: 'POST',
    path: `/channels/${channelId}/messages/bulk-delete`,
    body: {
      messages: messageIds,
    },
    reason,
  });
}

export async function deleteMessage({ token, channelId, messageId, reason }) {
  return discordRequest({
    token,
    method: 'DELETE',
    path: `/channels/${channelId}/messages/${messageId}`,
    reason,
  });
}

export async function getChannel({ token, channelId }) {
  return discordRequest({
    token,
    method: 'GET',
    path: `/channels/${channelId}`,
  });
}

export async function createGuildChannel({ token, guildId, body, reason }) {
  return discordRequest({
    token,
    method: 'POST',
    path: `/guilds/${guildId}/channels`,
    body,
    reason,
  });
}

export async function deleteChannel({ token, channelId, reason }) {
  return discordRequest({
    token,
    method: 'DELETE',
    path: `/channels/${channelId}`,
    reason,
  });
}
