import path from 'path';
import os from 'os';
import fs from 'fs';
import { extractContent } from './content-extractor.js';
const SCREENSHOT_DIR = path.join(os.homedir(), '.browser-secure', 'scrapbook', 'screenshots');
fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
function screenshotPath(prefix) {
    return path.join(SCREENSHOT_DIR, `${prefix}-${Date.now()}.png`);
}
async function takeScreenshot(page, prefix) {
    const p = screenshotPath(prefix);
    await page.screenshot({ path: p, fullPage: false });
    return p;
}
export async function analyzeSite(page, url) {
    const analysis = {
        url,
        hasLoginForm: false,
        hasSearch: false,
        navigation: [],
        contentLinks: [],
        suggestedSelectors: {},
        screenshots: [],
    };
    // Screenshot 1: landing page
    analysis.screenshots.push(await takeScreenshot(page, 'landing'));
    // 1. Detect login form
    const loginInfo = await page.evaluate(() => {
        const password = document.querySelector('input[type="password"]');
        const loginLinks = Array.from(document.querySelectorAll('a')).filter(a => /sign.in|log.in|login|authenticate|member/i.test(a.textContent || ''));
        return {
            hasPassword: !!password,
            loginLinkHref: loginLinks[0]?.getAttribute('href') || undefined,
            loginLinkText: loginLinks[0]?.textContent?.trim(),
        };
    });
    analysis.hasLoginForm = loginInfo.hasPassword || !!loginInfo.loginLinkHref;
    if (loginInfo.loginLinkHref) {
        analysis.loginUrl = loginInfo.loginLinkHref.startsWith('http')
            ? loginInfo.loginLinkHref
            : new URL(loginInfo.loginLinkHref, url).href;
    }
    // 2. Detect search
    const searchInfo = await page.evaluate(() => {
        const inputs = Array.from(document.querySelectorAll('input'));
        const searchInput = inputs.find(i => i.type === 'search' ||
            /search|q|query/i.test(i.name || '') ||
            /search|find/i.test(i.placeholder || ''));
        return {
            found: !!searchInput,
            selector: searchInput
                ? (searchInput.id ? `#${searchInput.id}` : `input[name="${searchInput.name}"]`)
                : undefined,
        };
    });
    analysis.hasSearch = searchInfo.found;
    if (searchInfo.selector)
        analysis.searchSelector = searchInfo.selector;
    // Screenshot 2: after analysis
    analysis.screenshots.push(await takeScreenshot(page, 'analyzed'));
    // 3. Extract navigation
    const navLinks = await page.evaluate(() => {
        const selectors = ['nav a', 'header a', '.menu a', '.navigation a', '#menu a'];
        for (const sel of selectors) {
            const links = Array.from(document.querySelectorAll(sel))
                .filter(a => {
                const el = a;
                return el.href && el.textContent && el.textContent.trim().length > 0 && el.textContent.trim().length < 50;
            })
                .slice(0, 10)
                .map(a => ({
                name: a.textContent.trim(),
                url: a.getAttribute('href') || '',
            }));
            if (links.length > 0)
                return links;
        }
        return [];
    });
    analysis.navigation = navLinks.map(l => ({
        name: l.name,
        url: l.url.startsWith('http') ? l.url : new URL(l.url, url).href,
    }));
    // 4. Extract content links (article listings)
    const contentLinks = await page.evaluate(() => {
        const articleLinks = Array.from(document.querySelectorAll('article a, .post a, .entry a, h2 a, h3 a, .title a'))
            .filter(a => {
            const el = a;
            return el.href && !el.href.includes('#') && el.textContent && el.textContent.trim().length > 10;
        })
            .slice(0, 5)
            .map(a => ({
            text: a.textContent.trim(),
            href: a.href,
        }));
        return articleLinks;
    });
    analysis.contentLinks = contentLinks.map(l => l.href);
    // 5. Test first content link to derive selectors
    if (analysis.contentLinks.length > 0) {
        try {
            await page.goto(analysis.contentLinks[0], { waitUntil: 'domcontentloaded', timeout: 15000 });
            await new Promise(r => setTimeout(r, 3000));
            analysis.screenshots.push(await takeScreenshot(page, 'sample-content'));
            const content = await extractContent(page);
            analysis.sampleExcerpt = content.excerpt;
            const detected = await page.evaluate(() => {
                const h1 = document.querySelector('h1');
                const titleSel = h1 ? (h1.id ? `h1#${h1.id}` : 'h1') : undefined;
                const article = document.querySelector('article');
                const main = document.querySelector('main');
                const bodySel = article
                    ? (article.className ? `article.${article.className.split(' ')[0]}` : 'article')
                    : main
                        ? (main.className ? `main.${main.className.split(' ')[0]}` : 'main')
                        : undefined;
                const authorEl = document.querySelector('.author, .byline, [rel="author"]');
                const authorSel = authorEl
                    ? (authorEl.className ? `.${authorEl.className.split(' ')[0]}` : '[rel="author"]')
                    : undefined;
                const timeEl = document.querySelector('time, .date, .publish-date');
                const dateSel = timeEl
                    ? (timeEl.className ? `.${timeEl.className.split(' ')[0]}` : 'time')
                    : undefined;
                return { titleSel, bodySel, authorSel, dateSel };
            });
            analysis.suggestedSelectors = {
                title: detected.titleSel,
                body: detected.bodySel,
                author: detected.authorSel,
                date: detected.dateSel,
            };
        }
        catch {
            // If sample content fails, leave selectors empty
        }
    }
    return analysis;
}
export function generateSiteId(url) {
    try {
        const u = new URL(url);
        return u.hostname.replace(/^www\./, '').replace(/\./g, '-');
    }
    catch {
        return url.replace(/[^a-z0-9]/gi, '-').toLowerCase();
    }
}
export function buildPlaybook(analysis, loginRequired) {
    return {
        discovery: {
            method: analysis.hasSearch ? 'search' : 'browse',
            search_url: analysis.hasSearch ? analysis.url : undefined,
            search_input_selector: analysis.searchSelector,
            search_submit_action: 'press enter',
            browse_url: analysis.contentLinks.length > 0
                ? analysis.contentLinks[0].replace(/\/[^/]*\/?$/, '')
                : analysis.url,
        },
        access: {
            login_required: loginRequired,
            login_url: analysis.loginUrl,
            login_form_selector: loginRequired ? 'form' : undefined,
        },
        extraction: {
            title_selector: analysis.suggestedSelectors.title,
            body_selector: analysis.suggestedSelectors.body,
            author_selector: analysis.suggestedSelectors.author,
            date_selector: analysis.suggestedSelectors.date,
        },
    };
}
export function buildSiteProfile(url, analysis, loginRequired, sampleExcerpt) {
    const id = generateSiteId(url);
    return {
        id,
        name: id,
        url,
        login_required: loginRequired,
        search: analysis.hasSearch
            ? { available: true, input_selector: analysis.searchSelector, submit_action: 'press enter' }
            : { available: false },
        navigation: analysis.navigation.slice(0, 5),
        content_selectors: analysis.suggestedSelectors,
        playbook: buildPlaybook(analysis, loginRequired),
        sample_excerpt: sampleExcerpt,
        init_confirmed_at: new Date().toISOString(),
        screenshots: analysis.screenshots,
    };
}
