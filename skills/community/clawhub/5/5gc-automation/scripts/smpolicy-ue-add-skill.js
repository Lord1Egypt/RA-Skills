/**
 * smpolicy-ue-add-skill.js - UE Smpolicy 添加工具
 *
 * 用法：
 *   node smpolicy-ue-add-skill.js --project XW_SUPF_5_1_2_4 --name ue_test --dnn internet
 *   node smpolicy-ue-add-skill.js --project XW_SUPF_5_1_2_4 --name ue_test --dnn internet --imsi 460001234567890
 *   node smpolicy-ue-add-skill.js --project XW_SUPF_5_1_2_4 --name ue_test --dnn internet --sst 1 --sd 111111 --pcc-rules pcc2
 *
 * 参数：
 *   --project       工程名（默认 XW_S5GC_1）
 *   --name          UE策略名称（必填）
 *   --dnn           DNN（必填）
 *   --imsi          IMSI起始值（可选，不填则自动生成）
 *   --imsi-num      IMSI数量（默认 1）
 *   --sst           sNssai SST（默认 1）
 *   --sd            sNssai SD（默认 111111）
 *   --sess-rules    会话规则名称（xm-select，多个逗号分隔）
 *   --pcc-rules    PCC规则名称（xm-select，多个逗号分隔）
 *   --pra-rules     PRA规则名称（xm-select，可选）
 *   --ref-qos-timer reflectiveQoSTimer 值（可选）
 *   --headed        显示浏览器窗口
 *
 * 添加页：/sim_5gc/smpolicy/ue/edit（layui-layer-iframe2）
 * xm-select: sessRules=idx0, pccRules=idx1, praRules=idx2
 *
 * xm-select 交互：
 *   1. frame.evaluate(() => inputs[idx].parentElement.click()) 打开下拉
 *   2. frame.locator('.xm-option', {hasText}).click() 选择选项
 *   3. page.keyboard.press('Escape') 关闭下拉
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    project: 'XW_S5GC_1',
    name: null,
    dnn: null,
    imsi: null,
    imsiNum: '1',
    sst: '1',
    sd: '111111',
    sessRules: null,
    pccRules: null,
    praRules: null,
    refQosTimer: null,
    headed: false,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' || args[i] === '-p') opts.project = args[++i];
    else if (args[i] === '--name') opts.name = args[++i];
    else if (args[i] === '--dnn') opts.dnn = args[++i];
    else if (args[i] === '--imsi') opts.imsi = args[++i];
    else if (args[i] === '--imsi-num') opts.imsiNum = args[++i];
    else if (args[i] === '--sst') opts.sst = args[++i];
    else if (args[i] === '--sd') opts.sd = args[++i];
    else if (args[i] === '--sess-rules') opts.sessRules = args[++i];
    else if (args[i] === '--pcc-rules') opts.pccRules = args[++i];
    else if (args[i] === '--pra-rules') opts.praRules = args[++i];
    else if (args[i] === '--ref-qos-timer') opts.refQosTimer = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }
  if (!opts.name) { console.error('❌ 缺少 --name 参数'); process.exit(1); }
  if (!opts.dnn) { console.error('❌ 缺少 --dnn 参数'); process.exit(1); }
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

async function selectProject(page, name) {
  await page.goto(`${globalBaseUrl}/sim_5gc/project/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(2000);
  await page.locator('input[name="project_search_name"]').fill(name);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);
  const found = await page.evaluate((n) => {
    let result = false;
    document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === n) {
        cells[1].querySelector('.iconfont')?.click();
        result = true;
      }
    });
    return result;
  }, name);
  if (!found) { console.error(`❌ 未找到工程: ${name}`); process.exit(1); }
  await page.waitForTimeout(3000);
  console.log(`✅ 工程 "${name}" 已选`);
}

/**
 * 选择 xm-select 中的一个选项（支持多选，同一选项点击可切换选中状态）
 */
async function xmSelectChooseOne(frame, page, index, value) {
  if (!value) return;

  // 打开下拉
  await frame.evaluate((idx) => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    if (inputs[idx]) inputs[idx].parentElement.click();
  }, index);
  await page.waitForTimeout(1000);

  // 点击目标选项
  const clicked = await frame.evaluate((text) => {
    const opts = document.querySelectorAll('.xm-option');
    for (const opt of opts) {
      if (opt.textContent.trim() === text) {
        opt.click();
        return true;
      }
    }
    return false;
  }, value);

  if (clicked) {
    console.log(`   ✅ xm-select[${index}] = ${value}`);
  } else {
    console.log(`   ⚠️ xm-select[${index}] 未找到选项: ${value}`);
  }

  await page.waitForTimeout(500);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
}

