/**
 * 小红书笔记自动发布脚本
 * 
 * 用法: node xiaohongshu_publish.js <标题> <正文文件> [图片路径]
 * 
 * Cookie文件：~/.qclaw/xiaohongshu_cookies.json
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const COOKIE_FILE = path.join(process.env.HOME, '.qclaw', 'xiaohongshu_cookies.json');
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36';

async function createBrowser() {
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const context = await browser.newContext({
    userAgent: USER_AGENT,
    viewport: { width: 1280, height: 800 },
  });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
  });

  if (fs.existsSync(COOKIE_FILE)) {
    const cookies = JSON.parse(fs.readFileSync(COOKIE_FILE, 'utf8'));
    await context.addCookies(cookies);
  }

  return { browser, context };
}

async function saveCookies(context) {
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIE_FILE, JSON.stringify(cookies, null, 2));
}

/**
 * 发布小红书笔记
 */
async function publishNote(title, content, imagePath = null) {
  const { browser, context } = await createBrowser();
  const page = await context.newPage();

  try {
    console.log('📖 打开小红书创作者页面...');
    await page.goto('https://creator.xiaohongshu.com/publish/publish', { 
      waitUntil: 'networkidle', 
      timeout: 30000 
    });
    await page.waitForTimeout(3000);

    // 检查是否需要登录
    const loginBtn = await page.$('text=登录');
    if (loginBtn) {
      console.log('⚠️ 需要登录小红书');
      // 等待用户扫码登录
      console.log('请在浏览器中扫码登录...');
      await page.waitForTimeout(60000); // 给用户1分钟登录时间
    }

    // 上传图片（如果有）
    if (imagePath && fs.existsSync(imagePath)) {
      console.log('📷 上传图片...');
      const uploadInput = await page.$('input[type="file"]');
      if (uploadInput) {
        await uploadInput.setInputFiles(imagePath);
        await page.waitForTimeout(5000); // 等待上传完成
      }
    }

    // 填写标题
    const titleInput = await page.$('input[placeholder*="标题"]') ||
                       await page.$('.title-input') ||
                       await page.$('#title-input');
    if (titleInput) {
      await titleInput.fill(title);
      console.log(`✅ 标题已填写: ${title}`);
    }

    // 填写正文 - 小红书用的是TipTap编辑器
    let editor = await page.$('.ProseMirror') ||
                 await page.$('[contenteditable="true"]') ||
                 await page.$('.ql-editor');
    
    if (!editor) {
      throw new Error('未找到编辑器');
    }

    await editor.click();
    await page.waitForTimeout(500);
    
    // 写入内容
    await page.evaluate((text) => navigator.clipboard.writeText(text), content);
    await page.waitForTimeout(300);
    await page.keyboard.press('Meta+v');
    await page.waitForTimeout(3000);
    console.log('✅ 正文已写入');

    // 发布
    const publishBtn = await page.$('button:has-text("发布")') ||
                       await page.$('.publishBtn');
    if (publishBtn) {
      await publishBtn.click();
      await page.waitForTimeout(5000);
      console.log('✅ 发布成功！');
    } else {
      console.log('⚠️ 未找到发布按钮，请手动发布');
    }

    const resultUrl = page.url();
    await saveCookies(context);
    await browser.close();

    return { success: true, url: resultUrl };
  } catch (err) {
    await saveCookies(context);
    await browser.close();
    return { success: false, error: err.message };
  }
}

// CLI入口
(async () => {
  const title = process.argv[2];
  const contentFile = process.argv[3];
  const imagePath = process.argv[4];

  if (!title || !contentFile) {
    console.log('用法: node xiaohongshu_publish.js <标题> <正文文件> [图片路径]');
    process.exit(1);
  }

  const content = fs.readFileSync(contentFile, 'utf8').trim();
  const result = await publishNote(title, content, imagePath);
  console.log(JSON.stringify(result));
})();

module.exports = { publishNote };
