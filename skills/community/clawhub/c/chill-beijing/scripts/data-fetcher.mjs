#!/usr/bin/env node
/**
 * Data Fetcher - 数据抓取模块
 * 抓取天气、猫眼、大麦、美团、小红书数据
 */

import puppeteer from 'puppeteer';

const TIMEOUT = 60000; // 60秒超时
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';

/**
 * 获取天气数据（今日+次日）
 * @returns {Object} 天气信息
 */
export async function fetchWeather() {
  console.log('[天气] 开始获取北京天气...');
  
  try {
    const response = await fetch('https://wttr.in/Beijing?format=j1', {
      headers: { 'User-Agent': USER_AGENT }
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    const data = await response.json();
    const current = data.current_condition[0];
    const today = data.weather[0];
    const tomorrow = data.weather[1];
    
    return {
      today: {
        temp: current.temp_C,
        feelsLike: current.FeelsLikeC,
        condition: current.lang_zh[0]?.value || current.weatherDesc[0].value,
        humidity: current.humidity,
        wind: current.windspeedKmph,
        maxTemp: today.maxtempC,
        minTemp: today.mintempC
      },
      tomorrow: {
        maxTemp: tomorrow.maxtempC,
        minTemp: tomorrow.mintempC,
        condition: tomorrow.hourly[12]?.lang_zh[0]?.value || tomorrow.hourly[12]?.weatherDesc[0]?.value || '未知',
        chanceOfRain: tomorrow.hourly[12]?.chanceofrain || '0'
      },
      source: 'wttr.in'
    };
  } catch (error) {
    console.error('[天气] 获取失败:', error.message);
    return {
      today: { temp: '--', condition: '获取失败' },
      tomorrow: { maxTemp: '--', minTemp: '--', condition: '未知' }
    };
  }
}

/**
 * 获取当日日期字符串
 */
function getTodayString() {
  const date = new Date();
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '-');
}

/**
 * 抓取猫眼电影数据
 * @returns {Array} 电影列表
 */
export async function fetchMaoyanMovies() {
  console.log('[猫眼] 开始抓取电影数据...');
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent(USER_AGENT);
    await page.setViewport({ width: 1920, height: 1080 });
    
    // 猫眼北京正在热映
    await page.goto('https://maoyan.com/films?showType=1&offset=0&limit=10', {
      waitUntil: 'networkidle2',
      timeout: TIMEOUT
    });
    
    // 等待电影列表加载
    await page.waitForSelector('.movie-list', { timeout: TIMEOUT });
    
    const movies = await page.evaluate(() => {
      const items = document.querySelectorAll('.movie-list .movie-item');
      return Array.from(items).slice(0, 5).map(item => {
        const title = item.querySelector('.movie-title')?.textContent?.trim();
        const rating = item.querySelector('.movie-rating')?.textContent?.trim();
        const tags = item.querySelector('.movie-tags')?.textContent?.trim();
        return { title, rating, tags, source: '猫眼' };
      }).filter(m => m.title);
    });
    
    console.log(`[猫眼] 成功抓取 ${movies.length} 部电影`);
    return movies;
    
  } catch (error) {
    console.error('[猫眼] 抓取失败:', error.message);
    return [];
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * 抓取大麦网演出数据
 * @returns {Array} 演出列表
 */
export async function fetchDamaiShows() {
  console.log('[大麦] 开始抓取演出数据...');
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent(USER_AGENT);
    
    const today = getTodayString();
    
    // 大麦北京演出
    await page.goto(`https://www.damai.cn/search.htm?spm=a2oeg.home.category.ditem_1.591b23e1xT9zBv&ctl=%E6%BC%94%E5%87%BA%E4%BC%9A&order=1&cty=%E5%8C%97%E4%BA%AC`, {
      waitUntil: 'networkidle2',
      timeout: TIMEOUT
    });
    
    await page.waitForSelector('.item__box', { timeout: TIMEOUT });
    
    const shows = await page.evaluate(() => {
      const items = document.querySelectorAll('.item__box');
      return Array.from(items).slice(0, 5).map(item => {
        const title = item.querySelector('.item__title')?.textContent?.trim();
        const venue = item.querySelector('.item__venue')?.textContent?.trim();
        const time = item.querySelector('.item__time')?.textContent?.trim();
        const price = item.querySelector('.item__price')?.textContent?.trim();
        return { title, venue, time, price, source: '大麦' };
      }).filter(s => s.title);
    });
    
    console.log(`[大麦] 成功抓取 ${shows.length} 场演出`);
    return shows;
    
  } catch (error) {
    console.error('[大麦] 抓取失败:', error.message);
    return [];
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * 抓取美团演出/活动数据
 * @returns {Array} 活动列表
 */
export async function fetchMeituanEvents() {
  console.log('[美团] 开始抓取活动数据...');
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent(USER_AGENT);
    
    // 美团北京休闲娱乐
    await page.goto('https://www.meituan.com/xiuxianyule/', {
      waitUntil: 'networkidle2',
      timeout: TIMEOUT
    });
    
    // 简化为返回空数组，实际实现需根据页面结构调整
    console.log('[美团] 抓取完成（需根据实际页面调整选择器）');
    return [];
    
  } catch (error) {
    console.error('[美团] 抓取失败:', error.message);
    return [];
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * 抓取小红书内容
 * @param {string} keyword - 搜索关键词
 * @returns {Array} 内容列表
 */
export async function fetchXiaohongshu(keyword) {
  console.log(`[小红书] 开始搜索: ${keyword}...`);
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent(USER_AGENT);
    
    // 小红书搜索（需登录，这里使用简化的示例）
    await page.goto(`https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}`, {
      waitUntil: 'networkidle2',
      timeout: TIMEOUT
    });
    
    console.log(`[小红书] 搜索完成: ${keyword}（需根据实际页面调整）`);
    return [];
    
  } catch (error) {
    console.error(`[小红书] 抓取失败:`, error.message);
    return [];
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * 获取工作日推荐数据
 */
export async function fetchWorkdayData() {
  console.log('\n=== 抓取工作日数据 ===');
  const startTime = Date.now();
  
  const [movies, shows, events] = await Promise.allSettled([
    fetchMaoyanMovies(),
    fetchDamaiShows(),
    fetchMeituanEvents()
  ]);
  
  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n抓取完成，耗时 ${duration} 秒\n`);
  
  return {
    movies: movies.status === 'fulfilled' ? movies.value : [],
    shows: shows.status === 'fulfilled' ? shows.value : [],
    events: events.status === 'fulfilled' ? events.value : [],
    fetchTime: new Date().toISOString()
  };
}

/**
 * 获取周末推荐数据
 */
export async function fetchWeekendData() {
  console.log('\n=== 抓取周末数据 ===');
  const startTime = Date.now();
  
  const [cityWalks, trips, socials, shows] = await Promise.allSettled([
    fetchXiaohongshu('北京 city walk'),
    fetchXiaohongshu('北京周边游 周末'),
    fetchXiaohongshu('北京 社交活动 桌游'),
    fetchDamaiShows()
  ]);
  
  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n抓取完成，耗时 ${duration} 秒\n`);
  
  return {
    cityWalks: cityWalks.status === 'fulfilled' ? cityWalks.value : [],
    trips: trips.status === 'fulfilled' ? trips.value : [],
    socials: socials.status === 'fulfilled' ? socials.value : [],
    shows: shows.status === 'fulfilled' ? shows.value : [],
    fetchTime: new Date().toISOString()
  };
}

export default {
  fetchMaoyanMovies,
  fetchDamaiShows,
  fetchMeituanEvents,
  fetchXiaohongshu,
  fetchWorkdayData,
  fetchWeekendData,
  fetchWeather
};