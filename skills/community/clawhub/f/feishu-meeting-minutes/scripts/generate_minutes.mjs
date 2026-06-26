import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const DEFAULT_FONT = "Noto Sans CJK SC";
const DEFAULT_TITLE = "未命名会议";
const TOKEN_RE = /^[A-Za-z0-9_-]{8,128}$/;

export function parseCliArgs(argv) {
  const options = {
    outputDir: process.cwd(),
    pdf: false,
    upload: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    switch (arg) {
      case "--minute-url":
        options.minuteUrl = argv[++index];
        break;
      case "--minute-token":
        options.minuteToken = argv[++index];
        break;
      case "--transcript-file":
        options.transcriptFile = argv[++index];
        break;
      case "--output-dir":
        options.outputDir = argv[++index];
        break;
      case "--title":
        options.title = argv[++index];
        break;
      case "--pdf":
        options.pdf = true;
        break;
      case "--upload":
        options.upload = true;
        break;
      case "--font":
        options.font = argv[++index];
        break;
      case "--help":
      case "-h":
        options.help = true;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return options;
}

export function extractMinuteToken(input) {
  if (!input || typeof input !== "string") {
    throw new Error("Minute token or minute URL is required.");
  }

  const trimmed = input.trim();
  if (TOKEN_RE.test(trimmed)) {
    return trimmed;
  }

  let parsedUrl;
  try {
    parsedUrl = new URL(trimmed);
  } catch {
    throw new Error("Minute token format is invalid.");
  }

  const minutesIndex = parsedUrl.pathname.split("/").findIndex((segment) => segment === "minutes");
  if (minutesIndex === -1) {
    throw new Error("Minute URL must contain /minutes/<minute_token>.");
  }

  const token = parsedUrl.pathname.split("/")[minutesIndex + 1];
  if (!TOKEN_RE.test(token ?? "")) {
    throw new Error("Minute token extracted from URL is invalid.");
  }
  return token;
}

export function slugifyTitle(title) {
  const normalized = (title ?? "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^A-Za-z0-9._-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase();

  return normalized || "meeting";
}

export function buildOutputBaseName({ title, minuteToken, dateTag }) {
  const safeDate = dateTag || new Date().toISOString().slice(0, 10).replaceAll("-", "");
  const slug = slugifyTitle(title).slice(0, 32);
  const suffix = (minuteToken || "manual").slice(0, 8);
  return `meeting_minutes_${safeDate}_${slug}_${suffix}`;
}

export function cleanTranscriptLine(line) {
  return line
    .replace(/\r/g, "")
    .replace(/^\s*\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*/u, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function parseSpeakerLine(line) {
  const trimmed = cleanTranscriptLine(line);
  const match = trimmed.match(/^([\p{L}\p{N}][\p{L}\p{N}\s.-]{0,30}?)[：:]\s*(.+)$/u);
  if (!match) {
    return { speaker: "", content: trimmed };
  }

  const speaker = match[1].trim();
  if (speaker.length > 20) {
    return { speaker: "", content: trimmed };
  }

  return {
    speaker,
    content: match[2].trim(),
  };
}

function isUsefulSentence(text) {
  return text.length >= 8 && !/^([嗯啊哦好的行收到]+|\.{3,}|…+)$/u.test(text);
}

function uniqueByNormalizedText(items, limit) {
  const seen = new Set();
  const result = [];
  for (const item of items) {
    const normalized = item.replace(/\s+/g, " ").trim();
    if (!normalized || seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    result.push(normalized);
    if (result.length >= limit) {
      break;
    }
  }
  return result;
}

function matchAny(text, patterns) {
  return patterns.some((pattern) => pattern.test(text));
}

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function inferDueDate(text) {
  const patterns = [
    /(\d{4}[-/]\d{1,2}[-/]\d{1,2})/,
    /(本周|下周|下下周|今天|明天|后天|月底|月初|本月内|下月初|下个月)/u,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1];
    }
  }
  return "待确认";
}

function inferOwner(text, participants, fallbackSpeaker) {
  if (fallbackSpeaker && /^(我|我来|我负责|我跟进|我这边)/u.test(text)) {
    return fallbackSpeaker;
  }

  for (const participant of participants) {
    const namePattern = new RegExp(`(?:由)?${escapeRegExp(participant)}(?:负责|跟进|推进|准备|提交|输出|安排|落实|同步)`, "u");
    if (namePattern.test(text)) {
      return participant;
    }
  }

  const ownerMatch = text.match(/(?:^|[\s，,；;])([\p{L}\p{N}]{2,20})(负责|跟进|推进|准备|提交|输出|安排|落实|同步)/u);
  if (ownerMatch) {
    return ownerMatch[1];
  }

  if (fallbackSpeaker) {
    return fallbackSpeaker;
  }

  for (const participant of participants) {
    if (text.includes(participant)) {
      return participant;
    }
  }

  return "待指定";
}

function pickMeetingNature(lines) {
  const joined = lines.join(" ");
  if (/周会|周例会/u.test(joined)) {
    return "周例会";
  }
  if (/复盘|回顾/u.test(joined)) {
    return "复盘会议";
  }
  if (/评审/u.test(joined)) {
    return "评审会议";
  }
  return "专题会议";
}

function toIsoDateTag(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return new Date().toISOString().slice(0, 10).replaceAll("-", "");
  }
  return date.toISOString().slice(0, 10).replaceAll("-", "");
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "待补充";
  }
  const day = `${date.getUTCFullYear()}-${`${date.getUTCMonth() + 1}`.padStart(2, "0")}-${`${date.getUTCDate()}`.padStart(2, "0")}`;
  return day;
}

function formatTimeRange(createTime, durationMs) {
  const start = new Date(createTime);
  if (Number.isNaN(start.getTime())) {
    return "待补充";
  }
  const end = new Date(start.getTime() + (durationMs || 0));
  const format = (date) => `${`${date.getUTCHours()}`.padStart(2, "0")}:${`${date.getUTCMinutes()}`.padStart(2, "0")}`;
  return `${format(start)}-${format(end)}`;
}

export function summarizeTranscript(transcriptText) {
  const rawLines = transcriptText
    .split(/\n+/u)
    .map((line) => line.trim())
    .filter(Boolean);

  const parsedLines = rawLines
    .map((line) => parseSpeakerLine(line))
    .filter((entry) => isUsefulSentence(entry.content));

  const participants = uniqueByNormalizedText(
    parsedLines
      .map((entry) => entry.speaker)
      .filter((speaker) => speaker && !/主持|记录|unknown/i.test(speaker)),
    12,
  );

  const contentLines = parsedLines.map((entry) => entry.content);

  const summary = uniqueByNormalizedText(contentLines, 3);
  const agenda = uniqueByNormalizedText(
    contentLines.filter((line) =>
      matchAny(line, [/议题/u, /议程/u, /关于/u, /重点/u, /安排/u, /计划/u, /先/u]),
    ),
    5,
  );
  const issues = uniqueByNormalizedText(
    contentLines.filter((line) => matchAny(line, [/问题/u, /风险/u, /阻塞/u, /困难/u, /bug/i, /缺口/u])),
    4,
  );
  const decisions = uniqueByNormalizedText(
    contentLines.filter((line) => matchAny(line, [/决定/u, /确认/u, /同意/u, /通过/u, /结论/u, /统一/u, /采用/u])),
    5,
  );
  const nextSteps = uniqueByNormalizedText(
    contentLines.filter((line) => matchAny(line, [/下周/u, /后续/u, /下一步/u, /本周内/u, /跟进/u, /推进/u])),
    5,
  );

  const actionItems = parsedLines
    .filter((entry) =>
      matchAny(entry.content, [/负责/u, /跟进/u, /推进/u, /完成/u, /提交/u, /输出/u, /准备/u, /安排/u, /落实/u, /同步/u, /deadline/i]),
    )
    .slice(0, 8)
    .map((entry, index) => ({
      index: index + 1,
      task: entry.content,
      owner: inferOwner(entry.content, participants, entry.speaker),
      due: inferDueDate(entry.content),
      status: "待办",
    }));

  const discussionLines = uniqueByNormalizedText(
    [...issues, ...decisions, ...summary, ...nextSteps],
    8,
  );

  const topics = [];
  const firstTopicLines = discussionLines.slice(0, 4);
  if (firstTopicLines.length > 0) {
    topics.push({
      title: "核心讨论",
      issue: issues[0] || summary[0] || "逐字稿中未明确指出现状问题，需要人工补充。",
      discussion: firstTopicLines,
      decisions: decisions.length > 0 ? decisions.slice(0, 3) : ["逐字稿中未出现明确决议，需要人工确认。"],
    });
  }

  if (actionItems.length > 0 || nextSteps.length > 0) {
    topics.push({
      title: "执行与跟进",
      issue: nextSteps[0] || "需要继续跟进会议中的行动项。",
      discussion: uniqueByNormalizedText(
        [...actionItems.map((item) => item.task), ...nextSteps],
        4,
      ),
      decisions: nextSteps.length > 0 ? nextSteps.slice(0, 3) : ["按照待办事项推进。"],
    });
  }

  return {
    participants,
    summary: summary.length > 0 ? summary : ["逐字稿内容较短，需要人工补充摘要。"],
    agenda: agenda.length > 0 ? agenda : summary.slice(0, 3),
    issues,
    decisions,
    nextSteps,
    actionItems,
    topics: topics.length > 0 ? topics : [
      {
        title: "待人工补充",
        issue: "逐字稿未能提取出足够的结构化信息。",
        discussion: summary.slice(0, 3),
        decisions: ["请人工补充决议与执行要求。"],
      },
    ],
    meetingNature: pickMeetingNature(contentLines),
  };
}

export function renderMinutesMarkdown(data) {
  const {
    title,
    minuteToken,
    minuteUrl,
    transcriptPath,
    transcriptSummary,
    metadata,
  } = data;

  const participants = transcriptSummary.participants.length > 0
    ? transcriptSummary.participants
    : ["待补充"];

  const dateLabel = metadata.meetingDate || "待补充";
  const timeRange = metadata.timeRange || "待补充";
  const durationLabel = metadata.durationLabel || "待补充";
  const reference = minuteUrl || minuteToken || "本地逐字稿";

  const summarySection = transcriptSummary.summary.map((line) => `- ${line}`).join("\n");
  const agendaSection = transcriptSummary.agenda.map((line, index) => `${index + 1}. ${line}`).join("\n");
  const participantRows = participants
    .map((name, index) => `| ${index + 1} | ${name} |`)
    .join("\n");

  const topicSections = transcriptSummary.topics
    .map((topic, index) => {
      const discussion = topic.discussion.map((line, lineIndex) => `${lineIndex + 1}. ${line}`).join("\n");
      const decisions = topic.decisions.map((line, lineIndex) => `${lineIndex + 1}. ${line}`).join("\n");
      return `### 5.${index + 1} ${topic.title}\n\n**现状问题**：${topic.issue}\n\n**关键讨论**：\n\n${discussion}\n\n**会议决议**：\n\n${decisions}`;
    })
    .join("\n\n---\n\n");

  const actionRows = transcriptSummary.actionItems.length > 0
    ? transcriptSummary.actionItems
      .map((item) => `| ${item.index} | ${item.task} | ${item.owner} | ${item.due} | ${item.status} |`)
      .join("\n")
    : "| 1 | 待人工补充任务项 | 待指定 | 待确认 | 待办 |";

  const decisionSection = (transcriptSummary.decisions.length > 0
    ? transcriptSummary.decisions
    : transcriptSummary.summary
  ).slice(0, 4).map((line, index) => `${index + 1}. ${line}`).join("\n");

  const nextSection = (transcriptSummary.nextSteps.length > 0
    ? transcriptSummary.nextSteps
    : transcriptSummary.actionItems.map((item) => item.task)
  ).slice(0, 4).map((line) => `- ${line}`).join("\n") || "- 待人工确认后续安排";

  return `# ${title}会议纪要

---

**编号**：AUTO-${metadata.dateTag}-${(minuteToken || "manual").slice(0, 6)}  
**日期**：${dateLabel}  
**密级**：内部

---

## 一、会议概况

| 项目 | 详情 |
|:-----|:-----|
| 会议名称 | ${title} |
| 会议时间 | ${timeRange} |
| 会议主持 | 待补充 |
| 记录整理 | AI 助手 |
| 会议时长 | ${durationLabel} |
| 会议性质 | ${transcriptSummary.meetingNature} |
| 原始记录 | ${reference} |
| Transcript 来源 | ${transcriptPath} |

---

## 二、出席人员

| 序号 | 姓名 |
|:-----|:-----|
${participantRows}

---

## 三、会议摘要

${summarySection}

---

## 四、会议议程

${agendaSection}

---

## 五、讨论纪要

${topicSections}

---

## 六、待办事项

| 序号 | 任务事项 | 责任人 | 完成时限 | 状态 |
|:-----|:---------|:-------|:---------|:-----|
${actionRows}

---

## 七、会议结论

${decisionSection}

---

## 八、下步安排

${nextSection}

---

*此文档由脚本自动生成，请结合原始逐字稿进行复核。*`;
}

function runCommand(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    shell: false,
    ...options,
  });

  if (result.error) {
    throw new Error(`${command} is not available: ${result.error.message}`);
  }

  if (result.status !== 0) {
    const stderr = (result.stderr || result.stdout || "").trim();
    throw new Error(stderr || `${command} exited with code ${result.status}`);
  }

  return (result.stdout || "").trim();
}

