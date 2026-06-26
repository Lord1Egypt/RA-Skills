import { delay } from '../browser.js';
import { logger } from '../utils/logger.js';
import { withRetry } from '../utils/retry.js';

/**
 * 使用天眼查招投标搜索页面获取记录
 * 
 * 流程:
 * 1. 访问 https://www.tianyancha.com/s/toubiao
 * 2. 在中间大搜索框输入企业全称
 * 3. 点击"天眼一下"按钮，跳转到 detail 页面
 * 4. 在 detail 页面使用 CSS 筛选器过滤: 公告类型=中标公告, 发布时间=近3个月
 * 5. 抓取搜索结果列表
 * 6. 数据去重：同一标题+日期的记录只保留一条
 * 
 * @param {import('puppeteer-core').Page} page
 * @param {string} companyUrl - 企业天眼查页面 URL（用于获取公司ID）
 * @param {string} companyName - 企业全称（Step1结果中的）
 * @param {Object} options
 * @param {string} options.startDate - 开始日期 (格式: YYYY-MM-DD)
 * @param {string} options.endDate - 结束日期 (格式: YYYY-MM-DD)
 * @param {number} options.minAmount - 最低金额（万元），0表示无门槛
 * @returns {Promise<Array>} 招投标记录列表
 */
export async function downloadBiddingRecords(page, companyUrl, companyName, options = {}) {
  const {
    startDate = '2026-01-01',
    endDate = '2026-03-31',
    minAmount = 0,
    useRecentDays = false  // 是否使用近7天筛选，默认否
  } = options;
  
  // 解析日期
  const startTimestamp = new Date(startDate).getTime();
  const endTimestamp = new Date(endDate).getTime();
  
  return withRetry(async () => {
    logger.info(`获取 "${companyName}" 的招投标记录...`);
    
    // 访问招投标搜索页面
    const searchUrl = 'https://www.tianyancha.com/s/toubiao';
    logger.info(`  访问搜索页面: ${searchUrl}`);
    
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    await delay(5000, 8000);

    // 检查验证码
    const needVerify = await page.evaluate(() => {
      return !!document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
    }).catch(() => false);

    if (needVerify) {
      logger.warn(`⚠️ 出现验证码，请手动处理...`);
      await page.waitForFunction(() => {
        return !document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
      }, { timeout: 120000 }).catch(() => {});
      await delay(3000, 5000);
    }

    // 使用 Puppeteer 原生方法操作搜索框和按钮
    try {
      // 等待搜索框出现
      await page.waitForSelector('#seo_seach_input, input[placeholder*="公司名称"]', { timeout: 10000 });
      
      // 清空并输入企业名称
      const searchInput = await page.$('#seo_seach_input') || await page.$('input[placeholder*="公司名称"]');
      if (!searchInput) {
        throw new Error('未找到搜索框');
      }
      
      await searchInput.click();
      await searchInput.evaluate(el => el.value = '');  // 清空
      await searchInput.type(companyName, { delay: 50 });
      logger.info(`  输入企业名称: ${companyName}`);
      
      await delay(1500, 2500);
      
      // 点击"天眼一下"按钮 - 使用精确的选择器
      const btnSelectors = [
        '.input-group-btn.btn.-h52.btn-primary',
        '.btn-primary.input-group-btn',
        '.input-group-btn.btn-primary',
        'div.btn-primary',
        'button.btn-primary'
      ];
      
      let btnClicked = false;
      for (const selector of btnSelectors) {
        const btn = await page.$(selector);
        if (btn) {
          const text = await btn.evaluate(el => el.textContent.trim());
          if (text === '天眼一下' || text.includes('天眼一下')) {
            await btn.click();
            logger.info(`  点击按钮: ${text} (${selector})`);
            btnClicked = true;
            break;
          }
        }
      }
      
      if (!btnClicked) {
        // 备选：查找 y 坐标约 383 的按钮
        const btn = await page.evaluateHandle(() => {
          const buttons = document.querySelectorAll('div, button');
          for (const btn of buttons) {
            const rect = btn.getBoundingClientRect();
            if (rect.y > 350 && rect.y < 450 && 
                rect.x > 800 && 
                btn.textContent.trim() === '天眼一下') {
              return btn;
            }
          }
          return null;
        });
        
        if (btn) {
          await btn.click();
          logger.info('  点击按钮 (坐标查找)');
          btnClicked = true;
        }
      }
      
      if (!btnClicked) {
        // 最后备选：回车
        await searchInput.press('Enter');
        logger.info('  按回车搜索');
      }
      
    } catch (err) {
      logger.warn(`  操作搜索框失败: ${err.message}，尝试备用方法...`);
      // 备用：使用 page.evaluate
      await page.evaluate((name) => {
        const input = document.querySelector('#seo_seach_input');
        if (input) {
          input.value = name;
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
      }, companyName);
      await delay(1000, 2000);
      await page.evaluate(() => {
        const btn = document.querySelector('.input-group-btn.btn.-h52.btn-primary');
        if (btn) btn.click();
      });
    }

    // 等待搜索结果加载 - 页面会跳转到 detail 页面
    logger.info('  等待搜索结果...');
    await delay(5000, 8000);
    
    // 检查 URL 是否变化（跳转到 detail 页面）
    const currentUrl = await page.url();
    logger.info(`  当前URL: ${currentUrl}`);
    
    // 如果还在搜索页面，可能没有结果，直接返回
    if (currentUrl.includes('/s/toubiao') && !currentUrl.includes('detail')) {
      logger.info('  未跳转到详情页，可能无搜索结果');
      return [];
    }
    
    // ===== 使用 CSS 筛选器过滤 =====
    const timeFilterText = useRecentDays ? '近7天' : '近3个月';
    logger.info(`  应用筛选器: 公告类型=中标公告, 发布时间=${timeFilterText}...`);

    try {
      // 等待筛选器加载
      await delay(2000, 3000);

      // 点击"公告类型"筛选 - 选择"中标公告"
      const typeFilterClicked = await page.evaluate(() => {
        // 查找包含"中标公告"的按钮/选项
        const allElements = document.querySelectorAll('button, a, span, div, li');
        for (const el of allElements) {
          const text = el.textContent.trim();
          // 找到"中标公告"按钮，且不是已选中状态
          if (text === '中标公告' && !el.classList.contains('active') && !el.classList.contains('selected')) {
            el.click();
            return { success: true, text: text, className: el.className };
          }
        }
        return { success: false, reason: '未找到中标公告按钮' };
      });

      if (typeFilterClicked.success) {
        logger.info(`    ✅ 已选择公告类型: 中标公告 (${typeFilterClicked.className?.substring(0, 50)})`);
        await delay(2000, 3000);
      } else {
        logger.info(`    ⚪ 公告类型筛选: ${typeFilterClicked.reason}`);
      }

      // 点击"发布时间"筛选 - 选择近7天或近3个月
      const timeFilterClicked = await page.evaluate((isRecent) => {
        const allElements = document.querySelectorAll('button, a, span, div, li');
        for (const el of allElements) {
          const text = el.textContent.trim();
          // 根据需要查找对应的按钮
          const targetTexts = isRecent ? ['近7天', '近七天', '7天内'] : ['近3个月', '近三月', '3个月内'];
          if (targetTexts.some(t => t === text) &&
              !el.classList.contains('active') && !el.classList.contains('selected')) {
            el.click();
            return { success: true, text: text, className: el.className };
          }
        }
        return { success: false, reason: `未找到${isRecent ? '近7天' : '近3个月'}按钮` };
      }, useRecentDays);

      if (timeFilterClicked.success) {
        logger.info(`    ✅ 已选择发布时间: ${timeFilterClicked.text} (${timeFilterClicked.className?.substring(0, 50)})`);
        await delay(2000, 3000);
      } else {
        logger.info(`    ⚪ 时间筛选: ${timeFilterClicked.reason}`);
      }
      
    } catch (err) {
      logger.warn(`  应用筛选器时出错: ${err.message}`);
    }
    
    // 等待列表刷新
    logger.info('  等待筛选后列表加载...');
    try {
      await page.waitForFunction(() => {
        const items = document.querySelectorAll('[class*="index_item__"]');
        return items.length > 0;
      }, { timeout: 15000 });
      logger.info('  列表已加载');
    } catch (e) {
      logger.warn('  等待列表超时，继续尝试...');
    }

    // 抓取所有页的招投标记录
    const allRecords = [];
    let pageNum = 1;
    let hasMore = true;

    while (hasMore) {
      logger.info(`  第 ${pageNum} 页...`);
      
      // 等待列表加载
      await delay(3000, 5000);
      
      // 抓取当前页的记录 - 只抓取中标公告
      const pageRecords = await page.evaluate(() => {
        const records = [];
        
        // ===== 从 __NEXT_DATA__ 解析详情链接 =====
        const titleLinkMap = new Map();
        try {
          const nextDataEl = document.getElementById('__NEXT_DATA__');
          if (nextDataEl) {
            const data = JSON.parse(nextDataEl.textContent);
            const queries = data?.props?.pageProps?.dehydratedState?.queries || [];
            
            for (const query of queries) {
              const items = query?.state?.data?.data?.items || [];
              for (const item of items) {
                if (item.title && item.detailUrl) {
                  titleLinkMap.set(item.title.trim(), item.detailUrl);
                }
              }
            }
          }
        } catch (e) {
          // JSON 解析失败，忽略
        }
        
        // ===== 遍历所有列表项提取信息 =====
        const items = document.querySelectorAll('[class*="index_item__"]');
        
        for (const item of items) {
          const fullText = item.textContent;
          
          // 筛选：只保留包含"中标公告"的项目
          if (!fullText.includes('中标公告')) {
            continue;
          }
          
          // ===== 提取标题 =====
          const titleEl = item.querySelector('[class*="index_item-header__"]');
          let title = '';
          
          if (titleEl) {
            title = titleEl.textContent.trim();
          }
          
          // 备用方法提取标题
          if (!title || title.length < 5) {
            const titleMatch = fullText.match(/^(.+?)(发布时间|中标公告)/);
            title = titleMatch ? titleMatch[1].trim() : '';
          }
          
          if (!title || title.length < 5 || title === '中标公告') {
            const textLines = fullText.split(/\n|\s{2,}/).filter(t => {
              const trimmed = t.trim();
              return trimmed.length > 5 && 
                     trimmed !== '中标公告' && 
                     !trimmed.startsWith('发布时间') &&
                     !trimmed.startsWith('招采单位') &&
                     !trimmed.startsWith('中标金额');
            });
            if (textLines.length > 0) {
              title = textLines[0].trim().substring(0, 150);
            }
          }
          
          // 过滤掉无效内容
          if (!title || 
              title.length < 5 || 
              title.includes('报告') || 
              title.includes('Excel') ||
              title === '发布时间' ||
              title === '中标公告' ||
              title.startsWith('发布时间：') ||
              title.startsWith('招采单位：') ||
              title.startsWith('中标金额：')) {
            continue;
          }
          
          // ===== 提取日期 =====
          const dateMatch = fullText.match(/发布时间[：:]?\s*(\d{4}-\d{2}-\d{2})/);
          const date = dateMatch ? dateMatch[1] : '';
          
          // ===== 提取金额 =====
          const amountMatch = fullText.match(/中标金额[：:]?\s*([\d,.]+\s*[万亿]?元)/);
          const amount = amountMatch ? amountMatch[1] : '';
          
          // ===== 提取招采单位 =====
          const buyerMatch = fullText.match(/招采单位[：:]?\s*([^标书\n]+)/);
          let buyer = buyerMatch ? buyerMatch[1].trim() : '';
          buyer = buyer.replace(/标书.*$/, '').trim();
          
          // ===== 提取详情页链接 =====
          let detailLink = titleLinkMap.get(title) || '';
          
          // 如果 __NEXT_DATA__ 中没有链接，尝试从 DOM 中的链接元素提取
          if (!detailLink) {
            const linkEl = item.querySelector('a[href*="/sub-details/bidInfo/"]');
            if (linkEl) {
              detailLink = linkEl.href || '';
            }
          }
          
          // 清理链接：去掉 ?cname= 及其后面的参数，保持链接简洁
          if (detailLink) {
            // 移除 URL 中 ? 及其后面的查询参数
            detailLink = detailLink.split('?')[0];
          }
          
          records.push({
            title: title,
            link: detailLink,
            buyer: buyer,
            amount: amount,
            date: date,
            type: '中标公告',
          });
        }
        
        return records;
      });

      // ===== 数据去重 =====
      // 使用标题+日期作为唯一键，同时清理相似标题
      const newRecords = pageRecords.filter(r => {
        // 生成唯一键：标题（去除空格和标点）+ 日期
        const normalizedTitle = r.title.replace(/[\s\p{P}]/gu, '').toLowerCase();
        const uniqueKey = `${normalizedTitle}_${r.date}`;
        
        // 检查是否已存在相同或相似记录
        const isDuplicate = allRecords.some(existing => {
          // 完全匹配
          if (existing.title === r.title && existing.date === r.date) {
            return true;
          }
          // 规范化后匹配
          const existingNormalized = existing.title.replace(/[\s\p{P}]/gu, '').toLowerCase();
          if (existingNormalized === normalizedTitle && existing.date === r.date) {
            return true;
          }
          // 相似度检查（标题相似度>80%且日期相同）
          if (existing.date === r.date) {
            const longer = Math.max(existing.title.length, r.title.length);
            const shorter = Math.min(existing.title.length, r.title.length);
            if (shorter / longer > 0.8 && existing.title.substring(0, 20) === r.title.substring(0, 20)) {
              return true;
            }
          }
          return false;
        });
        
        return !isDuplicate;
      });
      
      allRecords.push(...newRecords);
      logger.info(`    本页抓取 ${pageRecords.length} 条，去重后新增 ${newRecords.length} 条，累计 ${allRecords.length} 条`);

      // 检查是否有下一页
      hasMore = await page.evaluate(() => {
        const nextBtns = document.querySelectorAll(
          '.pagination .next:not(.disabled):not([disabled]), ' +
          'button.next:not([disabled]), ' +
          'a.next:not(.disabled), ' +
          '.ant-pagination-next:not(.ant-pagination-disabled), ' +
          '[class*="page-next"]:not(.disabled)'
        );
        for (const btn of nextBtns) {
          if (!btn.disabled && !btn.classList.contains('disabled')) {
            btn.click();
            return true;
          }
        }
        return false;
      });

      if (hasMore) {
        pageNum++;
        await delay(3000, 5000);
        // 安全限制：最多 10 页
        if (pageNum > 10) {
          logger.warn(`  已达 10 页限制，停止翻页`);
          break;
        }
      }
    }

    logger.info(`  共抓取 ${allRecords.length} 条原始记录`);

    // 筛选: 仅保留指定日期范围 + 金额>=minAmount 的记录
    const filtered = allRecords.filter(r => {
      // 日期范围筛选
      if (r.date) {
        const dateStr = r.date.replace(/年|月/g, '-').replace(/日/g, '');
        const recordTimestamp = new Date(dateStr).getTime();
        
        if (!isNaN(recordTimestamp)) {
          if (recordTimestamp < startTimestamp || recordTimestamp > endTimestamp) {
            return false;
          }
        } else {
          // 如果解析失败，尝试年份比较
          const yearMatch = r.date.match(/(\d{4})/);
          if (yearMatch) {
            const recordYear = parseInt(yearMatch[1]);
            const startYear = parseInt(startDate.substring(0, 4));
            if (recordYear < startYear) return false;
          }
        }
      }
      
      // 金额筛选（minAmount为0时不筛选）
      if (minAmount > 0 && r.amount) {
        const numMatch = r.amount.replace(/,/g, '').match(/([\d.]+)/);
        if (numMatch) {
          let amountWan = parseFloat(numMatch[1]);
          if (r.amount.includes('元') && !r.amount.includes('万')) {
            amountWan = amountWan / 10000;
          }
          if (amountWan < minAmount) return false;
        }
      }
      
      return true;
    });

    logger.info(`  筛选后: ${filtered.length} 条 (${startDate} 至 ${endDate}, ${minAmount === 0 ? '无金额门槛' : '≥' + minAmount + '万元'})`);
    
    return filtered.map(r => ({
      ...r,
      companyName,
      companyUrl,
    }));
  }, { maxRetries: 2, delayMs: 5000, label: `下载${companyName}招投标` });
}
