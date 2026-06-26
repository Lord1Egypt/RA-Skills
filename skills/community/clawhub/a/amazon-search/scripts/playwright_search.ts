/**
 * Playwright Amazon Search
 *
 * 使用 Playwright 直接搜索 Amazon 并解析结果
 */

import {Browser, BrowserContext, chromium, Page} from 'playwright';
import * as path from 'path';
import * as fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// UA 池
const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
];

function getRandomUA(): string {
    return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

// Session 缓存配置
const SESSION_TIMEOUT = 5 * 60 * 1000; // 5 分钟
const SESSION_DIR = path.join(__dirname, '..', 'cache', 'sessions');

interface SessionData {
    cookies: any[];
    userAgent: string;
    timestamp: number;
}

/**
 * 获取 session 文件路径
 */
function getSessionFilePath(proxy?: string): string {
    const sessionKey = proxy ? `proxy_${proxy.replace(/[^a-zA-Z0-9]/g, '_')}` : 'default';
    return path.join(SESSION_DIR, `${sessionKey}.json`);
}

/**
 * 加载未过期的 session
 */
function loadSession(proxy?: string): SessionData | null {
    const sessionFile = getSessionFilePath(proxy);

    if (!fs.existsSync(sessionFile)) {
        return null;
    }

    try {
        const content = fs.readFileSync(sessionFile, 'utf-8');
        const session: SessionData = JSON.parse(content);

        // 检查是否过期
        if (Date.now() - session.timestamp > SESSION_TIMEOUT) {
            console.log('Session expired, creating new one...');
            fs.unlinkSync(sessionFile);
            return null;
        }

        console.log('Reusing existing session...');
        return session;
    } catch (e) {
        return null;
    }
}

/**
 * 保存 session
 */
function saveSession(cookies: any[], userAgent: string, proxy?: string): void {
    try {
        if (!fs.existsSync(SESSION_DIR)) {
            fs.mkdirSync(SESSION_DIR, { recursive: true });
        }

        const sessionFile = getSessionFilePath(proxy);
        const session: SessionData = {
            cookies,
            userAgent,
            timestamp: Date.now()
        };

        fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2), 'utf-8');
    } catch (e) {
        console.error('Failed to save session:', e);
    }
}

/**
 * 清理过期 sessions
 */
function cleanExpiredSessions(): void {
    try {
        if (!fs.existsSync(SESSION_DIR)) return;

        const files = fs.readdirSync(SESSION_DIR);
        const now = Date.now();

        files.forEach(file => {
            if (!file.endsWith('.json')) return;

            const filepath = path.join(SESSION_DIR, file);
            try {
                const content = fs.readFileSync(filepath, 'utf-8');
                const session: SessionData = JSON.parse(content);

                if (now - session.timestamp > SESSION_TIMEOUT) {
                    fs.unlinkSync(filepath);
                    console.log(`Cleaned expired session: ${file}`);
                }
            } catch (e) {
                // 删除损坏的 session 文件
                fs.unlinkSync(filepath);
            }
        });
    } catch (e) {
        // 忽略清理错误
    }
}

export interface ItemAmazon {
    id_?: string;
    uuid?: string;
    original_image_url?: string;
    title?: string;
    item_page?: string;
    rating?: number;
    review_count?: number;
    price?: string;
    description?: string;
}

/**
 * 使用 Playwright 搜索 Amazon
 * @param keyword 搜索关键词
 * @param proxy 可选代理地址
 * @param pages 页数（默认1）
 * @returns 搜索结果数组
 */
