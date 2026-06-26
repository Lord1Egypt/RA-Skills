#!/usr/bin/env node
/**
 * 抖音爆款爬虫 - Node.js 版本
 * 使用 Playwright + 移动端 UA 解析真实搜索结果（无需登录）
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

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

function parseCount(text) {
    if (!text) return 0;
    text = text.trim().replace(/,/g, '').replace(/ /g, '');
    if (text.includes('亿')) return Math.floor(parseFloat(text.replace('亿', '')) * 100000000);
    if (text.includes('万')) return Math.floor(parseFloat(text.replace('万', '')) * 10000);
    const m = text.match(/\d+/);
    return m ? parseInt(m[0]) : 0;
}

class DouyinScraper {
    constructor(options = {}) {
        this.headless = options.headless !== false;
        this.delay = options.delay || 2000;
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
            locale: 'zh-CN',
        });

        this.page = await context.newPage();
        console.log('✅ 浏览器已启动');
    }

    async close() {
        if (this.page) await this.page.close();
        if (this.browser) await this.browser.close();
        console.log('✅ 浏览器已关闭');
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async searchVideos(keyword, limit = 10) {
        if (!this.page) await this.start();

        const searchUrl = `https://www.douyin.com/search/${encodeURIComponent(keyword)}`;
        console.log(`🔍 正在搜索: ${keyword}`);

        try {
            await this.page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
            try {
                await this.page.waitForSelector('.card-list .card-item', { timeout: 10000 });
            } catch { await this.sleep(4000); }
            await this.sleep(this.delay);

            // Scroll to load more
            for (let i = 0; i < Math.min(Math.ceil(limit / 4), 4); i++) {
                await this.page.evaluate('window.scrollBy(0, 1200)');
                await this.sleep(1500);
            }

            const cards = await this.page.$$('.card-list .card-item');
            console.log(`   找到 ${cards.length} 个卡片`);

            const videos = [];
            for (const card of cards) {
                if (videos.length >= limit) break;
                try {
                    const text = (await card.innerText()).trim();
                    if (!text) continue;
                    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
                    if (!lines.length) continue;
                    if (lines[0] === '大家还在搜' || lines[0].startsWith('商品') || lines[0] === '查看全部商品') continue;

                    const author = lines[0];
                    let publishTime = '';
                    let idx = 1;
                    const dateMatch = lines[idx]?.match(/^(\d{4})\.(\d{1,2})\.(\d{1,2})$/);
                    if (dateMatch) {
                        publishTime = `${dateMatch[1]}-${String(parseInt(dateMatch[2])).padStart(2,'0')}-${String(parseInt(dateMatch[3])).padStart(2,'0')}`;
                        idx++;
                    }

                    const descParts = [];
                    const stats = [];
                    while (idx < lines.length) {
                        const line = lines[idx++];
                        if (/^[\d,.万亿]+$/.test(line.replace(/万|亿/g, ''))) {
                            stats.push(parseCount(line));
                        } else if (line !== '广告' && line !== '团') {
                            descParts.push(line);
                        }
                    }

                    const description = descParts.join(' ');
                    const tags = [...new Set([keyword, ...description.matchAll(/#(\S+)/g).map(m => m[1])])].slice(0, 8);

                    let href = '';
                    const link = await card.$('a[href]');
                    if (link) {
                        href = await link.getAttribute('href') || '';
                        if (href.startsWith('/')) href = 'https://www.douyin.com' + href;
                    }

                    videos.push(new VideoData({
                        title: description.slice(0, 100) || author,
                        description,
                        author,
                        like_count: stats[0] || 0,
                        comment_count: stats[1] || 0,
                        share_count: stats[2] || 0,
                        url: href || searchUrl,
                        tags,
                        publish_time: publishTime || new Date().toISOString().split('T')[0],
                    }));
                } catch { continue; }
            }

            console.log(`✅ 已获取 ${videos.length} 条视频数据`);
            return videos;
        } catch (error) {
            console.error(`⚠️  搜索出错: ${error.message}`);
            return [];
        }
    }

    async getHotVideos(category = '', limit = 20) {
        if (!this.page) await this.start();
        console.log(`🔥 获取热榜: ${category || '全部'}`);
        // Hot page requires login on mobile too, return empty with note
        console.log('⚠️  热榜功能需要登录，暂不可用');
        return [];
    }
}

function saveToJson(videos, filepath) {
    fs.writeFileSync(filepath, JSON.stringify(videos, null, 2), 'utf-8');
    console.log(`💾 已保存到: ${filepath}`);
}

function displayResults(videos) {
    videos.forEach((v, i) => {
        const likes = v.like_count ? `👍${v.like_count.toLocaleString()}` : '';
        const comments = v.comment_count ? `💬${v.comment_count.toLocaleString()}` : '';
        const date = v.publish_time ? `📅${v.publish_time}` : '';
        console.log(`${i + 1}. @${v.author}  ${date}  ${likes}${comments}`);
        if (v.description) console.log(`   ${v.description.slice(0, 120)}`);
    });
}

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    if (!command || command === 'help' || command === '--help') {
        console.log(`
📱 抖音爆款爬虫

使用方法:
  node scripts/douyin_scraper.js search <关键词> [数量] [输出文件] [格式]
  node scripts/douyin_scraper.js hot [分类] [数量]

示例:
  node scripts/douyin_scraper.js search "海鲜" 10
  node scripts/douyin_scraper.js search "海鲜售卖" 20 seafood.json json
        `);
        return;
    }

    const scraper = new DouyinScraper({ headless: true });
    
    try {
        await scraper.start();
        let videos = [];
        
        if (command === 'search') {
            const keyword = args[1];
            const limit = parseInt(args[2]) || 10;
            if (!keyword) { console.error('❌ 请提供搜索关键词'); return; }
            videos = await scraper.searchVideos(keyword, limit);
            const outputFile = args[3];
            const format = args[4] || 'json';
            if (outputFile && videos.length) {
                if (format === 'csv') { /* csv not impl in JS */ }
                else saveToJson(videos, outputFile);
            }
        } else if (command === 'hot') {
            const category = args[1] || '';
            const limit = parseInt(args[2]) || 20;
            videos = await scraper.getHotVideos(category, limit);
        }
        
        if (videos.length) displayResults(videos);
    } catch (error) {
        console.error(`❌ 错误: ${error.message}`);
    } finally {
        await scraper.close();
    }
}

if (require.main === module) main();
module.exports = { DouyinScraper, VideoData };
