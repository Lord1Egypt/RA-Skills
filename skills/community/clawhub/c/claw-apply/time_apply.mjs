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

const jobId = "4363271952";
const jobUrl = "https://www.linkedin.com/jobs/view/" + jobId;
const applyUrl = jobUrl + "/apply/?openSDUIApplyFlow=true";

function ms(start) { return ((Date.now() - start) / 1000).toFixed(1) + "s"; }

const t0 = Date.now();
console.log("=== TIMED APPLY TEST (DRY RUN) ===");

let t = Date.now();
console.log("[browser] Creating...");
const { browser, page } = await createBrowser(settings, "linkedin");
console.log("[browser] " + ms(t));

t = Date.now();
await page.goto(applyUrl, { waitUntil: "domcontentloaded", timeout: 25000 });
console.log("[navigate] " + ms(t));

t = Date.now();
const modal = await page.waitForSelector(LINKEDIN_EASY_APPLY_MODAL_SELECTOR, { timeout: 10000 }).catch(() => null);
console.log("[modal wait] " + ms(t) + " found=" + !!modal);

if (!modal) { console.log("TOTAL: " + ms(t0)); await browser.close(); process.exit(1); }

const filler = new FormFiller(profile, answers, { apiKey, answersPath, jobContext: { title: "Test", company: "Test" } });

for (let step = 0; step < 12; step++) {
  const ss = Date.now();

  t = Date.now();
  const m = await page.$(LINKEDIN_EASY_APPLY_MODAL_SELECTOR);
  if (!m) { console.log("[step " + step + "] modal gone - submitted"); break; }
  const btns = await m.$$("button:not([disabled])");
  const bi = [];
  for (const b of btns) {
    const info = await b.evaluate(el => ({ t: (el.innerText||"").trim().slice(0,30), a: el.getAttribute("aria-label")||"" })).catch(()=>({}));
    if (info.t || info.a) bi.push(info);
  }
  const btnMs = ms(t);

  const hasSubmit = bi.some(b => (b.a||"").includes("Submit"));
  const hasReview = bi.some(b => b.t === "Review" || (b.a||"").includes("Review"));
  const hasNext = bi.some(b => b.t === "Next" || (b.a||"").includes("Continue to next"));

  if (hasSubmit && !hasNext && !hasReview) {
    console.log("[step " + step + "] SUBMIT PAGE (dry run, not clicking) btns=" + btnMs + " step=" + ms(ss));
    break;
  }

  t = Date.now();
  const unknowns = await filler.fill(page, profile.resume_path);
  const fillMs = ms(t);

  t = Date.now();
  if (hasNext) {
    const nb = btns.find((_,i) => (bi[i]?.a||"").includes("Continue to next") || bi[i]?.t === "Next");
    if (nb) await nb.click();
  } else if (hasReview) {
    const rb = btns.find((_,i) => (bi[i]?.a||"").includes("Review") || bi[i]?.t === "Review");
    if (rb) await rb.click();
  } else {
    console.log("[step " + step + "] NO NAV"); break;
  }
  await new Promise(r => setTimeout(r, 1500));
  const clickMs = ms(t);

  console.log("[step " + step + "] btns=" + btnMs + " fill=" + fillMs + " click+wait=" + clickMs + " total=" + ms(ss) + (unknowns.length ? " unknowns=" + unknowns.length : ""));
}

console.log("\nTOTAL: " + ms(t0));
await browser.close();
process.exit(0);
