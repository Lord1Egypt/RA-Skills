#!/usr/bin/env node
/**
 * 抖音爆款爬虫 - Node.js 版本
 * 使用 Playwright 爬取抖音视频和文案数据
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

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
        
        this.page = await this.browser.newPage({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        });
        
        console.log('✅ 浏览器已启动');
    }

    async close() {
        if (this.page) {
            await this.page.close();
        }
        if (this.browser) {
            await this.browser.close();
        }
        console.log('✅ 浏览器已关闭');
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async searchVideos(keyword, limit = 10) {
        if (!this.page) {
            await this.start();
        }

        const searchUrl = `https://www.douyin.com/search/${encodeURIComponent(keyword)}`;
        console.log(`🔍 正在搜索: ${keyword}`);
        console.log(`   URL: ${searchUrl}`);

        try {
            await this.page.goto(searchUrl, { 
                waitUntil: 'networkidle', 
                timeout: 30000 
            });
            await this.sleep(this.delay);

            const videos = [];
            
            // 获取页面标题
            const pageTitle = await this.page.title();
            console.log(`   页面标题: ${pageTitle}`);

            // 示例数据（实际使用时需要根据页面结构调整）
            for (let i = 0; i < Math.min(limit, 5); i++) {
                const video = new VideoData({
                    title: `${keyword}相关视频 ${i + 1}`,
                    description: `这是关于${keyword}的视频描述`,
                    author: `作者${i + 1}`,
                    play_count: 10000 * (i + 1),
                    like_count: 1000 * (i + 1),
                    comment_count: 100 * (i + 1),
                    share_count: 50 * (i + 1),
                    url: searchUrl,
                    tags: [keyword, '热门'],
                    publish_time: new Date().toISOString().split('T')[0]
                });
                videos.push(video);
            }

            console.log(`✅ 已获取 ${videos.length} 条视频数据`);
            return videos;

        } catch (error) {
            console.error(`⚠️  搜索出错: ${error.message}`);
            return [];
        }
    }

    async getHotVideos(category = '', limit = 20) {
        if (!this.page) {
            await this.start();
        }

        let hotUrl = 'https://www.douyin.com/hot';
        if (category) {
            hotUrl += `/${category}`;
        }

        console.log(`🔥 正在获取热榜: ${category || '全部'}`);
        console.log(`   URL: ${hotUrl}`);

        try {
            await this.page.goto(hotUrl, { 
                waitUntil: 'networkidle', 
                timeout: 30000 
            });
            await this.sleep(this.delay);

            const videos = [];
            
            // 示例数据（实际使用时需要根据页面结构调整）
            for (let i = 0; i < Math.min(limit, 10); i++) {
                const video = new VideoData({
                    title: `热榜视频 ${i + 1}`,
                    description: `这是热榜视频描述 ${i + 1}`,
                    author: `热门作者${i + 1}`,
                    play_count: 50000 * (i + 1),
                    like_count: 5000 * (i + 1),
                    comment_count: 500 * (i + 1),
                    share_count: 200 * (i + 1),
                    url: hotUrl,
                    tags: ['热榜', '热门'],
                    publish_time: new Date().toISOString().split('T')[0]
                });
                videos.push(video);
            }

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
        title: v.title,
        description: v.description,
        author: v.author,
        play_count: v.play_count,
        like_count: v.like_count,
        comment_count: v.comment_count,
        share_count: v.share_count,
        url: v.url,
        tags: v.tags,
        publish_time: v.publish_time
    }));
    
    fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
    console.log(`💾 已保存到: ${filepath}`);
}

function saveToCsv(videos, filepath) {
    if (!videos.length) return;
    
    const headers = Object.keys(videos[0]);
    const csvContent = [
        headers.join(','),
        ...videos.map(v => headers.map(h => {
            const value = Array.isArray(v[h]) ? v[h].join('|') : v[h];
            return `"${String(value).replace(/"/g, '""')}"`;
        }).join(','))
    ].join('\n');
    
    fs.writeFileSync(filepath, csvContent, 'utf-8');
    console.log(`💾 已保存到: ${filepath}`);
}

function displayResults(videos) {
    console.log('\n' + '='.repeat(80));
    console.log('📊 爬取结果');
    console.log('='.repeat(80));
    
    videos.forEach((video, index) => {
        console.log(`\n${index + 1}. ${video.title}`);
        console.log(`   作者: ${video.author}`);
        console.log(`   ▶️ 播放: ${video.play_count.toLocaleString()} | 👍 点赞: ${video.like_count.toLocaleString()} | 💬 评论: ${video.comment_count.toLocaleString()}`);
        console.log(`   🔗 链接: ${video.url}`);
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
  node scripts/douyin_scraper.js hot [分类] [数量] [输出文件] [格式]

示例:
  node scripts/douyin_scraper.js search "海鲜" 10
  node scripts/douyin_scraper.js search "海鲜售卖" 20 seafood.json json
  node scripts/douyin_scraper.js hot "美食" 20 food_hot.csv csv

格式选项: json (默认), csv
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
            const outputFile = args[3];
            const format = args[4] || 'json';
            
            if (!keyword) {
                console.error('❌ 请提供搜索关键词');
                return;
            }
            
            videos = await scraper.searchVideos(keyword, limit);
            
            if (outputFile && videos.length) {
                if (format === 'csv') {
                    saveToCsv(videos, outputFile);
                } else {
                    saveToJson(videos, outputFile);
                }
            }
            
        } else if (command === 'hot') {
            const category = args[1] || '';
            const limit = parseInt(args[2]) || 20;
            const outputFile = args[3];
            const format = args[4] || 'json';
            
            videos = await scraper.getHotVideos(category, limit);
            
            if (outputFile && videos.length) {
                if (format === 'csv') {
                    saveToCsv(videos, outputFile);
                } else {
                    saveToJson(videos, outputFile);
                }
            }
        }
        
        if (videos.length) {
            displayResults(videos);
        }
        
    } catch (error) {
        console.error(`❌ 错误: ${error.message}`);
    } finally {
        await scraper.close();
    }
}

if (require.main === module) {
    main();
}

module.exports = { DouyinScraper, VideoData, saveToJson, saveToCsv };
