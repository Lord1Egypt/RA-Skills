/**
 * Crawl: 招投标记录下载
 *
 * 基于 Search 确认的企业全称，在天眼查下载招投标记录。
 * 筛选: 自定义时间范围 + 金额门槛
 * 输出: data/bidding_records.csv
 *
 * 前置条件: 已完成 Search，且 data/company_list.csv 中有已确认企业
 * 用法: npm run crawl
 * 
 * 配置参数（修改以下常量）：
 *   - START_DATE: 开始日期 (格式: YYYY-MM-DD)
 *   - END_DATE: 结束日期 (格式: YYYY-MM-DD)
 *   - MIN_AMOUNT: 最低金额（万元），0 表示无门槛
 */
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { connectBrowser, openNewPage, delay } from './browser.js';
import { downloadBiddingRecords } from './modules/biddingDownload.js';
import { readCsv, writeCsv } from './utils/excel.js';
import { logger } from './utils/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const COMPANY_CSV = path.join(projectRoot, 'data', 'company_list.csv');
const OUTPUT_CSV = path.join(projectRoot, 'data', 'bidding_records.csv');
const PROGRESS_FILE = path.join(projectRoot, 'data', 'crawl_progress.json');

// ==================== 配置参数 ====================
// 时间范围配置
const START_DATE = '2026-01-01';  // 开始日期
const END_DATE = '2026-03-31';    // 结束日期

// 金额门槛配置（万元），0 表示无门槛
const MIN_AMOUNT = 0;

// CSV 表头
const CSV_HEADERS = [
  { id: 'companyName', title: '企业名称' },
  { id: 'title', title: '项目名称' },
  { id: 'type', title: '公告类型' },
  { id: 'buyer', title: '采购人' },
  { id: 'amount', title: '中标金额' },
  { id: 'date', title: '发布日期' },
  { id: 'link', title: '天眼查详情页链接' },
];

// 加载进度
function loadProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8'));
    } catch (e) {
      return { completed: [], failed: [] };
    }
  }
  return { completed: [], failed: [] };
}

// 保存进度
function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

async function processCompany(browser, company, startDate, endDate, minAmount) {
  const companyName = company['企业全称(天眼查)'] || company['企业简称(MD)'];
  const companyUrl = company['天眼查链接'];
  
  // 为每家企业创建新页面，避免 frame detached 问题
  const page = await openNewPage(browser);
  
  try {
    const records = await downloadBiddingRecords(page, companyUrl, companyName, {
      startDate,
      endDate,
      minAmount,
    });
    await page.close();
    return { success: true, records };
  } catch (err) {
    await page.close();
    // 如果是 frame detached 错误，重试一次
    if (err.message.includes('detached')) {
      logger.warn(`  🔄 Frame detached，重试一次...`);
      const retryPage = await openNewPage(browser);
      try {
        const records = await downloadBiddingRecords(retryPage, companyUrl, companyName, {
          startDate,
          endDate,
          minAmount,
        });
        await retryPage.close();
        return { success: true, records };
      } catch (retryErr) {
        await retryPage.close();
        return { success: false, error: retryErr.message };
      }
    }
    return { success: false, error: err.message };
  }
}

async function main() {
  logger.info('=== Crawl: 招投标记录下载 ===');

  // 读取 Search 的企业列表
  if (!fs.existsSync(COMPANY_CSV)) {
    logger.error(`未找到企业列表: ${COMPANY_CSV}`);
    logger.error('请先运行 npm run search');
    process.exit(1);
  }

  const companies = readCsv(COMPANY_CSV);
  const confirmedCompanies = companies.filter(c => c['搜索状态'] === '已确认' && c['天眼查链接']);
  
  logger.info(`共 ${confirmedCompanies.length} 家已确认企业需要查询招投标`);

  // 加载进度
  const progress = loadProgress();
  logger.info(`已处理: ${progress.completed.length} 家, 失败: ${progress.failed.length} 家`);

  // 过滤出未处理的企业
  const pendingCompanies = confirmedCompanies.filter(c => {
    const name = c['企业全称(天眼查)'] || c['企业简称(MD)'];
    return !progress.completed.includes(name);
  });
  
  if (pendingCompanies.length === 0) {
    logger.info('所有企业已处理完毕！');
  } else {
    logger.info(`剩余 ${pendingCompanies.length} 家企业待处理`);
  }

  // 连接浏览器
  const browser = await connectBrowser();

  // 加载已有记录
  let allRecords = [];
  if (fs.existsSync(OUTPUT_CSV)) {
    const existingRecords = readCsv(OUTPUT_CSV);
    allRecords = existingRecords.map(r => ({
      companyName: r['企业名称'],
      title: r['项目名称'],
      type: r['公告类型'],
      buyer: r['采购人'],
      amount: r['中标金额'],
      date: r['发布日期'],
      link: r['天眼查详情页链接'],
    }));
    logger.info(`已加载 ${allRecords.length} 条现有记录`);
  }

  let companiesWithRecords = new Set(allRecords.map(r => r.companyName)).size;

  for (let i = 0; i < pendingCompanies.length; i++) {
    const company = pendingCompanies[i];
    const companyName = company['企业全称(天眼查)'] || company['企业简称(MD)'];
    const companyUrl = company['天眼查链接'];

    logger.info(`[${i + 1}/${pendingCompanies.length}] 处理: ${companyName}`);

    const result = await processCompany(browser, company, START_DATE, END_DATE, MIN_AMOUNT);

    if (result.success) {
      if (result.records.length > 0) {
        companiesWithRecords++;
        allRecords.push(...result.records);
        logger.info(`  ✅ 找到 ${result.records.length} 条符合条件的记录`);
      } else {
        logger.info(`  ⚪ 无符合条件的招投标记录`);
      }
      progress.completed.push(companyName);
    } else {
      logger.error(`  ❌ 处理 "${companyName}" 失败: ${result.error}`);
      progress.failed.push({ name: companyName, error: result.error, time: new Date().toISOString() });
    }

    // 保存进度
    saveProgress(progress);

    // 每处理 3 家企业保存一次中间结果
    if ((i + 1) % 3 === 0 && allRecords.length > 0) {
      await writeCsv(OUTPUT_CSV, CSV_HEADERS, allRecords);
      logger.info(`中间保存: 已处理 ${i + 1} 家, 共 ${allRecords.length} 条记录`);
    }

    // 企业间隔 3-6 秒（减少等待时间）
    await delay(3000, 6000);
  }

  // 写入最终结果
  if (allRecords.length > 0) {
    await writeCsv(OUTPUT_CSV, CSV_HEADERS, allRecords);
  }

  logger.info('=== Step 2 完成 ===');
  logger.info(`时间范围: ${START_DATE} 至 ${END_DATE}`);
  logger.info(`金额门槛: ${MIN_AMOUNT === 0 ? '无门槛' : MIN_AMOUNT + '万元'}`);
  logger.info(`有招投标记录的企业: ${companiesWithRecords} 家`);
  logger.info(`符合条件的记录总数: ${allRecords.length} 条`);
  logger.info(`失败企业: ${progress.failed.length} 家`);
  logger.info(`输出文件: ${OUTPUT_CSV}`);
  logger.info('请检查 CSV 文件，然后运行 Step 3 进行深度核查');
}

main().catch(err => {
  logger.error(`Step 2 执行失败: ${err.message}`);
  process.exit(1);
});
