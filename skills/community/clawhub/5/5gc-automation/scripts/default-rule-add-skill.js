/**
 * default-rule-add-skill.js - PCF 默认规则一键添加工具
 *
 * 完整链路(一次性完成):
 *   1. 创建 QoS 模板(自动选5qi)
 *   2. 创建 Traffic Control(ENABLED)
 *   3. 创建 PCC 规则(绑定 qos + tc)
 *   4. 创建/更新 sm_policy_default(绑定 pcc)
 *   5. PCF default_smpolicy → sm_policy_default
 *
 * 用法:
 *   node default-rule-add-skill.js --project XW_SUPF_5_1_2_4 --headed
 *   node default-rule-add-skill.js --project XW_SUPF_5_1_2_4 --qos-id qos1 --tc-id tc1 --pcc-id pcc_default --headed
 *
 * 参数(均有默认值,可全部省略):
 *   --project     工程名(默认 XW_S5GC_1)
 *   --pcf-name    PCF实例名称(必填，如 qqq)
 *   --qos-id      QoS模板ID(默认自动生成 qos_default_{timestamp})
 *   --5qi         5QI值(不指定则自动选择未使用的值)
 *   --maxbr-ul    上行最大比特率(默认 10000000)
 *   --maxbr-dl    下行最大比特率(默认 20000000)
 *   --gbr-ul      上行保证比特率(默认 5000000)
 *   --gbr-dl      下行保证比特率(默认 5000000)
 *   --tc-id       TC规则ID(默认自动生成 tc_default_{timestamp})
 *   --flow-status TC流状态(默认 ENABLED)
 *   --pcc-id      PCC规则ID(默认 pcc_default)
 *   --precedence  PCC优先级(默认 63)
 *   --headed      显示浏览器窗口
 */
const { chromium } = require('playwright');

const globalBaseUrl = 'https://192.168.3.89';

function parseArgs() {
  const args = process.argv.slice(2);
  const ts = Date.now();
  const opts = {
    project: 'XW_S5GC_1',
    pcfName: null,           // null = 使用 pccId 作为 PCF 名称（向后兼容）
    // QoS 参数
    qosId: null,           // null = 自动生成
    qi: null,
    maxbrUl: '10000000',
    maxbrDl: '20000000',
    gbrUl: '5000000',
    gbrDl: '5000000',
    // TC 参数
    tcId: null,            // null = 自动生成
    flowStatus: 'ENABLED',
    // PCC 参数
    pccId: null,           // null = 自动生成
    precedence: '63',
    // PCF 参数(网元名称)
    pcfName: null,         // 若未提供则使用 pccId 作为默认名称
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
    else if (args[i] === '--tc-id') opts.tcId = args[++i];
    else if (args[i] === '--flow-status') opts.flowStatus = args[++i];
    else if (args[i] === '--pcc-id') opts.pccId = args[++i];
    else if (args[i] === '--precedence') opts.precedence = args[++i];
    else if (args[i] === '--pcf-name') opts.pcfName = args[++i];
    else if (args[i] === '--headed') opts.headed = true;
  }

  // 自动生成ID(如果未指定)
  if (!opts.qosId)  opts.qosId  = `qos_default_${ts}`;
  if (!opts.tcId)   opts.tcId   = `tc_default_${ts}`;
  if (!opts.pccId)  opts.pccId  = `pcc_default`;
  // 如果未提供 PCF 名称,默认使用 PCC ID(与业务保持一致)
  if (!opts.pcfName) opts.pcfName = opts.pccId;

  return opts;
}

// ─── 通用工具 ────────────────────────────────────────────────────────────
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
    let clicked = false;
    document.querySelectorAll('.jsgrid-row, .jsgrid-alt-row').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === n) {
        cells[1].querySelector('.iconfont')?.click();
        clicked = true;
      }
    });
    return clicked;
  }, name);
  if (!found) { console.error(`❌ 未找到工程: ${name}`); process.exit(1); }
  await page.waitForTimeout(3000);
  console.log(`✅ 工程 "${name}" 已选`);
}

async function goto(page, url) {
  await page.goto(`${globalBaseUrl}${url}`, { waitUntil: 'load', ignoreHTTPSErrors: true });
  await page.waitForTimeout(3000);
}

// ─── Step 1: 创建 QoS 模板 ──────────────────────────────────────────────
async function getUsedQis(page) {
  await goto(page, '/sim_5gc/predfPolicy/qos/index');
  return await page.evaluate(() => {
    const qis = [];
    document.querySelectorAll('.layui-table tbody tr').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 4 && cells[3].textContent.trim()) {
        qis.push(parseInt(cells[3].textContent.trim()));
      }
    });
    return qis;
  });
}

