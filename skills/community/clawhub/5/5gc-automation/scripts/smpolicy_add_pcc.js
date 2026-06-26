/**
 * smpolicy_add_pcc.js - 将 PCC 规则添加到 sm_policy_default 的 pccRules
 *
 * 用法:
 *   node smpolicy_add_pcc.js --project XW_SUPF_5_1_2_4 --pcc-id pcc_new
 *
 * 参数:
 *   --project     工程名（默认 XW_SUPF_5_1_2_4）
 *   --pcc-id      PCC规则ID（必填，需已存在）
 *   --headed      显示浏览器窗口
 *
 * 完整链路:
 *   smpolicy/default/index → 编辑 sm_policy_default 弹窗（iframe）
 *   → pccRules xm-select（第1个）中添加 --pcc-id
 *   → 提交
 *
 * xm-select 交互（Playwright locator）：
 *   1. JS: inputs[idx].parentElement.click() 打开下拉
 *   2. frame.locator('.xm-option.show-icon', {hasText}).click() 选择选项
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    project: 'XW_SUPF_5_1_2_4',
    pccId: null,
    headed: false,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' || args[i] === '-p') opts.project = args[++i];
    else if (args[i] === '--pcc-id') opts.pccId = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }
  if (!opts.pccId) {
    console.error('❌ 缺少 --pcc-id 参数');
    process.exit(1);
  }
  return opts;
}

async function login(page) {
  await page.goto(`${globalBaseUrl}/login`, { ignoreHTTPSErrors: true, timeout: 15000 });
  await page.waitForTimeout(1500);
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
    let result = false;
    document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === name) {
        cells[1].querySelector('.iconfont')?.click();
        result = true;
      }
    });
    return result;
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

  // 导航到 smpolicy/default/index
  await page.goto(`${globalBaseUrl}/sim_5gc/smpolicy/default/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  console.log('✅ 到达 smpolicy/default/index');

  // 点击"编辑"按钮（第1行 sm_policy_default）
  await page.evaluate(() => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    if (rows.length > 0) {
      const editBtn = rows[0].querySelector('a');
      if (editBtn) editBtn.click();
    }
  });
  await page.waitForTimeout(3000);

  // 进入弹窗 iframe
  const frame = page.frame('layui-layer-iframe2');
  if (!frame) { console.error('❌ 未找到弹窗iframe'); process.exit(1); }
  console.log('✅ 进入弹窗iframe');

  // 检查当前 pccRules 的值（pccRules = xm-select[1]）
  const before = await frame.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs.length >= 2) {
      return {
        pccRulesValue: inputs[1].value,
        pccRulesDisplay: inputs[1].parentElement.textContent.substring(0, 80),
      };
    }
    return null;
  });
  console.log('\n📋 编辑前状态:', JSON.stringify(before));

  // 打开 pccRules 下拉（第1个xm-select）
  console.log(`\n▶ 添加 ${opts.pccId} 到 pccRules...`);
  await frame.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs[1]) inputs[1].parentElement.click();
  });
  await page.waitForTimeout(1000);

  // 用 Playwright locator 点击选项
  const optLocator = frame.locator('.xm-option.show-icon', { hasText: opts.pccId });
  const visible = await optLocator.isVisible({ timeout: 3000 }).catch(() => false);
  if (visible) {
    await optLocator.click();
    console.log(`   ✅ 选择 ${opts.pccId}`);
  } else {
    console.log(`   ❌ 选项 ${opts.pccId} 不可见`);
    const availOpts = await frame.evaluate(() =>
      Array.from(document.querySelectorAll('.xm-option.show-icon')).map(o => o.textContent.trim())
    );
    console.log(`   可用选项: ${availOpts.join(', ')}`);
  }
  await page.waitForTimeout(500);

  // 关闭 xm-select 下拉（按 Escape 避免遮罩层）
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);

  // 提交
  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log('✅ 已提交');

  // 验证
  await page.goto(`${globalBaseUrl}/sim_5gc/smpolicy/default/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);

  const updated = await page.evaluate((targetPccId) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 6 && cells[2].textContent.trim() === 'sm_policy_default') {
        return { pccRules: cells[4].textContent.trim() };
      }
    }
    return null;
  }, opts.pccId);

  if (updated) {
    console.log('\n📋 更新后 pccRules:', updated.pccRules);
    console.log(updated.pccRules.includes(opts.pccId) ? `\n🎉 成功将 ${opts.pccId} 添加到 pccRules!` : `\n⚠️ 未检测到 ${opts.pccId}`);
  }

  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });