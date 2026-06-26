import { Page, BrowserContext } from 'playwright';
import { OrderLogistics, PlatformConfig, LogisticsStatus } from '../types/index.js';

export abstract class BaseAdapter {
  protected config: PlatformConfig;
  protected context: BrowserContext;
  protected page: Page | null = null;

  constructor(config: PlatformConfig, context: BrowserContext) {
    this.config = config;
    this.context = context;
  }

  abstract getName(): string;
  abstract isLoggedIn(): Promise<boolean>;
  abstract getOrders(): Promise<OrderLogistics[]>;
  abstract getOrderLogistics(orderId: string): Promise<OrderLogistics | null>;

  protected async initPage(): Promise<Page> {
    if (!this.page) {
      this.page = await this.context.newPage();
      await this.setupStealth(this.page);
    }
    return this.page;
  }

  protected async setupStealth(page: Page): Promise<void> {
    // Override navigator.webdriver
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });
      
      Object.defineProperty(navigator, 'plugins', {
        get: () => [
          { name: 'Chrome PDF Plugin' },
          { name: 'Chrome PDF Viewer' },
          { name: 'Native Client' }
        ]
      });

      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters: any) =>
        parameters.name === 'notifications'
          ? Promise.resolve({ state: Notification.permission } as PermissionStatus)
          : originalQuery(parameters);
    });

    // Set realistic viewport and user agent
    await page.setViewportSize({ width: 1920, height: 1080 });
  }

  protected async detectLoginPage(page: Page): Promise<boolean> {
    const url = page.url();
    const hasLoginIndicator = await page.locator(this.config.selectors.loginIndicator).count() > 0;
    return hasLoginIndicator || this.isLoginUrl(url);
  }

  protected abstract isLoginUrl(url: string): boolean;

  protected parseStatus(statusText: string): LogisticsStatus {
    const text = statusText.toLowerCase();
    if (text.includes('签收') || text.includes('完成') || text.includes('delivered')) {
      return 'delivered';
    }
    if (text.includes('派送') || text.includes('配送') || text.includes('out for delivery')) {
      return 'out_for_delivery';
    }
    if (text.includes('运输') || text.includes('中转') || text.includes('in transit')) {
      return 'in_transit';
    }
    if (text.includes('发货') || text.includes('shipped')) {
      return 'shipped';
    }
    if (text.includes('异常') || text.includes('exception') || text.includes('拒收')) {
      return 'exception';
    }
    if (text.includes('取消') || text.includes('cancelled')) {
      return 'cancelled';
    }
    return 'pending';
  }

  protected async safeGoto(url: string, options?: { timeout?: number; waitUntil?: any }): Promise<boolean> {
    const page = await this.initPage();
    try {
      await page.goto(url, {
        timeout: options?.timeout || 30000,
        waitUntil: options?.waitUntil || 'networkidle'
      });
      
      // Check if redirected to login
      if (await this.detectLoginPage(page)) {
        throw new Error('LOGIN_REQUIRED');
      }
      
      return true;
    } catch (error: any) {
      if (error.message === 'LOGIN_REQUIRED') {
        throw error;
      }
      throw new Error(`Navigation failed: ${error.message}`);
    }
  }

  async close(): Promise<void> {
    if (this.page) {
      await this.page.close();
      this.page = null;
    }
  }
}