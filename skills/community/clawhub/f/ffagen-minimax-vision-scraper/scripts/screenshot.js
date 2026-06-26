#!/usr/bin/env node
/**
 * MiniMax Vision Scraper
 * Playwright截图 + MiniMax图像理解
 * 
 * Usage: node screenshot.js <URL> [prompt]
 * 
 * 依赖：
 * - playwright (已安装)
 * - MINIMAX_API_KEY (环境变量)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// API配置
const API_KEY = process.env.MINIMAX_API_KEY || 'sk-cp-k1SEMY8000Zyv758QolXpmGovm8C-HrPl75iCi41WvuD4TE0HtgE6qQ68V4kCa55EtmErJJN48Z-dRyQ5BUesXsjmkjffWmsk2TpqX4Uxh-seySOxFXfack';
const API_HOST = process.env.MINIMAX_API_HOST || 'api.minimaxi.com';
const API_PATH = '/v1/coding_plan/vlm';

const url = process.argv[2];
const prompt = process.argv[3] || '分析这张截图的内容，提取关键信息';
const waitTime = parseInt(process.env.WAIT_TIME || '5000');
const headless = process.env.HEADLESS !== 'false';
const screenshotPath = process.env.SCREENSHOT_PATH || `/tmp/screenshot-${Date.now()}.png`;

if (!url) {
    console.error('❌ 请提供 URL');
    console.error('用法: node screenshot.js <URL> [prompt]');
    process.exit(1);
}

const defaultUA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

async function takeScreenshot() {
    console.log('🕷️ 启动 MiniMax Vision Scraper...');
    console.log(`🔗 URL: ${url}`);
    
    const startTime = Date.now();
    
    const browser = await chromium.launch({
        headless: headless,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
        ],
    });
    
    const context = await browser.newContext({
        userAgent: defaultUA,
        locale: 'zh-CN',
        viewport: { width: 375, height: 812 },
        extraHTTPHeaders: {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        },
    });
    
    // 隐藏自动化特征
    await context.addInitScript(() => {
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        window.chrome = { runtime: {} };
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    });
    
    const page = await context.newPage();
    
    console.log('📱 导航到目标页面...');
    try {
        const response = await page.goto(url, {
            waitUntil: 'domcontentloaded',
            timeout: 30000,
        });
        console.log(`📡 HTTP Status: ${response.status()}`);
    } catch (error) {
        console.error(`⚠️ 导航异常: ${error.message}`);
    }
    
    // 等待内容加载
    console.log(`⏳ 等待 ${waitTime}ms...`);
    await page.waitForTimeout(waitTime);
    
    // 检测 Cloudflare
    const isCloudflare = await page.evaluate(() => {
        return document.body.innerText.includes('Checking your browser') ||
               document.body.innerText.includes('Just a moment');
    });
    
    if (isCloudflare) {
        console.log('🛡️ 检测到 Cloudflare，等待额外 10s...');
        await page.waitForTimeout(10000);
    }
    
    // 截图
    console.log(`📸 截图保存到: ${screenshotPath}`);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`⏱️ 截图耗时: ${elapsed}s`);
    
    await browser.close();
    
    return screenshotPath;
}

function callMiniMaxVision(imagePath, prompt) {
    return new Promise((resolve, reject) => {
        // 读取图片并转 base64
        const imageBuffer = fs.readFileSync(imagePath);
        const base64Image = imageBuffer.toString('base64');
        const mimeType = 'image/png';
        
        const payload = {
            prompt: prompt,
            image_url: `data:${mimeType};base64,${base64Image}`
        };
        
        const body = JSON.stringify(payload);
        
        const options = {
            hostname: API_HOST,
            port: 443,
            path: API_PATH,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            }
        };
        
        console.log('🤖 调用 MiniMax 图像理解...');
        const startTime = Date.now();
        
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
                try {
                    const json = JSON.parse(data);
                    const result = json.choices?.[0]?.message?.content || JSON.stringify(json);
                    console.log(`⏱️ MiniMax 响应耗时: ${elapsed}s`);
                    resolve(result);
                } catch (e) {
                    resolve(data);
                }
            });
        });
        
        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

(async () => {
    try {
        const screenshotPath = await takeScreenshot();
        const result = await callMiniMaxVision(screenshotPath, prompt);
        
        console.log('\n✅ 分析结果:');
        console.log(result);
        
        // 清理临时截图
        fs.unlinkSync(screenshotPath);
        
        process.exit(0);
    } catch (error) {
        console.error('❌ 错误:', error.message);
        process.exit(1);
    }
})();
