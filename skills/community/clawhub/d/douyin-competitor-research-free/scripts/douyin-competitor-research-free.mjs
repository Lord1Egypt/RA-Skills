#!/usr/bin/env node
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const BASE_URL = "http://127.0.0.1:17777";
const SESSION_PREFIX = "douyin-competitor-research-free";
const BLOCKED = /登录|验证码|安全验证|风控|风险控制|访问受限|私密|已删除|地区限制|没有作品|请先登录/i;
const SENSITIVE_KEY = /token|cookie|authorization|localstorage|password|secret|phone|email|bearer/i;
const SECRET_VALUE = /Bearer\s+[^\s]+|(?:sk|rk|pk)-[A-Za-z0-9_-]{12,}/i;
const RISK_TEXT = /保证(?:赚钱|收益|流量|转化)|稳赚|零风险|全部自动|永远|完全自动|医疗|金融|确诊|死亡|伤亡|诉讼|政策/i;
const URL_HOST = /^(?:www\.)?douyin\.com$/i;

const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const now = () => new Date().toISOString();
const text = (value) => value == null ? null : String(value).trim() || null;
export const safeAlias = (value) => String(value || "").trim().replace(/[^a-zA-Z0-9_-]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
function fail(message, exitCode = 1) { const error = new Error(message); error.exitCode = exitCode; throw error; }
function safeError(value) { return String(value || "error").replace(/Bearer\s+[^\s]+/gi, "Bearer [redacted]").replace(/[A-Za-z0-9_-]{24,}/g, "[redacted]"); }

function publicUrl(value, label = "URL") {
  let url;
  try { url = new URL(String(value)); } catch { fail(`${label} 不是有效 URL`, 2); }
  if (url.protocol !== "https:" || !URL_HOST.test(url.hostname)) fail(`${label} 必须是抖音 https URL`, 2);
  url.search = "";
  url.hash = "";
  return url.href.replace(/\/$/, "");
}

export function scanSensitive(value, currentPath = "$", findings = []) {
  if (value == null) return findings;
  if (typeof value === "string") {
    if (SECRET_VALUE.test(value)) findings.push(currentPath);
    return findings;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanSensitive(item, `${currentPath}[${index}]`, findings));
    return findings;
  }
  if (typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      if (SENSITIVE_KEY.test(key)) findings.push(`${currentPath}.${key}`);
      scanSensitive(child, `${currentPath}.${key}`, findings);
    }
  }
  return findings;
}

function assertNoSensitive(value, label) {
  const findings = scanSensitive(value);
  if (findings.length) fail(`${label} contains sensitive fields: ${findings.slice(0, 3).join(", ")}`, 2);
}

function cleanMetrics(value) {
  return Array.isArray(value) ? [...new Set(value.map(text).filter(Boolean))].slice(0, 4) : [];
}

function titleSignals(value) {
  const source = text(value) || "";
  const tags = [];
  if (/[?？]|为什么|怎么|如何|难道|凭什么/.test(source)) tags.push("问题");
  if (/别再|不要|别急|先别|避开|小心/.test(source)) tags.push("提醒");
  if (/[0-9一二三四五六七八九十]+\s*(个|步|招|件|点|方法|原因)/.test(source)) tags.push("清单");
  if (/实测|演示|打开|跟我|带你|现场|看我/.test(source)) tags.push("演示");
  if (/省|提速|效率|变快|翻倍|结果|解决|搞定/.test(source)) tags.push("结果");
  if (/却|但是|但|竟然|原来|没想到|不是.{0,8}而是/.test(source)) tags.push("反差");
  if (/我|你|老板|同事|下班|上班|客户|新手/.test(source)) tags.push("人物场景");
  const pattern = tags[0] || "场景直入";
  const openingMove = pattern === "问题" ? "先抛出一个具体问题" : pattern === "提醒" ? "先给出避坑提醒" : pattern === "清单" ? "先亮出步骤或数量" : pattern === "演示" ? "先展示一个动作" : pattern === "结果" ? "先展示可见结果" : pattern === "反差" ? "先制造预期落差" : "先进入使用场景";
  return {
    pattern,
    tags: [...new Set(tags)],
    openingMove,
    confidence: source ? "heuristic-from-visible-title" : "insufficient-visible-text",
    titleLengthBucket: source.length < 10 ? "short" : source.length < 24 ? "medium" : "long",
    hasNumber: /[0-9一二三四五六七八九十]/.test(source),
    hasQuestion: /[?？]/.test(source),
  };
}

