/**
 * NRF 添加脚本
 * 完整流程：登录 → 选工程 → 进NRF列表 → 点添加(弹窗iframe) → 填表单 → 提交
 * 用法: node nrf-add-skill.js <名称> [--project <工程>] [--url <地址>] [--headed] \
 *       [--http2_sip <IP>] [--http2_port <端口>] [--MCC <值>] [--MNC <值>]
 * 示例: node nrf-add-skill.js NRF-TEST --project XW_S5GC_1
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'https://192.168.3.89';
const SESSION_DIR = path.join(__dirname, '.sessions');

function getSessionFile(baseUrl) {
  const host = baseUrl.replace(/https?:\/\//, '').replace(/\./g, '_');
  return `5gc_session_${host}.json`;
}

async function login(page, baseUrl) {
  const sessionPath = path.join(SESSION_DIR, getSessionFile(baseUrl));
  if (fs.existsSync(sessionPath)) {
    try {
      const storageState = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));
      if (storageState.cookies) {
        await page.context().addCookies(storageState.cookies);
        await page.goto(baseUrl + '/sim_5gc/project/index', { waitUntil: 'networkidle', timeout: 8000 }).catch(() => {});
        if (!page.url().includes('/login')) {
          console.log('  ✅ 使用缓存会话');
          return true;
        }
      }
    } catch {}
  }
  await page.goto(baseUrl + '/login', { waitUntil: 'networkidle', timeout: 15000 });
  await page.getByRole('textbox', { name: 'E-Mail地址' }).fill('dotouch@dotouch.com.cn');
  await page.getByRole('textbox', { name: '密码' }).fill('dotouch');
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForLoadState('networkidle');
  const ctx = page.context();
  const storageState = await ctx.storageState();
  fs.writeFileSync(sessionPath, JSON.stringify({ cookies: storageState.cookies }, null, 2));
  console.log('  ✅ 登录成功');
  return true;
}

async function selectProject(page, projectName) {
  await page.goto(BASE_URL + '/sim_5gc/project/index', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForSelector('.jsgrid-row, .jsgrid-alt-row', { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(300);

  for (let pageNum = 1; pageNum <= 200; pageNum++) {
    const clicked = await page.evaluate((targetName) => {
      const rows = document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row');
      for (const row of rows) {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 3 && cells[2].textContent.trim() === targetName) {
          const icon = cells[1].querySelector('.iconfont');
          if (icon) { icon.click(); return true; }
        }
      }
      return false;
    }, projectName);

    if (clicked) { await page.waitForTimeout(2000); return true; }

    const nextBtn = page.locator('.jsgrid-pager a:has-text("Next")');
    if (!(await nextBtn.count())) break;
    try { await nextBtn.click(); } catch { break; }
    await page.waitForTimeout(1500);
  }
  console.log(`  ❌ 未找到工程 "${projectName}"`);
  return false;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log('用法: node nrf-add-skill.js <名称> [--project <工程>] [--url <地址>] [--headed]');
    console.log('       [--http2_sip <IP>] [--http2_port <端口>] [--MCC <值>] [--MNC <值>]');
    console.log('示例: node nrf-add-skill.js NRF-TEST --project XW_S5GC_1');
    process.exit(1);
  }

  const name = args[0];
  let headless = true;
  let project = 'XW_S5GC_1';
  let http2_sip = '192.168.20.100';
  let http2_port = '80';
  let mcc = '460';
  let mnc = '01';

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--headed') headless = false;
    else if (args[i] === '--project') project = args[++i];
    else if (args[i] === '--url') BASE_URL = args[++i];
    else if (args[i] === '--http2_sip') http2_sip = args[++i];
    else if (args[i] === '--http2_port') http2_port = args[++i];
    else if (args[i] === '--MCC') mcc = args[++i];
    else if (args[i] === '--MNC') mnc = args[++i];
  }

  console.log(`▶ 添加 NRF: ${name}`);
  console.log(`  http2_sip=${http2_sip} http2_port=${http2_port} MCC=${mcc} MNC=${mnc}`);
  console.log(`  工程: ${project}`);

  const browser = await chromium.launch({ headless, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  await login(page, BASE_URL);
  const ok = await selectProject(page, project);
  if (!ok) throw new Error('工程选择失败');
  console.log('  ✓ 工程已选');

  // 进 NRF 列表（先点"核心网"菜单，再点"NRF"）
  await page.evaluate(() => {
    const links = document.querySelectorAll('a[href*="/nrf/"]');
    for (const l of links) {
      if (l.textContent.trim().includes('NRF')) { l.click(); return; }
    }
  });
  await page.waitForTimeout(3000);
  console.log('  ✓ 进入NRF列表，URL:', page.url());

  // 点添加按钮
  await page.waitForSelector('button:has-text("添加")', { timeout: 10000 }).catch(() => {});
  await page.locator('button:has-text("添加")').first().click();
  await page.waitForTimeout(2000);
  console.log('  ✓ 点添加（弹窗）');

  // 切换到弹窗 iframe
  await page.locator('iframe[name="layui-layer-iframe2"]').waitFor({ timeout: 5000 });
  const frame = page.frame('layui-layer-iframe2');
  if (!frame) throw new Error('未找到弹窗 iframe');
  await frame.waitForLoadState('domcontentloaded');
  console.log('  ✓ 切换到弹窗iframe');

  // 名称
  await frame.locator('input[name="name"]').fill(name);
  console.log(`  ✓ name = ${name}`);

  // 类型下拉
  await frame.getByRole('textbox', { name: '请选择' }).first().click();
  await frame.getByRole('definition').filter({ hasText: '仿真设备' }).click();
  await page.waitForTimeout(500);
  console.log('  ✓ 类型 = 仿真设备');

  // MCC
  await frame.getByRole('textbox', { name: '三位数字', exact: true }).fill(mcc);
  console.log(`  ✓ MCC = ${mcc}`);

  // MNC
  await frame.getByRole('textbox', { name: '二位或三位数字' }).fill(mnc);
  console.log(`  ✓ MNC = ${mnc}`);

  // HTTP2 SIP
  await frame.locator('input[name="http2_sip"]').fill(http2_sip);
  console.log(`  ✓ http2_sip = ${http2_sip}`);

  // HTTP2 PORT
  await frame.locator('input[name="http2_port"]').fill(http2_port);
  console.log(`  ✓ http2_port = ${http2_port}`);

  // 提交
  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log('  ✓ 已提交');

  const url = page.url();
  if (url.includes('/nrf/index')) {
    console.log(`  ✅ 添加成功，URL: ${url}`);
  } else {
    console.log(`  ⚠️ 可能未保存，URL: ${url}`);
  }

  await browser.close();
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
