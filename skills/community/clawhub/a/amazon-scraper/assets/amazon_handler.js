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
const maxPages = parseInt(args.find((a, i) => args[i-1] === '--pages') || '1');
const outputFile = args.find((a, i) => args[i-1] === '--output');
const concurrency = parseInt(args.find((a, i) => args[i-1] === '--concurrency') || '1');
const queriesArg = args.find((a, i) => args[i-1] === '--queries');
const queries = queriesArg ? queriesArg.split(',').map(s => s.trim()).filter(Boolean) : null;
const asinsArg = args.find((a, i) => args[i-1] === '--asins');
const asins = asinsArg ? asinsArg.split(',').map(s => s.trim()).filter(Boolean) : null;
const bsrMode = args.includes('--bsr');
const bsrCategories = (args.find((a, i) => args[i-1] === '--bsr-cats') || 'electronics,home,office-products,tools').split(',').map(s => s.trim());

if (!targetUrl && !queries && !bsrMode && !asins) {
    console.error('Usage: node assets/amazon_handler.js <AMAZON_URL> [--pages N] [--output path.json] [--concurrency N]');
    console.error('   OR: --queries "q1,q2,q3" [--pages N]');
    console.error('   OR: --bsr [--bsr-cats electronics,home,office-products,tools]');
    console.error('   OR: --asins "B07FW3GTXB,B081HH5X61,..." [--concurrency 5]');
    process.exit(1);
}

const OUTPUT_ROOT = process.env.AMAZON_OUTPUT_DIR || '/data';

/** Confines --output to OUTPUT_ROOT so a crafted path can't write outside the mount. */
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

function detectPageType(url) {
    if (url.includes('/zgbs/') || url.includes('/bestsellers/')) return 'bestsellers';
    if (url.includes('/new-releases/')) return 'new-releases';
    if (url.includes('/zg/movers-and-shakers/') || url.includes('/movers-and-shakers/')) return 'movers-shakers';
    if (url.includes('/dp/') || url.includes('/gp/product/')) return 'product-detail';
    if (url.includes('/s?') || url.includes('/s/')) return 'search';
    return 'generic';
}

const pageType = targetUrl ? detectPageType(targetUrl) : 'generic';

let PROXY_POOL;
try {
    PROXY_POOL = createProxyPool();
} catch (e) {
    console.log(JSON.stringify({ status: 'ERROR', message: e.message }));
    console.error(e.message);
    process.exit(1);
}

/**
 * Amazon answers a blocked request with HTTP 200 and an unrendered page, so every
 * extracted field comes back null. Callers must be able to tell that apart from a
 * genuine result; see SKILL.md "静默失败".
 */
function isSoftBlocked(products) {
    if (!products || products.length === 0) return true;
    const signals = ['title', 'price', 'rating', 'reviews', 'brand'];
    return products.every(p => signals.every(k => p[k] === null || p[k] === undefined));
}

async function createContext(browser) {
    const entry = PROXY_POOL.next();
    const proxyUrl = entry ? entry.raw : null;
    const fp = fingerprintForProxy(proxyUrl);
    console.error(`Using proxy: ${redact(proxyUrl)} fp=${fp.label}`);
    return createFingerprintedContext(browser, proxyUrl, entry ? entry.parsed : null);
}

