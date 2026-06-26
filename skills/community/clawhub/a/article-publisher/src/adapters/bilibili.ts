import { BaseAdapter } from '../lib/base-adapter.js';
import { ArticleContent, PublishResult } from '../types/index.js';

/**
 * Bilibili平台适配器
 */
export class BilibiliAdapter extends BaseAdapter {
  constructor() {
    super('bilibili');
  }

  /**
   * 获取Bilibili编辑器的iframe定位器
   * Bilibili的发布页面使用iframe加载编辑器，所有编辑元素都在iframe中
   */
  private getIframeLocator() {
    const page = this.browserManager.getPage();
    if (!page) {
      throw new Error('Page not initialized');
    }
    return page.frameLocator('iframe[src*="member.bilibili.com/york/read-editor"]');
  }

  /**
   * 发布文章到Bilibili
   * @param article 文章内容
   * @param testMode 测试模式，为true时不点击发布按钮
   */
  async publish(article: ArticleContent, testMode: boolean = false): Promise<PublishResult> {
    try {
      console.log(`🚀 开始发布文章到Bilibili...`);
      if (testMode) {
        console.log('📝 测试模式：将填写文章但不发布');
      }
      
      await this.browserManager.launch();
      const page = this.browserManager.getPage();
      if (!page) {
        throw new Error('Page not initialized');
      }

      console.log('📱 导航到发布页面...');
      await this.browserManager.gotoPublishPage();
      console.log('   等待页面加载...');
      await page.waitForTimeout(3000);

      // 检查登录
      if (this.browserManager.isOnLoginPage()) {
        console.log('⚠️ 检测到未登录，开始登录流程...');
        console.log('请在浏览器中扫码登录Bilibili...');
        
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
        await page.waitForTimeout(3000);
      }

      console.log('🔍 检查页面元素...');
      const currentUrl = page.url();
      console.log(`   当前URL: ${currentUrl}`);

      console.log('📝 填充文章标题...');
      await this.fillTitle(article.title);
      
      console.log('📝 填充文章内容...');
      await this.fillContent(article.content);

      // 处理封面图片（只支持本地文件路径）
      if (article.coverImage) {
        if (article.coverImage.startsWith('http')) {
          console.log('⚠️ 不支持 URL 形式的封面图片，请提供本地文件路径');
        } else {
          console.log('🖼️ 使用用户提供的封面图片...');
          console.log('📤 上传封面图片...');
          await this.uploadCover(article.coverImage);
        }
      } else {
        console.log('🖼️ 未提供封面图片，跳过封面设置');
      }

      if (article.tags && article.tags.length > 0) {
        console.log('🏷️ 设置标签...');
        await this.setTags(article.tags);
      }

      if (testMode) {
        console.log('');
        console.log('===========================================');
        console.log('✅ 测试模式：文章已填写完成！');
        console.log('⚠️  未点击发布按钮，请手动检查页面内容');
        console.log('===========================================');
        console.log('');
        
        const screenshotPath = `./test-screenshot-bilibili-${Date.now()}.png`;
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
          message: '测试模式：文章已填写完成，未发布',
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
        message: '文章发布成功',
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

  /**
   * 填充标题
   */
  protected async fillTitle(title: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) { 
      console.error('   ❌ 未获取到有效页面'); 
      return;
    }

    console.log('   等待iframe加载...');

    try {
      const iframeLocator = this.getIframeLocator();

      console.log('   等待标题输入框出现...');

      const titleSelectors = [
        'textarea.title-input__inner',
        'textarea[placeholder*="标题"]',
        '.title-input textarea',
        'input[placeholder*="标题"]',
      ];

      let foundSelector = '';
      for (const selector of titleSelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const locator = iframeLocator.locator(selector);
          await locator.waitFor({ timeout: 10000, state: 'visible' });
          foundSelector = selector;
          console.log(`   ✅ 找到标题输入框: ${selector}`);
          break;
        } catch (error) {
          console.log(`   ❌ 未找到: ${selector}`);
          continue;
        }
      }

      if (foundSelector) {
        const titleInput = iframeLocator.locator(foundSelector);

        console.log('   点击标题输入框...');
        await titleInput.click({ force: true });
        await page.waitForTimeout(500);

        console.log('   清空标题输入框...');
        await titleInput.fill('');
        await page.waitForTimeout(300);

        console.log(`   输入标题: ${title}`);
        await titleInput.fill(title);
        await page.waitForTimeout(500);

        console.log('   ✅ 标题填写完成');
      } else {
        console.warn('   ❌ 未找到标题输入框');
      }
    } catch (error) {
      console.error('   ❌ iframe操作失败:', error);
    }
  }

  /**
   * 填充内容
   */
  protected async fillContent(content: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    console.log('   等待iframe加载...');

    try {
      const iframeLocator = this.getIframeLocator();

      console.log('   等待内容编辑器出现...');

      const contentSelectors = [
        '.tiptap.ProseMirror.eva3-editor',
        '.eva3-editor[contenteditable="true"]',
        '.tiptap[contenteditable="true"]',
        '[contenteditable="true"].ProseMirror',
        '.ql-editor',
        '[contenteditable="true"]',
      ];

      let foundSelector = '';
      for (const selector of contentSelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const locator = iframeLocator.locator(selector);
          await locator.waitFor({ timeout: 10000, state: 'visible' });
          foundSelector = selector;
          console.log(`   ✅ 找到内容编辑器: ${selector}`);
          break;
        } catch (error) {
          console.log(`   ❌ 未找到: ${selector}`);
          continue;
        }
      }

      if (foundSelector) {
        const contentEditor = iframeLocator.locator(foundSelector);

        console.log('   点击内容编辑器...');
        await contentEditor.click({ force: true });
        await page.waitForTimeout(1000);

        console.log('   清空编辑器内容...');
        await contentEditor.press('Control+A');
        await page.waitForTimeout(300);
        await contentEditor.press('Backspace');
        await page.waitForTimeout(500);

        console.log('   开始输入内容...');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          await contentEditor.type(lines[i], { delay: 20 });
          if (i < lines.length - 1) {
            await contentEditor.press('Enter');
            await page.waitForTimeout(200);
          }
        }

        await page.waitForTimeout(500);
        console.log(`   ✅ 内容填写完成 (${content.length} 字符)`);
      } else {
        console.warn('   ❌ 未找到内容编辑器');
      }
    } catch (error) {
      console.error('   ❌ iframe操作失败:', error);
    }
  }

  protected async uploadCover(imagePath: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   等待iframe加载...');
      const iframeLocator = this.getIframeLocator();
      
      console.log('   🔍 寻找封面上传区域...');
      
      // 首先检查自定义封面开关状态
      // 根据实际 HTML 结构，开关在 .form-item 内，包含 "自定义封面" 文字
      const formItems = await iframeLocator.locator('.form-item').all();
      console.log(`   📋 找到 ${formItems.length} 个 .form-item 元素`);
      
      for (const formItem of formItems) {
        try {
          const labelText = await formItem.locator('.form-item-label').textContent();
          
          if (labelText?.includes('自定义封面')) {
            console.log('   找到"自定义封面"表单项');
            
            // 在这个 form-item 内查找开关
            const switchEl = formItem.locator('.vui_switch--switch');
            const isChecked = await switchEl.getAttribute('aria-checked');
            
            console.log(`   开关状态: aria-checked=${isChecked}`);
            
            if (isChecked !== 'true') {
              console.log('   正在开启自定义封面开关...');
              await switchEl.click();
              await page.waitForTimeout(1000);
              console.log('   ✅ 已开启自定义封面开关');
            } else {
              console.log('   ✅ 自定义封面开关已开启');
            }
            break;
          }
        } catch {
          continue;
        }
      }

      // 等待封面上传区域出现
      await page.waitForTimeout(1000);

      // 查找添加封面按钮
      const uploadButton = iframeLocator.locator('.upload-button:has-text("添加封面"), .select-cover .upload-button, .upload-button').first();
      
      try {
        await uploadButton.waitFor({ timeout: 5000, state: 'visible' });
        console.log('   找到封面上传按钮');
        
        console.log('   点击"添加封面"按钮...');
        await uploadButton.click();
        await page.waitForTimeout(1000);
        
        // 查找文件输入框
        const fileInput = iframeLocator.locator('input[type="file"]');
        await fileInput.waitFor({ timeout: 5000, state: 'visible' });
        console.log('   选择文件...');
        await fileInput.setInputFiles(imagePath);
        await page.waitForTimeout(2000);
        console.log(`   ✅ 封面图片已上传: ${imagePath}`);
        
        // 处理封面裁剪确认对话框
        await this.confirmCoverCrop();
        return;
      } catch {
        console.log('   未找到封面上传按钮');
      }

      // 备用方案：直接查找文件输入框
      console.log('   尝试直接查找文件输入框...');
      const fileInputs = await iframeLocator.locator('input[type="file"]').all();
      console.log(`   📋 页面共有 ${fileInputs.length} 个文件输入框`);
      
      for (const input of fileInputs) {
        try {
          await input.setInputFiles(imagePath);
          await page.waitForTimeout(2000);
          console.log(`   ✅ 封面图片已上传: ${imagePath}`);
          
          // 处理封面裁剪确认对话框
          await this.confirmCoverCrop();
          return;
        } catch {
          continue;
        }
      }

      console.warn('   ⚠️ 未能找到封面上传区域，跳过封面上传');
    } catch (error) {
      console.warn('   ⚠️ 封面上传失败:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 确认封面裁剪对话框
   */
  protected async confirmCoverCrop(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;
    
    console.log('   等待封面裁剪对话框...');
    
    try {
      // 等待对话框出现
      await page.waitForTimeout(2000);
      
      const iframeLocator = this.getIframeLocator();
      
      // 查找确认按钮（在iframe中）
      const confirmSelectors = [
        '.vui_dialog--footer button.vui_button--blue:has-text("确定")',
        '.vui_dialog--footer button:has-text("确定")',
        '.vui_dialog--btn-confirm',
        'button.vui_button--blue:has-text("确定")',
      ];

      for (const selector of confirmSelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const confirmButton = iframeLocator.locator(selector).first();
          await confirmButton.waitFor({ timeout: 5000, state: 'visible' });
          console.log('   ✅ 找到确认按钮');
          await confirmButton.click();
          await page.waitForTimeout(1000);
          console.log('   ✅ 已点击确认按钮');
          return;
        } catch {
          console.log(`   ❌ 未找到: ${selector}`);
          continue;
        }
      }
      
      console.log('   未找到封面裁剪对话框，继续执行');
    } catch (error) {
      console.log('   封面裁剪对话框处理失败:', error instanceof Error ? error.message : String(error));
    }
  }

  protected async setTags(tags: string[]): Promise<void> {
    console.log('   ⚠️ Bilibili已改为在正文中使用 #标签# 格式添加标签');
    console.log(`   建议标签: ${tags.map(t => `#${t}#`).join(' ')}`);
  }

  protected async clickPublish(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    console.log('   等待iframe加载...');
    
    try {
      const iframeLocator = this.getIframeLocator();
      
      const publishSelectors = [
        'button.vui_button--blue:has-text("发布")',
        'button:has-text("发布")',
        '.footer-right button.vui_button--blue',
      ];

      for (const selector of publishSelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const button = iframeLocator.locator(selector);
          await button.waitFor({ timeout: 10000, state: 'visible' });
          console.log(`   ✅ 找到发布按钮: ${selector}`);
          await button.click();
          await page.waitForTimeout(3000);
          console.log('   ✅ 已点击发布按钮');
          return;
        } catch (error) {
          console.log(`   ❌ 未找到: ${selector}`);
          continue;
        }
      }

      console.warn('   ⚠️ 未找到发布按钮');
    } catch (error) {
      console.error('   ❌ iframe操作失败:', error);
    }
  }

  protected async getArticleUrl(): Promise<string | null> {
    const page = this.browserManager.getPage();
    if (!page) return null;

    try {
      await page.waitForTimeout(2000);
      const url = page.url();
      if (url.includes('bilibili.com/read/')) {
        return url;
      }
      return null;
    } catch {
      return null;
    }
  }
}
