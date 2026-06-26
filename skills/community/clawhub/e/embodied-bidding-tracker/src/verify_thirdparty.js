/**
 * Verify: 第三方招投标数据核查
 *
 * 对 Excel 中每条记录，在天眼查招投标搜索页按项目名称搜索，
 * 找到匹配项后访问详情页核对，通过的记录输出标准格式供后续 extract → ingest 使用。
 *
 * 输入: Excel 文件（命令行参数或默认路径）
 * 输出:
 *   data/verify_bidding_records.csv  — 核查通过的记录（格式同 bidding_records.csv）
 *   data/verify_match_report.csv     — 全量核查报告
 *   data/raw_content/*.md            — 通过记录的详情页原文
 *   data/verify_progress.json        — 断点续跑进度
 *
 * 用法:
 *   npm run verify                                  — 使用默认 Excel 文件
 *   npm run verify -- path/to/other.xlsx            — 指定 Excel 文件
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { connectBrowser, openNewPage, delay } from './browser.js';
import { fetchBiddingDetail } from './modules/deepVerify.js';
import { readExcel, writeCsv } from './utils/excel.js';
import { logger } from './utils/logger.js';
import { withRetry } from './utils/retry.js';
import {
  parseAmountYuan,
  matchSearchResult,
  verifyDetail,
  filterResultsByYear,
  entityMatch,
  compareAmount,
} from './modules/fuzzyMatch.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');

// 默认 Excel 文件路径
const DEFAULT_EXCEL = path.join(projectRoot, '2025年全国具身智能机器人企业订单_数据表.xlsx');

// 输出路径
const VERIFY_BIDDING_CSV = path.join(projectRoot, 'data', 'verify_bidding_records.csv');
const VERIFY_REPORT_CSV  = path.join(projectRoot, 'data', 'verify_match_report.csv');
const RAW_CONTENT_DIR    = path.join(projectRoot, 'data', 'raw_content');
const PROGRESS_FILE      = path.join(projectRoot, 'data', 'verify_progress.json');
const VERIFY_TARGET_YEAR = 2025;
const VERIFY_SEARCH_MAX_PAGES = 6;
const VERIFY_MATCH_THRESHOLD = 55;

// CSV 表头：核查通过的记录（格式同 bidding_records.csv）
const BIDDING_HEADERS = [
  { id: 'companyName',  title: '企业名称' },
  { id: 'projectName',  title: '项目名称' },
  { id: 'type',         title: '公告类型' },
  { id: 'buyer',        title: '采购人' },
  { id: 'amount',       title: '中标金额' },
  { id: 'date',         title: '发布日期' },
  { id: 'link',         title: '天眼查详情页链接' },
];

// CSV 表头：全量核查报告
const REPORT_HEADERS = [
  { id: 'index',             title: '序号' },
  { id: 'excelBuyer',        title: '采购单位(Excel)' },
  { id: 'excelProject',      title: '项目名称(Excel)' },
  { id: 'excelWinner',       title: '中标单位(Excel)' },
  { id: 'excelCity',         title: '城市(Excel)' },
  { id: 'excelAmount',       title: '金额元(Excel)' },
  { id: 'excelSubject',      title: '标的物(Excel)' },
  { id: 'result',            title: '核查结果' },
  { id: 'reason',            title: '不通过/未找到原因' },
  { id: 'matchScore',        title: '匹配得分' },
  { id: 'tycProjectName',    title: '天眼查项目名' },
  { id: 'tycBuyer',          title: '天眼查采购人' },
  { id: 'tycAmount',         title: '天眼查金额' },
  { id: 'tycDate',           title: '天眼查发布日期' },
  { id: 'tycLink',           title: '天眼查链接' },
];

// ── 工具函数 ──────────────────────────────────────────────────────────────

function loadProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    try { return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8')); } catch { /* ignore */ }
  }
  return { completed: {}, failed: [] };
}

