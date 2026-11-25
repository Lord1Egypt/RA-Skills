#!/usr/bin/env node

import { mkdir, mkdtemp, readFile, rename, writeFile, rm, unlink } from "node:fs/promises";
import { homedir, tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { randomUUID } from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const DEFAULT_BRIDGE_URL = "http://127.0.0.1:17777";
const DEFAULT_OUTPUT = "douyin-work-analysis";
const MAX_SNAPSHOT_TEXT = 100_000;
const REPORT_FILES = ["douyin-work-analysis.json", "douyin-work-analysis.md"];
const VALUE_OPTIONS = new Map([
  ["--url", "url"],
  ["--browserId", "browserId"],
  ["--browser-id", "browserId"],
  ["--tabId", "tabId"],
  ["--tab-id", "tabId"],
  ["--output", "output"],
  ["--wait-ms", "waitMs"],
  ["--mock", "mock"],
]);

const HELP = `抖音作品分析

用法:
  node scripts/douyin-work-analyzer.mjs analyze --url <抖音作品URL> [选项]
  node scripts/douyin-work-analyzer.mjs self-test

选项:
  --browserId, --browser-id <id>  Easy WebBridge 浏览器 ID；只有一个在线浏览器时可省略
  --output <目录>    输出目录，默认 ./douyin-work-analysis
  --tabId, --tab-id <id> 使用已经打开的标签页，不新开页面
  --wait-ms <毫秒>   导航后等待时间，默认 1500（300-10000）
  --keep-tab         不关闭本次创建的任务标签组
  --mock <文件>      使用本地快照，仅用于测试，不访问 Bridge
  --help             显示帮助

环境变量:
  EASY_WEBBRIDGE_URL        默认 http://127.0.0.1:17777
  EASY_WEBBRIDGE_TOKEN      直接提供本机访问凭证（不得写入报告或日志）
  EASY_WEBBRIDGE_TOKEN_FILE 访问凭证文件路径，默认 ~/.easy-webbridge/bridge-token
`;

class UsageError extends Error {}

function parseArgs(argv) {
  const args = [...argv];
  const first = args[0] && !args[0].startsWith("-") ? args.shift() : "analyze";
  const options = { command: first };
  const seen = new Set();
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--help" || arg === "-h") return { command: "help" };
    if (arg === "--keep-tab") {
      if (seen.has("keepTab")) throw new UsageError("参数 --keep-tab 不能重复");
      seen.add("keepTab");
      options.keepTab = true;
      continue;
    }
    const key = VALUE_OPTIONS.get(arg);
    if (!key) throw new UsageError(`无法识别参数: ${arg}`);
    if (seen.has(key)) throw new UsageError(`参数 ${arg} 不能重复`);
    seen.add(key);
    const value = args[++index];
    if (!value || value.startsWith("--")) throw new UsageError(`参数 ${arg} 需要一个值`);
    options[key] = value;
  }
  return options;
}

function assertDouyinWorkUrl(value, label = "URL") {
  let url;
  try {
    url = new URL(String(value));
  } catch {
    throw new UsageError(`${label} 不是有效网址`);
  }
  const hostname = url.hostname.toLowerCase();
  if (!/^([a-z0-9-]+\.)*douyin\.com$/.test(hostname)) {
    throw new UsageError(`${label} 必须是 douyin.com 页面`);
  }
  if (!/^https?:$/.test(url.protocol)) throw new UsageError(`${label} 必须使用 http 或 https`);
  const match = url.pathname.match(/^\/(?:video|note)\/(\d{10,30})\/?$/);
  if (!match) throw new UsageError(`${label} 必须是单个抖音作品页面（/video/<作品ID> 或 /note/<作品ID>）`);
  return { url: url.toString(), workId: match[1], kind: url.pathname.startsWith("/note/") ? "note" : "video" };
}

function toWaitMs(value) {
  const waitMs = value == null ? 1500 : Number(value);
  if (!Number.isInteger(waitMs) || waitMs < 300 || waitMs > 10_000) {
    throw new UsageError("--wait-ms 必须是 300 到 10000 之间的整数");
  }
  return waitMs;
}

function sleep(ms) {
  return new Promise((resolvePromise) => setTimeout(resolvePromise, ms));
}

async function readBridgeToken() {
  if (process.env.EASY_WEBBRIDGE_TOKEN?.trim()) return process.env.EASY_WEBBRIDGE_TOKEN.trim();
  const tokenPath = process.env.EASY_WEBBRIDGE_TOKEN_FILE?.trim() || join(homedir(), ".easy-webbridge", "bridge-token");
  try {
    const token = (await readFile(tokenPath, "utf8")).trim();
    if (!token) throw new Error("empty credential");
    return token;
  } catch (error) {
    if (error.code === "ENOENT") return "";
    throw new Error("无法读取 Easy WebBridge 访问凭证文件；请检查文件路径和权限");
  }
}

function safeErrorMessage(error) {
  return String(error?.message || error)
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, "Bearer <redacted>")
    .replace(/(?:token|authorization|cookie|browserId|session)\s*[=:]\s*[^\s,;]+/gi, "sensitive-value=<redacted>")
    .replace(/douyin-work-analyzer-\d+-[a-f0-9-]+/gi, "task-session-<redacted>");
}

