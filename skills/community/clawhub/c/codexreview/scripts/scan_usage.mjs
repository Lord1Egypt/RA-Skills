#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { scanCodex } from "./adapters/codex.mjs";
import { formatUserError, userError } from "./core/diagnostics.mjs";
import { groupUsage, normalizeRules } from "./core/grouping.mjs";
import { addToken, emptyToken } from "./core/report-schema.mjs";

const args = parseArgs(process.argv.slice(2));

if (args.help) {
  printHelp();
  process.exit(0);
}

try {
  const days = parseDays(args.days);
  const workspace = path.resolve(args.workspace || process.cwd());
  const codexHome = path.resolve(args.codexHome || path.join(os.homedir(), ".codex"));
  const output = path.resolve(args.output || path.join(os.tmpdir(), "codex_review_scan.json"));
  const config = readConfig(args.config ? path.resolve(args.config) : path.join(workspace, ".codex-review.json"));
  const until = new Date();
  const since = new Date(until.getTime() - days * 24 * 60 * 60 * 1000);
  const diagnostics = [];
  const scanned = scanCodex({ codexHome, workspace, since, until, outputFile: output, diagnostics });
  const projects = groupUsage({
    sessions: scanned.sessions,
    artifacts: scanned.artifacts,
    config: { projectRules: normalizeRules(config.projectRules) },
  });
  if (projects.some((project) => project.confidence === "low")) {
    diagnostics.push({
      code: "low-confidence-grouping",
      level: "info",
      message: "部分任务没有识别到稳定项目名，已使用中性分类。",
      action: "可以在工作区添加 .codex-review.json，设置自己的项目归并规则。",
    });
  }

  const totalToken = emptyToken();
  let totalMinutes = 0;
  for (const project of projects) {
    totalMinutes += Number(project.minutes || 0);
    addToken(totalToken, project.token);
  }

  const mainSessions = scanned.sessions.filter((item) => !item.isAuxiliary && !item.isSynthetic);
  const report = {
    schemaVersion: 2,
    platform: "codex",
    generatedAt: new Date().toISOString(),
    range: { days, since: since.toISOString(), until: until.toISOString() },
    workspace: path.basename(workspace) || "本地工作区",
    summary: {
      mainSessionCount: mainSessions.length,
      auxiliarySessionCount: scanned.sessions.filter((item) => item.isAuxiliary).length,
      ignoredSyntheticSessionCount: scanned.sessions.filter((item) => item.isSynthetic).length,
      projectCount: projects.length,
      artifactCount: scanned.artifacts.length,
      totalMinutes,
      totalToken,
      hasWeeklyAutomation: scanned.environment.hasWeeklyAutomation,
    },
    projects,
    diagnostics,
    environment: scanned.environment,
  };

  writeJson(output, report);
  console.log(JSON.stringify({
    output,
    schemaVersion: report.schemaVersion,
    mainSessionCount: report.summary.mainSessionCount,
    auxiliarySessionCount: report.summary.auxiliarySessionCount,
    projectCount: report.summary.projectCount,
    artifactCount: report.summary.artifactCount,
    diagnosticCount: diagnostics.length,
    hasWeeklyAutomation: report.summary.hasWeeklyAutomation,
  }, null, 2));
} catch (error) {
  console.error(formatUserError(error, "无法完成 Codex 使用扫描"));
  process.exit(1);
}

function parseArgs(argv) {
  const out = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) out[key] = true;
    else {
      out[key] = next;
      index += 1;
    }
  }
  return out;
}

function parseDays(value) {
  const days = Number(value || 7);
  if (!Number.isFinite(days) || days <= 0 || days > 3650) {
    throw userError("时间范围无效", "请把 --days 设置为 1 到 3650 之间的数字。", String(value || ""));
  }
  return days;
}

function readConfig(file) {
  if (!fs.existsSync(file)) return {};
  try {
    const config = JSON.parse(fs.readFileSync(file, "utf8"));
    if (config.projectRules && !Array.isArray(config.projectRules)) {
      throw new Error("projectRules must be an array");
    }
    return config;
  } catch (error) {
    throw userError(
      "自定义配置文件无法读取",
      "请检查 JSON 格式，或暂时移走该配置文件后重试。",
      `${file}: ${error.message}`,
    );
  }
}

function writeJson(file, value) {
  try {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(value, null, 2));
  } catch (error) {
    throw userError("扫描结果无法写入", "请换一个有写入权限的 --output 路径。", `${file}: ${error.message}`);
  }
}

function printHelp() {
  console.log(`Codex Review 扫描工具

用法：
  node scripts/scan_usage.mjs [选项]

选项：
  --workspace <目录>   要扫描产物的工作区，默认当前目录
  --days <天数>        时间范围，默认 7
  --codexHome <目录>   Codex 数据目录，默认 ~/.codex
  --config <文件>      可选的项目归并配置 JSON
  --output <文件>      扫描结果，默认写入系统临时目录
  --help               查看帮助
`);
}
