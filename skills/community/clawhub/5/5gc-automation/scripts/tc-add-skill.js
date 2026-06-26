/**
 * tc-add-skill.js - Traffic Control 流量控制模板添加工具
 *
 * 用法：
 *   node tc-add-skill.js --project XW_SUPF_5_1_2_4 --tc-id tc_new --flow-status ENABLED-UPLINK [--headed]
 *
 * 参数：
 *   --project       工程名（默认 XW_S5GC_1）
 *   --tc-id         TC模板ID（必填，字母/数字/下划线）
 *   --flow-status   flowStatus（默认 ENABLED-UPLINK）
 *                  可选值：ENABLED-UPLINK, ENABLED-DOWNLINK, ENABLED, DISABLED, REMOVED
 *   --headed        显示浏览器窗口
 *
 * 完整链路：
 *   点击"添加" → 弹窗 iframe（layui-layer-iframe2）→ 填写 tcId + flowStatus（SELECT）
 *   → 提交 → 返回列表页
 *
 * 注意事项：
 *   - flowStatus 是 SELECT 下拉框，用 JS 方式设置值（layui 隐藏原生select）
 *   - tcId 是必填字段
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    project: 'XW_S5GC_1',
    tcId: null,
    flowStatus: 'ENABLED-UPLINK',
    headed: false,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' || args[i] === '-p') opts.project = args[++i];
    else if (args[i] === '--tc-id') opts.tcId = args[++i];
    else if (args[i] === '--flow-status') opts.flowStatus = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }

  if (!opts.tcId) {
    console.error('❌ 缺少必要参数: --tc-id');
    console.error('   示例: node tc-add-skill.js --project XW_SUPF_5_1_2_4 --tc-id tc_new --flow-status ENABLED-UPLINK');
    process.exit(1);
  }

  return opts;
}

async function login(page) {
  await page.goto(`${globalBaseUrl}/login`, { ignoreHTTPSErrors: true, timeout: 15000, waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  try { await page.locator('input[name="email"]').first().waitFor({ state: 'visible', timeout: 5000 }); } catch(e) {}
  await page.getByRole('textbox', { name: 'E-Mail地址' }).fill('dotouch@dotouch.com.cn');
  await page.getByRole('textbox', { name: '密码' }).fill('dotouch');
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForTimeout(2500);
  console.log('✅ 登录成功');
}

async function selectProject(page, projectName) {
  await page.goto(`${globalBaseUrl}/sim_5gc/project/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(2000);

  await page.locator('input[name="project_search_name"]').fill(projectName);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  const clicked = await page.evaluate((name) => {
    const rows = document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === name) {
        cells[1].querySelector('.iconfont').click();
        return true;
      }
    }
    return false;
  }, projectName);

  if (!clicked) { console.error(`❌ 未找到工程: ${projectName}`); process.exit(1); }
  await page.waitForTimeout(3000);
  console.log(`✅ 工程 "${projectName}" 已选`);
}

async function main() {
  const opts = parseArgs();
  const browser = await chromium.launch({ headless: !opts.headed, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  await login(page);
  await selectProject(page, opts.project);

  // 去 TC 列表页
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/trafficCtl/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  console.log(`✅ 到达TC列表页`);

  // 点击添加按钮
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(5000);

  // 获取弹窗 iframe（layui-layer-iframe2）
  const frame = page.frame('layui-layer-iframe2');
  if (!frame) { console.error('❌ 未找到弹窗iframe'); process.exit(1); }
  console.log(`✅ 进入弹窗iframe`);

  // 填写 tcId
  await frame.locator('input[name="tcId"]').fill(opts.tcId);
  console.log(`   tcId="${opts.tcId}"`);

  // 设置 flowStatus（用 JS 方式，因为 layui 隐藏了原生 select）
  await frame.evaluate((status) => {
    const sel = document.querySelector('select[name="flowStatus"]');
    if (sel) { sel.value = status; sel.dispatchEvent(new Event('change', { bubbles: true })); }
  }, opts.flowStatus);
  console.log(`   flowStatus="${opts.flowStatus}"`);

  // 提交
  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`✅ TC模板 ${opts.tcId} 已提交`);

  // 验证
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/trafficCtl/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);

  const tcData = await page.evaluate((targetId) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 4 && cells[2].textContent.trim() === targetId) {
        return { tcId: cells[2].textContent.trim(), flowStatus: cells[3].textContent.trim() };
      }
    }
    return null;
  }, opts.tcId);

  if (tcData) {
    console.log('\n📋 验证结果:');
    console.log(`   tcId      = ${tcData.tcId}`);
    console.log(`   flowStatus = ${tcData.flowStatus} ${tcData.flowStatus === opts.flowStatus ? '✅' : '❌'}`);
  } else {
    console.log('\n❌ TC模板未找到');
  }

  console.log('\n✅ 完成');
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });