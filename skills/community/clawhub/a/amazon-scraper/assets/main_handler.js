const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const targetUrl = args.find(a => a.startsWith('http'));
const outputFile = args.find((a, i) => args[i-1] === '--output');

if (!targetUrl) {
    console.error('Usage: node assets/main_handler.js <URL> [--output path.json]');
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

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    let context = null;
    let page = null;

    try {
        let success = false;
        let lastErr = null;
        for (let attempt = 0; attempt < Math.max(PROXY_LIST.length, 1); attempt++) {
            try {
                if (context) await context.close();
                context = await createContext(browser);
                page = await context.newPage();

                await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 60000 });
                await page.waitForTimeout(2000);

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

        const title = await page.title();
        const content = await page.evaluate(() => document.body.innerText);
        const result = {
            status: 'SUCCESS',
            type: 'GENERIC',
            url: targetUrl,
            title,
            data: content.substring(0, 10000),
            scrapedAt: new Date().toISOString()
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
})();
