import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const jobUrl = process.argv[2] || "https://www.linkedin.com/jobs/view/4377417471/";
const applyUrl = jobUrl.replace(/\/$/, "") + "/apply/?openSDUIApplyFlow=true";
console.log("Job URL:", jobUrl);
console.log("Apply URL:", applyUrl);

const { browser, page } = await createBrowser(settings, "linkedin");

// Navigate directly to apply URL
const t0 = Date.now();
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
const navMs = Date.now() - t0;
console.log(`Navigation: ${navMs}ms`);
console.log("Final URL:", page.url());

// Wait for modal
await new Promise(r => setTimeout(r, 3000));
const modal = await page.$('[role="dialog"]');
console.log("Modal found:", !!modal);

if (modal) {
  const info = await modal.evaluate(el => ({
    text: (el.innerText || "").slice(0, 300),
    hasForm: !!el.querySelector("form, input, select, textarea, fieldset"),
    hasProgress: !!el.querySelector("progress, [role='progressbar']"),
  }));
  console.log("Has form:", info.hasForm);
  console.log("Has progress:", info.hasProgress);
  console.log("Modal text:", info.text.slice(0, 200));

  // Check buttons
  const buttons = await modal.$$("button:not([disabled])");
  for (const btn of buttons) {
    const bInfo = await btn.evaluate(el => ({
      text: (el.innerText || "").trim().slice(0, 50),
      aria: el.getAttribute("aria-label") || "",
    }));
    if (bInfo.text || bInfo.aria) console.log("  Button:", JSON.stringify(bInfo));
  }
}

// Also grab meta from the page
const meta = await page.evaluate(() => ({
  title: document.querySelector(".job-details-jobs-unified-top-card__job-title, h1")?.textContent?.trim(),
  company: document.querySelector(".job-details-jobs-unified-top-card__company-name a")?.textContent?.trim(),
}));
console.log("\nMeta:", JSON.stringify(meta));

await browser.close();
process.exit(0);
