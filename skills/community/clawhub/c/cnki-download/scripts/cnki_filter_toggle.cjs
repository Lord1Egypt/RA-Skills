/**
 * CNKI filter expand/collapse helper (Node + Playwright)
 *
 * 核心函数 ensureFilterExpanded(page, groupitem, options):
 *   - 用稳定选择器 dt[groupitem="..."] i.icon-arrow
 *   - 状态判断用 getComputedStyle(dd).display (不用 className, 2026-06-05 复盘过)
 *   - 折叠 -> scrollIntoViewIfNeeded -> click -> waitForFunction 等展开
 *   - 已展开 -> 直接返回 { wasFolded: false }
 *
 * 2026-06-07 created by 小麻烦 (OpenClaw assistant)
 */

const { chromium } = require('playwright');

/**
 * Ensure the CNKI filter with given groupitem is expanded.
 * If already expanded -> no-op, returns { wasFolded: false }.
 * If folded -> scrolls into view, clicks arrow, waits for dd to become visible.
 *
 * @param {import('playwright').Page} page - Playwright Page (must be on a CNKI result page)
 * @param {string} groupitem - CNKI filter dt groupitem attribute (e.g. "年度", "来源类别")
 * @param {object} [options]
 * @param {number} [options.timeout=5000] - Wait timeout in ms
 * @param {boolean} [options.verbose=false] - Print detailed logs
 * @returns {Promise<{groupitem: string, wasFolded: boolean, isExpanded: boolean,
 *                    beforeDisplay: string, afterDisplay: string, dlClass: string}>}
 */
async function ensureFilterExpanded(page, groupitem, options = {}) {
  const { timeout = 5000, verbose = false } = options;

  const log = verbose ? console.log : () => {};

  // 1. Probe: dt must be unique
  await page.locator('dt[groupitem="年度"]').scrollIntoViewIfNeeded();
  const dtCount = await page.locator(`dt[groupitem="${groupitem}"]`).count();
  if (dtCount !== 1) {
    throw new Error(
      `[${groupitem}] dt not unique: count=${dtCount}. ` +
      `Make sure you are on a CNKI result page (kns8s/defaultresult/index) with the filter visible.`
    );
  }

  // 2. Read current state (use computed style, NOT className)
  const beforeState = await page.evaluate((title) => {
    const dt = document.querySelector(`dt[groupitem="${title}"]`);
    const dl = dt.parentElement;
    const dd = dl.querySelector('dd');
    const arrow = dt.querySelector('i.icon-arrow');
    let arrowRect = null;
    if (arrow) {
      const r = arrow.getBoundingClientRect();
      arrowRect = { x: r.x, y: r.y, w: r.width, h: r.height };
    }
    return {
      dlClass: dl.className,
      ddDisplay: getComputedStyle(dd).display,
      hasArrow: !!arrow,
      arrowRect
    };
  }, groupitem);

  log(`[${groupitem}] before: ddDisplay=${beforeState.ddDisplay} dlClass="${beforeState.dlClass}" arrow=${beforeState.hasArrow ? JSON.stringify(beforeState.arrowRect) : 'NONE'}`);

  if (!beforeState.hasArrow) {
    throw new Error(`[${groupitem}] arrow <i class="icon icon-arrow"> not found inside dt`);
  }

  // 3. Already expanded -> no-op
  if (beforeState.ddDisplay === 'block') {
    log(`[${groupitem}] already expanded, skip click`);
    return {
      groupitem,
      wasFolded: false,
      isExpanded: true,
      beforeDisplay: beforeState.ddDisplay,
      afterDisplay: beforeState.ddDisplay,
      dlClass: beforeState.dlClass
    };
  }

  // 4. Folded -> scroll into view -> click arrow
  // Use parent dl to scroll, then click the i.icon-arrow (uniquely located by parent dt)
  log(`[${groupitem}] folded (ddDisplay=${beforeState.ddDisplay}), scrolling into view and clicking...`);
  await page.locator(`dt[groupitem="${groupitem}"]`).scrollIntoViewIfNeeded();

  // Small wait for any animation
  await page.waitForTimeout(100);

  // Click the arrow inside the dt
  await page.locator(`dt[groupitem="${groupitem}"] i.icon-arrow`).click();

  // 5. Wait for state change (use computed style, not className)
  try {
    await page.waitForFunction(
      (title) => {
        const dt = document.querySelector(`dt[groupitem="${title}"]`);
        if (!dt) return false;
        const dd = dt.parentElement.querySelector('dd');
        return getComputedStyle(dd).display === 'block';
      },
      groupitem,
      { timeout }
    );
  } catch (err) {
    // Capture diagnostic info on timeout
    const debugState = await page.evaluate((title) => {
      const dt = document.querySelector(`dt[groupitem="${title}"]`);
      const dl = dt.parentElement;
      const dd = dl.querySelector('dd');
      return {
        dlClass: dl.className,
        ddDisplay: getComputedStyle(dd).display,
        dtOuterHTML: dt.outerHTML.slice(0, 400)
      };
    }, groupitem);
    throw new Error(
      `[${groupitem}] click did not expand within ${timeout}ms. ` +
      `Final state: dlClass="${debugState.dlClass}" ddDisplay=${debugState.ddDisplay}. ` +
      `dt: ${debugState.dtOuterHTML}`
    );
  }

  // 6. Read final state
  const afterState = await page.evaluate((title) => {
    const dt = document.querySelector(`dt[groupitem="${title}"]`);
    const dl = dt.parentElement;
    const dd = dl.querySelector('dd');
    return {
      dlClass: dl.className,
      ddDisplay: getComputedStyle(dd).display
    };
  }, groupitem);

  log(`[${groupitem}] after: ddDisplay=${afterState.ddDisplay} dlClass="${afterState.dlClass}"`);

  return {
    groupitem,
    wasFolded: true,
    isExpanded: afterState.ddDisplay === 'block',
    beforeDisplay: beforeState.ddDisplay,
    afterDisplay: afterState.ddDisplay,
    dlClass: afterState.dlClass
  };
}

