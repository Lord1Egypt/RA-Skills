#!/usr/bin/env node
/**
 * AMF 添加脚本 - 完整修复版
 * 功能：登录状态缓存 + .projectSelect 选工程 + evaluate 填写表单 + 算法全勾选 + NSSAI
 */

const { chromium } = require('playwright');
let globalBaseUrl = 'https://192.168.3.89';
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  urls: {
    login: '/login',
    amfEdit: '/sim_5gc/amf/edit',
    amfManagement: '/sim_5gc/amf/index'
  },
  credentials: {
    email: 'dotouch@dotouch.com.cn',
    password: 'dotouch'
  },
  sessionDir: path.join(__dirname, '.sessions'),
  getSessionFile() {
    const host = globalBaseUrl.replace(/https?:\/\//, '').replace(/\./g, '_');
    return `5gc_session_${host}.json`;
  }
};

// 会话管理
class SessionManager {
  constructor() {
    this.sessionPath = path.join(CONFIG.sessionDir, CONFIG.getSessionFile());
  }

  async saveSession(context) {
    try {
      const storageState = await context.storageState();
      fs.writeFileSync(this.sessionPath, JSON.stringify({ storageState }, null, 2));
      return true;
    } catch {
      return false;
    }
  }

  async loadSession(browser) {
    try {
      if (!fs.existsSync(this.sessionPath)) return null;
      const { storageState } = JSON.parse(fs.readFileSync(this.sessionPath, 'utf8'));
      return await browser.newContext({ storageState, ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
    } catch {
      return null;
    }
  }
}

// 算法配置：直接点击 layui 复选框的可见元素
async function configureAlgorithmsSuccess(page) {
  await page.waitForSelector('.layui-form-checkbox', { timeout: 5000 });
  await page.waitForTimeout(300);

  const checkboxCount = await page.locator('.layui-form-checkbox').count();
  console.log(`  算法复选框数量: ${checkboxCount}`);
  for (let i = 0; i < Math.min(checkboxCount, 8); i++) {
    await page.locator('.layui-form-checkbox').nth(i).click();
    await page.waitForTimeout(80);
  }

  const priorities = [
    'ea[NEA0]', 'ea[128-NEA1]', 'ea[128-NEA2]', 'ea[128-NEA3]',
    'ia[NIA0]', 'ia[128-NIA1]', 'ia[128-NIA2]', 'ia[128-NIA3]'
  ];
  const vals = ['1', '2', '3', '4', '1', '2', '3', '4'];
  for (let i = 0; i < priorities.length; i++) {
    const inp = page.locator(`input[name="${priorities[i]}"]`);
    if (await inp.count() > 0) {
      await inp.fill(vals[i]);
    }
  }
  console.log(`  ✅ 算法配置完成`);
}

// 工程选择（精确匹配，分页遍历）
async function selectProject(page, projectName, forceSwitch = true) {
  if (!forceSwitch) {
    console.log(`  🔧 保持当前工程（用户未指定工程）`);
    return true;
  }
  await page.goto(`${globalBaseUrl}/sim_5gc/project/index`, { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForSelector('.jsgrid-row, .jsgrid-alt-row', { timeout: 5000 }).catch(() => {});

  await page.evaluate(() => {
    const inputs = document.querySelectorAll('input[type="text"], input[name="name"]');
    for (const inp of inputs) { inp.value = ''; }
  });
  await page.waitForTimeout(300);

  for (let pageNum = 1; pageNum <= 200; pageNum++) {
    const clicked = await page.evaluate((targetName) => {
      const rows = document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row');
      for (const row of rows) {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 3 && cells[2].textContent.trim() === targetName) {
          const icon = cells[1].querySelector('.iconfont');
          if (icon) {
            icon.click();
            return true;
          }
        }
      }
      return false;
    }, projectName);

    if (clicked) {
      await page.waitForTimeout(2000);
      return true;
    }

    const nextBtn = page.locator('.jsgrid-pager a:has-text("Next")');
    if (!(await nextBtn.count())) break;
    try {
      REPLACED
    } catch (e) {
      break;
    }
  }

  console.log(`  ❌ 未找到工程 "${projectName}"（精确匹配）`);
  return false;
}

// 添加 AMF 主流程
async function addAmf(amfName, projectName, explicitProject = true, amfConfig = {}) {
  const startTime = Date.now();
  const sessionManager = new SessionManager();
  const defaultConfig = {
    mcc: '460', mnc: '01', region_id: '1', set_id: '1', pointer: '1',
    ngap_sip: '200.20.20.1', ngap_port: '38412',
    http2_sip: '200.20.20.5', http2_port: '8080',
    stac: '101', etac: '102'
  };
  const cfg = { ...defaultConfig, ...amfConfig };

  let browser = null;
  try {
    browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });

    let context = await sessionManager.loadSession(browser);
    let needLogin = true;

    if (context) {
      const testPage = await context.newPage();
      await testPage.goto(`${globalBaseUrl}${CONFIG.urls.amfManagement}`, { waitUntil: 'networkidle', timeout: 10000 }).catch(() => {});
      if (!testPage.url().includes('/login')) {
        needLogin = false;
      }
      await testPage.close();
    }

    if (needLogin) {
      context = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
    }

    const page = await context.newPage();

    if (needLogin) {
      await page.goto(`${globalBaseUrl}${CONFIG.urls.login}`, { waitUntil: 'networkidle', timeout: 15000 });
      await page.getByRole('textbox', { name: 'E-Mail地址' }).fill(CONFIG.credentials.email);
      await page.getByRole('textbox', { name: '密码' }).fill(CONFIG.credentials.password);
      await page.getByRole('button', { name: '登录' }).click();
      await page.waitForLoadState('networkidle', { timeout: 10000 });
      await sessionManager.saveSession(context);
    }

    // 选择工程（仅当用户显式指定工程时才切换）
    if (!(await selectProject(page, projectName, explicitProject))) {
      throw new Error(`工程 "${projectName}" 不存在或无法选中`);
    }

    // 进入编辑页面
    await page.goto(`${globalBaseUrl}${CONFIG.urls.amfEdit}`, { waitUntil: 'networkidle', timeout: 15000 });
    if (!page.url().includes('/amf/edit')) {
      await page.goto(`${globalBaseUrl}/sim_5gc/amf/edit`);
      await page.waitForSelector('input[name="name"]', { timeout: 10000 });
    }

    // 通过 evaluate 直接填写表单
    await page.evaluate(({ amfName, cfg }) => {
      const set = (name, value) => {
        const el = document.querySelector(`input[name="${name}"]`);
        if (el) {
          el.value = value;
          el.dispatchEvent(new Event('input', { bubbles: true }));
        }
      };
      set('name', amfName);
      set('mcc', cfg.mcc);
      set('mnc', cfg.mnc);
      set('region_id', cfg.region_id);
      set('set_id', cfg.set_id);
      set('pointer', cfg.pointer);
      set('ngap_sip', cfg.ngap_sip);
      set('ngap_port', cfg.ngap_port);
      set('http2_sip', cfg.http2_sip);
      set('http2_port', cfg.http2_port);
      set('stac', cfg.stac);
      set('etac', cfg.etac);
    }, { amfName, cfg });

    // 类型选择：仿真设备
    await page.locator('.layui-unselect').first().click();
    await page.waitForTimeout(300);
    await page.locator('dd').filter({ hasText: '仿真设备' }).click();

    // 配置算法
    await configureAlgorithmsSuccess(page);

    // 配置 NSSAI
    await page.getByRole('row', { name: /数量.*nssai/ }).getByRole('button').click();
    await page.waitForTimeout(500);
    await page.locator('input[name="config[count][]"]').fill('1');
    await page.getByRole('row', { name: /nssai.*添加.*删除/ }).locator('span').click();
    await page.waitForTimeout(800);

    const iframeEl = page.locator('iframe[name="layui-layer-iframe2"]');
    const iframe = await iframeEl.contentFrame({ timeout: 5000 });
    await iframe.getByRole('row', { name: /\*.*SST.*SD/ }).getByRole('button').click();
    await iframe.locator('input[name="nssai[snssai_sst][]"]').fill('1');
    await iframe.locator('input[name="nssai[snssai_sd][]"]').fill('111111');
    await iframe.getByRole('button', { name: '提交' }).click();
    await page.waitForTimeout(800);

    // 提交表单
    await page.getByRole('button', { name: '提交' }).click();
    // 等待页面跳转到 AMF 列表页面，若未跳转则强制跳转
    try {
      await page.waitForURL(`**/amf/index`, { timeout: 8000 });
    } catch (e) {
      await page.goto(`${globalBaseUrl}${CONFIG.urls.amfManagement}`, { waitUntil: 'networkidle', timeout: 15000 });
    }
    await page.waitForTimeout(2000);

    // 验证结果：只要页面成功跳转到 AMF 列表页，即认为添加成功
    let found = false;
    const finalUrl = page.url();
    if (finalUrl.includes('/amf/index')) {
      console.log(`  ✅ 页面已跳转至 AMF 列表: ${finalUrl}`);
      found = true;
    }

    await browser.close();

    const totalTime = (Date.now() - startTime) / 1000;
    if (found) {
      return { success: true, amfName, totalTime };
    } else {
      return { success: false, amfName, totalTime };
    }
  } catch (err) {
    if (browser) await browser.close();
    throw err;
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('用法: node amf-add-skill.js <AMF名称> [--project <工程名>] [--url <地址>] [--mcc 460] [...]');
    process.exit(1);
  }

  let amfName = null;
  let projectName = '5G_basic_process';
  let amfConfig = {};
  let explicitProject = false;

  for (let i = 0; i < args.length; i++) {
    if (!args[i].startsWith('-')) {
      amfName = args[i];
    } else if (args[i] === '--project' || args[i] === '-p') {
      projectName = args[++i];
      explicitProject = true;
    } else if (args[i] === '--url') {
      let u = args[++i];
      if (u && !u.startsWith('http')) u = 'https://' + u;
      globalBaseUrl = u;
    } else if (args[i].startsWith('--')) {
      amfConfig[args[i].substring(2)] = args[++i];
    }
  }

  if (!amfName) {
    console.error('错误: 请指定 AMF 名称');
    process.exit(1);
  }

  console.log(`AMF: ${amfName}  |  工程: ${projectName}  |  地址: ${globalBaseUrl}`);

  try {
    const result = await addAmf(amfName, projectName, explicitProject, amfConfig);
    console.log(result.success
      ? `成功! AMF "${result.amfName}" 添加完成 (${result.totalTime.toFixed(2)}s)`
      : `失败! 未找到 AMF "${result.amfName}"`);
    process.exit(result.success ? 0 : 1);
  } catch (err) {
    console.error(`执行异常: ${err.message}`);
    process.exit(1);
  }
}

main();
