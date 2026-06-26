/**
 * easy_apply.mjs — LinkedIn Easy Apply handler
 * Handles the LinkedIn Easy Apply modal flow
 *
 * IMPORTANT: LinkedIn renders the Easy Apply modal inside shadow DOM.
 * This means document.querySelector() inside evaluate() CANNOT find it.
 * Playwright's page.$() pierces shadow DOM, so we use ElementHandle-based
 * operations throughout — never document.querySelector for the modal.
 *
 * Button detection strategy: LinkedIn frequently changes aria-labels and button
 * structure. We use multiple fallback strategies:
 * 1. CSS selector via page.$() (pierces shadow DOM)
 * 2. ElementHandle.evaluate() for text matching (runs on already-found elements)
 *
 * Modal flow: Easy Apply → [fill → Next] × N → Review → Submit application
 * Check order per step: Next → Review → Submit (only submit when no forward nav exists)
 */
import {
  NAVIGATION_TIMEOUT, CLICK_WAIT, MODAL_STEP_WAIT,
  SUBMIT_WAIT, DISMISS_TIMEOUT, APPLY_CLICK_TIMEOUT,
  LINKEDIN_EASY_APPLY_MODAL_SELECTOR,
  LINKEDIN_MAX_MODAL_STEPS
} from '../constants.mjs';

export const SUPPORTED_TYPES = ['easy_apply'];

/**
 * Find a non-disabled button inside the modal using multiple strategies.
 * All searches use page.$() which pierces shadow DOM, unlike document.querySelector().
 *
 * @param {Page} page - Playwright page
 * @param {string} modalSelector - CSS selector for the modal container
 * @param {Object} opts
 * @param {string[]} opts.ariaLabels - aria-label values to try (exact then substring)
 * @param {string[]} opts.exactTexts - exact button text matches (case-insensitive, trimmed)
 * @returns {ElementHandle|null}
 */
async function findModalButton(page, modalSelector, { ariaLabels = [], exactTexts = [] }) {
  // Strategy 1: aria-label exact match inside modal (non-disabled only)
  // page.$() pierces shadow DOM — safe to use compound selectors
  for (const label of ariaLabels) {
    const btn = await page.$(`${modalSelector} button[aria-label="${label}"]:not([disabled])`);
    if (btn) return btn;
  }

  // Strategy 2: aria-label substring match inside modal
  for (const label of ariaLabels) {
    const btn = await page.$(`${modalSelector} button[aria-label*="${label}"]:not([disabled])`);
    if (btn) return btn;
  }

  // Strategy 3: find modal via page.$(), then scan buttons via ElementHandle.evaluate()
  // This works because evaluate() on an ElementHandle runs in the element's context
  if (exactTexts.length === 0) return null;

  const modal = await page.$(modalSelector);
  if (!modal) return null;

  // Get all non-disabled buttons inside the modal
  const buttons = await modal.$$('button:not([disabled])');
  const targets = exactTexts.map(t => t.toLowerCase());

  for (const btn of buttons) {
    const text = await btn.evaluate(el =>
      (el.innerText || el.textContent || '').trim().toLowerCase()
    ).catch(() => '');
    if (targets.includes(text)) return btn;
  }

  return null;
}

/**
 * Get debug info about the modal using ElementHandle operations.
 * Does NOT use document.querySelector — uses page.$() which pierces shadow DOM.
 */
