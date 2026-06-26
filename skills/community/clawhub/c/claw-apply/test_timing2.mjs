import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const url = process.argv[2] || "https://www.linkedin.com/jobs/view/4377417471/";
console.log("Testing:", url);
const { browser, page } = await createBrowser(settings, "linkedin");

const SELECTOR = '[aria-label*="Easy Apply"], [aria-label*="Continue applying"]';

// Run 3 attempts
for (let i = 1; i <= 3; i++) {
  await page.goto("about:blank");
  await new Promise(r => setTimeout(r, 1000));

  const t0 = Date.now();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 25000 });
  const domMs = Date.now() - t0;

  // Immediately check
  const immediate = await page.$(SELECTOR);
  const immMs = Date.now() - t0;

  // Scroll then check
  await page.evaluate(() => window.scrollTo(0, 300));

  // waitForSelector
  const t1 = Date.now();
  const btn = await page.waitForSelector(SELECTOR, { timeout: 15000, state: "attached" }).catch(() => null);
  const waitMs = Date.now() - t1;
  const totalMs = Date.now() - t0;

  console.log(`Run ${i}: dom=${domMs}ms immediate=${!!immediate}(${immMs}ms) waitForSelector=${waitMs}ms found=${!!btn} total=${totalMs}ms`);
}

await browser.close();
process.exit(0);
