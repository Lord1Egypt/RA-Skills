import { chromium, Browser, BrowserContext, Page } from 'playwright';
import { PlatformName, PLATFORMS } from '../types/index.js';
import { CookieManager } from './cookie-manager.js';
import { getConfig } from './config.js';

/**
 * 浏览器管理器
 */
export class BrowserManager {
  private browser: Browser | null = null;
  private context: BrowserContext | null = null;
  private page: Page | null = null;
  private platform: PlatformName;
  private cookieManager: CookieManager;

  constructor(platform: PlatformName) {
    this.platform = platform;
    this.cookieManager = new CookieManager(platform);
  }

  /**
   * 启动浏览器
   */
  async launch(): Promise<Page> {
    if (this.browser && this.page) {
      return this.page;
    }

    const config = getConfig();
    const platformInfo = PLATFORMS[this.platform];

    this.browser = await chromium.launch({
      headless: config.headless,
      slowMo: config.slowMo,
      args: [
        '--disable-features=IsolateOrigins,site-per-process',
      ],
    });

    const cookieData = await this.cookieManager.loadCookies();

    const storageState = cookieData ? {
      cookies: cookieData.cookies,
      origins: [],
    } : undefined;

    this.context = await this.browser.newContext({
      viewport: { width: 1280, height: 800 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      storageState,
    });

    this.page = await this.context.newPage();
    this.page.setDefaultTimeout(config.timeout);

    return this.page;
  }

  /**
   * 获取当前页面
   */
  getPage(): Page | null {
    return this.page;
  }

  /**
   * 获取浏览器上下文
   */
  getContext(): BrowserContext | null {
    return this.context;
  }

  /**
   * 保存当前Cookie
   */
  async saveCookies(): Promise<void> {
    if (!this.context) {
      throw new Error('Browser context not initialized');
    }

    const state = await this.context.storageState();
    await this.cookieManager.saveCookies(state.cookies);
  }

  /**
   * 导航到登录页面
   */
  async gotoLoginPage(): Promise<void> {
    if (!this.page) {
      throw new Error('Page not initialized');
    }

    const platformInfo = PLATFORMS[this.platform];
    await this.page.goto(platformInfo.loginUrl, { waitUntil: 'networkidle' });
  }

  /**
   * 导航到发布页面
   */
  async gotoPublishPage(): Promise<void> {
    if (!this.page) {
      throw new Error('Page not initialized');
    }

    const platformInfo = PLATFORMS[this.platform];
    console.log('   导航到发布页面:', platformInfo.publishUrl);
    
    try {
      await this.page.goto(platformInfo.publishUrl, { 
        waitUntil: 'domcontentloaded',
        timeout: 30000
      });
      
      await this.page.waitForTimeout(2000);
      
      const currentUrl = this.page.url();
      console.log('   当前页面URL:', currentUrl);
      
      if (this.isOnLoginPage() || currentUrl.includes('login')) {
        console.log('   ⚠️ 检测到未登录，页面已跳转到登录页面');
        await this.handleBaijiahaoLoginButton();
        return;
      }
      
      console.log('   导航到发布页面完毕:', platformInfo.publishUrl);
      
      if (this.platform === 'baijiahao') {
        await this.handleBaijiahaoLoginButton();
      }
    } catch (error) {
      const currentUrl = this.page.url();
      console.log('   导航过程中出现错误，当前URL:', currentUrl);
      
      if (this.isOnLoginPage() || currentUrl.includes('login')) {
        console.log('   ⚠️ 检测到未登录，页面已跳转到登录页面');
        await this.handleBaijiahaoLoginButton();
        return;
      }
      
      throw error;
    }
  }
  
  /**
   * 处理百家号登录按钮
   * 百家号需要先点击右上角的【登录】按钮才会显示扫码界面
   */
  private async handleBaijiahaoLoginButton(): Promise<void> {
    if (!this.page) return;
    
    try {
      // 等待页面加载完成
      await this.page.waitForTimeout(2000);
      
      // 检查是否在登录页面（未登录状态）
      const currentUrl = this.page.url();
      if (!currentUrl.includes('login')) {
        return; // 已经登录或不在登录页面
      }
      
      console.log('   检测到百家号登录页面，尝试点击登录按钮...');
      
      // 查找登录按钮
      const loginBtnSelectors = [
        '[data-testid="bjh-login-btn"]',  // 根据用户提供的HTML
        'button.loginBtn--lZVgU',          // 类名
        'header button',                   // header 中的 button
        'button:has-text("登录")',         // 包含"登录"文字的按钮
        '.loginBtn--lZVgU',
        '[class*="loginBtn"]',
      ];
      
      for (const selector of loginBtnSelectors) {
        try {
          const loginBtn = await this.page.$(selector);
          if (loginBtn) {
            const isVisible = await loginBtn.isVisible();
            if (isVisible) {
              const btnText = await loginBtn.textContent();
              console.log(`   找到登录按钮: ${btnText}`);
              await loginBtn.click();
              console.log('   ✅ 已点击登录按钮，等待扫码界面...');
              await this.page.waitForTimeout(2000);
              return;
            }
          }
        } catch {
          continue;
        }
      }
      
      console.log('   未找到登录按钮，可能页面已变化');
    } catch (error) {
      console.log('   处理登录按钮时出错:', error);
    }
  }

  /**
   * 检测当前页面是否在登录页面
   */
  isOnLoginPage(): boolean {
    if (!this.page) {
      return false;
    }
    
    const currentUrl = this.page.url();
    
    switch (this.platform) {
      case 'zhihu':
        return currentUrl.includes('signin') || currentUrl.includes('login');
      case 'bilibili':
        return currentUrl.includes('passport');
      case 'baijiahao':
        // 百家号登录检测：URL 包含 login 或者页面中有登录按钮
        if (currentUrl.includes('login')) {
          return true;
        }
        // 异步检查页面元素（简化版，实际检测在 publish 方法中完成）
        return false;
      case 'toutiao':
        return currentUrl.includes('login') || currentUrl.includes('passport');
      case 'xiaohongshu':
        return currentUrl.includes('login') || currentUrl.includes('signup');
      default:
        return false;
    }
  }
  
  /**
   * 异步检测是否在登录页面（通过检查页面元素）
   * 用于百家号等平台，需要检查页面中是否存在登录按钮
   */
  async isOnLoginPageAsync(): Promise<boolean> {
    if (!this.page) {
      return false;
    }
    
    // 先等待页面加载
    await this.page.waitForTimeout(1000);
    
    const currentUrl = this.page.url();
    
    // 先检查 URL
    switch (this.platform) {
      case 'baijiahao':
        if (currentUrl.includes('login')) {
          return true;
        }
        // 检查页面中是否有登录按钮
        try {
          const loginBtnSelectors = [
            '[data-testid="bjh-login-btn"]',
            'button.loginBtn--lZVgU',
            'header button',
            'button:has-text("登录")',
          ];
          
          for (const selector of loginBtnSelectors) {
            const btn = await this.page.$(selector);
            if (btn) {
              const isVisible = await btn.isVisible();
              if (isVisible) {
                return true;
              }
            }
          }
        } catch {
          // 忽略错误
        }
        return false;
        
      default:
        // 其他平台使用同步方法
        return this.isOnLoginPage();
    }
  }

  /**
   * 检测登录是否成功
   * 根据各平台的URL变化和页面特征判断登录状态
   */
  private async checkLoginSuccess(): Promise<boolean> {
    if (!this.page) {
      return false;
    }
    
    const currentUrl = this.page.url();
    
    switch (this.platform) {
      case 'zhihu':
        if (currentUrl.includes('zhihu.com') && 
            !currentUrl.includes('signin') && 
            !currentUrl.includes('login')) {
          try {
            const hasAvatar = await this.page.$('.AppHeader-profile img, .GlobalSideBar-userAvatar, [class*="Avatar"]');
            return hasAvatar !== null;
          } catch {
            return !currentUrl.includes('signin');
          }
        }
        return false;
        
      case 'bilibili':
        if ((currentUrl.includes('bilibili.com') && !currentUrl.includes('passport')) ||
            currentUrl.includes('member.bilibili.com')) {
          return true;
        }
        return false;
        
      case 'baijiahao':
        if (currentUrl.includes('baijiahao.baidu.com') && 
            !currentUrl.includes('login')) {
          try {
            const hasUserAvatar = await this.page.$('.user-avatar, .user-info, [class*="avatar"]');
            return hasUserAvatar !== null;
          } catch {
            return !currentUrl.includes('login');
          }
        }
        return false;
        
      case 'toutiao':
        if (currentUrl.includes('toutiao.com') && 
            !currentUrl.includes('login') && 
            !currentUrl.includes('passport')) {
          try {
            const hasUserAvatar = await this.page.$('.avatar-wrap, .user-avatar, [class*="avatar"]');
            return hasUserAvatar !== null;
          } catch {
            return !currentUrl.includes('login');
          }
        }
        return false;
        
      case 'xiaohongshu':
        if (currentUrl.includes('xiaohongshu.com') && 
            !currentUrl.includes('login') && 
            !currentUrl.includes('signup')) {
          try {
            const hasUserAvatar = await this.page.$('.user-avatar, [class*="avatar"], [class*="user-info"]');
            return hasUserAvatar !== null;
          } catch {
            return !currentUrl.includes('login');
          }
        }
        return false;
        
      default:
        return false;
    }
  }

  /**
   * 等待登录成功
   * 使用轮询机制检测登录状态
   */
  async waitForLogin(timeout: number = 120000): Promise<boolean> {
    if (!this.page) {
      throw new Error('Page not initialized');
    }

    const platformInfo = PLATFORMS[this.platform];
    const checkInterval = 2000;
    const startTime = Date.now();
    
    console.log(`⏳ 等待 ${platformInfo.displayName} 登录...（超时时间: ${timeout / 1000}秒）`);
    
    let dots = 0;
    while (Date.now() - startTime < timeout) {
      const isLoggedIn = await this.checkLoginSuccess();
      
      if (isLoggedIn) {
        console.log('');
        console.log('✅ 检测到登录成功！');
        await this.saveCookies();
        return true;
      }
      
      dots = (dots + 1) % 4;
      const dotsStr = '.'.repeat(dots);
      process.stdout.write(`\r🔍 检测登录状态中${dotsStr}   `);
      
      await this.page.waitForTimeout(checkInterval);
    }
    
    console.log('');
    return false;
  }

  /**
   * 检查是否已登录（通过访问发布页面检测）
   */
  async checkLoginStatus(): Promise<boolean> {
    if (!this.page) {
      return false;
    }

    const platformInfo = PLATFORMS[this.platform];
    
    try {
      await this.page.goto(platformInfo.publishUrl, { 
        waitUntil: 'domcontentloaded',
        timeout: 30000
      });
      
      await this.page.waitForTimeout(2000);
      
      const currentUrl = this.page.url();
      
      if (currentUrl.includes('login') || currentUrl.includes('signin')) {
        return false;
      }
      
      return true;
    } catch (error) {
      console.error('Failed to check login status:', error);
      return false;
    }
  }

  /**
   * 关闭浏览器
   */
  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.context = null;
      this.page = null;
    }
  }

  /**
   * 截图
   */
  async screenshot(path: string): Promise<void> {
    if (!this.page) {
      throw new Error('Page not initialized');
    }
    await this.page.screenshot({ path, fullPage: true });
  }
}
