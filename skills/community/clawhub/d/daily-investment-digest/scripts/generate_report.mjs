#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.dirname(SCRIPT_DIR);

function usage(exitCode = 2) {
  console.error(
    [
      "Usage: generate_report.mjs --input-json <path|-> [--output <path>] [--top-n 0] [--stdout]",
      "",
      "Options:",
      "  --input-json <path|-> Input normalized JSON file, or '-' for stdin (required)",
      "  --output <path>       Disabled (report is always printed to stdout)",
      "  --top-n <n>           Max events to display (default: 0=all, bounds: 0-500)",
      "  --stdout              Kept for compatibility (stdout is always enabled)",
      "  -h, --help            Show this help",
    ].join("\n")
  );
  process.exit(exitCode);
}

function parseIntOrDefault(value, defaultValue) {
  const num = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(num) ? num : defaultValue;
}

function localDateISO() {
  const now = new Date();
  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function clamp(value, low, high) {
  return Math.max(low, Math.min(value, high));
}

function resolvePath(value, fallbackAbsolutePath = "") {
  if (!value) return fallbackAbsolutePath;
  if (path.isAbsolute(value)) return value;
  return path.join(SKILL_DIR, value);
}

function parseArgs(argv) {
  const options = {
    inputJson: "",
    topN: 0,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") usage(0);

    if (arg === "--input-json") {
      options.inputJson = argv[i + 1] ?? "";
      i += 1;
      continue;
    }
    if (arg === "--output") {
      console.error("--output is disabled. This script is stdout-only.");
      process.exit(2);
    }
    if (arg === "--top-n") {
      options.topN = parseIntOrDefault(argv[i + 1], options.topN);
      i += 1;
      continue;
    }
    if (arg === "--stdout") {
      continue;
    }

    console.error(`Unknown arg: ${arg}`);
    usage();
  }

  if (!options.inputJson) usage();
  options.topN = clamp(options.topN, 0, 500);
  return options;
}

function parseDateTime(value) {
  if (!value) return 0;
  const ts = new Date(String(value).replace(" ", "T")).getTime();
  return Number.isFinite(ts) ? ts : 0;
}

function normalizeTags(value) {
  if (!Array.isArray(value)) return [];
  const seen = new Set();
  const tags = [];
  for (const item of value) {
    const tag = typeof item === "string" ? item : item?.tagName;
    const name = String(tag ?? "").trim();
    if (!name || seen.has(name)) continue;
    seen.add(name);
    tags.push(name);
  }
  return tags;
}

function extractRounds(text) {
  const source = String(text ?? "");
  const roundRegex =
    /(Pre-?A\+?轮|Pre-?B\+?轮|Pre-?C\+?轮|A\+\+轮|A\+轮|A轮|B\+\+轮|B\+轮|B轮|C\+\+轮|C\+轮|C轮|D\+\+轮|D\+轮|D轮|E轮|F轮|天使轮|种子轮|战略投资|股权融资)/g;
  const rounds = [];
  const seen = new Set();
  for (const match of source.matchAll(roundRegex)) {
    const value = String(match[1] ?? "").trim();
    if (!value || seen.has(value)) continue;
    seen.add(value);
    rounds.push(value);
  }
  return rounds;
}

function splitEntityList(text) {
  return String(text ?? "")
    .split(/[、,，\/]+/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function extractInvestors(title, brief) {
  const fromBrief = [];
  const patterns = [
    /由([^，。；]+?)(领投|投资|参投|联合投资)/,
    /投资方(?:为|是)([^，。；]+)/,
    /获([^，。；]+?)投资/,
    /([^，。；]+?)领投/,
  ];

  for (const pattern of patterns) {
    const m = String(brief ?? "").match(pattern);
    if (m?.[1]) fromBrief.push(...splitEntityList(m[1]));
  }

  const titleInvestor = String(title ?? "").match(/^(.+?)(?:战略)?投资/);
  if (titleInvestor?.[1] && !String(title ?? "").includes("获")) {
    fromBrief.push(...splitEntityList(titleInvestor[1]));
  }

  const rounds = extractRounds(`${title} ${brief}`);
  const cleaned = [];
  const seen = new Set();
  for (const item of fromBrief) {
    let value = item;
    for (const round of rounds) value = value.replaceAll(round, "");
    value = value
      .replace(/^由/, "")
      .replace(/^(多家|机构联合)$/g, "")
      .trim();
    if (!value || seen.has(value)) continue;
    seen.add(value);
    cleaned.push(value);
  }
  return cleaned;
}

function extractCompanyName(title, brief) {
  const titleText = String(title ?? "").trim();
  if (!titleText) return "未披露";

  if (titleText.includes("获")) {
    const left = titleText.split("获")[0]?.trim();
    if (left) return left;
  }

  if (titleText.includes("战略投资")) {
    const right = titleText.split("战略投资")[1]?.trim();
    if (right) return right.replace(/(Pre-?[A-Z]\+?轮|[A-F]\+?轮|天使轮|种子轮)$/, "").trim() || right;
  }

  if (titleText.includes("投资")) {
    const right = titleText.split("投资")[1]?.trim();
    if (right) {
      return right.replace(/(Pre-?[A-Z]\+?轮|[A-F]\+?轮|天使轮|种子轮)$/, "").trim() || right;
    }
  }

  const m = String(brief ?? "").match(/(?:服务提供商|研发商|公司|企业)([A-Za-z0-9\u4e00-\u9fa5·（）()\-]+?)(?:宣布|完成|获)/);
  if (m?.[1]) return m[1].trim();
  return titleText;
}

function enrichEvent(event) {
  const title = String(event?.postTitle ?? event?.title ?? "").trim();
  const brief = String(event?.brief ?? event?.summary ?? "").trim();
  const createdAt = String(event?.createdAt ?? event?.raw_created_at ?? "").trim();
  const originalLink = String(event?.originalLink ?? event?.source_url ?? "").trim();
  const tags = normalizeTags(event?.tags ?? event?.industry_tags ?? []);
  const industry = String(tags[0] ?? "").trim() || "未分类";
  return {
    title,
    brief,
    createdAt,
    originalLink,
    tags,
    industry,
    rounds: extractRounds(`${title} ${brief}`),
    investors: extractInvestors(title, brief),
    companyName: extractCompanyName(title, brief),
  };
}

function summarizeEvents(events) {
  const industryCounts = new Map();
  const roundCounts = new Map();
  for (const event of events) {
    const industry = String(event.industry ?? "").trim() || "未分类";
    industryCounts.set(industry, (industryCounts.get(industry) ?? 0) + 1);
    const rounds = Array.isArray(event.rounds) && event.rounds.length > 0 ? event.rounds : ["未披露"];
    for (const round of rounds) {
      const key = String(round ?? "").trim() || "未披露";
      roundCounts.set(key, (roundCounts.get(key) ?? 0) + 1);
    }
  }
  return { industryCounts, roundCounts };
}

function formatDistribution(countMap) {
  return [...countMap.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => `${name}（${count}起）`)
    .join("、");
}

function cleanCell(value, maxLen = 90) {
  const text = String(value ?? "")
    .replace(/\s+/g, " ")
    .trim();
  if (text.length <= maxLen) return text || "-";
  return `${text.slice(0, maxLen)}...`;
}

function groupEventsByIndustry(events) {
  const groups = new Map();
  for (const event of events) {
    const industry = String(event.industry ?? "").trim() || "未分类";
    if (!groups.has(industry)) groups.set(industry, []);
    groups.get(industry).push(event);
  }
  return [...groups.entries()].sort((a, b) => b[1].length - a[1].length);
}

function buildIndustryGroupedLines(events) {
  const lines = [];
  if (events.length === 0) {
    lines.push("暂无融资事件。");
    return lines;
  }

  const groups = groupEventsByIndustry(events);
  let index = 1;
  for (const [industry, group] of groups) {
    lines.push(`### 行业：${industry}（${group.length}起）`);
    lines.push("");
    for (const event of group) {
      const companyName = cleanCell(event.companyName || "未披露", 50);
      const rounds = Array.isArray(event.rounds) && event.rounds.length > 0
        ? cleanCell(event.rounds.join("、"), 40)
        : "未披露";
      const investors = Array.isArray(event.investors) && event.investors.length > 0
        ? cleanCell(event.investors.join("、"), 60)
        : "未披露";
      const intro = cleanCell(event.brief || "-", 110);
      const link = String(event.originalLink ?? "").trim();
      const linkCell = link ? `[查看原文](${link})` : "-";

      lines.push(`${index}. 公司简称：${companyName}`);
      lines.push(`轮次：${rounds}`);
      lines.push(`投资方：${investors}`);
      lines.push(`事件摘要：${intro}`);
      lines.push(`来源链接：${linkCell}`);
      lines.push("");
      index += 1;
    }
    lines.push("");
  }
  return lines;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }
  return Buffer.concat(chunks).toString("utf-8");
}

function formatCnDate(reportDate) {
  const match = String(reportDate).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) return `${reportDate}投融资日报`;
  const year = Number.parseInt(match[1], 10);
  const month = Number.parseInt(match[2], 10);
  const day = Number.parseInt(match[3], 10);
  return `${year}年${month}月${day}日投融资日报`;
}

function formatRangeTitle(reportDate, rangeStartDate, recentDays) {
  if (recentDays <= 1 || !rangeStartDate) return formatCnDate(reportDate);
  return `最近${recentDays}天投融资汇总（${rangeStartDate} 至 ${reportDate}）`;
}

function buildRangeSummary(reportDate, rangeStartDate, recentDays) {
  if (recentDays <= 1 || !rangeStartDate) return `统计日期：${reportDate}`;
  return `统计区间：${rangeStartDate} 至 ${reportDate}（最近${recentDays}天）`;
}

function buildReportText(reportDate, rangeStartDate, recentDays, allEvents, renderedEvents) {
  const lines = [];
  lines.push(formatRangeTitle(reportDate, rangeStartDate, recentDays));
  lines.push("核心数据概览");
  lines.push(buildRangeSummary(reportDate, rangeStartDate, recentDays));
  lines.push(`融资事件总数：${allEvents.length}起`);

  const { industryCounts, roundCounts } = summarizeEvents(allEvents);
  lines.push(`涉及行业分布：${formatDistribution(industryCounts) || "暂无"}`);
  lines.push(`融资轮次分布：${formatDistribution(roundCounts) || "暂无"}`);
  lines.push("注：部分事件涉及多轮次或多投资方");
  lines.push(`展示条数：${renderedEvents.length}/${allEvents.length}`);
  lines.push("");
  lines.push("融资事件按行业分类");
  lines.push("");
  lines.push(...buildIndustryGroupedLines(renderedEvents));
  if (renderedEvents.length < allEvents.length) {
    lines.push("");
    lines.push("说明：当前为简表模式。需要全量请使用 `--top-n 0`。");
  }
  return `${lines.join("\n")}\n`;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const inputPath = options.inputJson === "-" ? "-" : resolvePath(options.inputJson);
  const raw = inputPath === "-" ? await readStdin() : await fs.readFile(inputPath, "utf-8");
  const payload = JSON.parse(raw);

  const meta = payload?.meta ?? {};
  const reportDate = String(meta.report_date ?? "").trim() || localDateISO();
  const rangeStartDate = String(meta.range_start_date ?? "").trim();
  const recentDays = clamp(parseIntOrDefault(meta.recent_days, 1), 1, 7);

  const events = Array.isArray(payload?.events)
    ? payload.events.filter((x) => x && typeof x === "object").map((x) => enrichEvent(x))
    : [];
  events.sort((a, b) => parseDateTime(b.createdAt) - parseDateTime(a.createdAt));

  const renderedEvents = options.topN > 0 ? events.slice(0, options.topN) : events;

  const reportText = buildReportText(reportDate, rangeStartDate, recentDays, events, renderedEvents);

  process.stdout.write(reportText);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});
