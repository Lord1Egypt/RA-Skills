/**
 * pcc-add-skill.js - PCC规则添加工具（修复版）
 *
 * 用法：
 *   node pcc-add-skill.js --project XW_SUPF_5_1_2_4 --pcc-id pcc_new --qos qos2 --tc tc1 [--precedence 63] [--headed]
 *
 * 参数：
 *   --project     工程名（默认 XW_S5GC_1）
 *   --pcc-id     新PCC规则ID（必填，字母/数字/下划线）
 *   --precedence  优先级（默认 63，用户指定时用指定值）
 *   --qos         QoS模板名称（必填，如 qos1 / qos2）
 *   --tc          流量控制名称（必填，如 tc1）
 *   --flow-desc   流描述（可选）
 *   --headed      显示浏览器窗口
 *
 * 完整链路：
 *   点击"添加" → 主框架跳转 /predfPolicy/pcc/edit
 *   → 填写 pccRuleId + precedence
 *   → xm-select 选 qos（第0个）+ tc（第1个）+ 可选chg（第2个）
 *   → 提交 → 返回列表页
 *
 * xm-select 交互（Playwright locator）：
 *   1. JS: inputs[idx].parentElement.click() 打开下拉
 *   2. Playwright locator: page.locator('.xm-option.show-icon', {hasText}).click() 选择选项
 *   3. page.keyboard.press('Escape') 关闭下拉
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    project: 'XW_S5GC_1',
    pccId: null,
    precedence: null,   // null = 使用默认值63
    qos: null,          // 必填
    tc: null,           // 必填
    flowDesc: null,
    headed: false,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' || args[i] === '-p') opts.project = args[++i];
    else if (args[i] === '--pcc-id') opts.pccId = args[++i];
    else if (args[i] === '--precedence') opts.precedence = args[++i];
    else if (args[i] === '--qos') opts.qos = args[++i];
    else if (args[i] === '--tc') opts.tc = args[++i];
    else if (args[i] === '--flow-desc') opts.flowDesc = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }

  if (!opts.pccId) {
    console.error('❌ 缺少 --pcc-id 参数');
    process.exit(1);
  }
  if (!opts.qos) {
    console.error('❌ 缺少 --qos 参数（QoS模板名称）');
    process.exit(1);
  }
  if (!opts.tc) {
    console.error('❌ 缺少 --tc 参数（流量控制名称）');
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

  // 先尝试搜索工程名
  await page.locator('input[name="project_search_name"]').fill(projectName);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  const clicked = await page.evaluate((name) => {
    const rows = document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === name) {
        const icon = cells[1].querySelector('.iconfont');
        if (icon) { icon.click(); return true; }
      }
    }
    return false;
  }, projectName);

  if (!clicked) {
    // 尝试逐页查找
    for (let p = 1; p <= 100; p++) {
      const found = await page.evaluate((name) => {
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
      if (found) break;

      const hasNext = await page.evaluate(() => {
        const links = document.querySelectorAll('.jsgrid-pager a');
        for (const l of links) {
          if (l.textContent.trim() === 'Next' && !l.classList.contains('jsgrid-pager-disabled')) return true;
        }
        return false;
      });
      if (!hasNext) break;
      await page.evaluate(() => {
        const links = document.querySelectorAll('.jsgrid-pager a');
        for (const l of links) {
          if (l.textContent.trim() === 'Next') { l.click(); return; }
        }
      });
      await page.waitForTimeout(2000);
    }
  }

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

  // 去 PCC 列表页
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/pcc/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  console.log(`✅ 到达PCC列表页`);

  // 点击添加按钮
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);

  // 等待输入框出现（URL跳转完成）
  await page.waitForFunction(() => window.location.href.includes('/predfPolicy/pcc/edit'), { timeout: 10000 });
  await page.waitForTimeout(3000);
  console.log(`✅ 到达添加页: ${page.url()}`);

  // 填写文本字段
  const precedence = opts.precedence !== null ? String(opts.precedence) : '63';
  await page.locator('input[name="pccRuleId"]').fill(opts.pccId);
  await page.locator('input[name="precedence"]').fill(precedence);
  console.log(`   pccRuleId="${opts.pccId}", precedence="${precedence}"${opts.precedence !== null ? '（用户指定）' : '（默认63）'}`);

  // ── xm-select[0] = refQosData ──────────────────────────────────
  await page.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs[0]) inputs[0].parentElement.click();
  });
  await page.waitForTimeout(1000);
  const qosVisible = await page.locator('.xm-option.show-icon', { hasText: opts.qos }).isVisible({ timeout: 3000 }).catch(() => false);
  if (qosVisible) {
    await page.locator('.xm-option.show-icon', { hasText: opts.qos }).click();
    console.log(`   ✅ refQosData=${opts.qos} 已选`);
  } else {
    console.log(`   ❌ refQosData=${opts.qos} 不可见`);
  }
  await page.waitForTimeout(500);

  // ── xm-select[1] = refTcData ─────────────────────────────────
  await page.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs[1]) inputs[1].parentElement.click();
  });
  await page.waitForTimeout(1000);
  const tcVisible = await page.locator('.xm-option.show-icon', { hasText: opts.tc }).isVisible({ timeout: 3000 }).catch(() => false);
  if (tcVisible) {
    await page.locator('.xm-option.show-icon', { hasText: opts.tc }).click();
    console.log(`   ✅ refTcData=${opts.tc} 已选`);
  } else {
    console.log(`   ❌ refTcData=${opts.tc} 不可见`);
  }
  await page.waitForTimeout(500);

  // ── xm-select[2] = refChgData（可选，如有则自动选第一个）────────
  await page.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs[2]) inputs[2].parentElement.click();
  });
  await page.waitForTimeout(1000);
  const firstChg = page.locator('.xm-option.show-icon').first();
  if (await firstChg.isVisible({ timeout: 2000 }).catch(() => false)) {
    const txt = await firstChg.textContent();
    await firstChg.click();
    console.log(`   ℹ️ refChgData=(${txt.trim()}) 已选`);
  }
  await page.waitForTimeout(500);

  // 关闭 xm-select 下拉（按 Escape 避免遮罩拦截提交按钮）
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);

  // 提交
  await page.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`✅ PCC规则 ${opts.pccId} 已提交`);

  // 验证
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/pcc/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);

  const pccData = await page.evaluate((targetId) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 8 && cells[2].textContent.trim() === targetId) {
        return {
          pccRuleId: cells[2].textContent.trim(),
          precedence: cells[4].textContent.trim(),
          refQosData: cells[5].textContent.trim(),
          refTcData: cells[6].textContent.trim(),
        };
      }
    }
    return null;
  }, opts.pccId);

  if (pccData) {
    console.log('\n📋 验证结果:');
    console.log(`   pccRuleId  = ${pccData.pccRuleId}`);
    console.log(`   precedence = ${pccData.precedence}`);
    console.log(`   refQosData = ${pccData.refQosData} ${pccData.refQosData === opts.qos ? '✅' : '❌'}`);
    console.log(`   refTcData  = ${pccData.refTcData} ${pccData.refTcData === opts.tc ? '✅' : '❌'}`);
  }

  console.log('\n✅ 完成');
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });
