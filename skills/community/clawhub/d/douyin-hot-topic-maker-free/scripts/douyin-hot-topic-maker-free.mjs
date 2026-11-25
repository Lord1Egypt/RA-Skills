#!/usr/bin/env node
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const BASE_URL = "http://127.0.0.1:17777";
const SESSION_PREFIX = "skill-factory-douyin-hot-topic-maker-free";
const FIXED_PLAN_COUNT = 5;
const BLOCKED = /验证码|安全验证|访问过于频繁|风险控制|请登录|权限不足/i;
const BANNED = /保证\s*(?:流量|转化|爆|收益|播放)|必\s*(?:爆|上热门)|绕过验证码|自动发布/i;
const HIGH_RISK = /人物|政策|医疗|金融|灾害|伤亡|引语|诉讼|股价|确诊|死亡|亿元|万[人例]/i;
const SENSITIVE_KEYS = /browserId|token|cookie|authorization|localStorage|session|login|phone/i;
const RISK_LEVELS = new Set(["low", "medium", "high"]);
const FACT_STATUSES = new Set(["page_visible_only", "needs_fact_review", "blocked"]);
const PUBLISHABILITY = new Set(["ready_for_human_review", "needs_fact_review", "blocked"]);

export function validateBridgeBase(value = process.env.SKILL_FACTORY_WEBBRIDGE_URL || process.env.EASY_WEBBRIDGE_URL || BASE_URL) {
  let url;
  try { url = new URL(value); } catch { throw new Error("Easy WebBridge address must be local loopback HTTP"); }
  const loopback = url.hostname === "127.0.0.1" || url.hostname === "[::1]" || url.hostname === "::1";
  if (url.protocol !== "http:" || !loopback || url.username || url.password
      || (url.pathname !== "" && url.pathname !== "/") || url.search || url.hash) {
    throw new Error("Easy WebBridge address must be credential-free loopback HTTP without a path");
  }
  return url.origin;
}

