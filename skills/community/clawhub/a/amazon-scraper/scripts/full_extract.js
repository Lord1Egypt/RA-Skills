/**
 * Amazon Product Page - Full Extraction
 * 
 * 抓取亚马逊产品详情页的所有可见字段（43个），不预设字段列表。
 * 相比 amazon_handler.js 的 15 个字段，额外抓取：
 *   - 多种价格（划线价、deal价、buybox价、所有价格元素）
 *   - 评分分布直方图
 *   - 全部图片（main/thumbnail/hires/aplus 分类标记）
 *   - 视频列表（含poster帧）
 *   - A+ 内容文本
 *   - 完整详情表（20+ 键值对）
 *   - BSR 全文（含分类排名）
 *   - 卖家信息（seller/shipsFrom/fulfilledBy）
 *   - 库存状态、Prime标记、预计送达时间
 *   - 优惠券、Subscribe & Save
 *   - 变体选项（颜色/尺寸/规格）
 *   - Frequently Bought Together
 *   - 关联推荐 carousels
 *   - 客户问答 Q&A
 *   - 顶部评论（作者/评分/标题/日期/verified/有用数）
 *   - 安全警告、新版提示
 *   - 页面 meta 标签、canonical URL
 *   - JSON-LD 结构化数据
 *   - 整页纯文本（截断2万字）
 * 
 * 用法：
 *   docker run --rm -v /path/to/full_extract.js:/app/full_extract.js \
 *     amazon-scraper node /app/full_extract.js "https://www.amazon.com/dp/ASIN/"
 * 
 * 注意：
 *   - 代理走 assets/proxy.js：AMAZON_PROXIES / AMAZON_PROXY / AMAZON_PROXY_FILE / config/proxies.json
 *   - stdout 只输出 JSON，日志全部走 stderr（不要给 docker run 加 -t，否则 TTY 会把两者混流）
 *   - 需要 waitForTimeout(3000) + 8次滚动加载懒加载内容
 *   - 容器内路径是 /app/ 不是 __dirname/..
 */
const { chromium } = require('playwright');
const {
    fingerprintForProxy,
    createFingerprintedContext,
    warmupAmazon,
    humanizeMouse,
    saveFingerprintState,
    LAUNCH_ARGS
} = require('../assets/fingerprint');
const { createProxyPool, redact } = require('../assets/proxy');

const targetUrl = process.argv[2];
if (!targetUrl) {
    console.error('Usage: node full_extract.js <AMAZON_URL>');
    process.exit(1);
}

