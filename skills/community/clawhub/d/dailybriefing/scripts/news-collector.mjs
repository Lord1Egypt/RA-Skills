#!/usr/bin/env node
/**
 * News Collector
 * 新闻抓取模块 - 从多个新闻源获取实时新闻
 */

import { execSync } from 'child_process';
import * as cheerio from 'cheerio';
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_DIR = join(__dirname, '..', '.cache');
const CACHE_TTL = 30 * 60 * 1000; // 30分钟缓存

// 确保缓存目录存在
if (!existsSync(CACHE_DIR)) {
  mkdirSync(CACHE_DIR, { recursive: true });
}

/**
 * 使用 curl 获取网页内容
 * @param {string} url - URL
 * @param {Object} options - 选项
 * @returns {string} HTML 内容
 */
function fetchWithCurl(url, options = {}) {
  const { timeout = 15000, userAgent = 'Mozilla/5.0' } = options;
  
  try {
    const cmd = `curl -s -L --max-time ${timeout / 1000} -H "User-Agent: ${userAgent}" "${url}" 2>/dev/null || echo ''`;
    return execSync(cmd, { encoding: 'utf8', timeout });
  } catch (error) {
    console.error(`Fetch error for ${url}:`, error.message);
    return '';
  }
}

/**
 * 解析网易新闻
 * @returns {Array} 新闻列表
 */
export function parseNeteaseNews(html) {
  const $ = cheerio.load(html);
  const news = [];
  
  // 网易新闻首页的头条区域
  $('.mod_top_news2 .news_title a, .top_newslist li a, .hidden-title').each((i, el) => {
    const title = $(el).text().trim();
    const url = $(el).attr('href') || '';
    if (title && title.length > 10 && !title.includes('广告')) {
      news.push({
        source: '网易新闻',
        title: title.replace(/\s+/g, ' '),
        url: url.startsWith('http') ? url : `https://news.163.com${url}`,
        category: guessCategory(title)
      });
    }
  });
  
  return news.slice(0, 15);
}

/**
 * 解析新浪新闻
 * @returns {Array} 新闻列表
 */
export function parseSinaNews(html) {
  const $ = cheerio.load(html);
  const news = [];
  
  // 新浪新闻的各种选择器
  $('.news-item h2 a, .top-news a, .blk_01 a, .newslist a').each((i, el) => {
    const title = $(el).text().trim();
    const url = $(el).attr('href') || '';
    if (title && title.length > 10 && !title.includes('广告') && !title.includes('专题')) {
      news.push({
        source: '新浪新闻',
        title: title.replace(/\s+/g, ' '),
        url: url.startsWith('http') ? url : `https://news.sina.com.cn${url}`,
        category: guessCategory(title)
      });
    }
  });
  
  return news.slice(0, 15);
}

/**
 * 解析搜狐新闻
 * @returns {Array} 新闻列表
 */
export function parseSohuNews(html) {
  const $ = cheerio.load(html);
  const news = [];
  
  // 搜狐新闻的选择器
  $('.news-list .title a, .news-item h4 a, .feed-list a[data-role="title"]').each((i, el) => {
    const title = $(el).text().trim();
    const url = $(el).attr('href') || '';
    if (title && title.length > 10 && !title.includes('广告') && !title.includes('专题')) {
      news.push({
        source: '搜狐新闻',
        title: title.replace(/\s+/g, ' '),
        url: url.startsWith('http') ? url : `https://www.sohu.com${url}`,
        category: guessCategory(title)
      });
    }
  });
  
  return news.slice(0, 10);
}

/**
 * 根据标题猜测新闻分类
 * @param {string} title - 新闻标题
 * @returns {string} 分类
 */
function guessCategory(title) {
  const keywords = {
    international: ['美国', '俄罗斯', '乌克兰', '中东', '伊朗', '以色列', '特朗普', '拜登', '普京', '北约', '欧盟', '日本', '韩国', '朝鲜', '台湾', '香港', '国际', '外交', '战争', '冲突'],
    domestic: ['两会', '国务院', '总理', '主席', '部长', '政策', '中央', '全国人大常委会', '政协', '政府工作报告', '十四五', '二十大'],
    tech: ['AI', '人工智能', '芯片', '华为', '苹果', '小米', '新能源', '电动车', '特斯拉', '比亚迪', '科技', '互联网', '5G', '半导体', '光伏', '储能', '机器人', '大模型'],
    finance: ['股市', 'A股', '港股', '美股', '沪指', '深指', '创业板', '科创板', '黄金', '原油', '美联储', '央行', '降息', '加息', '通胀', 'CPI', 'PPI', 'GDP', '房地产', '楼市', '房价', '人民币', '汇率'],
    society: ['教育', '医疗', '医保', '社保', '就业', '养老', '生育', '人口', '春运', '天气', '地震', '火灾', '事故', '案件', '法院', '警察', '交通', '地铁', '公交']
  };
  
  for (const [category, words] of Object.entries(keywords)) {
    if (words.some(word => title.includes(word))) {
      return category;
    }
  }
  
  return 'other';
}

