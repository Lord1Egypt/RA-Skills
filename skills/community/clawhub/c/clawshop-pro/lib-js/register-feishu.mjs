/**
 * 注册飞书 Bot 快捷指令 /tkseller
 * 
 * 飞书 Bot Menu API 不同于 Discord slash commands。
 * 飞书的做法是在开发者后台配置，或通过 chat_menu_tree API 给群设置菜单。
 * 
 * 这个脚本尝试多种方式注册命令。
 */
import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const OPENCLAW_CONFIG = join(homedir(), '.openclaw', 'openclaw.json');

function loadCfg() {
  return JSON.parse(readFileSync(OPENCLAW_CONFIG, 'utf-8'));
}

async function getToken(appId, appSecret) {
  const r = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
  });
  const d = await r.json();
  if (!d.tenant_access_token) throw new Error(`get token failed: ${JSON.stringify(d)}`);
  return d.tenant_access_token;
}

async function main() {
  const cfg = loadCfg();
  const feishu = cfg.channels?.feishu || {};
  const appId = feishu.appId;
  const appSecret = feishu.appSecret;
  if (!appId || !appSecret) {
    console.log(JSON.stringify({ ok: false, error: 'feishu appId/appSecret not configured' }));
    process.exit(1);
  }

  const token = await getToken(appId, appSecret);

  // 方式1: 尝试 /open-apis/bot/v3/menu/create（旧版）
  let resp;
  try {
    resp = await fetch('https://open.feishu.cn/open-apis/bot/v3/menu/create', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        menu: {
          type: 'redirect',
          name: '/tkseller',
          redirect_url: '',
        },
      }),
    });
    const text = await resp.text();
    console.log('bot/v3/menu:', text);
  } catch (e) {
    console.log('bot/v3/menu error:', e.message);
  }

  // 方式2: 尝试发送 application bot command 设置
  try {
    resp = await fetch('https://open.feishu.cn/open-apis/application/v6/applications/' + appId + '/bot/commands', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        commands: [{
          command: 'tkseller',
          description: '自动带货 - 输入视频URL或留空推荐热门',
        }],
      }),
    });
    const text = await resp.text();
    console.log('application bot commands:', text);
  } catch (e) {
    console.log('application bot commands error:', e.message);
  }

  // 方式3: 查看 bot 已有的 commands
  try {
    resp = await fetch('https://open.feishu.cn/open-apis/application/v6/applications/' + appId + '?lang=zh_cn', {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    const d = await resp.json();
    console.log('app detail:', JSON.stringify(d, null, 2));
  } catch (e) {
    console.log('app detail error:', e.message);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
