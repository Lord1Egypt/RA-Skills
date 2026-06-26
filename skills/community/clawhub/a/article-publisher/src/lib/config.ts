import path from 'path';
import os from 'os';
import fs from 'fs';

/**
 * 配置接口
 */
export interface Config {
  cookieDir: string;
  cookieExpiryDays: number;
  headless: boolean;
  timeout: number;
  slowMo: number;
}

/**
 * 默认配置
 */
const defaultConfig: Config = {
  cookieDir: path.join(process.cwd(), 'data', 'cookies'),
  cookieExpiryDays: 30,
  headless: false,
  timeout: 60000,
  slowMo: 100,
};

/**
 * 获取配置
 */
export function getConfig(): Config {
  return { ...defaultConfig };
}

/**
 * 获取Cookie文件路径
 */
export function getCookiePath(platform: string): string {
  const config = getConfig();
  return path.join(config.cookieDir, `${platform}_cookies.json`);
}

/**
 * 确保Cookie目录存在
 */
export function ensureCookieDir(): string {
  const config = getConfig();
  if (!fs.existsSync(config.cookieDir)) {
    fs.mkdirSync(config.cookieDir, { recursive: true });
  }
  return config.cookieDir;
}
