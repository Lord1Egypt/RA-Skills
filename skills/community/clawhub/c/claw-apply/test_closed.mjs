import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));

// Yuki - confirmed "No longer accepting applications"
const closedUrl = "https://www.linkedin.com/jobs/view/4381968189/";
const applyUrl = closedUrl.replace(/\/$/, "") + "/apply/?openSDUIApplyFlow=true";

console.log("Testing closed job:");
console.log("  Apply URL:", applyUrl);

const { browser, page } = await createBrowser(settings, "linkedin");
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
await new Promise(r => setTimeout(r, 4000));

console.log("Final URL:", page.url());

// Check for modal
const modal = await page.$('[role="dialog"]');
console.log("Modal found:", !!modal);
if (modal) {
  const text = await modal.evaluate(el => (el.innerText || "").slice(0, 300));
  console.log("Modal text:", text);
}

// Check page for closed indicators
const pageCheck = await page.evaluate(() => {
  const text = (document.body.innerText || "").toLowerCase();
  return {
    noLongerAccepting: text.includes("no longer accepting"),
    noLongerAvailable: text.includes("no longer available"),
    expired: text.includes("this job has expired"),
    closed: text.includes("job is closed"),
    snippet: document.body.innerText.slice(0, 400),
  };
});
console.log("\nClosed checks:", JSON.stringify(pageCheck, null, 2));

await browser.close();
process.exit(0);