async function main() {
    let pool;
    try {
        pool = createProxyPool();
    } catch (e) {
        console.error(e.message);
        process.exit(1);
    }

    const browser = await chromium.launch({
        headless: true,
        args: LAUNCH_ARGS
    });

    const entry = pool.next();
    const proxyUrl = entry ? entry.raw : null;
    const fp = fingerprintForProxy(proxyUrl);
    console.error(`Using proxy: ${redact(proxyUrl)} fp=${fp.label}`);
    const context = await createFingerprintedContext(browser, proxyUrl, entry ? entry.parsed : null);
    const page = await context.newPage();

    try {
        await warmupAmazon(page);
        await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForSelector('#productTitle, #dp', { timeout: 15000 });
        await page.waitForTimeout(3000);
        await humanizeMouse(page);
        await page.evaluate(async () => {
            for (let i = 0; i < 8; i++) {
                window.scrollBy(0, window.innerHeight);
                await new Promise(r => setTimeout(r, 600));
            }
            window.scrollTo(0, 0);
            await new Promise(r => setTimeout(r, 1000));
        });

        const data = await page.evaluate(() => {
            const result = {};
            result.title = (document.querySelector('#productTitle') || {}).textContent?.trim() || null;
            const prices = {};
            const mainPrice = document.querySelector('.a-price .a-offscreen, #priceblock_ourprice, #priceblock_dealprice, #priceblock_saleprice');
            prices.main = mainPrice ? mainPrice.textContent.trim() : null;
            const listPrice = document.querySelector('.a-price.a-text-price .a-offscreen, .a-text-strike .a-offscreen, .a-text-strike');
            prices.listPrice = listPrice ? listPrice.textContent.trim() : null;
            const dealPrice = document.querySelector('#priceblock_dealprice, .priceBlockDealPriceString');
            prices.dealPrice = dealPrice ? dealPrice.textContent.trim() : null;
            const buyboxPrice = document.querySelector('#corePrice_feature_div .a-offscreen, #corePriceDisplay_desktop_feature_div .a-offscreen');
            prices.buybox = buyboxPrice ? buyboxPrice.textContent.trim() : null;
            prices.allPriceElements = Array.from(document.querySelectorAll('.a-price')).map(el => ({
                text: el.textContent.trim().replace(/\s+/g, ' '),
                classes: el.className,
            }));
            result.prices = prices;
            const ratingEl = document.querySelector('#acrPopover .a-icon-alt, [data-hook="rating-out-of-text"]');
            result.rating = ratingEl ? parseFloat(ratingEl.textContent) : null;
            result.ratingText = ratingEl ? ratingEl.textContent.trim() : null;
            const reviewsEl = document.querySelector('#acrCustomerReviewText, [data-hook="total-review-count"]');
            result.reviews = reviewsEl ? parseInt(reviewsEl.textContent.replace(/[^0-9]/g, '')) : null;
            result.reviewsText = reviewsEl ? reviewsEl.textContent.trim() : null;
            const ratingBars = {};
            document.querySelectorAll('#histogramTable tr, [data-hook="histogram-table"] tr').forEach(tr => {
                const starEl = tr.querySelector('.a-icon-alt');
                const pctEl = tr.querySelector('.a-text-right, .a-last, .a-link-normal');
                if (starEl) { const star = starEl.textContent.trim().match(/(\d)/); const pct = pctEl ? pctEl.textContent.trim() : null; if (star) ratingBars[star[1] + 'star'] = pct; }
            });
            result.ratingHistogram = ratingBars;
            result.asin = (window.location.pathname.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || null;
            let brand = (document.querySelector('#bylineInfo') || {}).textContent?.trim();
            if (brand) brand = brand.replace(/^Brand:\s*/i, '').replace(/^Visit the\s+/i, '').replace(/\s+Store$/i, '').trim();
            result.brand = brand;
            const brandLink = document.querySelector('#bylineInfo');
            result.brandUrl = brandLink ? brandLink.href : null;
            const images = [];
            const mainImg = document.querySelector('#landingImage, #imgBlkFront');
            if (mainImg) images.push({ type: 'main', src: mainImg.src, alt: mainImg.alt });
            document.querySelectorAll('#altImages img, #imageBlock img, #thumbs-image img').forEach(img => {
                const src = img.src || img.getAttribute('data-old-hires') || '';
                if (src && !src.includes('transparent') && !src.includes('play-icon')) images.push({ type: 'thumbnail', src, alt: img.alt || '' });
            });
            document.querySelectorAll('[data-old-hires]').forEach(el => { const hires = el.getAttribute('data-old-hires'); if (hires) images.push({ type: 'hires', src: hires, alt: el.alt || '' }); });
            document.querySelectorAll('#aplus img, #aplus_feature_div img, .aplus-v2 img').forEach(img => { images.push({ type: 'aplus', src: img.src, alt: img.alt || '' }); });
            result.images = images;
            const videos = [];
            document.querySelectorAll('video, [data-video-url], .videoBlockIngress img, [class*="video"]').forEach(el => {
                const src = el.tagName === 'VIDEO' ? (el.src || el.querySelector('source')?.src) : (el.getAttribute('data-video-url') || el.src);
                if (src && !src.includes('transparent')) videos.push({ type: 'video', src, poster: el.poster || null });
            });
            result.videos = videos;
            result.bullets = Array.from(document.querySelectorAll('#feature-bullets li span')).map(s => s.textContent.trim()).filter(t => t && !t.includes('See more'));
            result.bulletsCount = result.bullets.length;
            const aplusText = [];
            document.querySelectorAll('#aplus_feature_div, #aplus, .aplus-v2').forEach(div => { const text = div.innerText.trim(); if (text) aplusText.push(text); });
            result.aplusContent = aplusText.join('\n---\n');
            result.aplusLength = result.aplusContent.length;
            const details = {};
            document.querySelectorAll('#productDetails_techSpec_section_1 tr, #prodDetails tr, #productDetails_detailBullets_sections1 tr').forEach(row => {
                const cells = row.querySelectorAll('th, td'); if (cells.length >= 2) { const key = cells[0].textContent.trim().replace(/[:\s]+$/, ''); const val = cells[1].textContent.trim(); if (key && val && key.length < 100) details[key] = val; }
            });
            document.querySelectorAll('#detailBullets_feature_div li').forEach(li => {
                const keyEl = li.querySelector('.a-text-bold'); const valEl = li.querySelector('span:not(.a-text-bold)');
                if (keyEl && valEl) { const key = keyEl.textContent.trim().replace(/[:\s]+$/, ''); const val = valEl.textContent.trim(); if (key && val) details[key] = val; }
            });
            result.details = details;
            result.detailsCount = Object.keys(details).length;
            let bsr = null;
            const bsrMatch = document.body.innerText.match(/Best Sellers Rank.*?#([\d,]+)/s);
            if (bsrMatch) bsr = parseInt(bsrMatch[1].replace(/,/g, ''));
            if (!bsr) { document.querySelectorAll('#prodDetails tr, #productDetails_detailBullets_sections1 tr, #detailBullets_feature_div li').forEach(row => { const text = row.textContent; if (text.match(/Best Sellers Rank/i)) { const m = text.match(/#([\d,]+)/); if (m) bsr = parseInt(m[1].replace(/,/g, '')); } }); }
            result.bsr = bsr;
            const bsrFullMatch = document.body.innerText.match(/Best Sellers Rank[:\s]*([\s\S]*?)(?=\n[A-Z]|\nDate First|\nCustomer|\nASIN|$)/);
            result.bsrFullText = bsrFullMatch ? bsrFullMatch[1].trim() : null;
            result.category = Array.from(document.querySelectorAll('#wayfinding-breadcrumbs_feature_div a, #wayfinding-breadcrumbs_container a')).map(a => a.textContent.trim());
            result.categoryFull = Array.from(document.querySelectorAll('#wayfinding-breadcrumbs_feature_div li')).map(li => li.textContent.trim()).filter(t => t);
            let boughtPastMonth = null;
            const boughtMatch = document.body.innerText.match(/([\d,.]+[KkMm]?\+?)\s*bought in past month/i);
            if (boughtMatch) boughtPastMonth = boughtMatch[1];
            result.boughtPastMonth = boughtPastMonth;
            let dateFirstAvailable = null;
            const dateMatch = document.body.innerText.match(/Date First Available\s*[:\n]\s*([A-Za-z]+ \d+,? \d{4})/);
            if (dateMatch) dateFirstAvailable = dateMatch[1];
            result.dateFirstAvailable = dateFirstAvailable;
            let seller = null;
            const sellerEl = document.querySelector('#sellerProfileTriggerId, #merchantInfo_feature_div a, [data-feature-name="merchantInfo"] a');
            if (sellerEl) seller = sellerEl.textContent.trim();
            if (!seller) { const sellerMatch = document.body.innerText.match(/Sold by\s+([\w\s\-\.]+)/i); if (sellerMatch) seller = sellerMatch[1].trim(); }
            result.seller = seller;
            const shipMatch = document.body.innerText.match(/Ships from\s+([\w\s\-\.]+)/i);
            result.shipsFrom = shipMatch ? shipMatch[1].trim() : null;
            const fulfillMatch = document.body.innerText.match(/Fulfilled by\s+([\w\s\-\.]+)/i);
            result.fulfilledBy = fulfillMatch ? fulfillMatch[1].trim() : null;
            const availability = document.querySelector('#availability span, #availability .a-color-state, #availability .a-color-price');
            result.availability = availability ? availability.textContent.trim() : null;
            result.isPrime = !!document.querySelector('.a-icon-prime, #price-shipping-message .a-icon-prime');
            const deliveryEl = document.querySelector('#deliveryBlockMessage, #fast-track-message, .a-row .a-color-success .a-text-bold');
            result.delivery = deliveryEl ? deliveryEl.textContent.trim() : null;
            const couponEl = document.querySelector('#vpcButton, .promoPriceBlockMessage, #couponBadge, [data-csa-c-content-id="coupon-badge"]');
            result.coupon = couponEl ? couponEl.textContent.trim() : null;
            const variations = {};
            document.querySelectorAll('#variation_style_name, #variation_size_name, #variation_color_name').forEach(el => {
                const label = el.id.replace('variation_', '').replace('_name', '');
                const selected = el.querySelector('.selection') || el.querySelector('.a-button-selected');
                if (selected) variations[label] = selected.textContent.trim();
            });
            const variationOptions = [];
            document.querySelectorAll('#variation_style_name li, #variation_size_name li, #variation_color_name li, [id*="variation_"] li').forEach(li => { const text = li.textContent.trim(); if (text) variationOptions.push(text); });
            variations.allOptions = variationOptions;
            const twister = window.twisterController || null;
            if (twister && twister.dpIDs) { variations.allAsins = Object.keys(twister.dpIDs); }
            result.variations = variations;
            const fbtItems = [];
            document.querySelectorAll('#sims-fbt-form .a-checkbox, #sims-fbt-content .a-fixed-left-grid-col').forEach(el => { const text = el.textContent.trim().replace(/\s+/g, ' '); if (text && text.length > 5) fbtItems.push(text.substring(0, 200)); });
            result.frequentlyBoughtTogether = fbtItems;
            const carousels = [];
            document.querySelectorAll('[data-csa-c-content-type="amzn-carousel"], .a-carousel-card').forEach(card => {
                const title = card.querySelector('h2, .a-carousel-heading, .a-color-base')?.textContent?.trim();
                const items = Array.from(card.querySelectorAll('a')).map(a => a.textContent.trim()).filter(t => t.length > 5);
                if (items.length > 0) carousels.push({ title, items: items.slice(0, 10) });
            });
            result.carousels = carousels;
            const qa = [];
            document.querySelectorAll('#ask_feature_div .a-fixed-left-grid, #ask_lazy_load_div .a-fixed-left-grid').forEach(el => {
                const q = el.querySelector('.a-link-normal')?.textContent?.trim();
                const a = el.querySelector('.a-color-base')?.textContent?.trim();
                if (q) qa.push({ question: q, answer: a });
            });
            result.customerQA = qa;
            const topReviews = [];
            document.querySelectorAll('[data-hook="review"], #reviews-medley-footer [data-hook="review"]').forEach(el => {
                const author = el.querySelector('.a-profile-name')?.textContent?.trim();
                const ratingEl2 = el.querySelector('[data-hook="review-star-rating"], .a-icon-alt');
                const rating = ratingEl2 ? parseFloat(ratingEl2.textContent) : null;
                const title = el.querySelector('[data-hook="review-title"]')?.textContent?.trim();
                const date = el.querySelector('[data-hook="review-date"]')?.textContent?.trim();
                const body = el.querySelector('[data-hook="review-body"] span')?.textContent?.trim();
                const verified = el.querySelector('[data-hook="avp-badge"]')?.textContent?.trim();
                const helpful = el.querySelector('[data-hook="helpful-vote-statement"]')?.textContent?.trim();
                topReviews.push({ author, rating, title, date, body: body?.substring(0, 500), verified, helpful });
            });
            result.topReviews = topReviews;
            const snsEl = document.querySelector('#snsBasePrice, #snsBottomBox, [data-csa-c-content-id="sns"]');
            result.subscribeAndSave = snsEl ? snsEl.textContent.trim() : null;
            const newerEl = document.querySelector('#newer-version-message, .a-alert-content');
            if (newerEl && newerEl.textContent.includes('newer version')) { result.newerVersion = newerEl.textContent.trim(); }
            const safetyEl = document.querySelector('#productAlert_feature_div, .a-alert-warning');
            result.safetyWarning = safetyEl ? safetyEl.textContent.trim() : null;
            result.fullPageText = document.body.innerText.substring(0, 20000);
            const metaTags = {};
            document.querySelectorAll('meta[name], meta[property]').forEach(m => {
                const key = m.getAttribute('name') || m.getAttribute('property');
                const val = m.getAttribute('content');
                if (key && val && val.length < 500) metaTags[key] = val;
            });
            result.metaTags = metaTags;
            result.pageUrl = window.location.href;
            result.canonicalUrl = document.querySelector('link[rel="canonical"]')?.href || null;
            const jsonLd = [];
            document.querySelectorAll('script[type="application/ld+json"]').forEach(script => { try { jsonLd.push(JSON.parse(script.textContent)); } catch(e) {} });
            result.structuredData = jsonLd;
            return result;
        });

        await saveFingerprintState(context);
        console.log(JSON.stringify(data, null, 2));

    } catch (err) {
        console.error('Error:', err.message);
        process.exit(1);
    } finally {
        await context.close();
        await browser.close();
    }
}

main();
