#!/usr/bin/env node


const API_URL = "https://api.iyiou.com/skill/info";
const EVENT_HINT_KEYS = new Set([
  "id",
  "idStr",
  "postTitle",
  "brief",
  "originalLink",
  "createdAt",
]);


function usage(exitCode = 2) {
  console.error(
    [
      "Usage: fetch_events.mjs [options]",
      "",
      "Options:",
      "  --page-size <n>           Page size (default: 10, bounds: 1-100)",
      "  --max-page <n>            Max page number (default: 5 daily / 25 range, bounds: 1-25)",
      "  --report-date <YYYY-MM-DD>Report end date (default: yesterday)",
      "  --recent-days <n>         Recent day window (default: 1, bounds: 1-7)",
      "  --timeout-seconds <n>     Request timeout in seconds (default: 15)",
      "  --retry <n>               Retry count per page (default: 3, bounds: 1-10)",
      "  --delay-seconds <n>       Delay between pages (default: 0)",
      "  --stdout-json             Kept for compatibility (stdout is always enabled)",
      "  -h, --help                Show this help",
    ].join("\n")
  );
  process.exit(exitCode);
}

function localDateISO() {
  const now = new Date();
  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function yesterdayDateISO() {
  const now = new Date();
  now.setDate(now.getDate() - 1);
  return formatDateISO(now);
}

function localDateTime() {
  const now = new Date();
  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function formatDateISO(value) {
  const year = String(value.getFullYear());
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function parseISODate(value) {
  const text = String(value ?? "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return null;
  const date = new Date(`${text}T00:00:00`);
  return Number.isNaN(date.getTime()) ? null : date;
}

function shiftDateISO(value, diffDays) {
  const date = parseISODate(value);
  if (!date) return "";
  date.setDate(date.getDate() + diffDays);
  return formatDateISO(date);
}

function clamp(value, low, high) {
  return Math.max(low, Math.min(value, high));
}

function parseIntOrDefault(value, defaultValue) {
  const num = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(num) ? num : defaultValue;
}

function parseFloatOrDefault(value, defaultValue) {
  const num = Number.parseFloat(String(value ?? ""));
  return Number.isFinite(num) ? num : defaultValue;
}

function parseArgs(argv) {
  const options = {
    pageSize: 10,
    maxPage: 5,
    reportDate: yesterdayDateISO(),
    recentDays: 1,
    timeoutSeconds: 15,
    retry: 3,
    delaySeconds: 0,
    stdoutJson: true,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") usage(0);

    if (arg === "--page-size") {
      options.pageSize = parseIntOrDefault(argv[i + 1], options.pageSize);
      i += 1;
      continue;
    }
    if (arg === "--max-page") {
      options.maxPage = parseIntOrDefault(argv[i + 1], options.maxPage);
      i += 1;
      continue;
    }
    if (arg === "--report-date") {
      options.reportDate = argv[i + 1] ?? options.reportDate;
      i += 1;
      continue;
    }
    if (arg === "--recent-days") {
      options.recentDays = parseIntOrDefault(argv[i + 1], options.recentDays);
      i += 1;
      continue;
    }
    if (arg === "--timeout-seconds") {
      options.timeoutSeconds = parseIntOrDefault(argv[i + 1], options.timeoutSeconds);
      i += 1;
      continue;
    }
    if (arg === "--retry") {
      options.retry = parseIntOrDefault(argv[i + 1], options.retry);
      i += 1;
      continue;
    }
    if (arg === "--delay-seconds") {
      options.delaySeconds = parseFloatOrDefault(argv[i + 1], options.delaySeconds);
      i += 1;
      continue;
    }
    if (arg === "--stdout-json") {
      options.stdoutJson = true;
      continue;
    }

    console.error(`Unknown arg: ${arg}`);
    usage();
  }

  options.recentDays = clamp(options.recentDays, 1, 7);
  options.pageSize = clamp(options.pageSize, 1, 100);
  options.maxPage = clamp(options.maxPage, 1, 25);
  options.retry = clamp(options.retry, 1, 10);
  options.timeoutSeconds = clamp(options.timeoutSeconds, 1, 120);
  options.delaySeconds = Math.max(0, options.delaySeconds);
  if (!parseISODate(options.reportDate)) {
    throw new Error(`invalid --report-date: ${options.reportDate}`);
  }
  if (options.recentDays > 1) {
    options.maxPage = 25;
    options.pageSize = 10;
  }
  return options;
}

async function fetchJson(params, timeoutSeconds) {
  const url = new URL(API_URL);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, String(value));
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutSeconds * 1000);

  let response;
  try {
    response = await fetch(url, {
      method: "GET",
      headers: {
        "User-Agent": "daily-investment-digest/1.0",
        Accept: "application/json,text/plain,*/*",
      },
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timer);
    throw new Error(`request failed: ${err.message}`);
  }
  clearTimeout(timer);

  if (!response.ok) {
    const detail = (await response.text().catch(() => ""))
      .replace(/\s+/g, " ")
      .slice(0, 300);
    throw new Error(`HTTP ${response.status}: ${detail || "<empty>"}`);
  }

  const rawText = await response.text();
  try {
    return { payload: JSON.parse(rawText), requestUrl: url.toString() };
  } catch {
    const preview = rawText.replace(/\s+/g, " ").slice(0, 300);
    throw new Error(`invalid JSON: ${preview}`);
  }
}

function looksLikeEvent(item) {
  if (!item || typeof item !== "object" || Array.isArray(item)) return false;
  return Object.keys(item).some((key) => EVENT_HINT_KEYS.has(key));
}

function looksLikeEventList(value, allowEmpty = false) {
  if (!Array.isArray(value)) return false;
  if (value.length === 0) return allowEmpty;
  if (!value.every((item) => item && typeof item === "object" && !Array.isArray(item))) {
    return false;
  }
  return value.some((item) => looksLikeEvent(item));
}

function extractPostsStrict(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new Error("response is not an object");
  }

  if ("code" in payload && Number(payload.code) !== 0) {
    const message = String(payload.message ?? "").trim();
    throw new Error(`api code=${payload.code}${message ? `, message=${message}` : ""}`);
  }

  const data = payload.data;
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("missing object at response.data");
  }

  const posts = data.posts;
  if (!Array.isArray(posts)) {
    throw new Error("missing array at response.data.posts");
  }
  if (!looksLikeEventList(posts, true)) {
    throw new Error("response.data.posts is not a valid event list");
  }
  return posts;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function uniqueTagNames(value) {
  if (!Array.isArray(value)) return [];
  const seen = new Set();
  const names = [];
  for (const item of value) {
    if (!item || typeof item !== "object") continue;
    const name = String(item.tagName ?? "").trim();
    if (!name || seen.has(name)) continue;
    seen.add(name);
    names.push(name);
  }
  return names;
}

function eventKey(item, index) {
  for (const key of ["id", "idStr", "originalLink"]) {
    const value = item?.[key];
    if (value !== undefined && value !== null && String(value) !== "") {
      return `${key}:${String(value)}`;
    }
  }
  const title = String(item?.postTitle ?? item?.originalTitle ?? "").trim();
  const createdAt = String(item?.createdAt ?? "").trim();
  if (title || createdAt) return `title:${title}|createdAt:${createdAt}`;
  return `index:${index}`;
}

function normalizeEvent(item, index) {
  const brief = String(item?.brief ?? item?.description ?? "").trim();
  const createdAt = String(item?.createdAt ?? "").trim();
  const originalLink = String(item?.originalLink ?? "").trim();
  const postTitle = String(item?.postTitle ?? item?.originalTitle ?? "").trim();
  const tags = uniqueTagNames(item?.tags);

  if (!brief && !createdAt && !originalLink && !postTitle) {
    return {
      brief: "",
      createdAt: "",
      originalLink: "",
      postTitle: eventKey(item, index),
      tags: [],
    };
  }

  return {
    brief,
    createdAt,
    originalLink,
    postTitle,
    tags,
  };
}

function parseDateTime(value) {
  if (!value) return 0;
  const ts = new Date(value.replace(" ", "T")).getTime();
  return Number.isFinite(ts) ? ts : 0;
}

function dateFromCreatedAt(value) {
  const text = String(value ?? "").trim();
  if (text.length >= 10) {
    return text.slice(0, 10);
  }
  return "";
}

function isDateInRange(value, startDate, endDate) {
  const eventDate = dateFromCreatedAt(value);
  if (!eventDate) return false;
  return eventDate >= startDate && eventDate <= endDate;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const rangeStartDate = shiftDateISO(options.reportDate, 1 - options.recentDays);
  const rangeLabel = options.recentDays === 1 ? "single_day" : `recent_${options.recentDays}_days`;

  const uniqueRaw = [];
  const seenKeys = new Set();
  let totalRawEvents = 0;
  let rawIndex = 0;
  const errors = [];
  let fetchedPages = 0;
  let lastPageChecked = 0;

  for (let page = 1; page <= options.maxPage; page += 1) {
    lastPageChecked = page;
    let payload = null;
    let requestUrl = "";

    for (let attempt = 1; attempt <= options.retry; attempt += 1) {
      try {
        const result = await fetchJson(
          {
            page,
            pageSize: options.pageSize,
          },
          options.timeoutSeconds
        );
        payload = result.payload;
        requestUrl = result.requestUrl;
        break;
      } catch (err) {
        if (attempt === options.retry) {
          errors.push(`page ${page}: failed after ${options.retry} attempts: ${err.message}`);
        } else {
          await sleep(500 * attempt);
        }
      }
    }

    if (!payload) continue;

    let items;
    try {
      items = extractPostsStrict(payload);
    } catch (err) {
      errors.push(`page ${page}: invalid response schema from ${requestUrl}: ${err.message}`);
      continue;
    }

    fetchedPages += 1;
    if (items.length === 0) break;
    totalRawEvents += items.length;
    for (const item of items) {
      if (!isDateInRange(item?.createdAt, rangeStartDate, options.reportDate)) {
        continue;
      }
      const key = eventKey(item, rawIndex);
      rawIndex += 1;
      if (seenKeys.has(key)) continue;
      seenKeys.add(key);
      uniqueRaw.push(item);
    }
    if (options.delaySeconds > 0) {
      await sleep(Math.round(options.delaySeconds * 1000));
    }
  }

  const events = uniqueRaw.map((item, index) => normalizeEvent(item, index));
  events.sort((a, b) => parseDateTime(b.createdAt) - parseDateTime(a.createdAt));

  const outputPayload = {
    meta: {
      endpoint: API_URL,
      page_size: options.pageSize,
      max_page: options.maxPage,
      last_page_checked: lastPageChecked,
      fetched_pages: fetchedPages,
      total_raw_events: totalRawEvents,
      total_unique_events: uniqueRaw.length,
      generated_at: localDateTime(),
      report_date: options.reportDate,
      range_start_date: rangeStartDate,
      recent_days: options.recentDays,
      range_label: rangeLabel,
      current_date: localDateISO(),
      filter_rule: "createdAt date must be within [range_start_date, report_date], default single day is yesterday",
      source_list_field: "posts",
      response_path: "data.posts",
      kept_fields: ["brief", "createdAt", "originalLink", "postTitle", "tags"],
      errors,
    },
    events,
  };

  const outputJsonText = `${JSON.stringify(outputPayload)}\n`;
  process.stdout.write(outputJsonText);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});
