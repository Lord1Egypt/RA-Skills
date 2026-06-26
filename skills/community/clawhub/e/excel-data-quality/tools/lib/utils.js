"use strict";

function formatBytes(size) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let i = 0;
  while (size >= 1024 && i < units.length - 1) { size /= 1024; i++; }
  return `${size.toFixed(1)} ${units[i]}`;
}

function round(val, decimals) {
  if (val == null || isNaN(val)) return null;
  const f = Math.pow(10, decimals);
  return Math.round(val * f) / f;
}

function isNullish(v) {
  return v === null || v === undefined || v === "" ||
    (typeof v === "number" && isNaN(v)) ||
    (typeof v === "string" && ["nan", "none", "null", "undefined"].includes(v.toLowerCase().trim()));
}

function median(arr) {
  if (!arr.length) return null;
  const s = arr.slice().sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

function quantile(arr, q) {
  if (!arr.length) return null;
  const s = arr.slice().sort((a, b) => a - b);
  const pos = (s.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  if (lo === hi) return s[lo];
  return s[lo] + (s[hi] - s[lo]) * (pos - lo);
}

function std(arr) {
  if (arr.length < 2) return 0;
  const m = arr.reduce((a, b) => a + b, 0) / arr.length;
  const variance = arr.reduce((sum, v) => sum + (v - m) * (v - m), 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

function mode(arr) {
  if (!arr.length) return null;
  const freq = {};
  for (const v of arr) { freq[v] = (freq[v] || 0) + 1; }
  let best = null, bestCount = 0;
  for (const [k, c] of Object.entries(freq)) {
    if (c > bestCount) { best = k; bestCount = c; }
  }
  return best;
}

function countBy(arr) {
  const m = {};
  for (const v of arr) { m[v] = (m[v] || 0) + 1; }
  return m;
}

function topValues(arr, n) {
  const freq = countBy(arr);
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([value, count]) => ({ value, count, percentage: round(count / arr.length * 100, 2) }));
}

function toJsonSafe(v) {
  if (v === null || v === undefined) return null;
  if (typeof v === "number" && isNaN(v)) return null;
  if (typeof v === "number" && !isFinite(v)) return null;
  if (v instanceof Date) return v.toISOString();
  return v;
}

const MONTH_ABBR = {
  jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
  jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
  // French
  janv: 0, févr: 1, mars: 2, avr: 3, mai: 4, juin: 5,
  juil: 6, août: 7, sept: 8, oct: 9, nov: 10, déc: 11,
  // German
  jän: 0, mär: 2, mai: 4, okt: 9, dez: 11,
  // Spanish
  ene: 0, abr: 3, ago: 7, dic: 11,
};

function tryParseDate(v) {
  if (v == null || v === "") return null;
  if (v instanceof Date) return isNaN(v.getTime()) ? null : v;
  const s = String(v).trim();

  // ISO / YYYY-MM-DD / YYYY/MM/DD (with optional time)
  if (/^\d{4}[-/]\d{2}[-/]\d{2}/.test(s)) {
    const d = new Date(s);
    return isNaN(d.getTime()) ? null : d;
  }
  // YYYY.MM.DD (EU/CJK dot-separated)
  const dotYmd = s.match(/^(\d{4})\.(\d{1,2})\.(\d{1,2})$/);
  if (dotYmd) {
    const d = new Date(+dotYmd[1], +dotYmd[2] - 1, +dotYmd[3]);
    return isNaN(d.getTime()) ? null : d;
  }
  // DD.MM.YYYY (German, Swiss, Russian, Turkish, etc.)
  const dotDmy = s.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
  if (dotDmy) {
    const day = +dotDmy[1], m = +dotDmy[2], y = +dotDmy[3];
    if (m >= 1 && m <= 12 && day >= 1 && day <= 31) {
      const d = new Date(y, m - 1, day);
      return isNaN(d.getTime()) ? null : d;
    }
  }
  // YYYYMMDD compact
  if (/^\d{8}$/.test(s)) {
    const y = +s.slice(0, 4), m = +s.slice(4, 6), day = +s.slice(6, 8);
    if (m >= 1 && m <= 12 && day >= 1 && day <= 31) {
      const d = new Date(y, m - 1, day);
      return isNaN(d.getTime()) ? null : d;
    }
  }
  // DD/MM/YYYY (UK, Europe, Middle East, LatAm) — also catches MM/DD/YYYY (US)
  const slashMatch = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (slashMatch) {
    const a = +slashMatch[1], b = +slashMatch[2], y = +slashMatch[3];
    // If first > 12, must be day (DD/MM/YYYY)
    if (a > 12 && b <= 12) return new Date(y, b - 1, a);
    // If second > 12, must be day (MM/DD/YYYY)
    if (b > 12 && a <= 12) return new Date(y, a - 1, b);
    // Ambiguous — default to MM/DD/YYYY for compatibility
    const d = new Date(y, a - 1, b);
    return isNaN(d.getTime()) ? null : d;
  }
  // DD-MM-YYYY with dashes (common in India, parts of EU)
  const dashDmy = s.match(/^(\d{1,2})-(\d{1,2})-(\d{4})$/);
  if (dashDmy) {
    const a = +dashDmy[1], b = +dashDmy[2], y = +dashDmy[3];
    if (a > 12 && b <= 12) return new Date(y, b - 1, a);
    if (b > 12 && a <= 12) return new Date(y, a - 1, b);
    const d = new Date(y, b - 1, a); // default DD-MM-YYYY
    return isNaN(d.getTime()) ? null : d;
  }
  // DD-MMM-YYYY / DD MMM YYYY (e.g., 15-Mar-2024, 15 Mar 2024)
  const dMyMatch = s.match(/^(\d{1,2})[-\s]([a-záéíóúàèìòùäöüâêîôûñç]+)[-\s](\d{4})$/i);
  if (dMyMatch) {
    const mon = MONTH_ABBR[dMyMatch[2].toLowerCase()];
    if (mon !== undefined) {
      const d = new Date(+dMyMatch[3], mon, +dMyMatch[1]);
      return isNaN(d.getTime()) ? null : d;
    }
  }
  // MMM DD, YYYY (e.g., Mar 15, 2024)
  const mdyStrMatch = s.match(/^([a-záéíóúàèìòùäöüâêîôûñç]+)\s+(\d{1,2}),?\s+(\d{4})$/i);
  if (mdyStrMatch) {
    const mon = MONTH_ABBR[mdyStrMatch[1].toLowerCase()];
    if (mon !== undefined) {
      const d = new Date(+mdyStrMatch[3], mon, +mdyStrMatch[2]);
      return isNaN(d.getTime()) ? null : d;
    }
  }
  // Chinese/Japanese: YYYY年MM月DD日
  const cjkFull = s.match(/^(\d{4})年(\d{1,2})月(\d{1,2})日$/);
  if (cjkFull) {
    const d = new Date(+cjkFull[1], +cjkFull[2] - 1, +cjkFull[3]);
    return isNaN(d.getTime()) ? null : d;
  }
  // Chinese/Japanese: YYYY年MM月 (month-only)
  const cjkMonth = s.match(/^(\d{4})年(\d{1,2})月$/);
  if (cjkMonth) {
    const d = new Date(+cjkMonth[1], +cjkMonth[2] - 1, 1);
    return isNaN(d.getTime()) ? null : d;
  }
  // Korean: YYYY년 MM월 DD일 or YYYY년MM월DD일
  const krMatch = s.match(/^(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일$/);
  if (krMatch) {
    const d = new Date(+krMatch[1], +krMatch[2] - 1, +krMatch[3]);
    return isNaN(d.getTime()) ? null : d;
  }
  // Korean month-only: YYYY년 MM월
  const krMonth = s.match(/^(\d{4})년\s*(\d{1,2})월$/);
  if (krMonth) {
    const d = new Date(+krMonth[1], +krMonth[2] - 1, 1);
    return isNaN(d.getTime()) ? null : d;
  }
  // Japanese era (Reiwa): 令和N年M月D日
  const jpEra = s.match(/^令和(\d{1,2})年(\d{1,2})月(\d{1,2})日$/);
  if (jpEra) {
    const d = new Date(2018 + (+jpEra[1]), +jpEra[2] - 1, +jpEra[3]);
    return isNaN(d.getTime()) ? null : d;
  }
  // Unix epoch: 10-digit (seconds) or 13-digit (milliseconds)
  if (/^\d{10}$/.test(s)) {
    const d = new Date(+s * 1000);
    if (d.getFullYear() >= 2000 && d.getFullYear() <= 2100) return d;
  }
  if (/^\d{13}$/.test(s)) {
    const d = new Date(+s);
    if (d.getFullYear() >= 2000 && d.getFullYear() <= 2100) return d;
  }
  return null;
}

function tryParseNumber(v) {
  if (v == null || v === "") return null;
  if (typeof v === "number") return isNaN(v) ? null : v;
  const s = String(v).trim().replace(/,/g, "");
  if (s === "") return null;
  const n = Number(s);
  return isNaN(n) ? null : n;
}

module.exports = {
  formatBytes, round, isNullish, median, quantile, std, mode,
  countBy, topValues, toJsonSafe, tryParseDate, tryParseNumber,
};