function extractJsonObject(text) {
  const first = text.indexOf("{");
  const last = text.lastIndexOf("}");
  if (first === -1 || last === -1 || last <= first) {
    throw new Error("CLI output did not contain a JSON object.");
  }
  return JSON.parse(text.slice(first, last + 1));
}

function findValueDeep(value, keys) {
  if (value === null || value === undefined) {
    return undefined;
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findValueDeep(item, keys);
      if (found !== undefined) {
        return found;
      }
    }
    return undefined;
  }

  if (typeof value === "object") {
    for (const key of keys) {
      if (key in value && value[key] !== undefined && value[key] !== null) {
        return value[key];
      }
    }

    for (const nestedValue of Object.values(value)) {
      const found = findValueDeep(nestedValue, keys);
      if (found !== undefined) {
        return found;
      }
    }
  }

  return undefined;
}

function parseDurationMs(rawDuration) {
  if (rawDuration === undefined || rawDuration === null || rawDuration === "") {
    return 0;
  }

  const numeric = Number(rawDuration);
  if (Number.isNaN(numeric)) {
    return 0;
  }

  if (numeric > 1000) {
    return numeric;
  }

  return numeric * 1000;
}

function formatDuration(durationMs) {
  if (!durationMs) {
    return "待补充";
  }

  const totalMinutes = Math.round(durationMs / 60000);
  if (totalMinutes < 1) {
    return `${Math.round(durationMs / 1000)} 秒`;
  }
  return `${totalMinutes} 分钟`;
}

