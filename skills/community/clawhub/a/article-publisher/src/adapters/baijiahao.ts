import { BaseAdapter } from '../lib/base-adapter.js';
import { ArticleContent, PublishResult } from '../types/index.js';

/**
 * 百家号平台适配器
 * 
 * 百家号发布页面结构说明：
 * - 标题输入框：使用 cheetah-input 组件，通常是页面上第一个文本输入框
 * - 内容编辑器：使用 UEditor 编辑器，内容在 iframe 中
 * - 封面上传：在右侧设置区域，input[type="file"]
 * - 摘要输入框：textarea.cheetah-ui-pro-countable-textbox-textarea，placeholder="请输入摘要"
 * - 分类选择器：cheetah-select cheetah-cascader 组件，placeholder="请选择内容分类"
 */
export class BaijiahaoAdapter extends BaseAdapter {
  constructor() {
    super('baijiahao');
  }

  /**
   * 关闭百家号新手引导/确认框
   * 百家号在打开发布页面时可能会显示以下确认框：
   * 1. "新增风险检测" 确认框 - 点击 "我知道了" 按钮关闭
   * 2. "AI工具收起" 说明框 - 点击右上角 [x] 关闭按钮关闭
   */
  private async closeTourDialogs(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    console.log('   🔍 检查是否有新手引导/确认框...');

    try {
      // 等待一下让对话框出现
      await page.waitForTimeout(1000);

      // 循环关闭所有可能的确认框
      let hasDialog = true;
      let maxAttempts = 5;
      let attempt = 0;

      while (hasDialog && attempt < maxAttempts) {
        attempt++;
        hasDialog = false;

        // 检查是否有 cheetah-tour-content 对话框
        const tourContent = await page.$('.cheetah-tour-content');
        if (tourContent) {
          console.log(`   发现确认框 (尝试 ${attempt}/${maxAttempts})`);

          // 方法1: 优先点击"我知道了"按钮（这个对话框在最上层，有遮罩，必须先关闭）
          const allButtons = await page.$$('div.cheetah-tour-buttons > button');
          if (allButtons.length > 0) {
            console.log(`   找到 ${allButtons.length} 个按钮`);
            // 只点击第一个可见的按钮（最上层的对话框）
            // for (let i = 0; i < allButtons.length; i++) {
            for (let i = allButtons.length - 1; i >= 0; i--) {
              const btn = allButtons[i];
              const isVisible = await btn.isVisible();
              if (isVisible) {
                const btnText = await btn.textContent();
                console.log(`   点击按钮 [${i + 1}]: ${btnText}`);
                await btn.click();
                await page.waitForTimeout(500);
                hasDialog = true;
                break; // 只点击一个按钮就退出循环，等待下一次循环处理
              }
            }
            if (hasDialog) continue;
          }

          // 方法2: 点击关闭按钮 [x]
          const closeBtn = await page.$('button.cheetah-tour-close');
          if (closeBtn) {
            const isVisible = await closeBtn.isVisible();
            if (isVisible) {
              console.log('   点击关闭按钮 [x]');
              await closeBtn.click();
              await page.waitForTimeout(500);
              hasDialog = true;
              continue;
            }
          }
        }

        // 检查其他可能的对话框
        const otherDialogs = await page.$$('.cheetah-modal-content, .cheetah-dialog, [role="dialog"]');
        for (const dialog of otherDialogs) {
          const isVisible = await dialog.isVisible();
          if (isVisible) {
            const closeBtn = await dialog.$('button[class*="close"], .cheetah-modal-close, .close-btn');
            if (closeBtn) {
              console.log('   关闭其他对话框');
              await closeBtn.click();
              await page.waitForTimeout(500);
              hasDialog = true;
              break;
            }
          }
        }

        // 检查错误提示框（如"视频格式不正确"等）
        try {
          // 查找包含"提示"标题的对话框
          const tipDialogs = await page.$$('.cheetah-modal-wrap, [class*="modal"]');
          for (const dialog of tipDialogs) {
            const isVisible = await dialog.isVisible();
            if (isVisible) {
              const titleEl = await dialog.$('.cheetah-modal-title, [class*="title"]');
              const title = titleEl ? await titleEl.textContent() : '';
              const content = await dialog.textContent();

              // 检查是否是错误提示框
              if (title?.includes('提示') || content?.includes('格式不正确') || content?.includes('错误')) {
                console.log(`   发现错误提示框: ${title || '提示'}`);

                // 点击确认按钮关闭
                const confirmBtn = await dialog.$('button:has-text("确认"), button:has-text("确定"), .cheetah-btn-primary');
                if (confirmBtn) {
                  await confirmBtn.click();
                  console.log('   点击确认按钮关闭提示框');
                  await page.waitForTimeout(500);
                  hasDialog = true;
                  break;
                }

                // 点击关闭按钮
                const closeBtn = await dialog.$('button[class*="close"], .cheetah-modal-close');
                if (closeBtn) {
                  await closeBtn.click();
                  console.log('   点击关闭按钮关闭提示框');
                  await page.waitForTimeout(500);
                  hasDialog = true;
                  break;
                }
              }
            }
          }
        } catch {
          // 忽略错误
        }
      }

      if (attempt > 1) {
        console.log('   ✅ 确认框已处理完成');
      } else {
        console.log('   ✅ 未发现确认框');
      }
    } catch (error) {
      console.log('   ⚠️ 处理确认框时出错:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 处理错误提示框
   * 用于处理发布过程中出现的各种错误提示
   */
  private async handleErrorDialogs(): Promise<boolean> {
    const page = this.browserManager.getPage();
    if (!page) return false;

    let handled = false;

    try {
      // 查找常见的错误提示框
      const errorSelectors = [
        '.cheetah-modal-wrap',
        '.cheetah-modal-content',
        '[class*="modal"]',
        '[role="dialog"]',
      ];

      for (const selector of errorSelectors) {
        const dialogs = await page.$$(selector);
        for (const dialog of dialogs) {
          const isVisible = await dialog.isVisible();
          if (!isVisible) continue;

          const text = await dialog.textContent();

          // 检查是否是错误提示
          if (text?.includes('格式不正确') ||
            text?.includes('视频') ||
            text?.includes('错误') ||
            text?.includes('失败') ||
            text?.includes('提示')) {

            console.log(`   发现错误提示: ${text?.substring(0, 50)}...`);

            // 尝试点击确认/确定按钮
            const confirmBtn = await dialog.$('button:has-text("确认"), button:has-text("确定"), .cheetah-btn-primary, button');
            if (confirmBtn) {
              const btnText = await confirmBtn.textContent();
              console.log(`   点击按钮关闭提示: ${btnText}`);
              await confirmBtn.click();
              await page.waitForTimeout(500);
              handled = true;
              break;
            }

            // 尝试点击关闭按钮
            const closeBtn = await dialog.$('button[class*="close"], .cheetah-modal-close, [class*="close"]');
            if (closeBtn) {
              await closeBtn.click();
              console.log('   点击关闭按钮');
              await page.waitForTimeout(500);
              handled = true;
              break;
            }
          }
        }
        if (handled) break;
      }
    } catch (error) {
      console.log('   处理错误提示框时出错:', error);
    }

    return handled;
  }

  /**
   * 发布文章到百家号
   * @param article 文章内容
   * @param testMode 测试模式，为true时不点击发布按钮
   */
  async publish(article: ArticleContent, testMode: boolean = false): Promise<PublishResult> {
    try {
      console.log(`🚀 开始发布文章到百家号...`);
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
      // 等待页面加载完成
      await page.waitForTimeout(2000);

      // 先检查是否在登录页面（未登录状态）- 使用异步检测
      const isOnLoginPage = await this.browserManager.isOnLoginPageAsync();
      if (isOnLoginPage) {
        console.log('⚠️ 检测到未登录，开始登录流程...');
        console.log('请在浏览器中扫码登录百家号...');

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
      }

      // 等待编辑器加载完成
      console.log('   等待编辑器加载...');
      await page.waitForSelector('#ueditor', { timeout: 10000 });

      // 关闭百家号新手引导/确认框
      await this.closeTourDialogs();

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
          // 上传封面后，处理可能出现的错误提示框
          await this.handleErrorDialogs();
        }
      } else {
        console.log('🖼️ 未提供封面图片，跳过封面设置');
      }

      if (article.summary) {
        console.log('📝 填写文章摘要...');
        await this.fillSummary(article.summary);
      }

      if (article.category) {
        console.log('📁 选择文章分类...');
        await this.selectCategory(article.category);
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

        const screenshotPath = `./test-screenshot-baijiahao-${Date.now()}.png`;
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

  protected async fillTitle(title: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    console.log('   查找标题输入框...');

    // 百家号标题输入框：通过 #bjhNewsTitle 定位，然后找 contenteditable="true" 的元素
    const titleSelectors = [
      '#bjhNewsTitle [contenteditable="true"]',
      '#bjhNewsTitle .input-box [contenteditable="true"]',
      '[data-testid="news-title-input"] [contenteditable="true"]',
      '#newsTextArea [contenteditable="true"]',
    ];

    for (const selector of titleSelectors) {
      try {
        console.log(`   尝试选择器: ${selector}`);
        const titleInput = await page.$(selector);
        if (titleInput) {
          const isVisible = await titleInput.isVisible();
          if (isVisible) {
            console.log(`   ✅ 找到标题输入框: ${selector}`);

            // 点击并聚焦
            await titleInput.click();
            await page.waitForTimeout(300);

            // 清空并输入
            await page.keyboard.press('Control+A');
            await page.waitForTimeout(200);
            await page.keyboard.press('Backspace');
            await page.waitForTimeout(300);

            // 输入标题
            await page.keyboard.type(title, { delay: 50 });
            await page.waitForTimeout(500);

            console.log(`   ✅ 标题填写完成: ${title}`);
            return;
          }
        }
      } catch (error) {
        console.log(`   选择器 ${selector} 失败:`, error);
        continue;
      }
    }

    console.warn('   ❌ 未找到标题输入框');
  }

  protected async fillContent(content: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    console.log('   查找内容编辑器...');

    // 百家号使用 UEditor 编辑器，内容在 iframe 中
    // 首先尝试查找 iframe
    try {
      const iframeElement = await page.$('iframe[id*="editor"]');
      if (iframeElement) {
        console.log('   找到编辑器 iframe');
        const frame = await iframeElement.contentFrame();
        if (frame) {
          console.log('   在 iframe 中查找编辑区域...');
          const body = await frame.$('body.view');
          if (body) {
            console.log('   ✅ 找到内容编辑器 (iframe body)');
            await body.click();
            await page.waitForTimeout(500);

            // 输入内容
            const lines = content.split('\n');
            for (let i = 0; i < lines.length; i++) {
              const line = lines[i];

              // 逐字符输入
              for (let j = 0; j < line.length; j++) {
                const char = line[j];

                // 检查是否包含 #
                if (char == '#') {
                  // 输入字符
                  await page.keyboard.type(char, { delay: 100 });
                  // 遇到 # 号时等待话题对话框关闭
                  await page.keyboard.press('Escape');
                  await page.waitForTimeout(100);
                }
                else {
                  // 输入字符
                  await page.keyboard.type(char, { delay: 10 });
                }
              }

              // 换行（最后一行除外）
              if (i < lines.length - 1) {
                await page.keyboard.press('Enter');
                await page.waitForTimeout(200);
              }
            }

            console.log(`   ✅ 内容填写完成 (${content.length} 字符)`);
            return;
          }
        }
      }
    } catch (error) {
      console.log('   iframe 方式失败，尝试其他方式...');
    }

    // 备用方案：直接在页面中查找可编辑区域
    const contentSelectors = [
      '#editor',
      '[contenteditable="true"]',
      '.editor-content',
      '.ql-editor',
      '.ProseMirror',
      '.public-DraftEditor-content',
      '.edui-editor-iframeholder iframe',
    ];

    for (const selector of contentSelectors) {
      try {
        console.log(`   尝试选择器: ${selector}`);
        const contentEditor = await page.$(selector);
        if (contentEditor) {
          const isVisible = await contentEditor.isVisible();
          if (isVisible) {
            console.log(`   ✅ 找到内容编辑器: ${selector}`);
            await contentEditor.click();
            await page.waitForTimeout(500);

            // 清空编辑器
            await page.keyboard.press('Control+A');
            await page.waitForTimeout(300);
            await page.keyboard.press('Backspace');
            await page.waitForTimeout(500);

            // 输入内容
            const lines = content.split('\n');
            for (let i = 0; i < lines.length; i++) {
              await page.keyboard.type(lines[i], { delay: 10 });
              if (i < lines.length - 1) {
                await page.keyboard.press('Enter');
                await page.waitForTimeout(200);
              }
            }

            console.log(`   ✅ 内容填写完成 (${content.length} 字符)`);
            return;
          }
        }
      } catch {
        continue;
      }
    }

    console.warn('   ❌ 未找到内容编辑器');
  }

  protected async uploadCover(imagePath: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   🔍 寻找封面上传区域...');
      await page.waitForTimeout(1000);

      // 百家号封面上传流程：
      // 1. 先点击"添加封面"或封面区域触发上传
      // 2. 然后上传文件

      // 方法1: 尝试点击封面添加区域
      // 根据HTML结构，封面区域包含 "选择封面" 文字
      const coverTriggerSelectors = [
        '._93c3fe2a3121c388-item',           // 封面项容器
        '._73a3a52aab7e3a36-default',        // 封面默认区域
        '._73a3a52aab7e3a36-content',        // 封面内容区域
        '[class*="list"] [class*="item"]',   // 通用列表项
        '.bjh-news-cover-add',
        '[class*="cover-add"]',
        '[class*="cover"] [class*="add"]',
        '.cover-upload',
        '.cover-selector',
        '#bjhNewsCover [class*="add"]',
        '#bjhNewsCover .cheetah-btn',
        '#bjhNewsCover button',
      ];

      let clickedTrigger = false;
      for (const selector of coverTriggerSelectors) {
        try {
          const triggers = await page.$$(selector);
          console.log(`   查找选择器 ${selector}, 找到 ${triggers.length} 个元素`);

          for (const trigger of triggers) {
            const isVisible = await trigger.isVisible();
            if (isVisible) {
              const text = await trigger.textContent();
              console.log(`   元素文本: ${text?.substring(0, 30)}`);

              // 优先点击包含"选择封面"或"封面"文字的元素
              if (text?.includes('选择封面') || text?.includes('封面') || text?.includes('添加')) {
                console.log(`   ✅ 点击封面触发区域: ${selector}`);
                await trigger.click();
                await page.waitForTimeout(1000);
                clickedTrigger = true;
                break;
              }
            }
          }
          if (clickedTrigger) break;
        } catch (error) {
          console.log(`   选择器 ${selector} 失败:`, error);
          continue;
        }
      }

      // 如果没有找到特定文字的元素，尝试点击第一个可见的封面区域
      if (!clickedTrigger) {
        console.log('   尝试点击第一个可见的封面区域...');
        for (const selector of coverTriggerSelectors) {
          try {
            const trigger = await page.$(selector);
            if (trigger) {
              const isVisible = await trigger.isVisible();
              if (isVisible) {
                console.log(`   点击封面区域: ${selector}`);
                await trigger.click();
                await page.waitForTimeout(1000);
                clickedTrigger = true;
                break;
              }
            }
          } catch {
            continue;
          }
        }
      }

      // 查找 input[type="file"] 元素 - 优先查找图片上传
      // 注意：页面可能有多个 file input（视频、图片等），需要精确匹配
      const fileInputSelectors = [
        'input[type="file"][accept*="image"]:not([accept*="video"])',
        '#bjhNewsCover input[type="file"]',
        '[class*="cover"] input[type="file"]',
        '.cheetah-upload input[type="file"]',
      ];

      let uploaded = false;  // 标记是否已上传成功

      for (const selector of fileInputSelectors) {
        if (uploaded) break;  // 如果已上传，跳出外层循环

        try {
          const fileInputs = await page.$$(selector);
          console.log(`   查找选择器 ${selector}, 找到 ${fileInputs.length} 个元素`);

          for (const fileInput of fileInputs) {
            const accept = await fileInput.getAttribute('accept');
            console.log(`   file input accept: ${accept}`);

            // 确保是图片上传而不是视频上传
            if (!accept?.includes('video')) {
              console.log(`   ✅ 找到图片上传输入框: ${selector}`);
              await fileInput.setInputFiles(imagePath);
              await page.waitForTimeout(3000);
              console.log(`   ✅ 封面图片已上传: ${imagePath}`);
              uploaded = true;
              break;  // 跳出内层循环
            }
          }
        } catch (error) {
          console.log(`   选择器 ${selector} 失败:`, error);
          continue;
        }
      }

      // 如果第一种方式没成功，尝试备用方案
      if (!uploaded) {
        try {
          console.log('   尝试备用方案：查找所有 file input...');
          const allFileInputs = await page.$$('input[type="file"]');
          console.log(`   找到 ${allFileInputs.length} 个 file input`);

          for (const fileInput of allFileInputs) {
            const accept = await fileInput.getAttribute('accept');
            console.log(`   file input accept: ${accept}`);

            // 排除视频上传
            if (accept && !accept.includes('video')) {
              console.log('   ✅ 使用备用方案找到图片上传输入框');
              await fileInput.setInputFiles(imagePath);
              await page.waitForTimeout(3000);
              console.log(`   ✅ 封面图片已上传: ${imagePath}`);
              uploaded = true;
              break;
            }
          }
        } catch (error) {
          console.log('   备用方案失败:', error);
        }
      }

      // 上传图片后，点击"确定"按钮确认选择
      console.log('   点击确定按钮确认封面选择...');
      await page.waitForTimeout(1000);

      // 先找到弹出框容器，再在其中搜索确定按钮，避免找错按钮
      const modalSelectors = [
        '.cheetah-modal-content',
        '.cheetah-modal-wrap',
        '[class*="modal-content"]',
        '[role="dialog"]',
      ];

      let confirmed = false;

      // 先尝试在弹出框中查找确定按钮
      for (const modalSelector of modalSelectors) {
        if (confirmed) break;

        try {
          const modals = await page.$$(modalSelector);
          console.log(`   查找弹出框 ${modalSelector}, 找到 ${modals.length} 个`);

          for (const modal of modals) {
            const isVisible = await modal.isVisible();
            if (!isVisible) continue;

            // 在弹出框中查找确定按钮
            const confirmBtnSelectors = [
              '.e8c90bfac9d4eab4-confirmBtn',
              'button[class*="confirm"]',
              '.cheetah-btn-primary',
              'button:has-text("确定")',
              'button:has-text("确认")',
            ];

            for (const btnSelector of confirmBtnSelectors) {
              try {
                const confirmBtn = await modal.$(btnSelector);
                if (confirmBtn) {
                  const isVisible = await confirmBtn.isVisible();
                  if (isVisible) {
                    const btnText = await confirmBtn.textContent();
                    console.log(`   ✅ 在弹出框中找到确定按钮: ${btnText}`);
                    await confirmBtn.click();
                    await page.waitForTimeout(1000);
                    console.log('   ✅ 已点击确定按钮');
                    confirmed = true;
                    break;
                  }
                }
              } catch {
                continue;
              }
            }
            if (confirmed) break;
          }
        } catch {
          continue;
        }
      }

      // 如果在弹出框中没找到，尝试全局搜索
      if (!confirmed) {
        console.log('   尝试全局搜索确定按钮...');
        const globalBtnSelectors = [
          'button:has-text("确定")',
          'button:has-text("确认")',
          '.cheetah-btn-primary',
        ];

        for (const selector of globalBtnSelectors) {
          try {
            const confirmBtn = await page.$(selector);
            if (confirmBtn) {
              const isVisible = await confirmBtn.isVisible();
              if (isVisible) {
                const btnText = await confirmBtn.textContent();
                console.log(`   ✅ 找到确定按钮: ${btnText}`);
                await confirmBtn.click();
                await page.waitForTimeout(1000);
                console.log('   ✅ 已点击确定按钮');
                confirmed = true;
                break;
              }
            }
          } catch {
            continue;
          }
        }
      }

      if (!confirmed) {
        console.warn('   ⚠️ 未找到确定按钮');
      }

      return;
    } catch (error) {
      console.warn('   ⚠️ 封面上传失败:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 填写文章摘要
   * 百家号摘要输入框：textarea.cheetah-ui-pro-countable-textbox-textarea，placeholder="请输入摘要"
   */
  protected async fillSummary(summary: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   查找摘要输入框...');
      await page.waitForTimeout(500);

      // 百家号摘要输入框的精确选择器
      const summarySelectors = [
        'textarea.cheetah-ui-pro-countable-textbox-textarea',
        'textarea[placeholder="请输入摘要"]',
        'textarea[placeholder*="摘要"]',
        '.cheetah-ui-pro-countable-textbox-textarea',
      ];

      for (const selector of summarySelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const summaryInput = await page.$(selector);
          if (summaryInput) {
            const isVisible = await summaryInput.isVisible();
            if (isVisible) {
              const placeholder = await summaryInput.getAttribute('placeholder');
              console.log(`   元素 placeholder: ${placeholder}`);

              console.log(`   ✅ 找到摘要输入框: ${selector}`);
              await summaryInput.click();
              await page.waitForTimeout(300);
              await summaryInput.fill('');
              await page.waitForTimeout(300);
              await summaryInput.fill(summary);
              await page.waitForTimeout(500);
              console.log(`   ✅ 摘要填写完成: ${summary.substring(0, 50)}...`);
              return;
            }
          }
        } catch {
          continue;
        }
      }

      // 备用方案：查找所有 textarea
      try {
        console.log('   尝试备用方案：查找所有 textarea...');
        const allTextareas = await page.$$('textarea');
        for (const textarea of allTextareas) {
          const isVisible = await textarea.isVisible();
          if (isVisible) {
            const placeholder = await textarea.getAttribute('placeholder');
            if (placeholder?.includes('摘要')) {
              console.log(`   ✅ 通过备用方案找到摘要输入框`);
              await textarea.click();
              await page.waitForTimeout(300);
              await textarea.fill('');
              await page.waitForTimeout(300);
              await textarea.fill(summary);
              await page.waitForTimeout(500);
              console.log(`   ✅ 摘要填写完成: ${summary.substring(0, 50)}...`);
              return;
            }
          }
        }
      } catch {
        // 忽略错误
      }

      console.warn('   ❌ 未找到摘要输入框');
    } catch (error) {
      console.warn('   ⚠️ 摘要填写失败:', error instanceof Error ? error.message : String(error));
    }
  }

  /**
   * 选择文章分类
   * 百家号分类选择器：cheetah-select cheetah-cascader 组件
   * 支持级联选择，category 可以用 "/" 或 ">" 分隔多级分类
   * 例如: "科技/互联网" 或 "科技>互联网"
   */
  protected async selectCategory(category: string): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   查找分类选择器...');
      await page.waitForTimeout(500);

      // 解析分类层级
      const categories = category.split(/[\/>]/).map(c => c.trim()).filter(c => c);
      console.log(`   分类层级: ${categories.join(' > ')}`);

      // 方法1: 查找包含"分类"文本的下拉框
      try {
        const allSelects = await page.$$('.cheetah-select-selector');
        console.log(`   找到 ${allSelects.length} 个 cheetah-select-selector 元素`);

        for (const select of allSelects) {
          const text = await select.textContent();
          console.log(`   选择器文本: ${text?.substring(0, 50)}`);

          if (text?.includes('内容分类') || text?.includes('分类')) {
            console.log('   找到分类选择器');

            // 点击打开下拉框
            await select.click();
            await page.waitForTimeout(800);

            // 逐级选择分类
            for (let level = 0; level < categories.length; level++) {
              const cat = categories[level];
              console.log(`   选择第 ${level + 1} 级分类: ${cat}`);

              // 等待选项出现
              await page.waitForTimeout(500);

              // 查找当前级别的分类选项
              // 级联选择器通常有多列，每列是一个层级
              const menuSelectors = [
                '.cheetah-cascader-menu',
                '[class*="cascader-menu"]',
                '.cheetah-select-dropdown',
              ];

              let found = false;
              for (const menuSelector of menuSelectors) {
                const menus = await page.$$(menuSelector);
                console.log(`   找到 ${menus.length} 个菜单列`);

                // 选择对应层级的菜单
                const targetMenu = menus[level] || menus[menus.length - 1];
                if (targetMenu) {
                  const options = await targetMenu.$$('[class*="menu-item"], [class*="option"], li');
                  console.log(`   第 ${level + 1} 列有 ${options.length} 个选项`);

                  for (const opt of options) {
                    const optText = await opt.textContent();
                    if (optText?.includes(cat)) {
                      console.log(`   找到匹配选项: ${optText}`);
                      await opt.click();
                      await page.waitForTimeout(500);
                      found = true;
                      break;
                    }
                  }
                }
                if (found) break;
              }

              if (!found) {
                // 备用方案：在整个页面中查找匹配的选项
                console.log(`   尝试备用方案查找: ${cat}`);
                const allOptions = await page.$$('[class*="cascader-menu-item"], [class*="select-option"], [class*="option"], li');
                for (const opt of allOptions) {
                  const optText = await opt.textContent();
                  if (optText?.trim() === cat || optText?.includes(cat)) {
                    console.log(`   找到匹配选项: ${optText}`);
                    await opt.click();
                    await page.waitForTimeout(500);
                    found = true;
                    break;
                  }
                }
              }

              if (!found) {
                console.warn(`   ⚠️ 未找到第 ${level + 1} 级分类: ${cat}`);
                break;
              }
            }

            console.log(`   ✅ 分类选择完成: ${categories.join(' > ')}`);
            return;
          }
        }
      } catch (error) {
        console.log('   方法1失败:', error);
      }

      // 方法2: 查找包含"分类"标签的表单项
      try {
        const allFormItems = await page.$$('.cheetah-form-item');
        for (const formItem of allFormItems) {
          const labelEl = await formItem.$('.cheetah-form-item-label');
          const labelText = labelEl ? await labelEl.textContent() : '';
          if (labelText?.includes('分类')) {
            console.log('   找到分类表单项');

            const selector = await formItem.$('.cheetah-select-selector');
            if (selector) {
              await selector.click();
              await page.waitForTimeout(800);

              // 逐级选择分类（同上）
              for (let level = 0; level < categories.length; level++) {
                const cat = categories[level];
                console.log(`   选择第 ${level + 1} 级分类: ${cat}`);
                await page.waitForTimeout(500);

                const allOptions = await page.$$('[class*="cascader-menu-item"], [class*="select-option"], li');
                for (const opt of allOptions) {
                  const optText = await opt.textContent();
                  if (optText?.includes(cat)) {
                    await opt.click();
                    await page.waitForTimeout(500);
                    break;
                  }
                }
              }

              console.log(`   ✅ 分类选择完成: ${categories.join(' > ')}`);
              return;
            }
          }
        }
      } catch {
        // 忽略错误
      }

      console.warn('   ❌ 未找到分类选择器');
    } catch (error) {
      console.warn('   ⚠️ 分类选择失败:', error instanceof Error ? error.message : String(error));
    }
  }

  protected async setTags(tags: string[]): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    try {
      console.log('   查找标签输入框...');
      await page.waitForTimeout(500);

      const tagInputSelectors = [
        'input[placeholder*="标签"]',
        'input[placeholder*="关键词"]',
        'input[placeholder*="tag"]',
        '.tag-input input',
        '[class*="tag"] input',
      ];

      for (const selector of tagInputSelectors) {
        try {
          console.log(`   尝试选择器: ${selector}`);
          const tagInput = await page.$(selector);
          if (tagInput) {
            const isVisible = await tagInput.isVisible();
            if (isVisible) {
              console.log(`   ✅ 找到标签输入框: ${selector}`);

              for (const tag of tags.slice(0, 5)) {
                await tagInput.click();
                await page.waitForTimeout(300);
                await tagInput.fill(tag);
                await page.waitForTimeout(500);
                await page.keyboard.press('Enter');
                await page.waitForTimeout(500);
              }

              console.log(`   ✅ 标签设置完成: ${tags.slice(0, 5).join(', ')}`);
              return;
            }
          }
        } catch {
          continue;
        }
      }

      console.warn('   ❌ 未找到标签输入框');
    } catch (error) {
      console.warn('   ⚠️ 标签设置失败:', error instanceof Error ? error.message : String(error));
    }
  }

  protected async clickPublish(): Promise<void> {
    const page = this.browserManager.getPage();
    if (!page) return;

    const publishSelectors = [
      'button:has-text("发布")',
      '.publish-btn',
      '[class*="publish"]:not([class*="draft"])',
      'button[type="submit"]',
      '.submit-btn',
    ];

    for (const selector of publishSelectors) {
      try {
        console.log(`   尝试选择器: ${selector}`);
        const publishBtn = await page.$(selector);
        if (publishBtn) {
          const isVisible = await publishBtn.isVisible();
          if (isVisible) {
            console.log(`   ✅ 找到发布按钮: ${selector}`);
            await publishBtn.click();
            await page.waitForTimeout(3000);
            console.log('   ✅ 已点击发布按钮');
            return;
          }
        }
      } catch {
        continue;
      }
    }

    console.warn('   ⚠️ 未找到发布按钮');
  }

  protected async getArticleUrl(): Promise<string | null> {
    const page = this.browserManager.getPage();
    if (!page) return null;

    try {
      await page.waitForTimeout(2000);
      const url = page.url();
      if (url.includes('baijiahao.baidu.com/')) {
        return url;
      }
      return null;
    } catch {
      return null;
    }
  }
}
