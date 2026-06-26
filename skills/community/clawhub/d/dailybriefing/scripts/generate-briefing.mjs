#!/usr/bin/env node
/**
 * Daily Briefing Generator
 * 生成每日晨报（天气、限行、新闻）
 */

import { 
  getWeather, 
  getTrafficLimit, 
  formatWeather, 
  formatTrafficLimit 
} from './data-collector.mjs';

import { collectNews, formatNews } from './news-collector.mjs';

/**
 * 生成完整晨报（包含新闻）
 * @param {Object} options - 配置选项
 * @param {string} options.city - 城市（默认北京）
 * @param {number} options.dayOffset - 天数偏移（0=今天，1=明天）
 * @param {boolean} options.includeNews - 是否包含新闻（默认true）
 * @returns {string} 格式化晨报
 */
export async function generateBriefing(options = {}) {
  const { 
    city = 'Beijing', 
    dayOffset = 0,
    includeNews = true
  } = options;
  
  const date = new Date();
  date.setDate(date.getDate() + dayOffset);
  
  const dateStr = date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
  
  // 获取天气数据
  const weather = await getWeather(city);
  
  // 获取限行数据
  const trafficLimit = getTrafficLimit(date, 0);
  
  // 获取新闻数据
  let newsContent = '';
  let newsStats = { total: 0 };
  
  if (includeNews) {
    try {
      const newsData = await collectNews();
      newsContent = formatNews(newsData);
      newsStats = { total: newsData.total };
    } catch (error) {
      console.error('News fetch error:', error.message);
      newsContent = '\n📰 新闻获取失败，请稍后重试\n';
    }
  }
  
  // 构建输出
  let output = `📅 **${dateStr} ${dayOffset === 0 ? '今日' : '次日'}简报**\n`;
  output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  
  // 天气部分
  output += formatWeather(weather);
  output += '\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
  
  // 限行部分
  output += formatTrafficLimit(trafficLimit);
  
  // 新闻部分
  if (includeNews) {
    output += '\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
    output += `📰 **今日要闻精选**\n`;
    output += newsContent;
  }
  
  output += '\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
  output += `📊 **简报统计**\n`;
  output += `• 天气数据：${weather.isFallback ? '⚠️ 使用备用数据' : '✅ 实时获取'}\n`;
  output += `• 限行信息：✅ 已获取\n`;
  if (includeNews) {
    output += `• 新闻条数：${newsStats.total > 0 ? '✅ ' + newsStats.total + '条' : '⚠️ 获取失败'}\n`;
  }
  output += `• 生成时间：${new Date().toLocaleString('zh-CN')}\n`;
  
  return output;
}

/**
 * 生成简化版简报（仅天气+限行）
 * @param {Object} options - 配置选项
 * @returns {string} 格式化简报
 */
export async function generateSimpleBriefing(options = {}) {
  const { city = 'Beijing', dayOffset = 0 } = options;
  
  const date = new Date();
  date.setDate(date.getDate() + dayOffset);
  
  const dateStr = date.toLocaleDateString('zh-CN', {
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
  
  const weather = await getWeather(city);
  const trafficLimit = getTrafficLimit(date, 0);
  
  let output = `🌤️ **${dateStr}**\n`;
  output += `• 天气：${weather.condition} ${weather.currentTemp}°C（${weather.minTemp}°C~${weather.maxTemp}°C）\n`;
  
  if (trafficLimit.isWorkday) {
    output += `• 限行：尾号 ${trafficLimit.limits.join('、')}`;
  } else {
    output += `• 限行：今日不限行`;
  }
  
  return output;
}

/**
 * 生成 JSON 格式数据（供其他脚本使用）
 * @param {Object} options - 配置选项
 * @returns {Object} 结构化数据
 */
export async function generateBriefingData(options = {}) {
  const { city = 'Beijing', dayOffset = 0 } = options;
  
  const date = new Date();
  date.setDate(date.getDate() + dayOffset);
  
  const [weather, newsData] = await Promise.all([
    getWeather(city),
    collectNews().catch(() => null)
  ]);
  
  const trafficLimit = getTrafficLimit(date, 0);
  
  return {
    date: date.toISOString(),
    dateStr: date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long'
    }),
    dayOffset: dayOffset,
    weather: weather,
    trafficLimit: trafficLimit,
    news: newsData,
    generatedAt: new Date().toISOString()
  };
}

// CLI 用法
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    const args = process.argv.slice(2);
    const format = args.includes('--json') ? 'json' : 'text';
    const simple = args.includes('--simple');
    const tomorrow = args.includes('--tomorrow');
    const noNews = args.includes('--no-news');
    const dayOffset = tomorrow ? 1 : 0;
    
    console.log('Generating daily briefing...\n');
    
    if (format === 'json') {
      const data = await generateBriefingData({ dayOffset });
      console.log(JSON.stringify(data, null, 2));
    } else if (simple) {
      const briefing = await generateSimpleBriefing({ dayOffset });
      console.log(briefing);
    } else {
      const briefing = await generateBriefing({ dayOffset, includeNews: !noNews });
      console.log(briefing);
    }
  })();
}

export default {
  generateBriefing,
  generateSimpleBriefing,
  generateBriefingData
};
