import fs from "node:fs";
import path from "node:path";
import { createDiagnostic, redactHome, userError } from "../core/diagnostics.mjs";
import { emptyToken, maxToken } from "../core/report-schema.mjs";

const ARTIFACT_EXTENSIONS = new Set([
  ".md", ".html", ".xlsx", ".xls", ".csv", ".png", ".jpg", ".jpeg",
  ".webp", ".zip", ".pdf", ".pptx", ".docx", ".json", ".mjs", ".js",
  ".ts", ".tsx", ".jsx", ".py", ".sh", ".toml", ".yaml", ".yml",
]);

const SKIP_DIRECTORIES = new Set([
  ".git", "node_modules", "data", "reports", ".cache", ".next", "dist", "build",
]);

export function scanCodex({ codexHome, workspace, since, until, outputFile, diagnostics }) {
  ensureDirectory(codexHome, "没有找到 Codex 数据目录", "请确认 Codex 已安装并至少使用过一次，或通过 --codexHome 指定正确目录。");
  ensureDirectory(workspace, "工作区路径不存在", "请通过 --workspace 指定一个存在的项目或工作区目录。");

  const sessionRoots = [path.join(codexHome, "sessions"), path.join(codexHome, "archived_sessions")];
  const sessionFiles = sessionRoots.flatMap((root) => walk(root, {
    maxDepth: 8,
    filter: (file) => file.endsWith(".jsonl") && recent(file, since),
    diagnostics,
    label: "Codex 会话目录",
  }));
  const sessions = [];
  let malformedLineCount = 0;
  let sessionsWithoutToken = 0;

  for (const file of sessionFiles) {
    const parsed = parseJsonl(file);
    malformedLineCount += parsed.malformed;
    if (!parsed.items.length) continue;
    const meta = parsed.items.find((item) => item.type === "session_meta")?.payload || {};
    const scopedItems = parsed.items.filter((item) => {
      if (!item.timestamp) return item.type === "session_meta";
      const time = new Date(item.timestamp).getTime();
      return Number.isFinite(time) && time >= since.getTime() && time <= until.getTime();
    });
    const times = scopedItems
      .map((item) => item.timestamp)
      .filter(Boolean)
      .map((value) => new Date(value).getTime())
      .filter(Number.isFinite);
    if (!times.length) continue;

    const token = tokenUsageForRange(parsed.items, since, until);
    const userMessages = [];
    for (const item of scopedItems) {
      if (item.type === "event_msg" && item.payload?.type === "user_message" && item.payload.message) {
        const clean = cleanUserMessage(item.payload.message);
        if (clean) userMessages.push(clean);
      }
      if (item.type === "response_item" && item.payload?.type === "message" && item.payload.role === "user") {
        const clean = cleanUserMessage(textOf(item.payload.content));
        if (clean) userMessages.push(clean);
      }
    }
    if (!token.total_tokens) sessionsWithoutToken += 1;
    const start = Math.min(...times);
    const end = Math.max(...times);
    sessions.push({
      id: meta.id || path.basename(file, ".jsonl"),
      cwd: meta.cwd || "",
      title: meta.thread_name || meta.threadName || meta.title || "",
      isAuxiliary: meta.thread_source === "subagent" || Boolean(meta.source?.subagent),
      isSynthetic: isSyntheticSession(meta.cwd || "", userMessages),
      start: new Date(start).toISOString(),
      end: new Date(end).toISOString(),
      minutes: activeMinutes(times),
      activityTimes: [...new Set(times)].sort((a, b) => a - b),
      token,
      userMessages: dedupe(userMessages).slice(0, 12),
    });
  }

  if (!sessions.length) {
    diagnostics.push(createDiagnostic(
      "no-sessions",
      "warning",
      "所选时间范围内没有读取到 Codex 会话。",
      "可以扩大 --days 范围，或确认当前账号的 Codex 会话目录是否正确。",
    ));
  }
  if (malformedLineCount) {
    diagnostics.push(createDiagnostic(
      "malformed-jsonl",
      "warning",
      `有 ${malformedLineCount} 行会话记录损坏，已跳过这些行继续生成报告。`,
      "如果报告项目明显缺失，可以缩小时间范围后重试，或检查最近异常中断的会话。",
    ));
  }
  if (sessionsWithoutToken) {
    diagnostics.push(createDiagnostic(
      "missing-token-events",
      "info",
      `${sessionsWithoutToken} 个会话没有 Token 记录。`,
      "报告仍可使用，但 Token 总量可能偏低。",
    ));
  }

  const artifacts = walk(workspace, {
    maxDepth: 5,
    filter: (file) => ARTIFACT_EXTENSIONS.has(path.extname(file).toLowerCase()) && recent(file, since),
    diagnostics,
    label: "工作区",
    skip: (dir) => {
      const name = path.basename(dir);
      return SKIP_DIRECTORIES.has(name) || name.startsWith(".") || path.resolve(dir) === path.dirname(outputFile);
    },
  }).map((file) => ({
    relative: path.relative(workspace, file) || path.basename(file),
    modifiedAt: fs.statSync(file).mtime.toISOString(),
  })).filter((item) => {
    if (path.resolve(workspace, item.relative) === path.resolve(outputFile)) return false;
    return !["codex_usage_scan.json", "codex_review_scan.json"].includes(path.basename(item.relative));
  });

  const automationFiles = walk(path.join(codexHome, "automations"), {
    maxDepth: 4,
    filter: (file) => path.basename(file) === "automation.toml",
    diagnostics: [],
    label: "自动化任务目录",
  });
  const automationText = automationFiles.map((file) => safeRead(file)).join("\n");
  const skillChanges = walk(path.join(codexHome, "skills"), {
    maxDepth: 4,
    filter: (file) => recent(file, since),
    diagnostics: [],
    label: "Skills 目录",
  }).length;

  return {
    sessions,
    artifacts,
    environment: {
      skillChangeCount: skillChanges,
      automationCount: automationFiles.length,
      hasWeeklyAutomation: /Codex 周度使用体检|Codex 使用复盘|AI 使用体检|Codex Review/i.test(automationText),
    },
  };
}

