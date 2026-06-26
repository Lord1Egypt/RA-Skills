#!/usr/bin/env node

/**
 * 每日新闻简报简化版
 * 每天早上8点自动搜集并发布国际时事、经济形势、科技发展新闻
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

// 配置
const config = {
  newsSources: {
    international: ['https://news.cctv.com/world', 'https://news.sina.com.cn/world'],
    economic: ['https://finance.sina.com.cn'],
    technology: ['https://tech.sina.com.cn']
  },
  schedule: '0 8 * * *',
  timezone: 'Asia/Shanghai'
};

// 优先级关键词
const PRIORITY_KEYWORDS = {
  international: ['特朗普', '访华', '中美', '伊朗', '中东', '欧盟'],
  economic: ['GDP', '通胀', '美联储', '贸易', '股市', '黄金'],
  technology: ['AI', '人工智能', '芯片', '电动', '光伏', '量子']
};

async function fetchNews() {
  console.log('开始获取新闻...');
  
  const newsItems = {
    international: [],
    economic: [],
    technology: []
  };
  
  try {
    // 获取国际新闻
    for (const source of config.newsSources.international) {
      try {
        const items = await fetchFromSource(source, 'international');
        newsItems.international.push(...items);
      } catch (error) {
        console.warn(`国际新闻源 ${source} 获取失败:`, error.message);
      }
    }
    
    // 获取经济新闻
    for (const source of config.newsSources.economic) {
      try {
        const items = await fetchFromSource(source, 'economic');
        newsItems.economic.push(...items);
      } catch (error) {
        console.warn(`经济新闻源 ${source} 获取失败:`, error.message);
      }
    }
    
    // 获取科技新闻
    for (const source of config.newsSources.technology) {
      try {
        const items = await fetchFromSource(source, 'technology');
        newsItems.technology.push(...items);
      } catch (error) {
        console.warn(`科技新闻源 ${source} 获取失败:`, error.message);
      }
    }
    
    console.log('新闻获取完成');
    return newsItems;
  } catch (error) {
    console.error('获取新闻失败:', error.message);
    throw error;
  }
}

async function fetchFromSource(url, category) {
  console.log(`从 ${url} 获取 ${category} 新闻...`);
  
  try {
    const response = await axios.get(url, {
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    const $ = cheerio.load(response.data);
    const newsItems = [];
    
    // 解析新闻链接
    $('a').each((i, elem) => {
      const title = $(elem).text().trim();
      const href = $(elem).attr('href');
      
      if (title && href && href.startsWith('http') && title.length > 10) {
        // 过滤广告
        if (title.includes('广告') || title.includes('推广')) {
          return;
        }
        
        // 计算优先级
        let priority = 0;
        const keywords = PRIORITY_KEYWORDS[category] || [];
        keywords.forEach(keyword => {
          if (title.includes(keyword)) {
            priority += 10;
          }
        });
        
        // 特朗普访华特别权重
        if (title.includes('特朗普') && title.includes('访华')) {
          priority += 50;
        }
        
        newsItems.push({
          title,
          url: href,
          category,
          source: getSourceName(url),
          priority
        });
      }
    });
    
    // 按优先级排序并取前5条
    return newsItems
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 5);
  } catch (error) {
    console.error(`获取 ${url} 失败:`, error.message);
    return [];
  }
}

function getSourceName(url) {
  if (url.includes('sina.com.cn')) return '新浪';
  if (url.includes('cctv.com')) return '央视';
  return '其他';
}

function generateBrief(newsItems) {
  const today = new Date();
  const formattedDate = `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate()}日`;
  const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const dayOfWeek = days[today.getDay()];
  
  let markdown = `# 📰 每日新闻简报 | ${formattedDate} | ${dayOfWeek}\n\n`;
  
  // 国际时事
  markdown += `## 🌍 国际时事\n`;
  if (newsItems.international.length > 0) {
    newsItems.international.forEach((item, index) => {
      markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
    });
  } else {
    markdown += `暂无重要国际新闻\n`;
  }
  markdown += `\n`;
  
  // 经济形势
  markdown += `## 💰 经济形势\n`;
  if (newsItems.economic.length > 0) {
    newsItems.economic.forEach((item, index) => {
      markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
    });
  } else {
    markdown += `暂无重要经济新闻\n`;
  }
  markdown += `\n`;
  
  // 科技发展
  markdown += `## 🔬 科技发展\n`;
  if (newsItems.technology.length > 0) {
    newsItems.technology.forEach((item, index) => {
      markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
    });
  } else {
    markdown += `暂无重要科技新闻\n`;
  }
  markdown += `\n`;
  
  // 今日关注
  markdown += `## 👀 今日关注\n`;
  const allItems = [...newsItems.international, ...newsItems.economic, ...newsItems.technology];
  const highlights = allItems.sort((a, b) => b.priority - a.priority).slice(0, 3);
  if (highlights.length > 0) {
    highlights.forEach(item => {
      markdown += `• ${item.title}\n`;
    });
  }
  markdown += `\n`;
  
  // 历史回顾
  markdown += `## 📚 历史回顾\n`;
  markdown += `• 历史回顾：特朗普上次访华期间签署多项经贸合作协议\n`;
  markdown += `• 历史回顾：中美建交45周年，双边贸易额持续增长\n`;
  markdown += `• 历史回顾：人工智能技术在过去5年实现突破性进展\n`;
  markdown += `\n`;
  
  // 页脚
  markdown += `---\n`;
  markdown += `*简报生成时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}*\n`;
  markdown += `*数据来源：新浪、央视等主流媒体*\n`;
  markdown += `*注：以上新闻基于公开信息整理，具体细节请以官方发布为准*\n`;
  
  return markdown;
}

async function saveToFile(briefMarkdown) {
  const historyDir = path.join(__dirname, 'history');
  if (!fs.existsSync(historyDir)) {
    fs.mkdirSync(historyDir, { recursive: true });
  }
  
  const dateStr = new Date().toISOString().split('T')[0];
  const historyFile = path.join(historyDir, `${dateStr}.md`);
  
  fs.writeFileSync(historyFile, briefMarkdown, 'utf8');
  console.log(`简报已保存到: ${historyFile}`);
  
  // 同时保存到当前目录
  fs.writeFileSync('latest-brief.md', briefMarkdown, 'utf8');
  console.log(`简报已保存到: latest-brief.md`);
}

async function main() {
  console.log('=== 每日新闻简报系统启动 ===');
  console.log(`当前时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  
  try {
    // 1. 获取新闻
    const newsItems = await fetchNews();
    
    // 2. 生成简报
    const briefMarkdown = generateBrief(newsItems);
    
    // 3. 保存简报
    await saveToFile(briefMarkdown);
    
    // 4. 输出到控制台
    console.log('\n' + briefMarkdown);
    
    console.log('=== 每日新闻简报系统完成 ===');
  } catch (error) {
    console.error('系统运行失败:', error);
    process.exit(1);
  }
}

// 立即运行
if (require.main === module) {
  main();
}