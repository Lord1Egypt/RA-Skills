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
const apiKey = process.env.ANTHROPIC_API_KEY;

const jobUrl = "https://www.linkedin.com/jobs/view/4363271952";
const applyUrl = jobUrl + "/apply/?openSDUIApplyFlow=true";

function ms(start) { return ((Date.now() - start) / 1000).toFixed(1) + "s"; }
const t0 = Date.now();

const { browser, page } = await createBrowser(settings, "linkedin");
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
const modal = await page.waitForSelector(LINKEDIN_EASY_APPLY_MODAL_SELECTOR, { timeout: 10000 }).catch(() => null);
if (!modal) { console.log("No modal"); await browser.close(); process.exit(1); }

const filler = new FormFiller(profile, answers, { apiKey, answersPath, jobContext: { title: "Test", company: "Test" } });

// Snapshot and log what we see
let t = Date.now();
const snap = await filler._snapshotFields(modal);
console.log("Snapshot took " + ms(t));
console.log("Resume radios:", snap.resumeRadios.length, "checked:", snap.resumeChecked);
console.log("Inputs:", snap.inputs.length);
for (const f of snap.inputs) console.log("  ", JSON.stringify(f));
console.log("Textareas:", snap.textareas.length);
for (const f of snap.textareas) console.log("  ", JSON.stringify(f));
console.log("Fieldsets:", snap.fieldsets.length);
for (const f of snap.fieldsets) console.log("  ", JSON.stringify(f));
console.log("Selects:", snap.selects.length);
for (const f of snap.selects) console.log("  ", JSON.stringify(f));
console.log("Checkboxes:", snap.checkboxes.length);
for (const f of snap.checkboxes) console.log("  ", JSON.stringify(f));

console.log("\nTOTAL: " + ms(t0));
await browser.close();
process.exit(0);
