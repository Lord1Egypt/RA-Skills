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
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 25000 });
await page.evaluate(() => window.scrollTo(0, 300));
await new Promise(r => setTimeout(r, 6000));
console.log("Final URL:", page.url());

// Our selector
const eaBtn = await page.$('[aria-label*="Easy Apply"], [aria-label*="Continue applying"]');
console.log("Our selector match:", eaBtn ? "YES" : "NO");

// All apply-related buttons
const btns = await page.evaluate(() => {
  return Array.from(document.querySelectorAll("button, a")).map(b => ({
    tag: b.tagName,
    text: (b.innerText || "").trim().slice(0, 80),
    aria: b.getAttribute("aria-label") || "",
    href: b.href || "",
  })).filter(b => {
    const t = (b.text + " " + b.aria).toLowerCase();
    return t.includes("apply") || t.includes("easy") || t.includes("continue");
  });
});
console.log("\nApply-related elements:", btns.length);
for (const b of btns) console.log(" ", JSON.stringify(b));

// Page state
const info = await page.evaluate(() => ({
  h1: document.querySelector("h1")?.textContent?.trim()?.slice(0, 100) || "",
  closed: document.body.innerText.toLowerCase().includes("no longer accepting"),
  loginWall: document.body.innerText.toLowerCase().includes("sign in"),
}));
console.log("\nH1:", info.h1);
console.log("Closed:", info.closed);
console.log("Login wall:", info.loginWall);

await browser.close();
process.exit(0);
