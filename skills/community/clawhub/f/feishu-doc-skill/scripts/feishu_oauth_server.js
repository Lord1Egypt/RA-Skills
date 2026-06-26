#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const querystring = require('querystring');

const HOST = process.env.FEISHU_OAUTH_HOST || '127.0.0.1';
const PORT = Number(process.env.FEISHU_OAUTH_PORT || 3333);
const CALLBACK_PATH = process.env.FEISHU_OAUTH_CALLBACK_PATH || '/callback';
const REDIRECT_URI =
  process.env.FEISHU_REDIRECT_URI || `http://${HOST}:${PORT}${CALLBACK_PATH}`;
const TOKEN_OUTPUT =
  process.env.FEISHU_TOKEN_OUTPUT ||
  path.resolve(__dirname, '../.feishu-user-token.json');
const CONFIG_OUTPUT =
  process.env.FEISHU_OAUTH_CONFIG_OUTPUT ||
  path.resolve(__dirname, '../.feishu-oauth-config.json');

const defaultCredentials = {
  appId: process.env.FEISHU_APP_ID || '',
  appSecret: process.env.FEISHU_APP_SECRET || '',
};
const stateStore = new Map();

function loadSavedCredentials() {
  if (!fs.existsSync(CONFIG_OUTPUT)) {
    return { appId: '', appSecret: '' };
  }
  try {
    const data = JSON.parse(fs.readFileSync(CONFIG_OUTPUT, 'utf8'));
    return {
      appId: data.app_id || '',
      appSecret: data.app_secret || '',
    };
  } catch (error) {
    return { appId: '', appSecret: '' };
  }
}

function saveCredentials(appId, appSecret) {
  const payload = {
    saved_at: new Date().toISOString(),
    app_id: appId,
    app_secret: appSecret,
  };
  fs.writeFileSync(CONFIG_OUTPUT, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function deleteSavedCredentials() {
  if (fs.existsSync(CONFIG_OUTPUT)) {
    fs.unlinkSync(CONFIG_OUTPUT);
  }
}

async function readJson(response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`接口返回了非 JSON 内容: ${text.slice(0, 500)}`);
  }
}

async function getAppAccessToken(appId, appSecret) {
  const response = await fetch(
    'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        app_id: appId,
        app_secret: appSecret,
      }),
    },
  );

  const data = await readJson(response);
  if (!response.ok || data.code !== 0) {
    throw new Error(`获取 app_access_token 失败: ${JSON.stringify(data)}`);
  }

  return data.app_access_token;
}

async function getUserAccessToken(appId, appSecret, code) {
  const appAccessToken = await getAppAccessToken(appId, appSecret);
  const response = await fetch('https://open.feishu.cn/open-apis/authen/v1/access_token', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${appAccessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code,
    }),
  });

  const data = await readJson(response);
  if (!response.ok || data.code !== 0) {
    throw new Error(`获取 user_access_token 失败: ${JSON.stringify(data)}`);
  }

  return data.data;
}

function buildAuthorizeUrl(appId, state) {
  const url = new URL('https://open.feishu.cn/open-apis/authen/v1/index');
  url.searchParams.set('app_id', appId);
  url.searchParams.set('redirect_uri', REDIRECT_URI);
  url.searchParams.set('state', state);
  return url.toString();
}

