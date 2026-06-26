import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { logger } from '../utils/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '../..');

// 海外城市关键词 — 匹配到则跳过
const OVERSEAS_KEYWORDS = [
  '美国', '英国', '德国', '法国', '日本', '韩国', '挪威',
  '加州', '德州', '俄勒冈', '马萨诸塞', '宾州', '伦敦',
  '香港', '澳门', '台湾',
];

/**
 * 解析 具身智能中游企业数据库.md 文件，提取企业列表
 * @returns {Array<{index, name, field, product, city, isOverseas}>}
 */
export function parseCompanyList() {
  const mdPath = path.join(projectRoot, '具身智能中游企业数据库.md');
  
  if (!fs.existsSync(mdPath)) {
    logger.error(`文件不存在: ${mdPath}`);
    throw new Error('企业名单文件不存在');
  }

  const content = fs.readFileSync(mdPath, 'utf-8');
  const lines = content.split('\n');
  const companies = [];

  for (const line of lines) {
    // 跳过表头和分隔线
    if (!line.startsWith('|') || line.includes('索引') || line.includes('---')) continue;

    const cols = line.split('|').map(c => c.trim()).filter(c => c);
    if (cols.length < 5) continue;

    const [index, name, field, product, city] = cols;
    const indexNum = parseInt(index);
    if (isNaN(indexNum)) continue;

    const isOverseas = OVERSEAS_KEYWORDS.some(kw => city.includes(kw));

    companies.push({
      index: indexNum,
      name: name.trim(),
      field: field.trim(),
      product: product.trim(),
      city: city.trim(),
      isOverseas,
    });
  }

  const domesticCount = companies.filter(c => !c.isOverseas).length;
  const overseasCount = companies.filter(c => c.isOverseas).length;
  
  logger.info(`解析企业名单完成: 共 ${companies.length} 家，国内 ${domesticCount} 家，海外/港澳台 ${overseasCount} 家(将跳过)`);
  
  return companies;
}

/**
 * 获取需要在天眼查搜索的企业列表（排除海外）
 */
export function getDomesticCompanies() {
  return parseCompanyList().filter(c => !c.isOverseas);
}
