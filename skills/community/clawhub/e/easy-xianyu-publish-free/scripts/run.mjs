#!/usr/bin/env node
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";

const bridgeUrl = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777";
const dianqunhelpExtensionId = process.env.DIANQUNHELP_EXTENSION_ID || "oapgddmgefblpkmalflpkolkmbfhegaj";
const highRisk = /(百分百|绝对|保证|永久|永远|零风险|稳赚|必赚|高仿|精仿|复刻版|A货|盗版|破解版|绕过审核|防封|不会封号|规避风控|跳过验证)/gi;
function clean(value) { return String(value ?? "").replace(/\s+/g, " ").trim(); }
function arg(name) { const index = process.argv.indexOf(name); return index < 0 ? "" : process.argv[index + 1] || ""; }
function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }
async function token() { if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN; return (await readFile(join(homedir(), ".easy-webbridge", "bridge-token"), "utf8")).trim(); }
async function request(path, init = {}) { const response = await fetch(`${bridgeUrl}${path}`, { ...init, headers: { Authorization: `Bearer ${await token()}`, "Content-Type": "application/json", ...(init.headers || {}) } }); const body = await response.json().catch(() => ({})); if (!response.ok) throw new Error(body.error || `Easy WebBridge HTTP ${response.status}`); return body; }
async function command(browserId, action, args = {}, timeoutMs = 30000) { return request(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: "POST", body: JSON.stringify({ action, args, timeoutMs }) }); }
async function extensionCommand(browserId, accountAlias, action, options = {}, timeoutMs = 30000) { const response = await command(browserId, "extension_message", { extensionId: dianqunhelpExtensionId, message: { type: "DHH_EXTERNAL_COMMAND", browserId, accountAlias, action, ...options } }, timeoutMs); if (!response.result?.ok) throw new Error(response.result?.error || "店群助手执行失败"); return response.result.result; }
async function readJsonIfExists(path, fallback) { try { return JSON.parse(await readFile(path, "utf8")); } catch (error) { if (error.code === "ENOENT") return fallback; throw error; } }
async function writeJsonAtomic(path, value) { await mkdir(dirname(path), { recursive: true }); const temporary = `${path}.${process.pid}.${Date.now()}.tmp`; await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 }); await rename(temporary, path); }

