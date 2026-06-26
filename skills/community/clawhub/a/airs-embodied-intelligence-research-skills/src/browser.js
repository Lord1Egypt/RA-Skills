import puppeteer from 'puppeteer-core';
import { logger } from './utils/logger.js';

/**
 * 连接到已运行的 Chrome 浏览器（需要以 --remote-debugging-port=9222 启动）
 * 
 * 启动命令:
 * /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
 */
export async function connectBrowser() {
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null,
    });
    logger.info('成功连接到 Chrome 浏览器');
    return browser;
  } catch (err) {
    logger.error('无法连接 Chrome。请确保已用以下命令启动:');
    logger.error('/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222');
    throw err;
  }
}

/**
 * 在浏览器中打开新标签页
 */
export async function openNewPage(browser) {
  const page = await browser.newPage();
  // 设置较长的超时时间
  page.setDefaultTimeout(30000);
  page.setDefaultNavigationTimeout(30000);
  return page;
}

/**
 * 安全等待 - 随机延迟避免反爬
 */
export function delay(minMs = 2000, maxMs = 5000) {
  const ms = Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs;
  return new Promise(resolve => setTimeout(resolve, ms));
}
