#!/usr/bin/env node

// capture-fallback.mjs — Standalone Playwright capture script
// Used when Playwright MCP is NOT connected. Produces the same data shape
// as the MCP-based capture path so downstream analysis steps don't care
// which was used.
//
// Usage:
//   node capture-fallback.mjs --url https://linear.app --domain linear.app [--output ./] [--crawl] [--compare https://stripe.com]
//
// Prerequisites:
//   npx playwright install chromium    (one-time, ~100MB)
//
// The script:
//   1. Launches headless Chromium with fresh context (no cookies/state)
//   2. Resizes viewport to 1440×900
//   3. Navigates to URL, waits for hydration (3s + 3s if skeleton)
//   4. Takes viewport + full-page JPEG screenshots
//   5. Injects extract-dom.js via page.evaluate()
//   6. Performs hover interactions on nav links + buttons
//   7. Captures transition/transform deltas from hover states
//   8. Outputs JSON data file + screenshots to output dir
//   9. If --crawl: visits 2 additional same-domain pages from nav links
//  10. If --compare: repeats entire capture for second URL

import { chromium } from "playwright";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve, dirname, join } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// --- Parse CLI args ---
const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  if (idx === -1) return null;
  return args[idx + 1] || null;
}
function hasFlag(name) {
  return args.includes(`--${name}`);
}

const primaryUrl = getArg("url");
const domain = getArg("domain");
const outputDir = getArg("output") || ".";
const doCrawl = hasFlag("crawl");
const compareUrl = getArg("compare");

if (!primaryUrl || !domain) {
  console.error("Usage: node capture-fallback.mjs --url <url> --domain <domain> [--output <dir>] [--crawl] [--compare <url2>]");
  process.exit(1);
}

// --- Load the DOM extractor script ---
const extractScript = readFileSync(join(__dirname, "extract-dom.js"), "utf-8");

// --- Ensure output directory exists ---
if (!existsSync(outputDir)) {
  mkdirSync(outputDir, { recursive: true });
}