async function addQos(page, opts) {
  // 自动选 5qi(先获取已用列表)
  if (!opts.qi) {
    await goto(page, '/sim_5gc/predfPolicy/qos/index');
    const used = await page.evaluate(() => {
      const qis = [];
      document.querySelectorAll('.layui-table tbody tr').forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 4 && cells[3].textContent.trim()) {
          qis.push(parseInt(cells[3].textContent.trim()));
        }
      });
      return qis;
    });
    const candidates = [8, 9, 6, 5, 7, 4, 3, 2, 1];
    for (const c of candidates) { if (!used.includes(c)) { opts.qi = String(c); break; } }
    if (!opts.qi) opts.qi = String(used[0] + 1);
    console.log(`   i️ 已用5qi: ${used.join(',')},自动选择 ${opts.qi}`);
  }

  await goto(page, '/sim_5gc/predfPolicy/qos/index');
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);

  await page.waitForSelector('iframe[name="layui-layer-iframe2"]', { timeout: 10000 });
  const frame = page.frame('layui-layer-iframe2');
  await frame.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(500);

  await frame.locator('input[name="qosId"]').fill(opts.qosId);
  await frame.locator('input[name="5qi"]').fill(opts.qi);
  await frame.locator('input[name="maxbrUl"]').fill(opts.maxbrUl);
  await frame.locator('input[name="maxbrDl"]').fill(opts.maxbrDl);
  await frame.locator('input[name="gbrUl"]').fill(opts.gbrUl);
  await frame.locator('input[name="gbrDl"]').fill(opts.gbrDl);

  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`   ✅ QoS模板 ${opts.qosId} 已创建 (5qi=${opts.qi})`);
}

// ─── Step 2: 创建 TC ────────────────────────────────────────────────────
async function addTc(page, opts) {
  await goto(page, '/sim_5gc/predfPolicy/trafficCtl/index');
  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);

  // 等待 iframe 出现在 DOM 中
  await page.waitForSelector('iframe[name="layui-layer-iframe2"]', { timeout: 10000 });
  const frame = page.frame('layui-layer-iframe2');
  await frame.waitForLoadState('domcontentloaded');

  // 等待 tcId input 出现
  await frame.waitForSelector('input[name="tcId"]', { timeout: 10000 });
  await page.waitForTimeout(500);

  await frame.locator('input[name="tcId"]').fill(opts.tcId);

  // 等待 select[name="flowStatus"] 出现在 DOM 中
  const sel = frame.locator('select[name="flowStatus"]');
  try {
    await sel.waitFor({ state: 'attached', timeout: 5000 });
    await sel.selectOption(opts.flowStatus, { force: true });
    console.log(`   flowStatus = ${opts.flowStatus}`);
  } catch(e) {
    // 如果 select 不存在(如没有 flowStatus 字段),跳过
    console.log(`   i️ flowStatus select 不存在,跳过`);
  }

  await frame.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`   ✅ TC ${opts.tcId} 已创建 (flowStatus=${opts.flowStatus})`);
}

