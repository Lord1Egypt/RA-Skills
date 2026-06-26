/**
 * 知乎内容自动发布脚本
 * 
 * 支持两种模式：
 * 1. 回答问题：node zhihu_publish.js answer <问题URL> <回答内容文件>
 * 2. 发布文章：node zhihu_publish.js article <标题> <文章内容文件>
 * 
 * Cookie文件：~/.qclaw/zhihu_cookies.json
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const COOKIE_FILE = path.join(process.env.HOME, '.qclaw', 'zhihu_cookies.json');
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
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
  });

  // 加载Cookie
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
 * 发布知乎回答
 */
async function publishAnswer(questionUrl, content) {
  const { browser, context } = await createBrowser();
  const page = await context.newPage();

  try {
    console.log(`📖 访问题目: ${questionUrl}`);
    await page.goto(questionUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 找到问题区域的"写回答"按钮
    console.log('✍️ 点击写回答...');
    const btns = await page.$$('button');
    let targetBtn = null;
    let maxY = 0;
    for (const btn of btns) {
      const text = await btn.textContent();
      if (text?.trim().includes('写回答')) {
        const box = await btn.boundingBox();
        if (box && box.y > 100 && box.y > maxY) {
          maxY = box.y;
          targetBtn = btn;
        }
      }
    }

    if (!targetBtn) {
      throw new Error('未找到写回答按钮，请确认已登录知乎');
    }
    await targetBtn.click();
    console.log(`✅ 点击了写回答`);

    // 等待编辑器
    let editor = null;
    for (let i = 0; i < 15; i++) {
      editor = await page.$('.public-DraftEditor-content') ||
               await page.$('[contenteditable="true"]');
      if (editor) break;
      await page.waitForTimeout(1000);
    }

    if (!editor) {
      throw new Error('编辑器未出现');
    }
    console.log('✅ 编辑器就绪');

    // 写入内容
    await editor.click();
    await page.waitForTimeout(500);
    await page.evaluate((text) => navigator.clipboard.writeText(text), content);
    await page.waitForTimeout(300);
    await page.keyboard.press('Meta+v');
    await page.waitForTimeout(3000);

    // 验证写入
    const editorText = await editor.evaluate(el => el.innerText);
    console.log(`📝 已写入: ${editorText.length} 字符`);

    if (editorText.length < 10) {
      // 备用方法
      await editor.click();
      await page.evaluate((text) => {
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, text);
      }, content);
      await page.waitForTimeout(2000);
    }

    // 发布
    let publishBtn = null;
    for (let i = 0; i < 10; i++) {
      publishBtn = await page.$('button:has-text("发布回答")') ||
                   await page.$('button:has-text("发布")');
      if (publishBtn) break;
      await page.waitForTimeout(1000);
    }

    if (!publishBtn) {
      throw new Error('未找到发布按钮');
    }

    await publishBtn.click();
    await page.waitForTimeout(5000);

    const resultUrl = page.url();
    await saveCookies(context);
    await browser.close();

    return { success: true, url: resultUrl, type: 'answer' };
  } catch (err) {
    await saveCookies(context);
    await browser.close();
    return { success: false, error: err.message };
  }
}

/**
 * 发布知乎文章
 */
async function publishArticle(title, content) {
  const { browser, context } = await createBrowser();
  const page = await context.newPage();

  try {
    console.log(`📝 打开写作页面...`);
    await page.goto('https://zhuanlan.zhihu.com/write', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 填写标题
    const titleInput = await page.$('input[placeholder*="标题"]') ||
                       await page.$('.WriteIndex-titleInput input');
    if (titleInput) {
      await titleInput.fill(title);
      console.log(`✅ 标题已填写: ${title}`);
    }

    // 填写正文
    let editor = await page.$('.public-DraftEditor-content') ||
                 await page.$('[contenteditable="true"]');
    if (!editor) {
      throw new Error('文章编辑器未出现');
    }

    await editor.click();
    await page.waitForTimeout(500);
    await page.evaluate((text) => navigator.clipboard.writeText(text), content);
    await page.waitForTimeout(300);
    await page.keyboard.press('Meta+v');
    await page.waitForTimeout(3000);
    console.log('✅ 正文已写入');

    // 发布
    const publishBtn = await page.$('button:has-text("发布")');
    if (publishBtn) {
      await publishBtn.click();
      await page.waitForTimeout(5000);
    }

    const resultUrl = page.url();
    await saveCookies(context);
    await browser.close();

    return { success: true, url: resultUrl, type: 'article' };
  } catch (err) {
    await saveCookies(context);
    await browser.close();
    return { success: false, error: err.message };
  }
}

// CLI入口
(async () => {
  const mode = process.argv[2];
  
  if (mode === 'answer') {
    const questionUrl = process.argv[3];
    const contentFile = process.argv[4];
    if (!questionUrl || !contentFile) {
      console.log('用法: node zhihu_publish.js answer <问题URL> <回答内容文件>');
      process.exit(1);
    }
    const content = fs.readFileSync(contentFile, 'utf8').trim();
    const result = await publishAnswer(questionUrl, content);
    console.log(JSON.stringify(result));
  } else if (mode === 'article') {
    const title = process.argv[3];
    const contentFile = process.argv[4];
    if (!title || !contentFile) {
      console.log('用法: node zhihu_publish.js article <标题> <文章内容文件>');
      process.exit(1);
    }
    const content = fs.readFileSync(contentFile, 'utf8').trim();
    const result = await publishArticle(title, content);
    console.log(JSON.stringify(result));
  } else {
    console.log('用法: node zhihu_publish.js <answer|article> <参数...>');
    process.exit(1);
  }
})();

module.exports = { publishAnswer, publishArticle };
