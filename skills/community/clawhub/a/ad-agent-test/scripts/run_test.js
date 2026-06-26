/**
 * 投放Agent完整测试脚本
 * 
 * 使用方法：
 *   ACCOUNT_ID=74295795 COOKIES_FILE=./cookies.json node scripts/run_test.js
 * 
 * 环境变量：
 *   ACCOUNT_ID  - 广告主账户ID（必需）
 *   COOKIES_FILE - cookies.json路径（默认 ./cookies.json）
 *   OUTPUT_DIR  - 截图输出目录（默认 ./output）
 *   WAIT_REPLY  - 等待Agent回复秒数（默认 25）
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ACCOUNT_ID = process.env.ACCOUNT_ID || '74295795';
const COOKIES_FILE = process.env.COOKIES_FILE || './cookies.json';
const OUTPUT_DIR = process.env.OUTPUT_DIR || './output';
const WAIT_REPLY = parseInt(process.env.WAIT_REPLY || '25') * 1000;
const BASE_URL = `https://ad.qq.com/atlas/${ACCOUNT_ID}/agent`;

async function setup() {
  if (!fs.existsSync(COOKIES_FILE)) {
    console.error(`❌ Cookie文件不存在: ${COOKIES_FILE}`);
    console.error('   请先运行 inject_cookies.js 生成');
    process.exit(1);
  }
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({ 
    headless: true, 
    args: ['--no-sandbox', '--disable-dev-shm-usage'] 
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  
  const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf8'));
  await context.addCookies(cookies);
  
  const page = await context.newPage();
  return { browser, context, page };
}

async function shot(page, name) {
  const filepath = path.join(OUTPUT_DIR, `${name}.png`);
  await page.screenshot({ path: filepath, fullPage: false });
  console.log(`  📸 ${name}.png`);
  return filepath;
}

async function extractText(page) {
  return page.evaluate(() => document.body.innerText);
}

async function goHome(page) {
  await page.goto(BASE_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(8000);
}

async function sendMessage(page, text) {
  const editor = page.locator('[contenteditable="true"]').first();
  await editor.click({ force: true });
  await page.waitForTimeout(300);
  await page.keyboard.type(text, { delay: 20 });
  await page.keyboard.press('Enter');
  await page.waitForTimeout(WAIT_REPLY);
}

// ==================== 测试模块 ====================

async function testHomepage(page) {
  console.log('\n=== 第一阶段：首页验证 ===');
  await goHome(page);
  
  const bodyText = await extractText(page);
  if (bodyText.includes('微信账号登录') || bodyText.includes('扫一扫')) {
    console.error('❌ Cookie已过期，跳转到登录页！');
    await shot(page, '00_login_page');
    return false;
  }
  
  console.log('✅ 成功进入Agent页面');
  await shot(page, '01_home');
  
  // 提取首页快捷指令
  const quickCmds = await page.evaluate(() => {
    const cards = document.querySelectorAll('[class*="guideCard"], [class*="quickCommand"]');
    return Array.from(cards).map(c => c.innerText.trim()).filter(Boolean);
  });
  console.log(`  首页快捷指令: ${quickCmds.join(' | ')}`);
  
  return true;
}

async function testQuickCommands(page) {
  console.log('\n=== 第二阶段：快捷指令模板 ===');
  
  const commands = ['模仿优质广告新建', '删除并重建广告微调', '删除并重建广告', '为广告新建创意'];
  
  for (let i = 0; i < commands.length; i++) {
    await goHome(page);
    const cmdText = commands[i];
    
    const clicked = await page.evaluate((text) => {
      const els = document.querySelectorAll('[class*="guideCard"] span, [class*="quickCommand"] span, [class*="cardTitle"]');
      for (const el of els) {
        if (el.innerText.includes(text.substring(0, 4))) { el.click(); return true; }
      }
      return false;
    }, cmdText);
    
    if (clicked) {
      await page.waitForTimeout(3000);
      await shot(page, `02_cmd_${i + 1}_${cmdText.substring(0, 4)}`);
      
      // 提取模板内容
      const template = await page.evaluate(() => {
        const editor = document.querySelector('[contenteditable="true"]');
        return editor ? editor.innerText : '(未找到)';
      });
      console.log(`  [${cmdText}] 模板: ${template.substring(0, 80)}...`);
    }
  }
}

async function testCommandPanel(page) {
  console.log('\n=== 常用指令面板 ===');
  await goHome(page);
  
  await page.locator('[title="常用指令"]').first().click();
  await page.waitForTimeout(2000);
  await shot(page, '03_command_panel');
  
  // 提取所有指令
  const commands = await page.evaluate(() => {
    const items = document.querySelectorAll('[class*="commandItem"], [class*="menuItem"]');
    return Array.from(items).map(el => ({
      text: el.innerText.trim(),
      category: el.closest('[class*="group"]')?.querySelector('[class*="groupTitle"]')?.innerText || ''
    }));
  });
  console.log(`  共 ${commands.length} 条指令`);
  commands.forEach(c => console.log(`    ${c.category ? `[${c.category}] ` : ''}${c.text}`));
}

async function testFreeDialog(page) {
  console.log('\n=== 第三阶段：自由对话 ===');
  
  const scenarios = [
    { label: '投放前-预算', text: '我有5000元预算，想推广一个教育类小程序，应该怎么设置投放计划？' },
    { label: '投放前-选品', text: '我是做电商的，卖女装，适合选择什么投放版位和定向人群？' },
    { label: '投放中-数据', text: '帮我查一下今天的广告消耗和转化数据' },
    { label: '投放中-优化', text: '我的广告点击率很低只有0.5%，有什么优化建议？' },
    { label: '投放中-调预算', text: '帮我把所有在投的广告日预算统一调整到200元' },
    { label: '投放后-复盘', text: '帮我分析一下上周的投放效果，哪些广告ROI最高？' },
    { label: '投放后-关停', text: '帮我把转化成本超过50元的广告全部暂停' },
  ];
  
  for (let i = 0; i < scenarios.length; i++) {
    const { label, text } = scenarios[i];
    await goHome(page);
    
    console.log(`  [${label}] 发送: ${text.substring(0, 30)}...`);
    await sendMessage(page, text);
    await shot(page, `04_dialog_${i + 1}_${label}`);
    
    // 提取Agent回复
    const reply = await page.evaluate(() => {
      const msgs = document.querySelectorAll('[class*="message"], [class*="bubble"], [class*="agentMsg"]');
      if (msgs.length === 0) return '(无回复)';
      return msgs[msgs.length - 1].innerText.substring(0, 200);
    });
    console.log(`    回复: ${reply.substring(0, 100)}...`);
  }
}

async function testMiaozahao(page) {
  console.log('\n=== 第四阶段：妙招测试 ===');
  await goHome(page);
  
  // 进入妙招
  await page.evaluate(() => {
    const items = document.querySelectorAll('[class*="menuItem"], [class*="navItem"]');
    for (const item of items) {
      if (item.innerText.trim() === '妙招') { item.click(); return; }
    }
  });
  await page.waitForTimeout(5000);
  await shot(page, '05_miaozahao_main');
  
  // 测试每个妙招
  const miaozahaoNames = ['新建多个创意', '批量清理低效创意', '批量关停无效广告'];
  for (let i = 0; i < miaozahaoNames.length; i++) {
    await page.evaluate((name) => {
      const spans = document.querySelectorAll('span, div, h3, h4');
      for (const s of spans) {
        if (s.innerText.trim() === name) { s.click(); return; }
      }
    }, miaozahaoNames[i]);
    await page.waitForTimeout(3000);
    await shot(page, `05_miaozahao_${i + 1}`);
    
    const panelText = await extractText(page);
    console.log(`  [${miaozahaoNames[i]}] 面板内容: ${panelText.substring(0, 150)}...`);
  }
  
  // 测试一键执行按钮状态
  const btnState = await page.evaluate(() => {
    const btns = document.querySelectorAll('button');
    for (const btn of btns) {
      if (btn.innerText.includes('一键执行')) {
        return { disabled: btn.disabled, title: btn.title || '' };
      }
    }
    return null;
  });
  if (btnState) {
    console.log(`  一键执行按钮: disabled=${btnState.disabled}, title="${btnState.title}"`);
  }
}

// ==================== 主流程 ====================

(async () => {
  const { browser, page } = await setup();
  
  try {
    const loginOk = await testHomepage(page);
    if (!loginOk) {
      console.error('\n❌ 测试终止：Cookie无效');
      process.exit(1);
    }
    
    await testQuickCommands(page);
    await testCommandPanel(page);
    await testFreeDialog(page);
    await testMiaozahao(page);
    
    console.log('\n=== ✅ 所有测试完成 ===');
    console.log(`截图保存在: ${OUTPUT_DIR}/`);
    
  } catch (err) {
    console.error('❌ 测试异常:', err.message);
    await shot(page, 'error_screenshot');
  } finally {
    await browser.close();
  }
})();