// --- Core capture function for a single URL ---
async function capturePage(browser, url, filePrefix) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    ignoreHTTPSErrors: true,
    // Fresh context — no cookies/login state leaking in
  });

  const page = await context.newPage();
  const result = {
    captureMethod: "fallback",
    screenshots: {},
    domData: null,
    hoverDeltas: [],
    error: null,
  };

  try {
    // Navigate
    console.log(`  Navigating to ${url}...`);
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });

    // Wait for hydration (3s)
    await page.waitForTimeout(3000);

    // Check if still skeleton-looking (heuristic: very few text nodes visible)
    const textNodeCount = await page.evaluate(() => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let count = 0;
      while (walker.nextNode()) {
        if (walker.currentNode.textContent.trim().length > 10) count++;
        if (count > 20) return count;
      }
      return count;
    });

    if (textNodeCount < 5) {
      console.log("  Page looks sparse, waiting another 3s for hydration...");
      await page.waitForTimeout(3000);
      result.hydrationWarning = true;
    }

    // Check for error states
    const pageState = await page.evaluate(() => {
      const body = document.body?.textContent || "";
      const hasPasswordField = !!document.querySelector('input[type="password"]');
      const looksLikeCloudflare = body.includes("Verify you are human") || body.includes("Just a moment");
      return { hasPasswordField, looksLikeCloudflare, bodyLength: body.length };
    });

    if (pageState.hasPasswordField) {
      result.error = "LOGIN_PAGE: URL resolves to a login page (password field detected). Use the public marketing page instead.";
      await context.close();
      return result;
    }

    if (pageState.looksLikeCloudflare && pageState.bodyLength < 500) {
      result.error = "CLOUDFLARE_BLOCK: Bot detection/verification page detected. Try a different page on the same domain.";
      await context.close();
      return result;
    }

    // Screenshots
    console.log("  Taking viewport screenshot...");
    const vpPath = resolve(outputDir, `${filePrefix}-viewport.jpeg`);
    await page.screenshot({ path: vpPath, type: "jpeg", quality: 85 });
    result.screenshots.viewport = vpPath;

    console.log("  Taking full-page screenshot...");
    const fpPath = resolve(outputDir, `${filePrefix}-fullpage.jpeg`);
    await page.screenshot({ path: fpPath, type: "jpeg", quality: 75, fullPage: true });
    result.screenshots.fullPage = fpPath;

    // DOM extraction
    console.log("  Running DOM extractor...");
    result.domData = await page.evaluate(`(${extractScript})()`);

    // Hover interaction capture — nav links
    console.log("  Capturing hover interactions...");
    const hoverTargets = await page.evaluate(() => {
      const targets = [];
      // Nav links
      const navLinks = document.querySelectorAll("nav a, header a");
      for (const el of [...navLinks].slice(0, 2)) {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) {
          targets.push({
            type: "nav-link",
            x: Math.round(r.x + r.width / 2),
            y: Math.round(r.y + r.height / 2),
            selector: el.tagName.toLowerCase() + (el.className ? "." + el.className.trim().split(/\s+/)[0] : ""),
          });
        }
      }
      // Buttons
      const btns = document.querySelectorAll('button, a[class*="btn"], a[class*="button"], [role="button"]');
      for (const el of [...btns].slice(0, 2)) {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && r.height > 0 && r.top < window.innerHeight) {
          targets.push({
            type: "button",
            x: Math.round(r.x + r.width / 2),
            y: Math.round(r.y + r.height / 2),
            selector: el.tagName.toLowerCase() + (el.className ? "." + el.className.trim().split(/\s+/)[0] : ""),
          });
        }
      }
      return targets;
    });

    for (const target of hoverTargets) {
      try {
        // Capture before-hover state
        const before = await page.evaluate(({ x, y }) => {
          const el = document.elementFromPoint(x, y);
          if (!el) return null;
          const s = getComputedStyle(el);
          return {
            backgroundColor: s.backgroundColor,
            color: s.color,
            transform: s.transform,
            boxShadow: s.boxShadow,
            opacity: s.opacity,
            borderColor: s.borderColor,
          };
        }, target);

        // Hover
        await page.mouse.move(target.x, target.y);
        await page.waitForTimeout(400); // Wait for transition

        // Capture after-hover state
        const after = await page.evaluate(({ x, y }) => {
          const el = document.elementFromPoint(x, y);
          if (!el) return null;
          const s = getComputedStyle(el);
          return {
            backgroundColor: s.backgroundColor,
            color: s.color,
            transform: s.transform,
            boxShadow: s.boxShadow,
            opacity: s.opacity,
            borderColor: s.borderColor,
          };
        }, target);

        if (before && after) {
          // Record only properties that actually changed
          for (const prop of Object.keys(before)) {
            if (before[prop] !== after[prop]) {
              result.hoverDeltas.push({
                element: `${target.type} (${target.selector})`,
                property: prop,
                from: before[prop],
                to: after[prop],
              });
            }
          }
        }

        // Move mouse away to reset hover state
        await page.mouse.move(0, 0);
        await page.waitForTimeout(200);
      } catch {
        // Hover capture is best-effort, don't fail the whole pipeline
      }
    }

  } catch (e) {
    result.error = `CAPTURE_ERROR: ${e.message}`;
  }

  await context.close();
  return result;
}

