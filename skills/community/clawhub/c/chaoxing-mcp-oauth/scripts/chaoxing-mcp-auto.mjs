#!/usr/bin/env node
/**
 * 超星智雅 MCP —— 一键式自动接入（v1.1）
 * ------------------------------------------------------------------
 * 一条命令确保连接，自动完成：
 *   1. 读取凭据（环境变量 > 本地凭据文件）
 *   2. 检查本地令牌：未过期 → 直接验证 tools/list
 *   3. 已过期 → 用 refresh_token 自动刷新 → 验证
 *   4. 刷新失败/无令牌 → 自动弹出浏览器授权页 → 授权成功自动写配置
 *   5. 全部通过后自动关闭授权服务（防止重复授权作废令牌）
 *
 * 用法：
 *   node chaoxing-mcp-auto.mjs --setup           # 设置工作台（首次推荐：浏览器里逐项填凭据，自动保存+授权+验证一条龙）
 *   node chaoxing-mcp-auto.mjs --save <client_id> <client_secret> [scope]  # 命令行存凭据（不想弹页面时用）
 *   node chaoxing-mcp-auto.mjs                    # 一键确保连接（日常只用这条）
 *   node chaoxing-mcp-auto.mjs --status           # 只看状态，不做任何修改
 *   node chaoxing-mcp-auto.mjs --reauth           # 跳过刷新，强制重新授权
 *   node chaoxing-mcp-auto.mjs --daemon           # 常驻保活（临期自动刷新，进程不退出）
 *   node chaoxing-mcp-auto.mjs --daemon-once      # 无人值守单次保活（Windows 计划任务用：只刷新不弹授权页，静默退出）
 *
 * 凭据优先级：环境变量 CX_CLIENT_ID / CX_CLIENT_SECRET > chaoxing-credentials.json
 * 安全说明：--save 会把凭据明文存到 ~/.workbuddy/chaoxing-credentials.json（仅本机使用），
 *          泄露时去智雅「密钥管理 → 重置密钥」作废，再 --save 新密钥即可。
 */

import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const HOME = os.homedir();
const WB_DIR = path.join(HOME, '.workbuddy');
const CRED_FILE = path.join(WB_DIR, 'chaoxing-credentials.json');
const TOKEN_FILE = path.join(WB_DIR, 'chaoxing-studyai-token.json');
const MCP_CONFIG = path.join(WB_DIR, 'mcp.json');

const AUTHORIZE_URL = 'https://api.chaoxing.com/auth/oauth2/authorize';
const TOKEN_URL = 'https://api.chaoxing.com/auth/oauth2/token';
const MCP_URL = 'https://api.chaoxing.com/openai/studyai/data';
const SERVER_NAME = 'chaoxing-studyai';
const PORT = Number(process.env.CX_PORT || 8765);
const REDIRECT_URI = `http://localhost:${PORT}/callback`;

const ts = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const log = (...a) => console.log(`[${ts()}]`, ...a);

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const argOf = (name) => {
  const i = argv.indexOf('--' + name);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : null;
};
const CMD = argv[0] || ''; // '' | --save | --status | --reauth | --daemon

// ---------- 凭据 ----------
function loadCreds() {
  return {
    clientId: process.env.CX_CLIENT_ID || argOf('client-id'),
    clientSecret: process.env.CX_CLIENT_SECRET || argOf('client-secret'),
    scope: null,
  };
}
function loadCredFile() {
  try {
    return JSON.parse(fs.readFileSync(CRED_FILE, 'utf8'));
  } catch {
    return null;
  }
}
function saveCredFile(cred) {
  fs.mkdirSync(WB_DIR, { recursive: true });
  fs.writeFileSync(CRED_FILE, JSON.stringify(cred, null, 2) + '\n', 'utf8');
}
async function getCreds() {
  let cred = loadCreds();
  if (cred.clientId && cred.clientSecret) return cred;
  const saved = loadCredFile();
  if (saved?.clientId && saved?.clientSecret) return saved;
  return null;
}

