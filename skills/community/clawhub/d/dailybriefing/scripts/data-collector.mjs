#!/usr/bin/env node
/**
 * Daily Briefing Data Collector
 * 收集晨报所需数据：天气、限行、新闻
 */

import { execSync } from 'child_process';
import { writeFileSync, readFileSync, mkdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_DIR = join(__dirname, '..', '.cache');
const CACHE_TTL = 30 * 60 * 1000; // 30分钟缓存

// 确保缓存目录存在
if (!existsSync(CACHE_DIR)) {
  mkdirSync(CACHE_DIR, { recursive: true });
}

/**
 * 获取天气数据
 * @param {string} city - 城市名称
 * @returns {Object} 天气数据
 */
export async function getWeather(city = 'Beijing') {
  const cacheFile = join(CACHE_DIR, `weather_${city}.json`);
  
  // 检查缓存
  if (existsSync(cacheFile)) {
    const cache = JSON.parse(readFileSync(cacheFile, 'utf8'));
    if (Date.now() - cache.timestamp < CACHE_TTL) {
      return cache.data;
    }
  }
  
  try {
    // 使用 wttr.in 获取天气
    const cmd = `curl -s 'wttr.in/${city}?format=j1' 2>/dev/null || echo '{}'`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    const response = JSON.parse(output);
    
    // wttr.in 返回的数据可能嵌套在 "data" 字段中
    const data = response.data || response;
    
    if (!data.current_condition || !data.weather) {
      throw new Error('Invalid weather data structure');
    }
    
    const current = data.current_condition[0];
    const today = data.weather[0];
    
    const result = {
      city: city === 'Beijing' ? '北京' : city,
      currentTemp: current.temp_C,
      feelsLike: current.FeelsLikeC,
      maxTemp: today.maxtempC,
      minTemp: today.mintempC,
      condition: translateWeatherCondition(
        current.lang_zh?.[0]?.value || current.weatherDesc?.[0]?.value
      ),
      humidity: current.humidity,
      windSpeed: current.windspeedKmph,
      windDir: current.winddir16Point,
      visibility: current.visibility,
      uvIndex: current.uvIndex,
      sunrise: today.astronomy[0].sunrise,
      sunset: today.astronomy[0].sunset,
      timestamp: Date.now()
    };
    
    // 写入缓存
    writeFileSync(cacheFile, JSON.stringify({ timestamp: Date.now(), data: result }));
    
    return result;
  } catch (error) {
    console.error('Weather fetch error:', error.message);
    return getFallbackWeather();
  }
}

/**
 * 获取穿衣建议
 * @param {Object} weather - 天气数据
 * @returns {string} 穿衣建议
 */
export function getClothingAdvice(weather) {
  const temp = parseInt(weather.currentTemp);
  const maxTemp = parseInt(weather.maxTemp);
  const minTemp = parseInt(weather.minTemp);
  const diff = maxTemp - minTemp;
  
  let advice = '';
  
  if (temp < 0) {
    advice = '严寒天气，建议穿羽绒服、厚毛衣，戴帽子围巾手套，注意保暖防冻。';
  } else if (temp < 10) {
    advice = '天气寒冷，建议穿厚外套/羽绒服，内搭毛衣，注意防寒保暖。';
  } else if (temp < 20) {
    advice = '早晚较凉，建议穿外套+长袖，可采用洋葱式穿搭方便增减衣物。';
  } else if (temp < 28) {
    advice = '气温舒适，建议穿长袖T恤/薄外套，适合户外活动。';
  } else {
    advice = '天气炎热，建议穿短袖、轻薄透气衣物，注意防晒补水。';
  }
  
  if (diff > 10) {
    advice += ' 今日温差较大(' + diff + '°C)，建议携带外套方便穿脱。';
  }
  
  if (weather.humidity > 70) {
    advice += ' 湿度较高，体感可能较闷热。';
  }
  
  return advice;
}

/**
 * 限行规则配置
 */
const WEATHER_CONDITION_MAP = {
  'Clear': '晴朗',
  'Sunny': '晴天',
  'Partly cloudy': '多云',
  'Cloudy': '阴天',
  'Overcast': '阴天',
  'Mist': '薄雾',
  'Fog': '雾',
  'Freezing fog': '冻雾',
  'Patchy rain possible': '可能有阵雨',
  'Patchy snow possible': '可能有阵雪',
  'Patchy sleet possible': '可能有雨夹雪',
  'Patchy freezing drizzle possible': '可能有冻雨',
  'Thundery outbreaks possible': '可能有雷暴',
  'Blowing snow': '吹雪',
  'Blizzard': '暴风雪',
  'Fog': '雾',
  'Freezing fog': '冻雾',
  'Patchy light drizzle': '局部小雨',
  'Light drizzle': '小雨',
  'Freezing drizzle': '冻雨',
  'Heavy freezing drizzle': '大冻雨',
  'Patchy light rain': '局部小雨',
  'Light rain': '小雨',
  'Moderate rain at times': '中雨',
  'Moderate rain': '中雨',
  'Heavy rain at times': '大雨',
  'Heavy rain': '大雨',
  'Light freezing rain': '小冻雨',
  'Moderate or heavy freezing rain': '中到大冻雨',
  'Light sleet': '小雨夹雪',
  'Moderate or heavy sleet': '中到大雨夹雪',
  'Patchy light snow': '局部小雪',
  'Light snow': '小雪',
  'Patchy moderate snow': '局部中雪',
  'Moderate snow': '中雪',
  'Patchy heavy snow': '局部大雪',
  'Heavy snow': '大雪',
  'Ice pellets': '冰粒',
  'Light rain shower': '小阵雨',
  'Moderate or heavy rain shower': '中到大阵雨',
  'Torrential rain shower': '暴雨',
  'Light sleet showers': '小雨夹雪',
  'Moderate or heavy sleet showers': '中到大雨夹雪',
  'Light snow showers': '小雪',
  'Moderate or heavy snow showers': '中到大雪',
  'Light showers of ice pellets': '小冰粒',
  'Moderate or heavy showers of ice pellets': '中到大冰粒',
  'Patchy light rain with thunder': '局部雷雨',
  'Moderate or heavy rain with thunder': '中到大雷雨',
  'Patchy light snow with thunder': '局部雷雪',
  'Moderate or heavy snow with thunder': '中到大雷雪'
};

/**
 * 翻译天气状况为中文
 * @param {string} condition - 英文天气状况
 * @returns {string} 中文天气状况
 */
export function translateWeatherCondition(condition) {
  if (!condition) return '未知';
  return WEATHER_CONDITION_MAP[condition.trim()] || condition;
}

const TRAFFIC_RULES = {
  cycle: {
    start: '2025-12-29',
    end: '2026-03-29'
  },
  // 数组索引对应 JavaScript getDay() 返回值：0=周日, 1=周一, ..., 6=周六
  rules: [
    { day: 0, limits: [], desc: '周日不限行' },
    { day: 1, limits: [3, 8], desc: '周一限行 3 和 8' },
    { day: 2, limits: [4, 9], desc: '周二限行 4 和 9' },
    { day: 3, limits: [5, 0], desc: '周三限行 5 和 0' },
    { day: 4, limits: [1, 6], desc: '周四限行 1 和 6' },
    { day: 5, limits: [2, 7], desc: '周五限行 2 和 7' },
    { day: 6, limits: [], desc: '周六不限行' }
  ],
  time: '07:00-20:00',
  area: '五环路以内道路（不含五环路）'
};

/**
 * 获取限行信息
 * @param {Date} date - 日期对象，默认为今天
 * @param {number} offset - 天数偏移（0=今天，1=明天）
 * @returns {Object} 限行信息
 */
export function getTrafficLimit(date = new Date(), offset = 0) {
  const targetDate = new Date(date);
  targetDate.setDate(targetDate.getDate() + offset);
  
  const dayOfWeek = targetDate.getDay();
  const rule = TRAFFIC_RULES.rules[dayOfWeek];
  const dateStr = targetDate.toLocaleDateString('zh-CN', { 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  });
  
  // 检查是否在限行周期内
  const cycleStart = new Date(TRAFFIC_RULES.cycle.start);
  const cycleEnd = new Date(TRAFFIC_RULES.cycle.end);
  const inCycle = targetDate >= cycleStart && targetDate <= cycleEnd;
  
  return {
    date: dateStr,
    dayOfWeek: dayOfWeek,
    limits: rule.limits,
    limitDesc: rule.desc,
    time: TRAFFIC_RULES.time,
    area: TRAFFIC_RULES.area,
    inCycle: inCycle,
    cycleStart: TRAFFIC_RULES.cycle.start,
    cycleEnd: TRAFFIC_RULES.cycle.end,
    isWorkday: dayOfWeek >= 1 && dayOfWeek <= 5
  };
}

/**
 * 获取新闻数据（使用 kimi_fetch）
 * 注意：此函数在 cron 任务中由智能体调用，实际使用 kimi_fetch 工具
 * @returns {Object} 新闻分类数据
 */
export function getNewsCategories() {
  return {
    international: {
      name: '国际要闻',
      sources: ['news.163.com', 'news.sina.com.cn'],
      keywords: ['国际', '美国', '俄罗斯', '中东', '欧洲', '亚太']
    },
    domestic: {
      name: '国内时政',
      sources: ['news.163.com', 'news.sina.com.cn'],
      keywords: ['两会', '政策', '国务院', '部委', '地方']
    },
    tech: {
      name: '科技动态',
      sources: ['tech.163.com', 'tech.sina.com.cn'],
      keywords: ['AI', '芯片', '华为', '苹果', '小米', '新能源汽车']
    },
    finance: {
      name: '财经市场',
      sources: ['finance.sina.com.cn', 'cls.cn'],
      keywords: ['股市', 'A股', '港股', '美股', '黄金', '原油']
    },
    society: {
      name: '社会热点',
      sources: ['news.163.com', 'news.sina.com.cn'],
      keywords: ['民生', '教育', '医疗', '交通', '消费']
    }
  };
}

/**
 * 格式化天气输出
 * @param {Object} weather - 天气数据
 * @returns {string} 格式化字符串
 */
export function formatWeather(weather) {
  return `🌤️ **${weather.city}今日天气**
• 当前气温：**${weather.currentTemp}°C**（体感 ${weather.feelsLike}°C）
• 最高气温：**${weather.maxTemp}°C**
• 最低气温：**${weather.minTemp}°C**
• 天气状况：**${weather.condition}**
• 湿度：**${weather.humidity}%**
• 风力：**${weather.windDir} ${weather.windSpeed} km/h**
• 能见度：**${weather.visibility} km**
• 日出/日落：**${weather.sunrise} / ${weather.sunset}**

💡 **穿衣建议**：${getClothingAdvice(weather)}`;
}

/**
 * 格式化限行输出
 * @param {Object} limit - 限行信息
 * @returns {string} 格式化字符串
 */
export function formatTrafficLimit(limit) {
  let output = `🚗 **北京尾号限行（${limit.date}）**\n`;
  
  if (!limit.isWorkday) {
    output += `• 今日**不限行**（${limit.limitDesc}）\n`;
  } else {
    output += `• 今日限行尾号：**${limit.limits.join(' 和 ')}**\n`;
  }
  
  output += `• 限行时间：**${limit.time}**\n`;
  output += `• 限行范围：**${limit.area}**\n`;
  output += `• 限行周期：**${limit.cycleStart} 至 ${limit.cycleEnd}**`;
  
  return output;
}

/**
 * 获取备用天气数据（当 API 失败时）
 * @returns {Object} 默认天气数据
 */
function getFallbackWeather() {
  return {
    city: '北京',
    currentTemp: 'N/A',
    feelsLike: 'N/A',
    maxTemp: 'N/A',
    minTemp: 'N/A',
    condition: '获取失败',
    humidity: 'N/A',
    windSpeed: 'N/A',
    windDir: 'N/A',
    visibility: 'N/A',
    uvIndex: 'N/A',
    sunrise: 'N/A',
    sunset: 'N/A',
    timestamp: Date.now(),
    isFallback: true
  };
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    console.log('Daily Briefing Data Collector');
    console.log('=============================');
    
    // 测试天气获取
    console.log('\nFetching weather...');
    const weather = await getWeather('Beijing');
    console.log(formatWeather(weather));
    
    // 测试限行获取
    console.log('\nFetching traffic limit...');
    const limit = getTrafficLimit(new Date(), 0);
    console.log(formatTrafficLimit(limit));
    
    // 显示新闻分类
    console.log('\nNews categories:');
    const categories = getNewsCategories();
    Object.entries(categories).forEach(([key, value]) => {
      console.log(`  ${value.name}: ${value.keywords.slice(0, 3).join(', ')}...`);
    });
  })();
}

export default {
  getWeather,
  getTrafficLimit,
  getNewsCategories,
  formatWeather,
  formatTrafficLimit,
  getClothingAdvice
};
