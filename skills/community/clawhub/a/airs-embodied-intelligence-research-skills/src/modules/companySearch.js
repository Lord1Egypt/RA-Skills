import { delay } from '../browser.js';
import { logger } from '../utils/logger.js';
import { withRetry } from '../utils/retry.js';

/**
 * 在天眼查搜索企业名称，获取全称和链接
 * @param {import('puppeteer-core').Page} page 
 * @param {string} companyName - 企业简称
 * @returns {Promise<{fullName: string, url: string, status: string}>}
 */
export async function searchCompanyOnTianyancha(page, companyName) {
  return withRetry(async () => {
    // 访问天眼查搜索页
    const searchUrl = `https://www.tianyancha.com/search?key=${encodeURIComponent(companyName)}`;
    logger.info(`搜索企业: ${companyName} → ${searchUrl}`);
    
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    await delay(2000, 4000);

    // 检查是否有验证码
    const needVerify = await page.evaluate(() => {
      return !!document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
    }).catch(() => false);

    if (needVerify) {
      logger.warn(`⚠️ 搜索 "${companyName}" 时出现验证码，请手动处理...`);
      // 等待验证码消失 (最多2分钟)
      await page.waitForFunction(() => {
        const el = document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
        return !el;
      }, { timeout: 120000 }).catch(() => {});
      await delay(1000, 2000);
    }

    // 获取搜索结果列表中的第一个企业
    const result = await page.evaluate(() => {
      // 天眼查搜索结果的选择器 - 多种可能的选择器
      const selectors = [
        '.search-result-single .header a[href*="/company/"]',
        '.result-list .search-result-single .header a',
        '.search_result_single .header a[href*="/company/"]',
        'a[href*="/company/"].name',
        '.result-list a[href*="/company/"]',
      ];
      
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          return {
            fullName: el.textContent.replace(/<[^>]+>/g, '').trim(),
            url: el.href,
          };
        }
      }
      
      // 尝试更宽泛的匹配
      const allLinks = document.querySelectorAll('a[href*="/company/"]');
      for (const link of allLinks) {
        const text = link.textContent.trim();
        if (text.length > 2 && text.length < 50) {
          return {
            fullName: text,
            url: link.href,
          };
        }
      }
      
      return null;
    });

    if (!result) {
      logger.warn(`未找到企业 "${companyName}" 的搜索结果`);
      return { fullName: '', url: '', status: '未找到' };
    }

    // 清理全称中可能的 HTML 标签残留
    const cleanName = result.fullName
      .replace(/<[^>]+>/g, '')
      .replace(/\s+/g, '')
      .trim();

    logger.info(`✅ ${companyName} → ${cleanName}`);
    
    return {
      fullName: cleanName,
      url: result.url,
      status: '已确认',
    };
  }, { maxRetries: 2, delayMs: 5000, label: `搜索${companyName}` });
}
