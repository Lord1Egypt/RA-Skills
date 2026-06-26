const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const targetUrl = args.find(a => a.startsWith('http'));
const maxPages = parseInt(args.find((a, i) => args[i-1] === '--pages') || '1');
const outputFile = args.find((a, i) => args[i-1] === '--output');

if (!targetUrl) {
    console.error('Usage: node assets/amazon_handler.js <AMAZON_URL> [--pages N] [--output path.json]');
    process.exit(1);
}

function saveResult(data) {
    if (outputFile) {
        const outPath = path.isAbsolute(outputFile) ? outputFile : path.join('/data', outputFile);
        const dir = path.dirname(outPath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(outPath, JSON.stringify(data, null, 2));
        console.error(`Result saved to: ${outPath}`);
    }
}

function detectPageType(url) {
    if (url.includes('/zgbs/') || url.includes('/bestsellers/')) return 'bestsellers';
    if (url.includes('/zg/new-releases/')) return 'new-releases';
    if (url.includes('/zg/movers-and-shakers/')) return 'movers-shakers';
    if (url.includes('/dp/') || url.includes('/gp/product/')) return 'product-detail';
    if (url.includes('/s?') || url.includes('/s/')) return 'search';
    return 'generic';
}

const pageType = detectPageType(targetUrl);

// ---- Proxy rotation setup ----
// Load built-in proxy config, allow env vars to override
function loadProxies() {
    try {
        const configPath = path.join(__dirname, '..', 'config', 'proxies.json');
        if (fs.existsSync(configPath)) {
            const cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            if (cfg.proxies && cfg.proxies.length > 0) {
                return cfg.proxies;
            }
        }
    } catch (e) {
        console.error('Failed to load config/proxies.json:', e.message);
    }
    const single = process.env.AMAZON_PROXY;
    const multi = process.env.AMAZON_PROXIES;
    if (multi) return multi.split(',').map(s => s.trim()).filter(Boolean);
    if (single) return [single];
    return [];
}

const PROXY_LIST = loadProxies();

let proxyIdx = 0;
function getNextProxy() {
    if (PROXY_LIST.length === 0) return null;
    const p = PROXY_LIST[proxyIdx % PROXY_LIST.length];
    proxyIdx++;
    return p;
}

function parseProxy(proxyUrl) {
    try {
        const url = new URL(proxyUrl);
        return {
            server: `${url.protocol}//${url.host}`,
            username: decodeURIComponent(url.username),
            password: decodeURIComponent(url.password)
        };
    } catch (e) {
        console.error('Invalid proxy URL format:', proxyUrl);
        return null;
    }
}

async function createContext(browser) {
    const proxyUrl = getNextProxy();
    const contextOptions = {
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        extraHTTPHeaders: {
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'identity',
            'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document'
        }
    };
    if (proxyUrl) {
        const parsed = parseProxy(proxyUrl);
        if (parsed) {
            contextOptions.proxy = parsed;
            console.error(`Using proxy: ${parsed.server} (user: ${parsed.username})`);
        }
    }
    const context = await browser.newContext(contextOptions);
    await context.setExtraHTTPHeaders({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    });
    return context;
}

async function runCrawler() {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    let context = null;
    let page = null;

    try {
        let allProducts = [];

        for (let pg = 1; pg <= maxPages; pg++) {
            let url = targetUrl;
            if (pg > 1) url = targetUrl.includes('?') ? `${targetUrl}&pg=${pg}` : `${targetUrl}?pg=${pg}`;

            // Retry with proxy rotation on failure
            let success = false;
            let lastErr = null;
            for (let attempt = 0; attempt < Math.max(PROXY_LIST.length, 1); attempt++) {
                try {
                    if (context) await context.close();
                    context = await createContext(browser);
                    page = await context.newPage();

                    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
                    await page.waitForTimeout(3000);
                    await page.evaluate(async () => {
                        for (let i = 0; i < 5; i++) { window.scrollBy(0, window.innerHeight); await new Promise(r => setTimeout(r, 500)); }
                        window.scrollTo(0, 0);
                    });
                    success = true;
                    break;
                } catch (err) {
                    lastErr = err;
                    console.error(`Attempt ${attempt + 1} failed: ${err.message}`);
                    if (page) { try { await page.close(); } catch(e) {} }
                    if (context) { try { await context.close(); } catch(e) {} }
                }
            }
            if (!success) {
                throw new Error(`All proxies failed. Last error: ${lastErr.message}`);
            }

            let products = [];

            if (pageType === 'bestsellers' || pageType === 'new-releases' || pageType === 'movers-shakers') {
                products = await page.evaluate(() => {
                    const items = [];
                    const cards = document.querySelectorAll('[data-asin]');

                    if (cards.length > 0) {
                        cards.forEach(card => {
                            try {
                                const rankEl = card.querySelector('.zg-bdg-text, [class*="zg-badge"]');
                                const titleEl = card.querySelector('a span, ._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y, .p13n-sc-truncate');
                                const ratingEl = card.querySelector('[class*="a-icon-alt"]');
                                const reviewEl = card.querySelector('[class*="a-size-small"]');
                                const priceEl = card.querySelector('.p13n-sc-price, ._cDEzb_p13n-sc-price_3mJ9Z, .a-price .a-offscreen');
                                const imgEl = card.querySelector('img');
                                const linkEl = card.querySelector('a[href*="/dp/"]');
                                const asin = card.getAttribute('data-asin') || (linkEl && linkEl.href && linkEl.href.match(/\/dp\/([A-Z0-9]{10})/) ? linkEl.href.match(/\/dp\/([A-Z0-9]{10})/)[1] : null);

                                let boughtPastMonth = null;
                                card.querySelectorAll('span').forEach(s => {
                                    const t = s.textContent.trim();
                                    if (t.match(/bought in past month/i)) {
                                        const m = t.match(/([\d,.]+[KkMm]?\+?)\s*bought/i);
                                        boughtPastMonth = m ? m[1] : t;
                                    }
                                });

                                const rank = rankEl ? parseInt(rankEl.textContent.replace('#', '')) : null;
                                const title = titleEl ? titleEl.textContent.trim() : null;
                                const rating = ratingEl ? parseFloat(ratingEl.textContent) : null;
                                const reviews = reviewEl ? parseInt(reviewEl.textContent.replace(/[^0-9]/g, '')) : null;
                                const priceText = priceEl ? priceEl.textContent.trim() : null;
                                const price = priceText ? parseFloat(priceText.replace(/[^0-9.]/g, '')) : null;
                                const image = imgEl ? imgEl.src : null;
                                const url = linkEl ? linkEl.href : null;

                                if (title) {
                                    items.push({ rank, title, rating, reviews, price, priceStr: priceText, asin, image, url, boughtPastMonth });
                                }
                            } catch (e) {}
                        });
                    }

                    if (items.length === 0) {
                        const text = document.body.innerText;
                        const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
                        let currentRank = null;
                        let currentProduct = {};

                        for (const line of lines) {
                            const rankMatch = line.match(/^#(\d+)$/);
                            if (rankMatch) {
                                if (currentRank && currentProduct.title) items.push(currentProduct);
                                currentRank = parseInt(rankMatch[1]);
                                currentProduct = { rank: currentRank };
                                continue;
                            }
                            if (currentRank) {
                                if (line.match(/^([\d.]+) out of 5 stars$/)) {
                                    currentProduct.rating = parseFloat(line);
                                } else if (line.match(/^\$([\d,.]+)$/)) {
                                    currentProduct.price = parseFloat(line.replace(/[$,]/g, ''));
                                    currentProduct.priceStr = line;
                                } else if (line.match(/^\s*[\d,]+\s*$/) && !currentProduct.reviews && currentProduct.rating) {
                                    currentProduct.reviews = parseInt(line.replace(/,/g, ''));
                                } else if (line.match(/bought in past month/i)) {
                                    const m = line.match(/([\d,.]+[KkMm]?\+?)\s*bought/i);
                                    currentProduct.boughtPastMonth = m ? m[1] : line;
                                } else if (!currentProduct.title && line.length > 10
                                    && !line.includes('out of 5') && !line.includes('Best Seller')
                                    && !line.includes('Previous page') && !line.includes('Next page')) {
                                    currentProduct.title = line;
                                }
                            }
                        }
                        if (currentRank && currentProduct.title) items.push(currentProduct);
                    }
                    return items;
                });

            } else if (pageType === 'product-detail') {
                products = await page.evaluate(() => {
                    const title = (document.querySelector('#productTitle') || {}).textContent?.trim();
                    const priceEl = document.querySelector('.a-price .a-offscreen, #priceblock_ourprice, #priceblock_dealprice');
                    const priceStr = priceEl ? priceEl.textContent.trim() : null;
                    const price = priceStr ? parseFloat(priceStr.replace(/[^0-9.]/g, '')) : null;
                    const ratingEl = document.querySelector('#acrPopover .a-icon-alt');
                    const rating = ratingEl ? parseFloat(ratingEl.textContent) : null;
                    const reviewsEl = document.querySelector('#acrCustomerReviewText');
                    const reviews = reviewsEl ? parseInt(reviewsEl.textContent.replace(/[^0-9]/g, '')) : null;
                    const asin = (document.querySelector('[data-asin]') || {}).getAttribute?.('data-asin') || (window.location.pathname.match(/\/dp\/([A-Z0-9]{10})/) || [])[1];
                    const brand = (document.querySelector('#bylineInfo') || {}).textContent?.trim();
                    const image = (document.querySelector('#landingImage, #imgBlkFront') || {}).src;
                    const bsrMatch = document.body.innerText.match(/Best Sellers Rank.*?#([\d,]+)/);
                    const bsr = bsrMatch ? parseInt(bsrMatch[1].replace(/,/g, '')) : null;
                    const breadcrumbs = Array.from(document.querySelectorAll('#wayfinding-breadcrumbs_feature_div a')).map(a => a.textContent.trim());
                    const bullets = Array.from(document.querySelectorAll('#feature-bullets li span')).map(s => s.textContent.trim()).filter(Boolean);

                    let boughtPastMonth = null;
                    const boughtMatch = document.body.innerText.match(/([\d,.]+[KkMm]?\+?)\s*bought in past month/i);
                    if (boughtMatch) boughtPastMonth = boughtMatch[1];

                    const dateMatch = document.body.innerText.match(/Date First Available\s*[:\n]\s*([A-Za-z]+ \d+,? \d{4})/);
                    const dateFirstAvailable = dateMatch ? dateMatch[1] : null;

                    const details = {};
                    document.querySelectorAll('#productDetails_techSpec_section_1 tr, #detailBullets_feature_div li').forEach(row => {
                        const key = (row.querySelector('th, .a-text-bold') || {}).textContent?.trim()?.replace(/[:\s]+$/, '');
                        const val = (row.querySelector('td, span:not(.a-text-bold)') || {}).textContent?.trim();
                        if (key && val) details[key] = val;
                    });

                    return [{ title, price, priceStr, rating, reviews, asin, brand, image, bsr, boughtPastMonth, dateFirstAvailable, category: breadcrumbs, bullets, details }];
                });

            } else if (pageType === 'search') {
                products = await page.evaluate(() => {
                    const items = [];
                    document.querySelectorAll('[data-component-type="s-search-result"]').forEach(card => {
                        try {
                            const asin = card.getAttribute('data-asin');
                            const titleEl = card.querySelector('h2 a span');
                            const priceEl = card.querySelector('.a-price .a-offscreen');
                            const ratingEl = card.querySelector('.a-icon-alt');
                            const reviewEl = card.querySelector('[class*="s-link-style"] .a-size-base');
                            const imgEl = card.querySelector('.s-image');
                            const linkEl = card.querySelector('h2 a');
                            const sponsoredEl = card.querySelector('.s-label-popover-default');

                            let boughtPastMonth = null;
                            card.querySelectorAll('span').forEach(s => {
                                const t = s.textContent.trim();
                                if (t.match(/bought in past month/i)) {
                                    const m = t.match(/([\d,.]+[KkMm]?\+?)\s*bought/i);
                                    boughtPastMonth = m ? m[1] : t;
                                }
                            });

                            items.push({
                                asin,
                                title: titleEl ? titleEl.textContent.trim() : null,
                                price: priceEl ? parseFloat(priceEl.textContent.replace(/[^0-9.]/g, '')) : null,
                                priceStr: priceEl ? priceEl.textContent.trim() : null,
                                rating: ratingEl ? parseFloat(ratingEl.textContent) : null,
                                reviews: reviewEl ? parseInt(reviewEl.textContent.replace(/[^0-9]/g, '')) : null,
                                image: imgEl ? imgEl.src : null,
                                url: linkEl ? 'https://www.amazon.com' + linkEl.getAttribute('href') : null,
                                boughtPastMonth,
                                sponsored: !!sponsoredEl
                            });
                        } catch (e) {}
                    });
                    return items;
                });

            } else {
                // Generic fallback
                const content = await page.evaluate(() => document.body.innerText);
                const result = { status: 'SUCCESS', type: 'GENERIC', title, data: content.substring(0, 10000) };
                console.log(JSON.stringify(result));
                saveResult(result);
                await browser.close();
                return;
            }

            // Deduplicate by ASIN
            products = products.filter((p, i, arr) => {
                if (!p.asin) return true;
                const firstIdx = arr.findIndex(x => x.asin === p.asin);
                if (firstIdx !== i) {
                    if (p.rank && !arr[firstIdx].rank) arr[firstIdx].rank = p.rank;
                    if (p.boughtPastMonth && !arr[firstIdx].boughtPastMonth) arr[firstIdx].boughtPastMonth = p.boughtPastMonth;
                    return false;
                }
                return true;
            });

            allProducts.push(...products);
            if (pg < maxPages) await page.waitForTimeout(2000);
        }

        const metadata = await page.evaluate(() => {
            const title = document.title;
            const breadcrumbs = Array.from(document.querySelectorAll('#zg_browseRoot a, .zg-breadcrumb a')).map(a => a.textContent.trim());
            return { title, breadcrumbs };
        });

        const result = {
            status: 'SUCCESS',
            type: pageType,
            url: targetUrl,
            category: metadata.title?.replace('Amazon Best Sellers: Best ', '').replace('Amazon.com : ', ''),
            breadcrumbs: metadata.breadcrumbs,
            totalProducts: allProducts.length,
            pages: maxPages,
            scrapedAt: new Date().toISOString(),
            products: allProducts
        };
        console.log(JSON.stringify(result));
        saveResult(result);

    } catch (err) {
        const errorResult = { status: 'ERROR', message: err.message };
        console.error(JSON.stringify(errorResult));
        saveResult(errorResult);
        process.exit(1);
    } finally {
        if (context) { try { await context.close(); } catch(e) {} }
        await browser.close();
    }
}

runCrawler();
