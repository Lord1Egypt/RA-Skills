import crypto from "node:crypto";

export const DEFAULTS = Object.freeze({
  timezone: "Asia/Shanghai",
  defaultSchedule: "daily@09:00",
  maxManualResults: 10,
  maxPushResults: 20,
  maxSeenFingerprints: 2000,
});

const WEEKDAY_MAP = new Map([
  ["1", "1"],
  ["mon", "1"],
  ["monday", "1"],
  ["zhouyi", "1"],
  ["xingqiyi", "1"],
  ["周一", "1"],
  ["星期一", "1"],
  ["2", "2"],
  ["tue", "2"],
  ["tues", "2"],
  ["tuesday", "2"],
  ["zhouer", "2"],
  ["xingqier", "2"],
  ["周二", "2"],
  ["星期二", "2"],
  ["3", "3"],
  ["wed", "3"],
  ["wednesday", "3"],
  ["zhousan", "3"],
  ["xingqisan", "3"],
  ["周三", "3"],
  ["星期三", "3"],
  ["4", "4"],
  ["thu", "4"],
  ["thur", "4"],
  ["thurs", "4"],
  ["thursday", "4"],
  ["zhousi", "4"],
  ["xingqisi", "4"],
  ["周四", "4"],
  ["星期四", "4"],
  ["5", "5"],
  ["fri", "5"],
  ["friday", "5"],
  ["zhouwu", "5"],
  ["xingqiwu", "5"],
  ["周五", "5"],
  ["星期五", "5"],
  ["6", "6"],
  ["sat", "6"],
  ["saturday", "6"],
  ["zhouliu", "6"],
  ["xingqiliu", "6"],
  ["周六", "6"],
  ["星期六", "6"],
  ["7", "0"],
  ["sun", "0"],
  ["sunday", "0"],
  ["zhouri", "0"],
  ["xingqiri", "0"],
  ["周日", "0"],
  ["星期日", "0"],
  ["星期天", "0"],
]);

export function nowIso() {
  return new Date().toISOString();
}

export function normalizeText(value) {
  return String(value ?? "")
    .replace(/\s+/g, " ")
    .replace(/\u00a0/g, " ")
    .trim();
}