function writeTokenFile(appId, tokenData) {
  const payload = {
    saved_at: new Date().toISOString(),
    redirect_uri: REDIRECT_URI,
    app_id: appId,
    ...tokenData,
  };
  fs.writeFileSync(TOKEN_OUTPUT, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function renderPage({ title, eyebrow = '飞书文档读写', bodyClass = '', content }) {
  return `<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(title)}</title>
    <style>
      :root {
        --bg: #f6efe6;
        --bg-accent: #fffaf4;
        --panel: rgba(255, 250, 244, 0.88);
        --panel-strong: #fffdf9;
        --text: #1f1b16;
        --muted: #6a5f52;
        --line: rgba(121, 95, 62, 0.18);
        --brand: #b85c38;
        --brand-deep: #8f4327;
        --brand-soft: rgba(184, 92, 56, 0.12);
        --success: #1f7a55;
        --success-soft: rgba(31, 122, 85, 0.12);
        --warning: #946200;
        --warning-soft: rgba(148, 98, 0, 0.14);
        --danger: #9a2f2f;
        --danger-soft: rgba(154, 47, 47, 0.12);
        --shadow: 0 24px 80px rgba(89, 58, 35, 0.12);
        --radius-xl: 28px;
        --radius-lg: 18px;
        --radius-md: 12px;
      }

      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        font-family: "Avenir Next", "PingFang SC", "Hiragino Sans GB", "Segoe UI", sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(184, 92, 56, 0.16), transparent 32%),
          radial-gradient(circle at top right, rgba(255, 212, 163, 0.38), transparent 28%),
          linear-gradient(180deg, var(--bg-accent), var(--bg));
      }

      .shell {
        width: min(1100px, calc(100vw - 32px));
        margin: 32px auto;
        padding: 24px;
      }

      .hero {
        display: grid;
        grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
        gap: 24px;
        align-items: stretch;
      }

      .card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
      }

      .intro {
        padding: 32px;
        position: relative;
        overflow: hidden;
      }

      .intro::after {
        content: "";
        position: absolute;
        right: -60px;
        bottom: -70px;
        width: 220px;
        height: 220px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(184, 92, 56, 0.18), transparent 65%);
        pointer-events: none;
      }

      .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(121, 95, 62, 0.14);
        color: var(--brand-deep);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
      }

      h1 {
        margin: 18px 0 12px;
        font-size: clamp(32px, 5vw, 54px);
        line-height: 1.02;
        letter-spacing: -0.04em;
      }

      .lead {
        margin: 0;
        max-width: 44ch;
        color: var(--muted);
        font-size: 16px;
        line-height: 1.7;
      }

      .meta-grid,
      .step-grid {
        display: grid;
        gap: 14px;
      }

      .meta-grid {
        margin-top: 26px;
      }

      .meta-item,
      .step {
        padding: 16px 18px;
        border-radius: var(--radius-lg);
        background: rgba(255, 255, 255, 0.66);
        border: 1px solid rgba(121, 95, 62, 0.1);
      }

      .meta-label,
      .step-index,
      .section-title,
      .field label {
        font-size: 13px;
        font-weight: 700;
        color: var(--muted);
      }

      .meta-value,
      .step-title {
        margin-top: 6px;
        font-size: 16px;
        font-weight: 700;
      }

      .meta-value code,
      .help code,
      .note code,
      .result code {
        font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
        font-size: 13px;
        background: rgba(48, 32, 20, 0.06);
        padding: 3px 7px;
        border-radius: 8px;
        word-break: break-all;
      }

      .step-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin-top: 26px;
      }

      .step-index {
        display: inline-flex;
        width: 28px;
        height: 28px;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        background: var(--brand-soft);
        color: var(--brand-deep);
      }

      .step p,
      .help,
      .result-copy,
      .status-text {
        margin: 10px 0 0;
        color: var(--muted);
        line-height: 1.65;
        font-size: 14px;
      }

      .form-card {
        padding: 28px;
        background: var(--panel-strong);
      }

      .section-title {
        margin-bottom: 8px;
      }

      .section-heading {
        margin: 0;
        font-size: 28px;
        letter-spacing: -0.03em;
      }

      .fields {
        display: grid;
        gap: 16px;
        margin-top: 24px;
      }

      .field {
        display: grid;
        gap: 8px;
      }

      .field input[type="text"],
      .field input[type="password"] {
        width: 100%;
        padding: 14px 16px;
        border-radius: 14px;
        border: 1px solid rgba(121, 95, 62, 0.18);
        background: #fff;
        color: var(--text);
        font-size: 15px;
        outline: none;
        transition: border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease;
      }

      .field input:focus {
        border-color: rgba(184, 92, 56, 0.6);
        box-shadow: 0 0 0 4px rgba(184, 92, 56, 0.12);
      }

      .field input::placeholder {
        color: #aa9b89;
      }

      .checkbox {
        display: flex;
        gap: 12px;
        align-items: flex-start;
        padding: 14px 16px;
        border-radius: 14px;
        background: rgba(184, 92, 56, 0.06);
        border: 1px solid rgba(184, 92, 56, 0.1);
      }

      .checkbox input {
        margin-top: 3px;
        accent-color: var(--brand);
      }

      .checkbox strong {
        display: block;
        margin-bottom: 4px;
        font-size: 14px;
      }

      .checkbox span {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.6;
      }

      .actions {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-top: 18px;
      }

      .button {
        appearance: none;
        border: 0;
        border-radius: 999px;
        padding: 14px 20px;
        background: linear-gradient(135deg, var(--brand), var(--brand-deep));
        color: #fff;
        font-size: 15px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 16px 36px rgba(143, 67, 39, 0.24);
      }

      .button:hover {
        transform: translateY(-1px);
      }

      .message,
      .status {
        margin-top: 18px;
        padding: 14px 16px;
        border-radius: 16px;
        border: 1px solid transparent;
      }

      .message.warning,
      .status.warning {
        background: var(--warning-soft);
        border-color: rgba(148, 98, 0, 0.14);
        color: var(--warning);
      }

      .status.success {
        background: var(--success-soft);
        border-color: rgba(31, 122, 85, 0.14);
        color: var(--success);
      }

      .status.error {
        background: var(--danger-soft);
        border-color: rgba(154, 47, 47, 0.16);
        color: var(--danger);
      }

      .status-title {
        margin: 0;
        font-size: 22px;
        letter-spacing: -0.03em;
      }

      .result {
        margin-top: 18px;
        display: grid;
        gap: 12px;
      }

      .result-item {
        padding: 15px 16px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.74);
        border: 1px solid rgba(121, 95, 62, 0.1);
      }

      .note {
        margin-top: 16px;
        font-size: 13px;
        color: var(--muted);
        line-height: 1.65;
      }

      .result-layout {
        width: min(760px, calc(100vw - 32px));
        margin: 40px auto;
        padding: 24px;
      }

      @media (max-width: 900px) {
        .hero,
        .step-grid {
          grid-template-columns: 1fr;
        }

        .shell,
        .result-layout {
          width: min(100vw - 20px, 100%);
          margin: 16px auto;
          padding: 12px;
        }

        .intro,
        .form-card {
          padding: 22px;
        }

        .actions {
          flex-direction: column;
          align-items: stretch;
        }

        .button {
          width: 100%;
        }
      }
    </style>
  </head>
  <body class="${escapeHtml(bodyClass)}">
    ${content}
  </body>
</html>`;
}

function renderHomePage(message = '') {
  const saved = loadSavedCredentials();
  const appId = defaultCredentials.appId || saved.appId;
  const appSecret = defaultCredentials.appSecret || saved.appSecret;
  const checked = appId && appSecret && appId === saved.appId && appSecret === saved.appSecret;

  return renderPage({
    title: '飞书授权配置',
    content: `
      <main class="shell">
        <section class="hero">
          <div class="card intro">
            <div class="eyebrow">${escapeHtml('Feishu OAuth Setup')}</div>
            <h1>为这个 skill 完成一次可复用的飞书授权</h1>
            <p class="lead">
              这个页面会引导你填写飞书应用凭证，跳转到飞书授权页，并把返回的
              <code>user_access_token</code> 安全保存到本地文件，供读取文档和插图脚本复用。
            </p>

            <div class="meta-grid">
              <div class="meta-item">
                <div class="meta-label">回调地址</div>
                <div class="meta-value"><code>${escapeHtml(REDIRECT_URI)}</code></div>
              </div>
              <div class="meta-item">
                <div class="meta-label">Token 保存位置</div>
                <div class="meta-value"><code>${escapeHtml(TOKEN_OUTPUT)}</code></div>
              </div>
            </div>

            <div class="step-grid">
              <div class="step">
                <div class="step-index">1</div>
                <div class="step-title">填写应用信息</div>
                <p>输入飞书开放平台里的 <code>App ID</code> 和 <code>App Secret</code>。</p>
              </div>
              <div class="step">
                <div class="step-index">2</div>
                <div class="step-title">跳转授权</div>
                <p>服务会生成带有 <code>state</code> 的授权链接，并跳转到飞书确认页面。</p>
              </div>
              <div class="step">
                <div class="step-index">3</div>
                <div class="step-title">保存本地 token</div>
                <p>授权成功后，脚本会把返回的用户 token 写入本地，后续读取可直接复用。</p>
              </div>
            </div>
          </div>

          <div class="card form-card">
            <div class="section-title">开始配置</div>
            <h2 class="section-heading">输入飞书应用凭证</h2>
            <p class="help">
              如果你已经在环境变量或本地配置里保存过值，这里会自动帮你预填。
            </p>
            ${
              message
                ? `<div class="message warning">${escapeHtml(message)}</div>`
                : ''
            }
            <form method="post" action="/start" class="fields">
              <div class="field">
                <label for="app_id">App ID</label>
                <input id="app_id" type="text" name="app_id" value="${escapeHtml(appId)}" placeholder="请输入飞书应用 App ID" />
              </div>
              <div class="field">
                <label for="app_secret">App Secret</label>
                <input id="app_secret" type="password" name="app_secret" value="${escapeHtml(appSecret)}" placeholder="请输入飞书应用 App Secret" />
              </div>
              <label class="checkbox">
                <input type="checkbox" name="remember_credentials" value="1" ${checked ? 'checked' : ''} />
                <div>
                  <strong>记住凭证到本地配置文件</strong>
                  <span>下次打开页面会自动预填；如果不勾选，这些值只保留在当前服务进程中。</span>
                </div>
              </label>
              <div class="actions">
                <button class="button" type="submit">继续前往飞书授权</button>
              </div>
            </form>
            <p class="note">
              使用前请先在飞书开放平台安全设置中加入回调地址
              <code>${escapeHtml(REDIRECT_URI)}</code>，
              否则飞书会在授权阶段直接拒绝回调。
            </p>
          </div>
        </section>
      </main>`,
  });
}

function renderStatusPage({ title, statusClass, heading, text, details = [], note = '' }) {
  const detailHtml = details
    .map(
      ({ label, value }) => `
        <div class="result-item">
          <div class="meta-label">${escapeHtml(label)}</div>
          <div class="meta-value"><code>${escapeHtml(value)}</code></div>
        </div>`,
    )
    .join('');

  return renderPage({
    title,
    bodyClass: 'result-page',
    content: `
      <main class="result-layout">
        <section class="card form-card">
          <div class="status ${escapeHtml(statusClass)}">
            <div class="section-title">${escapeHtml('授权结果')}</div>
            <h1 class="status-title">${escapeHtml(heading)}</h1>
            <p class="status-text">${escapeHtml(text)}</p>
          </div>
          ${detailHtml ? `<div class="result">${detailHtml}</div>` : ''}
          ${note ? `<p class="note">${escapeHtml(note)}</p>` : ''}
        </section>
      </main>`,
  });
}

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${HOST}:${PORT}`);

  if (req.method === 'GET' && url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(renderHomePage());
    return;
  }

  if (req.method === 'POST' && url.pathname === '/start') {
    try {
      const body = await readRequestBody(req);
      const form = querystring.parse(body);
      const appId = String(form.app_id || '').trim();
      const appSecret = String(form.app_secret || '').trim();
      const rememberCredentials = form.remember_credentials === '1';

      if (!appId || !appSecret) {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(renderHomePage('请先填写 App ID 和 App Secret'));
        return;
      }

      const state = crypto.randomBytes(16).toString('hex');
      stateStore.set(state, {
        appId,
        appSecret,
        createdAt: Date.now(),
      });

      if (rememberCredentials) {
        saveCredentials(appId, appSecret);
      } else if (!defaultCredentials.appId && !defaultCredentials.appSecret) {
        deleteSavedCredentials();
      }

      res.writeHead(302, {
        Location: buildAuthorizeUrl(appId, state),
      });
      res.end();
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '启动授权失败',
          statusClass: 'error',
          heading: '启动授权失败',
          text: '本地服务未能生成飞书授权跳转，请检查输入内容或稍后重试。',
          details: [{ label: '错误信息', value: error.message }],
          note: '如果问题持续出现，先确认本地端口可用，且回调地址与飞书开放平台配置一致。',
        }),
      );
    }
    return;
  }

  if (req.method === 'GET' && url.pathname === CALLBACK_PATH) {
    const code = url.searchParams.get('code');
    const returnedState = url.searchParams.get('state');
    const error = url.searchParams.get('error');

    if (error) {
      res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '飞书授权失败',
          statusClass: 'error',
          heading: '飞书侧返回了授权失败',
          text: '通常是用户取消授权，或应用配置、回调地址、权限范围存在问题。',
          details: [{ label: '错误参数', value: error }],
          note: '你可以返回首页重新发起授权；如果是配置问题，优先检查开放平台里的安全设置和应用权限。',
        }),
      );
      return;
    }

    if (!code) {
      res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '回调参数不完整',
          statusClass: 'error',
          heading: '回调缺少 code 参数',
          text: '飞书没有返回有效授权码，本次流程无法继续。',
          note: '请重新发起授权，并确认开放平台里配置的回调地址与当前页面显示的一致。',
        }),
      );
      return;
    }

    const stateData = returnedState ? stateStore.get(returnedState) : null;
    if (!stateData) {
      res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '状态校验失败',
          statusClass: 'error',
          heading: 'state 校验失败',
          text: '返回请求与本地发起的授权上下文不匹配，服务已拒绝继续处理。',
          note: '这通常意味着页面过期、服务重启过，或者回调请求不是由当前页面发起。',
        }),
      );
      return;
    }

    try {
      const tokenData = await getUserAccessToken(stateData.appId, stateData.appSecret, code);
      writeTokenFile(stateData.appId, tokenData);
      stateStore.delete(returnedState);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '授权成功',
          statusClass: 'success',
          heading: '授权成功，token 已写入本地',
          text: '后续运行读取文档或插图脚本时，会优先复用这个 user_access_token。',
          details: [
            { label: 'Token 文件', value: TOKEN_OUTPUT },
            { label: '回调地址', value: REDIRECT_URI },
            { label: '应用 ID', value: stateData.appId },
          ],
          note: '现在可以关闭这个页面，回到终端继续运行 read_feishu_url_md.js、read_feishu_url.js 或 insert_feishu_local_image.js。',
        }),
      );
      setTimeout(() => server.close(), 500);
    } catch (tokenError) {
      res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(
        renderStatusPage({
          title: '换取 Token 失败',
          statusClass: 'error',
          heading: '飞书返回了 token 换取失败',
          text: '授权回调已经到达本地服务，但用授权码换取 user_access_token 时失败了。',
          details: [{ label: '错误信息', value: tokenError.message }],
          note: '优先检查 App ID / App Secret 是否匹配当前应用，以及应用是否已开通对应权限。',
        }),
      );
    }
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('not found\n');
});

server.listen(PORT, HOST, () => {
  console.log(`飞书 OAuth 调试服务已启动: http://${HOST}:${PORT}`);
  console.log(`请先在飞书开放平台把回调地址加入安全设置: ${REDIRECT_URI}`);
  console.log(`然后打开: http://${HOST}:${PORT}`);
});