async function bridgeRequest(baseUrl, path, { token = "", method = "GET", body, timeoutMs = 20_000 } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const headers = { Accept: "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers["Content-Type"] = "application/json";
  try {
    const response = await fetch(`${baseUrl.replace(/\/$/, "")}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
    });
    let payload = null;
    try {
      payload = await response.json();
    } catch {
      payload = null;
    }
    if (!response.ok) {
      if (response.status === 401) throw new Error("Easy WebBridge 访问凭证无效（HTTP 401）");
      if (response.status === 404) throw new Error("Easy WebBridge API 端点不存在；请检查服务版本");
      throw new Error(`Easy WebBridge 请求失败（HTTP ${response.status}）；请检查本机服务日志`);
    }
    return payload;
  } catch (error) {
    if (error.name === "AbortError") throw new Error("Easy WebBridge 请求超时；请检查本机服务和页面状态");
    if (error instanceof TypeError) throw new Error(`无法连接 Easy WebBridge（${baseUrl}）。请先启动本机服务。`);
    throw new Error(safeErrorMessage(error));
  } finally {
    clearTimeout(timer);
  }
}

async function bridgeCommand(baseUrl, token, browserId, action, args) {
  const path = `/v1/browsers/${encodeURIComponent(browserId)}/commands`;
  const payload = await bridgeRequest(baseUrl, path, {
    token,
    method: "POST",
    body: { action, args, timeoutMs: 20_000 },
  });
  return payload?.result ?? payload;
}

function normalizeSnapshot(payload) {
  let snapshot = payload;
  if (snapshot?.result && typeof snapshot.result === "object") snapshot = snapshot.result;
  if (!snapshot || typeof snapshot !== "object") throw new Error("页面快照为空或格式不正确");
  const text = typeof snapshot.text === "string" ? snapshot.text : "";
  const title = typeof snapshot.title === "string" ? snapshot.title.trim() : "";
  const url = typeof snapshot.url === "string" ? snapshot.url.trim() : "";
  const interactive = Array.isArray(snapshot.interactive) ? snapshot.interactive : [];
  if (!text.trim() && !title) throw new Error("页面快照没有可见标题或正文");
  return { title, url, text: text.slice(0, MAX_SNAPSHOT_TEXT), interactive };
}

function containsSensitiveMarker(value) {
  return /(?:token|authorization|cookie|browser(?:-|_)?id|session)/i.test(String(value || ""));
}

function sanitizeText(value, { nullable = false, maxLength } = {}) {
  if (value == null) return nullable ? null : "";
  const cleaned = String(value)
    .split(/\r?\n/)
    .filter((line) => !containsSensitiveMarker(line))
    .join(" ")
    .replace(/[\u200b\ufeff]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  const bounded = maxLength ? cleaned.slice(0, maxLength) : cleaned;
  return bounded || (nullable ? null : "");
}

function sanitizeUrl(value) {
  const url = new URL(assertDouyinWorkUrl(value).url);
  for (const key of [...url.searchParams.keys()]) {
    if (containsSensitiveMarker(key) || containsSensitiveMarker(url.searchParams.get(key))) {
      url.searchParams.delete(key);
    }
  }
  url.username = "";
  url.password = "";
  return url.toString();
}

function meaningfulLines(text) {
  return String(text || "")
    .split(/\r?\n/)
    .map((line) => line.replace(/[\u200b\ufeff]/g, "").replace(/\s+/g, " ").trim())
    .filter((line) => line && !containsSensitiveMarker(line))
    .filter((line) => !/^(登录|注册|首页|推荐|朋友|消息|我|分享|返回|更多|充钻石|通知|投稿|综合|视频|用户|直播|多列|单列|筛选|客户端|壁纸)$/.test(line))
    .filter((line) => !/^20\d{2} © 抖音$/.test(line))
    .filter((line) => !/(?:ICP备|京公网安备|许可证|营业执照|备案|人服证|举报|服务协议|隐私政策|账号找回|联系我们|加入我们|友情链接|站点地图)/.test(line));
}

function detectAccessGate(text) {
  const value = String(text || "")
    .replace(/请先登录后发表评论/g, "")
    .replace(/登录后发表评论/g, "");
  const patterns = [
    /请登录(?:后|抖音)/,
    /登录后(?:观看|查看|继续)/,
    /(?:手机号|手机号码).{0,12}(?:登录|注册|进入)/,
    /(?:扫码|密码|短信验证码|其他方式)登录/,
    /输入手机号/,
    /获取验证码/,
    /安全验证/,
    /验证码/,
    /访问受限/,
    /访问过于频繁/,
    /完成验证后继续/,
    /风险提示.*验证/,
  ];
  return patterns.find((pattern) => pattern.test(value))?.source || null;
}

function normalizedPageTitle(title) {
  return sanitizeText(title, { nullable: true, maxLength: 240 })
    ?.replace(/\s*[-_|｜]\s*抖音(?:短视频)?\s*$/i, "")
    .replace(/^抖音\s*[-_|｜:]?\s*/i, "")
    .trim() || null;
}

function targetWorkLines(snapshot, sourceUrl) {
  const source = assertDouyinWorkUrl(sourceUrl, "输入 URL");
  const page = assertDouyinWorkUrl(snapshot.url || sourceUrl, "当前页面 URL");
  if (source.workId !== page.workId) throw new Error("当前页面作品 ID 与输入 URL 不一致，已停止分析");

  const lines = meaningfulLines(snapshot.text);
  const titleAnchor = normalizedPageTitle(snapshot.title);
  const exactInteractiveTexts = snapshot.interactive
    .filter((item) => {
      try {
        return item?.visible !== false && assertDouyinWorkUrl(item.href, "交互链接").workId === source.workId;
      } catch {
        return false;
      }
    })
    .map((item) => sanitizeText(item.text, { nullable: true, maxLength: 240 }))
    .filter((text) => text && !/^(客户端|打开|播放|详情|视频)$/.test(text));
  const visibleHashtags = snapshot.interactive
    .filter((item) => item?.visible !== false && /^#[\p{L}\p{N}_-]{1,40}$/u.test(String(item.text || "").trim()))
    .map((item) => String(item.text).trim());

  const anchorIndexes = [];
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (line.includes(source.workId)) anchorIndexes.push(index);
    if (titleAnchor && titleAnchor.length >= 6 && (line === titleAnchor || line.includes(titleAnchor) || titleAnchor.includes(line))) anchorIndexes.push(index);
    if (exactInteractiveTexts.some((text) => line === text || line.includes(text))) anchorIndexes.push(index);
    if (visibleHashtags.length >= 2 && visibleHashtags.filter((tag) => line.includes(tag)).length >= 2) anchorIndexes.push(index);
  }
  if (!anchorIndexes.length) {
    const publishedAt = lines.findIndex((line) => /^发布时间\s*[:：]/.test(line));
    if (publishedAt >= 0) {
      const workText = lines
        .map((line, index) => ({ line, index }))
        .slice(Math.max(0, publishedAt - 12), publishedAt)
        .reverse()
        .find(({ line }) => line.length >= 12 && !/^\d+(?:\.\d+)?(?:万|亿)?$/.test(line) && !/^(作者声明|章节要点|举报)/.test(line));
      anchorIndexes.push(workText?.index ?? publishedAt);
    }
  }
  if (!anchorIndexes.length) {
    throw new Error("无法从快照建立目标作品身份边界；请确认标签页停留在指定作品详情页后重试");
  }

  const anchor = Math.min(...anchorIndexes);
  const boundaryPattern = /^(相关推荐|推荐视频|猜你喜欢|更多作品|相关搜索|为你推荐|评论区|全部评论|展开更多评论|大家都在搜：?)$/;
  let start = Math.max(0, anchor - 3);
  let end = Math.min(lines.length, anchor + 24);
  for (let index = anchor - 1; index >= start; index -= 1) {
    if (boundaryPattern.test(lines[index])) {
      start = index + 1;
      break;
    }
  }
  for (let index = anchor + 1; index < end; index += 1) {
    if (boundaryPattern.test(lines[index])) {
      end = index;
      break;
    }
  }
  while (start < anchor && boundaryPattern.test(lines[start])) start += 1;
  return { lines: lines.slice(start, end), workId: source.workId };
}

function visibleAuthor(lines) {
  const authorLine = lines.find((line) => /^(作者|创作者|发布者)\s*[:：]/.test(line));
  if (authorLine) {
    return {
      value: sanitizeText(authorLine.replace(/^(作者|创作者|发布者)\s*[:：]\s*/, ""), { nullable: true, maxLength: 120 }),
      evidence: authorLine,
    };
  }
  const atLine = lines.find((line) => /^@[\p{L}\p{N}_-]{1,80}(?:\s|$)/u.test(line));
  if (atLine) {
    return {
      value: sanitizeText(atLine.replace(/^@/, ""), { nullable: true, maxLength: 120 }),
      evidence: atLine,
    };
  }
  return { value: null, evidence: null };
}

function isAuxiliarySummaryLine(lines, index) {
  const markerPattern = /^(总结|章节要点|章节摘要|本集总结|内容总结)\s*[:：]?$/;
  if (markerPattern.test(lines[index])) return true;
  for (let previous = index - 1; previous >= 0 && previous >= index - 2; previous -= 1) {
    if (/^\d{1,2}:\d{2}$/.test(lines[previous])) continue;
    return markerPattern.test(lines[previous]);
  }
  return false;
}

function visibleDescription(lines, title, author, { skip = [] } = {}) {
  const ignored = new Set([title, author].filter(Boolean));
  for (const item of skip) if (item) ignored.add(item);
  const candidates = lines.filter((line, index) => {
    if (ignored.has(line)) return false;
    if (title && (line.startsWith(title) || title.startsWith(line))) return false;
    if (isAuxiliarySummaryLine(lines, index)) return false;
    if (/^https?:\/\//i.test(line) || /(?:fixture|离线自测|虚构样例|测试样例)/i.test(line)) return false;
    if (/^(作者|创作者|发布者)\s*[:：]/.test(line)) return false;
    if (/^(作者声明|总结|章节要点|章节摘要|本集总结|内容总结|发布时间|全部评论|大家都在搜|留下你的精彩评论吧|请先登录后发表评论)/.test(line)) return false;
    if (/^\d{1,2}:\d{2}\s*\/\s*\d{1,2}:\d{2}$/.test(line) || /^(发送|倍速|智能|清屏|连播|下一章)$/.test(line)) return false;
    if (/^(点赞|评论|收藏|分享)\s*[:：]?\s*[\d,.]+/.test(line)) return false;
    if (/(?:ICP备|京公网安备|许可证|营业执照|备案|人服证|举报|服务协议|隐私政策|账号找回|联系我们|加入我们|友情链接|站点地图)/.test(line)) return false;
    if (/^(?:#[\p{L}\p{N}_-]+\s*)+$/u.test(line)) return false;
    return line.length >= 8;
  });
  return candidates[0]?.slice(0, 600) || null;
}

function parseCount(value) {
  const normalized = String(value).replace(/,/g, "").replace(/\s/g, "");
  const match = normalized.match(/([\d.]+)(万|亿)?/);
  if (!match) return null;
  const number = Number(match[1]);
  if (!Number.isFinite(number)) return null;
  const multiplier = match[2] === "亿" ? 100_000_000 : match[2] === "万" ? 10_000 : 1;
  return Math.round(number * multiplier);
}

function visibleMetrics(text) {
  const metrics = {};
  for (const label of ["点赞", "评论", "收藏", "分享"]) {
    const pattern = new RegExp(`${label}\\s*[:：]?\\s*([\\d,.]+(?:万|亿)?)`);
    const match = String(text).match(pattern);
    metrics[label] = match ? parseCount(match[1]) : null;
  }
  return metrics;
}

function extractHashtags(text) {
  return [...new Set(String(text).match(/#[\p{L}\p{N}_-]{1,40}/gu) || [])].slice(0, 30);
}

function classifyHook(text) {
  if (!text) return "未能从可见文本确认";
  if (/[？?]/.test(text)) return "提问式";
  if (/(一招|只需|教你|方法|教程|效果|结果|直接)/.test(text)) return "结果或方法式";
  if (/(但是|却|没想到|原来|竟然|从不|别再)/.test(text)) return "反差或悬念式";
  return "直接陈述式";
}

function findCtaEvidence(lines) {
  return lines.find((line) => {
    if (/^(点赞|评论|收藏|分享)\s*[:：]?\s*[\d,.]+(?:万|亿)?$/.test(line)) return false;
    return /(?:请|记得|欢迎|别忘了|可以|想看).{0,12}(?:关注|点赞|收藏|评论|转发)|(?:关注|点赞|收藏|评论|转发).{0,12}(?:我|一下|支持|告诉|留言|下集|更多)/.test(line);
  }) || null;
}

function buildReport(snapshot, sourceUrl, capturedAt = new Date().toISOString()) {
  const { lines } = targetWorkLines(snapshot, sourceUrl);
  const safePageTitle = sanitizeText(snapshot.title, { nullable: true, maxLength: 240 });
  const pageTitleCandidate = normalizedPageTitle(snapshot.title);
  const visibleTitleCandidate = lines.find((line) => /#[\p{L}\p{N}_-]{1,40}/u.test(line) && line.length >= 8)
    || lines.find((line) => line.length >= 12 && !/^\d+(?:\.\d+)?(?:万|亿)?$/.test(line) && !/^(作者声明|章节要点|发布时间|全部评论|大家都在搜)/.test(line));
  const title = pageTitleCandidate || sanitizeText(visibleTitleCandidate, { nullable: true, maxLength: 240 });
  const authorResult = visibleAuthor(lines);
  const author = authorResult.value;
  const description = visibleDescription(lines, title, author);
  const contentText = [snapshot.title, ...lines].filter(Boolean).join("\n");
  const hashtags = extractHashtags(contentText);
  const metrics = visibleMetrics(lines.join("\n"));
  const hookText = description;
  const topic = hashtags.length ? hashtags.slice(0, 5).join("、") : (description ? description.slice(0, 48) : null);
  const metricEvidence = lines.filter((line) => /(点赞|评论|收藏|分享)/.test(line)).slice(0, 8);
  const titleEvidence = title ? (lines.find((line) => line === title || line.includes(title)) || title) : null;
  const hashtagEvidence = lines.filter((line) => /#[\p{L}\p{N}_-]{1,40}/u.test(line));
  const evidenceLines = [...new Set([
    titleEvidence,
    authorResult.evidence,
    description,
    ...hashtagEvidence,
    ...metricEvidence,
  ].filter(Boolean))].slice(0, 12);
  const bodyEvidence = visibleDescription(lines, title, author, { skip: [description] });
  const ctaEvidence = findCtaEvidence(lines);
  const strengths = [];
  if (hookText) strengths.push(`作品文案中有可识别的${classifyHook(hookText)}表达`);
  if (hashtags.length) strengths.push(`页面展示了 ${hashtags.length} 个话题标签，可用于归纳内容方向`);
  if (Object.values(metrics).some((value) => value !== null)) strengths.push("页面显示了部分互动指标，可作为当前页面的观察记录");
  if (!strengths.length) strengths.push("当前快照没有足够可见信息，暂不评价内容优劣");
  const issues = [];
  if (!description) issues.push("没有从快照中识别到足够长的作品文案");
  if (!hashtags.length) issues.push("当前页面没有识别到 #话题标签");
  issues.push("未从页面快照确认视频镜头、剪辑节奏、配乐和完整字幕");
  const reusableIdeas = [];
  if (hookText) reusableIdeas.push(`参考“${hookText.slice(0, 36)}${hookText.length > 36 ? "…" : ""}”的表达方式，再用自己的事实和案例重写`);
  if (hashtags.length) reusableIdeas.push(`围绕 ${hashtags.slice(0, 3).join("、")} 设计同主题选题，不直接复制原作内容`);
  reusableIdeas.push("先用 1 个明确问题或结果承诺抓住注意力，再在主体给出可验证的信息");

  return {
    schemaVersion: "1.0",
    kind: "douyin-work-analysis",
    source: {
      url: sanitizeUrl(sourceUrl),
      pageUrl: sanitizeUrl(snapshot.url || sourceUrl),
      pageTitle: safePageTitle,
      capturedAt,
      method: "Easy WebBridge visible page snapshot",
    },
    work: {
      title,
      author,
      description,
      hashtags,
      visibleMetrics: metrics,
    },
    analysis: {
      hook: { text: hookText, type: classifyHook(hookText) },
      topic,
      structure: [
        { section: "开头钩子", evidence: hookText, confidence: hookText ? "medium" : "none" },
        { section: "主体信息", evidence: bodyEvidence, confidence: bodyEvidence ? "low" : "none" },
        { section: "结尾行动", evidence: ctaEvidence, confidence: ctaEvidence ? "low" : "none" },
      ],
      strengths,
      issues,
      reusableIdeas,
    },
    evidence: {
      visibleTextSample: evidenceLines,
      metricLines: metricEvidence,
      extractionNotes: [
        "字段只来自当前页面快照；空值表示未在可见内容中确认。",
        "作者只接受目标作品文本区域内的明确作者标签或 @作者文本；未使用全局用户链接猜测作者。",
        "“总结”“章节要点”等页面辅助摘要不会写入作品文案，也不会据此生成开头钩子。",
        Object.values(metrics).some((value) => value !== null)
          ? "带有明确指标标签的缩写数字按页面显示值换算为整数，仅代表采集时刻的可见记录。"
          : "快照未提供带明确标签的互动数字，因此互动字段保持 null；未将无标签数字按位置猜测映射。",
      ],
    },
    limitations: [
      "这是单个页面的点时快照，不是官方榜单、历史趋势或真实性证明。",
      "页面快照不能证明视频画面、镜头节奏、音乐、语气或完整字幕。",
      "不抓取推荐流、不批量爬取、不读取浏览器身份存储、本地网页存储、网络正文或非公开数据。",
    ],
  };
}

function md(value) {
  return String(value ?? "未识别").replace(/\r?\n/g, " ").trim() || "未识别";
}

function reportMarkdown(report) {
  const { source, work, analysis, evidence, limitations } = report;
  const metricRows = Object.entries(work.visibleMetrics).map(([label, value]) => `| ${label} | ${value == null ? "未显示" : value.toLocaleString("zh-CN")} |`).join("\n");
  const structure = analysis.structure.map((item) => `- **${item.section}**（${item.confidence}）：${md(item.evidence)}`).join("\n");
  const list = (items) => items.map((item) => `- ${md(item)}`).join("\n");
  const evidenceText = evidence.visibleTextSample.length ? evidence.visibleTextSample.map((line) => `> ${md(line)}`).join("\n") : "> 未读取到可见正文";
  return `# 抖音作品分析报告

## 来源与采集时间

- 原始输入 URL：${source.url}
- 快照页面 URL：${source.pageUrl}
- 页面标题：${md(source.pageTitle)}
- 采集时间：${source.capturedAt}
- 读取方式：${source.method}

## 作品可见信息

- 标题：${md(work.title)}
- 作者：${md(work.author)}
- 作品文案：${md(work.description)}
- 话题：${work.hashtags.length ? work.hashtags.join(" ") : "未识别"}

## 开头钩子与主题

- 开头钩子：${md(analysis.hook.text)}
- 钩子类型：${md(analysis.hook.type)}
- 主题线索：${md(analysis.topic)}

## 可见内容结构

${structure}

## 可见互动信息

| 指标 | 页面显示值（换算后） |
| --- | ---: |
${metricRows}

## 亮点

${list(analysis.strengths)}

## 问题与未确认项

${list(analysis.issues)}

## 可借鉴方向

${list(analysis.reusableIdeas)}

## 页面证据摘录

${evidenceText}

## 限制与合规说明

${list(limitations)}

> 本报告只分析一个作品当前页面公开可见的信息，不代表抖音官方评价，也不执行点赞、评论、关注、收藏、发布或其他账号操作。
`;
}

async function writeReports(report, outputDir) {
  const directory = resolve(outputDir || DEFAULT_OUTPUT);
  await mkdir(directory, { recursive: true });
  const jsonTemp = join(directory, `.douyin-work-analysis-${randomUUID()}.json.tmp`);
  const markdownTemp = join(directory, `.douyin-work-analysis-${randomUUID()}.md.tmp`);
  try {
    await writeFile(jsonTemp, `${JSON.stringify(report, null, 2)}\n`, "utf8");
    await writeFile(markdownTemp, reportMarkdown(report), "utf8");
    await rename(jsonTemp, join(directory, REPORT_FILES[0]));
    await rename(markdownTemp, join(directory, REPORT_FILES[1]));
  } finally {
    await rm(jsonTemp, { force: true });
    await rm(markdownTemp, { force: true });
  }
  return directory;
}

async function clearReports(outputDir) {
  const directory = resolve(outputDir || DEFAULT_OUTPUT);
  await Promise.all(REPORT_FILES.map(async (file) => {
    try {
      await unlink(join(directory, file));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }));
}

function chooseBrowser(browsers, requestedId) {
  const online = browsers.filter((browser) => browser && browser.online);
  if (!online.length) throw new Error("Easy WebBridge 没有在线浏览器；请打开已授权浏览器并确认扩展已连接");
  if (requestedId) {
    const selected = online.find((browser) => String(browser.browserId) === String(requestedId));
    if (!selected) throw new Error("找不到指定的在线浏览器；请重新获取在线列表后精确选择");
    return selected;
  }
  if (online.length !== 1) {
    throw new Error("在线浏览器不止一个，请传入 --browser-id 精确选择；为避免泄露标识，本错误不回显在线列表");
  }
  return online[0];
}

async function runLive(options, dependencies = {}) {
  const request = dependencies.bridgeRequest || bridgeRequest;
  const command = dependencies.bridgeCommand || bridgeCommand;
  const getToken = dependencies.readBridgeToken || readBridgeToken;
  const wait = dependencies.sleep || sleep;
  if (!options.url) throw new UsageError("真实运行必须提供 --url");
  const sourceUrl = assertDouyinWorkUrl(options.url).url;
  const baseUrl = process.env.EASY_WEBBRIDGE_URL?.trim() || DEFAULT_BRIDGE_URL;
  const token = await getToken();
  if (!token) throw new Error("未找到 Easy WebBridge 访问凭证；请配置环境变量或默认凭证文件");
  try {
    await request(baseUrl, "/health");
  } catch (error) {
    throw new Error(`Easy WebBridge 健康检查失败：${safeErrorMessage(error)}`);
  }
  const browserPayload = await request(baseUrl, "/v1/browsers", { token });
  const browser = chooseBrowser(Array.isArray(browserPayload?.browsers) ? browserPayload.browsers : [], options.browserId);
  const session = `douyin-work-analyzer-${Date.now()}-${randomUUID().slice(0, 8)}`;
  let createdSession = false;
  let snapshot;
  try {
    let tabId = options.tabId == null ? null : Number(options.tabId);
    if (options.tabId != null && (!Number.isInteger(tabId) || tabId < 1)) throw new UsageError("--tab-id 必须是正整数");
    if (tabId == null) {
      createdSession = true;
      const navigation = await command(baseUrl, token, browser.browserId, "navigate", {
        url: sourceUrl,
        newTab: true,
        active: true,
        session,
        groupTitle: "抖音作品分析",
      });
      tabId = Number(navigation?.tabId);
      if (!Number.isInteger(tabId)) throw new Error("导航成功但没有返回 tabId");
      await wait(toWaitMs(options.waitMs));
    }
    snapshot = normalizeSnapshot(await command(baseUrl, token, browser.browserId, "snapshot", { tabId, maxTextLength: MAX_SNAPSHOT_TEXT }));
    const gate = detectAccessGate(`${snapshot.title}\n${snapshot.text}`);
    if (gate) throw new Error("当前页面要求登录、验证码或安全验证，已停止分析；请在已授权浏览器中完成合法验证后重试");
    const pageUrl = assertDouyinWorkUrl(snapshot.url || sourceUrl, "当前页面 URL");
    if (pageUrl.workId !== assertDouyinWorkUrl(sourceUrl).workId) throw new Error("当前页面作品 ID 与输入 URL 不一致，已停止分析");
    return { snapshot, sourceUrl };
  } finally {
    if (createdSession && !options.keepTab) {
      try {
        await command(baseUrl, token, browser.browserId, "close_session", { session });
      } catch (error) {
        process.stderr.write(`警告：无法关闭本次任务标签组：${safeErrorMessage(error)}\n`);
      }
    }
  }
}

async function runMock(options) {
  if (!options.mock) throw new UsageError("--mock 需要快照文件路径");
  const payload = JSON.parse(await readFile(resolve(options.mock), "utf8"));
  const snapshot = normalizeSnapshot(payload);
  const pageUrl = assertDouyinWorkUrl(snapshot.url, "快照 URL").url;
  const sourceUrl = assertDouyinWorkUrl(options.url || pageUrl, "输入 URL").url;
  const gate = detectAccessGate(`${snapshot.title}\n${snapshot.text}`);
  if (gate) throw new Error("Mock 快照包含登录或安全验证提示，按真实流程停止分析");
  return { snapshot, sourceUrl };
}

async function runAnalyze(options) {
  await clearReports(options.output);
  try {
    const { snapshot, sourceUrl } = options.mock ? await runMock(options) : await runLive(options);
    const report = buildReport(snapshot, sourceUrl);
    const outputDir = await writeReports(report, options.output);
    return { outputDir, report };
  } catch (error) {
    await clearReports(options.output);
    throw error;
  }
}

async function selfTest() {
  const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
  const outputDir = await mkdtemp(join(tmpdir(), "douyin-work-analyzer-"));
  const successDir = join(outputDir, "success");
  const scriptPath = join(projectRoot, "scripts", "douyin-work-analyzer.mjs");
  const runCli = (args, env = {}) => spawnSync(process.execPath, [scriptPath, ...args], { cwd: projectRoot, encoding: "utf8", env: { ...process.env, EASY_WEBBRIDGE_TOKEN: "", ...env } });
  const reportFiles = REPORT_FILES;
  const assertNoSensitiveData = (value, label) => {
    if (/(token|cookie|browserId|fake-secret-value|fixture-session-9988)/i.test(String(value))) throw new Error(`${label} 包含敏感字段或测试值`);
  };
  try {
    const requiredFiles = [
      "SKILL.md", "manifest.yaml", "package.json", "README.md", "README.en.md", "LICENSE",
      "agents/openai.yaml", "assets/icon-512.png", "fixtures/sample-snapshot.json",
      "fixtures/failure-login-gate.json", "fixtures/failure-empty-snapshot.json", "references/source.md",
    ];
    for (const file of requiredFiles) await readFile(join(projectRoot, file));
    const packageJson = JSON.parse(await readFile(join(projectRoot, "package.json"), "utf8"));
    if (packageJson.engines?.node !== ">=20" || packageJson.scripts?.test !== "node scripts/douyin-work-analyzer.mjs self-test") throw new Error("package.json 契约断言失败");
    const skillText = await readFile(join(projectRoot, "SKILL.md"), "utf8");
    const frontmatter = skillText.match(/^---\n([\s\S]*?)\n---/u)?.[1] || "";
    if (!/^name:\s*douyin-work-analyzer$/m.test(frontmatter) || !/^description:\s*\S/m.test(frontmatter)) throw new Error("SKILL.md frontmatter 断言失败");
    const agentText = await readFile(join(projectRoot, "agents/openai.yaml"), "utf8");
    if (!agentText.includes("$douyin-work-analyzer") || (agentText.match(/\.\/assets\/icon-512\.png/g) || []).length !== 2) throw new Error("agents/openai.yaml 契约断言失败");
    const icon = await readFile(join(projectRoot, "assets/icon-512.png"));
    if (icon.length < 1024 || icon.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a" || icon.readUInt32BE(16) !== 512 || icon.readUInt32BE(20) !== 512) throw new Error("512px PNG 图标断言失败");

    const success = runCli(["analyze", "--mock", "./fixtures/sample-snapshot.json", "--output", successDir]);
    if (success.status !== 0) throw new Error(`成功样例退出码断言失败: ${safeErrorMessage(success.stderr)}`);
    const jsonPath = join(successDir, reportFiles[0]);
    const mdPath = join(successDir, reportFiles[1]);
    const report = JSON.parse(await readFile(jsonPath, "utf8"));
    const markdown = await readFile(mdPath, "utf8");
    if (report.schemaVersion !== "1.0" || report.kind !== "douyin-work-analysis") throw new Error("JSON 顶层结构断言失败");
    if (report.work.title !== "三步看懂 AI 工具，今天把复杂流程讲清楚" || report.work.author !== "示例创作者") throw new Error("标题或作者解析断言失败");
    if (!report.work.description?.includes("为什么你的内容总是没人看")) throw new Error("作品文案解析断言失败");
    if (report.work.visibleMetrics["点赞"] !== 12_000 || report.work.visibleMetrics["评论"] !== 38 || report.work.visibleMetrics["收藏"] !== 560 || report.work.visibleMetrics["分享"] !== 9) throw new Error("互动指标解析断言失败");
    if (!report.work.hashtags.includes("#AI工具") || !report.work.hashtags.includes("#内容创作")) throw new Error("话题解析断言失败");
    for (const factEvidence of [report.work.title, "作者：示例创作者", report.work.description, ...report.evidence.metricLines]) {
      if (factEvidence && !report.evidence.visibleTextSample.includes(factEvidence) && !report.evidence.metricLines.includes(factEvidence)) {
        throw new Error(`事实字段缺少可独立核对的证据: ${factEvidence}`);
      }
    }
    if (report.analysis.structure.find((item) => item.section === "结尾行动")?.evidence !== null) throw new Error("互动指标被误判为结尾行动");
    for (const heading of ["来源与采集时间", "作品可见信息", "开头钩子与主题", "可见内容结构", "可见互动信息", "亮点", "问题与未确认项", "可借鉴方向", "页面证据摘录", "限制与合规说明"]) {
      if (!markdown.includes(`## ${heading}`)) throw new Error(`Markdown 缺少章节: ${heading}`);
    }
    if (!markdown.includes("- 作品文案：先问一个问题")) throw new Error("Markdown 未正确标注作品文案");
    assertNoSensitiveData(JSON.stringify(report), "JSON 报告");
    assertNoSensitiveData(markdown, "Markdown 报告");
    assertNoSensitiveData(safeErrorMessage(new Error("token=fake-secret-value cookie=fake-secret-value browserId=fake-secret-value session=fixture-session-9988")), "错误清理函数");

    const sensitiveFixture = join(outputDir, "sensitive-fields.json");
    await writeFile(sensitiveFixture, JSON.stringify({
      title: "安全的作品标题 - 抖音",
      url: "https://www.douyin.com/video/1000000000000000003?token=url-secret&safe=1",
      text: "https://www.douyin.com/video/1000000000000000003\n安全的作品标题\n作者：安全作者\n这是用于验证字段清理的可见文案\n点赞 1\nToken: title-secret",
      interactive: [{ visible: true, href: "https://www.douyin.com/video/1000000000000000003", text: "安全的作品标题" }],
    }), "utf8");
    const sensitiveDir = join(outputDir, "sensitive-fields");
    const sensitiveRun = runCli(["analyze", "--url", "https://www.douyin.com/video/1000000000000000003?token=input-secret&safe=1", "--mock", sensitiveFixture, "--output", sensitiveDir]);
    if (sensitiveRun.status !== 0) throw new Error("敏感字段清理样例运行失败");
    const sensitiveReport = await readFile(join(sensitiveDir, reportFiles[0]), "utf8");
    const sensitiveMarkdown = await readFile(join(sensitiveDir, reportFiles[1]), "utf8");
    assertNoSensitiveData(sensitiveReport, "敏感字段 JSON 报告");
    assertNoSensitiveData(sensitiveMarkdown, "敏感字段 Markdown 报告");

    for (const [fixture, expectedText] of [["failure-login-gate.json", "停止分析"], ["failure-empty-snapshot.json", "没有可见标题或正文"]]) {
      const failureDir = join(outputDir, fixture.replace(/\.json$/, ""));
      const failure = runCli(["analyze", "--mock", `./fixtures/${fixture}`, "--output", failureDir]);
      if (failure.status !== 1 || !failure.stderr.includes(expectedText)) throw new Error(`${fixture} 失败行为断言失败`);
      assertNoSensitiveData(failure.stderr, `${fixture} 错误输出`);
      for (const file of reportFiles) {
        try {
          await readFile(join(failureDir, file));
          throw new Error(`${fixture} 不应生成成功报告`);
        } catch (error) {
          if (error.code !== "ENOENT") throw error;
        }
      }
    }

    const staleFailure = runCli(["analyze", "--mock", "./fixtures/failure-login-gate.json", "--output", successDir]);
    if (staleFailure.status !== 1) throw new Error("同目录失败重跑退出码断言失败");
    for (const file of reportFiles) {
      try {
        await readFile(join(successDir, file));
        throw new Error("同目录失败重跑后保留了旧成功报告");
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
      }
    }

    for (const invalidUrl of ["not-a-url", "https://example.com/video/1234567890", "https://www.douyin.com/", "https://www.douyin.com/search/test"]) {
      const failure = runCli(["analyze", "--url", invalidUrl, "--output", join(outputDir, "invalid")]);
      if (failure.status !== 2) throw new Error(`非法 URL 退出码断言失败: ${invalidUrl}`);
      assertNoSensitiveData(failure.stderr, "非法 URL 错误输出");
    }

    for (const args of [["analyze", "--foo", "bar"], ["analyze", "--browser", "fixture-browser", "--url", "https://www.douyin.com/video/1000000000000000000"]]) {
      const failure = runCli(args);
      if (failure.status !== 2 || !failure.stderr.includes("无法识别参数")) throw new Error("未知参数未按用法错误拒绝");
    }

    const loginOnlyFixture = join(outputDir, "login-only.json");
    await writeFile(loginOnlyFixture, JSON.stringify({
      title: "登录抖音",
      url: "https://www.douyin.com/video/1000000000000000005",
      text: "登录\n手机号进入\n获取验证码",
      interactive: [],
    }), "utf8");
    const loginOnly = runCli(["analyze", "--mock", loginOnlyFixture, "--output", join(outputDir, "login-only")]);
    if (loginOnly.status !== 1 || !loginOnly.stderr.includes("停止分析")) throw new Error("明确登录页面未被门禁拦截");

    const pollutedFixture = join(outputDir, "polluted-feed.json");
    await writeFile(pollutedFixture, JSON.stringify({
      title: "目标作品标题 - 抖音",
      url: "https://www.douyin.com/video/1000000000000000006",
      text: [
        "推荐作品标题", "作者：推荐作者", "#错误话题", "点赞 9.9万", "推荐视频",
        "https://www.douyin.com/video/1000000000000000006", "目标作品标题", "作者：目标作者",
        "这是目标作品的可见文案内容", "#正确话题", "点赞 88", "评论 7", "相关推荐", "另一个作品 #污染话题 点赞 8.8万",
      ].join("\n"),
      interactive: [
        { visible: true, href: "https://www.douyin.com/user/recommended", text: "推荐链接作者" },
        { visible: true, href: "https://www.douyin.com/video/1000000000000000006", text: "目标作品标题" },
      ],
    }), "utf8");
    const pollutedDir = join(outputDir, "polluted-feed");
    const pollutedRun = runCli(["analyze", "--mock", pollutedFixture, "--output", pollutedDir]);
    if (pollutedRun.status !== 0) throw new Error(`推荐流边界样例失败: ${safeErrorMessage(pollutedRun.stderr)}`);
    const pollutedReport = JSON.parse(await readFile(join(pollutedDir, reportFiles[0]), "utf8"));
    if (pollutedReport.work.author !== "目标作者" || pollutedReport.work.visibleMetrics["点赞"] !== 88 || pollutedReport.work.hashtags.includes("#错误话题") || pollutedReport.work.hashtags.includes("#污染话题")) {
      throw new Error("目标作品边界未隔离推荐流内容");
    }

    const titlelessFixture = join(outputDir, "titleless-real-shape.json");
    await writeFile(titlelessFixture, JSON.stringify({
      title: "",
      url: "https://www.douyin.com/video/1000000000000000007",
      text: [
        "首页", "推荐", "登录", "00:00 / 08:55", "作者声明：个人观点，仅供参考", "章节要点",
        "小白入门工具，快速选出适合自己的方案 #工具学习 #入门教程", "1408", "55", "1454", "180",
        "发布时间：2026-08-25 18:38", "全部评论", "请先登录后发表评论", "大家都在搜：", "无关推荐内容",
      ].join("\n"),
      interactive: [
        { visible: true, href: "https://www.douyin.com/video/1000000000000000007", text: "客户端" },
        { visible: true, href: "https://www.douyin.com/search/工具学习", text: "#工具学习" },
        { visible: true, href: "https://www.douyin.com/search/入门教程", text: "#入门教程" },
        { visible: true, href: "https://www.douyin.com/user/example", text: "示例作者" },
      ],
    }), "utf8");
    const titlelessDir = join(outputDir, "titleless-real-shape");
    const titlelessRun = runCli(["analyze", "--mock", titlelessFixture, "--output", titlelessDir]);
    if (titlelessRun.status !== 0) throw new Error(`无页面标题真实形态样例失败: ${safeErrorMessage(titlelessRun.stderr)}`);
    const titlelessReport = JSON.parse(await readFile(join(titlelessDir, reportFiles[0]), "utf8"));
    if (!titlelessReport.work.title?.startsWith("小白入门工具") || titlelessReport.work.author !== null) throw new Error("无页面标题真实形态解析失败");
    if (titlelessReport.work.description !== null || titlelessReport.analysis.hook.text !== null) throw new Error("作者声明或章节摘要被误写为作品文案或钩子");
    if (JSON.stringify(titlelessReport.evidence).includes("示例作者")) throw new Error("全局用户链接污染了目标作品证据");

    const summaryFixture = join(outputDir, "summary-assistance.json");
    const summaryText = "选择AI工具需考虑能否完成工作、关键任务结果是否满足要求、投产比是否高。";
    await writeFile(summaryFixture, JSON.stringify({
      title: "小白入门AI，如何快速选出最适合自己的AI工具 - 抖音",
      url: "https://www.douyin.com/video/1000000000000000008",
      text: [
        "08:20", "总结", summaryText,
        "小白入门AI，如何快速选出最适合自己的AI工具 #AI工具 #AI学习 #AI教程",
        "1409", "55", "1455", "180", "发布时间：2026-08-25 18:38",
      ].join("\n"),
      interactive: [
        { visible: true, href: "https://www.douyin.com/user/recommended-first", text: "推荐作者" },
        { visible: true, href: "https://www.douyin.com/video/1000000000000000008", text: "小白入门AI，如何快速选出最适合自己的AI工具" },
        { visible: true, href: "https://www.douyin.com/user/target-but-unbound", text: "页面作者" },
      ],
    }), "utf8");
    const summaryDir = join(outputDir, "summary-assistance");
    const summaryRun = runCli(["analyze", "--mock", summaryFixture, "--output", summaryDir]);
    if (summaryRun.status !== 0) throw new Error(`页面辅助摘要样例失败: ${safeErrorMessage(summaryRun.stderr)}`);
    const summaryReport = JSON.parse(await readFile(join(summaryDir, reportFiles[0]), "utf8"));
    if (summaryReport.work.description !== null || summaryReport.analysis.hook.text !== null) throw new Error("页面辅助摘要被误写为作品文案或开头钩子");
    if (summaryReport.work.author !== null) throw new Error("未绑定目标区域的用户链接被误写为作者");
    if (JSON.stringify(summaryReport.evidence).includes(summaryText) || JSON.stringify(summaryReport.evidence).includes("推荐作者") || JSON.stringify(summaryReport.evidence).includes("页面作者")) {
      throw new Error("页面辅助摘要或交互节点污染了保留证据");
    }

    const cleanupActions = [];
    try {
      await runLive({ url: "https://www.douyin.com/video/1000000000000000004", waitMs: 300 }, {
        readBridgeToken: async () => "fixture-credential",
        bridgeRequest: async (_baseUrl, path) => path === "/health" ? { ok: true } : { browsers: [{ browserId: "fixture-browser", online: true }] },
        bridgeCommand: async (_baseUrl, _token, _browserId, action) => {
          cleanupActions.push(action);
          if (action === "navigate") return {};
          if (action === "close_session") return { ok: true };
          throw new Error("unexpected action");
        },
        sleep: async () => {},
      });
      throw new Error("缺失 tabId 的导航应失败");
    } catch (error) {
      if (!String(error.message).includes("没有返回 tabId")) throw error;
    }
    if (cleanupActions.join(",") !== "navigate,close_session") throw new Error("导航异常后未清理任务 session");

    const secondSuccess = runCli(["analyze", "--mock", "./fixtures/sample-snapshot.json", "--output", successDir]);
    if (secondSuccess.status !== 0) throw new Error("重复运行断言失败");
    process.stdout.write(JSON.stringify({ ok: true, tests: 27, files: reportFiles }, null, 2) + "\n");
  } finally {
    await rm(outputDir, { recursive: true, force: true });
  }
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.command === "help") {
    process.stdout.write(HELP);
    return;
  }
  if (options.command === "self-test") {
    await selfTest();
    return;
  }
  if (options.command !== "analyze") throw new UsageError(`无法识别命令: ${options.command}`);
  const result = await runAnalyze(options);
  process.stdout.write(JSON.stringify({ ok: true, outputDir: result.outputDir, files: ["douyin-work-analysis.json", "douyin-work-analysis.md"] }, null, 2) + "\n");
}

main().catch((error) => {
  const status = error instanceof UsageError ? 2 : 1;
  process.stderr.write(`错误：${safeErrorMessage(error)}\n`);
  process.exitCode = status;
});
