#!/usr/bin/env node
/**
 * 抖音搜索爬虫 - Node.js 版本
 * 使用 Playwright 爬取抖音搜索结果，支持自然语言查询
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

const STOP_WORDS = new Set(['一下','一些','相关','视频','内容','帖子','文案','直播','的','了','吗','吧','呢','帮','我','给','想','要','搜','找','看','查','搜索','看看']);

/**
 * Extract search keyword from natural-language query
 */
function extractKeyword(query) {
  let q = query.trim();
  // Pattern: "搜索一下海鲜视频" → "海鲜"
  let m = q.match(/(?:搜索|搜一下|搜搜|找|查找|查一下|看看).{0,4}?([^\s,，。！？]{1,20})(?:视频|内容|帖子|文案|直播)?(?:的?相关|的?内容)?$/);
  if (m) return cleanKeyword(m[1]);
  // Pattern: "帮我搜海鲜" → "海鲜"
  m = q.match(/(?:帮我|给我|想|要).{0,2}(?:搜|找|看|查)(?:一下|一搜|一找)?(.{1,20})/);
  if (m) return cleanKeyword(m[1]);
  // Pattern: "海鲜视频" → "海鲜"
  m = q.match(/^([^\s,，。！？]{1,20})(?:视频|内容|帖子|文案|直播)$/);
  if (m) return cleanKeyword(m[1]);
  return q;
}

function cleanKeyword(kw) {
  kw = kw.trim();
  for (const w of [...STOP_WORDS].sort((a, b) => b.length - a.length)) {
    if (kw.startsWith(w)) kw = kw.slice(w.length);
    if (kw.endsWith(w)) kw = kw.slice(0, -w.length);
  }
  return kw || kw || '海鲜';
}

class VideoData {
  constructor(data = {}) {
    this.title = data.title || '';
    this.description = data.description || '';
    this.author = data.author || '';
    this.play_count = data.play_count || 0;
    this.like_count = data.like_count || 0;
    this.comment_count = data.comment_count || 0;
    this.share_count = data.share_count || 0;
    this.url = data.url || '';
    this.tags = data.tags || [];
    this.publish_time = data.publish_time || '';
  }
}

class DouyinScraper {
  constructor(options = {}) {
    this.headless = options.headless !== false;
    this.delay = options.delay || 3000;
    this.browser = null;
    this.page = null;
  }

  async start() {
    console.log('🚀 启动浏览器...');
    this.browser = await chromium.launch({
      headless: this.headless,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
      ]
    });

    const context = await this.browser.newContext({
      userAgent: MOBILE_UA,
      viewport: { width: 390, height: 844 },
      isMobile: true,
    });

    this.page = await context.newPage();
    console.log('✅ 浏览器已启动 (移动端模式)');
  }

  async close() {
    if (this.page) await this.page.close();
    if (this.browser) await this.browser.close();
    console.log('✅ 浏览器已关闭');
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms || this.delay));
  }

  async searchVideos(keyword, limit = 10) {
    if (!this.page) await this.start();

    const searchUrl = `https://www.douyin.com/search/${encodeURIComponent(keyword)}`;
    console.log(`🔍 正在搜索: ${keyword}`);
    console.log(`   URL: ${searchUrl}`);

    try {
      await this.page.goto(searchUrl, { waitUntil: 'commit', timeout: 60000 });
      await this.sleep(this.delay);

      // Scroll to load more
      for (let i = 0; i < Math.min(Math.ceil(limit / 5), 4); i++) {
        await this.page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
        await this.sleep(1500);
      }

      // Check captcha
      const html = await this.page.content();
      if (html.includes('验证码')) {
        console.log('⚠️  遇到验证码页面，尝试等待...');
        await this.sleep(5000);
      }

      // Extract results from rendered page
      const rawItems = await this.page.evaluate((lim) => {
        const items = [];
        const allText = document.body.innerText || '';
        const lines = allText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        const skip = new Set(['综合','AI搜索','图片','视频','直播','用户','搜索','广告','宣传','团','充值','客户端','壁纸','通知','投稿','登录','精选','推荐','关注','朋友','我的','小游戏']);

        let currentItem = null;
        for (let i = 0; i < lines.length && items.length < lim * 3; i++) {
          const line = lines[i];
          if (skip.has(line) || line.startsWith('¥') || line.includes('查看地址') || line.includes('套餐')) continue;

          const isAuthor = line.length <= 20 && line.length >= 2
            && !line.endsWith('。') && !line.endsWith('！') && !line.endsWith('？')
            && !/^\d+$/.test(line);

          if (isAuthor && !currentItem) {
            currentItem = { author: line, description: '', date: '', stats: [0,0,0,0] };
          } else if (currentItem) {
            const dateMatch = line.match(/^20\d{2}[./-]\d{1,2}[./-]\d{1,2}$/);
            const statsMatch = line.match(/^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$/);

            if (dateMatch) {
              currentItem.date = line;
            } else if (statsMatch) {
              currentItem.stats = [parseInt(statsMatch[1]), parseInt(statsMatch[2]), parseInt(statsMatch[3]), parseInt(statsMatch[4])];
              items.push(currentItem);
              currentItem = null;
            } else if (line.length > 15 && !line.startsWith('¥') && !line.includes('查看地址') && !line.includes('套餐')) {
              if (!currentItem.description) {
                currentItem.description = line;
              }
            }
          }
        }
        return items;
      }, limit);

      const today = new Date().toISOString().split('T')[0];
      const videos = rawItems.slice(0, limit).map((item, idx) => new VideoData({
        title: (item.description || '').substring(0, 80),
        description: item.description || '',
        author: item.author || '',
        play_count: item.stats[0] || 0,
        like_count: item.stats[1] || 0,
        comment_count: item.stats[2] || 0,
        share_count: item.stats[3] || 0,
        url: searchUrl,
        tags: [keyword, '搜索'],
        publish_time: item.date || today,
      }));

      console.log(`✅ 已获取 ${videos.length} 条视频数据`);
      return videos;

    } catch (error) {
      console.error(`⚠️  搜索出错: ${error.message}`);
      return [];
    }
  }

  async getHotVideos(limit = 20) {
    console.log('🔥 正在获取热榜...');

    try {
      const { https } = require('follow-redirects') || require('https');
      const data = await new Promise((resolve, reject) => {
        const req = require('https').get('https://www.douyin.com/aweme/v1/web/hot/search/list/', {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.douyin.com/',
          }
        }, (res) => {
          let body = '';
          res.on('data', chunk => body += chunk);
          res.on('end', () => {
            try { resolve(JSON.parse(body)); }
            catch (e) { reject(e); }
          });
        });
        req.on('error', reject);
        req.setTimeout(15000, () => { req.destroy(); reject(new Error('timeout')); });
      });

      const wordList = (data.data || {}).word_list || [];
      const today = new Date().toISOString().split('T')[0];
      const videos = wordList.slice(0, limit).map((w, idx) => new VideoData({
        title: w.word || '',
        description: w.sentence_tag || '',
        author: '',
        play_count: w.hot_value || 0,
        like_count: 0,
        comment_count: 0,
        share_count: 0,
        url: `https://www.douyin.com/search/${encodeURIComponent(w.word || '')}`,
        tags: ['热榜'],
        publish_time: today,
      }));

      console.log(`✅ 已获取 ${videos.length} 条热榜数据`);
      return videos;

    } catch (error) {
      console.error(`⚠️  获取热榜出错: ${error.message}`);
      return [];
    }
  }
}