export async function searchAmazonWithPlaywright(
    keyword: string,
    proxy?: string,
    pages: number = 1
): Promise<ItemAmazon[]> {
    console.log(`Searching Amazon for: ${keyword}, pages: ${pages}`);

    // 清理过期 sessions
    cleanExpiredSessions();

    // 尝试加载现有 session
    const existingSession = loadSession(proxy);
    const userAgent = existingSession?.userAgent || getRandomUA();

    const launchOptions: any = {
        headless: true,
        timeout: 120000,
        args: [
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-web-security',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--window-size=1920,1080',
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
        console.log(`Using proxy: ${proxy}`);
        launchOptions.proxy = {
            server: proxy.startsWith('http') ? proxy : `http://${proxy}`
        };
    }

    const browser: Browser = await chromium.launch(launchOptions);
    const allItems: ItemAmazon[] = [];

    try {
        const context: BrowserContext = await browser.newContext({
            viewport: { width: 1920, height: 1080 },
            userAgent: userAgent,
            locale: 'en-US',
            timezoneId: 'America/New_York',
            permissions: ['geolocation'],
        });

        // 如果有现有 session，恢复 cookies
        if (existingSession?.cookies?.length > 0) {
            console.log(`Restoring ${existingSession.cookies.length} cookies...`);
            await context.addCookies(existingSession.cookies);
        } else {
            console.log(`Using new session with UA: ${userAgent.slice(0, 50)}...`);
        }

        const page: Page = await context.newPage();
        page.setDefaultTimeout(60000);

        // 设置 extra headers
        await page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1'
        });

        // 反检测脚本
        await context.addInitScript(() => {
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            // @ts-ignore
            window.chrome = { runtime: {} };
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters: any) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) as any :
                    originalQuery(parameters)
            );
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        });

        // 步骤1: 先访问 Amazon 首页
        console.log('Step 1: Visiting Amazon homepage...');
        await page.goto('https://www.amazon.com/', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });
        await page.waitForTimeout(2000 + Math.random() * 2000);

        // 模拟人类行为
        await page.mouse.move(200, 300);
        await page.mouse.wheel(0, 300);
        await page.waitForTimeout(1000 + Math.random() * 1000);

        // 步骤2: 多页搜索
        for (let currentPage = 1; currentPage <= pages; currentPage++) {
            if (currentPage > 1) {
                console.log(`Navigating to page ${currentPage}...`);
            }

            // 构建搜索 URL
            const searchUrl = `https://www.amazon.com/s?k=${encodeURIComponent(keyword)}${currentPage > 1 ? `&page=${currentPage}` : ''}`;
            console.log(`Searching: ${searchUrl}`);

            // 访问搜索页
            await page.goto(searchUrl, {
                waitUntil: 'domcontentloaded',
                timeout: 60000
            });

            // 等待页面加载
            await page.waitForTimeout(3000 + Math.random() * 2000);

            // 等待搜索结果加载
            try {
                await page.waitForSelector('[data-component-type="s-search-result"]', {
                    timeout: 30000
                });
            } catch (e) {
                console.log(`No results found on page ${currentPage}`);
                break;
            }

            // 解析搜索结果
            const results = await page.evaluate(() => {
                const items: any[] = [];
                const resultElements = document.querySelectorAll('[data-component-type="s-search-result"]');

                resultElements.forEach((el) => {
                    const item: any = {};

                    // ASIN
                    item.id_ = el.getAttribute('data-asin') || '';

                    // UUID - data-uuid 或 id
                    let data_uuid = el.getAttribute('data-uuid');
                    if (!data_uuid) data_uuid = el.getAttribute('id') || '';
                    item.uuid = data_uuid;

                    // 图片 - 优先从 srcset 取最高分辨率
                    const imgEl = el.querySelector('img.s-image');
                    if (imgEl) {
                        const srcset = imgEl.getAttribute('srcset');
                        if (srcset) {
                            const entries = srcset.split(',');
                            const lastEntry = entries[entries.length - 1].trim();
                            const parts = lastEntry.split(/\s+/);
                            item.original_image_url = parts[0];
                        } else {
                            item.original_image_url = imgEl.getAttribute('src') || '';
                        }
                    }

                    // 标题 - 多选择器
                    const h2El = el.querySelector('h2');
                    if (h2El) {
                        item.title = h2El.textContent?.trim() || '';
                    } else {
                        const spanEl = el.querySelector('h2 > span');
                        if (spanEl) {
                            item.title = spanEl.textContent?.trim() || '';
                        }
                    }

                    // 链接 - 多选择器回退
                    const linkSelectors = [
                        'a.a-link-normal.s-no-outline',
                        'a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal',
                        'a.a-link-normal.s-underline-text.s-underline-link-text.null.s-link-style',
                        'a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal',
                        'h2 a'
                    ];
                    let linkEl = null;
                    for (const selector of linkSelectors) {
                        linkEl = el.querySelector(selector);
                        if (linkEl) break;
                    }
                    if (linkEl) {
                        const href = linkEl.getAttribute('href') || '';
                        if (href) item.item_page = href.startsWith('http') ? href : `https://www.amazon.com${href}`;
                    }

                    // 评分 - 多选择器
                    const ratingEl = el.querySelector("div[data-cy='reviews-block'] span.a-size-small.a-color-base");
                    if (ratingEl) {
                        item.rating = parseFloat(ratingEl.textContent?.trim() || '0');
                    } else {
                        const popoverEl = el.querySelector('a.a-popover-trigger.a-declarative');
                        if (popoverEl) {
                            const val = popoverEl.textContent?.split(' ')[0];
                            if (val) item.rating = parseFloat(val);
                        }
                    }

                    // 评分人数 - 多选择器，支持 万/K 单位
                    const ratingsEl = el.querySelector('span.a-size-mini.puis-normal-weight-text.s-underline-text');
                    if (ratingsEl) {
                        const text = ratingsEl.textContent || '';
                        const numStr = text.replace(/[^0-9.]/g, '');
                        if (text.includes('万')) {
                            item.review_count = Math.floor(parseFloat(numStr) * 10000);
                        } else if (text.includes('K')) {
                            item.review_count = Math.floor(parseFloat(numStr) * 1000);
                        } else {
                            item.review_count = parseInt(numStr);
                        }
                    } else {
                        const fallbackEl = el.querySelector('span.a-size-base.s-underline-text');
                        if (fallbackEl) {
                            const text = fallbackEl.textContent || '';
                            const numStr = text.replace(/[^0-9.]/g, '');
                            if (text.includes('万')) {
                                item.review_count = Math.floor(parseFloat(numStr) * 10000);
                            } else if (text.includes('K')) {
                                item.review_count = Math.floor(parseFloat(numStr) * 1000);
                            } else {
                                item.review_count = parseInt(numStr);
                            }
                        }
                    }

                    // 价格 - 多选择器回退
                    const priceSelectors = [
                        'span.a-offscreen',
                        '.a-row.a-size-base.a-color-secondary span.a-color-base'
                    ];
                    let priceFound = false;
                    for (const selector of priceSelectors) {
                        const priceEl = el.querySelector(selector);
                        if (priceEl && priceEl.textContent?.includes('$')) {
                            item.price = priceEl.textContent.trim();
                            priceFound = true;
                            break;
                        }
                    }
                    if (!priceFound) {
                        const priceEl = el.querySelector('.a-price .a-offscreen');
                        if (priceEl) {
                            item.price = priceEl.textContent?.trim() || '';
                        }
                    }

                    // 描述 - 专用选择器
                    let descEl = el.querySelector('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal');
                    if (descEl) {
                        item.description = descEl.textContent?.trim() || '';
                    } else {
                        descEl = el.querySelector('a.s-line-clamp-2 > h2 > span');
                        if (descEl) {
                            item.description = descEl.textContent?.trim() || '';
                        } else {
                            item.description = item.title;
                        }
                    }

                    items.push(item);
                });

                return items;
            });

            console.log(`Page ${currentPage}: Found ${results.length} results`);
            allItems.push(...results);

            // 如果不是最后一页，等待一下
            if (currentPage < pages) {
                await page.waitForTimeout(2000 + Math.random() * 2000);
            }
        }

        console.log(`Total results: ${allItems.length}`);
        return allItems;

    } catch (e) {
        console.error('Search error:', e);
        // 保存截图和 HTML 用于调试
        try {
            const screenshotPath = path.join(__dirname, '..', 'debug_search.png');
            const htmlPath = path.join(__dirname, '..', 'debug_search.html');
            await page.screenshot({ path: screenshotPath, fullPage: true });
            const html = await page.content();
            fs.writeFileSync(htmlPath, html, 'utf-8');
            console.log(`Debug screenshot saved: ${screenshotPath}`);
            console.log(`Debug HTML saved: ${htmlPath}`);
        } catch (debugErr) {
            // 忽略调试保存错误
        }
        throw e;
    } finally {
        // 保存 session（cookies 和 UA）
        try {
            const cookies = await context.cookies();
            saveSession(cookies, userAgent, proxy);
            console.log(`Session saved (${cookies.length} cookies)`);
        } catch (saveErr) {
            console.error('Failed to save session:', saveErr);
        }
        await browser.close();
    }
}

// CLI 支持
(async () => {
    const isMain = import.meta.main || (process.argv[1] && process.argv[1].includes('playwright_search'));
    if (!isMain) return;

    const args = process.argv.slice(2);
    const keyword = args[0] || 'shirt';

    const proxyArg = args.find(arg => arg.startsWith('--proxy='));
    const proxy = proxyArg ? proxyArg.split('=')[1] : process.env.T2P_PROXY;

    const pagesArg = args.find(arg => arg.startsWith('--pages='));
    const pages = pagesArg ? parseInt(pagesArg.split('=')[1], 10) : 1;

    try {
        const results = await searchAmazonWithPlaywright(keyword, proxy, pages);
        // 输出格式化的结果，方便父进程解析
        console.log('\n=== Results ===');
        console.log(JSON.stringify(results, null, 2));
        console.log(`\nTotal: ${results.length} items`);
    } catch (err) {
        console.error('Failed:', err);
        process.exit(1);
    }
})();
