#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const rules = [
  { code: "absolute", pattern: /(百分百|绝对|保证|永久|永远|零风险|稳赚|必赚|保证成交|无条件退款)/g, replacement: "尽量", message: "绝对化或结果承诺" },
  { code: "counterfeit", pattern: /(高仿|精仿|复刻版|A货|盗版|破解版|免授权)/gi, replacement: "待确认版本", message: "仿冒、盗版或未授权风险" },
  { code: "bypass", pattern: /(绕过审核|防封|不会封号|规避风控|跳过验证)/g, replacement: "按平台规则使用", message: "规避规则或安全校验" },
  { code: "off_platform", pattern: /(加微信|加V|私下交易|支付宝转账|银行卡转账)/gi, replacement: "通过平台沟通和交易", message: "站外交易引导" },
];

function clean(value) { return String(value ?? "").replace(/\s+/g, " ").trim(); }
function multiline(value) { return String(value ?? "").replace(/\r\n/g, "\n").replace(/[ \t]+/g, " ").replace(/\n{3,}/g, "\n\n").trim(); }
function arg(name) { const index = process.argv.indexOf(name); return index < 0 ? "" : process.argv[index + 1] || ""; }
function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }

function check(text) {
  const findings = [];
  for (const rule of rules) {
    rule.pattern.lastIndex = 0;
    const matches = Array.from(String(text).matchAll(rule.pattern), (match) => match[0]);
    if (matches.length) findings.push({ code: rule.code, message: rule.message, matches: [...new Set(matches)], suggestion: rule.replacement });
  }
  return findings;
}

function safeText(text) {
  let value = String(text || "");
  for (const rule of rules) { rule.pattern.lastIndex = 0; value = value.replace(rule.pattern, rule.replacement); }
  return clean(value);
}

function createCopy(input) {
  const product = input.product || {};
  const name = clean(product.name || product.title);
  const facts = [...new Set((Array.isArray(product.facts) ? product.facts : []).map(clean).filter(Boolean))];
  const condition = clean(product.condition); const price = clean(product.price); const audience = clean(product.audience);
  const missingFacts = [];
  if (!name) missingFacts.push("商品名称");
  if (facts.length < 2) missingFacts.push(`真实事实至少 2 条（当前 ${facts.length} 条）`);
  if (missingFacts.length) return { status: "needs_user_input", missingFacts, titleVariants: [], description: "", sellingPoints: [], searchTerms: [], flaggedPhrases: [], disclaimers: [], nextAction: "补齐最少事实后重新运行" };
  const count = Math.max(3, Math.min(Number(input.variants) || 3, 5));
  const safeName = safeText(name); const safeFacts = facts.map(safeText);
  const candidates = [
    [safeName, condition, safeFacts[0]], [safeName, safeFacts[0], safeFacts[1]],
    [safeName, audience ? `适合${audience}` : safeFacts[1], condition], [condition, safeName, safeFacts[0]],
    [safeName, ...safeFacts.slice(0, 2)],
  ].map((parts) => clean(parts.filter(Boolean).join(" ")).slice(0, 60));
  const titleVariants = [...new Set(candidates)].slice(0, count).map((title) => ({ title, factsUsed: [safeName, ...safeFacts].filter((fact) => title.includes(fact)) }));
  const descriptionLines = [safeName, condition ? `成色：${safeText(condition)}` : "成色：待确认", ...safeFacts.map((fact) => `- ${fact}`), price ? `价格：${price}` : "价格：待补", "瑕疵、配件和交付方式请按实际情况补充，下单前可在平台内确认。"];
  const rawText = `${name}\n${facts.join("\n")}\n${product.description || ""}`;
  return { status: "completed", titleVariants, description: multiline(descriptionLines.join("\n")), sellingPoints: safeFacts, searchTerms: [...new Set([safeName, ...safeFacts.flatMap((fact) => fact.split(/[ /｜|]/))])].filter(Boolean).slice(0, 10), missingFacts: [!condition ? "成色" : "", !price ? "价格" : ""].filter(Boolean), flaggedPhrases: check(rawText), disclaimers: ["只使用输入中的真实事实，未知信息保留待确认"], nextAction: "人工核对成色、瑕疵、配件和价格后进入草稿" };
}

function selfTest() {
  const result = createCopy({ product: { name: "机械键盘", facts: ["87键", "有线"], condition: "九成新", price: "128" }, variants: 3 });
  if (result.status !== "completed" || result.titleVariants.length !== 3 || !result.description.includes("87键")) throw new Error("文案生成自测失败");
  if (!check("保证成交，零风险").length) throw new Error("风险词检查自测失败");
  if (createCopy({ product: { name: "键盘", facts: [] } }).status !== "needs_user_input") throw new Error("缺失事实自测失败");
  return { ok: true, tests: 3 };
}

async function main() {
  if (process.argv.includes("--self-test")) return print(selfTest());
  const inputPath = arg("--input"); if (!inputPath) throw new Error("用法：node scripts/run.mjs --input input.json [--output result.json]");
  const result = createCopy(JSON.parse(await readFile(resolve(inputPath), "utf8")));
  const output = arg("--output"); if (output) await writeFile(resolve(output), `${JSON.stringify(result, null, 2)}\n`);
  print(result);
}

main().catch((error) => { print({ ok: false, error: error.message }); process.exitCode = 1; });
