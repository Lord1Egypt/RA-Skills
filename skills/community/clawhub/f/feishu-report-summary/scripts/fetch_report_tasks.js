#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");

function printHelp() {
  const lines = [
    "Fetch Feishu report tasks and render them as JSON or Markdown.",
    "",
    "Usage:",
    "  node scripts/fetch_report_tasks.js [options]",
    "",
    "Options:",
    "  --date YYYY-MM-DD         Fetch one local calendar day",
    "  --start-date YYYY-MM-DD   Start date (inclusive, local time)",
    "  --end-date YYYY-MM-DD     End date (inclusive, local time)",
    "  --days N                  Fetch the last N local calendar days (default: 1)",
    "  --page-size N             Page size for report.task.query (default: 20, max: 20)",
    "  --max-items N             Stop after N tasks",
    "  --rule-id ID              Filter by report rule ID",
    "  --rule-name NAME          Resolve a rule ID from the rule name before querying",
    "  --user-id ID              Filter by reporter user ID",
    "  --user-id-type TYPE       user_id | union_id | open_id (default: open_id)",
    "  --account-id ID           Feishu account ID from ~/.openclaw/openclaw.json",
    "  --config PATH             OpenClaw config path (default: ~/.openclaw/openclaw.json)",
    "  --format FORMAT           json | markdown (default: markdown)",
    "  --output PATH             Write the rendered output to a file instead of stdout",
    "  --help                    Show this help message",
    "",
    "Environment overrides:",
    "  FEISHU_APP_ID",
    "  FEISHU_APP_SECRET",
    "  OPENCLAW_ROOT",
    "",
    "Examples:",
    "  node scripts/fetch_report_tasks.js --date 2026-03-14 --format json",
    "  node scripts/fetch_report_tasks.js --days 7 --rule-name \"研发团队工作日报\" --output /tmp/report.md",
  ];
  console.log(lines.join("\n"));
}

