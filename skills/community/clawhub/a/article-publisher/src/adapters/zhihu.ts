import { BaseAdapter } from '../lib/base-adapter.js';
import { ArticleContent, PublishResult, PlatformName } from '../types/index.js';

/**
 * 知乎平台适配器
 */
export class ZhihuAdapter extends BaseAdapter {
  constructor() {
    super('zhihu');
  }

  /**
   * 发布文章到知乎
   * @param article 文章内容
   * @param testMode 测试模式，为true时不点击发布按钮
   */
  async publish(article: ArticleContent, testMode: boolean = false): Promise<PublishResult> {
    try {
      console.log(`🚀 开始发布文章到知乎...`);
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
      await page.waitForTimeout(2000);

      if (this.browserManager.isOnLoginPage()) {
        console.log('⚠️ 检测到未登录，开始登录流程...');
        console.log('请在浏览器中扫码登录知乎...');
        
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
        
        const screenshotPath = `./test-screenshot-zhihu-${Date.now()}.png`;
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
    if (!page) return;

    const titleSelectors = [
      'textarea[placeholder*="标题"]',
      'textarea[placeholder*="输入标题"]',
      '.WriteIndex-titleInput textarea',
      '.title-input textarea',
      'textarea[class*="title"]',
      'textarea.Input',
      'input[placeholder*="输入标题"]',
      'input[placeholder*="标题"]',
    ];

    let titleInput = null;
    for (const selector of titleSelectors) {
      try {
        titleInput = await page.$(selector);
        if (titleInput) {
          console.log(`   ✅ 找到标题输入框，使用选择器: ${selector}`);
          break;
        }
      } catch {
        continue;
      }
    }

    if (!titleInput) {
      console.log('   ⚠️ 预设选择器未找到，尝试查找所有 textarea/input 元素...');
      const textareas = await page.$$('textarea');
      const inputs = await page.$$('input[type="text"], input:not([type])');
      console.log(`   📋 页面共有 ${textareas.length} 个textarea, ${inputs.length} 个input元素`);
      
      for (const textarea of textareas) {
        const placeholder = await textarea.getAttribute('placeholder');
        if (placeholder?.includes('标题')) {
          titleInput = textarea;
          console.log(`   ✅ 找到标题输入框(textarea): placeholder="${placeholder}"`);
          break;
        }
      }
      
      if (!titleInput) {
        for (const input of inputs) {
          const placeholder = await input.getAttribute('placeholder');
          const className = await input.getAttribute('class');
          if (placeholder?.includes('标题') || className?.toLowerCase().includes('title')) {
            titleInput = input;
            console.log(`   ✅ 找到标题输入框(input): placeholder="${placeholder}", class="${className}"`);
            break;
          }
        }
      }
    }

    if (titleInput) {
      await titleInput.click();
      await titleInput.fill(title);
      console.log(`   📝 标题已填充: ${title}`);
    } else {
      console.error('   ❌ 未找到标题输入框，尝试使用键盘输入作为后备方案...');
      await page.keyboard.type(title);
      console.log(`   ⚠️ 标题已通过键盘输入: ${title}`);
    }
  }

  /**
   * 填充内容
   */
  protected async fillContent(content: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const contentSelectors = [
      '.public-DraftEditor-content',
      '.DraftEditor-editorContainer [contenteditable="true"]',
      '[data-contents="true"]',
      '.ql-editor',
      '[contenteditable="true"]',
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
      console.warn('   未找到内容编辑器，尝试点击页面中央...');
      const viewport = page.viewportSize();
      if (viewport) {
        await page.mouse.click(viewport.width / 2, viewport.height / 2);
        await page.keyboard.type(content, { delay: 10 });
        console.log(`   内容长度: ${content.length} 字符`);
      }
    }
  }

  /**
   * 上传封面 - 修复版，上传到右侧封面区域
   */
  protected async uploadCover(imagePath: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   🔍 寻找封面上传区域...');

      // 知乎封面上传的正确选择器（基于实际 HTML 结构）
      const coverInputSelectors = [
        'input.UploadPicture-input',
        'input[type="file"][accept*=".jpg"], input[type="file"][accept*=".png"]',
        '.UploadPicture-wrapper input[type="file"]',
        'label.UploadPicture-wrapper input',
      ];

      let uploadSuccess = false;

      // 方法1: 直接查找封面上传输入框
      for (const selector of coverInputSelectors) {
        try {
          const input = await page.$(selector);
          if (input) {
            const isVisible = await input.isVisible().catch(() => false);
            const isHidden = !isVisible;
            
            // 即使 input 不可见，也可以直接设置文件
            console.log(`   找到封面上传输入框: ${selector} (visible: ${isVisible})`);
            
            await input.setInputFiles(imagePath);
            await page.waitForTimeout(2000);
            console.log(`   ✅ 封面图片已上传到封面区域: ${imagePath}`);
            uploadSuccess = true;
            break;
          }
        } catch {
          continue;
        }
      }

      // 方法2: 点击"添加封面"区域后上传
      if (!uploadSuccess) {
        const coverAreaSelectors = [
          'label.UploadPicture-wrapper',
          '.css-1i9x2dq',
          'text=添加文章封面',
          'text=添加封面',
        ];

        for (const selector of coverAreaSelectors) {
          try {
            const area = await page.$(selector);
            if (area) {
              console.log(`   找到封面区域: ${selector}`);
              await area.click();
              await page.waitForTimeout(1000);
              
              // 点击后查找文件输入框
              const input = await page.$('input[type="file"]');
              if (input) {
                await input.setInputFiles(imagePath);
                await page.waitForTimeout(2000);
                console.log(`   ✅ 封面图片已上传（点击后上传）: ${imagePath}`);
                uploadSuccess = true;
                break;
              }
            }
          } catch {
            continue;
          }
        }
      }

      // 方法3: 通过位置判断，封面区域通常在页面右侧
      if (!uploadSuccess) {
        const allInputs = await page.$$('input[type="file"]');
        console.log(`   📋 页面共有 ${allInputs.length} 个文件输入框`);
        
        for (const input of allInputs) {
          try {
            const box = await input.boundingBox();
            if (box) {
              console.log(`   输入框位置: x=${box.x}, y=${box.y}, width=${box.width}, height=${box.height}`);
              
              const viewport = page.viewportSize();
              if (viewport && box.x > viewport.width / 2) {
                await input.setInputFiles(imagePath);
                await page.waitForTimeout(2000);
                console.log(`   ✅ 封面图片已上传（通过位置判断）: ${imagePath}`);
                uploadSuccess = true;
                break;
              }
            }
          } catch {
            continue;
          }
        }
      }

      if (!uploadSuccess) {
        console.warn('   ⚠️ 未能找到封面上传区域，跳过封面上传');
      }

    } catch (error) {
      console.warn('   ⚠️ 封面上传失败:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 设置标签
   */
  protected async setTags(tags: string[]): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      const topicButtonSelectors = [
        'button:has-text("话题")',
        '[class*="topic"] button',
        '.TopicSelectButton',
        '[class*="TagButton"]',
      ];
      
      for (const selector of topicButtonSelectors) {
        try {
          const button = await page.$(selector);
          if (button) {
            await button.click();
            await page.waitForTimeout(500);
            console.log('   点击话题按钮展开');
            break;
          }
        } catch {
          continue;
        }
      }

      const tagInputSelectors = [
        'input[placeholder*="搜索话题"]:visible',
        'input[placeholder*="话题"]:visible',
        'input[aria-label*="话题"]:visible',
        '.TopicSelector input',
        '[class*="topic"] input:visible',
      ];

      let tagInput = null;
      for (const selector of tagInputSelectors) {
        try {
          tagInput = await page.$(selector);
          if (tagInput) {
            const isVisible = await tagInput.isVisible();
            if (isVisible) {
              console.log(`   找到话题输入框: ${selector}`);
              break;
            }
          }
        } catch {
          continue;
        }
      }

      if (!tagInput) {
        console.warn('   未找到可见的话题输入框，跳过标签设置');
        return;
      }

      for (const tag of tags.slice(0, 5)) {
        await tagInput.fill(tag);
        await page.waitForTimeout(800);
        
        // 等待下拉框出现
        const dropdownSelectors = [
          '.Popover-content button',
          '[class*="Popover"] button',
          '.css-ogem9c button',
        ];
        
        let dropdownVisible = false;
        for (const dropdownSelector of dropdownSelectors) {
          try {
            const dropdown = await page.$(dropdownSelector);
            if (dropdown) {
              const isVisible = await dropdown.isVisible().catch(() => false);
              if (isVisible) {
                console.log(`   找到话题下拉框，点击第一个选项`);
                await dropdown.click();
                await page.waitForTimeout(500);
                dropdownVisible = true;
                break;
              }
            }
          } catch {
            continue;
          }
        }
        
        // 如果下拉框没出现，按 Enter
        if (!dropdownVisible) {
          await page.keyboard.press('Enter');
          await page.waitForTimeout(500);
        }
      }
      console.log(`   标签: ${tags.slice(0, 5).join(', ')}`);
    } catch (error) {
      console.warn('   标签设置失败，跳过:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 点击发布
   */
  protected async clickPublish(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const publishSelector = 'button:has-text("发布"), .publish-button, [class*="publish"]';
    await page.waitForSelector(publishSelector, { timeout: 10000 });
    await page.click(publishSelector);
    await page.waitForTimeout(3000);
  }

  /**
   * 获取文章链接
   */
  protected async getArticleUrl(): Promise<string | null> {
    const page = this.browserManager.getPage();
    if (!page) return null;

    try {
      await page.waitForTimeout(2000);
      const url = page.url();
      if (url.includes('zhuanlan.zhihu.com/p/')) {
        return url;
      }
      return null;
    } catch {
      return null;
    }
  }
}