function extractMinuteMetadata(output) {
  const parsed = extractJsonObject(output);
  const title = findValueDeep(parsed, ["title", "topic", "name"]) || DEFAULT_TITLE;
  const rawDuration = findValueDeep(parsed, ["duration", "duration_ms"]);
  const rawCreateTime = findValueDeep(parsed, ["create_time", "start_time", "created_at"]);
  const durationMs = parseDurationMs(rawDuration);

  let createTime = rawCreateTime;
  if (typeof rawCreateTime === "string" && /^\d{10,13}$/.test(rawCreateTime)) {
    createTime = Number(rawCreateTime.length === 10 ? `${rawCreateTime}000` : rawCreateTime);
  }

  return {
    title,
    durationMs,
    createTime,
  };
}

export function findTranscriptFile(rootDir, minuteToken) {
  const stack = [resolve(rootDir)];
  const matches = [];

  while (stack.length > 0) {
    const current = stack.pop();
    const entries = readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }

      if (entry.isFile() && entry.name.toLowerCase() === "transcript.txt") {
        const inExpectedPath = minuteToken ? fullPath.includes(minuteToken) : true;
        if (!inExpectedPath) {
          continue;
        }
        matches.push({
          path: fullPath,
          mtimeMs: statSync(fullPath).mtimeMs,
        });
      }
    }
  }

  matches.sort((left, right) => right.mtimeMs - left.mtimeMs);
  return matches[0]?.path || "";
}

