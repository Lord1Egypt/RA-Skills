#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ACTIONS = new Set(["navigate", "snapshot", "close_session"]);
const BLOCKED = /登录|验证码|安全验证|访问受限|私密|已删除|地区限制|请先登录/i;
const CONTROL_LINES = /^(首页|推荐|朋友|消息|我|分享|收藏|转发|评论|全部评论|回复|展开|收起|更多|点赞|登录|关注)$/;
const THEME_HINTS = [
  ["教程与上手", /怎么|如何|教程|步骤|入门|不会|看不懂|学不会/],
  ["价格与成本", /价格|多少钱|收费|免费|贵|成本|预算/],
  ["功能与兼容", /功能|支持|兼容|能不能|有没有|批量|导出|格式/],
  ["获取与链接", /链接|地址|在哪|哪里|资料|模板|版本|购买/],
  ["效果与可信度", /效果|有用|靠谱|真实|案例|广告|骗人|套路/],
  ["隐私与安全", /隐私|安全|数据|权限|账号|泄露|验证码/],
];
const NEED_RE = /想要|希望|求|需要|建议|推荐|能不能|有没有|想问|链接|教程|模板|资料|价格|多少钱|免费版|支持/;
const QUESTION_RE = /[?？]|吗(?:[。！!，,]|$)|怎么|如何|能不能|是否|为什么|为何|哪里|在哪|多少|什么时候/;
const OBJECTION_RE = /但是|不过|不行|太贵|没用|无用|不支持|不兼容|麻烦|担心|坑|不靠谱|广告|骗人|套路|缺点|不如|难用|看不懂|不会/;

export function validateBridgeBase(value = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777") {
  let url;
  try { url = new URL(value); } catch { throw new Error("Easy WebBridge 地址必须是本机 loopback HTTP"); }
  const loopback = url.hostname === "127.0.0.1" || url.hostname === "[::1]" || url.hostname === "::1";
  if (url.protocol !== "http:" || !loopback || url.username || url.password
      || (url.pathname !== "" && url.pathname !== "/") || url.search || url.hash) {
    throw new Error("Easy WebBridge 地址只允许无凭据、无路径的本机 loopback HTTP");
  }
  return url.origin;
}

const SENSITIVE_RULES = [
  { type: "email", pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi },
  { type: "phone", pattern: /(?<!\d)(?:\+?86[-\s]?)?1[3-9]\d{9}(?!\d)/g },
  { type: "bearer", pattern: /\bBearer\s+[A-Za-z0-9._~+/=-]+/gi },
  { type: "secret", pattern: /(?:sk|pk)-[A-Za-z0-9_-]{16,}|(?:token|cookie|authorization|password|passwd|api[ _-]?key|验证码|密码)\s*[:=：]\s*[^\s,，;；]+/gi },
];

