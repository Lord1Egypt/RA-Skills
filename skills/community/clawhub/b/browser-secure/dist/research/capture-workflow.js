import path from 'path';
import os from 'os';
import fs from 'fs';
import { extractContent, extractWithCustomSelectors } from './content-extractor.js';
import { getSiteProfile, saveCapture } from './scrapbook.js';
const SCREENSHOT_DIR = path.join(os.homedir(), '.browser-secure', 'scrapbook', 'screenshots');
const HTML_DIR = path.join(os.homedir(), '.browser-secure', 'scrapbook', 'html');
export async function capturePage(page, url, siteId, credentialsUsed, options = {}) {
    const profile = getSiteProfile(siteId);
    const auto = options.autoApproved ?? false;
    // Extract content using playbook selectors if available
    let content;
    const selectors = {};
    if (profile?.playbook?.extraction?.body_selector) {
        selectors.body = profile.playbook.extraction.body_selector;
        if (profile.playbook.extraction.title_selector)
            selectors.title = profile.playbook.extraction.title_selector;
        if (profile.playbook.extraction.author_selector)
            selectors.author = profile.playbook.extraction.author_selector;
        if (profile.playbook.extraction.date_selector)
            selectors.date = profile.playbook.extraction.date_selector;
        content = await extractWithCustomSelectors(page, selectors);
    }
    else if (profile?.content_selectors?.body) {
        content = await extractWithCustomSelectors(page, profile.content_selectors);
    }
    else {
        content = await extractContent(page);
    }
    // Screenshot
    const screenshotPath = path.join(SCREENSHOT_DIR, `capture-${Date.now()}.png`);
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    await page.screenshot({ path: screenshotPath, fullPage: false });
    // Optional HTML save
    let htmlPath;
    if (options.saveHtml) {
        fs.mkdirSync(HTML_DIR, { recursive: true });
        htmlPath = path.join(HTML_DIR, `page-${Date.now()}.html`);
        const html = await page.content();
        fs.writeFileSync(htmlPath, html, 'utf-8');
    }
    const capture = {
        id: `cap-${Date.now()}`,
        site_id: siteId,
        url,
        referrer: options.referrer,
        discovery_method: options.discoveryMethod,
        title: content.title,
        excerpt: content.excerpt,
        full_text: options.saveFullText ? content.body : undefined,
        html_path: htmlPath,
        word_count: content.wordCount,
        captured_at: new Date().toISOString(),
        credentials_used: credentialsUsed,
        screenshot: screenshotPath,
        selectors_used: selectors,
        approval_chain: {
            site_access: { approved: true, auto },
            credential_use: { approved: credentialsUsed, auto },
            extract_content: { approved: true, auto },
            record_content: { approved: true, auto },
        },
    };
    saveCapture(capture);
    return { capture, screenshotPath, htmlPath };
}
export function getCapturePreview(capture) {
    const lines = [
        `Title: ${capture.title || 'Untitled'}`,
        `Source: ${capture.site_id}`,
        `URL: ${capture.url}`,
        `Word count: ${capture.word_count || 0}`,
        `Captured: ${capture.captured_at}`,
        '',
        'Excerpt:',
        capture.excerpt || '(no excerpt)',
    ];
    if (capture.selectors_used && Object.keys(capture.selectors_used).length > 0) {
        lines.push('', 'Selectors used:');
        for (const [k, v] of Object.entries(capture.selectors_used)) {
            lines.push(`  ${k}: ${v}`);
        }
    }
    return lines.join('\n');
}