function contentType(workUrl) {
  const match = text(workUrl)?.match(/\/((?:video)|(?:note))\//i);
  return match?.[1].toLowerCase() === "note" ? "图文" : match?.[1].toLowerCase() === "video" ? "视频" : "未知";
}

function normalizeItem(item, sourceType, sourceUrl, keyword, ordinal) {
  const workUrl = text(item?.workUrl) ? publicUrl(item.workUrl, "作品 URL") : null;
  const title = text(item?.title);
  const description = text(item?.description);
  const classifier = titleSignals(title || description);
  const observedFields = [title && "title", description && "description", text(item?.author) && "author", text(item?.publishedText) && "publishedText", cleanMetrics(item?.visibleMetricsText).length && "visibleMetricsText", workUrl && "workUrl"].filter(Boolean);
  if (!workUrl && !title) return null;
  return {
    sampleId: `sample-${String(ordinal).padStart(3, "0")}`,
    sourceType,
    sourceUrl,
    keyword: keyword || null,
    workUrl,
    competitor: text(item?.author) || "未显示作者",
    contentType: contentType(workUrl),
    publishedText: text(item?.publishedText),
    visibleMetricsText: cleanMetrics(item?.visibleMetricsText),
    structure: { ...classifier, riskFlags: RISK_TEXT.test(`${title || ""} ${description || ""}`) ? ["visible-text-needs-fact-review"] : [] },
    evidence: {
      observedFields,
      originalTextStored: false,
      evidenceType: cleanMetrics(item?.visibleMetricsText).length ? "visible-metric-label" : "visible-work-card",
      note: "仅保留字段存在性和页面显示标签，未保存标题、简介或字幕原文",
    },
  };
}

function normalizePage(page, sourceType, keyword, sampleLimit) {
  if (!page || BLOCKED.test(`${page.pageText || ""} ${page.title || ""}`)) return { status: "needs_user_action", reason: `${sourceType}_blocked` };
  const sourceUrl = publicUrl(page.sourceUrl || page.url, `${sourceType} sourceUrl`);
  if (!Array.isArray(page.items) || !page.items.length) return { status: "needs_user_action", reason: `${sourceType}_evidence_unavailable` };
  const items = page.items.slice(0, sampleLimit).map((item, index) => normalizeItem(item, sourceType, sourceUrl, keyword, index + 1)).filter(Boolean);
  if (!items.length) return { status: "needs_user_action", reason: `${sourceType}_evidence_unavailable` };
  return { status: "success", sourceUrl, sourceType, keyword: keyword || null, items };
}

export function validateRequest(request, env = {}) {
  if (!request || !["mock", "easy-webbridge"].includes(request.runtime)) fail("runtime must be mock or easy-webbridge", 2);
  const accountAlias = safeAlias(request.accountAlias);
  if (!accountAlias) fail("accountAlias is required", 2);
  const accountUrl = request.accountUrl ? publicUrl(request.accountUrl, "accountUrl") : null;
  const keywords = request.keywords ?? [];
  if (!accountUrl && (!Array.isArray(keywords) || !keywords.length)) fail("accountUrl or at least one keyword is required", 2);
  if (!Array.isArray(keywords) || keywords.length > 5 || keywords.some((item) => !text(item) || String(item).length > 80)) fail("keywords must contain 0-5 short non-empty values", 2);
  const sampleLimit = request.sampleLimit ?? 8;
  if (!Number.isInteger(sampleLimit) || sampleLimit < 1 || sampleLimit > 20) fail("sampleLimit must be an integer from 1 to 20", 2);
  const explicit = text(request.browserId), configured = text(env.EASY_WEBBRIDGE_BROWSER_ID || env.SKILL_FACTORY_WEBBRIDGE_BROWSER_ID);
  if (explicit && configured && explicit !== configured) fail("browserId conflicts with configured browser", 2);
  return { runtime: request.runtime, accountAlias, accountUrl, keywords: keywords.map(text), sampleLimit, browserId: explicit || configured || null, audience: text(request.audience) || "目标受众", niche: text(request.niche) || "本赛道" };
}

export function normalizeSnapshot(request, pages, capturedAt = now()) {
  if (!Array.isArray(pages) || !pages.length) fail("at least one page snapshot is required", 2);
  let ordinal = 0;
  let remaining = request.sampleLimit;
  const seenWorkUrls = new Set();
  const normalized = [];
  for (let pageIndex = 0; pageIndex < pages.length; pageIndex += 1) {
    const page = pages[pageIndex];
    if (remaining <= 0) break;
    const pagesLeft = pages.length - pageIndex;
    const pageLimit = pagesLeft > 1 ? Math.max(1, Math.floor(remaining / pagesLeft)) : remaining;
    const result = normalizePage(page, page.sourceType || "public-page", page.keyword || null, pageLimit);
    if (result.status !== "success") return { status: result.status, reason: result.reason };
    for (const item of result.items) {
      if (item.workUrl && seenWorkUrls.has(item.workUrl)) continue;
      if (item.workUrl) seenWorkUrls.add(item.workUrl);
      normalized.push({ ...item, sampleId: `sample-${String(++ordinal).padStart(3, "0")}` });
      remaining -= 1;
      if (remaining <= 0) break;
    }
  }
  const runId = `run-${request.accountAlias}-${new Date(capturedAt).getTime().toString(36)}`;
  const snapshot = {
    schemaVersion: "1.0",
    kind: "douyin-visible-competitor-snapshot",
    status: "success",
    runtime: request.runtime,
    runId,
    accountAlias: request.accountAlias,
    query: { accountUrl: request.accountUrl || null, keywords: request.keywords, sampleLimit: request.sampleLimit, audience: request.audience, niche: request.niche },
    capturedAt,
    sourceScope: "selected-account-public-visible-web-snapshot",
    samples: normalized,
    limitations: ["仅代表采集时刻的公开页面样本，不是全网样本或官方排名", "可见指标标签不等于后台数据，未推断播放、转化、账号规模或算法规则", "标题、简介、字幕和评论原文未保存"],
  };
  assertNoSensitive(snapshot, "snapshot");
  return snapshot;
}

function promiseFor(sample) {
  if (sample.contentType === "图文") return "用一张图或一组步骤帮助受众快速理解问题";
  if (sample.structure.pattern === "演示" || sample.structure.pattern === "结果") return "让受众先看到一个可复现的动作或结果";
  if (sample.structure.pattern === "清单") return "把复杂问题拆成可执行的步骤清单";
  return "用一个具体场景解释受众正在遇到的问题";
}

export function analyzeSnapshot(snapshot) {
  if (!snapshot || snapshot.schemaVersion !== "1.0" || snapshot.kind !== "douyin-visible-competitor-snapshot" || snapshot.status !== "success" || !Array.isArray(snapshot.samples) || !snapshot.samples.length) fail("snapshot schema or samples are invalid", 2);
  assertNoSensitive(snapshot, "snapshot");
  const matrix = snapshot.samples.map((sample) => ({
    sampleId: sample.sampleId,
    sourceType: sample.sourceType,
    sourceUrl: sample.sourceUrl,
    workUrl: sample.workUrl,
    competitor: sample.competitor,
    contentType: sample.contentType,
    hookStructure: sample.structure.pattern,
    hookSignals: sample.structure.tags,
    openingMove: sample.structure.openingMove,
    audiencePromise: promiseFor(sample),
    evidenceType: sample.evidence.evidenceType,
    visibleMetricsText: sample.visibleMetricsText,
    riskFlags: sample.structure.riskFlags || [],
    differentiation: sample.structure.pattern === "场景直入" ? "补充结果或实操证据，避免只做泛场景描述" : `在“${sample.structure.pattern}”之外测试另一种开场结构`,
    reviewStatus: sample.structure.riskFlags?.length || RISK_TEXT.test(`${sample.structure.pattern} ${sample.competitor}`) ? "needs_fact_review" : "ready_for_human_review",
  }));
  const counts = new Map();
  for (const row of matrix) counts.set(row.hookStructure, (counts.get(row.hookStructure) || 0) + 1);
  const hookStructures = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).map(([pattern, count]) => ({ pattern, sampleCount: count, sampleIds: matrix.filter((row) => row.hookStructure === pattern).map((row) => row.sampleId), interpretation: "样本频次，不代表播放或转化效果" }));
  const opportunities = [];
  const dominant = hookStructures[0];
  if (dominant) opportunities.push({ opportunityId: "opp-001", type: "hook", observation: `本次样本中“${dominant.pattern}”出现 ${dominant.sampleCount} 条`, action: `测试不使用“${dominant.pattern}”的结果先行或实操开场`, evidenceSampleIds: dominant.sampleIds });
  const formats = [...new Set(matrix.map((row) => row.contentType))];
  if (formats.length === 1) opportunities.push({ opportunityId: "opp-002", type: "format", observation: `样本格式集中为${formats[0]}`, action: "测试另一种公开可见的内容载体，并记录实际呈现证据", evidenceSampleIds: matrix.map((row) => row.sampleId) });
  const withoutMetrics = matrix.filter((row) => !row.visibleMetricsText.length);
  if (withoutMetrics.length) opportunities.push({ opportunityId: "opp-003", type: "evidence", observation: `${withoutMetrics.length} 条样本没有可见指标标签`, action: "把作品页面可见的动作、步骤或结果作为证据，不补写后台表现", evidenceSampleIds: withoutMetrics.map((row) => row.sampleId) });
  const audience = text(snapshot.query?.audience) || "目标受众";
  const niche = text(snapshot.query?.niche) || "本赛道";
  const topicSuggestions = [
    { topicId: "topic-001", title: `${niche}的一个具体问题`, hook: "先给出受众能看见的结果，再解释第一步", angle: "结果先行", audience, basedOn: dominant?.sampleIds || [], note: "用自己的案例和素材验证，不复用样本文案" },
    { topicId: "topic-002", title: `${niche}的三步实操演示`, hook: "只演示一个动作，现场看它如何完成", angle: "动作证据", audience, basedOn: matrix.filter((row) => row.hookStructure === "演示").map((row) => row.sampleId), note: "步骤和结论需在发布前实测" },
    { topicId: "topic-003", title: `${niche}的反常识对比`, hook: "大家先入为主的做法，可能不是最省事的那一步", angle: "反差测试", audience, basedOn: matrix.filter((row) => row.hookStructure === "反差").map((row) => row.sampleId), note: "只表达可验证的对比，不承诺收益" },
  ];
  const evidence = snapshot.samples.map((sample) => ({ sampleId: sample.sampleId, sourceType: sample.sourceType, sourceUrl: sample.sourceUrl, workUrl: sample.workUrl, observedFields: sample.evidence.observedFields, visibleMetricsText: sample.visibleMetricsText, capturedAt: snapshot.capturedAt, originalTextStored: false }));
  const report = {
    schemaVersion: "1.0",
    kind: "douyin-competitor-research",
    status: "ready_for_human_review",
    runtime: snapshot.runtime,
    runId: snapshot.runId,
    accountAlias: snapshot.accountAlias,
    capturedAt: snapshot.capturedAt,
    sampleCount: matrix.length,
    matrix,
    hookStructures,
    evidence,
    differentiationOpportunities: opportunities,
    topicSuggestions,
    safeguards: { sensitiveScan: "passed", originalTextStored: false, backendDataInferred: false, algorithmRulesClaimed: false, humanReviewRequired: true },
    limitations: snapshot.limitations,
  };
  assertNoSensitive(report, "report");
  return report;
}