/**
 * Batch version: ensure multiple filters are expanded.
 *
 * @param {import('playwright').Page} page
 * @param {string[]} groupitems
 * @param {object} [options]
 * @returns {Promise<Array<{groupitem: string, wasFolded: boolean, isExpanded: boolean, ...}>>}
 */
async function ensureFiltersExpanded(page, groupitems, options = {}) {
  const results = [];
  for (const gi of groupitems) {
    const r = await ensureFilterExpanded(page, gi, options);
    results.push(r);
   }
  return results;
}

// ============== CLI entry ==============
if (require.main === module) {
  (async () => {
    // Parse args:
    //   node cnki_filter_toggle.js [groupitem1,groupitem2,...] [--headless] [--url <url>]
    const args = process.argv.slice(2);
    let groupitems = ['年度', '来源类别'];
    let headless = false;
    let url = 'https://www.cnki.net/';  // 默认个人入口；可由 --url 覆盖

    for (let i = 0; i < args.length; i++) {
      const arg = args[i];
      if (arg === '--headless') {
        headless = true;
      } else if (arg === '--url') {
        url = args[++i] || url;
      } else if (arg === '--help' || arg === '-h') {
        console.log('Usage: node cnki_filter_toggle.js [groupitem1,groupitem2,...] [--headless] [--url <url>]');
        console.log('  Default groupitems: 年度,来源类别');
        console.log('  --headless: run without GUI (default: false, opens browser)');
        console.log('  --url: 知网入口 URL（默认 https://www.cnki.net/）');
        console.log('Examples:');
        console.log('  node cnki_filter_toggle.js');
        console.log('  node cnki_filter_toggle.js "年度,来源类别,学科"');
        console.log('  node cnki_filter_toggle.js "年度" --headless');
        console.log('  node cnki_filter_toggle.js --url "https://www.cnki.net/kns8s/"');
        process.exit(0);
      } else {
        groupitems = arg.split(',').map(s => s.trim()).filter(Boolean);
      }
    }

    console.log('========================================');
    console.log('  CNKI filter toggle (Playwright Node)');
    console.log('========================================');
    console.log(`Target groupitems: ${groupitems.join(', ')}`);
    console.log(`Mode: ${headless ? 'headless' : 'headed (browser will open)'}`);
    console.log('');

    console.log('-> Launching Chromium...');
    const context = await chromium.launchPersistentContext('./user-data', {
      headless: false,
      channel:"msedge",
      viewport: { width: 1440, height: 900 } 
    });
   
    const page = await context.newPage();

    console.log(`-> Navigating to CNKI: ${url}`);
    await page.goto(url, { waitUntil: 'domcontentloaded' });

    if (!headless) {
      console.log('');
      console.log('========================================');
      console.log('  ACTION REQUIRED');
      console.log('========================================');
      console.log('  1. 如果看到机构/SSO 登录页 → 用你所属机构账号登录');
      console.log('     (CARSI / Shibboleth / IdP 等统一认证流程按提示走)');
      console.log('  2. 登录完成后，做一次任意检索（如输入"cnn"）让左侧');
      console.log('     筛选分组展开');
      console.log('  3. 在 Playwright Inspector 里按 Resume 继续');
      console.log('========================================');
      console.log('');
      await page.pause();
    } else {
      console.log('-> Headless mode: assuming session is logged in (no manual pause).');
      console.log('-> Waiting 3s for page to settle...');
      await page.waitForTimeout(3000);
    }

    console.log(`-> Ensuring expanded: ${groupitems.join(', ')}`);
    try {
      const results = await ensureFiltersExpanded(page, groupitems, { verbose: true });
      console.log('');
      console.log('========================================');
      console.log('  RESULTS');
      console.log('========================================');
      for (const r of results) {
        const tag = r.wasFolded ? '[EXPANDED]' : '[ALREADY-EXPANDED]';
        console.log(`  ${tag} ${r.groupitem}: ${r.beforeDisplay} -> ${r.afterDisplay}`);
      }
      console.log('========================================');
      console.log('  All done.');
      console.log('========================================');
    } catch (err) {
      console.error('FAILED:', err.message);
      await page.screenshot({ path: 'cnki_filter_toggle_error.png', fullPage: true });
      console.error('Screenshot saved to: cnki_filter_toggle_error.png');
      process.exitCode = 1;
    } finally {
      // Don't auto-close in headed mode so user can inspect
      if (headless) {
        await browser.close();
      } else {
        console.log('-> Browser left open for inspection. Close it manually when done.');
      }
    }
  })().catch(err => {
    console.error('FATAL:', err);
    process.exit(1);
  });
}

module.exports = { ensureFilterExpanded, ensureFiltersExpanded };
