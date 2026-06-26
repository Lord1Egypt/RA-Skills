import { Platform, OrderLogistics, QueryOptions } from '../types/index.js';
import { TaobaoAdapter } from '../adapters/taobao-adapter.js';
import { JDAdapter } from '../adapters/jd-adapter.js';
import { PDDAdapter } from '../adapters/pdd-adapter.js';
import { DouyinAdapter } from '../adapters/douyin-adapter.js';
import { BaseAdapter } from '../adapters/base-adapter.js';
import { StealthBrowser } from './stealth-browser.js';
import { AuthManager } from './auth-manager.js';
import { RateLimiter } from './rate-limiter.js';
import chalk from 'chalk';

export class LogisticsAggregator {
  private browser: StealthBrowser;
  private rateLimiter: RateLimiter;
  private options: QueryOptions;
  private adapters: Map<Platform, BaseAdapter> = new Map();

  constructor(options: QueryOptions) {
    this.options = options;
    this.browser = new StealthBrowser(options.dataDir);
    this.rateLimiter = new RateLimiter();
  }

  async initialize(): Promise<void> {
    await this.browser.launch(this.options.headless !== false);
  }

  async queryAll(): Promise<Map<Platform, OrderLogistics[]>> {
    const platforms: Platform[] = ['taobao', 'jd', 'pdd', 'douyin'];
    const results = new Map<Platform, OrderLogistics[]>();

    for (const platform of platforms) {
      try {
        const orders = await this.queryPlatform(platform);
        results.set(platform, orders);
      } catch (error: any) {
        if (error.message === 'LOGIN_REQUIRED') {
          console.log(chalk.yellow(`\n⚠️  ${platform} Cookie 已过期，需要重新登录`));
          console.log(chalk.cyan(`请运行: npm run login -- --platform ${platform}\n`));
        } else {
          console.error(chalk.red(`\n❌ 查询 ${platform} 失败:`), error.message);
        }
        results.set(platform, []);
      }
    }

    return results;
  }

  async queryPlatform(platform: Platform): Promise<OrderLogistics[]> {
    await this.rateLimiter.waitForSlot(platform);

    const context = await this.browser.getContext(platform);
    const authManager = new AuthManager(context, this.options.dataDir);

    // Try to load existing cookies
    const hasCookies = await authManager.loadCookies(platform);
    if (!hasCookies) {
      throw new Error('LOGIN_REQUIRED');
    }

    // Get or create adapter
    let adapter = this.adapters.get(platform);
    if (!adapter) {
      switch (platform) {
        case 'taobao':
          adapter = new TaobaoAdapter(context);
          break;
        case 'jd':
          adapter = new JDAdapter(context);
          break;
        case 'pdd':
          adapter = new PDDAdapter(context);
          break;
        case 'douyin':
          adapter = new DouyinAdapter(context);
          break;
      }
      this.adapters.set(platform, adapter);
    }

    // Check if still logged in
    const isLoggedIn = await adapter.isLoggedIn();
    if (!isLoggedIn) {
      throw new Error('LOGIN_REQUIRED');
    }

    console.log(chalk.blue(`\n🔍 正在查询 ${adapter.getName()}...`));
    const orders = await adapter.getOrders();
    console.log(chalk.green(`✅ ${adapter.getName()}: 找到 ${orders.length} 个订单`));

    return orders;
  }

  async loginPlatform(platform: Platform): Promise<boolean> {
    const context = await this.browser.getContext(platform);
    const authManager = new AuthManager(context, this.options.dataDir);
    const page = await context.newPage();

    let loginUrl: string;
    switch (platform) {
      case 'taobao':
        loginUrl = 'https://login.taobao.com';
        break;
      case 'jd':
        loginUrl = 'https://passport.jd.com/login.aspx';
        break;
      case 'pdd':
        loginUrl = 'https://mobile.yangkeduo.com/login.html';
        break;
      case 'douyin':
        loginUrl = 'https://sso.douyin.com/login';
        break;
    }

    const success = await authManager.performQRLogin(page, platform, loginUrl);
    await page.close();
    return success;
  }

  async close(): Promise<void> {
    for (const adapter of this.adapters.values()) {
      await adapter.close();
    }
    await this.browser.close();
  }
}