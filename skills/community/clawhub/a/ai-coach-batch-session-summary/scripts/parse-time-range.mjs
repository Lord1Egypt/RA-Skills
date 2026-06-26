/**
 * 从用户原话规则解析查询时间窗（Asia/Shanghai）。
 * 未识别时默认近 1 个月；上限 12 个月 / 366 天。
 */

const DEFAULT_MONTHS = 1;
const MAX_MONTHS = 12;
const MAX_DAYS = 366;

const CN_DIGIT = { 一：1, 二：2, 两：2, 三：3, 四：4, 五：5, 六：6, 七：7, 八：8, 九：9, 十：10 };

function parseCnNumber(raw) {
  if (raw == null || raw === "") return null;
  if (/^\d+$/.test(raw)) return Number.parseInt(raw, 10);
  if (raw.length === 1 && CN_DIGIT[raw] != null) return CN_DIGIT[raw];
  if (raw === "十") return 10;
  const m = raw.match(/^ 十？([一二三四五六七八九])$/);
  if (m) return CN_DIGIT[m[1]] ?? null;
  return null;
}

function formatShanghai(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const get = (type) => parts.find((p) => p.type === type)?.value ?? "00";
  return `${get("year")}-${get("month")}-${get("day")} ${get("hour")}:${get("minute")}:${get("second")}`;
}

function addMonths(date, months) {
  const d = new Date(date);
  d.setMonth(d.getMonth() - months);
  return d;
}

function addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() - days);
  return d;
}

function clampRange(amount, unit) {
  if (unit === "day") return Math.min(Math.max(amount, 1), MAX_DAYS);
  if (unit === "week") return Math.min(Math.max(amount, 1), 52);
  if (unit === "month") return Math.min(Math.max(amount, 1), MAX_MONTHS);
  if (unit === "year") return Math.min(Math.max(amount, 1), 5);
  return amount;
}

/**
 * @param {string} text 用户原话 userMessage
 * @param {Date} [now]
 * @returns {{ startTime: string, endTime: string, source: 'user'|'default', amount: number, unit: string, label: string }}
 */
export function parseTimeRange(text, now = new Date()) {
  const raw = String(text ?? "").trim();
  const end = now;
  let amount = null;
  let unit = null;
  let source = "default";
  let confidence = "missing";

  const rules = [
    {
      confidence: "explicit",
      re: /(?:最近 | 近|past|last)\s*(\d+|[一二两三四五六七八九十])\s*(天 | 日|周|星期 | 个月 | 月|年|days?|weeks?|months?|years?)/i,
      pick(m) {
        amount = parseCnNumber(m[1]) ?? Number.parseInt(m[1], 10);
        unit = normalizeUnit(m[2]);
      },
    },
    {
      confidence: "explicit",
      re: /(?:近 | 最近)\s*(\d+|[一二两三四五六七八九十])\s* 个？\s* 月/,
      pick(m) {
        amount = parseCnNumber(m[1]) ?? Number.parseInt(m[1], 10);
        unit = "month";
      },
    },
    {
      confidence: "explicit",
      re: /(?:近 | 最近)\s* 三\s* 个？\s* 月|(?:last|past)\s*3\s*months?/i,
      pick() {
        amount = 3;
        unit = "month";
      },
    },
    {
      confidence: "ambiguous",
      re: /(?:最近 | 近期|recently|lately|recent\s+period)(?!\s*[\d 一二两三四五六七八九十])/i,
      pick() {
        amount = DEFAULT_MONTHS;
        unit = "month";
      },
    },
  ];

  for (const { re, pick, confidence: ruleConfidence } of rules) {
    const m = raw.match(re);
    if (m) {
      pick(m);
      source = ruleConfidence === "explicit" ? "user" : "default";
      confidence = ruleConfidence;
      break;
    }
  }

  if (amount == null || unit == null) {
    amount = DEFAULT_MONTHS;
    unit = "month";
    source = "default";
    confidence = "missing";
  }

  amount = clampRange(amount, unit);
  let start;
  if (unit === "day") start = addDays(end, amount);
  else if (unit === "week") start = addDays(end, amount * 7);
  else if (unit === "month") start = addMonths(end, amount);
  else if (unit === "year") start = addMonths(end, amount * 12);
  else start = addMonths(end, DEFAULT_MONTHS);

  const label =
    source === "default"
      ? `默认近 ${DEFAULT_MONTHS} 个月`
      : `最近 ${amount} ${unitLabel(unit)}`;

  return {
    startTime: formatShanghai(start),
    endTime: formatShanghai(end),
    source,
    confidence,
    amount,
    unit,
    label,
    timeZone: "Asia/Shanghai",
  };
}

function normalizeUnit(u) {
  const s = String(u).toLowerCase();
  if (/ 天 | 日|day/.test(s)) return "day";
  if (/ 周 | 星期|week/.test(s)) return "week";
  if (/ 月|month/.test(s)) return "month";
  if (/ 年|year/.test(s)) return "year";
  return "month";
}

function unitLabel(unit) {
  if (unit === "day") return "天";
  if (unit === "week") return "周";
  if (unit === "month") return "个月";
  if (unit === "year") return "年";
  return "个月";
}
