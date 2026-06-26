#!/usr/bin/env node
/**
 * 抖音爆款爬虫 - Node.js 版本
 * 使用 Playwright 移动端提取真实数据
 */

const { chromium } = require('playwright');
const fs = require('fs');

const MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

function parseCount(text) {
    if (!text) return 0;
    text = text.trim().replace(/,/g, '');
    let m = text.match(/([\d.]+)\s*万/);
    if (m) return Math.floor(parseFloat(m[1]) * 10000);
    m = text.match(/([\d.]+)\s*亿/);
    if (m) return Math.floor(parseFloat(m[1]) * 100000000);
    const nums = text.match(/\d+/);
    return nums ? parseInt(nums[0]) : 0;
}

class DouyinScraper {
    constructor(options = {}) {
        this.headless = options.headless !== false;
        this.delay = options.delay || 2000;
        this.browser = null;
        this.context = null;
    }

    async start() {
        this.browser = await chromium.launch({
            headless: this.headless,
            args: ['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-setuid-sandbox']
        });
        this.context = await this.browser.newContext({
            userAgent: MOBILE_UA,
            viewport: { width: 390, height: 844 },
            locale: 'zh-CN',
            isMobile: true
        });
    }

    async close() {
        if (this.context) await this.context.close();
        if (this.browser) await this.browser.close();
    }

    async sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

    async searchVideos(keyword, limit = 10) {
        if (!this.browser) await this.start();
        const page = await this.context.newPage();
        const videos = [];
        try {
            const url = `https://www.douyin.com/search/${encodeURIComponent(keyword)}`;
            console.error(`🔍 搜索: ${keyword}`);
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

            try {
                await page.waitForSelector('[class*="h5-video-card"], [class*="video-card"]', { timeout: 15000 });
                await this.sleep(this.delay);
            } catch {}

            const scrolls = Math.max(1, Math.ceil(limit / 5));
            for (let i = 0; i < scrolls; i++) {
                await page.evaluate(`window.scrollTo(0, ${(i + 1) * 800})`);
                await this.sleep(1500);
            }

            let cards = await page.$$('[class*="h5-video-card"]');
            if (!cards.length) cards = await page.$$('[class*="video-card"]');

            for (const card of cards.slice(0, limit)) {
                try {
                    const text = await card.innerText();
                    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

                    if (lines.some(l => l.includes('广告'))) continue;

                    const video = {
                        title: '', description: '', author: '', play_count: 0, like_count: 0,
                        comment_count: 0, share_count: 0, url: '', tags: [], publish_time: ''
                    };

                    const link = await card.$('a[href*="/video/"]');
                    if (link) {
                        let href = await link.getAttribute('href') || '';
                        if (href.startsWith('/')) href = 'https://www.douyin.com' + href;
                        video.url = href;
                    }

                    video.author = lines[0] || '';
                    video.publish_time = lines[1] || '';
                    video.title = lines[2] || '';
                    video.description = video.title;

                    const tags = video.title.match(/#(\S+)/g);
                    if (tags) video.tags = tags.map(t => t.slice(1));

                    const statLines = lines.slice(3);
                    const stats = [];
                    for (const s of statLines) {
                        if (/^[\d.]+万?$/.test(s)) {
                            const val = s.replace('万', '');
                            stats.push(s.includes('万') ? Math.floor(parseFloat(val) * 10000) : parseInt(val));
                        }
                    }
                    if (stats.length >= 1) video.like_count = stats[0];
                    if (stats.length >= 2) video.comment_count = stats[1];
                    if (stats.length >= 3) video.play_count = stats[2];
                    if (stats.length >= 4) video.share_count = stats[3];

                    if (!video.title) continue;
                    videos.push(video);
                } catch {}
            }
            console.error(`✅ 获取到 ${videos.length} 条结果`);
        } catch (e) {
            console.error(`⚠️  搜索出错: ${e.message}`);
        } finally {
            await page.close();
        }
        return videos;
    }

    async getHotVideos(category = '', limit = 20) {
        if (!this.browser) await this.start();
        const page = await this.context.newPage();
        const videos = [];
        try {
            let url = 'https://www.douyin.com/hot';
            if (category) url += '/' + encodeURIComponent(category);
            console.error(`🔥 获取热榜`);
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            try {
                await page.waitForSelector('[class*="h5-video-card"], [class*="hot"]', { timeout: 15000 });
                await this.sleep(this.delay);
            } catch {}
            for (let i = 0; i < 3; i++) {
                await page.evaluate(`window.scrollTo(0, ${(i + 1) * 800})`);
                await this.sleep(1500);
            }
            let cards = await page.$$('[class*="h5-video-card"]');
            if (!cards.length) cards = await page.$$('[class*="hot-item"], [class*="trending-item"]');
            for (const card of cards.slice(0, limit)) {
                try {
                    const text = await card.innerText();
                    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
                    if (lines.some(l => l.includes('广告'))) continue;
                    const video = { title: '', description: '', author: '', play_count: 0, like_count: 0, comment_count: 0, share_count: 0, url: '', tags: ['热榜'], publish_time: '' };
                    const link = await card.$('a[href*="/video/"]');
                    if (link) {
                        let href = await link.getAttribute('href') || '';
                        if (href.startsWith('/')) href = 'https://www.douyin.com' + href;
                        video.url = href;
                    }
                    video.author = lines[0] || '';
                    video.title = lines[2] || lines[0] || '';
                    video.publish_time = lines[1] || '';
                    if (video.title) videos.push(video);
                } catch {}
            }
            console.error(`✅ 获取到 ${videos.length} 条热榜数据`);
        } catch (e) {
            console.error(`⚠️  获取热榜出错: ${e.message}`);
        } finally {
            await page.close();
        }
        return videos;
    }
}

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    if (!command || command === 'help') {
        console.log(`用法: node douyin_scraper.js search <关键词> [数量] [输出文件] [格式]
       node douyin_scraper.js hot [分类] [数量] [输出文件] [格式]`);
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
        } else if (command === 'hot') {
            const category = args[1] || '';
            const limit = parseInt(args[2]) || 20;
            videos = await scraper.getHotVideos(category, limit);
        }
        console.log(JSON.stringify(videos, null, 2));
        const outputFile = args[3];
        const format = args[4] || 'json';
        if (outputFile && videos.length) {
            if (format === 'csv') {
                const headers = Object.keys(videos[0]);
                const csv = [headers.join(','), ...videos.map(v => headers.map(h => `"${String(Array.isArray(v[h]) ? v[h].join('|') : v[h]).replace(/"/g, '""')}"`).join(','))].join('\n');
                fs.writeFileSync(outputFile, csv, 'utf-8');
            } else {
                fs.writeFileSync(outputFile, JSON.stringify(videos, null, 2), 'utf-8');
            }
        }
    } catch (e) {
        console.error(`❌ 错误: ${e.message}`);
    } finally {
        await scraper.close();
    }
}

if (require.main === module) main();
module.exports = { DouyinScraper, parseCount };
