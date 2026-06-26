#!/usr/bin/env node

function safeHost(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return 'invalid-url';
  }
}

function inferAvatarUrl(item) {
  if (item.avatar_url) return item.avatar_url;
  const handle = item.person_handle || item.handle;
  if (handle) {
    return `https://unavatar.io/x/${handle.replace(/^@/, '')}`;
  }
  return null;
}

function resolveApiBase(domain) {
  if (domain === 'lark') {
    return 'https://open.larksuite.com/open-apis';
  }
  if (typeof domain === 'string' && domain.startsWith('http')) {
    return `${domain.replace(/\/+$/, '')}/open-apis`;
  }
  return 'https://open.feishu.cn/open-apis';
}

async function fetchJson(url, init) {
  const response = await fetch(url, init);
  let payload;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}: ${payload ? JSON.stringify(payload) : 'empty response'}`);
  }

  return payload;
}

async function getTenantToken(creds, log = () => {}) {
  const apiBase = resolveApiBase(creds.domain);
  log('info', 'Requesting Feishu tenant token', { accountId: creds.accountId });
  const payload = await fetchJson(`${apiBase}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      app_id: creds.appId,
      app_secret: creds.appSecret
    })
  });

  if (payload?.code !== 0 || !payload?.tenant_access_token) {
    throw new Error(`Failed to get Feishu tenant token: ${payload?.msg || 'unknown error'}`);
  }

  log('info', 'Feishu tenant token acquired', { accountId: creds.accountId });
  return payload.tenant_access_token;
}

async function fetchAvatarBuffer(item, log = () => {}) {
  const avatarUrl = inferAvatarUrl(item);
  if (!avatarUrl) {
    log('warning', 'Skipping avatar fetch because no avatar URL is available', {
      person: item.person_name || item.name || 'unknown'
    });
    return null;
  }

  log('info', 'Fetching avatar', {
    person: item.person_name || item.name || 'unknown',
    avatarHost: safeHost(avatarUrl)
  });

  const response = await fetch(avatarUrl, {
    headers: {
      'User-Agent': 'follow-builders-feishu-card/1.0'
    },
    redirect: 'follow'
  });

  if (!response.ok) {
    throw new Error(`Avatar fetch failed with status ${response.status}`);
  }

  return Buffer.from(await response.arrayBuffer());
}

async function uploadImage(token, creds, buffer, log = () => {}) {
  const apiBase = resolveApiBase(creds.domain);
  log('info', 'Uploading avatar image to Feishu', { accountId: creds.accountId });

  const form = new FormData();
  form.append('image_type', 'message');
  form.append('image', new Blob([buffer], { type: 'image/png' }), 'avatar.png');

  const response = await fetch(`${apiBase}/im/v1/images`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: form
  });

  const payload = await response.json();
  if (!response.ok || payload?.code !== 0 || !payload?.data?.image_key) {
    throw new Error(`Feishu image upload failed: ${payload?.msg || response.statusText}`);
  }

  log('info', 'Avatar uploaded to Feishu', { imageKey: payload.data.image_key });
  return payload.data.image_key;
}

async function sendCard(card, target, token, creds, receiveIdType, log = () => {}) {
  const apiBase = resolveApiBase(creds.domain);
  log('info', 'Sending Feishu card', {
    accountId: creds.accountId,
    receiveIdType
  });

  const payload = await fetchJson(`${apiBase}/im/v1/messages?receive_id_type=${encodeURIComponent(receiveIdType)}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      receive_id: target,
      msg_type: 'interactive',
      content: JSON.stringify(card)
    })
  });

  if (payload?.code !== 0 || !payload?.data?.message_id) {
    throw new Error(`Feishu card send failed: ${payload?.msg || 'unknown error'}`);
  }

  log('info', 'Feishu card sent', { messageId: payload.data.message_id });
  return payload.data.message_id;
}

export {
  fetchAvatarBuffer,
  getTenantToken,
  sendCard,
  uploadImage
};
