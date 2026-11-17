#!/usr/bin/env node
/**
 * 超星智雅 MCP —— scope 探测实验台（v2）
 * ------------------------------------------------------------------
 * v1 的收获（重要）：
 *   不带 scope          -> ?error=access_denied      & error_description=OAuth 2.0 Parameter: client_id
 *   带 scope=all / scope=studyai -> ?error=invalid_scope  & error_description=OAuth 2.0 Parameter: scope
 * 说明：加上 scope 后校验确实往下走了一步 —— 真正的拦路石是 **scope 的取值**，
 *       平台要求它必须是该应用登记过的范围，而 client_id 那条报错只是在"没带 scope"
 *       时的误导性提示。
 *
 * 本实验台做的事：把一批 scope 取值做成链接，你逐个点一遍；
 * 另外提供一个自由输入框，若智雅凭证页写了「数据范围(Scope)」，直接填进去试。
 * 任一链接返回 code，脚本自动换 JWT → 写 mcp.json → tools/list。
 *
 * 凭据：从环境变量 CX_CLIENT_ID / CX_CLIENT_SECRET 读取（切勿写入本文件）。
 *       也可用 --client-id / --client-secret 临时传入。
 *
 * 用法：
 *   CX_CLIENT_ID=xxx CX_CLIENT_SECRET=yyy node chaoxing-mcp-lab.mjs
 *   node chaoxing-mcp-lab.mjs --client-id xxx --client-secret yyy
 */

import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const argv0 = process.argv.slice(2);
const argOf = (name) => {
  const i = argv0.indexOf('--' + name);
  return i >= 0 && argv0[i + 1] && !argv0[i + 1].startsWith('--') ? argv0[i + 1] : null;
};

const CFG = {
  clientId: process.env.CX_CLIENT_ID || argOf('client-id'),
  clientSecret: process.env.CX_CLIENT_SECRET || argOf('client-secret'),
  authorizeUrl: 'https://api.chaoxing.com/auth/oauth2/authorize',
  tokenUrl: 'https://api.chaoxing.com/auth/oauth2/token',
  mcpUrl: 'https://api.chaoxing.com/openai/studyai/data',
  serverName: 'chaoxing-studyai',
  serverDesc: '超星智雅 StudyAI（OAuth2 授权码 + 静态 Bearer）',
};

if (!CFG.clientId) {
  console.error(
    '❌ 缺少 client_id。请用环境变量 CX_CLIENT_ID 传入，或加 --client-id <id>。\n' +
      '   （凭据来源：智雅平台 个人工作台 → 权限管理 → 第三方授权管理 → 密钥管理）'
  );
  process.exit(1);
}
// client_secret 允许缺失：可在实验台页面粘贴录入（仅存进程内存，不写入任何文件）

const MCP_CONFIG = path.join(os.homedir(), '.workbuddy', 'mcp.json');
const PORT = Number(process.env.CX_PORT || 8765);
const REDIRECT_URI = `http://localhost:${PORT}/callback`;

/** 已确认无效的取值，不再重复试 */
const KNOWN_BAD = new Set(['all', 'studyai']);

/** 官方文档确认：scope = 建密钥时「选择接口」对应的数据范围技术标识（多为三段式，如 <域>:<资源>:<动作>）
 *  完整值以智雅凭证页「数据范围（Scope）」一栏为准 —— 优先用页面里的自由输入框填原文 */
const SCOPE_CANDIDATES = [
  'statistic:studyai:read topic:resource:read:test',
  'statistic:studyai:read',
  'openid',
];

const attempts = [];
let finished = false;
let finalReport = '';

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function authUrl(scope) {
  const u = new URL(CFG.authorizeUrl);
  u.searchParams.set('client_id', CFG.clientId);
  u.searchParams.set('response_type', 'code');
  u.searchParams.set('redirect_uri', REDIRECT_URI);
  if (scope !== null) u.searchParams.set('scope', scope);
  u.searchParams.set('state', scope === null ? 'cxlab-noscope' : 'cxlab-' + scope);
  return u.toString();
}

