#!/usr/bin/env node

const BASE_URL = 'https://open.feishu.cn/open-apis';

async function readJson(response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`接口返回了非 JSON 内容: ${text.slice(0, 500)}`);
  }
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await readJson(response);
  if (!response.ok) {
    throw new Error(`HTTP 请求失败: ${response.status} ${response.statusText}: ${JSON.stringify(data)}`);
  }
  return data;
}

async function parseFeishuResponse(response, action) {
  const data = await readJson(response);
  if (!response.ok) {
    throw new Error(`HTTP 请求失败: ${response.status} ${response.statusText}: ${JSON.stringify(data)}`);
  }
  if (data.code !== 0) {
    throw new Error(`${action}失败: ${JSON.stringify(data)}`);
  }
  return data;
}

async function requestFeishuJson(path, { action, method = 'GET', headers = {}, query, body, timeout = 30000 } = {}) {
  const url = new URL(`${BASE_URL}${path}`);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, String(value));
      }
    }
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(url, {
      method,
      headers: body
        ? {
            'Content-Type': 'application/json',
            ...headers,
          }
        : headers,
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });
    return await parseFeishuResponse(response, action || path);
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`${action || path}失败: 请求超时`);
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

module.exports = {
  BASE_URL,
  readJson,
  requestJson,
  parseFeishuResponse,
  requestFeishuJson,
};
