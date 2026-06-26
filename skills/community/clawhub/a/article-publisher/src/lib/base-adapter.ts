import { BrowserManager } from './browser-manager.js';
import { CookieManager } from './cookie-manager.js';
import { PlatformName, PlatformInfo, ArticleContent, PublishResult, PLATFORMS } from '../types/index.js';

/**
 * 平台适配器基类
 */
export abstract class BaseAdapter {
  protected platform: PlatformName;
  protected platformInfo: PlatformInfo;
  protected browserManager: BrowserManager;
  protected cookieManager: CookieManager;

  constructor(platform: PlatformName) {
    this.platform = platform;
    this.platformInfo = PLATFORMS[platform];
    this.browserManager = new BrowserManager(platform);
    this.cookieManager = new CookieManager(platform);
  }

  /**
   * 获取平台名称
   */
  getPlatformName(): PlatformName {
    return this.platform;
  }

  /**
   * 获取平台显示名称
   */
  getDisplayName(): string {
    return this.platformInfo.displayName;
  }

  /**
   * 打开登录页面
   */
  async openLoginPage(): Promise<string> {
    await this.browserManager.launch();
    await this.browserManager.gotoLoginPage();
    return `请在打开的浏览器中扫码登录${this.platformInfo.displayName}，登录成功后将自动保存登录状态。`;
  }

  /**
   * 等待登录完成
   */
  async waitForLogin(timeout?: number): Promise<boolean> {
    const success = await this.browserManager.waitForLogin(timeout);
    if (success) {
      await this.browserManager.close();
    }
    return success;
  }

  /**
   * 检查登录状态
   */
  async checkLoginStatus(): Promise<boolean> {
    const hasCookies = await this.cookieManager.hasValidCookies();
    if (!hasCookies) {
      return false;
    }

    try {
      await this.browserManager.launch();
      const isLoggedIn = await this.browserManager.checkLoginStatus();
      await this.browserManager.close();
      return isLoggedIn;
    } catch (error) {
      await this.browserManager.close();
      return false;
    }
  }

  /**
   * 清除登录状态
   */
  async logout(): Promise<void> {
    await this.cookieManager.clearCookies();
  }

  /**
   * 发布文章 - 子类必须实现
   * @param article 文章内容
   * @param testMode 测试模式，为true时不点击发布按钮
   */
  abstract publish(article: ArticleContent, testMode?: boolean): Promise<PublishResult>;

  /**
   * 填充文章标题
   */
  protected async fillTitle(title: string): Promise<void> {
    throw new Error('fillTitle must be implemented by subclass');
  }

  /**
   * 填充文章内容
   */
  protected async fillContent(content: string): Promise<void> {
    throw new Error('fillContent must be implemented by subclass');
  }

  /**
   * 上传封面图片
   */
  protected async uploadCover(imagePath: string): Promise<void> {
    throw new Error('uploadCover must be implemented by subclass');
  }

  /**
   * 设置标签
   */
  protected async setTags(tags: string[]): Promise<void> {
    throw new Error('setTags must be implemented by subclass');
  }

  /**
   * 点击发布按钮
   */
  protected async clickPublish(): Promise<void> {
    throw new Error('clickPublish must be implemented by subclass');
  }

  /**
   * 获取发布后的文章链接
   */
  protected async getArticleUrl(): Promise<string | null> {
    throw new Error('getArticleUrl must be implemented by subclass');
  }

  /**
   * 截图保存当前页面状态
   */
  async screenshot(path: string): Promise<void> {
    await this.browserManager.screenshot(path);
  }
}
