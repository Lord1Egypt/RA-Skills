#!/usr/bin/env node

/**
 * 每日新闻简报脚本
 * 每天早上8点自动搜集并发布国际时事、经济形势、科技发展新闻
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const cron = require('node-cron');
const { exec } = require('child_process');
const util = require('util');

// 配置
const configPath = path.join(__dirname, 'config.json');
const config = require(configPath);
const templatePath = path.join(__dirname, 'templates', 'brief-template.md');
const historyDir = path.join(__dirname, 'history');

// 确保历史目录存在
if (!fs.existsSync(historyDir)) {
  fs.mkdirSync(historyDir, { recursive: true });
}

// 新闻源优先级
const PRIORITY_KEYWORDS = {
  international: [
    '特朗普', '访华', '中美', '贸易', '外交',
    '伊朗', '以色列', '中东', '冲突',
    '欧盟', '英国', '脱欧',
    '朝鲜', '台海', '南海',
    '联合国', '气候', '疫情'
  ],
  economic: [
    'GDP', '通胀', '就业', '经济',
    '美联储', '央行', '利率',
    '贸易', '投资', '外资',
    '新能源', '数字', '制造',
    '股市', '汇市', '黄金', '白银'
  ],
  technology: [
    'AI', '人工智能', '大模型',
    '芯片', '半导体', '制造',
    '电动', '汽车', '光伏', '储能',
    '基因', '医疗', '生物',
    '航天', '卫星', '太空'
  ]
};

// 历史模式关键词（基于用户提到的特朗普访华等）
const HISTORICAL_PATTERNS = [
  '特朗普访华',
  '中美关系',
  '贸易谈判',
  '科技竞争',
  '半导体',
  '新能源',
  '中东局势',
  '俄乌冲突'
];

class NewsFetcher {
  constructor() {
    this.newsItems = {
      international: [],
      economic: [],
      technology: []
    };
  }

  async fetchNews() {
    console.log('开始获取新闻...');
    
    try {
      // 并行获取各类新闻
      await Promise.all([
        this.fetchInternationalNews(),
        this.fetchEconomicNews(),
        this.fetchTechnologyNews()
      ]);
      
      console.log('新闻获取完成');
      return this.newsItems;
    } catch (error) {
      console.error('获取新闻失败:', error.message);
      throw error;
    }
  }

  async fetchInternationalNews() {
    const sources = config.newsSources.international;
    for (const source of sources) {
      try {
        const news = await this.fetchFromSource(source, 'international');
        this.newsItems.international.push(...news);
      } catch (error) {
        console.warn(`国际新闻源 ${source} 获取失败:`, error.message);
      }
    }
  }

  async fetchEconomicNews() {
    const sources = config.newsSources.economic;
    for (const source of sources) {
      try {
        const news = await this.fetchFromSource(source, 'economic');
        this.newsItems.economic.push(...news);
      } catch (error) {
        console.warn(`经济新闻源 ${source} 获取失败:`, error.message);
      }
    }
  }

  async fetchTechnologyNews() {
    const sources = config.newsSources.technology;
    for (const source of sources) {
      try {
        const news = await this.fetchFromSource(source, 'technology');
        this.newsItems.technology.push(...news);
      } catch (error) {
        console.warn(`科技新闻源 ${source} 获取失败:`, error.message);
      }
    }
  }

  async fetchFromSource(url, category) {
    console.log(`从 ${url} 获取 ${category} 新闻...`);
    
    const response = await axios.get(url, {
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    const $ = cheerio.load(response.data);
    const newsItems = [];
    
    // 根据不同网站结构解析新闻
    if (url.includes('sina.com.cn')) {
      newsItems.push(...this.parseSinaNews($, category));
    } else if (url.includes('cctv.com')) {
      newsItems.push(...this.parseCCTVNews($, category));
    } else {
      newsItems.push(...this.parseGenericNews($, category));
    }
    
    // 根据优先级关键词排序
    return this.sortByPriority(newsItems, category);
  }

  parseSinaNews($, category) {
    const newsItems = [];
    
    // 解析新浪新闻
    $('a').each((i, elem) => {
      const title = $(elem).text().trim();
      const href = $(elem).attr('href');
      
      if (title && href && href.startsWith('http')) {
        // 过滤广告和无关链接
        if (title.length > 10 && !this.isAdvertisement(title)) {
          newsItems.push({
            title,
            url: href,
            category,
            source: '新浪',
            timestamp: new Date().toISOString(),
            priority: this.calculatePriority(title, category)
          });
        }
      }
    });
    
    return newsItems;
  }

  parseCCTVNews($, category) {
    const newsItems = [];
    
    // 解析央视新闻
    $('a').each((i, elem) => {
      const title = $(elem).text().trim();
      const href = $(elem).attr('href');
      
      if (title && href && href.includes('ARTI')) {
        newsItems.push({
          title,
          url: href.startsWith('http') ? href : `https://news.cctv.com${href}`,
          category,
          source: '央视',
          timestamp: new Date().toISOString(),
          priority: this.calculatePriority(title, category)
        });
      }
    });
    
    return newsItems;
  }

  parseGenericNews($, category) {
    const newsItems = [];
    
    // 通用解析逻辑
    $('h1, h2, h3, h4').each((i, elem) => {
      const title = $(elem).text().trim();
      const link = $(elem).find('a').first();
      const href = link.attr('href');
      
      if (title && href) {
        newsItems.push({
          title,
          url: href.startsWith('http') ? href : `https://${new URL(config.newsSources[category][0]).hostname}${href}`,
          category,
          source: '其他',
          timestamp: new Date().toISOString(),
          priority: this.calculatePriority(title, category)
        });
      }
    });
    
    return newsItems;
  }

  isAdvertisement(title) {
    const adKeywords = ['广告', '推广', '赞助', 'ADVERTISEMENT', 'SPONSORED'];
    return adKeywords.some(keyword => title.includes(keyword));
  }

  calculatePriority(title, category) {
    let priority = 0;
    const keywords = PRIORITY_KEYWORDS[category] || [];
    
    // 基础优先级
    keywords.forEach(keyword => {
      if (title.includes(keyword)) {
        priority += 10;
      }
    });
    
    // 历史模式匹配
    HISTORICAL_PATTERNS.forEach(pattern => {
      if (title.includes(pattern)) {
        priority += 20;
      }
    });
    
    // 特朗普访华相关特别权重
    if (title.includes('特朗普') && title.includes('访华')) {
      priority += 50;
    }
    
    // 长度权重（避免过短标题）
    if (title.length > 20) {
      priority += 5;
    }
    
    return priority;
  }

  sortByPriority(newsItems, category) {
    return newsItems
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 10); // 每个类别最多取10条
  }
}

class NewsBriefGenerator {
  constructor() {
    this.today = new Date();
    this.formattedDate = this.formatDate(this.today);
    this.dayOfWeek = this.getDayOfWeek(this.today);
  }

  formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}年${month}月${day}日`;
  }

  getDayOfWeek(date) {
    const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    return days[date.getDay()];
  }

  generateBrief(newsItems) {
    console.log('生成新闻简报...');
    
    const brief = {
      title: `📰 每日新闻简报 | ${this.formattedDate} | ${this.dayOfWeek}`,
      sections: {
        international: this.filterAndFormat(newsItems.international, 'international'),
        economic: this.filterAndFormat(newsItems.economic, 'economic'),
        technology: this.filterAndFormat(newsItems.technology, 'technology')
      },
      highlights: this.generateHighlights(newsItems),
      historicalContext: this.generateHistoricalContext()
    };
    
    return this.formatAsMarkdown(brief);
  }

  filterAndFormat(items, category) {
    // 去重
    const uniqueItems = this.removeDuplicates(items);
    
    // 取前5条
    return uniqueItems.slice(0, 5).map(item => ({
      title: item.title,
      url: item.url,
      source: item.source,
      priority: item.priority
    }));
  }

  removeDuplicates(items) {
    const seen = new Set();
    return items.filter(item => {
      const key = `${item.title}-${item.source}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  generateHighlights(newsItems) {
    const allItems = [
      ...newsItems.international,
      ...newsItems.economic,
      ...newsItems.technology
    ];
    
    // 找出优先级最高的3条新闻
    return allItems
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 3)
      .map(item => item.title);
  }

  generateHistoricalContext() {
    const contexts = [];
    
    // 基于历史模式生成相关历史回顾
    if (config.historicalPatterns.trumpVisit) {
      contexts.push('• 历史回顾：特朗普上次访华期间签署多项经贸合作协议');
    }
    
    if (config.historicalPatterns.usChinaRelations) {
      contexts.push('• 历史回顾：中美建交45周年，双边贸易额持续增长');
    }
    
    if (config.historicalPatterns.middleEastTensions) {
      contexts.push('• 历史回顾：中东和平进程历经多次谈判与冲突');
    }
    
    if (config.historicalPatterns.aiDevelopment) {
      contexts.push('• 历史回顾：人工智能技术在过去5年实现突破性进展');
    }
    
    if (config.historicalPatterns.economicPolicies) {
      contexts.push('• 历史回顾：中国新能源政策推动产业快速发展');
    }
    
    return contexts;
  }

  formatAsMarkdown(brief) {
    let markdown = `# ${brief.title}\n\n`;
    
    // 国际时事
    markdown += `## 🌍 国际时事\n`;
    if (brief.sections.international.length > 0) {
      brief.sections.international.forEach((item, index) => {
        markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
      });
    } else {
      markdown += `暂无重要国际新闻\n`;
    }
    markdown += `\n`;
    
    // 经济形势
    markdown += `## 💰 经济形势\n`;
    if (brief.sections.economic.length > 0) {
      brief.sections.economic.forEach((item, index) => {
        markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
      });
    } else {
      markdown += `暂无重要经济新闻\n`;
    }
    markdown += `\n`;
    
    // 科技发展
    markdown += `## 🔬 科技发展\n`;
    if (brief.sections.technology.length > 0) {
      brief.sections.technology.forEach((item, index) => {
        markdown += `${index + 1}. **${item.title}** [${item.source}](${item.url})\n`;
      });
    } else {
      markdown += `暂无重要科技新闻\n`;
    }
    markdown += `\n`;
    
    // 今日关注
    markdown += `## 👀 今日关注\n`;
    if (brief.highlights.length > 0) {
      brief.highlights.forEach((highlight, index) => {
        markdown += `• ${highlight}\n`;
      });
    }
    markdown += `\n`;
    
    // 历史回顾
    markdown += `## 📚 历史回顾\n`;
    if (brief.historicalContext.length > 0) {
      brief.historicalContext.forEach(context => {
        markdown += `${context}\n`;
      });
    }
    markdown += `\n`;
    
    // 页脚
    markdown += `---\n`;
    markdown += `*简报生成时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}*\n`;
    markdown += `*数据来源：${Object.values(config.newsSources).flat().join(', ')}*\n`;
    markdown += `*注：以上新闻基于公开信息整理，具体细节请以官方发布为准*\n`;
    
    return markdown;
  }
}

class NewsPublisher {
  constructor() {
    this.execPromise = util.promisify(exec);
  }

  async publish(briefMarkdown) {
    console.log('发布新闻简报...');
    
    try {
      // 保存到历史文件
      await this.saveToHistory(briefMarkdown);
      
      // 发布到配置的渠道
      for (const channel of config.outputChannels) {
        await this.publishToChannel(channel, briefMarkdown);
      }
      
      console.log('新闻简报发布完成');
    } catch (error) {
      console.error('发布失败:', error.message);
      throw error;
    }
  }

  async saveToHistory(briefMarkdown) {
    const dateStr = new Date().toISOString().split('T')[0];
    const historyFile = path.join(historyDir, `${dateStr}.md`);
    
    fs.writeFileSync(historyFile, briefMarkdown, 'utf8');
    console.log(`简报已保存到历史文件: ${historyFile}`);
  }

  async publishToChannel(channel, briefMarkdown) {
    switch (channel) {
      case 'feishu':
        await this.publishToFeishu(briefMarkdown);
        break;
      case 'wechat':
        await this.publishToWechat(briefMarkdown);
        break;
      case 'console':
        console.log('\n' + briefMarkdown);
        break;
      default:
        console.warn(`未知的发布渠道: ${channel}`);
    }
  }

  async publishToFeishu(briefMarkdown) {
    console.log('发布到飞书...');
    
    // 使用OpenClaw的feishu_doc工具
    // 这里需要根据实际配置调整
    try {
      // 简化版：先输出到控制台
      console.log('飞书发布功能需要配置OpenClaw Feishu集成');
      console.log('简报内容已准备好，可以通过手动复制或配置自动发布');
    } catch (error) {
      console.error('飞书发布失败:', error.message);
    }
  }

  async publishToWechat(briefMarkdown) {
    console.log('发布到微信...');
    
    // 微信发布逻辑
    // 需要配置微信机器人或API
    console.log('微信发布功能需要配置微信机器人');
  }
}

// 主函数
async function main() {
  console.log('=== 每日新闻简报系统启动 ===');
  console.log(`当前时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  
  try {
    // 1. 获取新闻
    const fetcher = new NewsFetcher();
    const newsItems = await fetcher.fetchNews();
    
    // 2. 生成简报
    const generator = new NewsBriefGenerator();
    const briefMarkdown = generator.generateBrief(newsItems);
    
    // 3. 发布简报
    const publisher = new NewsPublisher();
    await publisher.publish(briefMarkdown);
    
    console.log('=== 每日新闻简报系统完成 ===');
  } catch (error) {
    console.error('系统运行失败:', error);
    process.exit(1);
  }
}

// 定时任务设置
function setupCronJob() {
  console.log('设置定时任务...');
  
  // 解析cron表达式
  const task = cron.schedule(config.schedule, async () => {
    console.log(`定时任务触发: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
    await main();
  }, {
    scheduled: true,
    timezone: config.timezone
  });
  
  task.start();
  console.log(`定时任务已设置: ${config.schedule} (${config.timezone})`);
  
  // 立即运行一次（测试用）
  console.log('立即运行一次测试...');
  main();
}

// 命令行参数处理
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--setup-cron')) {
    setupCronJob();
  } else if (args.includes('--run-now')) {
    main();
  } else {
    console.log('使用方法:');
    console.log('  node news-brief.js --run-now      # 立即运行一次');
    console.log('  node news-brief.js --setup-cron   # 设置定时任务');
  }
}