export function clean(value) {
  return String(value ?? "")
    .replace(/[\u200b\ufeff]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function sanitize(value) {
  let text = clean(value);
  const redactions = [];
  for (const rule of SENSITIVE_RULES) {
    rule.pattern.lastIndex = 0;
    let count = 0;
    text = text.replace(rule.pattern, () => {
      count += 1;
      return `[已脱敏:${rule.type}]`;
    });
    if (count) redactions.push({ type: rule.type, count });
  }
  return { text, redactions };
}

export function redactError(value) {
  return sanitize(value)
    .text
    .replace(new RegExp(os.homedir().replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g"), "[home]");
}

function usage(message) {
  const error = new Error(message);
  error.code = 2;
  throw error;
}

function canonicalDouyinUrl(value) {
  let url;
  try {
    url = new URL(value);
  } catch {
    usage("URL 不是有效网址");
  }
  if (url.protocol !== "https:") usage("作品链接必须使用 HTTPS");
  const host = url.hostname.toLowerCase();
  const match = host === "douyin.com" || host === "www.douyin.com"
    ? url.pathname.match(/^\/(video|note)\/(\d+)\/?$/)
    : null;
  if (match) {
    return {
      url: `${url.protocol}//${host === "douyin.com" ? "www.douyin.com" : host}/${match[1]}/${match[2]}`,
      type: match[1],
      id: match[2],
    };
  }
  if (host === "v.douyin.com" && /^\/[A-Za-z0-9_-]+\/?$/.test(url.pathname)) {
    return { url: `${url.protocol}//v.douyin.com${url.pathname}`, type: "share", id: null };
  }
  usage("只接受一个抖音视频、图文作品链接或 v.douyin.com 分享链接");
}

export function validateUrl(value) {
  if (typeof value !== "string" || !value.trim()) usage("必须提供一个抖音作品链接");
  const work = canonicalDouyinUrl(value.trim());
  return { input: work.url, work };
}

function pageFromSnapshotUrl(value) {
  if (!value) throw new Error("页面快照缺少最终 URL，无法确认作品身份");
  try {
    const parsed = canonicalDouyinUrl(value);
    if (parsed.type === "share") throw new Error("最终页面仍是分享中转页");
    return parsed;
  } catch {
    throw new Error("最终页面不是抖音单作品页");
  }
}

function commentText(item) {
  if (typeof item === "string") return item;
  return item?.text ?? item?.content ?? item?.commentText ?? item?.desc ?? "";
}

function commentLikeText(item) {
  if (!item || typeof item === "string") return null;
  const value = item.likeText ?? item.likesText ?? item.likeCountText ?? item.likes;
  return value === undefined || value === null || value === "" ? null : clean(value);
}

export function extractVisibleComments(snapshot, limit = 20) {
  const source = [];
  if (Array.isArray(snapshot?.comments)) source.push(...snapshot.comments);
  if (!source.length) {
    const lines = String(snapshot?.text || "")
      .split(/\r?\n/)
      .map(clean)
      .filter(Boolean);
    const marker = lines.findIndex((line) => /^评论(?:区|列表)?(?:\s*\d+)?$/.test(line));
    const visible = marker >= 0 ? lines.slice(marker + 1) : [];
    source.push(...visible.filter((line) => !CONTROL_LINES.test(line)));
  }
  const results = [];
  for (const item of source) {
    const raw = clean(commentText(item));
    if (!raw || CONTROL_LINES.test(raw)) continue;
    const likeText = commentLikeText(item);
    results.push({ raw, likeText });
    if (results.length >= limit) break;
  }
  return results;
}

function themeFor(text) {
  return THEME_HINTS.find(([, pattern]) => pattern.test(text))?.[0] || "使用体验与具体场景";
}

function signalsFor(text) {
  return {
    need: NEED_RE.test(text),
    question: QUESTION_RE.test(text),
    objection: OBJECTION_RE.test(text),
    theme: themeFor(text),
  };
}

function grouped(items, field, label) {
  const groups = new Map();
  for (const item of items) {
    const key = item.signals.theme;
    if (!groups.has(key)) groups.set(key, { theme: key, evidenceIndexes: [], count: 0, label });
    const group = groups.get(key);
    group.evidenceIndexes.push(item.index);
    group.count += 1;
  }
  return [...groups.values()].sort((a, b) => b.count - a.count || a.theme.localeCompare(b.theme, "zh-CN"));
}

function makeReply(kind, item) {
  const theme = item.theme;
  if (kind === "needs") {
    return `你提到的「${theme}」很关键。可以先明确使用场景和目标，再给出对应步骤或示例；如果方便，补充一下你现在卡住的环节。`;
  }
  if (kind === "questions") {
    return `这个问题可以先从「${theme}」拆开：确认使用前提，再用一个最小案例验证，避免只看宣传。这里的整理只基于当前可见评论。`;
  }
  return `这个关于「${theme}」的顾虑很实际。建议先核对限制、成本和适用场景，再决定是否合适；当前评论样本不能代表全部用户。`;
}

function mergeRedactions(target, entries) {
  for (const entry of entries) {
    const existing = target.find((item) => item.type === entry.type);
    if (existing) existing.count += entry.count;
    else target.push({ type: entry.type, count: entry.count });
  }
}

function buildInsights(comments) {
  const needs = comments.filter((item) => item.signals.need);
  const questions = comments.filter((item) => item.signals.question);
  const objections = comments.filter((item) => item.signals.objection);
  const needsGroups = grouped(needs, "need", "需求主题");
  const questionGroups = grouped(questions, "question", "问题");
  const objectionGroups = grouped(objections, "objection", "反对点");
  const replyDrafts = [
    ...needsGroups.slice(0, 3).map((item) => ({ kind: "need", theme: item.theme, evidenceIndexes: item.evidenceIndexes, draft: makeReply("needs", item) })),
    ...questionGroups.slice(0, 3).map((item) => ({ kind: "question", theme: item.theme, evidenceIndexes: item.evidenceIndexes, draft: makeReply("questions", item) })),
    ...objectionGroups.slice(0, 3).map((item) => ({ kind: "objection", theme: item.theme, evidenceIndexes: item.evidenceIndexes, draft: makeReply("objections", item) })),
  ];
  return { needs: needsGroups, questions: questionGroups, objections: objectionGroups, replyDrafts };
}

export function normalizeSnapshot(input, snapshot, options = {}) {
  if (!snapshot || typeof snapshot !== "object") throw new Error("页面快照不是对象");
  const page = pageFromSnapshotUrl(snapshot.url);
  const pageText = `${snapshot.title || ""}\n${snapshot.text || ""}\n${Array.isArray(snapshot.comments) ? snapshot.comments.map(commentText).join("\n") : ""}`;
  if (BLOCKED.test(pageText)) throw new Error("页面需要登录或人工处理验证");
  const limit = Number.isInteger(options.limit) ? options.limit : 20;
  const visible = extractVisibleComments(snapshot, limit);
  if (!visible.length) throw new Error("页面没有可见评论样本");

  const comments = [];
  const redactions = [];
  const titleSanitized = sanitize(snapshot.title || "");
  mergeRedactions(redactions, titleSanitized.redactions);
  for (const [offset, item] of visible.entries()) {
    const sanitized = sanitize(item.raw);
    const likeSanitized = item.likeText ? sanitize(item.likeText) : null;
    comments.push({
      index: offset + 1,
      quote: sanitized.text,
      ...(likeSanitized ? { visibleLikeText: likeSanitized.text } : {}),
      signals: signalsFor(sanitized.text),
    });
    mergeRedactions(redactions, sanitized.redactions);
    if (likeSanitized) mergeRedactions(redactions, likeSanitized.redactions);
  }
  const mode = options.mode === "real" ? "real" : "mock";
  const capturedAt = options.capturedAt || new Date().toISOString();
  const report = {
    schemaVersion: "1.0",
    kind: "douyin-comment-insights",
    status: "success",
    source: {
      inputUrl: input.input,
      pageUrl: page.url,
      workId: page.id,
      workType: page.type,
      capturedAt,
      mode,
      method: mode === "real" ? "Easy WebBridge visible page snapshot" : "local fixture visible snapshot",
      sampleLimit: limit,
      visibleCommentCount: comments.length,
    },
    sample: {
      title: titleSanitized.text || null,
      comments,
    },
    insights: buildInsights(comments),
    privacy: {
      redacted: redactions.length > 0,
      redactions,
      scannedFields: ["comment text", "visible like text", "page title"],
    },
    limitations: [
      "只包含指定作品页面在采集时刻实际可见的评论样本，不代表全部用户。",
      "需求、问题和反对点是基于原文关键词的启发式整理，回复草稿未发送。",
      mode === "mock" ? "本次结果来自本地 mock fixture，不是实时页面采集。" : "本次结果来自用户授权浏览器的可见页面快照。",
    ],
  };
  return report;
}

function mdEscape(value) {
  return String(value ?? "").replace(/[|`\r\n]/g, (char) => ({ "|": "\\|", "`": "\\`", "\r": " ", "\n": " " }[char]));
}

function listInsights(items, empty) {
  if (!items.length) return [`- ${empty}`];
  return items.flatMap((item) => [
    `- ${mdEscape(item.theme)}（${item.count} 条）｜证据评论：${item.evidenceIndexes.join("、")}`,
  ]);
}

export function toMarkdown(report) {
  const modeLabel = report.source.mode === "mock" ? "mock（本地 fixture）" : "real（Easy WebBridge）";
  const lines = [
    "# 抖音评论洞察",
    `- 运行模式：${modeLabel}`,
    `- 作品页：${report.source.pageUrl}`,
    `- 页面标题：${mdEscape(report.sample.title || "未显示")}`,
    `- 可见评论样本：${report.source.visibleCommentCount} 条`,
    "",
    "## 需求主题",
    ...listInsights(report.insights.needs, "样本中没有明确的需求表达"),
    "",
    "## 评论中的问题",
    ...listInsights(report.insights.questions, "样本中没有明确的问题表达"),
    "",
    "## 反对点",
    ...listInsights(report.insights.objections, "样本中没有明确的反对表达"),
    "",
    "## 原话证据（已脱敏）",
  ];
  for (const comment of report.sample.comments) {
    lines.push(`- 评论 ${comment.index}：${mdEscape(comment.quote)}${comment.visibleLikeText ? `｜可见点赞：${mdEscape(comment.visibleLikeText)}` : ""}`);
  }
  lines.push("", "## 回复草稿（未发送）");
  if (!report.insights.replyDrafts.length) lines.push("- 暂无足够信号生成回复草稿");
  for (const draft of report.insights.replyDrafts) {
    lines.push(`- ${draft.kind === "need" ? "需求" : draft.kind === "question" ? "问题" : "反对点"}｜${mdEscape(draft.theme)}｜证据评论：${draft.evidenceIndexes.join("、")}`);
    lines.push(`  ${mdEscape(draft.draft)}`);
  }
  lines.push("", "## 边界");
  for (const limitation of report.limitations) lines.push(`- ${mdEscape(limitation)}`);
  if (report.privacy.redacted) {
    lines.push("", "## 隐私处理", "- 评论中的敏感片段已脱敏；报告只记录类型和次数，不保留原始值。");
  }
  return `${lines.join("\n")}\n`;
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    throw new Error(`无法读取 JSON 文件：${redactError(error.message)}`);
  }
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function clearOutputs(output) {
  for (const file of ["douyin-comment-insights.json", "douyin-comment-insights.md"]) {
    fs.rmSync(path.join(output, file), { force: true });
  }
}

function diagnosticCode(reason) {
  const text = redactError(reason);
  if (/多个在线浏览器/.test(text)) return "browser_selection_required";
  if (/没有在线浏览器|浏览器当前不在线/.test(text)) return "browser_unavailable";
  if (/登录|验证|访问受限|私密|已删除|地区限制/.test(text)) return "page_access_requires_user_action";
  if (/没有可见评论/.test(text)) return "visible_comments_unavailable";
  if (/Token|WebBridge|HTTP/.test(text)) return "bridge_unavailable";
  return "extraction_failed";
}

function writeDiagnostic(output, reason) {
  const code = diagnosticCode(reason);
  const next = {
    browser_selection_required: "运行 list-browsers，并用 --browser-id 明确选择一个在线浏览器后重试",
    browser_unavailable: "启动 Easy WebBridge，并确认目标浏览器扩展在线后重试",
    page_access_requires_user_action: "在目标浏览器中完成登录或验证，确认作品评论可见后重试",
    visible_comments_unavailable: "确认作品页已显示评论列表；没有可见样本时不会猜测评论",
    bridge_unavailable: "检查 Easy WebBridge 服务和本机 Token 文件后重试",
    extraction_failed: "检查抖音作品链接和运行环境后重试",
  }[code];
  writeJson(path.join(output, "run-diagnostic.json"), {
    schemaVersion: "1.0",
    kind: "douyin-comment-insights-run-diagnostic",
    status: "needs_user_action",
    reason: code,
    next,
    recordedAt: new Date().toISOString(),
  });
}

function bridgeConfig(input = {}) {
  const base = validateBridgeBase();
  const tokenPath = process.env.EASY_WEBBRIDGE_TOKEN_FILE || path.join(os.homedir(), ".easy-webbridge", "bridge-token");
  let token;
  try {
    token = fs.readFileSync(tokenPath, "utf8").trim();
  } catch {
    throw new Error("找不到 Easy WebBridge Token 文件");
  }
  if (!token) throw new Error("Easy WebBridge Token 文件为空");
  return { base, token, browserId: input.browserId || process.env.EASY_WEBBRIDGE_BROWSER_ID || null };
}

export function bridgeFetchOptions(token, init = {}) {
  return {
    ...init,
    redirect: "error",
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
      ...(init.body ? { "Content-Type": "application/json" } : {}),
    },
  };
}

async function bridgeRequest(base, endpoint, token, init = {}) {
  const response = await fetch(`${base}${endpoint}`, bridgeFetchOptions(token, init));
  if (!response.ok) throw new Error(`Easy WebBridge 请求失败（HTTP ${response.status}）`);
  return response.json();
}

export function selectBrowser(browsers, requestedId = null) {
  const online = (Array.isArray(browsers) ? browsers : []).filter((browser) => browser?.online && browser.browserId);
  if (requestedId) {
    const selected = online.find((browser) => browser.browserId === requestedId);
    if (!selected) throw new Error("指定的浏览器当前不在线，请重新查看在线浏览器");
    return selected;
  }
  if (online.length === 1) return online[0];
  if (!online.length) throw new Error("没有在线浏览器，请先启动 Easy WebBridge 并连接扩展");
  throw new Error("检测到多个在线浏览器，请先运行 list-browsers，再用 --browser-id 明确选择一个环境");
}

async function listBrowsers() {
  const config = bridgeConfig();
  const payload = await bridgeRequest(config.base, "/v1/browsers", config.token);
  return (payload.browsers || []).filter((browser) => browser?.online).map((browser) => ({
    browserId: browser.browserId,
    displayName: clean(browser.displayName || browser.browserId),
    browser: clean(browser.browser || "Chromium"),
  }));
}

async function realInspect(input, options) {
  const config = bridgeConfig(options);
  const listed = await bridgeRequest(config.base, "/v1/browsers", config.token);
  const selected = selectBrowser(listed.browsers, config.browserId);
  const session = `douyin-comment-insights-free-${Date.now()}-${process.pid}`;
  let created = false;
  const command = async (action, args) => {
    if (!ACTIONS.has(action)) throw new Error("浏览器动作不在允许列表");
    const payload = await bridgeRequest(
      config.base,
      `/v1/browsers/${encodeURIComponent(selected.browserId)}/commands`,
      config.token,
      { method: "POST", body: JSON.stringify({ action, args, timeoutMs: 20_000 }) },
    );
    return payload.result ?? payload;
  };
  try {
    created = true;
    const nav = await command("navigate", {
      url: input.input,
      newTab: true,
      session,
      groupTitle: "抖音评论洞察",
    });
    const tabId = nav?.tabId;
    if (!tabId) throw new Error("导航没有返回标签页");
    const deadline = Date.now() + 12_000;
    let lastError = new Error("页面内容仍在加载");
    do {
      try {
        const snapshot = await command("snapshot", { tabId, maxTextLength: 30_000 });
        return normalizeSnapshot(input, snapshot, { mode: "real", limit: options.limit });
      } catch (error) {
        lastError = error;
        if (/登录|验证|访问受限|私密|已删除|地区限制/.test(error.message)) throw error;
        await new Promise((resolve) => setTimeout(resolve, 500));
      }
    } while (Date.now() < deadline);
    throw lastError;
  } finally {
    if (created) {
      try {
        await command("close_session", { session });
      } catch {
        // Cleanup failure must not expose the browser token or stop report sanitization.
      }
    }
  }
}

function parseArgs(argv) {
  const [action = "inspect", ...rest] = argv;
  const result = { action, output: "./comment-insights", limit: 20, browserId: null, url: null, mock: null };
  for (let index = 0; index < rest.length; index += 1) {
    const flag = rest[index];
    if (flag === "--url") result.url = rest[++index];
    else if (flag === "--output") result.output = rest[++index];
    else if (flag === "--mock") result.mock = rest[++index];
    else if (flag === "--browser-id") result.browserId = rest[++index];
    else if (flag === "--limit") result.limit = Number(rest[++index]);
    else usage(`未知参数：${flag}`);
  }
  if (!Number.isInteger(result.limit) || result.limit < 1 || result.limit > 50) usage("--limit 必须是 1-50 的整数");
  return result;
}

async function main(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  if (args.action === "list-browsers") {
    process.stdout.write(`${JSON.stringify({ browsers: await listBrowsers() }, null, 2)}\n`);
    return;
  }
  if (args.action === "self-test") {
    const result = spawnSync(process.execPath, [path.join(ROOT, "scripts", "self-test.mjs")], { stdio: "inherit" });
    if (result.error) throw result.error;
    if (result.status !== 0) {
      const failure = new Error("self-test 未通过");
      failure.code = result.status || 1;
      throw failure;
    }
    return;
  }
  if (args.action !== "inspect") usage("动作只能是 inspect、list-browsers 或 self-test");
  const input = validateUrl(args.url);
  const output = path.resolve(args.output);
  fs.mkdirSync(output, { recursive: true });
  clearOutputs(output);
  try {
    const report = args.mock
      ? normalizeSnapshot(input, readJson(path.resolve(args.mock)), { mode: "mock", limit: args.limit })
      : await realInspect(input, { browserId: args.browserId, limit: args.limit });
    writeJson(path.join(output, "douyin-comment-insights.json"), report);
    fs.writeFileSync(path.join(output, "douyin-comment-insights.md"), toMarkdown(report));
    process.stdout.write(`${JSON.stringify({ status: "success", mode: report.source.mode, comments: report.sample.comments.length, output }, null, 2)}\n`);
  } catch (error) {
    writeDiagnostic(output, error.message);
    process.stderr.write(`${redactError(error.message)}\n`);
    const failure = new Error(redactError(error.message));
    failure.code = 1;
    throw failure;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    process.exitCode = error.code || 1;
  });
}