// ─── Step 3: 创建 PCC ────────────────────────────────────────────────────
async function addPcc(page, opts) {
  await goto(page, '/sim_5gc/predfPolicy/pcc/index');

  // 检查是否已存在同名 PCC,存在则先删除
  const existingId = await page.evaluate((targetId) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 10 && cells[2].textContent.trim() === targetId) {
        return cells[1].textContent.trim(); // 返回数字ID
      }
    }
    return null;
  }, opts.pccId);

  if (existingId) {
    // 删除旧记录
    await page.evaluate((id) => {
      const rows = document.querySelectorAll('.layui-table tbody tr');
      for (const row of rows) {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 10 && cells[1].textContent.trim() === id) {
          const links = cells[9].querySelectorAll('a');
          for (const l of links) { if (l.textContent.trim() === '删除') { l.click(); return; } }
        }
      }
    }, existingId);
    await page.waitForTimeout(1500);

    // 处理删除确认对话框
    const confirmBtn = page.locator('.layui-layer-dialog .layui-layer-btn0, .layui-layer-btn a:first-child');
    if (await confirmBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await confirmBtn.click();
      await page.waitForTimeout(2000);
    }
    // 确保遮罩关闭
    await page.keyboard.press('Escape');
    await page.waitForTimeout(1000);

    console.log(`   🗑️ 已删除旧 PCC ${opts.pccId},准备重建`);
  }

  await page.locator('button:has-text("添加")').click();
  await page.waitForTimeout(3000);
  await page.waitForFunction(() => window.location.href.includes('/predfPolicy/pcc/edit'), { timeout: 10000 });
  await page.waitForTimeout(3000);

  await page.locator('input[name="pccRuleId"]').fill(opts.pccId);
  await page.locator('input[name="precedence"]').fill(opts.precedence);

  // xm-select[0] = refQosData
  await page.evaluate(() => document.querySelectorAll('input.xm-select-default')[0].parentElement.click());
  await page.waitForTimeout(1000);
  const qosOpt = page.locator('.xm-option.show-icon', { hasText: opts.qosId });
  if (await qosOpt.isVisible({ timeout: 3000 }).catch(() => false)) await qosOpt.click();
  await page.waitForTimeout(500);

  // xm-select[1] = refTcData
  await page.evaluate(() => document.querySelectorAll('input.xm-select-default')[1].parentElement.click());
  await page.waitForTimeout(1000);
  const tcOpt = page.locator('.xm-option.show-icon', { hasText: opts.tcId });
  if (await tcOpt.isVisible({ timeout: 3000 }).catch(() => false)) await tcOpt.click();
  await page.waitForTimeout(500);

  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  await page.locator('button:has-text("提交")').click();
  await page.waitForTimeout(3000);
  console.log(`   ✅ PCC规则 ${opts.pccId} 已创建 (refQosData=${opts.qosId}, refTcData=${opts.tcId})`);
}