async function runCrawler() {
    // ============== Multi-query / BSR / single-URL dispatch ==============
    let jobs = [];
    if (bsrMode) {
        // BSR mode: each category -> 1 URL with --pages 2 (BSR caps at 2 pages = ~60 products)
        for (const cat of bsrCategories) {
            jobs.push({ url: `https://www.amazon.com/gp/bestsellers/${cat}`, pages: 2, label: `BSR/${cat}` });
        }
    } else if (queries) {
        for (const q of queries) {
            jobs.push({ url: `https://www.amazon.com/s?k=${encodeURIComponent(q)}`, pages: maxPages, label: `search/${q}` });
        }
    } else if (asins) {
        for (const asin of asins) {
            jobs.push({ url: `https://www.amazon.com/dp/${asin}`, pages: 1, label: `dp/${asin}` });
        }
    } else {
        jobs.push({ url: targetUrl, pages: maxPages, label: 'single' });
    }

    const browser = await chromium.launch({
        headless: true,
        args: LAUNCH_ARGS
    });

    let context = null;

    try {
        // ============== Worker pool: process jobs with limited concurrency ==============
        const extractFromPage = async (page, pType) => {
            let products = [];

            if (pType === 'bestsellers' || pType === 'new-releases' || pType === 'movers-shakers') {
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

            } else if (pType === 'product-detail') {
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
                    let brand = (document.querySelector('#bylineInfo') || {}).textContent?.trim();
                    if (brand) {
                        brand = brand.replace(/^Brand:\s*/i, '').replace(/^Visit the\s+/i, '').replace(/\s+Store$/i, '').trim();
                    }
                    const image = (document.querySelector('#landingImage, #imgBlkFront') || {}).src;
                    const breadcrumbs = Array.from(document.querySelectorAll('#wayfinding-breadcrumbs_feature_div a')).map(a => a.textContent.trim());
                    const bullets = Array.from(document.querySelectorAll('#feature-bullets li span')).map(s => s.textContent.trim()).filter(Boolean);

                    let boughtPastMonth = null;
                    const boughtMatch = document.body.innerText.match(/([\d,.]+[KkMm]?\+?)\s*bought in past month/i);
                    if (boughtMatch) boughtPastMonth = boughtMatch[1];

                    // ---- BSR: try innerText regex first, then prodDetails table ----
                    let bsr = null;
                    const bsrMatch = document.body.innerText.match(/Best Sellers Rank.*?#([\d,]+)/s);
                    if (bsrMatch) {
                        bsr = parseInt(bsrMatch[1].replace(/,/g, ''));
                    } else {
                        // New layout: BSR is in #prodDetails tr
                        document.querySelectorAll('#prodDetails tr, #productDetails_detailBullets_sections1 tr, #productDetails_techSpec_section_1 tr').forEach(row => {
                            const cells = row.querySelectorAll('th, td');
                            if (cells.length >= 2) {
                                const key = cells[0].textContent.trim().replace(/[:\s]+$/, '');
                                const val = cells[1].textContent.trim();
                                if (key.match(/Best Sellers Rank/i)) {
                                    const m = val.match(/#([\d,]+)/);
                                    if (m) bsr = parseInt(m[1].replace(/,/g, ''));
                                }
                            }
                        });
                    }

                    // ---- Date First Available: try innerText regex, then prodDetails table ----
                    let dateFirstAvailable = null;
                    const dateMatch = document.body.innerText.match(/Date First Available\s*[:\n]\s*([A-Za-z]+ \d+,? \d{4})/);
                    if (dateMatch) {
                        dateFirstAvailable = dateMatch[1];
                    } else {
                        document.querySelectorAll('#prodDetails tr, #productDetails_detailBullets_sections1 tr, #productDetails_techSpec_section_1 tr').forEach(row => {
                            const cells = row.querySelectorAll('th, td');
                            if (cells.length >= 2) {
                                const key = cells[0].textContent.trim().replace(/[:\s]+$/, '');
                                const val = cells[1].textContent.trim();
                                if (key.match(/Date First Available/i)) {
                                    const m = val.match(/([A-Za-z]+ \d+,? \d{4})/);
                                    if (m) dateFirstAvailable = m[1];
                                }
                            }
                        });
                    }

                    // ---- Seller: try multiple methods ----
                    let seller = null;
                    // Method 1: sellerProfileTriggerId (most reliable on new layout)
                    const sellerEl = document.querySelector('#sellerProfileTriggerId, #merchantInfo_feature_div a, [data-feature-name="merchantInfo"] a');
                    if (sellerEl) seller = sellerEl.textContent.trim();
                    // Method 2: "Ships from\n{val}\nSold by\n{val}" pattern in innerText
                    if (!seller) {
                        const sellerMatch = document.body.innerText.match(/Sold by\s+([\w\s\-\.]+)/i);
                        if (sellerMatch) seller = sellerMatch[1].trim();
                    }
                    // Method 3: tabular "Ships from" row
                    if (!seller) {
                        document.querySelectorAll('#prodDetails tr, #productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr, #detailBullets_feature_div li').forEach(row => {
                            const key = (row.querySelector('th, .a-text-bold, .a-list-item') || {}).textContent?.trim()?.replace(/[:\s]+$/, '');
                            const val = (row.querySelector('td, span:not(.a-text-bold)') || {}).textContent?.trim();
                            if (key && key.match(/Ships from|Sold by/i) && val) seller = val;
                        });
                    }
                    // Clean up
                    if (seller) {
                        seller = seller.replace(/^(Sold by|Ships from|Fulfilled by)\s*/i, '').replace(/\.?\s*$/,'').trim();
                    }

                    // ---- Details: scan all known product detail sections ----
                    const details = {};
                    document.querySelectorAll('#productDetails_techSpec_section_1 tr, #detailBullets_feature_div li, #prodDetails tr, #productDetails_detailBullets_sections1 tr').forEach(row => {
                        const cells = row.querySelectorAll('th, td');
                        if (cells.length >= 2) {
                            const key = cells[0].textContent.trim().replace(/[:\s]+$/, '');
                            const val = cells[1].textContent.trim();
                            if (key && val) details[key] = val;
                        }
                    });

                    return [{ title, price, priceStr, rating, reviews, asin, brand, image, bsr, boughtPastMonth, dateFirstAvailable, seller, category: breadcrumbs, bullets, details }];
                });

            } else if (pType === 'search') {
                products = await page.evaluate(() => {
                    const items = [];
                    document.querySelectorAll('[data-component-type="s-search-result"]').forEach(card => {
                        try {
                            const asin = card.getAttribute('data-asin');
                            const titleEl = card.querySelector('h2 a span') || card.querySelector('h2 span');
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
                return [{ _generic: true, data: content.substring(0, 10000) }];
            }

            return products;
        };

        const runJob = async (job) => {
            const t0 = Date.now();
            console.error(`[${job.label}] starting...`);
            const jobPageType = detectPageType(job.url);
            let jobProducts = [];
            const failures = [];
            const proxyCount = Math.max(PROXY_POOL.size, 1);

            for (let pg = 1; pg <= job.pages; pg++) {
                let url = job.url;
                if (pg > 1) url = job.url.includes('?') ? `${job.url}&page=${pg}` : `${job.url}?page=${pg}`;

                let success = false;
                let lastErr = null;
                let jobContext = null;
                let jobPage = null;

                for (let attempt = 0; attempt < proxyCount; attempt++) {
                    try {
                        jobContext = await createContext(browser);
                        jobPage = await jobContext.newPage();
                        await warmupAmazon(jobPage);
                        await jobPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

                        if (jobPageType === 'search') {
                            try {
                                await jobPage.waitForSelector('[data-component-type="s-search-result"]', { timeout: 15000 });
                                await jobPage.waitForFunction(() => {
                                    const cards = document.querySelectorAll('[data-component-type="s-search-result"] h2 a span, [data-component-type="s-search-result"] h2 span');
                                    let nonEmpty = 0;
                                    for (const c of cards) { if (c.textContent.trim().length > 5) nonEmpty++; }
                                    return nonEmpty >= 10;
                                }, { timeout: 20000 });
                            } catch(e) { console.error(`[${job.label}] search wait:`, e.message); }
                        } else if (jobPageType === 'product-detail') {
                            try {
                                await jobPage.waitForSelector('#productTitle, #dp', { timeout: 15000 });
                                await jobPage.waitForTimeout(3000);
                            } catch(e) { console.error(`[${job.label}] detail wait:`, e.message); }
                        } else {
                            await jobPage.waitForTimeout(3000);
                        }
                        await jobPage.evaluate(async () => {
                            for (let i = 0; i < 5; i++) { window.scrollBy(0, window.innerHeight); await new Promise(r => setTimeout(r, 500)); }
                            window.scrollTo(0, 0);
                        });
                        await humanizeMouse(jobPage);

                        const pageProducts = await extractFromPage(jobPage, jobPageType);
                        if (pg === 1 && pageProducts.length === 0 && jobPageType === 'search') {
                            throw new Error('No products extracted - search page may be blocked');
                        }
                        // An all-null detail page is a soft block (or a dead ASIN), not a result.
                        // Treating it as success is what used to poison the price history.
                        if (jobPageType === 'product-detail' && isSoftBlocked(pageProducts)) {
                            throw new Error('Detail page returned no fields - soft blocked or ASIN unavailable');
                        }
                        jobProducts.push(...pageProducts);
                        await saveFingerprintState(jobContext);
                        success = true;
                        break;
                    } catch (err) {
                        lastErr = err;
                        console.error(`[${job.label}] attempt ${attempt + 1} failed: ${err.message}`);
                        if (jobPage) { try { await jobPage.close(); } catch(e) {} }
                        if (jobContext) { try { await jobContext.close(); } catch(e) {} }
                    }
                }

                if (!success) {
                    console.error(`[${job.label}] ALL PROXIES FAILED on page ${pg}: ${lastErr?.message}`);
                    failures.push({ job: job.label, page: pg, error: lastErr?.message || 'unknown' });
                }

                if (jobPage) { try { await jobPage.close(); } catch(e) {} }
                if (jobContext) { try { await jobContext.close(); } catch(e) {} }
                if (pg < job.pages) await new Promise(r => setTimeout(r, 1500));
            }

            console.error(`[${job.label}] done: ${jobProducts.length} products in ${(Date.now()-t0)/1000}s`);
            return { job, products: jobProducts, failures };
        };

        const workerPool = async (items, conc) => {
            const results = new Array(items.length);
            let idx = 0;
            const worker = async () => {
                while (idx < items.length) {
                    const myIdx = idx++;
                    results[myIdx] = await runJob(items[myIdx]);
                }
            };
            const workers = [];
            for (let i = 0; i < Math.min(conc, items.length); i++) workers.push(worker());
            await Promise.all(workers);
            return results;
        };

        const conc = Math.max(1, Math.min(concurrency, jobs.length, PROXY_POOL.size || 1));
        if (conc < concurrency) {
            console.error(
                `WARNING: --concurrency ${concurrency} reduced to ${conc} ` +
                `(${jobs.length} jobs, ${PROXY_POOL.size} proxy exits). ` +
                `Add more exit IPs to raise it; running more workers than exits only gets the IP blocked.`
            );
        }
        console.error(`Running ${jobs.length} jobs with concurrency=${conc}`);
        const t0 = Date.now();
        const results = await workerPool(jobs, conc);

        // Merge all results
        const seenAsin = new Set();
        const allProducts = [];
        const sourcesByAsin = {};
        for (const r of results) {
            for (const p of (r.products || [])) {
                if (p.asin && !seenAsin.has(p.asin)) {
                    seenAsin.add(p.asin);
                    p._source = r.job.label;
                    allProducts.push(p);
                } else if (p.asin && seenAsin.has(p.asin)) {
                    // already have it, merge source
                    if (!sourcesByAsin[p.asin]) sourcesByAsin[p.asin] = [p._source || r.job.label];
                    sourcesByAsin[p.asin].push(r.job.label);
                }
            }
        }
        // add merged sources
        for (const p of allProducts) {
            if (sourcesByAsin[p.asin]) {
                const all = new Set([p._source, ...sourcesByAsin[p.asin]]);
                p._sources = Array.from(all);
            }
        }

        // Deduplicate by ASIN within each job result already done, but cross-job merge handled above
        const failures = results.flatMap(r => r.failures || []);
        const failedJobs = [...new Set(failures.map(f => f.job))];

        // SUCCESS used to be hardcoded, so a fully blocked run looked identical to a
        // clean one. Downstream monitors need to distinguish these.
        let status = 'SUCCESS';
        if (failedJobs.length === jobs.length) status = 'ERROR';
        else if (failures.length > 0) status = 'PARTIAL';

        const result = {
            status,
            mode: bsrMode ? 'bsr' : (queries ? 'multi-query' : 'single'),
            jobs: jobs.map(j => j.label),
            concurrency: conc,
            totalJobs: jobs.length,
            failedJobs,
            failures,
            totalProducts: allProducts.length,
            uniqueAsins: seenAsin.size,
            durationSeconds: Math.round((Date.now() - t0) / 1000),
            scrapedAt: new Date().toISOString(),
            products: allProducts
        };
        console.log(JSON.stringify(result));
        saveResult(result);
        if (status === 'ERROR') process.exitCode = 2;
        else if (status === 'PARTIAL') process.exitCode = 3;

    } catch (err) {
        // On stdout, so a caller that parses stdout sees the failure instead of nothing.
        const errorResult = { status: 'ERROR', message: err.message };
        console.log(JSON.stringify(errorResult));
        console.error(err.stack || err.message);
        saveResult(errorResult);
        process.exit(1);
    } finally {
        if (context) { try { await context.close(); } catch(e) {} }
        await browser.close();
    }
}

runCrawler();
