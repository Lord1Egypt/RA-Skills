/**
 * 用抖音授权码 code 换取 open_id 和 access_token，并可选择写入 .env
 * 用法：node scripts/get-douyin-token.js <code> [--write]
 * 依赖 .env 或环境变量：DOUYIN_CLIENT_KEY、DOUYIN_CLIENT_SECRET
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { config } from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
config({ path: path.join(root, '.env') });

const code = process.argv[2];
const shouldWrite = process.argv.includes('--write');

if (!code || code === '--write') {
  console.log(`
用法: node scripts/get-douyin-token.js <授权码code> [--write]

  从授权回调 URL 的 code 参数拿到授权码后，传入此处即可换取 open_id 和 access_token。
  若加 --write，会把 DOUYIN_OPEN_ID 和 DOUYIN_ACCESS_TOKEN 写入项目 .env。

  需先在 .env 中配置（或环境变量）：
    DOUYIN_CLIENT_KEY=你的应用client_key
    DOUYIN_CLIENT_SECRET=你的应用client_secret

示例:
  node scripts/get-douyin-token.js ffab5ec26cd958fditn2GNr8Wx5m0i
  node scripts/get-douyin-token.js ffab5ec26cd958fditn2GNr8Wx5m0i --write
`);
  process.exit(1);
}

const clientKey = process.env.DOUYIN_CLIENT_KEY;
const clientSecret = process.env.DOUYIN_CLIENT_SECRET;
if (!clientKey || !clientSecret) {
  console.error('请先在 .env 中设置 DOUYIN_CLIENT_KEY 和 DOUYIN_CLIENT_SECRET');
  process.exit(1);
}

const body = new URLSearchParams({
  client_key: clientKey,
  client_secret: clientSecret,
  code,
  grant_type: 'authorization_code',
});

const res = await fetch('https://open.douyin.com/oauth/access_token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: body.toString(),
});

const json = await res.json();
const data = json.data;

if (data && data.error_code != null && data.error_code !== 0) {
  console.error('换取 token 失败:', data.description || json.message || JSON.stringify(json));
  process.exit(1);
}

const openId = data?.open_id;
const accessToken = data?.access_token;
if (!openId || !accessToken) {
  console.error('响应中缺少 open_id 或 access_token:', JSON.stringify(json, null, 2));
  process.exit(1);
}

console.log('open_id:', openId);
console.log('access_token:', accessToken);
console.log('expires_in(秒):', data?.expires_in);
if (data?.refresh_token) console.log('refresh_token:', data.refresh_token);

if (shouldWrite) {
  const envPath = path.join(root, '.env');
  let envContent = '';
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, 'utf8');
    const lines = envContent.split(/\r?\n/);
    const out = [];
    let hasOpenId = false;
    let hasToken = false;
    for (const line of lines) {
      if (/^\s*DOUYIN_OPEN_ID\s*=/.test(line)) {
        out.push(`DOUYIN_OPEN_ID=${openId}`);
        hasOpenId = true;
        continue;
      }
      if (/^\s*DOUYIN_ACCESS_TOKEN\s*=/.test(line)) {
        out.push(`DOUYIN_ACCESS_TOKEN=${accessToken}`);
        hasToken = true;
        continue;
      }
      out.push(line);
    }
    if (!hasOpenId) out.push(`DOUYIN_OPEN_ID=${openId}`);
    if (!hasToken) out.push(`DOUYIN_ACCESS_TOKEN=${accessToken}`);
    envContent = out.join('\n');
  } else {
    envContent = `DOUYIN_OPEN_ID=${openId}\nDOUYIN_ACCESS_TOKEN=${accessToken}\n`;
  }
  fs.writeFileSync(envPath, envContent, 'utf8');
  console.log('\n已写入 .env，之后发抖音将使用该凭证。');
}
