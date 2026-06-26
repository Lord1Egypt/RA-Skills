/**
 * TikTok 自动发布实现
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class TiktokPublisher {
  constructor(options = {}) {
    this.headless = options.headless ?? false;
    this.authDir = options.authDir || path.join(__dirname, '../../auth');
    this.browser = null;
    this.context = null;
    this.page = null;
  }

  async init(account) {
    this.browser = await chromium.launch({
      headless: this.headless,
      slowMo: 100
    });

    const storageState = account.cookiePath
      ? path.join(this.authDir, path.basename(account.cookiePath))
      : null;

    this.context = await this.browser.newContext({
      storageState: storageState && fs.existsSync(storageState) ? storageState : undefined,
      viewport: { width: 1920, height: 1080 },
      geolocation: { latitude: 37.7749, longitude: -122.4194 }, // US location example
      permissions: ['geolocation']
    });

    this.page = await this.context.newPage();
    return this;
  }

  /**
   * 登录并保存认证
   */
  async loginAndSave(cookiePath) {
    await this.page.goto('https://www.tiktok.com/', {
      waitUntil: 'networkidle'
    });

    console.log('⌛ 等待登录，请在浏览器中完成登录...');
    await this.page.waitForURL(/.*tiktok\.com\/.*@.*/, {
      timeout: 300000
    });

    const fullPath = path.join(this.authDir, cookiePath);
    await this.context.storageState({ path: fullPath });
    console.log(`✅ 登录成功，认证已保存到 ${cookiePath}`);

    return true;
  }

  /**
   * 发布视频
   */
  async publishVideo(options) {
    const { title, description, videoPath, tags = [] } = options;

    console.log('📤 开始发布TikTok视频...');

    await this.page.goto('https://www.tiktok.com/upload?lang=en', {
      waitUntil: 'networkidle'
    });

    // 等待上传区域
    await this.page.waitForSelector('input[type="file"]', { timeout: 15000 });
    const fileInput = await this.page.locator('input[type="file"]');
    await fileInput.setInputFiles(videoPath);

    // 等待上传处理
    await this.page.waitForTimeout(5000);

    // 填写标题
    const titleInput = await this.page.locator('div[placeholder="Add a caption"]');
    if (await titleInput.isVisible()) {
      await titleInput.fill(title);
    }

    // 填写描述
    // TikTok 标题和描述在同一个输入框

    // 添加话题标签
    for (const tag of tags) {
      await this.page.keyboard.type(` #${tag}`);
      await this.page.waitForTimeout(500);
    }

    console.log(`✅ 内容填写完成: ${title}`);
    console.log('🔍 请检查后点击发布...');

    return {
      success: true,
      message: '内容已填写，请检查后发布'
    };
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

module.exports = TiktokPublisher;
