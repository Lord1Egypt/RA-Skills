#!/usr/bin/env node
/**
 * 解析 feedback-log.md，按平台与 Issue 关键词汇总，输出规则候选提示。
 * 运行：node src/feedback-analyze.js [path/to/feedback-log.md]
 */
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

function parseFeedbackLog(content) {
  const entries = [];
  const blocks = content.split(/^## /m).slice(1);
  for (const block of blocks) {
    const lines = block.split("\n");
    const dateLine = lines[0]?.trim() ?? "";
    let platform = "";
    let issue = "";
    let ruleCandidate = "";
    for (const line of lines) {
      if (line.includes("**Platform**:")) platform = line.replace(/.*\*\*Platform\*\*:\s*/, "").trim();
      if (line.includes("**Issue**:")) issue = line.replace(/.*\*\*Issue\*\*:\s*/, "").trim();
      if (line.includes("**Rule candidate**:"))
        ruleCandidate = line.replace(/.*\*\*Rule candidate\*\*:\s*/, "").trim();
    }
    if (issue || ruleCandidate) entries.push({ dateLine, platform, issue, ruleCandidate });
  }
  return entries;
}

function main() {
  const args = process.argv.slice(2);
  const path = args[0] ? resolve(args[0]) : resolve(process.cwd(), "feedback-log.md");
  if (!existsSync(path)) {
    console.error(`File not found: ${path}`);
    process.exit(1);
  }
  const content = readFileSync(path, "utf8");
  const entries = parseFeedbackLog(content);

  const byPlatform = {};
  const issues = [];
  const rules = [];

  for (const e of entries) {
    const p = e.platform || "unknown";
    byPlatform[p] = (byPlatform[p] ?? 0) + 1;
    if (e.issue) issues.push(e.issue);
    if (e.ruleCandidate) rules.push(e.ruleCandidate);
  }

  const keywords = new Map();
  for (const i of issues) {
    for (const w of i.split(/[\s，,。.]+/).filter((x) => x.length > 1)) {
      keywords.set(w, (keywords.get(w) ?? 0) + 1);
    }
  }
  const topKw = [...keywords.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15);

  const out = {
    totalEntries: entries.length,
    byPlatform,
    topIssueKeywords: Object.fromEntries(topKw),
    ruleCandidates: [...new Set(rules)],
    summary:
      entries.length === 0
        ? "暂无结构化条目（确保使用 `## YYYY-MM-DD HH:MM` 分段）。"
        : `共 ${entries.length} 条反馈；可按 Rule candidate 合并为 Skill 补充规则。`,
  };

  console.log(JSON.stringify(out, null, 2));
}

main();