async function getModalDebugInfo(page, modalSelector) {
  const modal = await page.$(modalSelector);
  if (!modal) return { heading: '', buttons: [], errors: [] };

  // Single evaluate to extract all debug info at once
  return await modal.evaluate((el) => {
    const headingEl = el.querySelector('h1, h2, h3, [class*="title"], [class*="heading"]');
    const heading = headingEl?.textContent?.trim()?.slice(0, 60) || '';

    const buttons = [];
    for (const b of el.querySelectorAll('button, [role="button"]')) {
      const text = (b.innerText || b.textContent || '').trim().slice(0, 50);
      const aria = b.getAttribute('aria-label');
      const disabled = b.disabled;
      if (text || aria) buttons.push({ text, aria, disabled });
    }

    const errors = [];
    for (const e of el.querySelectorAll('[class*="error"], [aria-invalid="true"], .artdeco-inline-feedback--error')) {
      const text = e.textContent?.trim()?.slice(0, 60) || '';
      if (text) errors.push(text);
    }

    return { heading, buttons, errors };
  }).catch(() => ({ heading: '', buttons: [], errors: [] }));
}

/**
 * Find the Easy Apply modal among potentially multiple [role="dialog"] elements.
 * Returns the dialog that contains apply-related content (form, progress bar, submit button).
 * Falls back to the first dialog if none match specifically.
 */
async function findApplyModal(page) {
  const dialogs = await page.$$('[role="dialog"]');
  if (dialogs.length <= 1) return dialogs[0] || null;

  // Multiple dialogs — find the one with apply content
  for (const d of dialogs) {
    const isApply = await d.evaluate(el => {
      const text = (el.innerText || '').toLowerCase();
      const hasForm = el.querySelector('form, input, select, textarea, fieldset') !== null;
      const hasProgress = el.querySelector('progress, [role="progressbar"]') !== null;
      const hasApplyHeading = /apply to\b/i.test(text);
      return hasForm || hasProgress || hasApplyHeading;
    }).catch(() => false);
    if (isApply) return d;
  }

  return dialogs[0]; // fallback
}

