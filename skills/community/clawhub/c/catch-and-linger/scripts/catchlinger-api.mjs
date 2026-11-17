#!/usr/bin/env node
/**
 * catchlinger-api.mjs — CatchLinger REST API 客户端。
 *
 * 用法：
 *   node catchlinger-api.mjs save '<json>'            保存一条收藏（upsert）
 *   node catchlinger-api.mjs save-many '<json[]>'      批量保存（≤50）
 *   node catchlinger-api.mjs search --q 关键词 [--tag a] [--tag b] [--limit 20]
 *   node catchlinger-api.mjs stats                     统计概览
 *   node catchlinger-api.mjs tags                      标签列表
 *   node catchlinger-api.mjs notes --id <id> --body '<md>'
 *   node catchlinger-api.mjs account
 *
 * 配置：环境变量 CATCHLINGER_API_BASE 与 CATCHLINGER_API_KEY，
 *      或放在 ~/.config/catchlinger/env（KEY=VALUE 格式）。
 */

import { loadCatchLingerEnv } from './catchlinger-env.mjs';

const { base: BASE, key: KEY } = loadCatchLingerEnv() ?? { base: '', key: '' };

if (!BASE || !KEY) {
  console.error(
    JSON.stringify(
      {
        error:
          '缺少配置：请设置 CATCHLINGER_API_BASE 与 CATCHLINGER_API_KEY。请登录 https://catchlinger.sxyicheng.tech，在「我的语言 → 连接 Agent」手动生成新的 API Key，再更新 ~/.config/catchlinger/env。',
      },
      null,
      2,
    ),
  );
  process.exit(1);
}

function parseArgs(argv) {
  const positional = [];
  const flags = {};

  for (let i = 0; i < argv.length; i += 1) {
    const v = argv[i];
    if (v.startsWith('--')) {
      const key = v.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        flags[key] = true;
      } else {
        flags[key] = next;
        i += 1;
      }
    } else {
      positional.push(v);
    }
  }

  return { positional, flags };
}

async function request(pathname, { method = 'GET', body } = {}) {
  const res = await fetch(`${BASE}${pathname}`, {
    method,
    headers: {
      authorization: `Bearer ${KEY}`,
      accept: 'application/json',
      ...(body ? { 'content-type': 'application/json' } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

  const text = await res.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    // 非 JSON（例如 404 时 Next.js 返回的 HTML 页面）—— 别把整页塞进错误消息
    payload = null;
  }

  if (!res.ok) {
    const error =
      payload?.error ?? {
        code: `HTTP_${res.status}`,
        message: `请求 ${BASE}${pathname} 失败：HTTP ${res.status} ${res.statusText}`,
      };
    if (res.status === 401 || error.code === 'UNAUTHORIZED') {
      error.code = 'UNAUTHORIZED';
      error.message =
        'API Key 无效或已吊销。请登录 https://catchlinger.sxyicheng.tech，在「我的语言 → 连接 Agent」手动生成新的 API Key，再更新 ~/.config/catchlinger/env。';
    }
    console.error(JSON.stringify({ error }, null, 2));
    process.exit(1);
  }

  return payload?.data ?? payload;
}

const { positional, flags } = parseArgs(process.argv.slice(2));
const command = positional[0];

function requireArg(value, name) {
  if (!value) {
    console.error(JSON.stringify({ error: `缺少参数 --${name}` }, null, 2));
    process.exit(1);
  }
  return value;
}

switch (command) {
  case 'save': {
    const raw = positional[1];
    if (!raw) {
      console.error(JSON.stringify({ error: '用法：save <json>' }, null, 2));
      process.exit(1);
    }
    const payload = JSON.parse(raw);
    const data = await request('/items', { method: 'POST', body: payload });
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  case 'save-many': {
    const raw = positional[1];
    if (!raw) {
      console.error(JSON.stringify({ error: '用法：save-many <json[]>' }, null, 2));
      process.exit(1);
    }
    const items = JSON.parse(raw);
    const data = await request('/items', { method: 'POST', body: { items } });
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  case 'search': {
    const params = new URLSearchParams();
    if (flags.q) params.set('q', String(flags.q));
    if (flags.domain) params.set('domain', String(flags.domain));
    if (flags.type) params.set('content_type', String(flags.type));
    if (flags.source) params.set('source', String(flags.source));
    if (flags.status) params.set('status', String(flags.status));
    if (flags.read) params.set('read', String(flags.read));
    if (flags.limit) params.set('limit', String(flags.limit));
    if (flags.offset) params.set('offset', String(flags.offset));
    for (const tag of [].concat(flags.tag ?? [])) {
      params.append('tag', String(tag));
    }
    const data = await request(`/items?${params.toString()}`);
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  case 'stats': {
    const data = await request('/stats');
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  case 'tags': {
    const data = await request('/tags');
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  case 'notes': {
    const id = requireArg(flags.id, 'id');
    if (flags.body) {
      const data = await request(`/items/${id}/notes`, {
        method: 'POST',
        body: { body_md: String(flags.body) },
      });
      console.log(JSON.stringify(data, null, 2));
    } else {
      const data = await request(`/items/${id}/notes`);
      console.log(JSON.stringify(data, null, 2));
    }
    break;
  }

  case 'account': {
    const data = await request('/account');
    console.log(JSON.stringify(data, null, 2));
    break;
  }

  default: {
    console.error(
      JSON.stringify(
        {
          error:
            '未知命令。可用：save / save-many / search / stats / tags / notes / account',
          commands: ['save', 'save-many', 'search', 'stats', 'tags', 'notes', 'account'],
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }
}
