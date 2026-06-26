/** 从环境变量读取 TS_TOKEN 与 AIZNT_PROXY_URLS */
function loadClient() {
  const token = (process.env.TS_TOKEN || '').trim();
  if (!token) {
    throw new Error('缺少 TS_TOKEN（天树对话凭证 ts_xxx，对应 skills.entries 的 apiKey）');
  }
  const raw = process.env.AIZNT_PROXY_URLS;
  if (!raw || !String(raw).trim()) {
    throw new Error('缺少 AIZNT_PROXY_URLS（JSON 字符串，与 GET /miniapp/ai/chat/credentials 返回的 aiznt_proxy_urls 一致）');
  }
  let urls;
  try {
    urls = typeof raw === 'string' ? JSON.parse(raw) : raw;
  } catch {
    throw new Error('AIZNT_PROXY_URLS 不是合法 JSON');
  }
  if (!urls || typeof urls !== 'object') {
    throw new Error('AIZNT_PROXY_URLS 必须是对象');
  }
  return { token, urls };
}

function expandUrl(template, replacements = {}) {
  if (!template || typeof template !== 'string') {
    throw new Error('URL 模板无效');
  }
  let u = template;
  for (const [k, v] of Object.entries(replacements)) {
    u = u.split(`{${k}}`).join(String(v));
  }
  if (u.includes('{')) {
    throw new Error(`URL 仍有未替换占位符: ${u}`);
  }
  return u;
}

function authHeaders(token, extra = {}) {
  return {
    Authorization: `Bearer ${token}`,
    ...extra,
  };
}

async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(`非 JSON 响应 (${res.status}): ${text.slice(0, 200)}`);
  }
  if (!res.ok) {
    const msg = data?.message || data?.error?.message || text.slice(0, 200);
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  if (data.code !== undefined && data.code !== 0) {
    throw new Error(data.message || `业务错误 code=${data.code}`);
  }
  return data.data !== undefined ? data.data : data;
}

module.exports = {
  loadClient,
  expandUrl,
  authHeaders,
  fetchJson,
};
