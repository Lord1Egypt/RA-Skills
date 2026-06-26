/**
 * 抖音私信发送脚本（Playwright 版）
 * 用法: node send_douyin_dm.mjs <用户名> <消息内容>
 *
 * 示例: node send_douyin_dm.mjs 小楠子爱跳舞 "续火花🔥"
 */

import { chromium } from 'playwright';

const TARGET_URL = 'https://www.douyin.com/user/self';

async function main() {
  const args = process.argv.slice(2);
  const username = args[0] || '';
  const message = args[1] || '你好，这是一条测试消息';

  console.log(`开始发送私信...`);
  console.log(`目标用户: ${username}`);
  console.log(`消息内容: ${message}`);

  const browser = await chromium.launch({
    headless: false,
    userDataDir: '/Users/calvin/.openclaw/browser/openclaw/user-data'
  });

  const page = await browser.newPage();
  await page.goto(TARGET_URL);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  console.log('页面已加载');

  // === Step 1: 点击"私信"按钮 ===
  // 找到段落文本为"私信"的元素并点击
  const 私信Btn = page.locator('paragraph:text("私信")').first();
  await 私信Btn.click();
  console.log('已点击私信按钮');
  await page.waitForTimeout(1000);

  // === Step 2: 点击目标用户名 ===
  // 在下拉列表中查找目标用户
  const userItem = page.locator(`text=${username}`).first();
  const userVisible = await userItem.isVisible().catch(() => false);

  if (!userVisible) {
    console.error(`找不到用户: ${username}`);
    await page.screenshot({ path: 'debug_no_user.png' });
    await browser.close();
    process.exit(1);
  }

  await userItem.click();
  console.log(`已点击用户: ${username}，进入聊天窗口`);
  await page.waitForTimeout(1500);

  // === Step 3: 输入消息 ===
  // 等待聊天输入框出现
  await page.waitForTimeout(500);

  // 尝试多种输入框选择器
  const inputSelectors = [
    'div[contenteditable="true"]',
    'textarea',
    'input[type="text"]',
    'div[class*="editArea"]',
    'div[class*="input"][contenteditable]'
  ];

  let inputBox = null;
  for (const sel of inputSelectors) {
    const el = page.locator(sel).first();
    const count = await el.count();
    if (count > 0) {
      const visible = await el.first().isVisible().catch(() => false);
      if (visible) {
        inputBox = el.first();
        console.log(`找到输入框: ${sel}`);
        break;
      }
    }
  }

  if (!inputBox) {
    console.error('找不到聊天输入框');
    await page.screenshot({ path: 'debug_no_input.png' });
    await browser.close();
    process.exit(1);
  }

  await inputBox.click();
  await page.waitForTimeout(300);
  await inputBox.fill(message);
  await page.waitForTimeout(200);

  // 按 Enter 发送
  await inputBox.press('Enter');
  console.log(`消息已发送: ${message}`);

  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'debug_sent.png' });

  await page.close();
  console.log('页面已关闭');

  await browser.close();
  console.log('完成！');
}

main().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