function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

function saveRawContentToFile(companyName, projectName, rawContent) {
  if (!fs.existsSync(RAW_CONTENT_DIR)) {
    fs.mkdirSync(RAW_CONTENT_DIR, { recursive: true });
  }
  const safeCompany = companyName.replace(/[\/\\:*?"<>|]/g, '_');
  const safeProject = projectName.replace(/[\/\\:*?"<>|]/g, '_').substring(0, 30);
  const fileName = `${safeCompany}_${safeProject}.md`;
  const filePath = path.join(RAW_CONTENT_DIR, fileName);
  fs.writeFileSync(filePath, rawContent, 'utf-8');
  return fileName;
}

/**
 * 解析 Excel 文件，返回结构化记录列表
 */
function parseExcel(excelPath) {
  const rows = readExcel(excelPath);
  const records = [];

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    // Excel 列名可能带空格或 (Excel) 后缀，做 trim 并兼容多种格式
    const buyer      = (row['  采购单位  '] || row['采购单位'] || row['采购单位(Excel)'] || '').trim();
    const project    = (row['  项目名称  '] || row['项目名称'] || row['项目名称(Excel)'] || '').trim();
    const winner     = (row['  中标单位  '] || row['中标单位'] || row['中标单位(Excel)'] || '').trim();
    const city       = (row['  城市  '] || row['城市'] || row['城市(Excel)'] || '').trim();
    const amountRaw  = (row['  中标金额（元）  '] || row['中标金额（元）'] || row['中标金额(元)'] || row['金额元(Excel)'] || '').toString().trim();
    const subject    = (row['  标的物  '] || row['标的物'] || row['标的物(Excel)'] || '').trim();

    if (!project && !buyer) continue; // 跳过空行

    const amountYuan = parseAmountYuan(amountRaw);

    records.push({
      index: i + 1,
      buyer,
      projectName: project,
      winner,
      city,
      amountRaw,
      amountYuan,
      subject,
    });
  }

  return records;
}

/**
 * 在天眼查招投标搜索页搜索项目名称，返回搜索结果列表
 * 参考 biddingDownload.js 的搜索框操作模式
 */
async function searchProjectOnTianyancha(page, projectName) {
  return withRetry(async () => {
    const searchUrl = 'https://www.tianyancha.com/s/toubiao';
    logger.info(`  访问搜索页: ${searchUrl}`);

    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    await delay(3000, 5000);

    // 检查验证码
    const needVerify = await page.evaluate(() => {
      return !!document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
    }).catch(() => false);

    if (needVerify) {
      logger.warn(`  ⚠️ 出现验证码，请手动处理...`);
      await page.waitForFunction(() => {
        return !document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
      }, { timeout: 120000 }).catch(() => {});
      await delay(3000, 5000);
    }

    // 操作搜索框
    try {
      await page.waitForSelector('#seo_seach_input', { timeout: 10000 });
      const searchInput = await page.$('#seo_seach_input');
      if (!searchInput) throw new Error('未找到搜索框');

      // 绕过 React 受控组件的 value tracker，直接设置 value 并触发 input 事件
      // 避免 type() 被天眼查前端过滤特殊字符（如连字符 -）
      await page.evaluate((name) => {
        const input = document.querySelector('#seo_seach_input');
        if (input) {
          // 使用原生 setter 绕过 React value tracker
          const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          nativeSetter.call(input, name);
          // 必须用 jQuery trigger 才能让天眼查的 jQuery .val() 读到值
          if (typeof $ !== 'undefined' && $(input).trigger) {
            $(input).trigger('input');
          } else {
            input.dispatchEvent(new Event('input', { bubbles: true }));
          }
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }, projectName);
      logger.info(`  输入搜索: ${projectName.substring(0, 40)}...`);

      await delay(1000, 2000);

      // 点击"天眼一下"按钮（用 evaluate 避免 elementHandle 点击问题）
      await page.evaluate(() => {
        const btn = document.querySelector('.input-group-btn.btn.-h52.btn-primary');
        if (btn) btn.click();
      });
    } catch (err) {
      logger.warn(`  搜索框操作失败: ${err.message}，尝试备用方法...`);
      await page.evaluate((name) => {
        const input = document.querySelector('#seo_seach_input');
        if (input) {
          const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          nativeSetter.call(input, name);
          if (typeof $ !== 'undefined' && $(input).trigger) {
            $(input).trigger('input');
          } else {
            input.dispatchEvent(new Event('input', { bubbles: true }));
          }
        }
      }, projectName);
      await delay(1000, 2000);
      await page.evaluate(() => {
        const btn = document.querySelector('.input-group-btn.btn.-h52.btn-primary');
        if (btn) btn.click();
      });
    }

    // 等待搜索结果
    logger.info('  等待搜索结果...');
    await delay(5000, 8000);

    const currentUrl = await page.url();
    logger.info(`  当前URL: ${currentUrl}`);

    // 如果跳转到企业 detail 页面，尝试应用"中标公告"筛选（提升 winner 搜索命中率）
    if (currentUrl.includes('/detail/')) {
      try {
        const filterClicked = await page.evaluate(() => {
          const allElements = document.querySelectorAll('button, a, span, div, li');
          for (const el of allElements) {
            const text = el.textContent.trim();
            if (text === '中标公告' && !el.classList.contains('active') && !el.classList.contains('selected')) {
              el.click();
              return true;
            }
          }
          return false;
        });
        if (filterClicked) {
          logger.info('  已应用中标公告筛选');
          await delay(2000, 3000);
        }
      } catch (err) {
        logger.warn(`  应用筛选失败: ${err.message}`);
      }
    }

    // 等待列表加载
    try {
      await page.waitForFunction(() => {
        const items = document.querySelectorAll('[class*="index_item__"]');
        return items.length > 0;
      }, { timeout: 10000 });
    } catch {
      logger.warn('  未找到搜索结果列表');
      return [];
    }

    const allResults = [];
    const seenKeys = new Set();
    let pageNum = 1;
    let hasMore = true;

    while (hasMore && pageNum <= VERIFY_SEARCH_MAX_PAGES) {
      await delay(2000, 3000);

      const pageResults = await page.evaluate(() => {
        const records = [];

        // 从 __NEXT_DATA__ 解析详情链接
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
                  const cleanTitle = item.title.replace(/<[^>]+>/g, '').trim();
                  titleLinkMap.set(cleanTitle, item.detailUrl);
                  titleLinkMap.set(item.title.trim(), item.detailUrl);
                }
              }
            }
          }
        } catch { /* ignore */ }

        const items = document.querySelectorAll('[class*="index_item__"]');

        for (const item of items) {
          const fullText = item.textContent;

          const titleEl = item.querySelector('[class*="index_item-header__"]');
          let title = titleEl ? titleEl.textContent.trim() : '';

          if (!title || title.length < 5) {
            const textLines = fullText.split(/\n|\s{2,}/).filter(t => {
              const trimmed = t.trim();
              return trimmed.length > 5 &&
                     !trimmed.startsWith('发布时间') &&
                     !trimmed.startsWith('招采单位') &&
                     !trimmed.startsWith('中标金额');
            });
            if (textLines.length > 0) title = textLines[0].trim().substring(0, 150);
          }

          if (!title || title.length < 5) continue;

          const dateMatch = fullText.match(/发布时间[：:]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{4})/);
          let date = '';
          if (dateMatch) {
            const rawDate = dateMatch[1];
            if (rawDate.includes('/')) {
              const [m, d, y] = rawDate.split('/');
              date = `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            } else {
              date = rawDate;
            }
          }

          const amountMatch = fullText.match(/中标金额[：:]?\s*([\d,.]+\s*[万亿]?元)/);
          const amount = amountMatch ? amountMatch[1] : '';

          const buyerMatch = fullText.match(/招采单位[：:]?\s*(.+?)(?=\s*(发布时间|中标金额|预算金额|公告类型|招标代理|项目编号)|\n|$)/);
          let buyer = buyerMatch ? buyerMatch[1].trim() : '';
          buyer = buyer.replace(/(中标金额|预算金额|公告类型|招标代理).*$/g, '').trim();

          let type = '';
          if (fullText.includes('中标公告')) type = '中标公告';
          else if (fullText.includes('成交公告')) type = '成交公告';
          else if (fullText.includes('采购公告')) type = '采购公告';
          else if (fullText.includes('招标公告')) type = '招标公告';

          let detailLink = titleLinkMap.get(title) || '';
          if (!detailLink) {
            const linkEl = item.querySelector('a[href*="/sub-details/bidInfo/"]');
            if (linkEl) detailLink = linkEl.href || '';
          }
          if (detailLink) detailLink = detailLink.split('?')[0];

          records.push({
            title,
            link: detailLink,
            buyer,
            amount,
            date,
            type,
            fullText: fullText.substring(0, 500),
          });
        }

        return records;
      });

      let addedCount = 0;
      for (const result of pageResults) {
        const normalizedTitle = result.title.replace(/[\s\p{P}]/gu, '').toLowerCase();
        const dedupeKey = `${normalizedTitle}__${result.date || ''}`;
        if (seenKeys.has(dedupeKey)) continue;
        seenKeys.add(dedupeKey);
        allResults.push(result);
        addedCount++;
      }

      const yearHits = allResults.filter(r => r.date.startsWith(`${VERIFY_TARGET_YEAR}-`)).length;
      logger.info(`  第 ${pageNum} 页抓取 ${pageResults.length} 条，新增 ${addedCount} 条，累计 ${allResults.length} 条，其中 ${VERIFY_TARGET_YEAR} 年 ${yearHits} 条`);

      // 记录当前页第一条标题，用于判断翻页后内容是否已刷新
      const firstTitleBefore = pageResults.length > 0 ? pageResults[0].title : '';

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

      if (!hasMore) break;
      pageNum++;
      await delay(2500, 4000);

      // 显式等待新页面内容加载：第一条标题发生变化
      if (firstTitleBefore) {
        try {
          await page.waitForFunction((prevFirst) => {
            const items = document.querySelectorAll('[class*="index_item__"]');
            if (items.length === 0) return false;
            const firstTitle = items[0].querySelector('[class*="index_item-header__"]')?.textContent?.trim()
              || items[0].textContent?.trim();
            return firstTitle !== prevFirst;
          }, { timeout: 15000 }, firstTitleBefore);
        } catch {
          logger.warn('  翻页后内容未变化，可能已是最后一页或加载失败，停止翻页');
          break;
        }
      }
    }

    logger.info(`  搜索结果: ${allResults.length} 条`);
    return allResults;
  }, { maxRetries: 2, delayMs: 5000, label: `搜索${projectName.substring(0, 20)}` });
}

/**
 * 用关键词子串重试搜索（当完整项目名称搜不到时）
 */
function extractSearchKeywords(projectName) {
  if (!projectName) return '';

  // 优先保护的行业核心词（避免被停用词切散）
  const KEEP_WORDS = ['人形机器人', '具身智能', '四足机器人', '仿生机器人',
                      '机械臂', '灵巧手', '轮式机器人', '足式机器人',
                      '双足机器人', '人工智能', '智能机器人', '教育机器人',
                      '巡检机器人', '协作机器人', '康复机器人', '手术机器人',
                      '按摩机器人', '数据采集中心'];

  // 去除常见的通用词（不再包含"服务"，避免"养老服务机器人"被误切）
  const stopWords = ['项目', '采购', '设备', '招标', '公告', '中标', '成交',
                     '政府', '公开', '竞争性', '磋商', '谈判', '询价', '单一来源',
                     '及', '和', '的', '等', '与', '关于'];

  let text = projectName;
  const preserved = [];
  for (const kw of KEEP_WORDS) {
    if (text.includes(kw)) {
      preserved.push(kw);
      text = text.split(kw).join(' ');
    }
  }

  for (const w of stopWords) {
    text = text.replace(new RegExp(w, 'g'), ' ');
  }

  const words = text.split(/\s+/).filter(w => w.length >= 2)
    .sort((a, b) => b.length - a.length); // 优先保留更长的词（信息量大）
  const result = [...preserved, ...words].slice(0, 3).join(' ');
  return result || projectName.substring(0, Math.min(20, projectName.length));
}

function buildVerifyQueries(record) {
  const queries = [];
  const seen = new Set();

  const pushQuery = (query, source) => {
    const cleaned = (query || '').trim();
    if (!cleaned || seen.has(cleaned)) return;
    seen.add(cleaned);
    queries.push({ query: cleaned, source });
  };

  // 策略 1：完整项目名称（通常比中标单位更具体，命中精度更高）
  pushQuery(record.projectName, '项目名称');

  // 策略 2：优先用中标单位搜索
  if (record.winner) pushQuery(record.winner, '中标单位');

  // 策略 3：项目关键词
  const keywordQuery = extractSearchKeywords(record.projectName);
  if (keywordQuery !== record.projectName) {
    pushQuery(keywordQuery, '项目关键词');
  }

  // 策略 4：采购单位 + 项目关键词组合（适合学校/机构的短项目名）
  if (record.buyer && keywordQuery) {
    const combined = `${record.buyer.substring(0, 20)} ${keywordQuery.substring(0, 20)}`.trim();
    if (combined.length >= 5 && combined !== record.projectName) {
      pushQuery(combined, '采购单位+关键词');
    }
  }

  // 策略 5：标的物
  if (record.subject && record.subject.trim().length > 3) {
    const subjectQuery = extractSearchKeywords(record.subject);
    if (subjectQuery !== record.projectName && subjectQuery !== keywordQuery) {
      pushQuery(subjectQuery, '标的物');
    }
  }

  // 策略 6：采购单位兜底
  if (record.buyer) pushQuery(record.buyer, '采购单位');

  return queries;
}

// ── 主流程 ────────────────────────────────────────────────────────────────

async function main() {
  logger.info('=== Verify: 第三方招投标数据核查 ===');

  // 确定输入文件
  const excelPath = process.argv[2] || DEFAULT_EXCEL;
  if (!fs.existsSync(excelPath)) {
    logger.error(`未找到 Excel 文件: ${excelPath}`);
    process.exit(1);
  }
  logger.info(`输入文件: ${excelPath}`);

  // 解析 Excel
  const records = parseExcel(excelPath);
  logger.info(`解析到 ${records.length} 条记录`);

  if (records.length === 0) {
    logger.warn('Excel 中无有效数据');
    process.exit(0);
  }

  // 确保输出目录存在
  if (!fs.existsSync(RAW_CONTENT_DIR)) fs.mkdirSync(RAW_CONTENT_DIR, { recursive: true });
  const dataDir = path.join(projectRoot, 'data');
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

  // 加载进度
  const progress = loadProgress();
  const completedCount = Object.keys(progress.completed).length;
  logger.info(`已完成 ${completedCount} 条，失败 ${progress.failed.length} 条`);

  // 过滤待处理记录
  const pending = records.filter(r => {
    const key = `${r.index}||${r.projectName}`;
    return !progress.completed[key];
  });
  logger.info(`待处理 ${pending.length} 条`);

  if (pending.length === 0) {
    logger.info('所有记录已处理完毕，直接输出结果');
    await outputResults(progress, records);
    return;
  }

  // 连接浏览器
  const browser = await connectBrowser();
  const page = await openNewPage(browser);

  let processedCount = 0;

  for (let i = 0; i < pending.length; i++) {
    const r = pending[i];
    const key = `${r.index}||${r.projectName}`;

    logger.info(`\n[${i + 1}/${pending.length}] #${r.index} ${r.winner} | ${r.projectName.substring(0, 50)}`);

    const recordTimeout = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('单条记录处理超时（3分钟）')), 180000);
    });

    try {
      await Promise.race([recordTimeout, (async () => {
        // Step 1-5: 依次尝试多个查询词，优先翻页寻找 2025 年候选
        const queryPlans = buildVerifyQueries(r);
        let bestAttempt = {
          matched: null,
          score: 0,
          details: ['搜索结果为空'],
          searchResults: [],
          query: '',
        };

        for (let qIndex = 0; qIndex < queryPlans.length; qIndex++) {
          const plan = queryPlans[qIndex];
          logger.info(`  搜索策略 ${qIndex + 1}/${queryPlans.length}: ${plan.source} -> ${plan.query}`);

          const rawResults = await searchProjectOnTianyancha(page, plan.query);
          const yearFilteredResults = filterResultsByYear(rawResults, VERIFY_TARGET_YEAR);

          logger.info(`  ${plan.source} 命中 ${rawResults.length} 条，其中 ${VERIFY_TARGET_YEAR} 年 ${yearFilteredResults.length} 条`);

          const attempt = {
            ...matchSearchResult(r, yearFilteredResults, VERIFY_TARGET_YEAR),
            searchResults: yearFilteredResults,
            query: plan.query,
          };

          const shouldReplaceBest =
            attempt.score > bestAttempt.score ||
            (attempt.score === bestAttempt.score &&
              attempt.searchResults.length > bestAttempt.searchResults.length);

          if (shouldReplaceBest) {
            bestAttempt = attempt;
          }

          // 质量门控1：中标单位搜索时，如果采购单位不匹配（即使标题相似度较高），
          // 视为潜在错误匹配，继续尝试后续策略（如采购单位搜索）
          const isLowQualityWinnerMatch =
            plan.source === '中标单位' &&
            attempt.matched &&
            !entityMatch(r.buyer, attempt.matched.buyer);

          // 质量门控2：匹配到招标公告/采购公告（非中标/成交公告），
          // 即使分数够高也继续搜索，避免预算金额 vs 中标金额混淆
          const isWrongBidType =
            attempt.matched &&
            !['中标公告', '成交公告'].includes(attempt.matched.type) &&
            (attempt.matched.title.includes('招标公告') || attempt.matched.title.includes('采购公告'));

          if (attempt.matched && attempt.score >= VERIFY_MATCH_THRESHOLD && !isLowQualityWinnerMatch && !isWrongBidType) {
            bestAttempt = attempt;
            logger.info(`  当前查询已找到可接受候选，停止继续扩展查询`);
            break;
          }

          if (isLowQualityWinnerMatch) {
            logger.info(`  中标单位搜索匹配质量过低（标题相似度 ${(attempt.titleSimilarity * 100).toFixed(0)}%，采购单位不匹配），继续扩展查询`);
          }

          if (isWrongBidType) {
            logger.info(`  匹配到非中标/成交公告（${attempt.matched.type || '未知类型'}），继续扩展查询`);
          }
        }

        const {
          matched,
          score,
          details,
          searchResults,
        } = bestAttempt;

        if (!matched || score < VERIFY_MATCH_THRESHOLD) {
          // 未找到匹配
          progress.completed[key] = {
            ...r,
            result: '未找到',
            reason: searchResults.length === 0 ? '天眼查搜索无结果' : `最高匹配分 ${score}，低于阈值${VERIFY_MATCH_THRESHOLD}`,
            matchScore: score,
            matchDetails: details,
            tycProjectName: matched?.title || '',
            tycBuyer: matched?.buyer || '',
            tycAmount: matched?.amount || '',
            tycDate: matched?.date || '',
            tycLink: matched?.link || '',
          };
          logger.info(`  ❌ 未找到匹配 (最高分: ${score})`);
          details.forEach(d => logger.info(`     ${d}`));

        } else {
          // 找到候选匹配，进入详情页核查
          logger.info(`  匹配候选: ${matched.title.substring(0, 50)} (分数: ${score})`);
          details.forEach(d => logger.info(`     ${d}`));

          let verifyResult = score >= 70 ? '通过' : '待人工确认';
          let verifyReasons = score >= 70 ? [] : ['匹配得分较低，需人工复核'];
          let rawContentFile = '';

          if (matched.link) {
            // 访问详情页核查
            try {
              const detail = await fetchBiddingDetail(page, matched.link, matched.title);

              // 金额兜底：如果详情页提取的金额和搜索结果列表中的金额差异 > 50%，以搜索结果列表为准
              const detailAmountYuan = parseAmountYuan(detail.amount, { sourceHint: 'tianyancha' });
              const matchedAmountYuan = parseAmountYuan(matched.amount, { sourceHint: 'tianyancha' });
              if (detailAmountYuan && matchedAmountYuan) {
                const { match: amountMatch } = compareAmount(detailAmountYuan, matchedAmountYuan, 0.5);
                if (!amountMatch) {
                  logger.info(`  详情页金额(${detail.amount})与搜索结果金额(${matched.amount})差异过大，采用搜索结果金额`);
                  detail.amount = matched.amount;
                }
              }

              // 核对详情页数据（强制目标年份）
              const verification = verifyDetail(r, detail, VERIFY_TARGET_YEAR);

              if (!verification.passed) {
                // 无论匹配分多高，详情页不一致一律降级为"待人工确认"
                verifyResult = '待人工确认';
                verifyReasons = [...new Set([...verifyReasons, ...verification.reasons])];
                logger.info(`  ⚠️ 详情核查有偏差，待人工确认: ${verification.reasons.join('; ')}`);
              } else {
                if (score >= 70) {
                  verifyResult = '通过';
                  verifyReasons = [];
                }
                logger.info(`  ✅ 详情核查通过`);
              }

              // 保存 raw_content（通过和待人工确认都保存）
              if (detail.rawContent) {
                rawContentFile = saveRawContentToFile(r.winner, matched.title, detail.rawContent);
                logger.info(`  📄 已保存 raw_content: ${rawContentFile}`);
              }

            } catch (err) {
              logger.warn(`  ⚠️ 详情页访问失败: ${err.message}，仅依据搜索结果判定`);
              verifyResult = score >= 70 ? '通过' : '待人工确认';
              if (score < 70) verifyReasons.push(`详情页访问失败: ${err.message}`);
            }
          } else {
            // 无详情链接
            verifyResult = score >= 70 ? '通过' : '待人工确认';
            if (!verifyReasons.includes('无天眼查详情链接')) {
              verifyReasons.push('无天眼查详情链接');
            }
          }

          progress.completed[key] = {
            ...r,
            result: verifyResult,
            reason: verifyReasons.join('; '),
            matchScore: score,
            matchDetails: details,
            tycProjectName: matched.title,
            tycBuyer: matched.buyer,
            tycAmount: matched.amount,
            tycDate: matched.date,
            tycLink: matched.link,
            tycType: matched.type || '中标公告',
            rawContentFile,
          };

          const icon = verifyResult === '通过' ? '✅' : '⚠️';
          logger.info(`  ${icon} 核查结果: ${verifyResult}`);
        }
      })()]);

    } catch (err) {
      logger.error(`  ❌ 处理失败: ${err.message}`);
      progress.completed[key] = {
        ...r,
        result: '处理失败',
        reason: err.message,
        matchScore: 0,
        matchDetails: [],
        tycProjectName: '',
        tycBuyer: '',
        tycAmount: '',
        tycDate: '',
        tycLink: '',
      };
      progress.failed.push({ key, error: err.message, time: new Date().toISOString() });
    }

    // 保存进度
    processedCount++;
    saveProgress(progress);

    // 每 10 条输出一次中间结果
    if (processedCount % 10 === 0) {
      await outputResults(progress, records);
      logger.info(`  中间保存: 已处理 ${processedCount} 条`);
    }

    // 延迟（避免频繁请求）
    await delay(3000, 6000);
  }

  await page.close();

  // 最终输出
  await outputResults(progress, records);

  // 统计
  const allCompleted = Object.values(progress.completed);
  const passed     = allCompleted.filter(r => r.result === '通过').length;
  const pendingR   = allCompleted.filter(r => r.result === '待人工确认').length;
  const notFound   = allCompleted.filter(r => r.result === '未找到').length;
  const failedR    = allCompleted.filter(r => r.result === '处理失败').length;

  logger.info('\n=== Verify 完成 ===');
  logger.info(`总计: ${records.length} 条`);
  logger.info(`通过: ${passed} | 待人工确认: ${pendingR} | 未找到: ${notFound} | 失败: ${failedR}`);
  logger.info(`核查报告: ${VERIFY_REPORT_CSV}`);
  logger.info(`通过记录: ${VERIFY_BIDDING_CSV}`);
  logger.info('');
  logger.info('后续操作:');
  logger.info('  1. 查看 verify_match_report.csv 确认核查结果');
  logger.info('  2. 将 verify_bidding_records.csv 的内容追加到 bidding_records.csv');
  logger.info('  3. 运行 npm run extract → npm run ingest 完成入库');
}

/**
 * 输出结果文件
 */
async function outputResults(progress, allRecords) {
  const completed = Object.values(progress.completed);

  // 1. 核查报告（全量）
  const reportRows = allRecords.map(r => {
    const key = `${r.index}||${r.projectName}`;
    const c = progress.completed[key];
    if (!c) {
      return {
        index: r.index,
        excelBuyer: r.buyer,
        excelProject: r.projectName,
        excelWinner: r.winner,
        excelCity: r.city,
        excelAmount: r.amountRaw,
        excelSubject: r.subject,
        result: '待处理',
        reason: '',
        matchScore: '',
        tycProjectName: '',
        tycBuyer: '',
        tycAmount: '',
        tycDate: '',
        tycLink: '',
      };
    }
    return {
      index: c.index,
      excelBuyer: c.buyer,
      excelProject: c.projectName,
      excelWinner: c.winner,
      excelCity: c.city,
      excelAmount: c.amountRaw,
      excelSubject: c.subject,
      result: c.result,
      reason: c.reason || '',
      matchScore: c.matchScore ?? '',
      tycProjectName: c.tycProjectName || '',
      tycBuyer: c.tycBuyer || '',
      tycAmount: c.tycAmount || '',
      tycDate: c.tycDate || '',
      tycLink: c.tycLink || '',
    };
  });

  await writeCsv(VERIFY_REPORT_CSV, REPORT_HEADERS, reportRows);

  // 2. 通过的记录（格式同 bidding_records.csv）
  // 注意：只输出"通过"的记录，"待人工确认"不自动入库
  const passedRows = completed
    .filter(c => c.result === '通过')
    .map(c => ({
      companyName: c.winner,
      projectName: c.tycProjectName || c.projectName,
      type: c.tycType || '中标公告',
      buyer: c.tycBuyer || c.buyer,
      amount: c.tycAmount || c.amountRaw,
      date: c.tycDate || '',
      link: c.tycLink || '',
    }));

  if (passedRows.length > 0) {
    await writeCsv(VERIFY_BIDDING_CSV, BIDDING_HEADERS, passedRows);
  }
}

main().catch(err => {
  logger.error(`Verify 执行失败: ${err.message}`);
  process.exit(1);
});