function fail(message) {
  console.error(`Error: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    days: 1,
    pageSize: 20,
    userIdType: "open_id",
    format: "markdown",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      fail(`Unexpected positional argument: ${token}`);
    }
    const key = token.slice(2);
    if (key === "help") {
      args.help = true;
      continue;
    }
    const next = argv[index + 1];
    if (next === undefined || next.startsWith("--")) {
      fail(`Missing value for --${key}`);
    }
    index += 1;
    switch (key) {
      case "date":
        args.date = next;
        break;
      case "start-date":
        args.startDate = next;
        break;
      case "end-date":
        args.endDate = next;
        break;
      case "days":
        args.days = parsePositiveInteger(next, "--days");
        break;
      case "page-size":
        args.pageSize = parsePositiveInteger(next, "--page-size");
        break;
      case "max-items":
        args.maxItems = parsePositiveInteger(next, "--max-items");
        break;
      case "rule-id":
        args.ruleId = next;
        break;
      case "rule-name":
        args.ruleName = next;
        break;
      case "user-id":
        args.userId = next;
        break;
      case "user-id-type":
        args.userIdType = next;
        break;
      case "account-id":
        args.accountId = next;
        break;
      case "config":
        args.config = next;
        break;
      case "format":
        args.format = next;
        break;
      case "output":
        args.output = next;
        break;
      default:
        fail(`Unknown option: --${key}`);
    }
  }

  if (!["open_id", "user_id", "union_id"].includes(args.userIdType)) {
    fail("--user-id-type must be one of: open_id, user_id, union_id");
  }
  if (!["json", "markdown"].includes(args.format)) {
    fail("--format must be one of: json, markdown");
  }
  if (args.date && (args.startDate || args.endDate)) {
    fail("--date cannot be combined with --start-date or --end-date");
  }
  if (args.ruleId && args.ruleName) {
    fail("--rule-id cannot be combined with --rule-name");
  }

  return args;
}

function parsePositiveInteger(value, flagName) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    fail(`${flagName} must be a positive integer`);
  }
  return parsed;
}

function parseDateString(value, flagName) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    fail(`${flagName} must be in YYYY-MM-DD format`);
  }
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) {
    fail(`${flagName} is not a valid date`);
  }
  return date;
}

function formatDateOnly(date) {
  return [
    String(date.getFullYear()).padStart(4, "0"),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("-");
}

function formatDateTime(epochSeconds) {
  const date = new Date(epochSeconds * 1000);
  return [
    formatDateOnly(date),
    [
      String(date.getHours()).padStart(2, "0"),
      String(date.getMinutes()).padStart(2, "0"),
      String(date.getSeconds()).padStart(2, "0"),
    ].join(":"),
  ].join(" ");
}

function addDays(date, days) {
  const next = new Date(date.getTime());
  next.setDate(next.getDate() + days);
  return next;
}

function resolveRange(args) {
  if (args.date) {
    const startDate = parseDateString(args.date, "--date");
    const endDateExclusive = addDays(startDate, 1);
    return buildRange(startDate, endDateExclusive);
  }

  if (args.startDate || args.endDate) {
    if (!args.startDate || !args.endDate) {
      fail("--start-date and --end-date must be provided together");
    }
    const startDate = parseDateString(args.startDate, "--start-date");
    const endDateInclusive = parseDateString(args.endDate, "--end-date");
    const endDateExclusive = addDays(endDateInclusive, 1);
    if (endDateExclusive <= startDate) {
      fail("--end-date must be on or after --start-date");
    }
    return buildRange(startDate, endDateExclusive);
  }

  const now = new Date();
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startDate = addDays(todayStart, -(args.days - 1));
  const endDateExclusive = addDays(todayStart, 1);
  return buildRange(startDate, endDateExclusive);
}

function buildRange(startDate, endDateExclusive) {
  return {
    startDate: formatDateOnly(startDate),
    endDateInclusive: formatDateOnly(addDays(endDateExclusive, -1)),
    startEpochSeconds: Math.floor(startDate.getTime() / 1000),
    endEpochSecondsExclusive: Math.floor(endDateExclusive.getTime() / 1000),
  };
}

function dedupe(values) {
  const seen = new Set();
  const result = [];
  for (const value of values) {
    const normalized = path.resolve(value);
    if (seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    result.push(normalized);
  }
  return result;
}

function readCommandOutput(command, commandArgs) {
  return execFileSync(command, commandArgs, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"],
  }).trim();
}

function findOpenClawRoot() {
  const candidates = [];

  if (process.env.OPENCLAW_ROOT) {
    candidates.push(process.env.OPENCLAW_ROOT);
  }

  try {
    const npmRoot = readCommandOutput("npm", ["root", "-g"]);
    if (npmRoot) {
      candidates.push(path.join(npmRoot, "openclaw"));
    }
  } catch {}

  try {
    const openclawBinary = fs.realpathSync(readCommandOutput("which", ["openclaw"]));
    const prefix = path.resolve(path.dirname(openclawBinary), "..");
    candidates.push(path.join(prefix, "lib", "node_modules", "openclaw"));
  } catch {}

  candidates.push(path.join(os.homedir(), ".npm-global", "lib", "node_modules", "openclaw"));
  candidates.push("/usr/lib/node_modules/openclaw");

  for (const candidate of dedupe(candidates)) {
    if (fs.existsSync(path.join(candidate, "package.json"))) {
      return candidate;
    }
  }

  fail(
    "Could not locate the OpenClaw installation. Set OPENCLAW_ROOT to the openclaw package directory.",
  );
}

function loadLarkSdk() {
  const openClawRoot = findOpenClawRoot();
  const sdkPath = path.join(openClawRoot, "node_modules", "@larksuiteoapi", "node-sdk");
  if (!fs.existsSync(path.join(sdkPath, "package.json"))) {
    fail(`Could not locate @larksuiteoapi/node-sdk under ${openClawRoot}`);
  }
  return require(sdkPath);
}

function loadConfig(configPath) {
  const resolvedPath = configPath || path.join(os.homedir(), ".openclaw", "openclaw.json");
  if (!fs.existsSync(resolvedPath)) {
    fail(`OpenClaw config not found: ${resolvedPath}`);
  }
  try {
    return {
      path: resolvedPath,
      data: JSON.parse(fs.readFileSync(resolvedPath, "utf8")),
    };
  } catch (error) {
    fail(`Failed to read OpenClaw config: ${error.message}`);
  }
}

function resolveFeishuAccount(configData, explicitAccountId) {
  const feishu = configData.channels && configData.channels.feishu;
  if (!feishu) {
    fail("channels.feishu is missing from the OpenClaw config");
  }

  const accounts = feishu.accounts && typeof feishu.accounts === "object" ? feishu.accounts : {};
  const accountIds = Object.keys(accounts);
  const accountId =
    explicitAccountId ||
    feishu.defaultAccount ||
    (accountIds.includes("default") ? "default" : accountIds[0] || "default");

  const { accounts: _accounts, defaultAccount: _defaultAccount, ...baseConfig } = feishu;
  const merged = { ...baseConfig, ...(accounts[accountId] || {}) };
  const appId = process.env.FEISHU_APP_ID || merged.appId;
  const appSecret = process.env.FEISHU_APP_SECRET || merged.appSecret;

  if (!appId || !appSecret) {
    fail(`Missing appId/appSecret for Feishu account "${accountId}"`);
  }
  if (String(appSecret).startsWith("secret://")) {
    fail(
      `appSecret for Feishu account "${accountId}" is a secret reference. Set FEISHU_APP_SECRET before running this script.`,
    );
  }

  return {
    accountId,
    appId,
    appSecret,
    domain: merged.domain === "lark" ? "Lark" : "Feishu",
  };
}

function ensureSuccess(response, apiName) {
  if (response && response.code === 0) {
    return response;
  }
  const code = response && Object.prototype.hasOwnProperty.call(response, "code") ? response.code : -1;
  const message = response && response.msg ? response.msg : "unknown error";
  fail(`${apiName} failed with code=${code}: ${message}`);
}

function describeApiError(error) {
  const response = error && error.response ? error.response : null;
  const body = response && response.data ? response.data : null;
  if (!body) {
    return error instanceof Error ? error.message : String(error);
  }

  const parts = [];
  if (body.msg) {
    parts.push(body.msg);
  }
  if (body.code !== undefined) {
    parts.push(`code=${body.code}`);
  }
  if (body.error && body.error.log_id) {
    parts.push(`log_id=${body.error.log_id}`);
  }
  const violations =
    body.error && Array.isArray(body.error.field_violations) ? body.error.field_violations : [];
  if (violations.length > 0) {
    parts.push(
      `field_violations=${violations
        .map((item) => `${item.field}: ${item.description}`)
        .join("; ")}`,
    );
  }
  return parts.join(" | ");
}

async function callApi(apiName, fn) {
  try {
    return ensureSuccess(await fn(), apiName);
  } catch (error) {
    fail(`${apiName} request failed: ${describeApiError(error)}`);
  }
}

async function resolveRuleId(client, ruleName) {
  const response = await callApi("report.rule.query", () =>
    client.report.rule.query({ params: { rule_name: ruleName } }),
  );
  const rules = response.data && response.data.rules ? response.data.rules : [];
  const exactMatches = rules.filter((rule) => rule.name === ruleName);
  if (exactMatches.length === 1) {
    return exactMatches[0];
  }
  if (exactMatches.length > 1) {
    fail(`Multiple report rules matched "${ruleName}" exactly`);
  }
  if (rules.length === 1) {
    return rules[0];
  }
  if (rules.length === 0) {
    fail(`No report rule matched "${ruleName}"`);
  }
  fail(
    `Multiple report rules matched "${ruleName}": ${rules
      .map((rule) => rule.name || rule.rule_id)
      .join(", ")}`,
  );
}

async function fetchTasks(client, query) {
  const tasks = [];
  let pageToken = "0";
  const pageSize = Math.min(query.pageSize || 20, 20);

  while (true) {
    const payload = {
      data: {
        commit_start_time: query.startEpochSeconds,
        commit_end_time: query.endEpochSecondsExclusive,
        page_token: pageToken,
        page_size: pageSize,
      },
    };
    if (query.ruleId) {
      payload.data.rule_id = query.ruleId;
    }
    if (query.userId) {
      payload.data.user_id = query.userId;
      payload.params = { user_id_type: query.userIdType };
    }

    const response = await callApi("report.task.query", () => client.report.task.query(payload));
    const items = response.data && response.data.items ? response.data.items : [];
    tasks.push(...items);

    if (query.maxItems && tasks.length >= query.maxItems) {
      return tasks.slice(0, query.maxItems);
    }
    if (!response.data || !response.data.has_more || !response.data.page_token) {
      return tasks;
    }
    pageToken = response.data.page_token;
  }
}

function countBy(items, selector, limit) {
  const map = new Map();
  for (const item of items) {
    const key = selector(item) || "Unknown";
    map.set(key, (map.get(key) || 0) + 1);
  }
  return [...map.entries()]
    .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))
    .slice(0, limit)
    .map(([name, count]) => ({ name, count }));
}

function prettyFieldValue(rawValue) {
  if (rawValue === null || rawValue === undefined) {
    return "";
  }
  if (typeof rawValue !== "string") {
    return JSON.stringify(rawValue);
  }

  const trimmed = rawValue.trim();
  if (!trimmed) {
    return "";
  }

  try {
    return renderStructuredValue(JSON.parse(trimmed));
  } catch {
    return trimmed;
  }
}

function renderStructuredValue(value) {
  if (value === null || value === undefined) {
    return "";
  }
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (Array.isArray(value)) {
    return value.map((entry) => renderStructuredValue(entry)).filter(Boolean).join(", ");
  }
  if (typeof value === "object") {
    if (typeof value.text === "string" && Object.keys(value).length <= 2) {
      return value.text;
    }
    return Object.entries(value)
      .map(([key, entry]) => `${key}: ${renderStructuredValue(entry)}`)
      .filter((entry) => !entry.endsWith(": "))
      .join("; ");
  }
  return String(value);
}

function normalizeTasks(tasks) {
  return tasks.map((task) => ({
    task_id: task.task_id || "",
    rule_id: task.rule_id || "",
    rule_name: task.rule_name || "",
    from_user_id: task.from_user_id || "",
    from_user_name: task.from_user_name || "",
    department_name: task.department_name || "",
    commit_time: task.commit_time || 0,
    commit_time_local: task.commit_time ? formatDateTime(task.commit_time) : "",
    to_user_ids: task.to_user_ids || [],
    to_user_names: task.to_user_names || [],
    fields: (task.form_contents || []).map((field) => ({
      field_id: field.field_id || "",
      field_name: field.field_name || "",
      field_value_raw: field.field_value || "",
      field_value_pretty: prettyFieldValue(field.field_value || ""),
    })),
  }));
}

function renderMarkdown(report) {
  const lines = [
    "# Feishu Report Export",
    "",
    `- Generated at: ${report.generated_at_local}`,
    `- Account: ${report.account_id}`,
    `- Config: ${report.config_path}`,
    `- Range: ${report.range.start_date} to ${report.range.end_date_inclusive} (local dates)`,
    `- Total tasks: ${report.total_tasks}`,
  ];

  if (report.filters.rule_name || report.filters.rule_id || report.filters.user_id) {
    lines.push("- Filters:");
    if (report.filters.rule_name) {
      lines.push(`  - Rule name: ${report.filters.rule_name}`);
    }
    if (report.filters.rule_id) {
      lines.push(`  - Rule ID: ${report.filters.rule_id}`);
    }
    if (report.filters.user_id) {
      lines.push(`  - User ID (${report.filters.user_id_type}): ${report.filters.user_id}`);
    }
  }

  if (report.stats.by_rule.length > 0) {
    lines.push(`- Top rules: ${report.stats.by_rule.map((item) => `${item.name} (${item.count})`).join(", ")}`);
  }
  if (report.stats.by_reporter.length > 0) {
    lines.push(
      `- Top reporters: ${report.stats.by_reporter
        .map((item) => `${item.name} (${item.count})`)
        .join(", ")}`,
    );
  }

  lines.push("");

  if (report.items.length === 0) {
    lines.push("No report tasks matched the query.");
    return `${lines.join("\n")}\n`;
  }

  lines.push("## Entries", "");

  report.items.forEach((item, index) => {
    lines.push(
      `### ${index + 1}. ${item.from_user_name || "Unknown"} | ${item.rule_name || "Unnamed rule"} | ${item.commit_time_local || "Unknown time"}`,
    );
    lines.push(`- task_id: ${item.task_id || "-"}`);
    lines.push(`- department: ${item.department_name || "-"}`);
    lines.push(`- recipients: ${item.to_user_names.length > 0 ? item.to_user_names.join(", ") : "-"}`);
    if (item.fields.length === 0) {
      lines.push("- fields: -");
    } else {
      lines.push("- fields:");
      item.fields.forEach((field) => {
        const prettyValue = field.field_value_pretty || "(empty)";
        const valueLines = prettyValue.split(/\r?\n/);
        if (valueLines.length === 1) {
          lines.push(`  - ${field.field_name || field.field_id || "field"}: ${valueLines[0]}`);
          return;
        }
        lines.push(`  - ${field.field_name || field.field_id || "field"}:`);
        valueLines.forEach((line) => {
          lines.push(`    ${line}`);
        });
      });
    }
    lines.push("");
  });

  return `${lines.join("\n").trimEnd()}\n`;
}

