#!/usr/bin/env node
/**
 * 每日神价推送 - 报告生成器 v2
 * 通过什么值得买聚合各平台优惠（更可靠）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置 - 什么值得买各平台汇总页
const CONFIG = {
  platforms: [
    { name: '京东', url: 'https://faxian.smzdm.com/h3s183t0f0c0p1/', keyword: '数码' },  // 京东好价
    { name: '拼多多', url: 'https://faxian.smzdm.com/h3s8645t0f0c0p1/', keyword: '百亿补贴' },  // 拼多多
    { name: '天猫', url: 'https://faxian.smzdm.com/h3s247t0f0c0p1/', keyword: '天猫' },  // 天猫
    { name: '淘宝', url: 'https://faxian.smzdm.com/h3s241t0f0c0p1/', keyword: '淘宝' }  // 聚划算
  ],
  categories: {
    digital: { name: '数码', keywords: ['iPhone', 'iPad', 'MacBook', '显卡', '手机', '电脑', '耳机', '路由器', '显示器', '相机'] },
    clothing: { name: '服饰', keywords: ['优衣库', '羽绒服', 'T 恤', '裤子', '鞋', '运动'] },
    home: { name: '家居', keywords: ['净化器', '扫地机', '电饭煲', '床垫', '家具'] },
    food: { name: '食品', keywords: ['牛奶', '零食', '饮料', '水果', '生鲜'] }
  },
  topN: 15
};

// 抓取单个页面
function scrapePage(platformName, url, keyword) {
  const deals = [];
  const scraperPath = '/home/gaof/.openclaw/skills/anti-bot-scraper-1.0.0/scripts/scraper-stealth.js';
  const parserPath = path.join(__dirname, 'parse-smzdm.py');
  
  try {
    console.log(`🔍 抓取${platformName}：${keyword}`);
    const htmlPath = `/tmp/deal_${platformName}_${keyword}.html`;
    
    const cmd = `node ${scraperPath} "${url}" --wait 3000 --html ${htmlPath}`;
    execSync(cmd, { timeout: 60000, stdio: 'pipe' });
    
    const result = execSync(`python3 ${parserPath} ${htmlPath}`, { encoding: 'utf8' });
    const parsed = JSON.parse(result.trim());
    
    parsed.forEach(d => {
      d.platform = platformName;
      d.source = platformName;
    });
    
    return parsed.slice(0, 8);  // 每平台最多 8 个
    
  } catch (e) {
    console.error(`   ❌ 抓取${platformName}失败:`, e.message);
    return [];
  }
}

// 去重
function deduplicateDeals(deals) {
  const seen = new Set();
  return deals.filter(d => {
    const key = d.title.substring(0, 25) + d.price.replace(/\D/g, '');
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

// 分类
function categorizeDeals(deals) {
  const categorized = { digital: [], clothing: [], home: [], food: [], other: [] };
  
  deals.forEach(d => {
    let matched = false;
    for (const [key, cat] of Object.entries(CONFIG.categories)) {
      if (cat.keywords.some(kw => d.title.toLowerCase().includes(kw.toLowerCase()))) {
        categorized[key].push(d);
        matched = true;
        break;
      }
    }
    if (!matched) categorized.other.push(d);
  });
  
  return categorized;
}

// 生成报告
function generateReport(categorizedDeals) {
  const today = new Date().toISOString().split('T')[0];
  const weekday = new Date().toLocaleDateString('zh-CN', { weekday: 'long' });
  
  let report = `🔥 每日神价日报 ${today} ${weekday}\n\n`;
  report += `📊 数据来源：什么值得买聚合（京东/拼多多/天猫/淘宝）\n\n`;
  
  let rank = 1;
  let totalDeals = 0;
  
  // 数码类优先
  const priority = ['digital', 'clothing', 'home', 'food', 'other'];
  
  for (const key of priority) {
    const deals = categorizedDeals[key];
    if (deals.length === 0) continue;
    
    const catName = CONFIG.categories[key]?.name || '其他';
    report += `【${catName}】\n`;
    
    for (const deal of deals.slice(0, 5)) {
      report += `${rank}. ${deal.title}\n`;
      report += `   💰 ${deal.price}\n`;
      report += `   🛒 ${deal.platform}\n`;
      report += `   🔗 ${deal.url}\n\n`;
      
      rank++;
      totalDeals++;
    }
  }
  
  report += `📊 今日统计：\n`;
  report += `- 神价数量：${totalDeals}\n`;
  report += `- 覆盖平台：京东/拼多多/天猫/淘宝\n\n`;
  
  report += `💡 购物建议：\n`;
  report += `1. 关注"绝对值""手慢无"标签\n`;
  report += `2. 拼多多百亿补贴需验货\n`;
  report += `3. 京东注意保价政策\n`;
  report += `4. 比价后下单更划算\n\n`;
  
  report += `⚠️ 免责声明：仅供参考，不构成投资建议`;
  
  return report;
}

// 主函数
async function main() {
  console.log('🚀 开始生成每日神价报告...\n');
  
  // 抓取各平台
  console.log('📡 抓取全网优惠...\n');
  
  let allDeals = [];
  
  for (const platform of CONFIG.platforms) {
    const deals = scrapePage(platform.name, platform.url, platform.keyword);
    console.log(`✅ ${platform.name}：${deals.length} 个商品`);
    allDeals.push(...deals);
  }
  
  // 去重
  allDeals = deduplicateDeals(allDeals);
  console.log(`\n✅ 去重后：${allDeals.length} 个商品\n`);
  
  // 分类
  console.log('📂 分类整理...');
  const categorized = categorizeDeals(allDeals);
  
  // 生成报告
  console.log('📝 生成报告...');
  const report = generateReport(categorized);
  
  // 保存报告
  const reportPath = path.join(__dirname, '../assets/daily-report.txt');
  fs.writeFileSync(reportPath, report);
  
  console.log('\n✅ 报告生成完成！');
  console.log(`📄 保存路径：${reportPath}`);
  console.log('\n--- 报告预览 ---\n');
  console.log(report);
}

main().catch(console.error);
