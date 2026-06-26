import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
import { FormFiller } from "./lib/form_filler.mjs";
const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const profile = loadConfig(resolve(__dir, "config/profile.json"));
const filler = new FormFiller(profile, []);

const applyUrl = "https://www.linkedin.com/jobs/view/4311307116/apply/?openSDUIApplyFlow=true";
const { browser, page } = await createBrowser(settings, "linkedin");
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
await new Promise(r => setTimeout(r, 4000));

const modal = await page.$('[role="dialog"]');
// Navigate to the problem step (step 4, progress=67)
for (let i = 0; i < 4; i++) {
  const nextBtn = await modal.$('button[aria-label*="Continue"], button[aria-label*="next"]');
  if (nextBtn) { await nextBtn.click(); await new Promise(r => setTimeout(r, 2000)); }
}

console.log("=== FIELDSETS ===");
const fieldsets = await modal.$$("fieldset");
console.log(`Found ${fieldsets.length} fieldsets`);
for (const fs of fieldsets) {
  const legend = await fs.$eval("legend", el => el.textContent?.trim()).catch(() => "NO LEGEND");
  const radios = await fs.$$('input[type="radio"]');
  const checkboxes = await fs.$$('input[type="checkbox"]');
  console.log(`  legend="${legend}" radios=${radios.length} checkboxes=${checkboxes.length}`);
}

console.log("\n=== CHECKBOXES (outside fieldsets) ===");
const allCbs = await modal.$$('input[type="checkbox"]');
console.log(`Found ${allCbs.length} checkboxes total`);
for (const cb of allCbs) {
  const visible = await cb.isVisible().catch(() => false);
  if (!visible) continue;
  const label = await filler.getLabel(cb);
  const checked = await cb.isChecked().catch(() => false);
  const required = await filler.isRequired(cb);
  console.log(`  label="${label}" checked=${checked} required=${required}`);
}

console.log("\n=== SELECTS ===");
const selects = await modal.$$("select");
for (const sel of selects) {
  const visible = await sel.isVisible().catch(() => false);
  if (!visible) continue;
  const label = await filler.getLabel(sel);
  const value = await sel.inputValue().catch(() => "");
  console.log(`  label="${label}" value="${value}"`);
}

console.log("\n=== VALIDATION ERRORS ===");
const errors = await modal.$$eval('[class*="error"], [role="alert"]', els => els.map(el => el.textContent?.trim()).filter(Boolean)).catch(() => []);
console.log(errors);

// Look for any element with "make a selection" text
const selectionText = await modal.evaluate(el => {
  const all = el.querySelectorAll('*');
  const matches = [];
  for (const node of all) {
    if (node.textContent?.includes('make a selection') && node.children.length === 0) {
      matches.push({ tag: node.tagName, class: node.className, parent: node.parentElement?.className });
    }
  }
  return matches;
}).catch(() => []);
console.log("\n=== 'make a selection' elements ===");
console.log(JSON.stringify(selectionText, null, 2));

await browser.close();
process.exit(0);