// --- Main ---
async function main() {
  console.log(`\n🎨 Capture Fallback — Design Extraction`);
  console.log(`   Primary URL: ${primaryUrl}`);
  console.log(`   Domain: ${domain}`);
  console.log(`   Crawl: ${doCrawl ? "multi-page" : "single page"}`);
  if (compareUrl) console.log(`   Compare URL: ${compareUrl}`);
  console.log();

  const browser = await chromium.launch({ headless: true });

  try {
    // --- Primary URL capture ---
    console.log(`[1/1] Capturing primary page...`);
    const primary = await capturePage(browser, primaryUrl, domain);

    if (primary.error) {
      console.error(`\n❌ ${primary.error}`);
      process.exit(1);
    }

    const allPages = [{ url: primaryUrl, data: primary }];

    // --- Multi-page crawl ---
    if (doCrawl && primary.domData?.navLinks?.length > 0) {
      // Pick 2 additional pages: prefer shorter paths, distinct sections
      const candidates = primary.domData.navLinks
        .filter(l => l.href && l.text)
        .sort((a, b) => new URL(a.href).pathname.length - new URL(b.href).pathname.length)
        .slice(0, 2);

      for (let i = 0; i < candidates.length; i++) {
        const link = candidates[i];
        console.log(`\n[Crawl ${i + 1}/${candidates.length}] Capturing ${link.href}...`);
        const crawled = await capturePage(browser, link.href, `${domain}-page${i + 2}`);
        if (!crawled.error) {
          allPages.push({ url: link.href, data: crawled });
        } else {
          console.warn(`  ⚠ Skipping ${link.href}: ${crawled.error}`);
        }
      }
    }

    // --- Merge multi-page data: tag system vs local signals ---
    const mergedData = primary.domData;
    if (allPages.length > 1) {
      // Track which color/radius/shadow values appear on multiple pages
      const colorSets = allPages.map(p => new Set(
        (p.data.domData?.colors?.backgroundColors || []).map(c => c.value)
      ));
      const radiusSets = allPages.map(p => new Set(
        (p.data.domData?.effects?.radii || []).map(r => r.value)
      ));

      // Mark system signals (appear on 2+ pages)
      if (mergedData.colors?.backgroundColors) {
        for (const c of mergedData.colors.backgroundColors) {
          const appearsOnPages = colorSets.filter(s => s.has(c.value)).length;
          c.signal = appearsOnPages >= 2 ? "system" : "local";
        }
      }
    }

    // --- Comparative mode ---
    let compareData = null;
    if (compareUrl) {
      const compareDomain = new URL(compareUrl).hostname.replace(/^www\./, "");
      console.log(`\n[Compare] Capturing ${compareUrl}...`);
      const compared = await capturePage(browser, compareUrl, compareDomain);
      if (compared.error) {
        console.warn(`  ⚠ Compare URL error: ${compared.error}`);
      } else {
        compareData = {
          url: compareUrl,
          domain: compareDomain,
          data: compared,
        };
      }
    }

    // --- Write output ---
    const output = {
      primary: {
        url: primaryUrl,
        domain,
        domData: mergedData,
        hoverDeltas: primary.hoverDeltas,
        screenshots: primary.screenshots,
        pagesAnalyzed: allPages.map(p => p.url),
        captureMethod: "fallback",
        hydrationWarning: primary.hydrationWarning || false,
      },
    };

    if (compareData) {
      output.compare = {
        url: compareData.url,
        domain: compareData.domain,
        domData: compareData.data.domData,
        hoverDeltas: compareData.data.hoverDeltas,
        screenshots: compareData.data.screenshots,
        captureMethod: "fallback",
      };
    }

    const outputPath = resolve(outputDir, `${domain}-capture.json`);
    writeFileSync(outputPath, JSON.stringify(output, null, 2));
    console.log(`\n✅ Capture complete!`);
    console.log(`   Data: ${outputPath}`);
    console.log(`   Screenshots: ${Object.values(primary.screenshots).join(", ")}`);
    if (compareData) {
      console.log(`   Compare screenshots: ${Object.values(compareData.data.screenshots).join(", ")}`);
    }

  } finally {
    await browser.close();
  }
}

main().catch((e) => {
  console.error(`\n❌ Fatal error: ${e.message}`);
  process.exit(1);
});