export async function apply(page, job, formFiller) {
  const meta = { title: job.title, company: job.company };

  // Navigate directly to the apply URL — opens the modal without needing to find/click the button
  const applyUrl = job.url.replace(/\/$/, '') + '/apply/?openSDUIApplyFlow=true';
  await page.goto(applyUrl, { waitUntil: 'domcontentloaded', timeout: NAVIGATION_TIMEOUT });

  // Read meta from the job page (renders behind the modal)
  const pageMeta = await page.evaluate(() => ({
    title: document.querySelector('.job-details-jobs-unified-top-card__job-title, h1[class*="title"]')?.textContent?.trim(),
    company: document.querySelector('.job-details-jobs-unified-top-card__company-name a, .jobs-unified-top-card__company-name a')?.textContent?.trim(),
  })).catch(() => ({}));
  Object.assign(meta, pageMeta);

  // Wait for modal to appear
  let modal = await page.waitForSelector(LINKEDIN_EASY_APPLY_MODAL_SELECTOR, { timeout: 10000 }).catch(() => null);

  if (!modal) {
    // Check if the listing is closed
    const closed = await page.evaluate(() => {
      const text = (document.body.innerText || '').toLowerCase();
      return text.includes('no longer accepting') || text.includes('no longer available') ||
             text.includes('this job has expired') || text.includes('job is closed');
    }).catch(() => false);
    if (closed) {
      console.log(`    ℹ️  Job closed — no longer accepting applications`);
      return { status: 'closed', meta };
    }
    console.log(`    ❌ Modal did not open. Page URL: ${page.url()}`);
    return { status: 'no_modal', meta };
  }

  // If multiple [role="dialog"] exist (cookie banners, notifications), tag the apply modal
  // so all subsequent selectors target the right one
  const applyModal = await findApplyModal(page);
  let MODAL = LINKEDIN_EASY_APPLY_MODAL_SELECTOR;
  if (applyModal) {
    const multipleDialogs = (await page.$$('[role="dialog"]')).length > 1;
    if (multipleDialogs) {
      await applyModal.evaluate(el => el.setAttribute('data-claw-apply-modal', 'true'));
      MODAL = '[data-claw-apply-modal="true"]';
      console.log(`    ℹ️  Multiple dialogs detected — tagged apply modal`);
    }
  }

  // Step through modal
  let samePageCount = 0;
  for (let step = 0; step < LINKEDIN_MAX_MODAL_STEPS; step++) {
    const modalStillOpen = await page.$(MODAL);
    if (!modalStillOpen) {
      console.log(`    ✅ Modal closed — submitted`);
      return { status: 'submitted', meta };
    }

    // Read progress bar — LinkedIn uses <progress> element (no explicit role="progressbar")
    const progressEl = await page.$(`${MODAL} progress, ${MODAL} [role="progressbar"]`);
    const progress = progressEl
      ? await progressEl.evaluate(el => el.getAttribute('aria-valuenow') || el.value?.toString() || el.getAttribute('value') || el.style?.width || '').catch(() => '')
      : '';

    // Debug snapshot using ElementHandle operations (shadow DOM safe)
    const debugInfo = await getModalDebugInfo(page, MODAL);
    console.log(`    [step ${step}] progress=${progress} heading="${debugInfo.heading}" buttons=${JSON.stringify(debugInfo.buttons)}${debugInfo.errors.length ? ' errors=' + JSON.stringify(debugInfo.errors) : ''}`);

    // LinkedIn sometimes opens sub-forms (education, experience, date pickers) with Cancel/Save.
    // Dismiss them before filling to avoid filling sub-form fields.
    const cancelBtn = await findModalButton(page, MODAL, { ariaLabels: [], exactTexts: ['Cancel'] });
    if (cancelBtn) {
      console.log(`    [step ${step}] sub-form/picker detected — cancelling`);
      await cancelBtn.click({ timeout: APPLY_CLICK_TIMEOUT }).catch(() => {});
      await page.waitForTimeout(CLICK_WAIT);
      // Check if another Cancel is still open (e.g. date picker behind education form)
      const cancelBtn2 = await findModalButton(page, MODAL, { ariaLabels: [], exactTexts: ['Cancel'] });
      if (cancelBtn2) {
        await cancelBtn2.click({ timeout: APPLY_CLICK_TIMEOUT }).catch(() => {});
        await page.waitForTimeout(CLICK_WAIT);
      }
    }

    // Fill form fields — page.$() in form_filler pierces shadow DOM
    const unknowns = await formFiller.fill(page, formFiller.profile.resume_path);
    if (unknowns.length > 0) console.log(`    [step ${step}] unknown fields: ${JSON.stringify(unknowns.map(u => u.label || u))}`);

    if (unknowns[0]?.honeypot) {
      console.log(`    ⏸️  STOPPING — honeypot detected: "${unknowns[0].label}". Dismissing modal.`);
      await dismissModal(page, MODAL);
      return { status: 'skipped_honeypot', meta };
    }

    if (unknowns.length > 0) {
      console.log(`    ⏸️  STOPPING — unknown required field: "${unknowns[0].label || unknowns[0]}". Dismissing modal, will ask via Telegram.`);
      await dismissModal(page, MODAL);
      return { status: 'needs_answer', pending_question: unknowns[0], meta };
    }

    await page.waitForTimeout(MODAL_STEP_WAIT);

    // Check for validation errors after form fill (shadow DOM safe)
    const postModal = await page.$(MODAL);
    const postFillErrors = [];
    if (postModal) {
      const errorEls = await postModal.$$('[class*="error"], [aria-invalid="true"], .artdeco-inline-feedback--error');
      for (const e of errorEls) {
        const text = await e.evaluate(el => el.textContent?.trim()?.slice(0, 80) || '').catch(() => '');
        if (text) postFillErrors.push(text);
      }
    }

    if (postFillErrors.length > 0) {
      console.log(`    [step ${step}] ❌ Validation errors after fill: ${JSON.stringify(postFillErrors)}`);
      console.log(`    Action: check answers.json or profile.json for missing/wrong answers`);
      await dismissModal(page, MODAL);
      return { status: 'incomplete', meta, validation_errors: postFillErrors };
    }

    // --- Button check order: Next → Review → Submit ---
    // Check Next first — only fall through to Submit when there's no forward navigation.
    // This prevents accidentally clicking a Submit-like element on early modal steps.

    // Check for Next button
    const nextBtn = await findModalButton(page, MODAL, {
      ariaLabels: ['Continue to next step'],
      exactTexts: ['Next'],
    });
    if (nextBtn) {
      console.log(`    [step ${step}] clicking Next`);
      await nextBtn.click({ timeout: APPLY_CLICK_TIMEOUT }).catch(() => {});

      // Detect if we're stuck — wait for content to change after clicking Next
      await page.waitForTimeout(CLICK_WAIT);
      const newProgress = await (async () => {
        const el = await page.$(`${MODAL} progress, ${MODAL} [role="progressbar"]`);
        return el ? await el.evaluate(e => e.getAttribute('aria-valuenow') || e.value?.toString() || '').catch(() => '') : '';
      })();

      if (newProgress === progress) {
        samePageCount++;
        if (samePageCount >= 3) {
          console.log(`    [step ${step}] stuck — clicked Next ${samePageCount} times but progress unchanged at ${progress}`);
          console.log(`    Action: a required field may be unfilled. Check select dropdowns still at "Select an option"`);
          await dismissModal(page, MODAL);
          return { status: 'stuck', meta };
        }
      } else {
        samePageCount = 0;
      }
      continue;
    }

    // Check for Review button
    const reviewBtn = await findModalButton(page, MODAL, {
      ariaLabels: ['Review your application'],
      exactTexts: ['Review'],
    });
    if (reviewBtn) {
      console.log(`    [step ${step}] clicking Review`);
      await reviewBtn.click({ timeout: APPLY_CLICK_TIMEOUT }).catch(() => {});
      await page.waitForTimeout(CLICK_WAIT);
      samePageCount = 0;
      continue;
    }

    // Check for Submit button (only when no Next/Review exists)
    const submitBtn = await findModalButton(page, MODAL, {
      ariaLabels: ['Submit application'],
      exactTexts: ['Submit application'],
    });
    if (submitBtn) {
      console.log(`    [step ${step}] clicking Submit`);
      await submitBtn.click({ timeout: APPLY_CLICK_TIMEOUT }).catch(() => {});

      // Wait for modal to close — LinkedIn may take a few seconds after submit
      const modalClosed = await page.waitForSelector(MODAL, { state: 'detached', timeout: 8000 }).then(() => true).catch(() => false);
      if (modalClosed) {
        console.log(`    ✅ Submit confirmed — modal closed`);
        return { status: 'submitted', meta };
      }

      // Modal still open — LinkedIn often shows a post-submit confirmation/success
      // dialog that still matches [role="dialog"]. Check for success indicators.
      const postSubmitModal = await page.$(MODAL);
      if (postSubmitModal) {
        const postSubmitInfo = await postSubmitModal.evaluate(el => {
          const text = (el.innerText || el.textContent || '').toLowerCase();
          return {
            hasSuccess: text.includes('application was sent') || text.includes('applied') ||
                        text.includes('thank you') || text.includes('submitted') ||
                        text.includes('application has been') || text.includes('successfully'),
            hasDone: text.includes('done') || text.includes('got it'),
            snippet: (el.innerText || '').trim().slice(0, 200),
          };
        }).catch(() => ({ hasSuccess: false, hasDone: false, snippet: '' }));

        console.log(`    [step ${step}] post-submit modal: "${postSubmitInfo.snippet}"`);

        if (postSubmitInfo.hasSuccess || postSubmitInfo.hasDone) {
          console.log(`    ✅ Submit confirmed — success dialog detected`);
          // Try to dismiss the success dialog
          const doneBtn = await findModalButton(page, MODAL, {
            ariaLabels: ['Dismiss', 'Done', 'Close'],
            exactTexts: ['Done', 'Got it', 'Close'],
          });
          if (doneBtn) await doneBtn.click().catch(() => {});
          return { status: 'submitted', meta };
        }

        // Check for validation errors — real failure
        const postErrors = await postSubmitModal.$$('[class*="error"], [aria-invalid="true"], .artdeco-inline-feedback--error');
        const errorTexts = [];
        for (const e of postErrors) {
          const t = await e.evaluate(el => el.textContent?.trim()?.slice(0, 80) || '').catch(() => '');
          if (t) errorTexts.push(t);
        }

        if (errorTexts.length > 0) {
          console.log(`    [step ${step}] ❌ Validation errors after Submit: ${JSON.stringify(errorTexts)}`);
          await dismissModal(page, MODAL);
          return { status: 'incomplete', meta, validation_errors: errorTexts };
        }

        // No errors, no success text — but Submit button is gone, likely succeeded
        // (LinkedIn sometimes shows a follow-up prompt like "Follow company?")
        const submitStillThere = await findModalButton(page, MODAL, {
          ariaLabels: ['Submit application'],
          exactTexts: ['Submit application'],
        });
        if (!submitStillThere) {
          console.log(`    ✅ Submit likely succeeded — Submit button gone, no errors`);
          await dismissModal(page, MODAL);
          return { status: 'submitted', meta };
        }

        console.log(`    [step ${step}] ⚠️  Submit button still present — click may not have registered`);
        await dismissModal(page, MODAL);
        return { status: 'incomplete', meta };
      }
    }

    // Stuck detection — no Next/Review/Submit found
    // (stuck-after-click detection is handled above in the Next button section)

    console.log(`    [step ${step}] ❌ No Next/Review/Submit button found in modal`);
    console.log(`    Action: LinkedIn may have changed button text/structure. Check button snapshot above.`);
    break;
  }

  await dismissModal(page, MODAL);
  return { status: 'incomplete', meta };
}

