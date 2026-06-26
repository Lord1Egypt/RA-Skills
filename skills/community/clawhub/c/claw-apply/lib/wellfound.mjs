/**
 * wellfound.mjs — Wellfound search
 * Apply logic lives in lib/apply/wellfound.mjs
 */
import {
  WELLFOUND_BASE, NAVIGATION_TIMEOUT, SEARCH_NAVIGATION_TIMEOUT,
  SEARCH_LOAD_WAIT, SEARCH_SCROLL_WAIT, LOGIN_WAIT,
  SEARCH_RESULTS_MAX, WELLFOUND_MAX_INFINITE_SCROLL
} from './constants.mjs';

export async function verifyLogin(page) {
  await page.goto(`${WELLFOUND_BASE}/`, { waitUntil: 'domcontentloaded', timeout: NAVIGATION_TIMEOUT });
  await page.waitForTimeout(LOGIN_WAIT);
  const loggedIn = await page.evaluate(() =>
    document.body.innerText.includes('Applied') || document.body.innerText.includes('Open to offers')
  );
  return loggedIn;
}

export async function searchWellfound(page, search, { onPage } = {}) {
  const jobs = [];

  for (const keyword of search.keywords) {
    const url = `${WELLFOUND_BASE}/jobs?q=${encodeURIComponent(keyword)}&remote=true`;
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: SEARCH_NAVIGATION_TIMEOUT });
    } catch (e) {
      console.error(`    ⚠️ Navigation failed for "${keyword}": ${e.message}`);
      continue;
    }
    await page.waitForTimeout(SEARCH_LOAD_WAIT);

    // Scroll to bottom repeatedly to trigger infinite scroll
    let lastHeight = 0;
    for (let i = 0; i < WELLFOUND_MAX_INFINITE_SCROLL; i++) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(SEARCH_SCROLL_WAIT);
      const newHeight = await page.evaluate(() => document.body.scrollHeight);
      if (newHeight === lastHeight) break;
      lastHeight = newHeight;
    }

    const found = await page.evaluate(({ track, excludes, maxResults }) => {
      const seen = new Set();
      const results = [];

      document.querySelectorAll('a[href]').forEach(a => {
        const href = a.href;
        if (!href || seen.has(href)) return;
        const isJob = href.match(/wellfound\.com\/(jobs\/.{5,}|l\/.+)/) &&
                      !href.match(/\/(home|applications|messages|starred|on-demand|settings|profile|jobs\?)$/);
        if (!isJob) return;
        seen.add(href);

        const card = a.closest('[class*="job"]') || a.closest('[class*="card"]') || a.closest('div') || a.parentElement;
        const title = a.textContent?.trim().substring(0, 100) || '';
        const company = card?.querySelector('[class*="company"], [class*="startup"], h2')?.textContent?.trim() || '';

        // Exclusion filter
        const titleL = title.toLowerCase();
        const companyL = company.toLowerCase();
        for (const ex of excludes) {
          if (titleL.includes(ex.toLowerCase()) || companyL.includes(ex.toLowerCase())) return;
        }

        if (title.length > 3) {
          // Deterministic ID from URL path
          const slug = href.split('/').pop().split('?')[0];
          results.push({
            id: `wf_${slug}`,
            platform: 'wellfound',
            apply_type: 'wellfound',
            track,
            title,
            company,
            url: href,
          });
        }
      });

      return results.slice(0, maxResults);
    }, { track: search.track, excludes: search.exclude_keywords || [], maxResults: SEARCH_RESULTS_MAX });

    jobs.push(...found);
    if (found.length > 0 && onPage) onPage(found);
  }

  // Dedupe by URL
  const seen = new Set();
  return jobs.filter(j => { if (seen.has(j.url)) return false; seen.add(j.url); return true; });
}
