"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.braveBrowsePlatform = braveBrowsePlatform;
const playwright_1 = require("playwright");
const OPENCLAW_CDP_PORT = 18800;
const SELECTORS = {
    x: {
        name: "X/Twitter",
        url: (u) => `https://x.com/${u}`,
        container: 'article[data-testid="tweet"]',
        text: 'div[data-testid="tweetText"]',
        time: 'time[datetime]',
        accountBtn: 'button[data-testid="accountButton"], button[aria-label="Account menu"]',
        profileName: 'h1[data-testid="UserName"], h1',
        profileHandle: '[data-testid="UserDescription"] span, [data-testid="UserName"] + div > span',
        profileBio: '[data-testid="UserDescription"]',
        profileFollowers: 'a[href*="/verified_followers"]',
        getStats: (tweet) => ({
            replies: tweet.querySelector('[data-testid="reply"] [data-testid="count"]')?.innerText?.trim() || null,
            retweets: tweet.querySelector('[data-testid="retweet"] [data-testid="count"]')?.innerText?.trim() || null,
            likes: tweet.querySelector('[data-testid="like"] [data-testid="count"]')?.innerText?.trim() || null,
            shares: tweet.querySelector('[data-testid="share"] [data-testid="count"]')?.innerText?.trim() || null
        })
    },
    twitter: {
        name: "X/Twitter",
        url: (u) => `https://twitter.com/${u}`,
        container: 'article[data-testid="tweet"]',
        text: 'div[data-testid="tweetText"]',
        time: 'time[datetime]',
        accountBtn: 'button[data-testid="accountButton"], button[aria-label="Account menu"]',
        profileName: 'h1[data-testid="UserName"], h1',
        profileHandle: '[data-testid="UserDescription"] span, [data-testid="UserName"] + div > span',
        profileBio: '[data-testid="UserDescription"]',
        profileFollowers: 'a[href*="/verified_followers"]',
        getStats: (tweet) => ({
            replies: tweet.querySelector('[data-testid="reply"] [data-testid="count"]')?.innerText?.trim() || null,
            retweets: tweet.querySelector('[data-testid="retweet"] [data-testid="count"]')?.innerText?.trim() || null,
            likes: tweet.querySelector('[data-testid="like"] [data-testid="count"]')?.innerText?.trim() || null,
            shares: tweet.querySelector('[data-testid="share"] [data-testid="count"]')?.innerText?.trim() || null
        })
    },
    facebook: {
        name: "Facebook",
        url: (u) => `https://www.facebook.com/${u}`,
        container: 'div[data-pagelet^="FeedUnit_"], div[data-testid="post_message"], div[role="article"]',
        text: '[data-ad-preview], [data-testid="post_message"], .x1lliihq, .xdj266r, span[dir="auto"]',
        time: 'time, abbr[title], span[data-utime]',
        accountBtn: 'a[href*="/settings"], [aria-label*="account"], [role="button"] span',
        profileName: 'h1, span[aria-label*="Profile"], [data-testid="profile_name"]',
        profileHandle: '[data-testid="profile_username"], [data-testid="profile_header"] span',
        profileBio: '[data-testid="profile_bio"], [data-testid="profile_description"]',
        profileFollowers: 'a[href*="/followers"], [data-testid="followers"]',
        getStats: (post) => ({
            replies: post.querySelector('[data-testid="comment"], .x1i10hfl')?.innerText?.trim() || null,
            shares: post.querySelector('[data-testid="share"], .x1n2onr6')?.innerText?.trim() || null,
            likes: post.querySelector('[data-testid="like"], [aria-label*="like"]')?.innerText?.trim() || null,
            reactions: post.querySelector('[data-testid="react"], [aria-label*="reaction"]')?.innerText?.trim() || null
        })
    }
};
async function connectBrowser() {
    // Try CDP first (OpenClaw)
    try {
        const browser = await playwright_1.chromium.connectOverCDP(`http://localhost:${OPENCLAW_CDP_PORT}`);
        const contexts = browser.contexts();
        if (contexts.length > 0) {
            const context = contexts[0];
            const pages = context.pages();
            const page = pages.length > 0 ? pages[0] : await context.newPage();
            return { browser, context, page, mode: 'opencdl' };
        }
    }
    catch (e) {
        // ignore and try launching
    }
    // Launch new Brave
    const userDataDir = `/home/shuttle/.config/google-chrome`;
    const context = await playwright_1.chromium.launchPersistentContext(userDataDir, {
        headless: false,
        viewport: null,
        executablePath: '/usr/bin/brave-browser',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
    });
    const pages = context.pages();
    const page = pages.length > 0 ? pages[0] : await context.newPage();
    return { browser: null, context, page, mode: 'launch' };
}
async function extractPosts(page, selectors, max, withStats) {
    const container = selectors.container;
    try {
        await page.waitForSelector(container, { timeout: 8000 });
    }
    catch (e) {
        // ignore
    }
    return await page.evaluate(({ containerSel, textSel, timeSel, getStats, max: limit, withStats: flag }) => {
        const results = [];
        const posts = document.querySelectorAll(containerSel);
        console.log(`[TS] 找到 ${posts.length} 個帖子容器`);
        posts.forEach((post, idx) => {
            if (idx >= limit)
                return;
            try {
                const textEl = post.querySelector(textSel);
                const timeEl = post.querySelector(timeSel);
                const postData = {
                    time: timeEl ? (timeEl.getAttribute('datetime') || timeEl.getAttribute('data-utime') || timeEl.getAttribute('title') || timeEl.innerText?.trim()) : null,
                    text: textEl ? textEl.innerText?.trim() : null
                };
                if (flag) {
                    postData.stats = getStats(post);
                }
                results.push(postData);
            }
            catch (e) {
                // ignore
            }
        });
        // Fallback for Facebook if too few results
        if (results.length < limit && containerSel.includes('facebook')) {
            console.log('[TS] 主要選擇器效果不佳，嘗試備選方案...');
            const allDivs = document.querySelectorAll('div');
            const candidates = Array.from(allDivs).filter(div => {
                const txt = div.innerText || '';
                return txt.length >= 30 && txt.length <= 2000 && !div.closest('nav') && !div.closest('[role="navigation"]');
            }).slice(0, limit - results.length);
            candidates.forEach(div => {
                results.push({ time: null, text: div.innerText?.trim().substring(0, 500), stats: null });
            });
        }
        return results;
    }, { containerSel: container, textSel: selectors.text, timeSel: selectors.time, getStats: selectors.getStats, max, withStats });
}
async function extractProfile(page, selectors) {
    return await page.evaluate((s) => ({
        name: document.querySelector(s.profileName)?.innerText?.trim() || null,
        handle: document.querySelector(s.profileHandle)?.innerText?.trim() || null,
        bio: document.querySelector(s.profileBio)?.innerText?.trim() || null,
        followers: document.querySelector(s.profileFollowers)?.innerText?.trim() || null
    }), selectors);
}
async function detectLoginStatus(page, accountBtnSelector) {
    return await page.evaluate((sel) => {
        const btn = document.querySelector(sel);
        if (btn) {
            const text = btn.innerText?.trim();
            const img = btn.querySelector('img[alt]');
            return text || (img?.alt) || '已登入（未知帳號）';
        }
        return '未檢測到登入狀態';
    }, accountBtnSelector);
}
async function braveBrowsePlatform(username, options = {}) {
    const platformKey = (options.platform || 'x').toLowerCase();
    const platform = SELECTORS[platformKey];
    if (!platform) {
        throw new Error(`不支援的平台: ${platformKey}。支援：x, twitter, facebook`);
    }
    const maxPosts = options.maxPosts || 5;
    const includeStats = options.includeStats !== false;
    let browser = null;
    let context = null;
    let page = null;
    let mode = null;
    try {
        ({ browser, context, page, mode } = await connectBrowser());
        const url = platform.url(username);
        try {
            await page.goto(url, { waitUntil: 'load', timeout: 15000 });
        }
        catch (e) {
            // ignore
        }
        await page.waitForTimeout(platformKey === 'facebook' ? 5000 : 2000);
        const loginStatus = await detectLoginStatus(page, platform.accountBtn);
        const posts = await extractPosts(page, platform, maxPosts, includeStats);
        const profile = await extractProfile(page, platform);
        return {
            username,
            platform: platformKey,
            loginStatus,
            profile,
            posts,
            metadata: {
                maxPosts,
                includeStats,
                timestamp: new Date().toISOString(),
                connectionMode: mode
            }
        };
    }
    finally {
        // Do not close browser (keep session alive)
    }
}
// CLI entry
if (require.main === module) {
    let input = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', async () => {
        try {
            const options = input ? JSON.parse(input) : {};
            const args = process.argv.slice(2);
            const username = options.username || args[0];
            const platform = options.platform || args[1] || args[3] || 'x';
            const maxPosts = options.maxPosts || options.maxTweets || parseInt(args[2]) || parseInt(args[4]) || 5;
            const includeStats = options.includeStats !== undefined ? options.includeStats : (args[3] !== 'false' && args[5] !== 'false');
            if (!username) {
                console.error(JSON.stringify({
                    error: "缺少必要參數：username",
                    example: 'node index.js realDonaldTrump x 2 true',
                    json_format: '{"username":"realDonaldTrump","platform":"x","maxPosts":2,"includeStats":true}'
                }, null, 2));
                process.exit(1);
            }
            const result = await braveBrowsePlatform(username, { platform, maxPosts, includeStats });
            console.log(JSON.stringify(result, null, 2));
            process.exit(0);
        }
        catch (err) {
            console.error(JSON.stringify({ error: err.message, stack: process.env.DEBUG ? err.stack : undefined }));
            process.exit(1);
        }
    });
}