function ensureDirectory(pathValue) {
  mkdirSync(pathValue, { recursive: true });
  return resolve(pathValue);
}

function ensureFileExists(pathValue, label) {
  if (!existsSync(pathValue)) {
    throw new Error(`${label} does not exist: ${pathValue}`);
  }
}

function buildMetadata(options, minuteInfo) {
  const durationMs = minuteInfo.durationMs || 0;
  const createTime = minuteInfo.createTime;
  const dateTag = createTime ? toIsoDateTag(createTime) : toIsoDateTag(Date.now());
  return {
    durationMs,
    durationLabel: formatDuration(durationMs),
    meetingDate: createTime ? formatDate(createTime) : "待补充",
    timeRange: createTime ? formatTimeRange(createTime, durationMs) : "待补充",
    dateTag,
  };
}

function fetchMinuteInfo(minuteToken) {
  const stdout = runCommand("lark-cli", [
    "minutes",
    "minutes",
    "get",
    "--params",
    JSON.stringify({ minute_token: minuteToken }),
  ]);
  return extractMinuteMetadata(stdout);
}

function fetchTranscript(minuteToken, outputDir) {
  const sessionDir = ensureDirectory(join(outputDir, `minute-${minuteToken}-${Date.now()}`));
  runCommand("lark-cli", [
    "vc",
    "+notes",
    "--minute-tokens",
    minuteToken,
    "--as",
    "user",
  ], { cwd: sessionDir });

  const transcriptPath = findTranscriptFile(sessionDir, minuteToken);
  if (!transcriptPath) {
    throw new Error("Transcript download finished but transcript.txt was not found inside the session directory.");
  }

  return transcriptPath;
}