/**
 * 获取所有新闻
 * @returns {Object} 分类后的新闻
 */
export async function collectNews() {
  const cacheFile = join(CACHE_DIR, 'news.json');
  
  // 检查缓存
  if (existsSync(cacheFile)) {
    try {
      const cache = JSON.parse(readFileSync(cacheFile, 'utf8'));
      if (Date.now() - cache.timestamp < CACHE_TTL) {
        console.log('Using cached news data');
        return cache.data;
      }
    } catch (e) {
      // 缓存解析失败，继续获取新数据
    }
  }
  
  console.log('Fetching news from multiple sources...');
  
  // 并行获取多个新闻源
  const [neteaseHtml, sinaHtml, sohuHtml] = await Promise.all([
    fetchWithCurl('https://news.163.com'),
    fetchWithCurl('https://news.sina.com.cn'),
    fetchWithCurl('https://www.sohu.com')
  ]);
  
  // 解析新闻
  const allNews = [
    ...parseNeteaseNews(neteaseHtml),
    ...parseSinaNews(sinaHtml),
    ...parseSohuNews(sohuHtml)
  ];
  
  // 去重（基于标题相似度）
  const uniqueNews = deduplicateNews(allNews);
  
  // 分类
  const categorized = {
    international: uniqueNews.filter(n => n.category === 'international').slice(0, 5),
    domestic: uniqueNews.filter(n => n.category === 'domestic').slice(0, 5),
    tech: uniqueNews.filter(n => n.category === 'tech').slice(0, 5),
    finance: uniqueNews.filter(n => n.category === 'finance').slice(0, 5),
    society: uniqueNews.filter(n => n.category === 'society').slice(0, 5)
  };
  
  const result = {
    timestamp: Date.now(),
    total: uniqueNews.length,
    categories: categorized,
    all: uniqueNews.slice(0, 30)
  };
  
  // 写入缓存
  writeFileSync(cacheFile, JSON.stringify({ timestamp: Date.now(), data: result }));
  
  return result;
}

/**
 * 简单去重（基于标题相似度）
 * @param {Array} newsList - 新闻列表
 * @returns {Array} 去重后的列表
 */
function deduplicateNews(newsList) {
  const seen = new Set();
  return newsList.filter(news => {
    // 提取标题前15个字符作为指纹
    const fingerprint = news.title.slice(0, 15).replace(/\s/g, '');
    if (seen.has(fingerprint)) {
      return false;
    }
    seen.add(fingerprint);
    return true;
  });
}

/**
 * 格式化新闻输出
 * @param {Object} newsData - 新闻数据
 * @returns {string} 格式化字符串
 */
export function formatNews(newsData) {
  const { categories } = newsData;
  
  let output = '';
  
  const categoryNames = {
    international: '【国际要闻】',
    domestic: '【国内时政】',
    tech: '【科技动态】',
    finance: '【财经市场】',
    society: '【社会热点】'
  };
  
  for (const [key, name] of Object.entries(categoryNames)) {
    const items = categories[key];
    if (items && items.length > 0) {
      output += `\n${name}\n`;
      items.forEach((item, index) => {
        output += `${index + 1}. ${item.title}\n`;
      });
    }
  }
  
  return output || '\n暂无新闻数据\n';
}

/**
 * 获取简化版新闻（用于测试）
 * @returns {string} 简化版新闻
 */
export async function getSimpleNews() {
  try {
    const newsData = await collectNews();
    const lines = [];
    
    Object.entries(newsData.categories).forEach(([category, items]) => {
      if (items.length > 0) {
        const categoryNames = {
          international: '🌍 国际',
          domestic: '🏛️ 国内',
          tech: '💻 科技',
          finance: '💰 财经',
          society: '👥 社会'
        };
        lines.push(`${categoryNames[category] || category}: ${items[0].title.slice(0, 30)}...`);
      }
    });
    
    return lines.join('\n') || '暂无新闻';
  } catch (error) {
    return `新闻获取失败: ${error.message}`;
  }
}

// CLI 测试
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    console.log('Testing news collector...\n');
    
    const newsData = await collectNews();
    console.log(`Total news: ${newsData.total}`);
    console.log(`\nCategorized news:`);
    console.log(formatNews(newsData));
  })();
}

export default {
  collectNews,
  formatNews,
  getSimpleNews,
  parseNeteaseNews,
  parseSinaNews,
  parseSohuNews
};