export function normalizeLoose(value) {
  return normalizeText(value)
    .replace(/[《》"'“”‘’]/g, "")
    .replace(/\s+/g, "")
    .toLowerCase();
}

export function createEmptyState() {
  return {
    version: 1,
    subscriptions: [],
  };
}

export function normalizeState(raw) {
  const state = raw && typeof raw === "object" ? raw : createEmptyState();
  const subscriptions = Array.isArray(state.subscriptions) ? state.subscriptions : [];
  return {
    version: Number.isInteger(state.version) ? state.version : 1,
    subscriptions: subscriptions
      .filter((item) => item && typeof item === "object")
      .map((item) => ({
        id: String(item.id ?? ""),
        cronId: item.cronId ? String(item.cronId) : null,
        type: item.type === "journal" ? "journal" : "topic",
        query: normalizeText(item.query),
        schedule: normalizeText(item.schedule),
        timezone: normalizeText(item.timezone) || DEFAULTS.timezone,
        createdAt: normalizeText(item.createdAt),
        lastRunAt: item.lastRunAt ? normalizeText(item.lastRunAt) : null,
        lastSuccessAt: item.lastSuccessAt ? normalizeText(item.lastSuccessAt) : null,
        lastError: item.lastError ? normalizeText(item.lastError) : null,
        seenFingerprints: Array.isArray(item.seenFingerprints)
          ? item.seenFingerprints
              .map((entry) => String(entry))
              .filter((entry) => entry)
          : [],
      }))
      .filter((item) => item.id && item.query),
  };
}

export function ensurePositiveInt(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

export function normalizeTimeSpec(value) {
  const match = /^(\d{1,2}):(\d{2})$/.exec(normalizeText(value));
  if (!match) {
    throw new Error(`Invalid time: ${value}`);
  }
  const hour = Number.parseInt(match[1], 10);
  const minute = Number.parseInt(match[2], 10);
  if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
    throw new Error(`Invalid time: ${value}`);
  }
  return { hour, minute };
}

export function normalizeWeekday(value) {
  const key = normalizeLoose(value);
  if (!WEEKDAY_MAP.has(key)) {
    throw new Error(`Invalid weekday: ${value}`);
  }
  return WEEKDAY_MAP.get(key);
}

export function parseScheduleSpec(spec, timezone = DEFAULTS.timezone) {
  const trimmed = normalizeText(spec);
  if (!trimmed) {
    throw new Error("Schedule is required");
  }

  if (trimmed.startsWith("every:")) {
    const every = normalizeText(trimmed.slice("every:".length));
    if (!every) {
      throw new Error("Missing every: duration");
    }
    return {
      kind: "every",
      normalized: `every:${every}`,
      cliArgs: ["--every", every],
    };
  }

  if (trimmed.startsWith("at:")) {
    const at = normalizeText(trimmed.slice("at:".length));
    if (!at) {
      throw new Error("Missing at: timestamp");
    }
    return {
      kind: "at",
      normalized: `at:${at}`,
      cliArgs: ["--at", at],
    };
  }

  if (trimmed.startsWith("cron:")) {
    const expr = normalizeText(trimmed.slice("cron:".length));
    if (!expr) {
      throw new Error("Missing cron expression");
    }
    return {
      kind: "cron",
      normalized: `cron:${expr}`,
      cliArgs: ["--cron", expr, "--tz", timezone, "--exact"],
    };
  }

  if (/^\S+(?:\s+\S+){4,5}$/.test(trimmed)) {
    return {
      kind: "cron",
      normalized: `cron:${trimmed}`,
      cliArgs: ["--cron", trimmed, "--tz", timezone, "--exact"],
    };
  }

  if (trimmed.startsWith("daily@")) {
    const { hour, minute } = normalizeTimeSpec(trimmed.slice("daily@".length));
    const expr = `${minute} ${hour} * * *`;
    return {
      kind: "cron",
      normalized: `daily@${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`,
      cliArgs: ["--cron", expr, "--tz", timezone, "--exact"],
    };
  }

  if (trimmed.startsWith("workday@")) {
    const { hour, minute } = normalizeTimeSpec(trimmed.slice("workday@".length));
    const expr = `${minute} ${hour} * * 1-5`;
    return {
      kind: "cron",
      normalized: `workday@${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`,
      cliArgs: ["--cron", expr, "--tz", timezone, "--exact"],
    };
  }

  if (trimmed.startsWith("weekly@")) {
    const parts = trimmed.split("@");
    if (parts.length !== 3) {
      throw new Error(`Invalid weekly schedule: ${trimmed}`);
    }
    const weekday = normalizeWeekday(parts[1]);
    const { hour, minute } = normalizeTimeSpec(parts[2]);
    const expr = `${minute} ${hour} * * ${weekday}`;
    return {
      kind: "cron",
      normalized: `weekly@${parts[1]}@${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`,
      cliArgs: ["--cron", expr, "--tz", timezone, "--exact"],
    };
  }

  throw new Error(`Unsupported schedule format: ${trimmed}`);
}

export function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\"'\"'`)}'`;
}

export function buildCronPrompt(baseDir, subscriptionId) {
  const scriptPath = `${baseDir}/scripts/cnki_watch.mjs`;
  return [
    "Run the CNKI subscription checker now.",
    `Run this exact command in bash: node ${shellQuote(scriptPath)} run-subscription --id ${shellQuote(subscriptionId)} --json`,
    "Do not browse manually and do not improvise any extra workflow.",
    "The script handles CNKI access, de-duplication, and main-chat delivery by itself.",
    "If the command fails, report the exact error. If it succeeds, reply with one short status line only.",
  ].join("\n");
}

export function fingerprintRecord(record) {
  const basis = record.record_id
    ? `id:${record.record_id}`
    : record.url
      ? `url:${record.url}`
      : `fallback:${normalizeLoose(record.title)}|${normalizeLoose(record.source)}|${normalizeLoose(record.publish_date)}`;
  return crypto.createHash("sha256").update(basis).digest("hex");
}

export function appendSeenFingerprints(existing, fingerprints, maxSeen = DEFAULTS.maxSeenFingerprints) {
  const merged = [];
  const seen = new Set();
  for (const value of [...fingerprints, ...existing]) {
    const normalized = String(value ?? "").trim();
    if (!normalized || seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    merged.push(normalized);
    if (merged.length >= maxSeen) {
      break;
    }
  }
  return merged;
}

export function formatRecordLine(record, index) {
  const parts = [
    `${index}. ${normalizeText(record.title) || "(无标题)"}`,
    `来源：${normalizeText(record.source) || "未知"}`,
  ];
  if (normalizeText(record.authors)) {
    parts.push(`作者：${normalizeText(record.authors)}`);
  }
  if (normalizeText(record.publish_date)) {
    parts.push(`日期：${normalizeText(record.publish_date)}`);
  }
  if (normalizeText(record.url)) {
    parts.push(`链接：${normalizeText(record.url)}`);
  }
  return parts.join("\n");
}

export function formatManualResults(kind, query, records) {
  const header = kind === "journal" ? `CNKI 期刊查询：${query}` : `CNKI 主题查询：${query}`;
  if (!records.length) {
    return `${header}\n未找到可提取的结果。`;
  }
  return [header, ...records.map((record, index) => formatRecordLine(record, index + 1))].join("\n\n");
}

export function formatPushMessage(subscription, records, maxDisplay) {
  const typeLabel = subscription.type === "journal" ? "期刊订阅" : "主题订阅";
  const displayed = records.slice(0, maxDisplay);
  const lines = [
    `[CNKI Watch] ${typeLabel}更新`,
    `订阅：${subscription.query}`,
    `新增：${records.length} 篇`,
    "",
    ...displayed.map((record, index) => formatRecordLine(record, index + 1)),
  ];
  if (records.length > displayed.length) {
    lines.push("", `还有 ${records.length - displayed.length} 篇未展开。`);
  }
  return lines.join("\n");
}

export function formatErrorPushMessage(subscription, message) {
  const typeLabel = subscription.type === "journal" ? "期刊订阅" : "主题订阅";
  return [
    `[CNKI Watch] ${typeLabel}运行失败`,
    `订阅：${subscription.query}`,
    `错误：${normalizeText(message)}`,
  ].join("\n");
}

export function parseArgs(argv) {
  const positionals = [];
  const flags = {};
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (!value.startsWith("--")) {
      positionals.push(value);
      continue;
    }
    const key = value.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      flags[key] = true;
      continue;
    }
    flags[key] = next;
    index += 1;
  }
  return { positionals, flags };
}