// ---------- JWT / 令牌 ----------
function decodeJwtPayload(jwt) {
  try {
    const p = String(jwt).split('.')[1];
    return JSON.parse(Buffer.from(p, 'base64url').toString('utf8'));
  } catch {
    return {};
  }
}
function tokenState() {
  try {
    const t = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    const payload = decodeJwtPayload(t.access_token || '');
    const expMs = payload.exp
      ? payload.exp * 1000
      : t.expires_at
        ? Date.parse(t.expires_at)
        : 0;
    return { ...t, payload, expMs, expired: !expMs || expMs <= Date.now() };
  } catch {
    return null;
  }
}
function writeTokenFile(pair) {
  fs.mkdirSync(WB_DIR, { recursive: true });
  fs.writeFileSync(
    TOKEN_FILE,
    JSON.stringify({ ...pair, obtained_at: new Date().toISOString() }, null, 2) + '\n',
    'utf8'
  );
}
function writeMcpConfig(accessToken) {
  let cfg = { mcpServers: {} };
  try {
    cfg = JSON.parse(fs.readFileSync(MCP_CONFIG, 'utf8'));
  } catch {
    if (fs.existsSync(MCP_CONFIG)) fs.copyFileSync(MCP_CONFIG, MCP_CONFIG + '.bak');
    cfg = { mcpServers: {} };
  }
  cfg.mcpServers = cfg.mcpServers || {};
  const prev = cfg.mcpServers[SERVER_NAME] || {};
  cfg.mcpServers[SERVER_NAME] = {
    ...prev,
    type: 'http',
    url: MCP_URL,
    headers: { ...(prev.headers || {}), Authorization: `Bearer ${accessToken}` },
    description: prev.description || '超星智雅 StudyAI（OAuth2 授权码 + 静态 Bearer）',
  };
  fs.mkdirSync(path.dirname(MCP_CONFIG), { recursive: true });
  fs.writeFileSync(MCP_CONFIG, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
  return MCP_CONFIG;
}

// ---------- API ----------
async function postForm(bodyObj) {
  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(bodyObj),
  });
  const text = await res.text();
  try {
    return { status: res.status, json: JSON.parse(text) };
  } catch {
    return { status: res.status, json: { raw: text } };
  }
}
async function exchangeCode(cred, code) {
  return postForm({
    grant_type: 'authorization_code',
    client_id: cred.clientId,
    client_secret: cred.clientSecret,
    code: String(code),
    redirect_uri: REDIRECT_URI,
  });
}
async function refreshAccessToken(cred, refreshToken) {
  return postForm({
    grant_type: 'refresh_token',
    client_id: cred.clientId,
    client_secret: cred.clientSecret,
    refresh_token: refreshToken,
  });
}
async function verifyToken(accessToken) {
  const res = await fetch(MCP_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
    },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list', params: {} }),
  });
  return { status: res.status, text: (await res.text()).slice(0, 300) };
}

// 应用令牌：写令牌文件 + 写 mcp.json
function applyToken(json) {
  const pair = {
    access_token: json.access_token,
    refresh_token: json.refresh_token || null,
    scope: json.scope || null,
    expires_in: json.expires_in || null,
  };
  writeTokenFile(pair);
  writeMcpConfig(pair.access_token);
  const expMs = Date.now() + (Number(json.expires_in) || 3599) * 1000;
  log(`✅ 新令牌已生效，过期时间：${new Date(expMs).toISOString()}（本地时间约 ${(new Date(expMs)).toLocaleString()}）`);
  return pair;
}

// ---------- 子命令：--save ----------
async function cmdSave() {
  const id = argOf('client-id') || argv[1];
  const secret = argOf('client-secret') || argv[2];
  const scope = argv[3] && !argv[3].startsWith('--') ? argv[3] : null;
  if (!id || !secret) {
    console.error('用法：node chaoxing-mcp-auto.mjs --save <client_id> <client_secret> [scope]');
    process.exit(1);
  }
  saveCredFile({ clientId: id, clientSecret: secret, scope, saved_at: new Date().toISOString() });
  log(`✅ 凭据已保存到 ${CRED_FILE}${scope ? `（scope: ${scope}）` : '（scope 暂缺，授权时可自由输入）'}`);
}

