/**
 * qos-add-skill.js - QoS模板添加工具
 *
 * 用法:
 *   node qos-add-skill.js --project XW_SUPF_5_1_2_4 --qos-id qos3 --maxbr-ul 10000000 --maxbr-dl 20000000 --gbr-ul 5000000 --gbr-dl 5000000 [--headed]
 *   node qos-add-skill.js --project XW_SUPF_5_1_2_4 --qos-id qos3 --5qi 8 --maxbr-ul 10000000 --maxbr-dl 20000000 --gbr-ul 5000000 --gbr-dl 5000000 [--headed]
 *
 * 参数:
 *   --project     工程名（默认 XW_S5GC_1）
 *   --qos-id      QoS模板ID（必填）
 *   --5qi         5QI值（不指定则自动从已有5qi列表中选择一个不同的值）
 *   --maxbr-ul    上行最大比特率（不指定则用默认值）
 *   --maxbr-dl    下行最大比特率（不指定则用默认值）
 *   --gbr-ul      上行保证比特率（不指定则用默认值）
 *   --gbr-dl      下行保证比特率（不指定则用默认值）
 *   --priority    优先级（默认空）
 *   --headed      显示浏览器窗口
 *
 * 默认值（用户未指定时）:
 *   maxbrUl=10000000, maxbrDl=20000000, gbrUl=5000000, gbrDl=5000000
 *   5qi=自动选择（从已有5qi列表中挑一个不存在的值，优先8/9/6/5...）
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    project: 'XW_S5GC_1',
    qosId: null,
    qi: null,
    maxbrUl: null,
    maxbrDl: null,
    gbrUl: null,
    gbrDl: null,
    priority: '',
    headed: false,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' || args[i] === '-p') opts.project = args[++i];
    else if (args[i] === '--qos-id') opts.qosId = args[++i];
    else if (args[i] === '--5qi') opts.qi = args[++i];
    else if (args[i] === '--maxbr-ul') opts.maxbrUl = args[++i];
    else if (args[i] === '--maxbr-dl') opts.maxbrDl = args[++i];
    else if (args[i] === '--gbr-ul') opts.gbrUl = args[++i];
    else if (args[i] === '--gbr-dl') opts.gbrDl = args[++i];
    else if (args[i] === '--priority') opts.priority = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }
  if (!opts.qosId) {
    console.error('❌ 缺少必要参数: --qos-id');
    console.error('   示例: node qos-add-skill.js --project XW_SUPF_5_1_2_4 --qos-id qos3 --maxbr-ul 10000000 --maxbr-dl 20000000 --gbr-ul 5000000 --gbr-dl 5000000');
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
  if (!clicked) { console.log('❌ 未找到工程'); process.exit(1); }
  await page.waitForTimeout(3000);
  console.log(`✅ 工程 "${projectName}" 已选`);
}

async function getUsed5qis(page) {
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/qos/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  const usedQis = await page.evaluate(() => {
    const qis = new Set();
    document.querySelectorAll('.layui-table tbody tr').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 4) {
        const qi = parseInt(cells[3].textContent.trim());
        if (!isNaN(qi)) qis.add(qi);
      }
    });
    return [...qis];
  });
  return usedQis;
}

function autoSelect5qi(usedQis) {
  const candidates = [8, 9, 6, 5, 4, 3, 2, 1];
  for (const c of candidates) {
    if (!usedQis.includes(c)) return c;
  }
  return 8;
}

const DEFAULT_BR = { maxbrUl: '10000000', maxbrDl: '20000000', gbrUl: '5000000', gbrDl: '5000000' };

async function main() {
  const opts = parseArgs();
  const browser = await chromium.launch({ headless: !opts.headed, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  await login(page);
  await selectProject(page, opts.project);

  // 自动确定5qi（用户未指定时）
  if (opts.qi === null) {
    console.log('\n📋 检测已有QoS模板的5qi...');
    const usedQis = await getUsed5qis(page);
    console.log(`   已使用5qi: ${usedQis.join(', ')}`);
    opts.qi = autoSelect5qi(usedQis);
    console.log(`   ✅ 自动选择 5qi = ${opts.qi}（与已有不同）`);
  } else {
    console.log(`\n📋 用户指定 5qi = ${opts.qi}`);
  }

  // 应用默认值
  const params = {
    qosId: opts.qosId,
    qi: opts.qi,
    maxbrUl: opts.maxbrUl || DEFAULT_BR.maxbrUl,
    maxbrDl: opts.maxbrDl || DEFAULT_BR.maxbrDl,
    gbrUl: opts.gbrUl || DEFAULT_BR.gbrUl,
    gbrDl: opts.gbrDl || DEFAULT_BR.gbrDl,
  };

  console.log('\n📋 最终参数:');
  console.log(`   qosId   = ${params.qosId}`);
  console.log(`   5qi     = ${params.qi}`);
  console.log(`   maxbrUl = ${params.maxbrUl}`);
  console.log(`   maxbrDl = ${params.maxbrDl}`);
  console.log(`   gbrUl   = ${params.gbrUl}`);
  console.log(`   gbrDl   = ${params.gbrDl}`);

  // 去添加页
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/qos/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);

  const frame = page.frame('layui-layer-iframe2');
  if (!frame) { console.error('❌ 未找到弹窗iframe'); process.exit(1); }
  await page.waitForTimeout(1000);

  // 填写字段（使用 first() 确保能获取到元素）
  await frame.locator('input[name="qosId"]').first().fill(params.qosId);
  await frame.locator('input[name="5qi"]').first().fill(params.qi);
  await frame.locator('input[name="maxbrUl"]').first().fill(params.maxbrUl);
  await frame.locator('input[name="maxbrDl"]').first().fill(params.maxbrDl);
  await frame.locator('input[name="gbrUl"]').first().fill(params.gbrUl);
  await frame.locator('input[name="gbrDl"]').first().fill(params.gbrDl);

  // 提交
  await frame.locator('button:has-text("提交")').first().click();
  await page.waitForTimeout(3000);

  // 验证
  await page.goto(`${globalBaseUrl}/sim_5gc/predfPolicy/qos/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);

  const qosData = await page.evaluate((targetId) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      for (let i = 0; i < cells.length; i++) {
        if (cells[i].textContent.trim() === targetId) {
          return {
            id: cells[1].textContent.trim(),
            qi: cells[3].textContent.trim(),
            maxbrUl: cells[4].textContent.trim(),
            maxbrDl: cells[5].textContent.trim(),
            gbrUl: cells[6].textContent.trim(),
            gbrDl: cells[7].textContent.trim(),
          };
        }
      }
    }
    return null;
  }, params.qosId);

  if (qosData) {
    console.log('\n📋 保存的QoS数据:');
    console.log(`   ID=${qosData.id}, 5qi=${qosData.qi}, maxbrUl=${qosData.maxbrUl}, maxbrDl=${qosData.maxbrDl}, gbrUl=${qosData.gbrUl}, gbrDl=${qosData.gbrDl}`);
    const ok = qosData.qi === params.qi && qosData.maxbrUl === params.maxbrUl && qosData.maxbrDl === params.maxbrDl && qosData.gbrUl === params.gbrUl && qosData.gbrDl === params.gbrDl;
    console.log(ok ? '\n✅ QoS模板创建成功！' : '\n⚠️ 部分数据可能未正确保存');
  }

  console.log('\n✅ 完成');
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });
