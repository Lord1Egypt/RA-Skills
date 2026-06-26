import { BrowserContext, Page } from 'playwright';
import { AuthState } from '../types/index.js';
import fs from 'fs-extra';
import path from 'path';

export class AuthManager {
  private context: BrowserContext;
  private dataDir: string;

  constructor(context: BrowserContext, dataDir: string) {
    this.context = context;
    this.dataDir = dataDir;
  }

  async saveCookies(platform: string): Promise<void> {
    const cookies = await this.context.cookies();
    const authState: AuthState = {
      cookies,
      lastRefreshed: Date.now()
    };

    const cookieDir = path.join(this.dataDir, 'cookies');
    await fs.ensureDir(cookieDir);
    
    const cookieFile = path.join(cookieDir, `${platform}.json`);
    await fs.writeFile(cookieFile, JSON.stringify(authState, null, 2));
  }

  async loadCookies(platform: string): Promise<boolean> {
    const cookieFile = path.join(this.dataDir, 'cookies', `${platform}.json`);
    
    if (!(await fs.pathExists(cookieFile))) {
      return false;
    }

    try {
      const content = await fs.readFile(cookieFile, 'utf-8');
      const authState: AuthState = JSON.parse(content);
      
      // Check if cookies are too old (30 days)
      const maxAge = 30 * 24 * 60 * 60 * 1000;
      if (Date.now() - authState.lastRefreshed > maxAge) {
        console.log(`⚠️  ${platform} cookies 已过期 (>30天)`);
        return false;
      }

      await this.context.addCookies(authState.cookies);
      return true;
    } catch (error) {
      console.error(`Failed to load cookies for ${platform}:`, error);
      return false;
    }
  }

  async clearCookies(platform: string): Promise<void> {
    const cookieFile = path.join(this.dataDir, 'cookies', `${platform}.json`);
    try {
      await fs.unlink(cookieFile);
    } catch (e) {
      // File doesn't exist, ignore
    }
  }

  async performQRLogin(page: Page, platform: string, loginUrl: string): Promise<boolean> {
    console.log(`\n📱 ${platform} 需要登录`);
    console.log(`正在打开登录页面，请扫描二维码...\n`);

    await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // Wait for QR code to appear
    await page.waitForTimeout(2000);

    // Take screenshot of QR code area if possible
    try {
      const qrSelector = 'canvas, img[src*="qr"], .qrcode, [class*="qr"], [class*="scan"]'
      const qrElement = await page.$(qrSelector);
      if (qrElement) {
        const screenshotPath = `${this.dataDir}/${platform}-qr.png`;
        await qrElement.screenshot({ path: screenshotPath });
        console.log(`✅ 二维码已保存: ${screenshotPath}`);
      }
    } catch (e) {
      // Screenshot failed, but continue anyway
    }

    console.log('请在打开的浏览器窗口中完成扫码登录');
    console.log('等待登录完成... (超时: 120秒)\n');

    // Wait for login success - check URL change or specific element
    const startTime = Date.now();
    const timeout = 120000; // 2 minutes

    while (Date.now() - startTime < timeout) {
      await page.waitForTimeout(2000);
      
      const url = page.url();
      console.log(`  [DEBUG] Current URL: ${url}`);
      
      // Check if we're on a login page (not just URL contains 'login')
      const isLoginPath = 
        url.includes('/login') || 
        url.includes('/signin') ||
        url.includes('sso.') ||
        url.includes('passport.');
      
      // For PDD, index.html with refer_page_name=login means logged in
      const isPDDLoggedIn = platform === 'pdd' && 
        url.includes('index.html') && 
        url.includes('refer_page_name=login');
      
      const isStillOnLoginPage = isLoginPath && !isPDDLoggedIn;

      if (!isStillOnLoginPage) {
        console.log(`✅ ${platform} 登录成功! (URL changed)`);
        await this.saveCookies(platform);
        return true;
      }

      // Check for logged-in indicator
      const hasUserElement = await page.$('.user-name, .nickname, [class*="user"], [class*="avatar"], .user-info, .member-info').catch(() => null);
      if (hasUserElement) {
        console.log(`✅ ${platform} 登录成功! (User element found)`);
        await this.saveCookies(platform);
        return true;
      }
      
      // Check for PDD specific logged-in indicators
      if (platform === 'pdd') {
        const hasPDDUser = await page.$('[data-testid="user-avatar"], .user-avatar, .personal-center').catch(() => null);
        if (hasPDDUser) {
          console.log(`✅ ${platform} 登录成功! (PDD user element found)`);
          await this.saveCookies(platform);
          return true;
        }
      }
    }

    console.error(`❌ ${platform} 登录超时，请重试`);
    return false;
  }
}