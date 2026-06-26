import { BaseAdapter } from '../lib/base-adapter.js';
import { ArticleContent, PublishResult } from '../types/index.js';

/**
 * 小红书平台适配器
 */
export class XiaohongshuAdapter extends BaseAdapter {
  constructor() {
    super('xiaohongshu');
  }

  /**
   * 发布笔记到小红书
   * @param article 文章内容
   * @param testMode 测试模式，为true时不点击发布按钮
   */
  async publish(article: ArticleContent, testMode: boolean = false): Promise<PublishResult> {
    try {
      console.log(`🚀 开始发布笔记到小红书...`);
      if (testMode) {
        console.log('📝 测试模式：将填写笔记但不发布');
      }
      
      await this.browserManager.launch();
      const page = this.browserManager.getPage();
      if (!page) {
        throw new Error('Page not initialized');
      }

      console.log('📱 导航到发布页面...');
      await this.browserManager.gotoPublishPage();
      await page.waitForTimeout(2000);

      if (this.browserManager.isOnLoginPage()) {
        console.log('⚠️ 检测到未登录，开始登录流程...');
        console.log('请在浏览器中扫码登录小红书...');
        
        const loginSuccess = await this.browserManager.waitForLogin(120000);
        if (!loginSuccess) {
          await this.browserManager.close();
          return {
            success: false,
            platform: this.platform,
            message: '登录超时，请重试',
          };
        }
        
        console.log('📱 登录成功，继续发布流程...');
        await this.browserManager.gotoPublishPage();
        await page.waitForTimeout(2000);
      }

      console.log('📝 填充笔记标题...');
      await this.fillTitle(article.title);
      
      console.log('📝 填充笔记内容...');
      await this.fillContent(article.content);

      if (article.coverImage) {
        console.log('🖼️ 上传封面图片...');
        await this.uploadCover(article.coverImage);
      }

      if (article.tags && article.tags.length > 0) {
        console.log('🏷️ 设置标签...');
        await this.setTags(article.tags);
      }

      if (testMode) {
        console.log('');
        console.log('===========================================');
        console.log('✅ 测试模式：笔记已填写完成！');
        console.log('⚠️  未点击发布按钮，请手动检查页面内容');
        console.log('===========================================');
        console.log('');
        
        const screenshotPath = `./test-screenshot-xiaohongshu-${Date.now()}.png`;
        await this.screenshot(screenshotPath);
        console.log(`📸 截图已保存: ${screenshotPath}`);
        
        await this.browserManager.saveCookies();
        
        console.log('');
        console.log('💡 浏览器将保持打开状态，请手动检查页面内容');
        console.log('   检查完成后，请手动关闭浏览器窗口');
        console.log('');
        
        return {
          success: true,
          platform: this.platform,
          message: '测试模式：笔记已填写完成，未发布',
          testMode: true,
        };
      }

      console.log('📤 点击发布按钮...');
      await this.clickPublish();
      
      const articleUrl = await this.getArticleUrl();
      
      await this.browserManager.saveCookies();
      await this.browserManager.close();

      return {
        success: true,
        platform: this.platform,
        message: '笔记发布成功',
        url: articleUrl || undefined,
      };
    } catch (error) {
      await this.browserManager.close();
      return {
        success: false,
        platform: this.platform,
        message: '发布失败',
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  protected async fillTitle(title: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const titleSelectors = [
      'input[placeholder*="标题"]',
      '.title-input input',
      'input[class*="title"]',
      'input[name="title"]',
    ];

    let titleInput = null;
    for (const selector of titleSelectors) {
      try {
        titleInput = await page.$(selector);
        if (titleInput) {
          console.log(`   使用选择器: ${selector}`);
          break;
        }
      } catch {
        continue;
      }
    }

    if (titleInput) {
      await titleInput.click();
      await titleInput.fill(title);
      console.log(`   标题: ${title}`);
    } else {
      console.warn('   未找到标题输入框');
    }
  }

  protected async fillContent(content: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const contentSelectors = [
      '#post-textarea',
      '[contenteditable="true"]',
      '.editor-content',
      'textarea[placeholder*="正文"]',
    ];

    let contentEditor = null;
    for (const selector of contentSelectors) {
      try {
        contentEditor = await page.$(selector);
        if (contentEditor) {
          console.log(`   使用选择器: ${selector}`);
          break;
        }
      } catch {
        continue;
      }
    }

    if (contentEditor) {
      await contentEditor.click();
      await page.waitForTimeout(500);
      await contentEditor.fill('');
      await page.keyboard.type(content, { delay: 10 });
      console.log(`   内容长度: ${content.length} 字符`);
    } else {
      console.warn('   未找到内容编辑器');
    }
  }

  protected async uploadCover(imagePath: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      const coverSelector = 'input[type="file"][accept*="image"], .upload-input input';
      await page.setInputFiles(coverSelector, imagePath);
      await page.waitForTimeout(3000);
      console.log(`   封面图片: ${imagePath}`);
    } catch (error) {
      console.warn('   封面上传失败:', error);
    }
  }

  protected async setTags(tags: string[]): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      const tagInputSelector = 'input[placeholder*="话题"], input[placeholder*="标签"], .tag-input input';
      await page.waitForSelector(tagInputSelector, { timeout: 5000 });
      
      for (const tag of tags.slice(0, 3)) {
        await page.fill(tagInputSelector, '#' + tag);
        await page.waitForTimeout(500);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(500);
      }
      console.log(`   标签: ${tags.slice(0, 3).join(', ')}`);
    } catch (error) {
      console.warn('   标签设置失败:', error);
    }
  }

  protected async clickPublish(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const publishSelector = 'button:has-text("发布"), .publish-btn, [class*="publish"]';
    await page.waitForSelector(publishSelector, { timeout: 10000 });
    await page.click(publishSelector);
    await page.waitForTimeout(3000);
  }

  protected async getArticleUrl(): Promise<string | null> {
    const page = this.browserManager.getPage();
    if (!page) return null;

    try {
      await page.waitForTimeout(2000);
      const url = page.url();
      if (url.includes('xiaohongshu.com/')) {
        return url;
      }
      return null;
    } catch {
      return null;
    }
  }
}
