const { chromium } = require('playwright');
const {
    fingerprintForProxy,
    createFingerprintedContext,
    warmupAmazon,
    humanizeMouse,
    saveFingerprintState,
    LAUNCH_ARGS
} = require('./fingerprint');
const { createProxyPool, redact } = require('./proxy');

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const targetUrl = args.find(a => a.startsWith('http'));
const outputFile = args.find((a, i) => args[i-1] === '--output');

if (!targetUrl) {
    console.error('Usage: node assets/main_handler.js <URL> [--output path.json]');
    process.exit(1);
}

const OUTPUT_ROOT = process.env.AMAZON_OUTPUT_DIR || '/data';

function resolveOutputPath(name) {
    const outPath = path.resolve(OUTPUT_ROOT, name);
    const root = path.resolve(OUTPUT_ROOT);
    if (outPath !== root && !outPath.startsWith(root + path.sep)) {
        throw new Error(`--output must stay inside ${root} (got "${name}")`);
    }
    return outPath;
}

function saveResult(data) {
    if (outputFile) {
        const outPath = resolveOutputPath(outputFile);
        fs.mkdirSync(path.dirname(outPath), { recursive: true });
        fs.writeFileSync(outPath, JSON.stringify(data, null, 2));
        console.error(`Result saved to: ${outPath}`);
    }
}

let PROXY_POOL;
try {
    PROXY_POOL = createProxyPool();
} catch (e) {
    console.log(JSON.stringify({ status: 'ERROR', message: e.message }));
    console.error(e.message);
    process.exit(1);
}

async function createContext(browser) {
    const entry = PROXY_POOL.next();
    const proxyUrl = entry ? entry.raw : null;
    const fp = fingerprintForProxy(proxyUrl);
    console.error(`Using proxy: ${redact(proxyUrl)} fp=${fp.label}`);
    const namespace = `generic-${new URL(targetUrl).hostname}`;
    return createFingerprintedContext(browser, proxyUrl, entry ? entry.parsed : null, namespace);
}

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: LAUNCH_ARGS
    });

    let context = null;
    let page = null;

    try {
        // Only warm up on amazon.com. Warming up unconditionally sent every
        // third-party target a `Referer: https://www.amazon.com/` and burned a
        // request on a host that has nothing to do with the target.
        const isAmazonTarget = /(^|\.)amazon\.[a-z.]+$/i.test(new URL(targetUrl).hostname);

        let success = false;
        let lastErr = null;
        for (let attempt = 0; attempt < Math.max(PROXY_POOL.size, 1); attempt++) {
            try {
                if (context) await context.close();
                context = await createContext(browser);
                page = await context.newPage();
                if (isAmazonTarget) await warmupAmazon(page);
                await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 60000 });
                await page.waitForTimeout(2000);
                await humanizeMouse(page);
                await saveFingerprintState(context);

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
        console.log(JSON.stringify(errorResult));
        console.error(err.stack || err.message);
        saveResult(errorResult);
        process.exit(1);
    } finally {
        if (context) { try { await context.close(); } catch(e) {} }
        await browser.close();
    }
})();
