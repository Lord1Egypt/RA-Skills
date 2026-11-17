#!/usr/bin/env node
import fs from "node:fs";

const evalPath = process.argv[2] || "evals/trigger_eval.json";
const skillText = fs.readFileSync("SKILL.md", "utf8");
const evalSpec = JSON.parse(fs.readFileSync(evalPath, "utf8"));
const description = extractDescription(skillText).toLowerCase();

const requiredDescriptionTerms = [
  "road trip",
  "interactive html",
  "fixed",
  "limited stamina",
  "priority-ranked",
  "calendar"
];

const missingDescriptionTerms = requiredDescriptionTerms.filter(term => !description.includes(term));
const failures = [];

if (missingDescriptionTerms.length) {
  failures.push(`SKILL.md description is missing route terms: ${missingDescriptionTerms.join(", ")}`);
}

for (const testCase of evalSpec.cases || []) {
  const actual = shouldTrigger(testCase.prompt);
  if (actual !== testCase.shouldTrigger) {
    failures.push(`${testCase.id}: expected ${testCase.shouldTrigger}, got ${actual} (${testCase.reason})`);
  }
}

if (failures.length) {
  for (const failure of failures) console.error(`FAIL ${failure}`);
  console.error(`FAILED trigger eval: ${failures.length} failure(s)`);
  process.exit(1);
}

console.log(`PASS trigger eval: ${(evalSpec.cases || []).length} case(s)`);

function extractDescription(text) {
  const match = text.match(/^description:\s*(.+)$/m);
  return match ? match[1] : "";
}

function shouldTrigger(prompt) {
  const text = prompt.toLowerCase();
  const explicitSkill = text.includes("$comfortable-roadtrip-planner") || text.includes("comfortable-roadtrip-planner");
  const selfDrive = /(road\s*trip|self[-\s]*drive|driving route|自驾|开车|自驾路线|路书|路线|行程)/i.test(text);
  const artifact = /(html|map|地图|route app|calendar|日历|ics|导航)/i.test(text);
  const comfort = /(fixed hotel|hotels are fixed|酒店.*固定|酒店已经订|订好了|孕妇|pregnan|low[-\s]*stamina|limited stamina|老人|小孩|体力|comfort|舒适|不开夜路|少走路|少绕路|a\/b\/c|必留|看状态|可删)/i.test(text);
  const routeTradeoff = /(a\/b\/c|必留|看状态|可删|skip|keep).*(少走路|少绕路|体力|worth|optional|景点|stop)/i.test(text);
  const exclusions = /(flight|机票|translate|翻译|history|历史|city walk|walking|只走路|不自驾|不用行程|不需要行程|订酒店|要比价|hotel booking)/i.test(text);
  const strongPositive = explicitSkill || routeTradeoff || (selfDrive && (artifact || comfort));
  if (exclusions && !explicitSkill && !(selfDrive && comfort && !/flight|机票|translate|翻译/i.test(text))) return false;
  return Boolean(strongPositive);
}
