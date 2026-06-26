/**
 * 页面选择器诊断工具
 * 运行后会打开 eBay 商品页，打印各类选择器的命中情况
 */

const ads = require('./ads_api');
const WebSocket = require('ws');
const http = require('http');
const config = require('./config');

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  if (process.argv.length < 3) {
    console.error('用法: node diag_selectors2.js <user_id>');
    process.exit(1);
  }
  const userId = process.argv[2];

  console.log('正在启动浏览器...');
  const browserData = await ads.startBrowser(userId);
  const debugPort = browserData.debug_port;
  console.log(`debug_port: ${debugPort}`);

  // 连接 browser WS
  const browserWs = await new Promise((resolve, reject) => {
    const ws = new WebSocket(browserData.ws?.puppeteer);
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });
  await delay(2000);

  // 创建页面
  let msgId = 0;
  const pending = {};
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++msgId;
    const timer = setTimeout(() => { delete pending[id]; reject(new Error(`timeout: ${method}`)); }, 20000);
    pending[id] = { resolve, timer };
    browserWs.send(JSON.stringify({ id, method, params }));
  });
  browserWs.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id && pending[msg.id]) { clearTimeout(pending[msg.id].timer); pending[msg.id].resolve(msg.result || msg); }
  });

  const newTarget = await send('Target.createTarget', { url: 'about:blank' });
  await delay(1000);

  const pageList = await new Promise((resolve) => {
    http.get(`http://127.0.0.1:${debugPort}/json`, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch(e) { resolve([]); } });
    }).on('error', () => resolve([]));
  });
  const newPage = pageList.find(p => p.url === 'about:blank' && p.type === 'page');
  const pageWs = await new Promise((resolve, reject) => {
    const ws = new WebSocket(newPage.webSocketDebuggerUrl);
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });

  const pagePending = {};
  const pSend = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++msgId;
    const timer = setTimeout(() => { delete pagePending[id]; reject(new Error(`timeout: ${method}`)); }, 20000);
    pagePending[id] = { resolve, timer };
    pageWs.send(JSON.stringify({ id, method, params }));
  });
  pageWs.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id && pagePending[msg.id]) { clearTimeout(pagePending[msg.id].timer); pagePending[msg.id].resolve(msg.result || msg); }
  });

  await pSend('Page.enable');
  await delay(500);

  // 导航到 eBay 商品页
  console.log('\n导航到商品页...');
  await pSend('Page.navigate', { url: 'https://www.ebay.com/itm/254288769712' });
  await delay(6000);

  console.log('\n========== 选择器诊断结果 ==========\n');

  // 测试收藏按钮
  const watchSelectors = [
    '.x-watch-heart-btn',
    '.dp-watchlist-toggle-button',
    'svg[aria-label="Watchlist"]',
    'svg[data-test-id="heart"]',
    '#watchit',
    'button[data-test-id="watch-list-dropdown-trigger"]',
  ];

  console.log('【收藏按钮】');
  for (const sel of watchSelectors) {
    const r = await pSend('Runtime.evaluate', {
      expression: `!!document.querySelector('${sel}')`,
      returnByValue: true,
    });
    console.log(`  ${sel}: ${r?.result?.value ? '✅ 找到' : '❌ 未找到'}`);
  }

  // 测试加购按钮
  const cartSelectors = [
    '#atcBtn_btn_1',
    'button[data-test-id="add-to-cart"]',
    'a.ux-call-to-action',
    'a[data-test-id="add-to-cart"]',
  ];

  console.log('\n【加购按钮】');
  for (const sel of cartSelectors) {
    const r = await pSend('Runtime.evaluate', {
      expression: `!!document.querySelector('${sel}')`,
      returnByValue: true,
    });
    console.log(`  ${sel}: ${r?.result?.value ? '✅ 找到' : '❌ 未找到'}`);
  }

  // 测试搜索框
  const searchSelectors = ['#gh-ac', 'input[name="_nkw"]', 'input[placeholder*="Search"]'];
  console.log('\n【搜索框】');
  for (const sel of searchSelectors) {
    const r = await pSend('Runtime.evaluate', {
      expression: `!!document.querySelector('${sel}')`,
      returnByValue: true,
    });
    console.log(`  ${sel}: ${r?.result?.value ? '✅ 找到' : '❌ 未找到'}`);
  }

  // 商品链接
  console.log('\n【商品链接】');
  const linkR = await pSend('Runtime.evaluate', {
    expression: `document.querySelectorAll('a[href*="/itm/"]').length`,
    returnByValue: true,
  });
  console.log(`  商品链接总数: ${linkR?.result?.value}`);

  console.log('\n诊断完成，正在关闭浏览器...');
  pageWs.close();
  browserWs.close();
  await ads.stopBrowser(userId);
}

main().catch(e => { console.error(e); process.exit(1); });