function inspect(input) {
  const product = input.product || input;
  const images = Array.isArray(product.images) ? product.images : [];
  const errors = []; const warnings = [];
  // 原创商品必须使用自身本地身份和真实交付清单，来源商品仍要求平台 ID。
  if (product.sourceType === "original") {
    if (!clean(product.localId)) errors.push("原创商品缺少本地身份");
    // 定制交付以明确范围登记，成品必须具备实际交付文件；两类商品不能互相冒充。
    if (product.fulfillmentMode === "custom-service") {
      if (!clean(product.serviceScope)) errors.push("定制服务缺少明确交付范围");
    } else if (!Array.isArray(product.deliveryFiles) || !product.deliveryFiles.length) errors.push("原创商品缺少真实交付文件清单");
  } else if (!clean(product.itemId)) errors.push("缺少来源商品 ID");
  if (!clean(product.title)) errors.push("缺少标题"); else if (clean(product.title).length > 60) errors.push("标题超过 60 字");
  if (!clean(product.description)) errors.push("缺少描述");
  if (!(Number(product.price) > 0)) errors.push("价格必须大于 0");
  if (!images.length) errors.push("至少需要一张商品图片");
  images.forEach((image, index) => { const url = clean(typeof image === "string" ? image : image.url); if (!/^https:\/\//.test(url)) errors.push(`第 ${index + 1} 张图片必须是可访问的 HTTPS 地址`); const width = Number(image?.width || 0); const height = Number(image?.height || 0); if (width && height && Math.min(width, height) < 300) errors.push(`第 ${index + 1} 张图片短边小于 300px`); if (!width || !height) warnings.push(`第 ${index + 1} 张图片尺寸未知`); });
  highRisk.lastIndex = 0; const risks = [...`${product.title || ""}\n${product.description || ""}`.matchAll(highRisk)].map((match) => match[0]);
  if (risks.length) errors.push(`包含高风险词：${[...new Set(risks)].join("、")}`);
  return { ok: !errors.length, errors, warnings, product: { ...product, title: clean(product.title), description: String(product.description || "").trim(), price: Number(product.price), images } };
}

function selfTest() {
  const valid = inspect({ itemId: "1", title: "机械键盘", description: "九成新，有线", price: 99, images: [{ url: "https://img.example/a.jpg", width: 800, height: 800 }] });
  if (!valid.ok) throw new Error("合法草稿自测失败");
  if (inspect({ title: "保证成交", description: "零风险", price: 0, images: [] }).ok) throw new Error("风险阻断自测失败");
  const service = { sourceType: "original", localId: "service-self-test", fulfillmentMode: "custom-service", serviceScope: "一个已确认功能", title: "插件定制", description: "确认需求后开发", price: 88, images: [{ url: "https://img.example/service.png", width: 1080, height: 1080 }] };
  if (!inspect(service).ok) throw new Error("定制服务范围自测失败");
  if (inspect({ ...service, serviceScope: "" }).ok) throw new Error("缺失服务范围未阻止");
  if (inspect({ ...service, fulfillmentMode: "standard" }).ok) throw new Error("成品文件门禁被绕过");
  return { ok: true, tests: 5 };
}

async function run(input, outputPath, confirmed) {
  const browserId = clean(input.browserId); const accountAlias = clean(input.accountAlias); const mode = input.mode || "draft-only";
  if (!browserId || !accountAlias) throw new Error("browserId 和 accountAlias 必填");
  if (!["draft-only", "confirm-before-publish"].includes(mode)) throw new Error("mode 只能是 draft-only 或 confirm-before-publish");
  const checked = inspect(input.product || {});
  const base = { browserId, accountAlias, intentId: clean(input.intentId), checkedAt: new Date().toISOString(), filledFields: ["title", "description", "price", "images"].filter((field) => checked.product[field]?.length || checked.product[field] > 0), missingFields: checked.errors, imageCount: checked.product.images.length, warnings: checked.warnings, errors: checked.errors };
  if (!checked.ok) return { ...base, status: "failed", nextAction: "修正草稿后重新运行" };
  if (mode === "draft-only") return { ...base, status: "draft_ready", product: checked.product, nextAction: "核对草稿后改用 confirm-before-publish 并提供 --confirm" };
  if (!confirmed) return { ...base, status: "needs_user_action", product: checked.product, nextAction: "确认目标店铺和商品后重新运行并加 --confirm" };
  if (!base.intentId) throw new Error("真实上架必须提供唯一 intentId");
  const journalPath = `${outputPath}.intents.json`;
  const journal = await readJsonIfExists(journalPath, { intents: {} });
  if (journal.intents[base.intentId]) throw new Error(`intentId 已执行或结果不确定：${base.intentId}`);
  const browsers = (await request("/v1/browsers")).browsers || [];
  if (!browsers.some((browser) => browser.browserId === browserId && browser.online)) throw new Error(`browserId 不在线：${browserId}`);
  const session = `xianyu-publish-${Date.now()}`; let keepSession = false;
  const navigation = await command(browserId, "navigate", { url: "https://www.goofish.com/", newTab: true, active: false, session, groupTitle: "闲鱼上架" });
  try {
    await new Promise((resolveWait) => setTimeout(resolveWait, 1200));
    const health = await extensionCommand(browserId, accountAlias, "health", {}, 12000);
    if (health.store?.browserId !== browserId || health.store?.alias !== accountAlias) throw new Error("店群助手绑定的店铺与本次任务不一致");
    journal.intents[base.intentId] = { status: "running", browserId, accountAlias, at: new Date().toISOString() };
    await writeJsonAtomic(journalPath, journal);
    const result = await extensionCommand(browserId, accountAlias, "publish", { tabId: navigation.result.tabId, payload: { product: checked.product }, authorized: true, idempotencyKey: base.intentId }, 120000);
    // 保留平台异常状态，不能把受理后状态异常覆盖成成功或丢失商品ID。
    const status = ["published", "uncertain", "needs_user_action"].includes(result.status) ? result.status : "uncertain";
    keepSession = status === "needs_user_action";
    journal.intents[base.intentId] = { ...journal.intents[base.intentId], status, result, finishedAt: new Date().toISOString() };
    await writeJsonAtomic(journalPath, journal);
    return { ...base, status, result, sourceUrl: result.itemUrl || "", nextAction: status === "published" ? "已回读商品状态与标题；持续在售另行核对" : "核对已取得ID对应的商品状态，禁止重复发布" };
  } catch (error) {
    const uncertain = /超时|timeout|网络|连接|未响应/i.test(error.message);
    const needsUser = /登录|验证|安全校验|实名/i.test(error.message);
    keepSession = needsUser;
    journal.intents[base.intentId] = { ...(journal.intents[base.intentId] || {}), status: uncertain ? "uncertain" : needsUser ? "needs_user_action" : "failed", error: error.message, finishedAt: new Date().toISOString() };
    await writeJsonAtomic(journalPath, journal);
    return { ...base, status: journal.intents[base.intentId].status, errors: [error.message], nextAction: uncertain ? "人工回读，禁止自动重试" : needsUser ? "在保留页面中处理登录或验证" : "修正后使用新的 intentId" };
  } finally {
    if (!keepSession) await command(browserId, "close_session", { session }).catch(() => {});
  }
}

async function main() {
  if (process.argv.includes("--self-test")) return print(selfTest());
  const inputPath = arg("--input"); if (!inputPath) throw new Error("用法：node scripts/run.mjs --input input.json --output result.json [--confirm]");
  const outputPath = resolve(arg("--output") || join(dirname(resolve(inputPath)), "publish-result.json"));
  const result = await run(JSON.parse(await readFile(resolve(inputPath), "utf8")), outputPath, process.argv.includes("--confirm"));
  await writeJsonAtomic(outputPath, result); print(result);
}

main().catch((error) => { print({ ok: false, error: error.message }); process.exitCode = 1; });