function buildReportPayload(context) {
  return {
    generated_at_local: formatDateTime(Math.floor(Date.now() / 1000)),
    account_id: context.accountId,
    config_path: context.configPath,
    range: {
      start_date: context.range.startDate,
      end_date_inclusive: context.range.endDateInclusive,
      start_epoch_seconds: context.range.startEpochSeconds,
      end_epoch_seconds_exclusive: context.range.endEpochSecondsExclusive,
    },
    filters: {
      rule_id: context.rule && context.rule.rule_id ? context.rule.rule_id : context.args.ruleId || "",
      rule_name: context.rule && context.rule.name ? context.rule.name : context.args.ruleName || "",
      user_id: context.args.userId || "",
      user_id_type: context.args.userId ? context.args.userIdType : "",
    },
    total_tasks: context.items.length,
    stats: {
      by_rule: countBy(context.items, (item) => item.rule_name, 5),
      by_reporter: countBy(context.items, (item) => item.from_user_name, 5),
    },
    items: context.items,
  };
}

function writeOutput(outputPath, content) {
  if (!outputPath) {
    process.stdout.write(content);
    return;
  }
  const resolvedPath = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolvedPath), { recursive: true });
  fs.writeFileSync(resolvedPath, content, "utf8");
  console.error(`Wrote ${resolvedPath}`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }

  const Lark = loadLarkSdk();
  const config = loadConfig(args.config);
  const account = resolveFeishuAccount(config.data, args.accountId);
  const range = resolveRange(args);

  const client = new Lark.Client({
    appId: account.appId,
    appSecret: account.appSecret,
    appType: Lark.AppType.SelfBuild,
    domain: account.domain === "Lark" ? Lark.Domain.Lark : Lark.Domain.Feishu,
  });

  const resolvedRule = args.ruleName ? await resolveRuleId(client, args.ruleName) : null;
  const tasks = await fetchTasks(client, {
    startEpochSeconds: range.startEpochSeconds,
    endEpochSecondsExclusive: range.endEpochSecondsExclusive,
    pageSize: args.pageSize,
    maxItems: args.maxItems,
    ruleId: args.ruleId || (resolvedRule ? resolvedRule.rule_id : ""),
    userId: args.userId,
    userIdType: args.userIdType,
  });
  const normalizedTasks = normalizeTasks(tasks);
  const report = buildReportPayload({
    accountId: account.accountId,
    configPath: config.path,
    range,
    args,
    rule: resolvedRule,
    items: normalizedTasks,
  });

  const content =
    args.format === "json"
      ? `${JSON.stringify(report, null, 2)}\n`
      : renderMarkdown(report);

  writeOutput(args.output, content);
}

main().catch((error) => {
  fail(error instanceof Error ? error.message : String(error));
});
