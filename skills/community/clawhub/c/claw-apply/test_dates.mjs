import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { existsSync } from "fs";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
import { FormFiller } from "./lib/form_filler.mjs";
import { LINKEDIN_EASY_APPLY_MODAL_SELECTOR } from "./lib/constants.mjs";

const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const profile = loadConfig(resolve(__dir, "config/profile.json"));
const answersPath = resolve(__dir, "config/answers.json");
const answers = existsSync(answersPath) ? loadConfig(answersPath) : [];
const filler = new FormFiller(profile, answers, {});
const { browser, page } = await createBrowser(settings, "linkedin");
const MODAL = LINKEDIN_EASY_APPLY_MODAL_SELECTOR;

await page.goto("https://www.linkedin.com/jobs/view/4377448382/apply/?openSDUIApplyFlow=true", { waitUntil: "domcontentloaded", timeout: 25000 });
await page.waitForSelector(MODAL, { timeout: 10000 });

// Navigate to step 5 (the date step)
for (let i = 0; i < 4; i++) {
  // Cancel sub-forms first
  const btns = await page.$$(`${MODAL} button:not([disabled])`);
  for (const b of btns) {
    const t = await b.evaluate(el => (el.innerText||"").trim()).catch(()=>"");
    if (t === "Cancel") { await b.click(); await new Promise(r => setTimeout(r, 1500)); break; }
  }
  const next = await page.$(`${MODAL} button[aria-label="Continue to next step"]:not([disabled])`);
  if (next) { await next.click(); await new Promise(r => setTimeout(r, 2000)); }
}

// Cancel any date pickers/sub-forms on step 5
const cancelBtns = await page.$$(`${MODAL} button:not([disabled])`);
for (const b of cancelBtns) {
  const t = await b.evaluate(el => (el.innerText||"").trim()).catch(()=>"");
  if (t === "Cancel") { await b.click(); await new Promise(r => setTimeout(r, 1000)); }
}

console.log("=== STEP 5 SNAPSHOT ===");
const modal = await page.$(MODAL);
const snap = await filler._snapshotFields(modal);
console.log("Inputs:");
for (const f of snap.inputs) console.log("  ", JSON.stringify(f));
console.log("Textareas:");
for (const f of snap.textareas) console.log("  ", JSON.stringify(f));
console.log("Fieldsets:");
for (const f of snap.fieldsets) console.log("  ", JSON.stringify({legend: f.legend, options: f.options, isCheckboxGroup: f.isCheckboxGroup}));
console.log("Selects:");
for (const f of snap.selects) console.log("  ", JSON.stringify({label: f.label, value: f.value, options: f.options.slice(0,5)}));

await browser.close();
process.exit(0);
