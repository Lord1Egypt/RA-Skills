#!/usr/bin/env node
/**
 * 超星智雅 MCP —— 令牌刷新器（常驻）
 * ------------------------------------------------------------------
 * 作用：access_token 只有 1 小时寿命。本脚本用 refresh_token 定期刷新，
 *      并把新令牌写回 ~/.workbuddy/mcp.json 的 chaoxing-studyai 条目。
 *
 * 凭据：从环境变量 CX_CLIENT_ID / CX_CLIENT_SECRET 读取（切勿写入本文件）。
 *       也可用 --client-id / --client-secret 临时传入。
 *
 * 用法：
 *   node chaoxing-mcp-refresh.mjs --token <JSON文件路径>   # 首次：导入换好的令牌对
 *   node chaoxing-mcp-refresh.mjs                          # 之后：常驻按周期刷新
 *   node chaoxing-mcp-refresh.mjs --once                   # 只刷新一次就退出
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const argv0 = process.argv.slice(2);
const argOf = (name) => {
  const i = argv0.indexOf('--' + name);
  return i >= 0 && argv0[i + 1] && !argv0[i + 1].startsWith('--') ? argv0[i + 1] : null;
};

const CFG = {
  clientId: process.env.CX_CLIENT_ID || argOf('client-id'),
  clientSecret: process.env.CX_CLIENT_SECRET || argOf('client-secret'),
  tokenUrl: 'https://api.chaoxing.com/auth/oauth2/token',
  mcpUrl: 'https://api.chaoxing.com/openai/studyai/data',
  serverName: 'chaoxing-studyai',
};

if (!CFG.clientId || !CFG.clientSecret) {
  console.error(
    '❌ 缺少凭据。请用环境变量 CX_CLIENT_ID / CX_CLIENT_SECRET 传入，' +
      '或加 --client-id <id> --client-secret <secret>。\n' +
      '   （凭据来源：智雅平台 个人工作台 → 权限管理 → 第三方授权管理 → 密钥管理）'
  );
  process.exit(1);
}

const MCP_CONFIG = path.join(os.homedir(), '.workbuddy', 'mcp.json');
const STATE_FILE = path.join(os.homedir(), '.workbuddy', 'chaoxing-studyai-token.json');

const argv = process.argv.slice(2);
const arg = (name, def = null) => {
  const i = argv.indexOf('--' + name);
  return i >= 0 ? (argv[i + 1] !== undefined && !argv[i + 1].startsWith('--') ? argv[i + 1] : true) : def;
};
const ONCE = !!arg('once', false);
const IMPORT = arg('token', null);

function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return null;
  }
}

function writeState(s) {
  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2) + '\n', 'utf8');
}

/** 把 access_token 写入 mcp.json；refresh_token 存本地状态文件（避免敏感信息进 mcp.json） */
function writeMcpConfig(accessToken) {
  let cfg = { mcpServers: {} };
  try {
    cfg = JSON.parse(fs.readFileSync(MCP_CONFIG, 'utf8'));
  } catch {
    /* 重建 */
  }
  cfg.mcpServers = cfg.mcpServers || {};
  const prev = cfg.mcpServers[CFG.serverName] || {};
  cfg.mcpServers[CFG.serverName] = {
    ...prev,
    type: 'http',
    url: CFG.mcpUrl,
    headers: { ...(prev.headers || {}), Authorization: `Bearer ${accessToken}` },
    description: prev.description || '超星智雅 StudyAI（OAuth2 授权码 + 静态 Bearer）',
  };
  fs.mkdirSync(path.dirname(MCP_CONFIG), { recursive: true });
  fs.writeFileSync(MCP_CONFIG, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
}

async function refreshToken(refreshToken) {
  const body = new URLSearchParams({
    grant_type: 'refresh_token',
    client_id: CFG.clientId,
    client_secret: CFG.clientSecret,
    refresh_token: refreshToken,
  });
  const res = await fetch(CFG.tokenUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const text = await res.text();
  try {
    return { status: res.status, json: JSON.parse(text) };
  } catch {
    return { status: res.status, json: { raw: text } };
  }
}

async function verifyToken(accessToken) {
  const res = await fetch(CFG.mcpUrl, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
    },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list', params: {} }),
  });
  const text = await res.text();
  return { status: res.status, text };
}

