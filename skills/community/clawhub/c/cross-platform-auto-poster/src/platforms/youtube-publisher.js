/**
 * YouTube 自动发布实现
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class YoutubePublisher {
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
      viewport: { width: 1920, height: 1080 }
    });

    this.page = await this.context.newPage();
    return this;
  }

  /**
   * 登录并保存认证
   */
  async loginAndSave(cookiePath) {
    await this.page.goto('https://studio.youtube.com/', {
      waitUntil: 'networkidle'
    });

    console.log('⌛ 等待登录，请在浏览器中完成Google登录...');
    await this.page.waitForURL(/.*studio\.youtube\.com/, {
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
    const { title, description, videoPath, tags = [], category = "22" } = options;
    // category 22 = People & Blogs

    console.log('📤 开始发布YouTube视频...');

    await this.page.goto('https://studio.youtube.com/channel/-/video-upload', {
      waitUntil: 'networkidle'
    });

    // 等待文件输入
    await this.page.waitForSelector('input[type="file"]', { timeout: 15000 });
    const fileInput = await this.page.locator('input[type="file"]');
    await fileInput.setInputFiles(videoPath);

    // 等待上传
    await this.page.waitForTimeout(5000);

    // 填写标题
    await this.page.waitForSelector('[aria-label="Title"]', { timeout: 30000 });
    const titleInput = await this.page.locator('[aria-label="Title"]');
    await titleInput.fill(title);

    // 填写描述
    const descInput = await this.page.locator('[aria-label="Description"]');
    await descInput.fill(description);

    // 添加标签
    if (tags.length > 0) {
      await this.page.getByText('Show more').click();
      await this.page.waitForTimeout(1000);
      const tagsInput = await this.page.locator('[aria-label="Tags"]');
      await tagsInput.fill(tags.join(', '));
    }

    console.log(`✅ 内容填写完成: ${title}`);
    console.log('🔍 请检查设置后点击发布...');

    return {
      success: true,
      message: '内容已填写，请检查设置后点击发布'
    };
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

module.exports = YoutubePublisher;