function md(value) { return String(value ?? "").replace(/[\\`*_{}\[\]()<>#+.!|-]/g, "\\$&"); }
function html(value) {
  return String(value ?? "").replace(/[&<>\"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" })[character]);
}

export function renderHtml(report) {
  const rows = report.matrix.map((row) => `<tr><td>${html(row.sampleId)}</td><td>${html(row.competitor)}</td><td>${html(row.contentType)}</td><td>${html(row.hookStructure)}</td><td>${html(row.openingMove)}</td><td>${html(row.evidenceType)}</td></tr>`).join("");
  const opportunities = report.differentiationOpportunities.map((item) => `<li><strong>${html(item.observation)}</strong>：${html(item.action)}</li>`).join("");
  const topics = report.topicSuggestions.map((item) => `<li><strong>${html(item.title)}</strong>｜${html(item.hook)}｜${html(item.angle)}</li>`).join("");
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>免费抖音竞品研究报告</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:1100px;margin:32px auto;padding:0 20px;color:#202124;line-height:1.6}table{border-collapse:collapse;width:100%;margin:12px 0 28px}th,td{border:1px solid #d9dce1;padding:8px;text-align:left;vertical-align:top}th{background:#f3f5f7}input{width:min(420px,100%);padding:8px;border:1px solid #c5cad3;border-radius:4px}code{word-break:break-all}section{margin:28px 0}</style></head><body><h1>免费抖音竞品研究报告</h1><p>运行模式：${html(report.runtime)}；安全别名：${html(report.accountAlias)}；样本数：${html(report.sampleCount)}；采集时间：${html(report.capturedAt)}</p><section><h2>竞品矩阵</h2><label>筛选矩阵：<input id="filter" type="search" placeholder="输入格式、钩子或账号"></label><table id="matrix"><thead><tr><th>样本</th><th>来源账号</th><th>格式</th><th>钩子结构</th><th>开场动作</th><th>页面证据</th></tr></thead><tbody>${rows}</tbody></table></section><section><h2>差异机会</h2><ul>${opportunities}</ul></section><section><h2>选题建议</h2><ul>${topics}</ul></section><section><h2>研究限制</h2><p>只代表公开页面在采集时刻的可见样本；没有保存原文，没有推断后台数据，也没有声称平台算法规则。发布前人工核验事实、权利和账号定位。</p></section><script>document.querySelector('#filter').addEventListener('input',event=>{const query=event.target.value.trim().toLowerCase();document.querySelectorAll('#matrix tbody tr').forEach(row=>{row.hidden=query&&!row.textContent.toLowerCase().includes(query);});});</script></body></html>\n`;
}

export function renderMarkdown(report) {
  const lines = ["# 免费抖音竞品研究报告", `- 运行模式：${md(report.runtime)}`, `- 安全别名：${md(report.accountAlias)}`, `- 采集时间：${md(report.capturedAt)}`, `- 样本数：${report.sampleCount}`, "", "## 竞品矩阵", "| 样本 | 来源 | 格式 | 钩子结构 | 开场动作 | 页面证据 |", "| --- | --- | --- | --- | --- | --- |"];
  for (const row of report.matrix) lines.push(`| ${md(row.sampleId)} | ${md(row.competitor)} | ${md(row.contentType)} | ${md(row.hookStructure)} | ${md(row.openingMove)} | ${md(row.evidenceType)} |`);
  lines.push("", "## 钩子结构", ...report.hookStructures.map((item) => `- ${md(item.pattern)}：${item.sampleCount} 条（${item.interpretation}）`), "", "## 可见证据", ...report.evidence.map((item) => `- ${md(item.sampleId)}：${md(item.workUrl || item.sourceUrl)}；可见字段 ${item.observedFields.map(md).join("、") || "无"}；页面指标 ${item.visibleMetricsText.map(md).join("、") || "无"}`), "", "## 差异机会", ...report.differentiationOpportunities.map((item) => `- ${md(item.observation)}：${md(item.action)}`), "", "## 选题建议", ...report.topicSuggestions.map((item) => `- ${md(item.title)}｜钩子：${md(item.hook)}｜角度：${md(item.angle)}｜${md(item.note)}`), "", "## 研究限制", "只代表公开页面在采集时刻的可见样本；没有保存原文，没有推断后台数据，也没有声称平台算法规则。发布前人工核验事实、权利和账号定位。", "");
  return lines.join("\n");
}

async function token() {
  const file = process.env.EASY_WEBBRIDGE_TOKEN_FILE || process.env.SKILL_FACTORY_WEBBRIDGE_TOKEN_FILE || path.join(os.homedir(), ".easy-webbridge", "bridge-token");
  try { const value = (await readFile(file, "utf8")).trim(); if (!value) fail("Easy WebBridge Token 文件为空", 2); return value; } catch (error) { if (error.exitCode) throw error; fail("找不到 Easy WebBridge Token 文件", 2); }
}
async function api(endpoint, init = {}) {
  try {
    const response = await fetch(`${(process.env.EASY_WEBBRIDGE_URL || process.env.SKILL_FACTORY_WEBBRIDGE_URL || BASE_URL).replace(/\/$/, "")}${endpoint}`, { ...init, headers: { Accept: "application/json", "Content-Type": "application/json", Authorization: `Bearer ${await token()}`, ...(init.headers || {}) } });
    if (!response.ok) fail(`Easy WebBridge request failed (HTTP ${response.status})`, 1);
    return await response.json();
  } catch (error) { if (error.exitCode) throw error; fail("Easy WebBridge unavailable; start the local bridge and retry", 1); }
}

export function selectBrowser(browsers, requestedId = null) {
  const online = (Array.isArray(browsers) ? browsers : []).filter((item) => item?.online && text(item.browserId));
  if (requestedId) { const selected = online.find((item) => item.browserId === requestedId); if (!selected) fail("selected browser is not online", 1); return selected; }
  if (!online.length) fail("no online browser is available", 1);
  if (online.length > 1) fail("multiple browsers are online; run list and set one browserId explicitly", 2);
  return online[0];
}

export function bridgeCommandPayload(action, args, session) { return { action, args: { ...args, session }, timeoutMs: 20_000 }; }
export function extractCode(kind, keyword = null) {
  const expected = kind === "account" ? "account" : "keyword-search";
  return `(() => { const pageText = document.body?.innerText?.slice(0, 12000) || ''; const links = [...document.querySelectorAll('a[href*="/video/"],a[href*="/note/"]')]; return { sourceType: ${JSON.stringify(expected)}, keyword: ${JSON.stringify(keyword)}, sourceUrl: location.href, pageText, items: links.map((a) => { const card = a.closest('div'); const raw = (card?.innerText || a.innerText || '').split(/\\n+/).map((x) => x.trim()).filter(Boolean); const imageAlt = [...(card?.querySelectorAll('img') || [])].map((img) => (img.alt || '').trim()).find(Boolean) || null; const title = a.innerText.trim() || imageAlt || raw.find((value) => value.length > 2 && !/^@/.test(value) && !/^(赞|评论|收藏|人在看|[0-9.万千]+)$/.test(value)) || null; return { title, workUrl: new URL(a.href, location.href).href, author: raw.find((x) => x.startsWith('@'))?.slice(1) || null, publishedText: raw.find((x) => /前$/.test(x)) || null, visibleMetricsText: raw.filter((x) => /赞|评论|收藏|人在看/.test(x)).slice(0, 3) }; }).filter((x) => x.title) }; })()`;
}

export function pageMatchesExpected(sourceUrl, kind) {
  try {
    const url = new URL(sourceUrl);
    if (!URL_HOST.test(url.hostname)) return false;
    if (kind === "account") return /^\/user\//i.test(url.pathname);
    if (kind === "keyword-search") return /^\/jingxuan\/search\//i.test(url.pathname);
    return false;
  } catch {
    return false;
  }
}
async function command(browserId, action, args, session) { return (await api(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: "POST", body: JSON.stringify(bridgeCommandPayload(action, args, session)) })).result; }
async function waitExtract(browserId, session, url, kind, keyword, limit) {
  const nav = await command(browserId, "navigate", { url, newTab: true, active: true, groupTitle: "抖音竞品研究" }, session);
  const tabId = nav?.tabId || nav?.id; if (!tabId) fail("navigation did not return a tab", 1);
  await new Promise((resolve) => setTimeout(resolve, 1800));
  let last = { sourceUrl: url, pageText: "", items: [] };
  for (let attempt = 0; attempt < 8; attempt++) {
    const page = await command(browserId, "evaluate", { tabId, code: extractCode(kind, keyword) }, session); last = page || last;
    if (page?.sourceUrl && pageMatchesExpected(page.sourceUrl, kind) && Array.isArray(page.items) && page.items.length) return { ...page, sourceType: kind, keyword, items: page.items.slice(0, limit) };
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  return { ...last, sourceType: kind, keyword, items: [] };
}
async function collectWebBridge(request, output) {
  const listed = await api("/v1/browsers");
  const browser = selectBrowser(listed.browsers || [], request.browserId);
  const session = `${SESSION_PREFIX}-${Date.now()}-${process.pid}`;
  const pages = [];
  try {
    if (request.accountUrl) pages.push(await waitExtract(browser.browserId, session, request.accountUrl, "account", null, request.sampleLimit));
    for (const keyword of request.keywords) pages.push(await waitExtract(browser.browserId, session, `https://www.douyin.com/jingxuan/search/${encodeURIComponent(keyword)}?type=general`, "keyword-search", keyword, request.sampleLimit));
    return normalizeSnapshot(request, pages, now());
  } finally { try { await command(browser.browserId, "close_session", {}, session); } catch {} }
}

async function cleanSuccess(output) { await Promise.all(["research-snapshot.json", "competitor-research.json", "competitor-research.md", "competitor-research.html"].map((name) => rm(path.join(output, name), { force: true }))); }
async function diagnostic(output, reason, nextStep) { await mkdir(output, { recursive: true }); await cleanSuccess(output); await writeFile(path.join(output, "run-diagnostic.json"), json({ schemaVersion: "1.0", kind: "douyin-competitor-run-diagnostic", status: "needs_user_action", reason: safeError(reason), nextStep, recordedAt: now() })); }

async function collectCommand(request, input, output) {
  await mkdir(output, { recursive: true }); await cleanSuccess(output);
  let snapshot;
  if (request.runtime === "mock") {
    if (!input) fail("mock collect needs --input fixture", 2);
    const fixture = JSON.parse(await readFile(input, "utf8"));
    const pages = Array.isArray(fixture) ? fixture : fixture.pages;
    snapshot = normalizeSnapshot(request, pages, fixture.capturedAt || now());
  } else snapshot = await collectWebBridge(request, output);
  if (snapshot.status !== "success") { await diagnostic(output, snapshot.reason, "在指定浏览器中人工处理登录、验证或公开页面状态后重试。"); fail(`collection needs user action (${snapshot.reason})`, 1); }
  await writeFile(path.join(output, "research-snapshot.json"), json(snapshot));
  return snapshot;
}

function parseArgs(argv) {
  const [verb = "help", ...rest] = argv, options = {};
  for (let i = 0; i < rest.length; i++) { if (!rest[i].startsWith("--")) fail(`unexpected argument: ${rest[i]}`, 2); const key = rest[i].slice(2).replaceAll("-", "_"); if (!rest[i + 1] || rest[i + 1].startsWith("--")) fail(`missing value for --${key}`, 2); options[key] = rest[++i]; }
  return { verb, options };
}
function usage() { console.log("Usage:\n  node scripts/douyin-competitor-research-free.mjs list\n  node scripts/douyin-competitor-research-free.mjs collect --request ./request.json [--input ./fixture.json] --output ./output\n  node scripts/douyin-competitor-research-free.mjs analyze --snapshot ./output/research-snapshot.json --output ./output\n  node scripts/douyin-competitor-research-free.mjs self-test"); }
async function main() {
  const { verb, options } = parseArgs(process.argv.slice(2));
  if (verb === "help") return usage();
  if (verb === "self-test") { console.log("Run npm test for the deterministic self-test."); return; }
  if (verb === "list") { const listed = await api("/v1/browsers"); console.log(JSON.stringify({ browsers: (listed.browsers || []).filter((item) => item.online).map((item) => ({ displayName: item.displayName, browserId: item.browserId, browser: item.browser })) })); return; }
  if (verb === "collect") {
    if (!options.request || !options.output) fail("collect needs --request and --output", 2);
    await mkdir(options.output, { recursive: true });
    await cleanSuccess(options.output);
    try { const request = validateRequest(JSON.parse(await readFile(options.request, "utf8")), process.env); const snapshot = await collectCommand(request, options.input, options.output); console.log(JSON.stringify({ status: "success", runtime: snapshot.runtime, sampleCount: snapshot.samples.length, output: options.output })); }
    catch (error) { await diagnostic(options.output, error.message, "检查输入、Easy WebBridge 和页面状态后重试。"); throw error; }
    return;
  }
  if (verb === "analyze") {
    if (!options.snapshot || !options.output) fail("analyze needs --snapshot and --output", 2);
    await mkdir(options.output, { recursive: true });
    try { const snapshot = JSON.parse(await readFile(options.snapshot, "utf8")); const report = analyzeSnapshot(snapshot); await writeFile(path.join(options.output, "competitor-research.json"), json(report)); await writeFile(path.join(options.output, "competitor-research.md"), renderMarkdown(report)); await writeFile(path.join(options.output, "competitor-research.html"), renderHtml(report)); console.log(JSON.stringify({ status: report.status, sampleCount: report.sampleCount, output: options.output })); }
    catch (error) { await diagnostic(options.output, "analysis_failed", "修正快照结构或重新采集公开样本后重试。"); throw error; }
    return;
  }
  fail("unknown command", 2);
}
if (import.meta.url === `file://${process.argv[1]}`) main().catch((error) => { console.error(safeError(error.message)); process.exit(error.exitCode || 1); });
