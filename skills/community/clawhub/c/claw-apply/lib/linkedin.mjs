/**
 * linkedin.mjs — LinkedIn search + job classification
 * Apply logic lives in lib/apply/easy_apply.mjs
 */
import {
  LINKEDIN_BASE, NAVIGATION_TIMEOUT, FEED_NAVIGATION_TIMEOUT,
  PAGE_LOAD_WAIT, SCROLL_WAIT, CLICK_WAIT,
  EXTERNAL_ATS_PATTERNS, LINKEDIN_MAX_SEARCH_PAGES, LINKEDIN_SECONDS_PER_DAY
} from './constants.mjs';

export async function verifyLogin(page) {
  await page.goto(`${LINKEDIN_BASE}/feed/`, { waitUntil: 'domcontentloaded', timeout: FEED_NAVIGATION_TIMEOUT });
  await page.waitForTimeout(CLICK_WAIT);
  return page.url().includes('/feed');
}

export async function searchLinkedIn(page, search, { onPage, onKeyword } = {}) {
  const callbacks = { onPage, onKeyword };
  const jobs = [];
  const seenIds = new Set();

  for (let ki = 0; ki < search.keywords.length; ki++) {
    const keyword = search.keywords[ki];
    const globalIdx = (search.keywordOffset || 0) + ki;
    const globalTotal = (search.keywordOffset || 0) + search.keywords.length;
    console.log(`  [${search.track_label || search.track}] keyword ${globalIdx + 1}/${globalTotal}: "${keyword}"`);
    const params = new URLSearchParams({ keywords: keyword, sortBy: 'DD' });
    if (search.filters?.remote) params.set('f_WT', '2');
    if (search.filters?.easy_apply_only) params.set('f_LF', 'f_AL');
    if (search.filters?.posted_within_days) {
      params.set('f_TPR', `r${search.filters.posted_within_days * LINKEDIN_SECONDS_PER_DAY}`);
    }

    const url = `${LINKEDIN_BASE}/jobs/search/?${params.toString()}`;
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: NAVIGATION_TIMEOUT });
    } catch (e) {
      console.error(`    ⚠️ Navigation failed for "${keyword}": ${e.message}`);
      continue;
    }
    await page.waitForTimeout(PAGE_LOAD_WAIT);

    let pageNum = 0;
    while (pageNum < LINKEDIN_MAX_SEARCH_PAGES) {
      // Scroll to load all cards
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(SCROLL_WAIT);

      // Get all job IDs on this page
      const pageIds = await page.evaluate(() =>
        [...new Set(
          Array.from(document.querySelectorAll('a[href*="/jobs/view/"]'))
            .map(a => a.href.match(/\/jobs\/view\/(\d+)/)?.[1])
            .filter(Boolean)
        )]
      );

      const pageJobs = [];

      for (const jobId of pageIds) {
        if (seenIds.has(jobId)) continue;

        // Click the job card to load right panel
        try {
          await page.evaluate((id) => {
            const link = document.querySelector(`a[href*="/jobs/view/${id}"]`);
            link?.closest('li')?.click() || link?.click();
          }, jobId);
          await page.waitForTimeout(CLICK_WAIT);
        } catch (e) {
          console.warn(`    ⚠️ Could not click job card ${jobId}: ${e.message}`);
        }

        // Read title, company, location from detail panel (more accurate)
        const meta = await page.evaluate(({ id, track, excludes }) => {
          const panel = document.querySelector('.jobs-unified-top-card, .job-details-jobs-unified-top-card__job-title');
          const title = document.querySelector('.job-details-jobs-unified-top-card__job-title, h1[class*="title"]')?.textContent?.trim()
            || document.querySelector('.jobs-unified-top-card__job-title')?.textContent?.trim() || '';
          const company = document.querySelector('.job-details-jobs-unified-top-card__company-name a, .jobs-unified-top-card__company-name a')?.textContent?.trim() || '';
          // .tvm__text spans contain: location, "·", time ago, "·", applicants, work type, etc.
          const tvmTexts = Array.from(document.querySelectorAll('.tvm__text')).map(e => e.textContent.trim()).filter(s => s && s !== '·');
          const location = tvmTexts[0] || ''; // first non-separator is location
          const workType = tvmTexts.find(t => ['Remote', 'Hybrid', 'On-site'].includes(t)) || '';

          const tl = title.toLowerCase(), cl = company.toLowerCase();
          for (const ex of excludes) {
            if (tl.includes(ex.toLowerCase()) || cl.includes(ex.toLowerCase())) return null;
          }
          const description = document.querySelector('.job-details-about-the-job-module__description')?.textContent?.trim().slice(0, 2000) || '';
          return { title, company, location, work_type: workType, description };
        }, { id: jobId, track: search.track, excludes: search.exclude_keywords || [] });

        if (!meta) { seenIds.add(jobId); continue; } // excluded

        // Detect apply type from right panel
        const applyInfo = await page.evaluate(({ atsPatterns }) => {
          const eaBtn = document.querySelector('button.jobs-apply-button[aria-label*="Easy Apply"]');
          if (eaBtn) return { apply_type: 'easy_apply', apply_url: null };

          const interestedBtn = document.querySelector('button[aria-label*="interested"]');
          if (interestedBtn) return { apply_type: 'recruiter_only', apply_url: null };

          // Look for external ATS link
          const allLinks = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
          for (const href of allLinks) {
            for (const { name, pattern } of atsPatterns) {
              if (new RegExp(pattern).test(href)) return { apply_type: name, apply_url: href };
            }
          }

          const externalBtn = document.querySelector('button.jobs-apply-button:not([aria-label*="Easy Apply"])');
          if (externalBtn) return { apply_type: 'unknown_external', apply_url: null };

          return { apply_type: 'unknown', apply_url: null };
        }, { atsPatterns: EXTERNAL_ATS_PATTERNS.map(({ name, pattern }) => ({ name, pattern: pattern.source })) });

        seenIds.add(jobId);
        const job = {
          id: `li_${jobId}`,
          platform: 'linkedin',
          track: search.track,
          jobId,
          url: `https://www.linkedin.com/jobs/view/${jobId}/`,
          classified_at: Date.now(),
          ...meta,
          ...applyInfo,
        };
        pageJobs.push(job);
        jobs.push(job);
      }

      if (pageJobs.length > 0 && callbacks.onPage) callbacks.onPage(pageJobs);

      const nextBtn = await page.$('button[aria-label="View next page"]');
      if (!nextBtn) break;
      await nextBtn.click();
      await page.waitForTimeout(PAGE_LOAD_WAIT);
      pageNum++;
    }
    // Mark keyword complete after all its pages are done
    callbacks.onKeyword?.(ki);
  }

  return jobs;
}
