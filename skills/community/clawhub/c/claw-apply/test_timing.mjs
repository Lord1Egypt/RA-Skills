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

// Test 1: networkidle timing
const t0 = Date.now();
await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
const networkIdleMs = Date.now() - t0;
const btnAfterIdle = await page.$(SELECTOR);
console.log(`networkidle: ${networkIdleMs}ms — button present: ${!!btnAfterIdle}`);

// Test 2: reload with domcontentloaded + waitForSelector
await page.goto("about:blank");
const t1 = Date.now();
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
const domLoadedMs = Date.now() - t1;
const btnAfterDom = await page.$(SELECTOR);
console.log(`domcontentloaded: ${domLoadedMs}ms — button present: ${!!btnAfterDom}`);

// Now time how long waitForSelector takes from domcontentloaded
const t2 = Date.now();
const btn = await page.waitForSelector(SELECTOR, { timeout: 15000, state: "attached" }).catch(() => null);
const selectorMs = Date.now() - t2;
console.log(`waitForSelector after domcontentloaded: +${selectorMs}ms — found: ${!!btn}`);
console.log(`total domcontentloaded + waitForSelector: ${domLoadedMs + selectorMs}ms`);

// Test 3: reload with domcontentloaded + scroll + waitForSelector
await page.goto("about:blank");
const t3 = Date.now();
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.evaluate(() => window.scrollTo(0, 300));
const btn2 = await page.waitForSelector(SELECTOR, { timeout: 15000, state: "attached" }).catch(() => null);
const totalMs = Date.now() - t3;
console.log(`domcontentloaded + scroll + waitForSelector: ${totalMs}ms — found: ${!!btn2}`);

console.log("\nSummary:");
console.log(`  networkidle:     ${networkIdleMs}ms`);
console.log(`  domcontentloaded + selector: ${domLoadedMs + selectorMs}ms`);
console.log(`  domcontentloaded + scroll + selector: ${totalMs}ms`);

await browser.close();
process.exit(0);
