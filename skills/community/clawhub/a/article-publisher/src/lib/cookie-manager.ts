import fs from 'fs';
import path from 'path';
import { CookieData, PlatformName } from '../types/index.js';
import { getCookiePath, ensureCookieDir, getConfig } from './config.js';

/**
 * Cookie管理器
 */
export class CookieManager {
  private platform: PlatformName;

  constructor(platform: PlatformName) {
    this.platform = platform;
  }

  /**
   * 保存Cookie
   */
  async saveCookies(cookies: CookieData['cookies']): Promise<void> {
    ensureCookieDir();
    const config = getConfig();
    const now = new Date();
    const expiresAt = new Date(now.getTime() + config.cookieExpiryDays * 24 * 60 * 60 * 1000);

    const cookieData: CookieData = {
      cookies,
      createdAt: now.toISOString(),
      expiresAt: expiresAt.toISOString(),
    };

    const cookiePath = getCookiePath(this.platform);
    fs.writeFileSync(cookiePath, JSON.stringify(cookieData, null, 2), 'utf-8');
  }

  /**
   * 读取Cookie
   */
  async loadCookies(): Promise<CookieData | null> {
    const cookiePath = getCookiePath(this.platform);
    
    if (!fs.existsSync(cookiePath)) {
      return null;
    }

    try {
      const content = fs.readFileSync(cookiePath, 'utf-8');
      const cookieData: CookieData = JSON.parse(content);
      
      if (this.isExpired(cookieData)) {
        await this.clearCookies();
        return null;
      }

      return cookieData;
    } catch (error) {
      console.error(`Failed to load cookies for ${this.platform}:`, error);
      return null;
    }
  }

  /**
   * 检查Cookie是否过期
   */
  isExpired(cookieData: CookieData): boolean {
    const expiresAt = new Date(cookieData.expiresAt);
    return expiresAt < new Date();
  }

  /**
   * 清除Cookie
   */
  async clearCookies(): Promise<void> {
    const cookiePath = getCookiePath(this.platform);
    
    if (fs.existsSync(cookiePath)) {
      fs.unlinkSync(cookiePath);
    }
  }

  /**
   * 检查是否存在有效的Cookie
   */
  async hasValidCookies(): Promise<boolean> {
    const cookieData = await this.loadCookies();
    return cookieData !== null && !this.isExpired(cookieData);
  }

  /**
   * 获取Cookie创建时间
   */
  async getCookieInfo(): Promise<{ createdAt: Date; expiresAt: Date } | null> {
    const cookieData = await this.loadCookies();
    
    if (!cookieData) {
      return null;
    }

    return {
      createdAt: new Date(cookieData.createdAt),
      expiresAt: new Date(cookieData.expiresAt),
    };
  }
}