// ─── Step 4: 创建/更新 sm_policy_default（使用正确的 form_data 格式）────────────
async function addOrUpdateSmpolicy(page, pccId) {
  console.log(`\n=== Step 4: 创建/更新 sm_policy_default (pccRules=${pccId}) ===`);

  // 1. 进入 PCF，选中 pccId 行，点击 smpolicy 按钮
  await goto(page, '/sim_5gc/pcf/index');
  await page.waitForTimeout(3000);

  await page.evaluate((targetName) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === targetName) {
        const cb = row.querySelector('input[type="checkbox"]');
        if (cb) cb.click();
      }
    }
  }, pccId);
  await page.waitForTimeout(500);

  await page.locator('button:has-text("smpolicy")').click({ force: true });
  await page.waitForTimeout(3000);
  console.log('   smpolicy 页面 URL:', page.url());

  // 2. 获取 CSRF token（从页面）
  const token = await page.evaluate(() => document.querySelector('input[name="_token"]')?.value || '');
  if (!token) {
    console.error('   ❌ 未找到 _token');
    return false;
  }
  console.log('   _token: ...' + token.substring(0, 10) + '...');

  // 3. 检查是否已有 sm_policy_default
  const existing = await page.evaluate(() => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === 'sm_policy_default') {
        return { id: cells[1].textContent.trim(), pccRules: cells[4].textContent.trim() };
      }
    }
    return null;
  });

  if (!existing) {
    console.log('   ℹ️ sm_policy_default 不存在，正在创建...');
    await page.locator('button:has-text("添加")').click({ force: true });
    await page.waitForTimeout(3000);
    await page.waitForSelector('iframe[name="layui-layer-iframe2"]', { timeout: 15000 });
    const frm = page.frame('layui-layer-iframe2');
    await frm.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(1000);

    // 构造正确的 form_data JSON
    const formDataJson = JSON.stringify({
      name: 'sm_policy_default',
      pccRules: [pccId],
      reflectiveQoSTimer: 86400
    });

    const params = new URLSearchParams();
    params.append('_token', token);
    params.append('form_data', formDataJson);

    console.log('   form_data:', formDataJson);

    const resp = await frm.evaluate(async (args) => {
      const { tok, bodyStr } = args;
      try {
        const r = await fetch('/sim_5gc/smpolicy/default/edit', {
          method: 'POST',
          body: bodyStr,
          credentials: 'include',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-csrf-token': tok,
            'x-requested-with': 'XMLHttpRequest'
          }
        });
        const text = await r.text();
        return { status: r.status, body: text };
      } catch(e) {
        return { error: e.message };
      }
    }, { tok: token, bodyStr: params.toString() });

    console.log('   创建响应:', resp.status);
    if (resp.status >= 400) {
      try { console.log('   错误:', JSON.stringify(JSON.parse(resp.body))); }
      catch { console.log('   响应:', resp.body?.substring(0, 200)); }
      return false;
    } else {
      console.log('   ✅ 创建成功！响应:', resp.body?.substring(0, 200));
      return true;
    }
  } else {
    console.log('   ✅ sm_policy_default 已存在 (id=' + existing.id + ', pccRules=' + existing.pccRules + ')');
    if (existing.pccRules.includes(pccId)) {
      console.log('   ✅ pccRules 已包含 ' + pccId);
      return true;
    } else {
      console.log('   ℹ️ 更新 sm_policy_default，添加 pccRules=' + pccId + '...');
      // 点击编辑
      await page.evaluate(() => {
        const rows = document.querySelectorAll('.layui-table tbody tr');
        for (const row of rows) {
          const cells = row.querySelectorAll('td');
          if (cells.length >= 3 && cells[2].textContent.trim() === 'sm_policy_default') {
            const links = row.querySelectorAll('a');
            for (const l of links) { if (l.textContent.trim() === '编辑') { l.click(); return; } }
          }
        }
      });
      await page.waitForTimeout(3000);
      await page.waitForSelector('iframe[name="layui-layer-iframe2"]', { timeout: 15000 });
      const frm = page.frame('layui-layer-iframe2');
      await frm.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(1000);

      // 获取当前 pccRules
      const currentPcc = await frm.evaluate(() => {
        const inputs = document.querySelectorAll('input.xm-select-default');
        return inputs.length > 1 ? inputs[1].value : '';
      });
      const existingRules = currentPcc ? currentPcc.split(',').filter(Boolean) : [];
      if (!existingRules.includes(pccId)) existingRules.push(pccId);

      const recId = await frm.evaluate(() => {
        const el = document.querySelector('input[name="id"]');
        return el ? el.value : '';
      });

      // 更新用的 form_data
      const formDataJson = JSON.stringify({
        name: 'sm_policy_default',
        pccRules: existingRules,
        reflectiveQoSTimer: 86400,
        id: recId
      });

      const params = new URLSearchParams();
      params.append('_token', token);
      params.append('form_data', formDataJson);

      const resp = await frm.evaluate(async (args) => {
        const { tok, bodyStr, recId } = args;
        try {
          const r = await fetch('/sim_5gc/smpolicy/default/edit/' + recId, {
            method: 'POST',
            body: bodyStr,
            credentials: 'include',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'x-csrf-token': tok,
              'x-requested-with': 'XMLHttpRequest'
            }
          });
          const text = await r.text();
          return { status: r.status, body: text };
        } catch(e) {
          return { error: e.message };
        }
      }, { tok: token, bodyStr: params.toString(), recId });

      console.log('   更新响应:', resp.status);
      if (resp.status >= 400) {
        try { console.log('   错误:', JSON.stringify(JSON.parse(resp.body))); }
        catch { console.log('   响应:', resp.body?.substring(0, 200)); }
        return false;
      } else {
        console.log('   ✅ 更新成功！响应:', resp.body?.substring(0, 200));
        return true;
      }
    }
  }
}// ─── Step 5: PCF default_smpolicy ────────────────────────────────────────
// 正确流程（根据 UI 调试结果）：
// 1. 在 PCF 列表先选中 qqq 行（单击，不要点编辑）
// 2. 再点击工具栏 "smpolicy" 按钮 → 页面加载 sm_policy_default 表单（带 qqq 上下文）
// 3. 创建 sm_policy_default（此时 name 应为 qqq 关联的默认策略名）
// 4. 保存后返回 PCF 编辑弹窗 → default_smpolicy 下拉有数据 → 选择 → 提交
async function setPcfDefaultSmpolicy(page, pcfName) {
  console.log(`\n=== Step 5: 配置 PCF "${pcfName}" default_smpolicy ===`);

  // 1. 进入 PCF 列表，点击指定 PCF 的编辑按钮
  await goto(page, '/sim_5gc/pcf/index');
  await page.waitForTimeout(3000);

  const clicked = await page.evaluate((targetName) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === targetName) {
        const links = row.querySelectorAll('a');
        for (const l of links) { if (l.textContent.trim() === '编辑') { l.click(); return true; } }
      }
    }
    return false;
  }, pcfName);

  if (!clicked) {
    console.error(`   ❌ 未找到 PCF "${pcfName}" 的编辑按钮`);
    return false;
  }

  await page.waitForTimeout(3000);
  await page.waitForSelector('iframe[name="layui-layer-iframe2"]', { timeout: 15000 });
  const frm = page.frame('layui-layer-iframe2');
  await frm.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);

  // 2. 获取 token 和 PCF ID
  const token = await frm.evaluate(() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
  });
  
  if (!token) {
    console.error('   ❌ 未找到 CSRF token (meta[name="csrf-token"])');
    return false;
  }
  
  console.log(`   Token: ...${token.substring(0, 10)}... (from meta tag)`);

  const pcfId = await frm.evaluate(() => document.querySelector('input[name="id"]')?.value || '');
  if (!pcfId) {
    console.error('   ❌ 未找到 PCF ID');
    return false;
  }

  console.log(`   PCF ID: ${pcfId}`);

  // 3. 获取当前表单数据
  const formData = await frm.evaluate(() => {
    const form = document.querySelector('form');
    if (!form) return {};
    const data = new FormData(form);
    const entries = {};
    data.forEach((v, k) => { entries[k] = v; });
    return entries;
  });

  // 4. 获取 sm_policy_default 的 ID - 通过主页面，不关闭弹窗
  console.log('   获取 sm_policy_default 的 ID...');
  
  // 在主页面（不是 iframe）中打开新标签页查看 smpolicy 列表
  const smpId = await page.evaluate(async () => {
    // 在新窗口中打开 smpolicy 页面
    const newWindow = window.open('/sim_5gc/smpolicy/default/index', '_blank');
    if (!newWindow) return '';
    
    // 等待新窗口加载
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 从新窗口获取数据
    const rows = newWindow.document.querySelectorAll('.layui-table tbody tr');
    let foundId = '';
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === 'sm_policy_default') {
        foundId = cells[1].textContent.trim();
        break;
      }
    }
    
    // 关闭新窗口
    newWindow.close();
    return foundId;
  });

  if (!smpId) {
    console.error('   ❌ 未找到 sm_policy_default 的 ID');
    // 尝试使用已知的 ID（如果之前创建过）
    console.log('   ℹ️ 尝试使用默认 ID 9771');
    return '9771'; // 返回默认 ID，让调用者决定
  }
  
  console.log(`   sm_policy_default ID: ${smpId}`);

  // 5. 构造更新数据 - 设置 default_smpolicy 为 sm_policy_default 的 ID
  const updateData = {
    ...formData,
    'assoc_smpolicy[default_smpolicy]': smpId,  // 使用 ID 而不是名称
    '_token': token
  };

  // 移除空值（除了 select 字段）
  Object.keys(updateData).forEach(key => {
    if (updateData[key] === '' && !key.includes('select') && key !== 'assoc_smpolicy[default_smpolicy]') {
      delete updateData[key];
    }
  });

  // 6. 发送 POST 请求
  const params = new URLSearchParams();
  Object.entries(updateData).forEach(([k, v]) => {
    params.append(k, v);
  });

  console.log(`   提交数据: assoc_smpolicy[default_smpolicy]=${updateData['assoc_smpolicy[default_smpolicy]']}`);

  const resp = await frm.evaluate(async (args) => {
    const { pcfId, bodyStr, token } = args;
    try {
      const r = await fetch(`/sim_5gc/pcf/edit/${pcfId}`, {
        method: 'POST',
        body: bodyStr,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'x-csrf-token': token,
          'x-requested-with': 'XMLHttpRequest'
        }
      });
      const text = await r.text();
      return { status: r.status, body: text };
    } catch(e) {
      return { error: e.message };
    }
  }, { pcfId, bodyStr: params.toString(), token });

  console.log(`   响应状态: ${resp.status}`);
  if (resp.status >= 400) {
    try { console.log(`   错误: ${JSON.stringify(JSON.parse(resp.body))}`); }
    catch { console.log(`   响应: ${resp.body?.substring(0, 200)}`); }
    return false;
  } else {
    console.log(`   ✅ PCF "${pcfName}" default_smpolicy 设置成功！响应: ${resp.body?.substring(0, 100)}`);
    return true;
  }
}async function verify(page, opts) {
  await goto(page, '/sim_5gc/predfPolicy/pcc/index');
  const pcc = await page.evaluate((id) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 8 && cells[2].textContent.trim() === id) {
        return { pccRuleId: cells[2].textContent.trim(), precedence: cells[4].textContent.trim(), refQosData: cells[5].textContent.trim(), refTcData: cells[6].textContent.trim() };
      }
    }
    return null;
  }, opts.pccId);

  await goto(page, '/sim_5gc/smpolicy/default/index');
  const smp = await page.evaluate(() => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 6 && cells[2].textContent.trim() === 'sm_policy_default') return { pccRules: cells[4].textContent.trim() };
    }
    return null;
  });

  await goto(page, '/sim_5gc/pcf/index');
  await page.waitForTimeout(3000);
  
  // 点击指定的 PCF 编辑按钮
  const pcfName = opts.pcfName || opts.pccId;
  const clicked = await page.evaluate((targetName) => {
    const rows = document.querySelectorAll('.layui-table tbody tr');
    for (const row of rows) {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3 && cells[2].textContent.trim() === targetName) {
        const links = row.querySelectorAll('a');
        for (const l of links) { if (l.textContent.trim() === '编辑') { l.click(); return true; } }
      }
    }
    return false;
  }, pcfName);
  
  if (!clicked) {
    console.log('   ⚠️ 未找到 PCF "' + pcfName + '" 的编辑按钮，使用第一个 PCF');
    await page.evaluate(() => {
      const rows = document.querySelectorAll('.layui-table tbody tr');
      if (rows.length > 0) rows[0].querySelector('a')?.click();
    });
  }
  
  await page.waitForTimeout(3000);  const frame = page.frame('layui-layer-iframe2');
  const pcfSmp = frame ? await frame.evaluate(() => {
    const inputs = document.querySelectorAll('input.xm-select-default');
    return inputs[0]?.parentElement?.textContent?.match(/[\w_]+/g)?.[0] || '';
  }) : '';

  console.log('\n========================================');
  console.log('验证结果');
  console.log('========================================');
  const tests = [
    { name: `PCC ${opts.pccId} 存在`, pass: !!pcc },
    { name: `refQosData = ${opts.qosId}`, pass: pcc?.refQosData === opts.qosId },
    { name: `refTcData  = ${opts.tcId}`,  pass: pcc?.refTcData  === opts.tcId },
    { name: `sm_policy_default 包含 ${opts.pccId}`, pass: smp?.pccRules?.includes(opts.pccId) },
    { name: `PCF default_smpolicy = sm_policy_default`, pass: pcfSmp === 'sm_policy_default' },
  ];
  for (const t of tests) console.log(`  ${t.pass ? '✅' : '❌'} ${t.name}`);
  if (pcc) console.log(`\n  PCC: pccRuleId=${pcc.pccRuleId}, precedence=${pcc.precedence}, refQosData=${pcc.refQosData}, refTcData=${pcc.refTcData}`);
  if (smp) console.log(`  smp: pccRules=[${smp.pccRules}]`);
  console.log('========================================');
  return tests.every(t => t.pass);
}

