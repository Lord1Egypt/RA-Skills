/**
 * Search: 企业名称搜索
 *
 * 从企业名单 MD 文件中解析企业简称，在天眼查搜索确认全称。
 * 输出: data/company_list.csv
 *
 * 用法:
 *   1. 先用远程调试模式启动 Chrome 并登录天眼查:
 *      /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
 *   2. 运行: npm run search
 */
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { connectBrowser, openNewPage, delay } from './browser.js';
import { getDomesticCompanies, parseCompanyList } from './modules/parseCompanyList.js';
import { searchCompanyOnTianyancha } from './modules/companySearch.js';
import { writeCsv, readCsv } from './utils/excel.js';
import { logger } from './utils/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const OUTPUT_CSV = path.join(projectRoot, 'data', 'company_list.csv');

const CSV_HEADERS = [
  { id: 'index', title: '索引' },
  { id: 'shortName', title: '企业简称(MD)' },
  { id: 'fullName', title: '企业全称(天眼查)' },
  { id: 'companyId', title: '公司ID' },
  { id: 'url', title: '天眼查链接' },
  { id: 'field', title: '所属领域' },
  { id: 'product', title: '产品名称' },
  { id: 'city', title: '城市' },
  { id: 'status', title: '搜索状态' },
];

/**
 * 从天眼查链接中提取公司ID
 * @param {string} url - 天眼查企业链接
 * @returns {string} 公司ID
 */
function extractCompanyId(url) {
  if (!url) return '';
  const match = url.match(/\/company\/(\d+)/);
  return match ? match[1] : '';
}

async function main() {
  logger.info('=== Step 1: 企业名称搜索 ===');
  
  // 解析企业名单
  const allCompanies = parseCompanyList();
  const domesticCompanies = allCompanies.filter(c => !c.isOverseas);
  const overseasCompanies = allCompanies.filter(c => c.isOverseas);
  
  logger.info(`跳过海外/港澳台企业 ${overseasCompanies.length} 家: ${overseasCompanies.map(c => c.name).join(', ')}`);

  // 检查是否有已搜索的缓存
  let existingResults = {};
  if (fs.existsSync(OUTPUT_CSV)) {
    try {
      const existing = readCsv(OUTPUT_CSV);
      for (const row of existing) {
        if (row['搜索状态'] === '已确认') {
          existingResults[row['企业简称']] = row;
        }
      }
      logger.info(`已有 ${Object.keys(existingResults).length} 家已确认企业，将跳过`);
    } catch (e) {
      logger.warn(`读取已有结果失败: ${e.message}`);
    }
  }

  // 连接浏览器
  const browser = await connectBrowser();
  const page = await openNewPage(browser);

  const results = [];
  let searchedCount = 0;
  let skippedCount = 0;

  for (const company of domesticCompanies) {
    // 如果已有确认结果，直接使用缓存
    if (existingResults[company.name]) {
      const cached = existingResults[company.name];
      results.push({
        index: company.index,
        shortName: company.name,
        fullName: cached['企业全称'],
        companyId: cached['公司ID'] || extractCompanyId(cached['天眼查链接']),
        url: cached['天眼查链接'],
        field: company.field,
        product: company.product,
        city: company.city,
        status: '已确认',
      });
      skippedCount++;
      continue;
    }

    try {
      const searchResult = await searchCompanyOnTianyancha(page, company.name);
      results.push({
        index: company.index,
        shortName: company.name,
        fullName: searchResult.fullName,
        companyId: extractCompanyId(searchResult.url),
        url: searchResult.url,
        field: company.field,
        product: company.product,
        city: company.city,
        status: searchResult.status,
      });
      searchedCount++;

      // 每搜索 10 家保存一次中间结果
      if (searchedCount % 10 === 0) {
        await writeCsv(OUTPUT_CSV, CSV_HEADERS, results);
        logger.info(`中间保存: 已搜索 ${searchedCount} 家，跳过缓存 ${skippedCount} 家`);
      }

      // 搜索间隔 3-6 秒
      await delay(3000, 6000);
    } catch (err) {
      logger.error(`搜索 "${company.name}" 失败: ${err.message}`);
      results.push({
        index: company.index,
        shortName: company.name,
        fullName: '',
        companyId: '',
        url: '',
        field: company.field,
        product: company.product,
        city: company.city,
        status: `失败: ${err.message}`,
      });
    }
  }

  // 同时输出海外企业（标记为跳过）
  for (const company of overseasCompanies) {
    results.push({
      index: company.index,
      shortName: company.name,
      fullName: '',
      companyId: '',
      url: '',
      field: company.field,
      product: company.product,
      city: company.city,
      status: '海外企业-跳过',
    });
  }

  // 按索引排序
  results.sort((a, b) => a.index - b.index);

  // 写入最终结果
  await writeCsv(OUTPUT_CSV, CSV_HEADERS, results);

  // 统计
  const confirmed = results.filter(r => r.status === '已确认').length;
  const notFound = results.filter(r => r.status === '未找到').length;
  const failed = results.filter(r => r.status.startsWith('失败')).length;
  const skipped = results.filter(r => r.status === '海外企业-跳过').length;

  logger.info('=== Step 1 完成 ===');
  logger.info(`已确认: ${confirmed} | 未找到: ${notFound} | 失败: ${failed} | 海外跳过: ${skipped}`);
  logger.info(`输出文件: ${OUTPUT_CSV}`);
  logger.info('请检查 CSV 文件，确认企业全称是否正确，然后运行 Step 2');

  await page.close();
}

main().catch(err => {
  logger.error(`Step 1 执行失败: ${err.message}`);
  process.exit(1);
});