function ensureDirectory(dir, message, action) {
  try {
    if (!fs.statSync(dir).isDirectory()) throw new Error("not a directory");
  } catch (error) {
    throw userError(message, action, redactHome(dir));
  }
}

function walk(dir, options, depth = 0) {
  const { maxDepth, filter, diagnostics, label, skip = () => false } = options;
  if (depth > maxDepth || !fs.existsSync(dir) || skip(dir)) return [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (error) {
    diagnostics.push(createDiagnostic(
      "unreadable-directory",
      "warning",
      `无法读取部分${label}，已跳过。`,
      "请检查目录权限；报告仍会使用其余可读取数据。",
      dir,
    ));
    return [];
  }
  const out = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full, options, depth + 1));
    else if (filter(full)) out.push(full);
  }
  return out;
}

function parseJsonl(file) {
  let text;
  try {
    text = fs.readFileSync(file, "utf8");
  } catch {
    return { items: [], malformed: 0 };
  }
  let malformed = 0;
  const items = text.split("\n").filter(Boolean).map((line) => {
    try {
      return JSON.parse(line);
    } catch {
      malformed += 1;
      return null;
    }
  }).filter(Boolean);
  return { items, malformed };
}

function cleanUserMessage(value) {
  let text = String(value || "");
  text = text.replace(/<environment_context>[\s\S]*?<\/environment_context>/g, "").trim();
  if (text.startsWith("# AGENTS.md instructions")) {
    const parts = text.split(/\n---\n/g).map((part) => part.trim()).filter(Boolean);
    text = parts.length > 1 ? parts[parts.length - 1] : "";
  }
  if (!text || text.startsWith("<skill>") || text.startsWith("<INSTRUCTIONS>")) return "";
  if (text === "<turn_aborted>") return "";
  if (text.startsWith("The following is the Codex agent history whose request action you are assessing.")) return "";
  return redactSecrets(text);
}

function textOf(content) {
  if (!content) return "";
  if (typeof content === "string") return content;
  if (Array.isArray(content)) return content.map((item) => item?.text || item?.input_text || item?.output_text || "").join(" ");
  return "";
}

function tokenUsageForRange(items, since, until) {
  const baseline = emptyToken();
  const latest = emptyToken();
  let sawInRange = false;
  for (const item of items) {
    if (item.type !== "event_msg" || item.payload?.type !== "token_count") continue;
    const time = new Date(item.timestamp || 0).getTime();
    if (!Number.isFinite(time)) continue;
    const usage = item.payload.info?.total_token_usage;
    if (time < since.getTime()) maxToken(baseline, usage);
    else if (time <= until.getTime()) {
      maxToken(latest, usage);
      sawInRange = true;
    }
  }
  if (!sawInRange) return emptyToken();
  for (const key of Object.keys(latest)) latest[key] = Math.max(0, latest[key] - baseline[key]);
  return latest;
}

function recent(file, since) {
  try {
    return fs.statSync(file).mtime >= since;
  } catch {
    return false;
  }
}

function activeMinutes(times) {
  const ordered = [...new Set(times)].sort((a, b) => a - b);
  if (ordered.length < 2) return 1;
  let milliseconds = 60 * 1000;
  for (let index = 1; index < ordered.length; index += 1) {
    milliseconds += Math.min(ordered[index] - ordered[index - 1], 15 * 60 * 1000);
  }
  return Math.max(1, milliseconds / 60000);
}

function safeRead(file) {
  try {
    return fs.readFileSync(file, "utf8");
  } catch {
    return "";
  }
}

function dedupe(values) {
  return [...new Set(values)];
}

function isSyntheticSession(cwd, messages) {
  const uniqueMessages = dedupe(messages);
  const text = uniqueMessages.join("\n");
  if (/^\/tmp\/(?:hermes|codex)[-_]/i.test(cwd)) return true;
  if (/append exactly one new line containing.+do not modify any other file/i.test(text)) return true;
  if (uniqueMessages.length === 1 && /说一个\s*1\s*到\s*100\s*的随机数/.test(text)) return true;
  if (uniqueMessages.length === 1 && /^\[@[^\]]+\]\(plugin:\/\/[^)]+\)\s+Inspect PRs, triage issues/i.test(text)) return true;
  return false;
}

function redactSecrets(value) {
  return String(value || "")
    .replace(/((?:auth[_ -]?token|access[_ -]?token|api[_ -]?key|secret|password|密码|密钥)\s*(?:[:=]|是)\s*)[^\s,;，；]+/gi, "$1[已隐藏]")
    .replace(/((?:auth[_ -]?token|access[_ -]?token|api[_ -]?key|secret|password|密码|密钥)[^\n]{0,24}?[:：]\s*)[a-z0-9_-]{12,}/gi, "$1[已隐藏]")
    .replace(/\b(?:sk|pk)-[a-z0-9_-]{12,}\b/gi, "[已隐藏]");
}
