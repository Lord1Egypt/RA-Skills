#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";

const bridgeUrl = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777";
const dianqunhelpExtensionId = process.env.DIANQUNHELP_EXTENSION_ID || "oapgddmgefblpkmalflpkolkmbfhegaj";

function clean(value) { return String(value ?? "").replace(/\s+/g, " ").trim(); }
function arg(name) { const index = process.argv.indexOf(name); return index < 0 ? "" : process.argv[index + 1] || ""; }
function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }
async function token() { if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN; return (await readFile(join(homedir(), ".easy-webbridge", "bridge-token"), "utf8")).trim(); }
async function request(path, init = {}) { const response = await fetch(`${bridgeUrl}${path}`, { ...init, headers: { Authorization: `Bearer ${await token()}`, "Content-Type": "application/json", ...(init.headers || {}) } }); const body = await response.json().catch(() => ({})); if (!response.ok) throw new Error(body.error || `Easy WebBridge HTTP ${response.status}`); return body; }
async function command(browserId, action, args = {}, timeoutMs = 30000) { return request(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: "POST", body: JSON.stringify({ action, args, timeoutMs }) }); }
async function extensionCommand(browserId, accountAlias, action, options = {}, timeoutMs = 30000) {
  const response = await command(browserId, "extension_message", { extensionId: dianqunhelpExtensionId, message: { type: "DHH_EXTERNAL_COMMAND", browserId, accountAlias, action, ...options } }, timeoutMs);
  if (!response.result?.ok) throw new Error(response.result?.error || "店群助手执行失败");
  return response.result.result;
}

function summarize(products) {
  const prices = products.map((item) => Number(item.price || 0)).filter((value) => value > 0).sort((a, b) => a - b);
  const middle = prices.length ? (prices[Math.floor((prices.length - 1) / 2)] + prices[Math.ceil((prices.length - 1) / 2)]) / 2 : 0;
  const words = new Map();
  for (const item of products) for (const word of clean(`${item.title} ${item.description || ""}`).split(/[\s，。！？、｜|【】（）()]+/).filter((word) => word.length >= 2 && word.length <= 12)) words.set(word, (words.get(word) || 0) + 1);
  return { sampleSize: products.length, priceSummary: { min: prices[0] || 0, max: prices.at(-1) || 0, median: middle }, commonSellingPoints: [...words.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([text, count]) => ({ text, count })) };
}

function toCSV(products) {
  const fields = ["title", "url", "visiblePrice", "condition", "brand", "seller", "collectedAt", "missingFields"];
  const quote = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
  return [fields.join(","), ...products.map((item) => fields.map((field) => quote(Array.isArray(item[field]) ? item[field].join("|") : item[field])).join(","))].join("\n") + "\n";
}

function selfTest() {
  const result = summarize([{ title: "机械键盘 87键", price: 100 }, { title: "机械键盘 有线", price: 200 }, { title: "机械键盘", price: 300 }]);
  if (result.sampleSize !== 3 || result.priceSummary.median !== 200) throw new Error("价格汇总自测失败");
  if (!toCSV([{ title: 'A"B', missingFields: [] }]).includes('"A""B"')) throw new Error("CSV 转义自测失败");
  return { ok: true, tests: 2 };
}

async function run(input, outputDir) {
  const browserId = clean(input.browserId); const accountAlias = clean(input.accountAlias); const keyword = clean(input.keyword);
  const limit = Math.max(1, Math.min(Number(input.limit) || 10, 30));
  if (!browserId || !accountAlias || !keyword) throw new Error("browserId、accountAlias 和 keyword 必填");
  const browsers = (await request("/v1/browsers")).browsers || [];
  if (!browsers.some((browser) => browser.browserId === browserId && browser.online)) throw new Error(`browserId 不在线：${browserId}`);
  const session = `xianyu-competitor-${Date.now()}`;
  const navigation = await command(browserId, "navigate", { url: `https://www.goofish.com/search?q=${encodeURIComponent(keyword)}`, newTab: true, active: false, session, groupTitle: "闲鱼竞品采集" });
  const tabId = navigation.result.tabId;
  try {
    await new Promise((resolveWait) => setTimeout(resolveWait, 1800));
    const health = await extensionCommand(browserId, accountAlias, "health", {}, 12000);
    if (health.store?.browserId !== browserId || health.store?.alias !== accountAlias) throw new Error("店群助手绑定的店铺与本次任务不一致");
    const collected = await extensionCommand(browserId, accountAlias, "collect", { tabId, payload: { limit } }, 30000);
    // products 是历史商品库；竞品报告只使用本轮采集返回的真实样本。
    // 缺少当前样本契约时明确失败，不能把旧库或未知结果包装成采集成功。
    if (!Array.isArray(collected?.collectedProducts)) throw new Error("店群助手未返回本次采样 collectedProducts 数组，无法确认当前搜索样本");
    const rows = collected.collectedProducts;
    const products = rows.map((item) => {
      const missingFields = ["condition", "brand", "sellerName"].filter((field) => !clean(item[field]));
      return { title: clean(item.title), url: clean(item.sourceUrl), visiblePrice: Number(item.price || 0), condition: clean(item.condition), brand: clean(item.brand), specs: [], accessories: [], sellingPoints: [], visibleEngagement: "", seller: clean(item.sellerName), collectedAt: item.collectedAt || new Date().toISOString(), missingFields };
    });
    const summary = summarize(products.map((item) => ({ ...item, price: item.visiblePrice })));
    const report = { schemaVersion: 1, status: products.length ? "completed" : "partial", browserId, accountAlias, keyword, sourceUrl: `https://www.goofish.com/search?q=${encodeURIComponent(keyword)}`, ...summary, products, observations: ["价格和卖点仅代表本次页面可见样本"], limitations: products.some((item) => item.missingFields.length) ? ["部分字段未在搜索页显示，已保留为空"] : [], finishedAt: new Date().toISOString() };
    await mkdir(outputDir, { recursive: true });
    await Promise.all([
      writeFile(join(outputDir, "competitors.json"), `${JSON.stringify(report, null, 2)}\n`),
      writeFile(join(outputDir, "competitors.csv"), toCSV(products)),
      writeFile(join(outputDir, "competitors.md"), `# ${keyword} 竞品采样\n\n店铺环境：${accountAlias}（${browserId}）\n\n样本：${summary.sampleSize} 条；价格范围：${summary.priceSummary.min}-${summary.priceSummary.max}；中位价：${summary.priceSummary.median}。\n\n${products.map((item, index) => `${index + 1}. [${item.title}](${item.url}) - ${item.visiblePrice || "价格未显示"}`).join("\n")}\n`),
    ]);
    return { ok: true, status: report.status, outputDir, sampleSize: products.length };
  } finally {
    await command(browserId, "close_session", { session }).catch(() => {});
  }
}

async function main() {
  if (process.argv.includes("--self-test")) return print(selfTest());
  const inputPath = resolve(arg("--input")); const outputDir = resolve(arg("--output") || join(dirname(inputPath), "competitor-output"));
  if (!arg("--input")) throw new Error("用法：node scripts/run.mjs --input input.json [--output output-dir]");
  return print(await run(JSON.parse(await readFile(inputPath, "utf8")), outputDir));
}

main().catch((error) => { print({ ok: false, error: error.message }); process.exitCode = 1; });
