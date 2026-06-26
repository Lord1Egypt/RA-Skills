import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
import { FormFiller } from "./lib/form_filler.mjs";
import { LINKEDIN_EASY_APPLY_MODAL_SELECTOR } from "./lib/constants.mjs";

const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const profile = loadConfig(resolve(__dir, "config/profile.json"));
const answersPath = resolve(__dir, "data/answers.json");
const answers = loadConfig(answersPath);
const apiKey = process.env.ANTHROPIC_API_KEY;

const jobUrl = process.argv[2];
if (!jobUrl) { console.log("Usage: node test_apply.mjs <linkedin-job-url>"); process.exit(1); }
const applyUrl = jobUrl.replace(/\/$/, "") + "/apply/?openSDUIApplyFlow=true";
const DRY_RUN = !process.argv.includes("--submit");

console.log("Job:", jobUrl);
console.log("Mode:", DRY_RUN ? "DRY RUN (add --submit to actually submit)" : "LIVE SUBMIT");

const { browser, page } = await createBrowser(settings, "linkedin");
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
await new Promise(r => setTimeout(r, 4000));

const modal = await page.$(LINKEDIN_EASY_APPLY_MODAL_SELECTOR);
if (!modal) { console.log("No modal found"); await browser.close(); process.exit(1); }

const filler = new FormFiller(profile, answers, { apiKey, answersPath, jobContext: { title: "Test", company: "Test" } });

const MAX_STEPS = 15;
for (let step = 0; step < MAX_STEPS; step++) {
  // Get step info
  const progress = await modal.$eval("progress, [role='progressbar']", el => el.value || el.getAttribute("aria-valuenow") || "").catch(() => "");
  const heading = await modal.$eval("h2, h3", el => el.textContent?.trim()).catch(() => "");

  // Check for Review or Submit
  const buttons = await modal.$$("button:not([disabled])");
  const btnInfos = [];
  for (const btn of buttons) {
    const info = await btn.evaluate(el => ({
      text: (el.innerText || "").trim(),
      aria: el.getAttribute("aria-label") || "",
    })).catch(() => ({ text: "", aria: "" }));
    if (info.text || info.aria) btnInfos.push(info);
  }

  const hasSubmit = btnInfos.some(b => b.text.includes("Submit") || b.aria.includes("Submit"));
  const hasReview = btnInfos.some(b => b.text === "Review" || b.aria.includes("Review"));
  const hasNext = btnInfos.some(b => b.text === "Next" || b.aria.includes("Continue to next"));

  console.log(`\n[step ${step}] progress=${progress} heading="${heading}"`);

  // Check errors from previous step
  const errors = await modal.$$eval('[class*="error"]:not([class*="error-icon"]), [role="alert"]',
    els => els.map(el => el.textContent?.trim()).filter(t => t && t.length > 3)
  ).catch(() => []);
  if (errors.length > 0) {
    console.log(`  ❌ ERRORS: ${JSON.stringify(errors)}`);
  }

  if (hasSubmit && !hasNext && !hasReview) {
    console.log("  ✅ REACHED SUBMIT PAGE");
    if (!DRY_RUN) {
      console.log("  Clicking Submit...");
      // find and click submit
    } else {
      console.log("  (dry run — not submitting)");
    }
    break;
  }

  if (hasReview && !hasNext) {
    console.log("  📋 REACHED REVIEW PAGE");
    // In dry run, this is success
    if (DRY_RUN) {
      console.log("  ✅ SUCCESS — form is complete, ready to submit");
      break;
    }
  }

  // Fill form
  console.log("  Filling form...");
  const unknowns = await filler.fill(page, profile.resume_path);
  if (unknowns.length > 0) {
    console.log(`  ⚠️  Unknowns: ${JSON.stringify(unknowns)}`);
  }

  // Dump form state after fill
  const fieldsets = await modal.$$("fieldset");
  for (const fs of fieldsets) {
    const leg = await fs.$eval("legend", el => el.textContent?.trim().slice(0, 80)).catch(() => "");
    if (!leg) continue;
    const checked = await fs.$("input:checked");
    const isCheckbox = (await fs.$$('input[type="checkbox"]')).length > 0;
    console.log(`  fieldset: "${leg}" type=${isCheckbox ? "checkbox" : "radio"} checked=${!!checked}`);
    if (!checked) {
      const labels = await fs.$$("label");
      for (const lbl of labels) {
        const t = (await lbl.textContent().catch(() => "") || "").trim();
        if (t) console.log(`    option: "${t}"`);
      }
    }
  }

  const selects = await modal.$$("select");
  for (const sel of selects) {
    if (!await sel.isVisible().catch(() => false)) continue;
    const lbl = await filler.getLabel(sel);
    const val = await sel.inputValue().catch(() => "");
    if (/^select/i.test(val)) console.log(`  select UNFILLED: "${lbl}" value="${val}"`);
  }

  const checkboxes = await modal.$$('input[type="checkbox"]');
  for (const cb of checkboxes) {
    if (!await cb.isVisible().catch(() => false)) continue;
    const lbl = await filler.getLabel(cb);
    const checked = await cb.isChecked().catch(() => false);
    if (!checked) console.log(`  checkbox UNCHECKED: "${lbl}"`);
  }

  // Click next/review
  if (hasNext) {
    console.log("  → clicking Next");
    const nextBtn = buttons.find((_, i) => btnInfos[i]?.aria?.includes("Continue to next") || btnInfos[i]?.text === "Next");
    if (nextBtn) await nextBtn.click();
  } else if (hasReview) {
    console.log("  → clicking Review");
    const revBtn = buttons.find((_, i) => btnInfos[i]?.aria?.includes("Review") || btnInfos[i]?.text === "Review");
    if (revBtn) await revBtn.click();
  } else {
    console.log("  ⚠️  No navigation button found");
    break;
  }

  await new Promise(r => setTimeout(r, 2500));
}

await browser.close();
process.exit(0);
