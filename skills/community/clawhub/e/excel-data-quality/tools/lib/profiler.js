"use strict";
const U = require("./utils");

const PATTERNS = {
  email:        /^[\w.\-+]+@[\w.\-]+\.\w{2,}$/,
  phone_cn:     /^1[3-9]\d{9}$/,
  phone_us:     /^(?:\+1)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$/,
  phone_intl:   /^\+?\d{10,15}$/,
  url:          /^https?:\/\/[\w.\-]+(?:\/[\w.\-/?=&#%]*)*$/,
  ip_v4:        /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,
  date_iso:     /^\d{4}-\d{2}-\d{2}$/,
  date_eu_dot:  /^\d{1,2}\.\d{1,2}\.\d{4}$/,
  date_eu_slash:/^\d{1,2}\/\d{1,2}\/\d{4}$/,
  date_cn:      /^\d{4}年\d{1,2}月\d{1,2}日$/,
  date_kr:      /^\d{4}년\s?\d{1,2}월\s?\d{1,2}일$/,
  datetime_iso: /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}/,
  percentage:   /^\d+(\.\d+)?%$/,
  currency_cny: /^¥[\d,]+(\.\d{2})?$/,
  currency_usd: /^\$[\d,]+(\.\d{2})?$/,
  currency_eur: /^€[\d,.]+$/,
  currency_gbp: /^£[\d,.]+$/,
  currency_jpy: /^¥?[\d,]+円$/,
  currency_krw: /^₩?[\d,]+(?:원)?$/,
  id_card_cn:   /^\d{17}[\dXx]$/,
  uuid:         /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i,
};

const MAX_UNIQUE_FOR_CATEGORICAL = 50;

function profile(headers, rows, sampleSize) {
  sampleSize = sampleSize || 10;
  const start = Date.now();

  const tableStats = profileTable(headers, rows);
  const fieldStats = headers.map(h => profileField(h, rows));
  const sampleData = extractSample(headers, rows, sampleSize);
  const dataValidity = checkDataValidity(rows, tableStats, fieldStats);

  return {
    tableStats,
    fieldStats,
    sampleData,
    sampleSize: sampleData.length,
    profilingDurationMs: Date.now() - start,
    dataValidity,
  };
}

function profileTable(headers, rows) {
  const totalRows = rows.length;
  const totalCols = headers.length;
  let totalNulls = 0;
  let completeRows = 0;

  for (const row of rows) {
    let allPresent = true;
    for (const h of headers) {
      if (U.isNullish(row[h])) { totalNulls++; allPresent = false; }
    }
    if (allPresent) completeRows++;
  }

  const totalCells = totalRows * totalCols;
  const duplicateRows = countDuplicateRows(headers, rows);

  const columnTypes = {};
  for (const h of headers) {
    const t = inferFieldType(h, rows);
    columnTypes[t] = (columnTypes[t] || 0) + 1;
  }

  const memBytes = estimateMemory(headers, rows);

  return {
    totalRows,
    totalColumns: totalCols,
    memorySizeBytes: memBytes,
    memorySizeReadable: U.formatBytes(memBytes),
    completeRows,
    completeRowsPercentage: U.round(completeRows / Math.max(totalRows, 1) * 100, 2),
    totalNullCells: totalNulls,
    totalNullPercentage: U.round(totalNulls / Math.max(totalCells, 1) * 100, 2),
    columnTypes,
    duplicateRows,
    duplicatePercentage: U.round(duplicateRows / Math.max(totalRows, 1) * 100, 2),
  };
}

function profileField(name, rows) {
  const values = rows.map(r => r[name]);
  const totalCount = values.length;
  const nonNullValues = values.filter(v => !U.isNullish(v));
  const nonNullCount = nonNullValues.length;
  const nullCount = totalCount - nonNullCount;
  const uniqueSet = new Set(nonNullValues.map(String));
  const uniqueCount = uniqueSet.size;
  const inferredType = inferFieldType(name, rows);

  const stat = {
    name,
    inferredType,
    totalCount,
    nonNullCount,
    nullCount,
    nullPercentage: U.round(nullCount / Math.max(totalCount, 1) * 100, 2),
    uniqueCount,
    uniquePercentage: U.round(uniqueCount / Math.max(nonNullCount, 1) * 100, 2),
    sampleValues: nonNullValues.slice(0, 5).map(U.toJsonSafe),
  };

  if (inferredType === "integer" || inferredType === "float") {
    const nums = nonNullValues.map(U.tryParseNumber).filter(n => n !== null);
    if (nums.length) {
      stat.minValue = Math.min(...nums);
      stat.maxValue = Math.max(...nums);
      stat.meanValue = U.round(nums.reduce((a, b) => a + b, 0) / nums.length, 2);
      stat.medianValue = U.round(U.median(nums), 2);
      stat.stdValue = nums.length > 1 ? U.round(U.std(nums), 2) : 0;
    }
  }

  if (["string", "text", "categorical"].includes(inferredType)) {
    const lens = nonNullValues.map(v => String(v).length);
    if (lens.length) {
      stat.minLength = Math.min(...lens);
      stat.maxLength = Math.max(...lens);
      stat.avgLength = U.round(lens.reduce((a, b) => a + b, 0) / lens.length, 1);
    }
  }

  if (uniqueCount <= MAX_UNIQUE_FOR_CATEGORICAL && nonNullCount > 0) {
    stat.topValues = U.topValues(nonNullValues.map(String), 10);
  }

  if (inferredType === "string" && nonNullCount > 0) {
    const detected = detectPatterns(nonNullValues);
    if (detected.length) stat.detectedPatterns = detected;
  }

  return stat;
}

function inferFieldType(name, rows) {
  const sample = rows.slice(0, 100).map(r => r[name]).filter(v => !U.isNullish(v));
  if (!sample.length) return "unknown";

  const boolVals = new Set(["true", "false", "yes", "no", "是", "否", "1", "0"]);
  if (sample.every(v => boolVals.has(String(v).toLowerCase()))) return "boolean";

  if (sample.every(v => { const n = U.tryParseNumber(v); return n !== null; })) {
    return sample.some(v => String(v).includes(".")) ? "float" : "integer";
  }

  const dateCount = sample.filter(v => U.tryParseDate(v) !== null).length;
  if (dateCount > sample.length * 0.8) {
    return sample.some(v => /[T ]\d{2}:/.test(String(v))) ? "datetime" : "date";
  }

  const strs = sample.map(v => String(v));
  const avgLen = strs.reduce((s, v) => s + v.length, 0) / strs.length;
  if (avgLen > 100) return "text";

  const allValues = rows.map(r => r[name]).filter(v => !U.isNullish(v));
  const uniq = new Set(allValues.map(String));
  const uniqueRatio = uniq.size / Math.max(allValues.length, 1);
  if (uniqueRatio < 0.05 && uniq.size <= MAX_UNIQUE_FOR_CATEGORICAL) return "categorical";

  return "string";
}

function detectPatterns(values) {
  const sample = values.slice(0, 100).map(String);
  const found = [];
  for (const [name, regex] of Object.entries(PATTERNS)) {
    const matched = sample.filter(v => regex.test(v)).length;
    if (matched / sample.length > 0.8) found.push(name);
  }
  return found;
}

function extractSample(headers, rows, size) {
  if (!rows.length) return [];
  const scored = rows.map((row, idx) => {
    const filled = headers.filter(h => !U.isNullish(row[h])).length;
    return { idx, filled };
  });
  scored.sort((a, b) => b.filled - a.filled);
  return scored.slice(0, size).map(s => {
    const obj = {};
    headers.forEach(h => { obj[h] = U.toJsonSafe(rows[s.idx][h]); });
    return obj;
  });
}

function countDuplicateRows(headers, rows) {
  const seen = new Set();
  let dups = 0;
  for (const row of rows) {
    const key = headers.map(h => String(row[h] ?? "")).join("\x00");
    if (seen.has(key)) dups++;
    else seen.add(key);
  }
  return dups;
}

function estimateMemory(headers, rows) {
  let bytes = 0;
  for (const row of rows) {
    for (const h of headers) {
      const v = row[h];
      if (v == null) bytes += 8;
      else if (typeof v === "number") bytes += 8;
      else if (typeof v === "string") bytes += v.length * 2;
      else bytes += 16;
    }
  }
  return bytes;
}

function checkDataValidity(rows, tableStats, fieldStats) {
  const issues = [];
  const warnings = [];
  let canProceed = true;
  const { totalRows, totalColumns: totalCols, totalNullPercentage: nullRate,
    completeRowsPercentage: completeRatio, duplicatePercentage: dupRatio } = tableStats;

  if (totalCols > 100) { issues.push(`Too many columns (${totalCols}), may not be a standard table`); canProceed = false; }
  else if (totalCols > 50) warnings.push(`Many columns (${totalCols}), some checks will use simplified mode`);
  if (totalCols < 2) { issues.push("Too few columns for meaningful analysis"); canProceed = false; }
  if (totalRows < 5) { issues.push(`Too few rows (${totalRows}) for statistical analysis`); canProceed = false; }
  if (nullRate > 90) { issues.push(`Extremely high null rate (${nullRate}%), data is nearly empty`); canProceed = false; }
  else if (nullRate > 70) warnings.push(`High null rate (${nullRate}%), data may be incomplete`);

  const unnamedCols = fieldStats.filter(f => /Unnamed|Column_\d+/.test(f.name)).length;
  const unnamedRatio = unnamedCols / Math.max(totalCols, 1);
  if (unnamedRatio > 0.7) { issues.push(`Many unnamed columns (${unnamedCols}/${totalCols}), header may not be detected`); canProceed = false; }
  else if (unnamedRatio > 0.3) warnings.push(`Several unnamed columns (${unnamedCols}), check header`);

  const objectFields = fieldStats.filter(f => ["string", "text", "unknown"].includes(f.inferredType)).length;
  if (objectFields / Math.max(totalCols, 1) > 0.95 && totalCols > 5) {
    warnings.push("Nearly all columns are text type, may not be structured data");
  }
  if (completeRatio < 5 && totalRows > 100) warnings.push(`Very low complete-row ratio (${completeRatio}%)`);
  if (dupRatio > 80) warnings.push(`Very high duplicate-row ratio (${dupRatio}%)`);

  return {
    canProceed,
    issues,
    warnings,
    blockReason: canProceed ? null : (issues[0] || null),
    summary: { totalRows, totalCols, nullRate, unnamedCols, completeRowsPct: completeRatio },
  };
}

module.exports = { profile, inferFieldType, profileField, profileTable };