function page(title, body) {
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>${esc(title)}</title><style>
 body{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#14161a;color:#e8eaed;margin:0;padding:30px 38px;line-height:1.6}
 h1{font-size:21px;margin:0 0 6px} h2{font-size:15px;margin:24px 0 8px;color:#9aa4b2;font-weight:600}
 .sub{color:#8b94a3;font-size:13px;margin-bottom:16px}
 .grid{display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:0;list-style:none}
 .grid li{margin:0}
 .grid a{display:inline-block;padding:7px 13px;background:#1c1f26;border:1px solid #2a2f39;border-radius:7px;color:#7cc4ff;text-decoration:none;font-size:14px;font-family:Consolas,monospace}
 .grid a:hover{border-color:#3d4756;background:#22262e}
 .grid a.ok{border-color:#2ea043aa;background:#16281c;color:#7ee787}
 .grid a.bad{border-color:#d2992244;background:#251f14;color:#e3b341}
 .note{color:#8b94a3;font-size:12.5px}
 pre{background:#0f1115;border:1px solid #2a2f39;border-radius:6px;padding:10px 12px;overflow:auto;font-size:12.5px;color:#c8d0da}
 code{font-family:Consolas,monospace}
 input{background:#0f1115;border:1px solid #2a2f39;color:#e8eaed;padding:8px 10px;border-radius:6px;font-family:Consolas,monospace;font-size:14px;width:320px}
 button{background:#1f6feb;border:0;color:#fff;padding:8px 16px;border-radius:6px;font-size:14px;cursor:pointer}
 .warn{background:#251f14;border:1px solid #d2992255;border-radius:8px;padding:12px 14px;font-size:13px;color:#e3b341;margin:14px 0}
 .fail{color:#ff8a80}.good{color:#7ee787}
</style></head><body>${body}</body></html>`;
}

function labPage(badSecret = false) {
  if (!CFG.clientSecret) {
    return page(
      '超星智雅 MCP 授权 — 第一步',
      `<h1>第一步：粘贴 client_secret</h1>
       <div class="sub">client_id 已就绪：<code>${esc(CFG.clientId)}</code>。secret 只保存在本进程内存中，不写入任何文件、不进日志。</div>
       <div class="warn">粘贴后点保存 —— 会自动验证密钥，正确就直接跳到学习通授权页。</div>
       <form action="/secret" method="post">
         <input type="password" name="secret" placeholder="粘贴 client_secret" autocomplete="off" style="width:420px">
         <button type="submit">保存并自动验证</button>
       </form>`
    );
  }
  const cells = SCOPE_CANDIDATES.map((s) => {
    const hit = attempts.filter((a) => a.scope === s).pop();
    const cls = hit ? (hit.code ? 'ok' : 'bad') : '';
    const mark = hit ? (hit.code ? ' ✔' : ' ✘') : '';
    return `<li><a class="${cls}" href="/try?scope=${encodeURIComponent(s)}">${esc(s)}${mark}</a></li>`;
  }).join('');

  const history = attempts
    .map(
      (a) =>
        `#${String(a.n).padStart(2)} ${a.time}  scope=${a.scope === null ? '(不带)' : '[' + a.scope + ']'}  ->  ` +
        (a.code ? `code=${a.code.slice(0, 10)}…` : `${a.error || ''} / ${a.desc || ''}`)
    )
    .join('\n');

  return page(
    '超星智雅 scope 探测实验台',
    `${badSecret ? '<div class="warn">❌ 上一次粘贴的密钥验证未通过（invalid_client）。请回智雅重新复制 client_secret —— 建议直接「重置密钥」拿全新的，复制后确认无断行再贴。</div>' : ''}
     <h1>超星智雅 MCP 授权实验台</h1>
     <div class="sub">密钥已就绪（长度 ${CFG.clientSecret.length}，已通过/待验证）。下面按钮任选其一走授权；推荐点第一个。</div>

     <div class="warn">官方文档已确认（3.3 节）：<b>scope 就是你在智雅「新建密钥 → 选择接口」时所选接口的技术标识</b>，格式形如 <code>user:read</code>、<code>course:read</code>，<b>并且完整显示在智雅凭证页面的「数据范围（Scope）」一栏</b>。优先去凭证页抄那一栏的值填进下面的自由输入框，命中率最高。</div>

     <h2>第一步：粘贴 client_secret（已录入过则无需重复）</h2>
     <form action="/secret" method="post" style="display:flex;gap:8px;align-items:center">
       <input type="password" name="secret" placeholder="粘贴 client_secret" autocomplete="off" style="width:360px">
       <button type="submit">保存</button>
     </form>
     <form action="/verify-secret" method="get" style="margin-top:6px">
       <button type="submit" style="background:#2ea043">🔍 验证密钥（不消耗授权）</button>
     </form>

     <h2>常见取值（点一下就走一次授权，逐个点）</h2>
     <ul class="grid">${cells}</ul>

     <h2>不带 scope（对照）</h2>
     <ul class="grid"><li><a href="/try-noscope">不传 scope</a></li><li><a href="/try?scope=">scope= 空串</a></li></ul>

     <h2>自由输入 —— 若智雅文档写了 scope，直接填这里</h2>
     <form action="/try" method="get">
       <input name="scope" placeholder="例如 studyai.read 或文档里给的原值" autocomplete="off">
       <button type="submit">用这个 scope 授权</button>
     </form>

     <h2>本次记录 ${attempts.length} 次</h2>
     <pre>${esc(history || '(暂无)')}</pre>
     <p class="note"><a href="/lab">↻ 刷新本页</a>　|　只要出现 <span class="good">code=…</span> 就说明成功，脚本会自动写配置。</p>`
  );
}

function resultPage(a) {
  const head = a.code
    ? `<h1 class="good">✅ 成功，拿到授权码了</h1><div class="sub">正在自动换取令牌 / 写配置 / 跑连通性测试，结果见下方。</div>`
    : a.error === 'invalid_scope'
      ? `<h1 class="fail">✘ 这个 scope 不被认可</h1><div class="sub">换下一个取值继续试。</div>`
      : `<h1 class="fail">✘ 这一条仍然失败</h1><div class="sub">继续试别的。</div>`;
  return page(
    'scope 试跑结果',
    `${head}
     <h2>本次回调</h2><pre>scope  : ${esc(a.scope === null ? '(不带)' : a.scope)}
error  : ${esc(a.error || '(无)')}
desc   : ${esc(a.desc || '(无)')}
query  : ${esc(a.query || '(空)')}</pre>
     <h2>脚本后续输出</h2><pre>${esc(finalReport || '(等待中…)')}</pre>
     <p><a href="/lab">← 返回实验台继续</a></p>`
  );
}

function openBrowser(url) {
  try {
    if (process.platform === 'win32') {
      spawn('cmd', ['/c', 'start', '', url], { detached: true, stdio: 'ignore' }).unref();
    } else if (process.platform === 'darwin') {
      spawn('open', [url], { detached: true, stdio: 'ignore' }).unref();
    } else {
      spawn('xdg-open', [url], { detached: true, stdio: 'ignore' }).unref();
    }
  } catch {
    /* 忽略 */
  }
}

async function exchange(code) {
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CFG.clientId,
    client_secret: CFG.clientSecret,
    code: String(code),
    redirect_uri: REDIRECT_URI,
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

function writeMcpConfig(token) {
  let cfg = { mcpServers: {} };
  if (fs.existsSync(MCP_CONFIG)) {
    try {
      cfg = JSON.parse(fs.readFileSync(MCP_CONFIG, 'utf8'));
    } catch {
      fs.copyFileSync(MCP_CONFIG, MCP_CONFIG + '.bak');
      cfg = { mcpServers: {} };
    }
  }
  cfg.mcpServers = cfg.mcpServers || {};
  cfg.mcpServers[CFG.serverName] = {
    type: 'http',
    url: CFG.mcpUrl,
    headers: { Authorization: `Bearer ${token}` },
    description: CFG.serverDesc,
  };
  fs.mkdirSync(path.dirname(MCP_CONFIG), { recursive: true });
  fs.writeFileSync(MCP_CONFIG, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
  return MCP_CONFIG;
}

async function callMcp(token, method = 'tools/list', params = {}) {
  const res = await fetch(CFG.mcpUrl, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
    },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  });
  return { status: res.status, text: await res.text() };
}

async function handleSuccess(code) {
  const log = [];
  const say = (s) => {
    console.log(s);
    log.push(s);
  };
  say('\n已获得授权码，正在与令牌端点换取 access_token …');
  const { status, json } = await exchange(code);
  if (!json.access_token) {
    say(`❌ 换取令牌失败 (HTTP ${status})：${JSON.stringify(json)}`);
    return log.join('\n');
  }
  const token = json.access_token;
  say('✅ 令牌获取成功');
  say(`   token_type   : ${json.token_type || 'Bearer'}`);
  say(`   expires_in   : ${json.expires_in} 秒`);
  say(`   scope        : ${json.scope || '(未返回)'}`);
  say(`   refresh_token: ${json.refresh_token ? '有' : '无'}`);
  say(`   token 预览   : ${token.slice(0, 24)}…（${token.length} 字符）`);
  // 导出令牌对，供 chaoxing-mcp-refresh.mjs 使用
  const tokenPairPath = path.join(os.homedir(), '.workbuddy', 'chaoxing-studyai-token.json');
  fs.mkdirSync(path.dirname(tokenPairPath), { recursive: true });
  fs.writeFileSync(
    tokenPairPath,
    JSON.stringify(
      {
        access_token: token,
        refresh_token: json.refresh_token || null,
        scope: json.scope || null,
        expires_in: json.expires_in || null,
        obtained_at: new Date().toISOString(),
      },
      null,
      2
    ) + '\n',
    'utf8'
  );
  say(`   令牌对已导出 : ${tokenPairPath}`);
  say(`\n✅ 已写入配置：${writeMcpConfig(token)}`);
  say('\n=== 连通性测试：POST MCP 端点 ===');
  const r = await callMcp(token, 'tools/list');
  say(`HTTP ${r.status}`);
  say(r.text.slice(0, 4000));
  if (r.status === 403 && /scope_denied/i.test(r.text)) {
    say('\n⚠️ scope_denied：这个 JWT 的 scope 不含 MCP 端点要求的范围（例如只有 openid）。');
    say('   请换用智雅凭证页「数据范围(Scope)」一栏的完整值重新授权，成功后配置会自动覆盖更新。');
    return log.join('\n');
  }
  // 连通成功后自动拉起保活守护（凭据通过环境变量传递，不落盘）
  if (r.status === 200 && CFG.clientSecret) {
    try {
      const refreshScript = path.join(path.dirname(fileURLToPath(import.meta.url)), 'chaoxing-mcp-refresh.mjs');
      const child = spawn(
        process.execPath,
        [refreshScript],
        {
          env: { ...process.env, CX_CLIENT_ID: CFG.clientId, CX_CLIENT_SECRET: CFG.clientSecret },
          detached: true,
          stdio: 'ignore',
        }
      );
      child.unref();
      say('\n✅ 保活守护已在后台启动（每 55 分钟用 refresh_token 刷新，会话期间有效）。');
      say('   若新会话中 MCP 报 401/403，重跑一次刷新脚本 --once 即可恢复。');
    } catch (e) {
      say(`\n⚠️ 保活守护启动失败（${e.message}），可稍后手动运行 refresh 脚本。`);
    }
  }
  return log.join('\n');
}

/** 假 code 诊断：不消耗真授权，判定密钥对错。
 *  invalid_grant = 密钥正确（code 假是预期）；invalid_client = 密钥错误 */
async function fakeCodeTest() {
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CFG.clientId,
    client_secret: CFG.clientSecret,
    code: 'fake-code-diagnostic-do-not-use',
    redirect_uri: REDIRECT_URI,
  });
  const res = await fetch(CFG.tokenUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const text = await res.text();
  let err = '';
  try {
    err = JSON.parse(text).error || '';
  } catch {
    err = text.slice(0, 120);
  }
  if (err === 'invalid_grant') return { ok: true, msg: '✅ 密钥正确（invalid_grant：code 是假的属预期，说明 client_id + client_secret 这一对已被平台认可）。现在点上面的授权按钮即可一次通过。' };
  if (err === 'invalid_client') return { ok: false, msg: `❌ 密钥错误（invalid_client）。粘贴的 secret 与平台登记的不一致 —— 请在智雅「密钥管理」重新复制（或重置密钥后再复制），注意别漏字符。` };
  return { ok: false, msg: `⚠️ 未预期的响应：HTTP ${res.status} ${err}` };
}

/** 清洗粘贴内容：去除零宽字符/不可见字符，仅保留可打印 ASCII */
function sanitizeSecret(s) {
  // eslint-disable-next-line no-control-regex
  return String(s).replace(/[^\x21-\x7E]/g, '');
}

const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, `http://127.0.0.1:${PORT}`);

  if (u.pathname === '/favicon.ico') {
    res.writeHead(204);
    return res.end();
  }

  // 网页录入 secret：POST /secret（仅存进程内存）→ 自动验证 → 通过则自动跳授权
  if (u.pathname === '/secret' && req.method === 'POST') {
    let raw = '';
    req.on('data', (c) => {
      raw += c;
      if (raw.length > 10_000) req.destroy();
    });
    req.on('end', async () => {
      const val = sanitizeSecret(new URLSearchParams(raw).get('secret') || '');
      if (val) {
        CFG.clientSecret = val;
        console.log(`>>> client_secret 已更新（仅内存，长度 ${val.length}，已清洗不可见字符）`);
      }
      if (!CFG.clientSecret) {
        res.writeHead(302, { Location: '/lab' });
        return res.end();
      }
      // 自动验证密钥（假 code 诊断，不消耗授权）
      const v = await fakeCodeTest();
      console.log(`>>> 自动验证密钥：${v.ok ? '✅ 通过，自动进入授权' : '❌ 失败，留在录入页'}`);
      res.writeHead(302, { Location: v.ok ? '/try?scope=' + encodeURIComponent(SCOPE_CANDIDATES[0]) : '/lab?badsecret=1' });
      res.end();
    });
    return;
  }

  // 假 code 诊断：验证密钥对错（不消耗授权）
  if (u.pathname === '/verify-secret') {
    if (!CFG.clientSecret) {
      res.writeHead(302, { Location: '/lab' });
      return res.end();
    }
    const r = await fakeCodeTest();
    console.log(`>>> 密钥诊断：${r.ok ? '通过' : '失败'}`);
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(
      page(
        '密钥诊断结果',
        `<h1>${r.ok ? '密钥 OK' : '密钥有问题'}</h1><div class="sub" style="font-size:15px">${esc(r.msg)}</div>
         <p><a href="/lab">← 返回实验台</a></p>`
      )
    );
  }

  if (u.pathname === '/lab') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(labPage(u.searchParams.get('badsecret') === '1'));
  }

  if (u.pathname === '/') {
    res.writeHead(302, { Location: '/lab' });
    return res.end();
  }

  if (u.pathname === '/try' || u.pathname === '/try-noscope') {
    const noCope = u.pathname === '/try-noscope';
    const raw = u.searchParams.get('scope');
    // 修剪首尾空白：从凭证页复制常带空格/换行，会导致 invalid_scope
    const scope = noCope ? null : raw === '' ? '' : raw?.trim();
    const target = authUrl(scope === undefined ? '' : scope);
    console.log(`\n>>> 试 scope = ${scope === null ? '(不带)' : '[' + scope + ']'}`);
    res.writeHead(302, { Location: target });
    return res.end();
  }

  if (u.pathname === '/callback') {
    const code = u.searchParams.get('code');
    const st = u.searchParams.get('state') || '';
    let scope = null;
    if (st === 'cxlab-noscope') scope = null;
    else if (st.startsWith('cxlab-')) scope = st.slice(6);
    else if (st) scope = st;
    const a = {
      n: attempts.length + 1,
      time: new Date().toISOString().replace('T', ' ').slice(11, 19),
      query: u.search,
      code,
      scope,
      error: u.searchParams.get('error'),
      desc: u.searchParams.get('error_description'),
    };
    attempts.push(a);
    console.log(
      `--- 回调 #${a.n} [${a.time}] scope=${scope === null ? '(不带)' : '[' + scope + ']'} -> ${
        code ? 'CODE 拿到' : `${a.error} / ${a.desc}`
      }`
    );
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(resultPage(a));
    if (code && !finished) {
      finished = true;
      finalReport = await handleSuccess(code);
    }
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404');
});

server.listen(PORT, '127.0.0.1', () => {
  const lab = `http://localhost:${PORT}/lab`;
  console.log(`\n=== scope 探测实验台已启动 ===\n请在浏览器打开：${lab}\n`);
  console.log(`回调地址：${REDIRECT_URI}（本机监听 127.0.0.1:${PORT}）`);
  console.log(`候选 scope 共 ${SCOPE_CANDIDATES.length} 个；已排除已知无效：${[...KNOWN_BAD].join(', ')}`);
  console.log(`client_secret：${CFG.clientSecret ? '已通过环境变量/参数提供' : '未提供 —— 打开页面按提示粘贴（仅存内存）'}\n`);
  openBrowser(lab);
});
