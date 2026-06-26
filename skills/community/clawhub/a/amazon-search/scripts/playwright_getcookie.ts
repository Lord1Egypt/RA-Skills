/**
 * Playwright Cookie Getter
 *
 * 使用 Playwright 获取 Amazon cookies。
 * 使用 headless 模式 + 反检测配置
 */

import {Browser, BrowserContext, chromium, Page} from 'playwright';
import * as path from 'path';
import * as fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 简单 UA 池
const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
];

function getRandomUA(): string {
    return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

/**
 * 使用 Playwright 获取 Amazon cookies
 * @param proxy 可选代理地址
 * @returns cookie 字符串和 userAgent，失败时返回 null
 */
export async function getCookiesFromPlaywright(proxy?: string): Promise<{ cookies: string; userAgent: string } | null> {
    console.log('Launching headless browser with anti-detection...');

    const launchOptions: any = {
        headless: true,
        timeout: 120000,
        args: [
            // Anti-detection args
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-web-security',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--window-size=1920,1080',
            // Hide automation
            '--disable-extensions',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-features=TranslateUI',
            '--disable-component-extensions-with-background-pages',
            '--no-first-run',
            '--no-default-browser-check'
        ],
    };

    if (proxy) {
        console.log(`proxy ip: ${proxy}`);
        launchOptions.proxy = {
            server: proxy.startsWith('http') ? proxy : `http://${proxy}`
        };
    }

    const browser: Browser = await chromium.launch(launchOptions);

    try {
        const userAgent = getRandomUA();
        const context: BrowserContext = await browser.newContext({
            viewport: { width: 1920, height: 1080 },
            userAgent: userAgent,
            locale: 'en-US',
            timezoneId: 'America/New_York',
            // Hide webdriver
            permissions: ['geolocation'],
        });

        const page: Page = await context.newPage();
        page.setDefaultTimeout(5 * 60 * 1000);

        await page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1'
        });

        // 拦截图片以加速
        await page.route('**/*.{png,jpg,jpeg,gif,webp,svg}', route => route.abort());

        // 高级反检测脚本
        await context.addInitScript(() => {
            // 删除 webdriver 属性
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            // 伪装 chrome
            // @ts-ignore
            window.chrome = { runtime: {} };
            // 伪装 permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters: any) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) as any :
                    originalQuery(parameters)
            );
            // 伪装 plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            // 伪装 languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        });

        // 打开页面
        console.log('Navigating to Amazon...');
        await page.goto('https://www.amazon.com/', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        // 模拟真实行为
        console.log('Simulating human behavior...');
        await page.mouse.move(200, 300);
        await page.mouse.wheel(0, 500);
        await page.waitForTimeout(2000 + Math.random() * 2000);
        await page.mouse.move(500, 400);
        await page.mouse.wheel(0, -300);
        await page.waitForTimeout(2000 + Math.random() * 2000);

        // 截图和保存 HTML 用于调试
        const screenshotPath = path.join(__dirname, '..', 'debug_screenshot.png');
        const htmlPath = path.join(__dirname, '..', 'debug_page.html');
        await page.screenshot({ path: screenshotPath, fullPage: true });
        const html = await page.content();
        fs.writeFileSync(htmlPath, html, 'utf-8');
        console.log(`Screenshot saved to: ${screenshotPath}`);
        console.log(`HTML saved to: ${htmlPath}`);

        // 获取 cookies
        const cookies = await context.cookies();
        const cookieStr = cookies
            .map(c => `${c.name}=${c.value}`)
            .join(';');

        console.log('Cookies obtained successfully');
        return { cookies: cookieStr, userAgent };
    } catch (e) {
        console.error('Error:', e);
        return null;
    } finally {
        await browser.close();
    }
}

// 直接运行此文件时的 CLI 支持
(async () => {
    // Bun: import.meta.main, Node.js: process.argv[1] includes filename
    const isMain = import.meta.main || (process.argv[1] && process.argv[1].includes('playwright_getcookie'));
    if (!isMain) return;

    const args = process.argv.slice(2);
    const proxyArg = args.find(arg => arg.startsWith('--proxy='));
    const proxy = proxyArg ? proxyArg.split('=')[1] : process.env.T2P_PROXY;

    console.log('Getting Amazon cookies using Playwright...');
    if (proxy) {
        console.log(`Using proxy: ${proxy}`);
    }

    const result = await getCookiesFromPlaywright(proxy);

    if (result) {
        console.log('\n=== Cookies ===');
        console.log(result.cookies);
        console.log('\n=== User-Agent ===');
        console.log(result.userAgent);
        console.log('\nUse these cookies with:');
        console.log(`bun run scripts/amazon_search.ts "keyword" --cookies="${result.cookies}"`);
    } else {
        console.error('Failed to get cookies');
        process.exit(1);
    }
})();
