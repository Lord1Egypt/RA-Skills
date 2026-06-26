/**
 * wellfound.mjs — Wellfound apply handler
 */
import {
  NAVIGATION_TIMEOUT, PAGE_LOAD_WAIT, FORM_FILL_WAIT, SUBMIT_WAIT
} from '../constants.mjs';

export const SUPPORTED_TYPES = ['wellfound', 'wellfound_apply'];

export async function apply(page, job, formFiller) {
  await page.goto(job.url, { waitUntil: 'domcontentloaded', timeout: NAVIGATION_TIMEOUT });
  await page.waitForTimeout(PAGE_LOAD_WAIT);

  const meta = await page.evaluate(() => ({
    title: document.querySelector('h1')?.textContent?.trim(),
    company: document.querySelector('[class*="company"] h2, [class*="startup"] h2, h2')?.textContent?.trim(),
  })).catch(() => ({}));

  // Check if listing is closed/unavailable
  const closed = await page.evaluate(() => {
    const text = (document.body.innerText || '').toLowerCase();
    return text.includes('no longer accepting') || text.includes('position has been filled') ||
           text.includes('this job is no longer') || text.includes('job not found');
  }).catch(() => false);
  if (closed) {
    console.log(`    ℹ️  Job closed — no longer available`);
    return { status: 'closed', meta };
  }

  const applyBtn = page.locator('a:has-text("Apply"), button:has-text("Apply Now"), a:has-text("Apply Now")').first();
  if (await applyBtn.count() === 0) return { status: 'no_button', meta };

  await applyBtn.click();
  await page.waitForTimeout(FORM_FILL_WAIT);

  const unknowns = await formFiller.fill(page, formFiller.profile.resume_path);

  if (unknowns[0]?.honeypot) return { status: 'skipped_honeypot', meta };
  if (unknowns.length > 0) return { status: 'needs_answer', pending_question: unknowns[0], meta };

  const submitBtn = await page.$('button[type="submit"]:not([disabled]), input[type="submit"]');
  if (!submitBtn) return { status: 'no_submit', meta };

  await submitBtn.click();
  await page.waitForTimeout(SUBMIT_WAIT);

  // Verify submission — check for success indicators or form gone
  const postSubmit = await page.evaluate(() => {
    const text = (document.body.innerText || '').toLowerCase();
    return {
      hasSuccess: text.includes('application submitted') || text.includes('successfully applied') ||
                  text.includes('thank you') || text.includes('application received'),
      hasForm: !!document.querySelector('form button[type="submit"]:not([disabled])'),
    };
  }).catch(() => ({ hasSuccess: false, hasForm: false }));

  if (postSubmit.hasSuccess || !postSubmit.hasForm) {
    return { status: 'submitted', meta };
  }

  console.log(`    ⚠️  Submit clicked but form still present — may not have submitted`);
  return { status: 'incomplete', meta };
}