function decodeJwtPayload(jwt) {
  try {
    const p = jwt.split('.')[1];
    return JSON.parse(Buffer.from(p, 'base64url').toString('utf8'));
  } catch {
    return {};
  }
}

async function cycle(reason) {
  const state = readState();
  if (!state?.refresh_token) {
    console.error('❌ 本地状态文件缺少 refresh_token，请先用 --token 导入令牌对');
    process.exit(1);
  }
  console.log(`\n[${new Date().toISOString()}] 刷新令牌（原因：${reason}）…`);
  const { status, json } = await refreshToken(state.refresh_token);
  if (!json.access_token) {
    console.error(`❌ 刷新失败 (HTTP ${status})：`, JSON.stringify(json).slice(0, 400));
    console.error('   refresh_token 可能已被轮换或失效，需要重新走一次授权（chaoxing-mcp-lab.mjs）。');
    if (ONCE) process.exit(2);
    return; // 常驻模式下等下一轮再试
  }
  const payload = decodeJwtPayload(json.access_token);
  const newState = {
    ...state,
    access_token: json.access_token,
    // 部分实现刷新时不返回新的 refresh_token，沿用旧的
    refresh_token: json.refresh_token || state.refresh_token,
    scope: json.scope || payload.scope || state.scope,
    refreshed_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + (Number(json.expires_in) || 3599) * 1000).toISOString(),
  };
  writeState(newState);
  writeMcpConfig(newState.access_token);
  console.log(`✅ 新令牌已写入 ${MCP_CONFIG}`);
  console.log(`   scope      : ${JSON.stringify(newState.scope)}`);
  console.log(`   过期时间    : ${newState.expires_at}`);

  if (ONCE) {
    const v = await verifyToken(newState.access_token);
    console.log(`\n=== tools/list 验证：HTTP ${v.status} ===`);
    console.log(v.text.slice(0, 600));
  }
}

(async () => {
  // 首次导入：--token 指向实验台导出的令牌对 JSON（或直接内联 JSON 字符串）
  if (IMPORT) {
    let pair = null;
    try {
      pair = JSON.parse(fs.readFileSync(String(IMPORT), 'utf8'));
    } catch {
      try {
        pair = JSON.parse(String(IMPORT));
      } catch {
        console.error('❌ --token 参数需要是令牌对 JSON 文件路径或内联 JSON');
        process.exit(1);
      }
    }
    if (!pair.refresh_token) {
      console.error('❌ 导入内容缺少 refresh_token');
      process.exit(1);
    }
    const prev = readState();
    writeState({
      refresh_token: pair.refresh_token,
      access_token: pair.access_token || prev?.access_token || '',
      scope: pair.scope || prev?.scope || null,
    });
    console.log('✅ 令牌对已导入', STATE_FILE);
    if (pair.access_token) writeMcpConfig(pair.access_token);
  }

  await cycle(ONCE ? '一次性刷新' : '启动');

  if (ONCE) return;

  // 修复：unref() 的 setInterval 会让 Node 事件循环为空而自动退出。
  // 改为可 ref 的 interval（保持常驻）；兜底每 5 分钟检查状态文件是否缺失。
  const MIN5 = 5 * 60 * 1000;
  const HOUR = 55 * 60 * 1000; // 55 分钟刷一次（令牌寿命 60 分钟）
  setInterval(() => cycle('定时'), HOUR);
  setInterval(() => cycle('兜底'), MIN5);
  console.log('\n常驻模式：每 55 分钟刷新一次（兜底每 5 分钟检查状态文件是否缺失）。按 Ctrl+C 退出。');
})();
