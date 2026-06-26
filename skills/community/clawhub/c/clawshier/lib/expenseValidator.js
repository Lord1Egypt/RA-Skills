const CURRENCY_ALIASES = { "$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY" };
const STRICT_ISO = /^\d{4}-\d{2}-\d{2}$/;

function isValidDateParts(year, month, day) {
  if (!Number.isInteger(year) || !Number.isInteger(month) || !Number.isInteger(day)) return false;
  if (month < 1 || month > 12 || day < 1 || day > 31) return false;
  const date = new Date(Date.UTC(year, month - 1, day));
  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
}

function toIso(year, month, day) {
  if (!isValidDateParts(year, month, day)) {
    throw new Error(`Invalid date components: ${year}-${month}-${day}`);
  }
  return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

function parseOverrideDate(argv = process.argv) {
  const idx = argv.indexOf("--date");
  if (idx === -1 || !argv[idx + 1]) return null;
  const val = argv[idx + 1];
  if (!STRICT_ISO.test(val)) {
    throw new Error(`--date must be in YYYY-MM-DD format, received: "${val}"`);
  }
  const [year, month, day] = val.split("-").map((part) => parseInt(part, 10));
  if (!isValidDateParts(year, month, day)) {
    throw new Error(`--date is not a valid date: "${val}"`);
  }
  return val;
}

function resolveDate(raw, today = new Date()) {
  raw = String(raw || "").replace(/[T ].*$/, "").trim();
  if (!raw) throw new Error("Date field is empty");

  if (STRICT_ISO.test(raw)) {
    const [year, month, day] = raw.split("-").map((part) => parseInt(part, 10));
    if (isValidDateParts(year, month, day)) return raw;
    throw new Error(`Invalid ISO date: "${raw}"`);
  }

  const parts = raw.match(/^(\d{1,4})[/\-.](\d{1,2})[/\-.](\d{1,4})$/);
  if (!parts) throw new Error(`Unable to parse date: "${raw}"`);

  let [, p1, p2, p3] = parts;
  p1 = parseInt(p1, 10);
  p2 = parseInt(p2, 10);
  p3 = parseInt(p3, 10);

  let year;
  let a;
  let b;

  if (p3 >= 100) {
    year = p3;
    a = p1;
    b = p2;
  } else if (p1 >= 100) {
    year = p1;
    a = p2;
    b = p3;
  } else {
    year = p3 + 2000;
    a = p1;
    b = p2;
  }

  const todayMonth = today.getMonth() + 1;
  const todayDay = today.getDate();

  const candidates = [
    { month: a, day: b, label: "MM-DD" },
    { month: b, day: a, label: "DD-MM" },
  ].filter((candidate, index, arr) => {
    if (!isValidDateParts(year, candidate.month, candidate.day)) return false;
    return index === arr.findIndex((item) => item.month === candidate.month && item.day === candidate.day);
  });

  const matchesToday = candidates.filter(
    (candidate) => candidate.month === todayMonth && candidate.day === todayDay
  );

  if (matchesToday.length === 1) {
    return toIso(year, matchesToday[0].month, matchesToday[0].day);
  }

  if (matchesToday.length === 2) {
    return toIso(year, matchesToday[0].month, matchesToday[0].day);
  }

  throw new Error(
    `Date "${raw}" does not match today (${toIso(today.getFullYear(), todayMonth, todayDay)}). ` +
    "For old invoices, re-run with --date YYYY-MM-DD to set the date explicitly."
  );
}

function sheetNameFromDate(dateStr) {
  const [year, month, day] = String(dateStr).split("-").map((part) => parseInt(part, 10));
  if (!isValidDateParts(year, month, day)) {
    throw new Error(`Cannot derive sheet name from invalid date: "${dateStr}"`);
  }
  return `${String(month).padStart(2, "0")}-${String(year).slice(-2)}`;
}

function normalize(expense, { overrideDate = null, today = new Date() } = {}) {
  const normalized = {
    ...expense,
    vendor: String(expense.vendor || "").trim(),
    date: overrideDate || resolveDate(expense.date, today),
    category: String(expense.category || "Other").trim(),
  };

  const rawCurrency = String(expense.currency || "USD").trim();
  normalized.currency = (CURRENCY_ALIASES[rawCurrency] || rawCurrency || "USD").toUpperCase().trim();

  normalized.total = parseFloat(expense.total);
  normalized.total = Number.isFinite(normalized.total) ? normalized.total : 0;

  normalized.subtotal = parseFloat(expense.subtotal);
  normalized.subtotal = Number.isFinite(normalized.subtotal) ? normalized.subtotal : normalized.total;

  normalized.tax = parseFloat(expense.tax);
  normalized.tax = Number.isFinite(normalized.tax) ? normalized.tax : 0;

  normalized.items = (expense.items || []).map((item) => ({
    description: String(item.description || "Unknown item").trim(),
    quantity: Number.isFinite(parseFloat(item.quantity)) ? parseFloat(item.quantity) : 1,
    amount: Number.isFinite(parseFloat(item.amount)) ? parseFloat(item.amount) : 0,
  }));

  return normalized;
}

function validate(expense) {
  const missing = [];
  if (!expense.vendor) missing.push("vendor");
  if (!expense.date) missing.push("date");
  if (!Number.isFinite(expense.total) || expense.total <= 0) missing.push("total");
  if (missing.length) throw new Error(`Missing required fields: ${missing.join(", ")}`);
}

module.exports = {
  CURRENCY_ALIASES,
  STRICT_ISO,
  isValidDateParts,
  parseOverrideDate,
  toIso,
  resolveDate,
  sheetNameFromDate,
  normalize,
  validate,
};
