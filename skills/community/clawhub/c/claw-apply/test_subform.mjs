import { loadEnv } from "./lib/env.mjs";
loadEnv();
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { existsSync } from "fs";
import { createBrowser } from "./lib/browser.mjs";
import { loadConfig } from "./lib/queue.mjs";
import { FormFiller } from "./lib/form_filler.mjs";
import { apply } from "./lib/apply/easy_apply.mjs";

const __dir = dirname(fileURLToPath(import.meta.url));
const settings = loadConfig(resolve(__dir, "config/settings.json"));
const profile = loadConfig(resolve(__dir, "config/profile.json"));
const answersPath = resolve(__dir, "config/answers.json");
const answers = existsSync(answersPath) ? loadConfig(answersPath) : [];
const apiKey = process.env.ANTHROPIC_API_KEY;

const { browser, page } = await createBrowser(settings, "linkedin");
const formFiller = new FormFiller(profile, answers, { apiKey, answersPath, jobContext: { title: "Founding Sales", company: "Cynet" } });

const job = { url: "https://www.linkedin.com/jobs/view/4377448382", title: "Founding Sales Executive", company: "Cynet Systems" };

console.log("Testing easy_apply flow...");
const t = Date.now();
const result = await apply(page, job, formFiller);
console.log("\nResult:", JSON.stringify(result, null, 2));
console.log("Time:", ((Date.now() - t) / 1000).toFixed(1) + "s");

await browser.close();
process.exit(0);