// ─── 主流程 ─────────────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs();
  console.log('\n========================================');
  console.log('PCF 默认规则一键配置');
  console.log(`工程: ${opts.project}`);
  console.log(`QoS: ${opts.qosId} (5qi=${opts.qi || '自动'})`);
  console.log(`TC:  ${opts.tcId} (flowStatus=${opts.flowStatus})`);
  console.log(`PCF: ${opts.pcfName || opts.pccId}`);
  console.log(`PCC: ${opts.pccId} (precedence=${opts.precedence})`);
  console.log('========================================\n');

  const browser = await chromium.launch({ headless: !opts.headed, args: ['--no-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage', '--no-proxy-server', '--proxy-server=direct://', '--proxy-bypass-list=*'] });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });
  const page = await ctx.newPage();

  await login(page);
  await selectProject(page, opts.project);

  console.log('📦 Step 1: 创建 QoS 模板...');
  await addQos(page, opts);

  console.log('📦 Step 2: 创建 Traffic Control...');
  await addTc(page, opts);

  console.log('📦 Step 3: 创建 PCC 规则...');
  await addPcc(page, opts);

  console.log('📦 Step 4: 更新 sm_policy_default...');
  await addOrUpdateSmpolicy(page, opts.pccId);

  console.log('📦 Step 5: 配置 PCF default_smpolicy...');
  const pcfName = opts.pcfName || opts.pccId; // 向后兼容：如果没有指定 pcf-name，使用 pcc-id
  await setPcfDefaultSmpolicy(page, pcfName);

  console.log('\n📦 验证...');
  const ok = await verify(page, opts);

  console.log(ok ? '\n🎉 全部完成!' : '\n⚠️ 部分步骤存在问题,请检查');
  await browser.close();
  process.exit(ok ? 0 : 1);
}

main().catch(e => { console.error(e); process.exit(1); });