/**
 * Dismiss the Easy Apply modal.
 * Tries multiple strategies: Dismiss button → Close/X → Escape key.
 * Handles the "Discard" confirmation dialog that appears after Escape.
 * All searches use page.$() which pierces shadow DOM.
 */
async function dismissModal(page, modalSelector) {
  // Step 1: Close the modal — Dismiss button, Close/X, or Escape
  const dismissBtn = await page.$(`${modalSelector} button[aria-label="Dismiss"]`);
  if (dismissBtn) {
    await dismissBtn.click({ timeout: DISMISS_TIMEOUT }).catch(() => {});
  } else {
    const closeBtn = await page.$(`${modalSelector} button[aria-label="Close"], ${modalSelector} button[aria-label*="close"]`);
    if (closeBtn) {
      await closeBtn.click({ timeout: DISMISS_TIMEOUT }).catch(() => {});
    } else {
      await page.keyboard.press('Escape').catch(() => {});
    }
  }

  // Step 2: LinkedIn shows a "Discard" confirmation — always wait for it and click
  const discardBtn = await page.waitForSelector(
    'button[data-test-dialog-primary-btn]',
    { timeout: DISMISS_TIMEOUT, state: 'visible' }
  ).catch(() => null);
  if (discardBtn) {
    await discardBtn.click().catch(() => {});
    await page.waitForTimeout(500);
    return;
  }

  // Fallback: find Discard by text — scope to dialogs/modals to avoid clicking wrong buttons
  const dialogBtns = await page.$$('[role="dialog"] button, [role="alertdialog"] button, [data-test-modal] button');
  for (const btn of dialogBtns) {
    const text = await btn.evaluate(el => (el.innerText || '').trim().toLowerCase()).catch(() => '');
    if (text === 'discard') {
      await btn.click().catch(() => {});
      await page.waitForTimeout(500);
      return;
    }
  }
}