/**
 * 选择 xm-select 中的多个选项（逗号分隔）
 */
async function xmSelectChooseMultiple(frame, page, index, values) {
  if (!values) return;
  const items = values.split(',').map(s => s.trim()).filter(Boolean);
  for (const item of items) {
    await xmSelectChooseOne(frame, page, index, item);
  }
}

async function main() {
  const opts = parseArgs();
  const browser = await chromium.launch({ headless: !opts.headed, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  await login(page);
  await selectProject(page, opts.project);

  // 导航到 UE smpolicy 列表页
  await page.goto(`${globalBaseUrl}/sim_5gc/smpolicy/ue/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
  console.log(`✅ 到达 UE Smpolicy 列表页`);

  // 点击添加按钮
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);

  // 获取编辑帧
  const frame = page.frame('layui-layer-iframe2');
  if (!frame) { console.error('❌ 未找到弹窗iframe'); process.exit(1); }
  await frame.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);
  console.log(`✅ 进入弹窗iframe: ${frame.url()}`);

  // ① 填写文本字段
  // 自动生成 IMSI（如果未提供）
  const autoImsi = opts.imsi || `4600${Date.now().toString().slice(-10)}`;
  const textFields = [
    { name: 'name', value: opts.name },
    { name: 'dnn', value: opts.dnn },
    { name: 'imsi', value: autoImsi },
    { name: 'imsi_num', value: opts.imsiNum },
    { name: 'sNssai[sst]', value: opts.sst },
    { name: 'sNssai[sd]', value: opts.sd },
  ];
  if (opts.refQosTimer) {
    textFields.push({ name: 'smPolicyDecision[reflectiveQoSTimer]', value: opts.refQosTimer });
  }

  for (const f of textFields) {
    const loc = frame.locator(`[name="${f.name}"]`).first();
    if (await loc.count() > 0) {
      await loc.fill(String(f.value));
      console.log(`   ✅ ${f.name} = "${f.value}"`);
    } else {
      console.log(`   ⚠️ 字段 ${f.name} 不存在`);
    }
  }

  // ② xm-select 选择（sessRules=idx0, pccRules=idx1, praRules=idx2）
  // sessRules 通常无数据（暂无数据），有则选
  const sessDisplay = await frame.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    return inputs[0]?.parentElement?.textContent || '';
  });
  if (!sessDisplay.includes('暂无数据')) {
    await xmSelectChooseMultiple(frame, page, 0, opts.sessRules);
  } else if (opts.sessRules) {
    console.log(`   ℹ️ sessRules 无可用数据，跳过`);
  }

  // pccRules
  await xmSelectChooseMultiple(frame, page, 1, opts.pccRules);

  // praRules 通常无数据
  const praDisplay = await frame.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    return inputs[2]?.parentElement?.textContent || '';
  });
  if (!praDisplay.includes('暂无数据')) {
    await xmSelectChooseMultiple(frame, page, 2, opts.praRules);
  } else if (opts.praRules) {
    console.log(`   ℹ️ praRules 无可用数据，跳过`);
  }

  // ③ 提交
  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`✅ 已提交`);

  // ④ 验证：回到列表页检查
  await page.goto(`${globalBaseUrl}/sim_5gc/smpolicy/ue/index`, { waitUntil: 'networkidle', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);

  const added = await page.evaluate((targetName) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 8 && cells[2].textContent.trim() === targetName) {
        return {
          name: cells[2].textContent.trim(),
          dnn: cells[3].textContent.trim(),
          sst: cells[4].textContent.trim(),
          sd: cells[5].textContent.trim(),
          sessRules: cells[6].textContent.trim(),
          pccRules: cells[7].textContent.trim(),
        };
      }
    }
    return null;
  }, opts.name);

  if (added) {
    console.log('\n📋 验证结果:');
    console.log(`   name      = ${added.name} ${added.name === opts.name ? '✅' : '❌'}`);
    console.log(`   dnn       = ${added.dnn} ${added.dnn === opts.dnn ? '✅' : '❌'}`);
    console.log(`   sst       = ${added.sst}`);
    console.log(`   sd        = ${added.sd}`);
    console.log(`   sessRules = ${added.sessRules}`);
    console.log(`   pccRules  = ${added.pccRules}`);
    if (opts.pccRules) {
      const expectedPccs = opts.pccRules.split(',').map(s => s.trim());
      const match = expectedPccs.every(p => added.pccRules.includes(p));
      console.log(`   pccRules 匹配: ${match ? '✅' : '⚠️'}`);
    }
  } else {
    console.log('\n❌ 未在列表中找到创建的 UE Smpolicy');
  }

  console.log('\n✅ 完成');
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });
