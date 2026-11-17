// Render the backend snapshot without re-ranking, filtering or estimating markets.
export function validateDivergenceLimit(limit) {
  if (limit !== undefined && (!Number.isInteger(limit) || limit < 1 || limit > 100)) {
    throw Object.assign(new Error("Divergence limit must be an integer from 1 to 100"), { code: "INVALID_INPUT" });
  }
  return limit;
}

// Require the caller's localized wording; never silently fall back to English.
export function validateDivergenceLabels(labels) {
  const keys = ["cournot_above", "cournot_below", "link"];
  if (!labels || typeof labels !== "object" || Array.isArray(labels) ||
      Object.keys(labels).some(key => !keys.includes(key)) ||
      keys.some(key => typeof labels[key] !== "string" || !labels[key].trim() || /[\r\n\u2028\u2029]/u.test(labels[key]))) {
    throw Object.assign(new Error("Provide --labels-json with single-line cournot_above, cournot_below and link labels in the user's language"), { code: "INVALID_INPUT" });
  }
  return { ...labels };
}

// Cross-check the original suffix so an agent cannot accidentally turn 2.5 into 2.
// Word-only counts still require the agent's natural-language interpretation.
export function validateDivergenceCountText(limit, text) {
  validateDivergenceLimit(limit);
  if (limit === undefined && text === undefined) return;
  const numbers = typeof text === "string" ? text.match(/[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?/gi) : null;
  if (limit === undefined || typeof text !== "string" || !text.trim() ||
      (numbers && (numbers.length !== 1 || !Number.isInteger(Number(numbers[0])) || Number(numbers[0]) !== limit))) {
    throw Object.assign(new Error("Use the unchanged original count text with an integer limit from 1 to 100; do not round, truncate or clamp counts"), { code: "INVALID_INPUT" });
  }
}

function invalid(field) {
  throw Object.assign(new Error(`Invalid divergence response: ${field}`), { code: "INVALID_API_RESPONSE" });
}

function cell(value) {
  return String(value).replace(/[\r\n\u2028\u2029]+/g, " ")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/[\\|\[\]*_`]/g, "\\$&");
}

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
function title(value) {
  return value.replace(/\bat any time\b/gi, "").replace(/\s+/g, " ").trim()
    .replace(/\b(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2} UTC\b/g, (match, year, month, day) => {
      const date = new Date(`${year}-${month}-${day}T00:00:00Z`);
      return !Number.isNaN(date.getTime()) && date.toISOString().startsWith(`${year}-${month}-${day}`)
        ? `${months[Number(month) - 1]} ${Number(day)}, ${year}` : match;
    });
}

function link(value, label) {
  // Validate without serializing through URL.href: serialization can change
  // casing, ports, path segments and encoding in an otherwise valid source URL.
  // Reject values that cannot be embedded unchanged in this Markdown table.
  if (typeof value !== "string" || !/^https?:\/\//i.test(value) || /[\s<>|\\\u0000-\u001f\u007f]/u.test(value)) invalid("market url");
  let url;
  try { url = new URL(value); } catch { invalid("market url"); }
  if (!["https:", "http:"].includes(url.protocol) || url.username || url.password) invalid("market url");
  return `[${cell(label)}](<${value}>)`;
}

const platforms = { kalshi: "Kalshi", polymarket: "Polymarket", limitless: "Limitless", myriad: "Myriad", "predict.fun": "Predict.fun" };
const number = (value) => value.toLocaleString("en-US", { maximumFractionDigits: 10 });
const percent = (value) => number(Number((value * 100).toPrecision(12)));

export function formatDivergenceRows(response, { limit = 10, labels } = {}) {
  validateDivergenceLimit(limit);
  labels = validateDivergenceLabels(labels);
  const data = response?.data;
  const divergence = data?.divergence;
  if (response?.code !== 0 || !Array.isArray(divergence?.items)) invalid("items");
  const items = divergence.items;
  if (items.length > limit) invalid("item count exceeds requested limit");
  if (items.length === 0) {
    // The empty-list contract promises no charge. Contradictory evidence must not be hidden.
    if (data.charged !== false || data.x402?.txn_hash) invalid("empty result billing is not confirmed");
    return "";
  }
  const rows = items.map((item) => {
    if (!item || !Number.isSafeInteger(item.rank) || item.rank < 1 ||
        typeof item.title !== "string" || !item.title.trim() ||
        typeof item.source !== "string" || !item.source.trim()) invalid("market rank, title or source");
    for (const field of ["cournot_price", "market_price", "deviation", "market_liquidity"]) {
      if (!Number.isFinite(item[field]) || item[field] < 0 || (field !== "market_liquidity" && item[field] > 1)) invalid(field);
    }
    if (!["cournot_above", "cournot_below"].includes(item.direction)) invalid("direction");
    const deviationPp = Math.round(Number((item.deviation * 100).toPrecision(12)));
    return `| ${item.rank} | ${cell(title(item.title))} | ${cell(platforms[item.source.toLowerCase()] || item.source)} | ${cell(labels[item.direction])} | ${(item.cournot_price * 100).toFixed(1)}% | ${percent(item.market_price)}¢ | ${deviationPp}pp | $${number(item.market_liquidity)} | ${link(item.url, labels.link)} |`;
  });
  return rows.join("\n");
}