const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const now = () => new Date().toISOString();
const text = (value) => value == null ? null : String(value).trim() || null;
export const safeAlias = (value) => String(value || "").trim().replace(/[^a-zA-Z0-9_-]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
function fail(message, exitCode = 1) { const error = new Error(message); error.exitCode = exitCode; throw error; }
function safeError(value) { return String(value || "error").replace(/Bearer\s+[^\s]+/gi, "Bearer [redacted]").replace(/[A-Za-z0-9_-]{16,}/g, "[redacted]"); }
function runKey(alias, capturedAt, nonce = "") { return `run-${safeAlias(alias)}-${new Date(capturedAt).getTime().toString(36)}${nonce ? `-${nonce}` : ""}`; }
function sessionKey(runId) { return `${SESSION_PREFIX}-${runId}`; }
function cleanSuccess(output) { return Promise.all(["research-snapshot.json", "publishable-plan.json", "publishable-plan.md"].map((name) => rm(path.join(output, name), { force: true }))); }
async function diagnostic(output, reason, nextStep) { await mkdir(output, { recursive: true }); await cleanSuccess(output); await writeFile(path.join(output, "run-diagnostic.json"), json({ schemaVersion: "1.0", kind: "douyin-run-diagnostic", status: "needs_user_action", reason, nextStep, recordedAt: now() })); }

export function validateRequest(request, env = {}) {
  if (!request || request.runtime !== "easy-webbridge") fail("runtime must be easy-webbridge", 2);
  const explicit = text(request.browserId), configured = text(env.SKILL_FACTORY_WEBBRIDGE_BROWSER_ID);
  if (explicit && configured && explicit !== configured) fail("browserId conflicts with configured browser", 2);
  const profile = request.accountProfile || {}, accountAlias = safeAlias(request.accountAlias);
  if (!accountAlias || !text(profile.niche) || !text(profile.audience) || !Array.isArray(profile.contentPillars) || !profile.contentPillars.filter(text).length) fail("accountAlias, niche, audience, and contentPillars are required", 2);
  const keywords = request.keywords ?? [], searchLimitPerKeyword = request.searchLimitPerKeyword ?? 12;
  if (!Array.isArray(keywords) || keywords.length > 5 || keywords.some((item) => !text(item))) fail("keywords must contain 0-5 non-empty values", 2);
  if (request.planCount != null && request.planCount !== FIXED_PLAN_COUNT) fail("planCount is fixed at 5", 2);
  if (!Number.isInteger(searchLimitPerKeyword) || searchLimitPerKeyword < 1 || searchLimitPerKeyword > 20) fail("searchLimitPerKeyword must be an integer from 1 to 20", 2);
  return { ...request, browserId: explicit || configured || null, accountAlias, keywords: keywords.map(text), planCount: FIXED_PLAN_COUNT, searchLimitPerKeyword, accountProfile: { ...profile, contentPillars: profile.contentPillars.map(text).filter(Boolean), restrictedTopics: Array.isArray(profile.restrictedTopics) ? profile.restrictedTopics.map(text).filter(Boolean) : [], recentTopics: Array.isArray(profile.recentTopics) ? profile.recentTopics.map(text).filter(Boolean) : [] } };
}

export function selectBrowser(request, browsers) {
  const online = (Array.isArray(browsers) ? browsers : []).filter((item) => item?.online && text(item.browserId));
  if (request.browserId) {
    const selected = online.find((item) => item.browserId === request.browserId);
    if (!selected) fail("selected browser is not online", 1);
    return selected;
  }
  if (online.length === 1) return online[0];
  if (!online.length) fail("no online browser is available", 1);
  fail("multiple browsers are online; run list and set one browserId explicitly", 2);
}

function rawKey(item) { return text(item.workUrl) || text(item.contentId) || (text(item.title) || "").toLowerCase(); }
function toEvidence(item, sourceType, keyword) { return { sourceType, sourceUrl: text(item.sourceUrl) || (sourceType === "hot-page" ? "https://www.douyin.com/hot" : `https://www.douyin.com/jingxuan/search/${encodeURIComponent(keyword)}?type=general`), keyword: keyword || null, visibleLabel: text(item.visibleLabel), title: text(item.title), author: text(item.author), publishedText: text(item.publishedText), visibleMetricsText: Array.isArray(item.visibleMetricsText) ? item.visibleMetricsText.map(text).filter(Boolean) : [], workUrl: text(item.workUrl) }; }
export function normalizeSnapshot(request, hotPage, searches = [], capturedAt = now(), runNonce = "") {
  if (!hotPage || BLOCKED.test(`${hotPage?.pageText || ""} ${hotPage?.title || ""}`)) return { status: "needs_user_action", reason: "hot_page_blocked" };
  if (!Array.isArray(hotPage.items) || !hotPage.items.length) return { status: "needs_user_action", reason: "hot_page_evidence_unavailable" };
  const pages = [{ page: hotPage, type: "hot-page", keyword: null }];
  for (const search of searches) {
    if (!search || BLOCKED.test(`${search?.pageText || ""} ${search?.title || ""}`)) return { status: "needs_user_action", reason: "keyword_blocked" };
    if (text(search.keyword) !== text(search.requestedKeyword)) return { status: "needs_user_action", reason: "keyword_mismatch" };
    if (!Array.isArray(search.items) || !search.items.length) return { status: "needs_user_action", reason: "keyword_evidence_unavailable" };
    pages.push({ page: search, type: "keyword-search", keyword: search.requestedKeyword });
  }
  const candidates = new Map();
  for (const { page, type, keyword } of pages) for (const item of page.items) {
    const key = rawKey(item); if (!key) continue;
    if (!candidates.has(key)) candidates.set(key, { ...toEvidence(item, type, keyword), evidence: [] });
    candidates.get(key).evidence.push(toEvidence(item, type, keyword));
  }
  const runId = runKey(request.accountAlias, capturedAt, runNonce); let ordinal = 0;
  const sources = [...candidates.values()].map((candidate) => ({ sourceId: `${runId}-src-${String(++ordinal).padStart(3, "0")}`, ...candidate }));
  return { schemaVersion: "1.0", kind: "douyin-visible-topic-snapshot", status: "success", runId, accountAlias: request.accountAlias, accountProfile: { niche: request.accountProfile.niche, audience: request.accountProfile.audience, contentPillars: request.accountProfile.contentPillars, restrictedTopics: request.accountProfile.restrictedTopics, recentTopics: request.accountProfile.recentTopics }, accountBinding: { accountAlias: request.accountAlias, snapshotId: `${runId}-snapshot` }, capturedAt, timezone: "Asia/Shanghai", sourceScope: "selected-account-visible-web-snapshot", requestedPlanCount: request.planCount, sources, notices: ["只记录指定账号在采集时刻页面可见字段", "不是官方 API、统一热榜或历史趋势"] };
}

function editorialText(plan) { return [plan.topic, plan.title, plan.angle, plan.accountFit, plan.hook3s, ...((plan.outline || []).flatMap((item) => [item.section, item.purpose, ...(item.keyPoints || [])]))].map(text).filter(Boolean).join(" "); }
function assertNoSensitive(value, label = "draft") { if (!value || typeof value !== "object") return; for (const [key, child] of Object.entries(value)) { if (SENSITIVE_KEYS.test(key)) fail(`${label} contains sensitive field: ${key}`, 2); assertNoSensitive(child, label); } }
function markdown(value) { return String(value).replace(/([\\`*_{}\[\]()<>#+.!|-])/g, "\\$1"); }
export function validateDraft(snapshot, draft) {
  if (!snapshot || snapshot.schemaVersion !== "1.0" || snapshot.kind !== "douyin-visible-topic-snapshot" || snapshot.status !== "success" || !text(snapshot.runId) || !text(snapshot.accountAlias) || snapshot.accountBinding?.accountAlias !== snapshot.accountAlias || snapshot.accountBinding?.snapshotId !== `${snapshot.runId}-snapshot`) fail("snapshot schema or run binding is invalid", 2);
  if (!draft || draft.schemaVersion !== "1.0" || draft.kind !== "douyin-topic-plan-draft" || draft.status !== "draft") fail("draft schema, kind, or status is invalid", 2);
  assertNoSensitive(draft);
  if (draft.accountAlias !== snapshot.accountAlias || draft.sourceRunId !== snapshot.runId || draft.snapshotId !== snapshot.accountBinding?.snapshotId) fail("draft is not bound to this account snapshot", 2);
  if (!Array.isArray(draft.plans) || draft.plans.length !== FIXED_PLAN_COUNT) fail("draft must contain exactly 5 plans", 2);
  const sourceById = new Map(snapshot.sources.map((source) => [source.sourceId, source]));
  return draft.plans.map((plan, index) => {
    if (!plan || !text(plan.topic) || !text(plan.title) || !text(plan.angle) || !text(plan.accountFit) || !text(plan.hook3s)) fail(`plan ${index + 1} is missing required editorial fields`, 2);
    if (!Array.isArray(plan.sourceIds) || !plan.sourceIds.length || plan.sourceIds.some((id) => !sourceById.has(id))) fail(`plan ${index + 1} references a source outside this snapshot`, 2);
    if (!Array.isArray(plan.outline) || plan.outline.length !== 3) fail(`plan ${index + 1} outline must contain exactly 3 sections`, 2);
    const sections = plan.outline.filter((item) => text(item?.section) && text(item?.purpose) && Array.isArray(item?.keyPoints) && item.keyPoints.some(text)).map((item) => item.section);
    if (sections.join("|") !== "开场|核心展开|结尾行动") fail(`plan ${index + 1} outline needs ordered 开场、核心展开、结尾行动`, 2);
    const risk = plan.risk || {}; if (!RISK_LEVELS.has(risk.level) || !FACT_STATUSES.has(risk.factStatus) || !Array.isArray(risk.notes) || !risk.notes.some(text) || !PUBLISHABILITY.has(plan.publishability)) fail(`plan ${index + 1} has invalid risk or publishability`, 2);
    const combined = editorialText(plan); if (BANNED.test(combined)) fail(`plan ${index + 1} contains a prohibited promise`, 2);
    if (snapshot.accountProfile?.restrictedTopics?.some((topic) => combined.includes(topic)) || snapshot.accountProfile?.recentTopics?.some((topic) => plan.topic.includes(topic))) fail(`plan ${index + 1} conflicts with restricted or recent topics`, 2);
    if (HIGH_RISK.test(combined) && (risk.factStatus === "page_visible_only" || plan.publishability === "ready_for_human_review")) fail(`plan ${index + 1} contains high-risk claims and needs fact review`, 2);
    return { ...plan, rank: index + 1, sourceEvidence: plan.sourceIds.flatMap((id) => { const source = sourceById.get(id); return source.evidence.flatMap((evidence) => [evidence.title, evidence.author, evidence.publishedText, ...(evidence.visibleMetricsText || [])]).filter(Boolean).slice(0, 4); }) };
  });
}
export function renderPlan(snapshot, draft) {
  const plans = validateDraft(snapshot, draft);
  const sources = snapshot.sources.map(({ sourceId, sourceType, sourceUrl, keyword, title, author, publishedText, visibleMetricsText, workUrl }) => ({ sourceId, sourceType, sourceUrl, keyword, title, author, publishedText, visibleMetricsText, workUrl }));
  const finalPlan = { schemaVersion: "1.0", kind: "douyin-publishable-topic-plan", status: "ready_for_human_review", accountAlias: snapshot.accountAlias, generatedAt: now(), sourceCapturedAt: snapshot.capturedAt, sourceScope: snapshot.sourceScope, accountFitSummary: text(draft.accountFitSummary) || "按账号适配优先级排序，不是抖音热度排名。", sources, plans, globalChecks: ["人工复核标题、事实、合规和账号语气后再发布"], limitations: ["仅依据当前可见页面，不代表全网热榜", "不保证爆款，不执行自动发布"] };
  const lines = ["# 免费抖音热点选题助手", `- 账号安全别名：${markdown(snapshot.accountAlias)}`, `- 生成时间：${finalPlan.generatedAt}`, `- 来源采集时间：${snapshot.capturedAt}`, `- 来源范围：指定浏览器当前可见页面`, "", "## 本次可见来源", ...sources.map((source) => `- ${markdown(source.sourceId)}：${markdown(source.title || source.keyword || "抖音页面信号")}｜${markdown(source.workUrl || source.sourceUrl)}`), "", "## 本轮账号匹配", markdown(finalPlan.accountFitSummary)];
  for (const plan of plans) lines.push("", `## ${plan.rank}. ${markdown(plan.topic)}`, `- 标题：${markdown(plan.title)}`, `- 3 秒钩子：${markdown(plan.hook3s)}`, `- 切入角度：${markdown(plan.angle)}`, `- 账号适配：${markdown(plan.accountFit)}`, `- 三段提纲：${plan.outline.map((item) => `${markdown(item.section)}（${markdown(item.purpose)}：${item.keyPoints.map(markdown).join("、")}）`).join("；")}`, `- 来源引用：${plan.sourceIds.map((id) => { const source = snapshot.sources.find((item) => item.sourceId === id); return `${markdown(id)} ${markdown(source.workUrl || source.sourceUrl)}`; }).join("；")}`, `- 复核状态：${plan.risk.level} / ${plan.risk.factStatus}；${plan.risk.notes.map(markdown).join("；")}`);
  lines.push("", "## 全局限制", "仅为指定账号当前可见网页快照，不是官方排名，不保证流量；人工确认事实、合规和账号语气后再发布。");
  return { finalPlan, markdown: `${lines.join("\n")}\n` };
}

async function token() { const file = process.env.SKILL_FACTORY_WEBBRIDGE_TOKEN_FILE || process.env.EASY_WEBBRIDGE_TOKEN_FILE || path.join(os.homedir(), ".easy-webbridge", "bridge-token"); try { const value = (await readFile(file, "utf8")).trim(); if (!value) fail("Easy WebBridge Token 文件为空", 2); return value; } catch (error) { if (error.exitCode) throw error; fail("找不到 Easy WebBridge Token 文件", 2); } }
async function api(endpoint, init = {}) { try { const base = validateBridgeBase(); const auth = await token(); const response = await fetch(`${base}${endpoint}`, { ...init, redirect: "error", headers: { "Content-Type": "application/json", Authorization: `Bearer ${auth}`, ...(init.headers || {}) } }); if (!response.ok) fail(`Easy WebBridge request failed (${response.status}); check selected browser and local authorization`, 1); return await response.json(); } catch (error) { if (error.exitCode) throw error; fail("Easy WebBridge is unavailable; start the local bridge and retry", 1); } }
export function bridgeCommandPayload(action, args, session) { return { action, args: { ...args, session }, timeoutMs: 20000 }; }
async function command(browserId, action, args, session) { return (await api(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: "POST", body: JSON.stringify(bridgeCommandPayload(action, args, session)) })).result; }
export const HOT_EXTRACT = `(() => {
  const visible = (node) => {
    const rect = node.getBoundingClientRect();
    const style = getComputedStyle(node);
    return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden" && !node.closest("[hidden],[inert]");
  };
  const cards = [...document.querySelectorAll('a[href*="/video/"], a[href*="/note/"]')].filter(visible).slice(0, 30);
  return {
    url: location.href,
    pageText: document.body.innerText.slice(0, 12000),
    pageType: /\\/hot(?:[/?#]|$)/.test(location.pathname),
    visible: cards.length > 0,
    items: cards.map((anchor) => {
      const container = anchor.closest("div");
      const visibleText = container?.innerText || anchor.innerText || "";
      return {
        title: anchor.innerText.trim() || null,
        workUrl: new URL(anchor.href, location.href).href,
        visibleLabel: visibleText.match(/上升热点|热点/)?.[0] || null,
        visibleMetricsText: visibleText.match(/\\d+(?:\\.\\d+)?[万亿]?人在看/g) || [],
      };
    }).filter((item) => item.title),
  };
})()`;
export const SEARCH_EXTRACT = `(() => {
  const input = document.querySelector('[data-e2e="searchbar-input"]');
  const visible = (node) => {
    const rect = node.getBoundingClientRect();
    const style = getComputedStyle(node);
    return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden" && !node.closest("[hidden],[inert]");
  };
  const cards = [...document.querySelectorAll(".search-result-card")].filter(visible);
  return {
    url: location.href,
    pageText: document.body.innerText.slice(0, 12000),
    pageType: /\\/(?:jingxuan\\/)?search(?:[/?#]|$)/.test(location.pathname),
    visible: cards.length > 0,
    keyword: input?.value.trim() || "",
    items: cards.map((card) => {
      const lines = card.innerText.split(/\\n+/).map((line) => line.trim()).filter(Boolean);
      return {
        title: lines[0] || null,
        author: lines.find((line) => line.startsWith("@"))?.slice(1) || null,
        publishedText: lines.find((line) => line.startsWith("·"))?.replace(/^·\\s*/, "") || null,
        visibleMetricsText: lines.filter((line) => /赞|评论|收藏/.test(line)).slice(0, 2),
        workUrl: card.querySelector('a[href*="/video/"], a[href*="/note/"]')?.href || null,
      };
    }),
  };
})()`;
async function waitAndExtract(browserId, session, url, code, keyword, limit) { const tab = await command(browserId, "navigate", { url, newTab: keyword == null, groupTitle: "抖音热点选题" }, session); const tabId = tab.tabId || tab.id; if (!tabId) fail("Bridge navigation did not return a task tab", 1); await new Promise((resolve) => setTimeout(resolve, 2500)); for (let attempt = 0; attempt < 6; attempt++) { const page = await command(browserId, "evaluate", { tabId, code }, session); const actualUrl = text(page?.url) ? new URL(page.url) : null; const pathname = actualUrl?.pathname || ""; const expectedPath = keyword == null ? /^\/hot(?:\/|$)/.test(pathname) : /^\/(?:jingxuan\/)?search(?:\/|$)/.test(pathname); if (actualUrl?.protocol === "https:" && actualUrl.hostname === "www.douyin.com" && expectedPath && page.pageType === true && page.visible === true && !BLOCKED.test(page.pageText || "") && (page.items || []).length) return { ...page, requestedKeyword: keyword, items: page.items.slice(0, limit) }; if (attempt < 5) { if (attempt >= 2) await command(browserId, "evaluate", { tabId, code: "window.scrollBy(0, Math.max(600, window.innerHeight)); true" }, session); await new Promise((resolve) => setTimeout(resolve, 500)); } }
  return { pageText: "", keyword: null, requestedKeyword: keyword, items: [] };
}
async function collect(request, output) {
  await mkdir(output, { recursive: true }); await cleanSuccess(output); const session = sessionKey(runKey(request.accountAlias, now(), Math.random().toString(36).slice(2, 8))); let navigated = false;
  let selectedBrowserId = null;
  try {
    const browserList = await api("/v1/browsers");
    selectedBrowserId = selectBrowser(request, browserList.browsers || []).browserId;
    navigated = true;
    const hot = await waitAndExtract(selectedBrowserId, session, "https://www.douyin.com/hot", HOT_EXTRACT, null, 30);
    const searches = []; for (const keyword of request.keywords) searches.push(await waitAndExtract(selectedBrowserId, session, `https://www.douyin.com/jingxuan/search/${encodeURIComponent(keyword)}?type=general`, SEARCH_EXTRACT, keyword, request.searchLimitPerKeyword));
    const snapshot = normalizeSnapshot(request, hot, searches); if (snapshot.status !== "success") { await diagnostic(output, snapshot.reason, "在指定浏览器中人工处理登录、验证或页面加载后重试。"); fail("Douyin needs user action; diagnostic written", 1); }
    await writeFile(path.join(output, "research-snapshot.json"), json(snapshot)); await rm(path.join(output, "run-diagnostic.json"), { force: true }); return snapshot;
  } catch (error) { if (!String(error.message).includes("diagnostic written")) await diagnostic(output, "collection_failed", "检查本机 Easy WebBridge、精确选择的浏览器和页面状态后重试。"); throw error; }
  finally { if (navigated && selectedBrowserId && !request.keepTab) try { await command(selectedBrowserId, "close_session", {}, session); } catch {} }
}
function parseArgs(argv) { const [verb = "help", ...rest] = argv, options = {}; for (let index = 0; index < rest.length; index++) { if (!rest[index].startsWith("--")) fail(`unexpected argument: ${rest[index]}`, 2); const key = rest[index].slice(2).replaceAll("-", "_"); if (key === "keep_tab") { options.keepTab = true; continue; } if (!rest[index + 1]) fail(`missing value for --${key}`, 2); options[key] = rest[++index]; } return { verb, options }; }
function usage() { console.log("Usage:\n  node scripts/douyin-hot-topic-maker-free.mjs list\n  node scripts/douyin-hot-topic-maker-free.mjs collect --request ./request.json --output ./output/account-alias\n  node scripts/douyin-hot-topic-maker-free.mjs validate-plan --snapshot ./output/account-alias/research-snapshot.json --draft ./output/account-alias/plan-draft.json --output ./output/account-alias\n  node scripts/douyin-hot-topic-maker-free.mjs help"); }
async function main() {
  const { verb, options } = parseArgs(process.argv.slice(2));
  if (verb === "help") return usage();
  if (verb === "list") {
    const browsers = (await api("/v1/browsers")).browsers || [];
    console.log(JSON.stringify({ browsers: browsers.filter((item) => item.online).map((item) => ({ displayName: item.displayName, browserId: item.browserId, browser: item.browser })) }));
    return;
  }
  if (verb === "collect") {
    if (!options.request || !options.output) fail("collect needs --request and --output", 2);
    await mkdir(options.output, { recursive: true });
    const request = validateRequest(JSON.parse(await readFile(options.request, "utf8")), process.env);
    const snapshot = await collect({ ...request, keepTab: options.keepTab || request.keepTab }, options.output);
    console.log(JSON.stringify({ status: "success", sourceCount: snapshot.sources.length, output: options.output }));
    return;
  }
  if (verb === "validate-plan") {
    if (!options.snapshot || !options.draft || !options.output) fail("validate-plan needs --snapshot, --draft and --output", 2);
    await mkdir(options.output, { recursive: true });
    try {
      const snapshot = JSON.parse(await readFile(options.snapshot, "utf8"));
      const draft = JSON.parse(await readFile(options.draft, "utf8"));
      const { finalPlan, markdown: rendered } = renderPlan(snapshot, draft);
      await writeFile(path.join(options.output, "publishable-plan.json"), json(finalPlan));
      await writeFile(path.join(options.output, "publishable-plan.md"), rendered);
      console.log(JSON.stringify({ status: "ready_for_human_review", planCount: finalPlan.plans.length, output: options.output }));
    } catch (error) {
      await diagnostic(options.output, "plan_validation_failed", "修正同账号快照引用、风险状态和必填字段后重试。");
      throw error;
    }
    return;
  }
  fail("unknown command", 2);
}
if (import.meta.url === `file://${process.argv[1]}`) main().catch((error) => { console.error(safeError(error.message)); process.exit(error.exitCode || 1); });