function exportPdf(markdownPath, pdfPath, fontName) {
  runCommand("pandoc", [
    markdownPath,
    "-o",
    pdfPath,
    "--pdf-engine=xelatex",
    "-V",
    `mainfont=${fontName}`,
    "-V",
    "geometry:margin=1in",
  ]);
}

function uploadPdf(pdfPath) {
  return runCommand("lark-cli", [
    "drive",
    "+upload",
    "--file",
    pdfPath,
    "--name",
    basename(pdfPath),
    "--as",
    "user",
  ]);
}

export function generateMinutesWorkflow(options) {
  const outputDir = ensureDirectory(resolve(options.outputDir || process.cwd()));
  const transcriptFile = options.transcriptFile ? resolve(options.transcriptFile) : "";
  const minuteToken = options.minuteToken
    ? extractMinuteToken(options.minuteToken)
    : options.minuteUrl
      ? extractMinuteToken(options.minuteUrl)
      : "";

  if (!transcriptFile && !minuteToken) {
    throw new Error("Provide either --transcript-file or --minute-url/--minute-token.");
  }

  let minuteInfo = {
    title: options.title || DEFAULT_TITLE,
    durationMs: 0,
    createTime: undefined,
  };

  let resolvedTranscriptPath = transcriptFile;
  if (transcriptFile) {
    ensureFileExists(transcriptFile, "Transcript file");
  } else {
    minuteInfo = fetchMinuteInfo(minuteToken);
    resolvedTranscriptPath = fetchTranscript(minuteToken, outputDir);
  }

  if (options.title) {
    minuteInfo.title = options.title;
  }

  const transcriptText = readFileSync(resolvedTranscriptPath, "utf8");
  const transcriptSummary = summarizeTranscript(transcriptText);
  const metadata = buildMetadata(options, minuteInfo);
  const baseName = buildOutputBaseName({
    title: minuteInfo.title,
    minuteToken,
    dateTag: metadata.dateTag,
  });
  const markdownPath = join(outputDir, `${baseName}.md`);
  const pdfPath = join(outputDir, `${baseName}.pdf`);

  const markdown = renderMinutesMarkdown({
    title: minuteInfo.title,
    minuteToken,
    minuteUrl: options.minuteUrl,
    transcriptPath: resolvedTranscriptPath,
    transcriptSummary,
    metadata,
  });

  writeFileSync(markdownPath, markdown, "utf8");

  let uploaded = "";
  if (options.pdf) {
    exportPdf(markdownPath, pdfPath, options.font || DEFAULT_FONT);
  }
  if (options.upload) {
    if (!options.pdf) {
      throw new Error("--upload requires --pdf because Feishu upload expects the generated PDF.");
    }
    uploaded = uploadPdf(pdfPath);
  }

  return {
    minuteToken,
    transcriptPath: resolvedTranscriptPath,
    markdownPath,
    pdfPath: options.pdf ? pdfPath : "",
    uploaded,
    title: minuteInfo.title,
  };
}

export function formatHelp() {
  return `Usage:
  node scripts/generate_minutes.mjs --minute-url "<url>" --output-dir "./output"
  node scripts/generate_minutes.mjs --minute-token "<token>" --output-dir "./output" --pdf --upload
  node scripts/generate_minutes.mjs --transcript-file "./transcript.txt" --title "项目周会" --output-dir "./output"

Options:
  --minute-url <url>         Feishu minutes URL
  --minute-token <token>     Raw Feishu minute token
  --transcript-file <path>   Existing transcript file; skip remote fetch
  --output-dir <path>        Directory for markdown, pdf, and session files
  --title <text>             Override meeting title
  --pdf                      Export PDF via pandoc + xelatex
  --upload                   Upload generated PDF to Feishu Drive
  --font <name>              Override PDF font name
  --help                     Show this message`;
}

function isMainModule() {
  return process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

if (isMainModule()) {
  try {
    const options = parseCliArgs(process.argv.slice(2));
    if (options.help) {
      console.log(formatHelp());
      process.exit(0);
    }

    const result = generateMinutesWorkflow(options);
    console.log("Markdown:", result.markdownPath);
    if (result.pdfPath) {
      console.log("PDF:", result.pdfPath);
    }
    if (result.uploaded) {
      console.log("Upload:", result.uploaded);
    }
    console.log("Transcript:", result.transcriptPath);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}