function saveToJson(videos, filepath) {
  const data = videos.map(v => ({
    title: v.title, description: v.description, author: v.author,
    play_count: v.play_count, like_count: v.like_count,
    comment_count: v.comment_count, share_count: v.share_count,
    url: v.url, tags: v.tags, publish_time: v.publish_time
  }));
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`💾 已保存到: ${filepath}`);
}

function displayResults(videos) {
  if (!videos.length) { console.log('没有找到结果。'); return; }
  console.log('\n' + '='.repeat(70));
  console.log(`📊 搜索结果 (${videos.length} 条)`);
  console.log('='.repeat(70));
  videos.forEach((video, index) => {
    console.log(`\n${index + 1}. ${video.title}`);
    if (video.author) console.log(`   👤 作者: ${video.author}`);
    if (video.play_count || video.like_count)
      console.log(`   ▶️ 播放: ${video.play_count.toLocaleString()} | 👍 点赞: ${video.like_count.toLocaleString()} | 💬 评论: ${video.comment_count.toLocaleString()}`);
    if (video.publish_time) console.log(`   📅 日期: ${video.publish_time}`);
    if (video.tags.length) console.log(`   🏷️ 标签: ${video.tags.join(', ')}`);
  });
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help') {
    console.log(`
📱 抖音搜索爬虫

使用方法:
  node scripts/douyin_scraper.js search <关键词或自然语言> [数量] [输出文件] [格式]
  node scripts/douyin_scraper.js hot [数量] [输出文件] [格式]

自然语言示例:
  node scripts/douyin_scraper.js search "搜索一下海鲜视频" 10
  node scripts/douyin_scraper.js search "帮我找小龙虾" 15
  node scripts/douyin_scraper.js search "海鲜" 10

关键词搜索:
  node scripts/douyin_scraper.js search "海鲜" 10
  node scripts/douyin_scraper.js search "海鲜售卖" 20 seafood.json json

热榜:
  node scripts/douyin_scraper.js hot 20

格式选项: json (默认), csv
    `);
    return;
  }

  const scraper = new DouyinScraper({ headless: true });

  try {
    let videos = [];

    if (command === 'search') {
      const rawKeyword = args[1];
      const limit = parseInt(args[2]) || 10;
      const outputFile = args[3];
      const format = args[4] || 'json';

      if (!rawKeyword) {
        console.error('❌ 请提供搜索关键词');
        return;
      }

      // Auto-extract keyword from natural language
      const keyword = extractKeyword(rawKeyword);
      if (keyword !== rawKeyword) {
        console.log(`💡 解析自然语言: '${rawKeyword}' → 关键词: '${keyword}'`);
      }

      await scraper.start();
      videos = await scraper.searchVideos(keyword, limit);

      if (outputFile && videos.length) {
        if (format === 'csv') {
          // CSV not implemented in JS version, fall back to JSON
          saveToJson(videos, outputFile);
        } else {
          saveToJson(videos, outputFile);
        }
      }

    } else if (command === 'hot') {
      const limit = parseInt(args[1]) || 20;
      const outputFile = args[2];
      const format = args[3] || 'json';

      videos = await scraper.getHotVideos(limit);

      if (outputFile && videos.length) {
        saveToJson(videos, outputFile);
      }
    }

    if (videos.length) {
      displayResults(videos);
    }

  } catch (error) {
    console.error(`❌ 错误: ${error.message}`);
  } finally {
    if (scraper.browser) await scraper.close();
  }
}

if (require.main === module) {
  main();
}

module.exports = { DouyinScraper, VideoData, extractKeyword, saveToJson };
