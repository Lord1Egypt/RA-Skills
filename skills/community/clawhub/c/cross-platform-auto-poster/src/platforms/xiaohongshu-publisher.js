/**
 * 小红书自动发布实现
 * 使用 Playwright 浏览器自动化
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class XiaohongshuPublisher {
  constructor(options = {}) {
    this.headless = options.headless ?? false; // 开发阶段显示浏览器
    this.authDir = options.authDir || path.join(__dirname, '../../auth');
    this.browser = null;
    this.context = null;
    this.page = null;
  }

  /**
   * 初始化浏览器
   */
  async init(account) {
    this.browser = await chromium.launch({
      headless: this.headless,
      slowMo: 100 // 放慢操作方便看清楚
    });

    // 如果有保存的认证状态，加载它
    const storageState = account.cookiePath
      ? path.join(this.authDir, path.basename(account.cookiePath))
      : null;

    this.context = await this.browser.newContext({
      storageState: storageState && fs.existsSync(storageState) ? storageState : undefined,
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });

    this.page = await this.context.newPage();
    await this.context.addInitScript({
      content: `Object.defineProperty(navigator, 'webdriver', { get: () => undefined });`
    });

    return this;
  }

  /**
   * 登录（如果没登录的话）
   * 会打开登录页让用户扫码，完成后保存cookies
   */
  async loginAndSave(cookiePath) {
    await this.page.goto('https://creator.xiaohongshu.com/', {
      waitUntil: 'networkidle'
    });

    console.log('⌛ 等待登录，请在浏览器中扫码完成登录...');

    // 等待跳转到创作者中心，说明登录成功
    await this.page.waitForURL(/.*creator\.xiaohongshu\.com\/.*home/, {
      timeout: 300000 // 给5分钟扫码
    });

    // 保存认证状态
    const fullPath = path.join(this.authDir, cookiePath);
    await this.context.storageState({ path: fullPath });
    console.log(`✅ 登录成功，认证信息已保存到 ${cookiePath}`);

    return true;
  }

  /**
   * 发布图文笔记
   */
  async publishPost(options) {
    const { title, content, coverImage, images = [] } = options;

    console.log('📝 开始发布小红书笔记...');

    // 打开创作页面
    await this.page.goto('https://creator.xiaohongshu.com/publish/publish?type=image', {
      waitUntil: 'networkidle'
    });

    // 等待上传区域加载
    await this.page.waitForSelector('.upload-input', { timeout: 15000 });

    // 上传封面图和其他图片
    const allImages = [coverImage, ...images].filter(Boolean);
    const fileInput = await this.page.waitForSelector('input[type="file"]');
    await fileInput.setInputFiles(allImages);

    // 等待上传完成
    await this.page.waitForTimeout(3000 + allImages.length * 1000);

    // 填写标题
    const titleInput = await this.page.locator('div[placeholder="请输入标题"]');
    await titleInput.fill(title);

    // 填写正文
    const contentInput = await this.page.locator('div[placeholder="请输入正文内容"]');
    await contentInput.fill(content);

    // 这里需要等待话题系统加载，可以根据需要添加话题

    console.log(`✅ 内容填写完成: ${title}`);
    console.log('🔍 请检查内容是否正确，确认后点击发布...');

    // 在自动化模式下可以取消注释自动发布
    // const publishButton = await this.page.getByRole('button', { name: '发布' });
    // await publishButton.click();
    // await this.page.waitForURL(/.*publish\/success/, { timeout: 30000 });

    // 获取发布后的链接
    // const postUrl = this.page.url();
    // return { success: true, postUrl };

    return {
      success: true,
      message: '内容已填写，请手动检查后发布',
      title,
      content
    };
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

module.exports = XiaohongshuPublisher;
