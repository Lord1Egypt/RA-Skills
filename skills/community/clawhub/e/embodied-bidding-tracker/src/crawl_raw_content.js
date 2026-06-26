/**
 * 补充下载 Crawl 更新数据对应的 raw_content 文件
 *
 * 用途: 当 Crawl 下载了新的中标记录但没有下载对应的 raw_content 文件时使用
 *
 * 输入: data/bidding_records.csv
 * 输出: data/raw_content/*.md
 *
 * 用法: npm run crawl:rawcontent
 */
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { connectBrowser, openNewPage, delay } from './browser.js';
import { fetchBiddingDetail } from './modules/deepVerify.js';
import { readCsv } from './utils/excel.js';
import { logger } from './utils/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const INPUT_CSV = path.join(projectRoot, 'data', 'bidding_records.csv');
const RAW_CONTENT_DIR = path.join(projectRoot, 'data', 'raw_content');
const PROGRESS_FILE = path.join(projectRoot, 'data', 'crawl_raw_content_progress.json');

// 保存原始内容到单独的 Markdown 文件
function saveRawContentToFile(companyName, projectName, rawContent) {
  if (!fs.existsSync(RAW_CONTENT_DIR)) {
    fs.mkdirSync(RAW_CONTENT_DIR, { recursive: true });
  }

  // 生成文件名：企业名_项目名前30字.md
  const safeCompany = companyName.replace(/[\/\\:*?"<>|]/g, '_');
  const safeProject = projectName.replace(/[\/\\:*?"<>|]/g, '_').substring(0, 30);
  const fileName = `${safeCompany}_${safeProject}.md`;
  const filePath = path.join(RAW_CONTENT_DIR, fileName);

  fs.writeFileSync(filePath, rawContent, 'utf-8');
  return filePath;
}

// 检查记录是否已有对应的 raw_content 文件
// 严格匹配：文件名必须以 "{企业名}_{项目名前30字}" 开头
function hasRawContentFile(companyName, projectName) {
  if (!fs.existsSync(RAW_CONTENT_DIR)) return false;

  const safeCompany = companyName.replace(/[\/\\:*?"<>|]/g, '_');
  const safeProject = projectName.replace(/[\/\\:*?"<>|]/g, '_').substring(0, 30);

  const files = fs.readdirSync(RAW_CONTENT_DIR).filter(f => f.endsWith('.md'));
  return files.some(f => f.startsWith(`${safeCompany}_${safeProject}`));
}

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

async function main() {
  logger.info('=== 补充下载 raw_content 文件 ===');

  if (!fs.existsSync(INPUT_CSV)) {
    logger.error(`未找到招投标记录: ${INPUT_CSV}`);
    logger.error('请先运行 npm run crawl');
    process.exit(1);
  }

  const records = readCsv(INPUT_CSV);
  logger.info(`共 ${records.length} 条记录`);

  // 过滤出有详情链接且没有 raw_content 文件的记录
  const recordsToDownload = records.filter(r => {
    const companyName = r['企业名称'];
    const projectName = r['项目名称'];
    const hasLink = r['天眼查详情页链接'];

    return hasLink && !hasRawContentFile(companyName, projectName);
  });

  logger.info(`需要下载 raw_content 的记录数: ${recordsToDownload.length}`);

  const progress = loadProgress();
  logger.info(`已完成: ${progress.completed.length} 条, 失败: ${progress.failed.length} 条`);

  // 过滤出未处理的记录
  const pendingRecords = recordsToDownload.filter(r => {
    const key = `${r['企业名称']}_${r['项目名称']}`;
    return !progress.completed.includes(key) && !progress.failed.includes(key);
  });

  logger.info(`剩余 ${pendingRecords.length} 条待下载`);

  if (pendingRecords.length === 0) {
    logger.info('所有记录的 raw_content 文件都已存在');
    process.exit(0);
  }

  const browser = await connectBrowser();
  const page = await openNewPage(browser);

  for (let i = 0; i < pendingRecords.length; i++) {
    const record = pendingRecords[i];
    const companyName = record['企业名称'];
    const projectName = record['项目名称'];
    const detailUrl = record['天眼查详情页链接'];
    const key = `${companyName}_${projectName}`;

    logger.info(`[${i + 1}/${pendingRecords.length}] 下载: ${companyName} - ${projectName}`);

    try {
      const detail = await fetchBiddingDetail(page, detailUrl, projectName);

      if (detail.rawContent) {
        const filePath = saveRawContentToFile(companyName, projectName, detail.rawContent);
        logger.info(`  ✅ 已保存: ${path.basename(filePath)}`);
      } else {
        logger.warn(`  ⚠️ 无内容可保存`);
      }

      // 标记为已完成
      progress.completed.push(key);

    } catch (err) {
      logger.error(`  ❌ 下载失败: ${err.message}`);
      progress.failed.push(key);
    }

    // 保存进度
    saveProgress(progress);

    // 每处理 5 条休息一下
    if ((i + 1) % 5 === 0) {
      logger.info('  休息一下...');
      await delay(5000, 8000);
    } else {
      await delay(3000, 6000);
    }
  }

  await page.close();

  logger.info('=== 补充下载完成 ===');
  logger.info(`总记录数: ${records.length}`);
  logger.info(`需要下载: ${recordsToDownload.length}`);
  logger.info(`成功: ${progress.completed.length}`);
  logger.info(`失败: ${progress.failed.length}`);
  logger.info(`raw_content 目录文件数: ${fs.readdirSync(RAW_CONTENT_DIR).filter(f => f.endsWith('.md')).length}`);
  logger.info('请运行 npm run extract 进行 LLM 结构化提取');
}

main().catch(err => {
  logger.error(`执行失败: ${err.message}`);
  process.exit(1);
});