// ---------- 子命令：--status ----------
async function cmdStatus(cred) {
  const st = tokenState();
  log('=== 当前状态 ===');
  log(`凭据文件 : ${fs.existsSync(CRED_FILE) ? CRED_FILE : '（无，用 --save 保存）'}`);
  log(`凭据来源 : ${process.env.CX_CLIENT_ID ? '环境变量' : cred ? '本地凭据文件' : '无'}`);
  if (!st) {
    log('本地令牌 : 无（需要授权）');
    return;
  }
  log(`scope    : ${st.scope || st.payload.scope || '(未知)'}`);
  log(`过期时间 : ${st.expMs ? new Date(st.expMs).toISOString() : '(未知)'} ${st.expired ? '【已过期】' : '【有效】'}`);
  log(`最后刷新 : ${st.refreshed_at || st.obtained_at || '(未知)'}`);
  const v = await verifyToken(st.access_token);
  log(`在线验证 : HTTP ${v.status} ${v.status === 200 ? '✅ 可用' : '❌ 不可用'}`);
}

// ---------- 授权服务（自动弹出，成功即自动关闭） ----------
function openBrowser(url) {
  try {
    if (process.platform === 'win32') spawn('cmd', ['/c', 'start', '', url], { detached: true, stdio: 'ignore' }).unref();
    else if (process.platform === 'darwin') spawn('open', [url], { detached: true, stdio: 'ignore' }).unref();
    else spawn('xdg-open', [url], { detached: true, stdio: 'ignore' }).unref();
  } catch { /* 忽略 */ }
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
function page(body) {
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>超星智雅 MCP 授权</title><style>
body{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#14161a;color:#e8eaed;margin:0;padding:40px;line-height:1.7}
h1{font-size:20px}.sub{color:#9aa4b2;font-size:13px}
input{background:#0f1115;border:1px solid #2a2f39;color:#e8eaed;padding:8px 10px;border-radius:6px;font-family:Consolas,monospace;font-size:14px;width:340px}
button{background:#1f6feb;border:0;color:#fff;padding:8px 18px;border-radius:6px;font-size:14px;cursor:pointer}
a{color:#7cc4ff}.good{color:#7ee787}.fail{color:#ff8a80}
pre{background:#0f1115;border:1px solid #2a2f39;border-radius:6px;padding:10px;font-size:12.5px;color:#c8d0da;overflow:auto}
</style></head><body>${body}</body></html>`;
}

function authUrlFor(scope) {
  const u = new URL(AUTHORIZE_URL);
  u.searchParams.set('client_id', scope === undefined ? '' : '', ); // noop 占位避免误用
  return null;
}
function buildAuthUrl(cred, scope) {
  const u = new URL(AUTHORIZE_URL);
  u.searchParams.set('client_id', cred.clientId);
  u.searchParams.set('response_type', 'code');
  u.searchParams.set('redirect_uri', REDIRECT_URI);
  if (scope !== null && scope !== undefined) u.searchParams.set('scope', scope);
  u.searchParams.set('state', 'auto-' + (scope ?? ''));
  return u.toString();
}

function runAuthLab(cred, defaultScope) {
  return new Promise((resolve) => {
    let done = false;
    let authTarget = null; // 待跳转的授权 URL（/try 时生成）
    const finish = (ok) => {
      if (done) return;
      done = true;
      try { server.close(); } catch { /* */ }
      resolve(ok);
    };

    const server = http.createServer(async (req, res) => {
      const u = new URL(req.url, `http://127.0.0.1:${PORT}`);

      if (u.pathname === '/favicon.ico') { res.writeHead(204); return res.end(); }

      if (u.pathname === '/' || u.pathname === '/lab') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end(page(`
          <h1>超星智雅 MCP 授权</h1>
          <div class="sub">点击下方按钮 → 登录学习通 → 点「确认授权」→ 全自动完成配置。成功后本页服务会自动关闭。</div>
          <p><button onclick="location.href='/try?scope=${encodeURIComponent(defaultScope || '')}'">用已保存的 scope 授权${defaultScope ? `：${esc(defaultScope)}` : '（未保存 scope）'}</button></p>
          <p>或填入其他 scope（多个用<b>空格</b>分隔）：</p>
          <form action="/try" method="get"><input name="scope" placeholder="例如 statistic:studyai:read" autocomplete="off"> <button type="submit">授权</button></form>
          <p class="sub">提示：回调地址 ${REDIRECT_URI} 需已在智雅「继续配置」中登记。</p>`));
      }

      if (u.pathname === '/try') {
        const scope = u.searchParams.get('scope');
        const target = buildAuthUrl(cred, scope === '' || scope === null ? undefined : scope);
        res.writeHead(302, { Location: target });
        return res.end();
      }

      if (u.pathname === '/callback') {
        const code = u.searchParams.get('code');
        const err = u.searchParams.get('error');
        const desc = u.searchParams.get('error_description');
        if (!code) {
          log(`授权失败：${err} / ${desc}`);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">✘ 授权未通过：${esc(err || '')} ${esc(desc || '')}</h1><p><a href="/lab">← 返回重试（检查 scope 取值）</a></p>`));
        }
        log('收到授权码，正在换取令牌…');
        const { status, json } = await exchangeCode(cred, code);
        if (!json.access_token) {
          log(`❌ 换取令牌失败 (HTTP ${status})：${JSON.stringify(json)}`);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">✘ 换取令牌失败（HTTP ${status}）</h1><pre>${esc(JSON.stringify(json))}</pre><p class="sub">invalid_client 通常是 client_secret 不对，请重置密钥后 --save 保存新密钥。</p>`));
        }
        const pair = applyToken(json);
        const v = await verifyToken(pair.access_token);
        if (v.status !== 200) {
          log(`⚠️ 令牌已拿到但 tools/list 返回 HTTP ${v.status}：${v.text}`);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">令牌已写入，但 MCP 验证失败（HTTP ${v.status}）</h1><pre>${esc(v.text)}</pre>`));
        }
        // 记住成功的 scope，下次免输入
        const saved = loadCredFile() || {};
        saveCredFile({ ...saved, clientId: cred.clientId, clientSecret: cred.clientSecret, scope: pair.scope || saved.scope || null, saved_at: saved.saved_at || new Date().toISOString() });
        log(`✅ 授权完成，tools/list 验证通过，配置已写入 ${MCP_CONFIG}`);
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(page(`<h1 class="good">✅ 授权成功，MCP 已连接！</h1><div class="sub">本页面服务已自动关闭，可以直接关闭此标签页。<br>之后任何时候只需一条命令即可自动保持连接。</div>`));
        setTimeout(() => finish(true), 300);
        return;
      }

      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404');
    });

    server.on('error', (e) => {
      console.error(`❌ 授权服务启动失败（端口 ${PORT} 可能被占用）：${e.message}`);
      finish(false);
    });

    server.listen(PORT, '127.0.0.1', () => {
      const lab = `http://localhost:${PORT}/lab`;
      log(`授权页已启动：${lab}（浏览器将自动打开，10 分钟内未完成自动放弃）`);
      openBrowser(lab);
      setTimeout(() => {
        if (!done) {
          log('❌ 等待授权超时（10 分钟），放弃。可重新运行重试。');
          finish(false);
        }
      }, 10 * 60 * 1000).unref();
    });
  });
}

// ---------- 一键确保连接 ----------
async function ensureConnected() {
  const cred = await getCreds();
  if (!cred) {
    console.error('❌ 缺少凭据。首次使用请先执行：');
    console.error('   node chaoxing-mcp-auto.mjs --save <client_id> <client_secret> [scope]');
    console.error('   （凭据来源：智雅 → 个人工作台 → 权限管理 → 第三方授权管理 → 密钥管理）');
    process.exit(1);
  }

  // 1. 本地令牌未过期 → 直接验证
  const st = tokenState();
  if (st && !st.expired) {
    log(`本地令牌有效（过期：${new Date(st.expMs).toISOString()}），在线验证中…`);
    const v = await verifyToken(st.access_token);
    if (v.status === 200) { log('✅ MCP 已连接，一切正常。'); return true; }
    log(`在线验证失败（HTTP ${v.status}），尝试刷新…`);
  } else if (st) {
    log(`本地令牌已过期（${new Date(st.expMs).toISOString()}），自动刷新…`);
  } else {
    log('本地无令牌，需要走一次授权…');
  }

  // 2. 过期/失效 → refresh
  if (st?.refresh_token) {
    const r = await refreshAccessToken(cred, st.refresh_token);
    if (r.json.access_token) {
      const pair = applyToken(r.json);
      const v = await verifyToken(pair.access_token);
      if (v.status === 200) { log('✅ 刷新成功，MCP 已连接。'); return true; }
      log(`刷新后验证仍失败（HTTP ${v.status}），转授权流程…`);
    } else {
      log(`刷新失败（HTTP ${r.status}）：${JSON.stringify(r.json).slice(0, 200)}`);
    }
  }

  // 3. 自动授权
  log('启动自动授权（需要你在浏览器里登录学习通并点一次「确认授权」）…');
  const ok = await runAuthLab(cred, cred.scope || st?.scope || null);
  if (ok) { log('✅ MCP 已连接。'); return true; }
  process.exit(1);
}

// ---------- 常驻保活 ----------
async function daemon() {
  const cred = await getCreds();
  if (!cred) { console.error('❌ 缺少凭据，先 --save 保存。'); process.exit(1); }
  const REFRESH_AHEAD = 10 * 60 * 1000; // 剩余 <10 分钟时刷新
  let working = false;
  const tick = async () => {
    if (working) return;
    working = true;
    try {
      const st = tokenState();
      if (!st) { log('本地无令牌，跳过本轮（先运行一键连接完成授权）。'); return; }
      const remain = st.expMs - Date.now();
      if (remain > REFRESH_AHEAD) return; // 还很新鲜，不动
      log(`令牌剩余 ${Math.max(0, Math.round(remain / 1000))}s，自动刷新…`);
      const r = await refreshAccessToken(cred, st.refresh_token);
      if (r.json.access_token) {
        applyToken(r.json);
        const v = await verifyToken(r.json.access_token);
        log(`刷新完成，验证 HTTP ${v.status}${v.status === 200 ? ' ✅' : ' ❌ ' + v.text.slice(0, 120)}`);
      } else {
        log(`❌ 刷新失败（HTTP ${r.status}）：${JSON.stringify(r.json).slice(0, 200)}`);
        log('   提示：运行 node chaoxing-mcp-auto.mjs 可自动重新授权。');
      }
    } catch (e) {
      log(`保活异常：${e.message}`);
    } finally {
      working = false;
    }
  };
  await tick();
  setInterval(tick, 5 * 60 * 1000); // 不加 unref，进程常驻
  log('保活守护已启动：每 5 分钟检查一次，临期自动刷新。Ctrl+C 退出。');
}

// ---------- 无人值守单次保活（计划任务用：只刷新不弹授权，静默退出） ----------
async function daemonOnce() {
  const cred = await getCreds();
  if (!cred) { log('缺少凭据，跳过（先 --save 保存）'); process.exit(0); }
  const st = tokenState();
  // 剩余不足 15 分钟才需要刷新，否则直接确认即可
  const REFRESH_AHEAD = 15 * 60 * 1000;
  if (st?.refresh_token && st.expMs - Date.now() > REFRESH_AHEAD) {
    const v = await verifyToken(st.access_token);
    if (v.status === 200) { log(`令牌仍有效（至 ${new Date(st.expMs).toISOString()}），无需刷新`); return; }
    log(`本地令牌未过期但服务端已失效（HTTP ${v.status}），强制刷新…`);
  }
  if (!st?.refresh_token) { log('本地无 refresh_token，需人工授权（跑一键命令），本次跳过'); process.exit(0); }
  const r = await refreshAccessToken(cred, st.refresh_token);
  if (r.json.access_token) {
    applyToken(r.json);
    const v = await verifyToken(r.json.access_token);
    log(`刷新完成，验证 HTTP ${v.status}${v.status === 200 ? ' ✅' : ' ❌ ' + v.text.slice(0, 120)}`);
    if (v.status !== 200) process.exit(2);
  } else {
    log(`❌ 刷新失败（HTTP ${r.status}）：${JSON.stringify(r.json).slice(0, 200)}；需人工授权（跑一键命令）`);
    process.exit(2);
  }
}

// ---------- 设置工作台（--setup：浏览器逐项填凭据 → 保存 → 自动授权 → 自动验证，全程不进对话） ----------
function setupPageHtml(saved, st) {
  const stateRows = st
    ? `<tr><td>当前 scope</td><td>${esc(st.scope || st.payload.scope || '(未知)')}</td></tr>
       <tr><td>令牌状态</td><td>${st.expired ? '❌ 已过期' : '✅ 本地有效（至 ' + esc(new Date(st.expMs).toISOString()) + '）'}</td></tr>`
    : `<tr><td>令牌状态</td><td>❌ 尚未授权</td></tr>`;
  return page(`
    <h1>超星智雅 MCP · 设置工作台</h1>    <div class="sub">全程在本页完成：填凭据 → 授权 → 自动验证。密钥无需粘贴进对话。</div>

    <div style="background:#1c1f26;border:1px solid #2a2f39;border-radius:8px;padding:12px 16px;margin:12px 0">
      <b style="color:#7cc4ff">📋 操作流程（按顺序做，全程约 2 分钟）</b>
      <ol style="margin:10px 0 0;padding-left:20px;font-size:13px;line-height:1.9">
        <li><b>登记回调地址（只需一次，必须最先做）</b>：登录智雅 → 个人工作台 → 权限管理 → 第三方授权管理 → 找到你的授权记录 → 点「继续配置」→ 把下面的地址粘贴进「回调地址」一栏并保存：
          <div style="display:flex;align-items:center;gap:8px;margin:6px 0">
            <input id="cburl" readonly value="http://localhost:${PORT}/callback" style="width:300px" onclick="this.select()">
            <button type="button" onclick="copyCb(this)">复制回调地址</button>
          </div>
          <span style="display:inline-block;background:#251f14;border:1px solid #d2992255;border-radius:6px;padding:4px 10px;font-size:12px;color:#e3b341">⚠️ 必须先登记回调、再点授权；顺序反了授权页会报 400（Whitelabel Error Page）</span>
        </li>
        <li><b>抄下三项凭据</b>（同一平台的「密钥管理」页）：<br>
          　① Client ID（客户端 ID）<br>
          　② Client Secret（客户端密钥，<b>仅生成时完整显示一次</b>；丢失请点「重置密钥」重新生成）<br>
          　③ Scope（凭证页「数据范围(Scope)」一栏原文；多个用<b>空格</b>分隔，不要用逗号）
        </li>
        <li><b>在下方表单填写三项</b> → 点「保存并连接」（保存前会自动校验密钥有效性，抄错立即提示，不会带病进入授权）</li>
        <li><b>自动跳转学习通授权页</b> → 登录 → 点「确认授权」</li>
        <li><b>自动完成剩余全部</b>：换令牌 → 写入 mcp.json → 在线验证 ✓（结果直接显示在本页）</li>
      </ol>
    </div>
    <table style="border-collapse:collapse;font-size:12.5px;color:#9aa4b2;margin-bottom:14px">
      <tr><td style="padding-right:16px">凭据文件</td><td>${fs.existsSync(CRED_FILE) ? '✅ 已存在（下方填写将覆盖）' : '（尚未保存）'}</td></tr>
      ${stateRows}
    </table>
    <form id="f">
      <p>① Client ID（客户端 ID）<br><input id="clientId" value="${esc(saved?.clientId || '')}" placeholder="cx_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" autocomplete="off" style="width:420px"></p>
      <p>② Client Secret（客户端密钥）<br><input id="clientSecret" type="password" value="" placeholder="${saved?.clientSecret ? '已保存（留空则沿用旧值）' : '仅生成时完整显示一次，请粘贴完整'}" autocomplete="off" style="width:420px"></p>
      <p>③ Scope（数据范围，可留空由下一步自动记忆；多个用<b>空格</b>分隔，不要用逗号）<br><input id="scope" value="${esc(saved?.scope || '')}" placeholder="例如 statistic:studyai:read" autocomplete="off" style="width:420px"></p>
      <p><button type="submit">保存并连接</button> <span id="msg" class="sub"></span></p>
    </form>
    <div id="result"></div>
    <script>
      function copyCb(btn) {
        const inp = document.getElementById('cburl');
        inp.select();
        try { document.execCommand('copy'); } catch (e) { navigator.clipboard && navigator.clipboard.writeText(inp.value); }
        btn.textContent = '✓ 已复制';
        setTimeout(() => { btn.textContent = '复制回调地址'; }, 1500);
      }
      document.getElementById('f').addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = document.getElementById('msg');
        const box = document.getElementById('result');
        msg.textContent = '提交中…';
        try {
          const r = await fetch('/api/setup', { method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              clientId: document.getElementById('clientId').value.trim(),
              clientSecret: document.getElementById('clientSecret').value.trim(),
              scope: document.getElementById('scope').value.trim(),
            })});
          const j = await r.json();
          if (j.ok) {
            msg.textContent = '';
            box.innerHTML = '<div style="background:#16281c;border:1px solid #2ea04388;border-radius:8px;padding:14px;margin-top:10px">' +
              '<b class="good">✅ 已保存凭据，正在跳转学习通授权页…</b><br><span class="sub">在授权页点「确认授权」后本流程自动完成（换令牌 → 写配置 → 验证），完成后本页会显示结果。</span></div>';
            if (j.authUrl) setTimeout(() => { location.href = j.authUrl; }, 800);
          } else {
            msg.textContent = '';
            box.innerHTML = '<div style="background:#251f14;border:1px solid #d2992288;border-radius:8px;padding:12px;margin-top:10px" class="fail">❌ ' + esc(j.error || '未知错误') + '</div>';
          }
        } catch (err) { msg.textContent = ''; box.innerHTML = '<p class="fail">请求失败：' + esc(String(err)) + '</p>'; }
      });
    </script>`);
}

function runSetup() {
  return new Promise((resolve) => {
    let done = false;
    let pendingScope = null; // 保存凭据后待跳转的授权 scope
    let pendingCred = null;

    const finish = (ok) => {
      if (done) return;
      done = true;
      try { server.close(); } catch { /* */ }
      resolve(ok);
    };

    const server = http.createServer(async (req, res) => {
      const u = new URL(req.url, `http://127.0.0.1:${PORT}`);

      if (u.pathname === '/favicon.ico') { res.writeHead(204); return res.end(); }

      // 工作台主页
      if (u.pathname === '/' || u.pathname === '/setup' || u.pathname === '/lab') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end(setupPageHtml(loadCredFile(), tokenState()));
      }

      // 保存凭据并返回授权跳转
      if (u.pathname === '/api/setup' && req.method === 'POST') {
        let body = '';
        req.on('data', (c) => { body += c; });
        req.on('end', async () => {
          try {
            const { clientId, clientSecret, scope } = JSON.parse(body || '{}');
            const saved = loadCredFile() || {};
            const id = clientId || saved.clientId;
            const sec = clientSecret || saved.clientSecret;
            if (!id || !sec) {
              res.writeHead(200, { 'Content-Type': 'application/json' });
              return res.end(JSON.stringify({ ok: false, error: 'Client ID 和 Client Secret 不能为空' }));
            }
            // 假 code 快速校验密钥有效性：invalid_grant=密钥对，invalid_client=密钥错
            log('校验密钥有效性（假 code 探测）…');
            const probe = await postForm({
              grant_type: 'authorization_code', client_id: id, client_secret: sec,
              code: 'setup-probe-' + Date.now(), redirect_uri: REDIRECT_URI,
            });
            if (probe.json.error === 'invalid_client') {
              res.writeHead(200, { 'Content-Type': 'application/json' });
              return res.end(JSON.stringify({ ok: false, error: 'Client ID / Secret 校验失败（invalid_client）。请核对是否复制完整——注意相似字符 l/1/I、0/O/D、cK/ck；必要时去智雅重置密钥。' }));
            }
            // 密钥有效，保存
            saveCredFile({ clientId: id, clientSecret: sec, scope: scope || saved.scope || null, saved_at: new Date().toISOString() });
            log(`✅ 凭据已保存（${CRED_FILE}）`);
            pendingCred = { clientId: id, clientSecret: sec, scope: scope || saved.scope || null };
            pendingScope = pendingCred.scope || null;
            const authTarget = buildAuthUrl(pendingCred, pendingScope);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            return res.end(JSON.stringify({ ok: true, authUrl: authTarget }));
          } catch (e) {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            return res.end(JSON.stringify({ ok: false, error: e.message }));
          }
        });
        return;
      }

      // OAuth 回调：自动换令牌 → 写配置 → 验证 → 展示最终结果（可与 /api/setup 同端口共存）
      if (u.pathname === '/callback') {
        const code = u.searchParams.get('code');
        const err = u.searchParams.get('error');
        const desc = u.searchParams.get('error_description');
        const cred = pendingCred || (await getCreds());
        if (!cred) {
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page('<h1 class="fail">无凭据，请回到工作台重新填写。</h1><p><a href="/setup">← 返回工作台</a></p>'));
        }
        if (!code) {
          log(`授权失败：${err} / ${desc}`);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">✘ 授权未通过：${esc(err || '')} ${esc(desc || '')}</h1><p><a href="/setup">← 返回工作台重试</a></p>`));
        }
        log('收到授权码，换取令牌…');
        const { status, json } = await exchangeCode(cred, code);
        if (!json.access_token) {
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">✘ 换取令牌失败（HTTP ${status}）</h1><pre>${esc(JSON.stringify(json))}</pre><p><a href="/setup">← 返回工作台</a></p>`));
        }
        const pair = applyToken(json);
        const v = await verifyToken(pair.access_token);
        // 记住生效 scope
        const saved = loadCredFile() || {};
        saveCredFile({ ...saved, clientId: cred.clientId, clientSecret: cred.clientSecret, scope: pair.scope || saved.scope || null, saved_at: saved.saved_at || new Date().toISOString() });
        if (v.status !== 200) {
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          return res.end(page(`<h1 class="fail">令牌已写入但 MCP 验证失败（HTTP ${v.status}）</h1><pre>${esc(v.text)}</pre><p class="sub">若为 403：去智雅「第三方授权管理」检查授权状态是否「启用中」，或 scope 是否覆盖 StudyAI 接口。</p><p><a href="/setup">← 返回工作台</a></p>`));
        }
        log('✅ 设置工作台流程全部完成');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(page(`<h1 class="good">🎉 全部完成！</h1>
          <table style="border-collapse:collapse;font-size:13px;color:#c8d0da">
            <tr><td style="padding:4px 18px 4px 0">凭据</td><td>✅ 已保存（下次免填）</td></tr>
            <tr><td style="padding:4px 18px 4px 0">授权</td><td>✅ 令牌已获取并写入 mcp.json</td></tr>
            <tr><td style="padding:4px 18px 4px 0">验证</td><td>✅ tools/list HTTP 200</td></tr>
            <tr><td style="padding:4px 18px 4px 0">scope</td><td>${esc(pair.scope || '(未返回)')}</td></tr>
            <tr><td style="padding:4px 18px 4px 0">令牌到期</td><td>${esc(new Date(Date.now() + (Number(json.expires_in) || 3599) * 1000).toLocaleString())}（之后由计划任务自动续期）</td></tr>
          </table>
          <p class="sub">本页服务已自动关闭，可直接关闭标签页。最后一步：WorkBuddy「连接器管理 → 自定义连接器」对 chaoxing-studyai 点「信任」。</p>`));
        setTimeout(() => finish(true), 500);
        return;
      }

      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404');
    });

    server.on('error', (e) => {
      console.error(`❌ 设置工作台启动失败（端口 ${PORT} 可能被占用）：${e.message}`);
      finish(false);
    });

    server.listen(PORT, '127.0.0.1', () => {
      const url = `http://localhost:${PORT}/setup`;
      log(`设置工作台已启动：${url}（浏览器将自动打开；15 分钟内未完成自动关闭）`);
      openBrowser(url);
      setTimeout(() => {
        if (!done) { log('等待超时（15 分钟），工作台自动关闭。'); finish(false); }
      }, 15 * 60 * 1000).unref();
    });
  });
}

// ---------- 入口 ----------
(async () => {
  const cred = await getCreds();
  if (CMD === '--save') return cmdSave();
  if (CMD === '--setup') { const ok = await runSetup(); process.exit(ok ? 0 : 1); }
  if (CMD === '--daemon') return daemon();
  if (CMD === '--daemon-once') return daemonOnce();
  if (CMD === '--status') return cmdStatus(cred);
  if (CMD === '--reauth') {
    if (!cred) { console.error('❌ 缺少凭据，先 --save 保存。'); process.exit(1); }
    log('强制重新授权…');
    const ok = await runAuthLab(cred, cred?.scope || null);
    process.exit(ok ? 0 : 1);
  }
  await ensureConnected();
})().catch((e) => {
  console.error(`❌ 异常：${e.message}`);
  process.exit(1);
});
