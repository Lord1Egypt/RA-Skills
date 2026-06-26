#!/usr/bin/env node
/**
 * News Search Module
 * 按规则搜索和整理新闻：国际5条、科技5条、互联网5条、热点5条
 */

import { kimi_search } from 'kimi-search';

/**
 * 按分类搜索新闻
 * @param {string} category - 分类名称
 * @param {string} query - 搜索关键词
 * @param {number} limit - 获取条数
 * @returns {Array} 新闻列表
 */
async function searchNewsByCategory(category, query, limit = 5) {
  try {
    // 使用 kimi_search 搜索
    const results = await kimi_search({
      query: query,
      limit: limit + 2, // 多获取几条用于过滤
      freshness: 'day'
    });
    
    return results.map(item => ({
      category: category,
      title: item.title,
      summary: item.summary || item.snippet || '',
      url: item.url,
      date: item.date || new Date().toISOString().split('T')[0],
      source: item.source || '网络'
    }));
  } catch (error) {
    console.error(`Search error for ${category}:`, error.message);
    return [];
  }
}

/**
 * 过滤重复新闻
 * @param {Array} newsList - 新闻列表
 * @returns {Array} 去重后的新闻
 */
function filterDuplicates(newsList) {
  const seen = new Set();
  return newsList.filter(item => {
    // 基于标题相似度去重
    const key = item.title.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '').substring(0, 15);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * 收集所有分类新闻
 * @returns {Object} 分类新闻数据
 */
export async function collectNewsByCategories() {
  const today = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  
  // 并行搜索所有分类
  const [
    internationalNews,
    techNews,
    internetNews,
    hotNews
  ] = await Promise.all([
    // 国际新闻 5条
    searchNewsByCategory('international', `国际新闻 全球 ${today}`, 5),
    // 科技新闻 5条
    searchNewsByCategory('tech', `科技新闻 AI 人工智能 ${today}`, 5),
    // 互联网 5条
    searchNewsByCategory('internet', `互联网 产业 ${today}`, 5),
    // 热点事件 5条
    searchNewsByCategory('hot', `今日热点 社会 ${today}`, 5)
  ]);
  
  // 合并并去重
  const allNews = [
    ...internationalNews,
    ...techNews,
    ...internetNews,
    ...hotNews
  ];
  
  const uniqueNews = filterDuplicates(allNews);
  
  // 按分类重新组织
  const categorized = {
    international: uniqueNews.filter(n => n.category === 'international').slice(0, 5),
    tech: uniqueNews.filter(n => n.category === 'tech').slice(0, 5),
    internet: uniqueNews.filter(n => n.category === 'internet').slice(0, 5),
    hot: uniqueNews.filter(n => n.category === 'hot').slice(0, 5)
  };
  
  return {
    categories: categorized,
    total: categorized.international.length + categorized.tech.length + 
           categorized.internet.length + categorized.hot.length,
    generatedAt: new Date().toISOString()
  };
}

/**
 * 格式化新闻为简报格式
 * @param {Object} newsData - 新闻数据
 * @returns {string} 格式化的新闻内容
 */
export function formatNewsByCategories(newsData) {
  const { categories } = newsData;
  let output = '';
  
  // 国际新闻
  if (categories.international.length > 0) {
    output += '\n**🌍 国际新闻（5条）**\n';
    categories.international.forEach((item, index) => {
      output += `${index + 1}. **${item.title}**\n`;
      if (item.summary) {
        output += `   ${item.summary.substring(0, 80)}${item.summary.length > 80 ? '...' : ''}\n`;
      }
    });
  }
  
  // 科技新闻
  if (categories.tech.length > 0) {
    output += '\n**💻 科技新闻（5条）**\n';
    categories.tech.forEach((item, index) => {
      output += `${index + 1}. **${item.title}**\n`;
      if (item.summary) {
        output += `   ${item.summary.substring(0, 80)}${item.summary.length > 80 ? '...' : ''}\n`;
      }
    });
  }
  
  // 互联网
  if (categories.internet.length > 0) {
    output += '\n**🌐 互联网/产业（5条）**\n';
    categories.internet.forEach((item, index) => {
      output += `${index + 1}. **${item.title}**\n`;
      if (item.summary) {
        output += `   ${item.summary.substring(0, 80)}${item.summary.length > 80 ? '...' : ''}\n`;
      }
    });
  }
  
  // 热点事件
  if (categories.hot.length > 0) {
    output += '\n**🔥 热点事件（5条）**\n';
    categories.hot.forEach((item, index) => {
      output += `${index + 1}. **${item.title}**\n`;
      if (item.summary) {
        output += `   ${item.summary.substring(0, 80)}${item.summary.length > 80 ? '...' : ''}\n`;
      }
    });
  }
  
  return output;
}

// CLI 测试用法
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    console.log('Searching news by categories...\n');
    const newsData = await collectNewsByCategories();
    console.log(`Total news: ${newsData.total}`);
    console.log(formatNewsByCategories(newsData));
  })();
}

export default {
  collectNewsByCategories,
  formatNewsByCategories
};