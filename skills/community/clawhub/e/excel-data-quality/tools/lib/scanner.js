"use strict";
const U = require("./utils");
const { inferFieldType } = require("./profiler");

// ===================== Completeness =====================

function scanNullValues(headers, rows, fieldStats) {
  const issues = [];
  const totalRows = rows.length;
  const totalCols = headers.length;
  const thresholds = { critical: 80, high: 50, medium: 20, low: 5 };
  const severityFields = { critical: [], high: [], medium: [], low: [] };
  const nullStats = {};

  for (const h of headers) {
    let count = 0;
    const indices = [];
    rows.forEach((r, i) => { if (U.isNullish(r[h])) { count++; if (indices.length < 100) indices.push(i); } });
    const pct = count / Math.max(totalRows, 1) * 100;
    nullStats[h] = { count, pct };
    if (pct >= thresholds.critical) severityFields.critical.push({ col: h, pct, count, indices });
    else if (pct >= thresholds.high) severityFields.high.push({ col: h, pct, count, indices });
    else if (pct >= thresholds.medium) severityFields.medium.push({ col: h, pct, count, indices });
    else if (pct >= thresholds.low) severityFields.low.push({ col: h, pct, count, indices });
  }

  const problemCount = Object.values(severityFields).reduce((s, a) => s + a.length, 0);
  const problemRatio = problemCount / Math.max(totalCols, 1);
  const weights = { critical: 4, high: 3, medium: 2, low: 1 };
  const totalWeight = Object.entries(severityFields).reduce((s, [k, v]) => s + v.length * weights[k], 0);
  const baseDeduction = Math.min(problemRatio * 40, 30);
  const severityBonus = totalCols > 0 ? Math.min(totalWeight / totalCols * 20, 20) : 0;
  const totalDeduction = baseDeduction + severityBonus;

  function allocDeduction(sev, list) {
    if (!list.length || !totalWeight) return;
    const perField = (weights[sev] * list.length / totalWeight * totalDeduction) / list.length;
    const maxPer = { critical: 10, high: 6, medium: 4, low: 2 }[sev];
    const sevMap = { critical: "critical", high: "high", medium: "medium", low: "low" };
    const titleMap = { critical: "Extremely High Null Rate", high: "High Null Rate", medium: "Multiple Null Values", low: "Few Null Values" };
    for (const f of list) {
      issues.push({
        id: `null_${sev}_${f.col}`, moduleId: "null_value", category: "completeness",
        severity: sevMap[sev], title: `[${f.col}] ${titleMap[sev]} (Missing Values)`,
        description: `Null values account for ${U.round(f.pct, 1)}% of the field`,
        affectedColumns: [f.col], affectedRows: f.count,
        affectedPercentage: U.round(f.pct, 1), affectedRowIndices: f.indices,
        suggestion: sev === "critical" ? "Consider removing this field or checking data collection" : "Check data source or fill missing values",
        deduction: U.round(Math.min(perField, maxPer), 2),
      });
    }
  }
  allocDeduction("critical", severityFields.critical);
  allocDeduction("high", severityFields.high);
  allocDeduction("medium", severityFields.medium);
  allocDeduction("low", severityFields.low);

  return { moduleId: "null_value", moduleName: "Null Value Check", issues };
}

function scanEmptyStrings(headers, rows) {
  const issues = [];
  const totalRows = rows.length;
  const totalCols = headers.length;
  const textCols = headers.filter(h => rows.some(r => typeof r[h] === "string"));
  const problems = [];

  for (const col of textCols) {
    let count = 0;
    const indices = [];
    const emptyVals = new Set(["", "nan", "none", "null", "NULL", "NaN"]);
    rows.forEach((r, i) => {
      if (r[col] != null && emptyVals.has(String(r[col]).trim())) { count++; if (indices.length < 100) indices.push(i); }
    });
    const pct = count / Math.max(totalRows, 1) * 100;
    if (pct >= 10) problems.push({ col, count, pct, indices });
  }

  if (problems.length) {
    const ratio = problems.length / Math.max(totalCols, 1);
    const totalDed = Math.min(ratio * 15 + 2, 10);
    const perField = totalDed / problems.length;
    for (const p of problems) {
      issues.push({
        id: `empty_str_${p.col}`, moduleId: "empty_string", category: "completeness",
        severity: "medium", title: `[${p.col}] Empty Strings Present`,
        description: `Found ${p.count} empty strings or pseudo-null values (${U.round(p.pct, 1)}%)`,
        affectedColumns: [p.col], affectedRows: p.count, affectedPercentage: U.round(p.pct, 1),
        affectedRowIndices: p.indices,
        suggestion: "Convert empty strings to true null values for unified processing",
        deduction: U.round(Math.min(perField, 3), 2),
      });
    }
  }
  return { moduleId: "empty_string", moduleName: "Empty String Check", issues };
}

function scanRowCompleteness(headers, rows) {
  const issues = [];
  const totalRows = rows.length;
  const totalCols = headers.length;

  let emptyRowCount = 0;
  const emptyIndices = [];
  let highNullCount = 0;
  const highNullIndices = [];

  rows.forEach((row, i) => {
    const nulls = headers.filter(h => U.isNullish(row[h])).length;
    if (nulls === totalCols) { emptyRowCount++; if (emptyIndices.length < 100) emptyIndices.push(i); }
    else if (nulls / totalCols > 0.5) { highNullCount++; if (highNullIndices.length < 100) highNullIndices.push(i); }
  });

  if (emptyRowCount > 0) {
    const pct = emptyRowCount / totalRows * 100;
    issues.push({
      id: "empty_rows", moduleId: "row_completeness", category: "completeness",
      severity: "high", title: "Completely Empty Rows Present",
      description: `Found ${emptyRowCount} completely empty rows (${U.round(pct, 1)}%)`,
      affectedRows: emptyRowCount, affectedPercentage: U.round(pct, 1),
      affectedRowIndices: emptyIndices,
      suggestion: "Consider removing completely empty rows",
      deduction: U.round(Math.min(pct / 100 * 20, 10), 2),
    });
  }
  if (highNullCount > 0) {
    issues.push({
      id: "high_null_rows", moduleId: "row_completeness", category: "completeness",
      severity: "info", title: "High Missing Rate Rows Present",
      description: `Found ${highNullCount} rows with >50% fields missing`,
      affectedRows: highNullCount, affectedPercentage: U.round(highNullCount / totalRows * 100, 1),
      affectedRowIndices: highNullIndices,
      suggestion: "Check data source for these rows", deduction: 0,
    });
  }
  return { moduleId: "row_completeness", moduleName: "Row Completeness Check", issues };
}

// ===================== Uniqueness =====================

function scanDuplicateRows(headers, rows) {
  const issues = [];
  const totalRows = rows.length;
  const seen = new Map();

  rows.forEach((row, i) => {
    const key = headers.map(h => String(row[h] ?? "")).join("\x00");
    if (!seen.has(key)) seen.set(key, []);
    seen.get(key).push(i);
  });

  let dupCount = 0;
  let dupGroups = 0;
  const dupIndices = [];
  for (const [, idxs] of seen) {
    if (idxs.length > 1) {
      dupGroups++;
      dupCount += idxs.length;
      for (const i of idxs) { if (dupIndices.length < 100) dupIndices.push(i); }
    }
  }

  if (dupCount > 0) {
    const pct = dupCount / totalRows * 100;
    const sev = pct > 10 ? "critical" : pct > 5 ? "high" : "medium";
    issues.push({
      id: "duplicate_rows", moduleId: "duplicate_row", category: "uniqueness",
      severity: sev, title: "Duplicate Rows Present",
      description: `Found ${dupCount} duplicate rows (${dupGroups} groups)`,
      affectedRows: dupCount, affectedPercentage: U.round(pct, 1),
      affectedRowIndices: dupIndices,
      suggestion: "Consider removing duplicate rows or checking data import",
      deduction: U.round(Math.min(pct * 0.5, 10), 2),
    });
  }
  return { moduleId: "duplicate_row", moduleName: "Duplicate Row Check", issues };
}

function scanPrimaryKey(headers, rows, fieldStats) {
  const issues = [];
  const totalRows = rows.length;
  const pkKeywords = [
    "id", "key", "code", "no", "pk", "uid", "uuid", "index",
    "编号", "编码", "序号",              // Chinese
    "番号", "コード",                   // Japanese
    "번호", "코드",                    // Korean
    "número", "código", "numéro",     // ES/PT/FR
    "nummer", "schlüssel",            // German
    "رقم",                            // Arabic
  ];

  const candidates = fieldStats.filter(f =>
    f.uniquePercentage > 95 && f.nullPercentage < 5 &&
    !["date", "datetime", "boolean"].includes(f.inferredType)
  ).sort((a, b) => {
    const aMatch = pkKeywords.some(k => a.name.toLowerCase().includes(k)) ? 1 : 0;
    const bMatch = pkKeywords.some(k => b.name.toLowerCase().includes(k)) ? 1 : 0;
    return (bMatch - aMatch) || (b.uniquePercentage - a.uniquePercentage);
  }).slice(0, 3);

  for (const fs of candidates) {
    const col = fs.name;
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v));
    const dupSet = new Set();
    const seen = new Set();
    const dupIndices = [];
    vals.forEach((v, i) => {
      const s = String(v);
      if (seen.has(s)) { dupSet.add(s); if (dupIndices.length < 100) dupIndices.push(i); }
      else seen.add(s);
    });

    if (dupSet.size > 0) {
      const dupCount = dupIndices.length;
      issues.push({
        id: `pk_duplicate_${col}`, moduleId: "primary_key", category: "uniqueness",
        severity: "high", title: `[${col}] Suspected Primary Key Has Duplicates`,
        description: `Potential primary key has ${dupCount} duplicate values`,
        affectedColumns: [col], affectedRows: dupCount, affectedRowIndices: dupIndices,
        examples: [...dupSet].slice(0, 5),
        suggestion: "Check source of duplicate data if this field should be unique",
        deduction: 5,
      });
    }
  }
  return { moduleId: "primary_key", moduleName: "Primary Key Uniqueness Check", issues };
}

// ===================== Consistency =====================

function scanDataTypeConsistency(headers, rows, fieldStats) {
  const issues = [];
  for (const fs of fieldStats) {
    if (fs.inferredType !== "string") continue;
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v));
    if (!vals.length) continue;
    const numCount = vals.filter(v => U.tryParseNumber(v) !== null).length;
    const numPct = numCount / vals.length * 100;
    if (numPct > 10 && numPct < 90) {
      issues.push({
        id: `mixed_type_${fs.name}`, moduleId: "dtype_consistency", category: "consistency",
        severity: "medium", title: `[${fs.name}] Mixed Data Types`,
        description: `Contains ${U.round(numPct, 1)}% numeric and ${U.round(100 - numPct, 1)}% text data`,
        affectedColumns: [fs.name], examples: vals.slice(0, 5),
        suggestion: "Consider unifying data types or splitting the field",
        deduction: 3,
      });
    }
  }
  return { moduleId: "dtype_consistency", moduleName: "Data Type Consistency", issues };
}

function scanCaseConsistency(headers, rows, fieldStats) {
  const issues = [];
  const catFields = fieldStats.filter(f => f.inferredType === "categorical");
  for (const fs of catFields) {
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v)).map(String);
    const uniq = [...new Set(vals)];
    const lowerMap = {};
    for (const v of uniq) {
      const lv = v.toLowerCase();
      if (!lowerMap[lv]) lowerMap[lv] = [];
      lowerMap[lv].push(v);
    }
    const caseIssues = Object.values(lowerMap).filter(a => a.length > 1);
    if (caseIssues.length) {
      issues.push({
        id: `case_inconsistent_${fs.name}`, moduleId: "case_consistency", category: "consistency",
        severity: "low", title: `[${fs.name}] Case Inconsistency`,
        description: `Found ${caseIssues.length} groups of values with inconsistent case`,
        affectedColumns: [fs.name], examples: caseIssues.slice(0, 3).map(String),
        suggestion: "Consider unifying case format", deduction: 1,
      });
    }
  }
  return { moduleId: "case_consistency", moduleName: "Case Consistency", issues };
}

function scanDateFormat(headers, rows, fieldStats) {
  const issues = [];
  const dateKeywords = [
    "date", "time", "period", "year", "month", "day", "week",
    "created", "updated", "timestamp", "start", "end",
    "日期", "时间", "年份", "月份",                 // Chinese
    "日付", "時間", "年", "月",                    // Japanese
    "날짜", "시간", "연도", "월",                   // Korean
    "fecha", "hora", "período",                   // Spanish
    "datum", "zeit", "monat",                     // German
    "تاريخ", "وقت",                               // Arabic
    "date", "heure", "mois",                      // French
    "data", "ora",                                // Italian
  ];
  const stdPatterns = [
    [/^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}/, "ISO DateTime"],
    [/^\d{4}-\d{2}-\d{2}/, "YYYY-MM-DD"],
    [/^\d{4}\/\d{2}\/\d{2}/, "YYYY/MM/DD"],
    [/^\d{4}\.\d{1,2}\.\d{1,2}$/, "YYYY.MM.DD"],
    [/^\d{1,2}\.\d{1,2}\.\d{4}$/, "DD.MM.YYYY"],
    [/^\d{1,2}\/\d{1,2}\/\d{4}/, "DD/MM/YYYY or MM/DD/YYYY"],
    [/^\d{1,2}-\d{1,2}-\d{4}$/, "DD-MM-YYYY"],
    [/^\d{8}$/, "YYYYMMDD"],
    [/^\d{4}年\d{1,2}月\d{1,2}日/, "YYYY年MM月DD日"],
    [/^\d{4}년\s?\d{1,2}월\s?\d{1,2}일/, "YYYY년MM월DD일"],
    [/^令和\d{1,2}年/, "JP Era (Reiwa)"],
    [/^\d{1,2}[-\s][A-Za-z]{3,}[-\s]\d{4}$/, "DD-Mon-YYYY"],
    [/^[A-Za-z]{3,}\s+\d{1,2},?\s+\d{4}$/, "Mon DD, YYYY"],
    [/^\d{10}$/, "Unix Epoch (s)"],
    [/^\d{13}$/, "Unix Epoch (ms)"],
  ];

  const dateFields = fieldStats.filter(f => ["date", "datetime"].includes(f.inferredType));
  const dateNames = new Set(dateFields.map(f => f.name));
  const potentialDateFields = fieldStats.filter(f =>
    !dateNames.has(f.name) && f.inferredType === "string" &&
    dateKeywords.some(k => f.name.toLowerCase().includes(k))
  );

  for (const fs of [...dateFields, ...potentialDateFields]) {
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v)).map(String).slice(0, 500);
    if (!vals.length) continue;
    const formats = {};
    let nonStd = 0;
    for (const v of vals) {
      let found = false;
      for (const [re, name] of stdPatterns) {
        if (re.test(v)) { formats[name] = (formats[name] || 0) + 1; found = true; break; }
      }
      if (!found) { formats["Non-standard"] = (formats["Non-standard"] || 0) + 1; nonStd++; }
    }
    const uniqueFormats = Object.keys(formats).length;
    if (!dateNames.has(fs.name) && nonStd / vals.length > 0.1) {
      const sev = nonStd / vals.length > 0.5 ? "high" : "medium";
      issues.push({
        id: `date_format_nonstandard_${fs.name}`, moduleId: "date_format", category: "consistency",
        severity: sev, title: `[${fs.name}] Suspected Date Field Has Non-Standard Format`,
        description: `Field name suggests date/time but contains ${uniqueFormats} formats`,
        affectedColumns: [fs.name], examples: vals.filter(v => !stdPatterns.some(([re]) => re.test(v))).slice(0, 5),
        suggestion: "Convert to standard date format (YYYY-MM-DD)", deduction: sev === "high" ? 4 : 2,
      });
    } else if (dateNames.has(fs.name) && uniqueFormats > 1) {
      issues.push({
        id: `date_format_${fs.name}`, moduleId: "date_format", category: "consistency",
        severity: "medium", title: `[${fs.name}] Inconsistent Date Format`,
        description: `Detected ${uniqueFormats} date formats: ${Object.keys(formats).join(", ")}`,
        affectedColumns: [fs.name], examples: Object.keys(formats),
        suggestion: "Unify to ISO 8601 format (YYYY-MM-DD)", deduction: 2,
      });
    }
  }
  return { moduleId: "date_format", moduleName: "Date Format Consistency", issues };
}

// ===================== Validity =====================

function scanFormatValidity(headers, rows, fieldStats) {
  const issues = [];
  for (const fs of fieldStats) {
    const col = fs.name;
    const colLower = col.toLowerCase();
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v)).map(String);
    if (!vals.length) continue;

    const emailKw = [
      "email", "mail", "e-mail", "邮箱", "邮件",
      "メール", "이메일", "correo", "courriel", "بريد",
    ];
    if (emailKw.some(k => colLower.includes(k))) {
      const re = /^[\w.\-+]+@[\w.\-]+\.\w{2,}$/;
      const invalid = vals.filter(v => !re.test(v));
      if (invalid.length) {
        issues.push({
          id: `email_invalid_${col}`, moduleId: "format_validity", category: "validity",
          severity: "medium", title: `[${col}] Invalid Email Format`,
          description: `Found ${invalid.length} invalid email addresses`,
          affectedColumns: [col], affectedRows: invalid.length,
          affectedPercentage: U.round(invalid.length / vals.length * 100, 1),
          examples: invalid.slice(0, 5), suggestion: "Check email format", deduction: 2,
        });
      }
    }
    const phoneKw = [
      "phone", "mobile", "tel", "cell", "fax",
      "电话", "手机", "座机",                     // Chinese
      "電話", "携帯",                            // Japanese
      "전화", "휴대폰",                           // Korean
      "teléfono", "móvil", "celular",           // Spanish
      "téléphone", "portable",                  // French
      "telefon", "handy",                       // German
      "هاتف", "جوال", "موبايل",                   // Arabic
    ];
    if (phoneKw.some(k => colLower.includes(k))) {
      const phonePatterns = [
        /^1[3-9]\d{9}$/,                        // China mobile
        /^\d{3,4}-?\d{7,8}$/,                   // China landline
        /^0\d{1,4}-?\d{6,8}$/,                  // Japan / regional
        /^0[1-9]0-?\d{4}-?\d{4}$/,              // Japan mobile
        /^01[016789]-?\d{3,4}-?\d{4}$/,         // Korea mobile
        /^\+?\d{1,4}[\s\-]?\(?\d{1,5}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,5}$/, // Intl generic
        /^\(\d{3}\)\s?\d{3}-\d{4}$/,            // US (xxx) xxx-xxxx
        /^\d{3}-\d{3}-\d{4}$/,                  // US xxx-xxx-xxxx
        /^0\d{2,4}\s?\d{6,8}$/,                 // EU landline
        /^05\d{8}$/,                            // Middle East mobile (SA, AE)
      ];
      const invalid = vals.filter(v => {
        const cleaned = v.replace(/\s/g, "");
        return !phonePatterns.some(re => re.test(cleaned) || re.test(v));
      });
      if (invalid.length > vals.length * 0.1) {
        issues.push({
          id: `phone_invalid_${col}`, moduleId: "format_validity", category: "validity",
          severity: "medium", title: `[${col}] Suspicious Phone Format`,
          description: `Found ${invalid.length} possibly invalid phone numbers`,
          affectedColumns: [col], affectedRows: invalid.length, examples: invalid.slice(0, 5),
          suggestion: "Check phone number format and country code",
          deduction: 2,
        });
      }
    }
  }
  return { moduleId: "format_validity", moduleName: "Format Validity", issues };
}

function scanSpecialChars(headers, rows) {
  const issues = [];
  const totalRows = rows.length;
  const textCols = headers.filter(h => rows.some(r => typeof r[h] === "string"));
  const invisibleRe = /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/;

  for (const col of textCols) {
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v)).map(String);
    if (!vals.length) continue;

    const invisibleCount = vals.filter(v => invisibleRe.test(v)).length;
    if (invisibleCount > 0) {
      issues.push({
        id: `invisible_char_${col}`, moduleId: "special_char", category: "validity",
        severity: "medium", title: `[${col}] Contains Invisible Characters`,
        description: `Found ${invisibleCount} records containing invisible control characters`,
        affectedColumns: [col], affectedRows: invisibleCount,
        suggestion: "Clean invisible characters", deduction: 2,
      });
    }

    const leadTrail = vals.filter(v => /^\s/.test(v) || /\s$/.test(v)).length;
    if (leadTrail > vals.length * 0.05) {
      issues.push({
        id: `whitespace_${col}`, moduleId: "special_char", category: "validity",
        severity: "low", title: `[${col}] Extra Whitespace Present`,
        description: `Found ${leadTrail} records with leading/trailing whitespace`,
        affectedColumns: [col], affectedRows: leadTrail,
        suggestion: "Use TRIM to clean whitespace", deduction: 0.5,
      });
    }
  }
  return { moduleId: "special_char", moduleName: "Special Character Check", issues };
}

function scanRangeValidity(headers, rows, fieldStats) {
  const issues = [];
  const numFields = fieldStats.filter(f => ["integer", "float"].includes(f.inferredType));
  const posKw = [
    "count", "amount", "price", "quantity", "age", "salary", "weight", "height", "area", "size",
    "数量", "金额", "价格", "面积", "人数", "年龄",                     // Chinese
    "数量", "金額", "価格", "年齢",                                   // Japanese
    "수량", "금액", "가격", "나이",                                    // Korean
    "cantidad", "precio", "edad", "monto",                          // Spanish
    "betrag", "preis", "alter", "menge",                            // German
    "quantité", "prix", "âge", "montant",                           // French
    "كمية", "مبلغ", "سعر", "عمر",                                    // Arabic
  ];
  const pctKw = [
    "rate", "percent", "%", "ratio", "pct", "proportion",
    "率", "比例", "百分比",                                           // Chinese
    "率", "割合",                                                    // Japanese
    "율", "비율",                                                    // Korean
    "tasa", "porcentaje",                                           // Spanish
    "taux", "pourcentage",                                          // French
    "rate", "prozent", "anteil",                                    // German
    "نسبة", "معدل",                                                  // Arabic
  ];

  for (const fs of numFields) {
    const col = fs.name;
    const colLower = col.toLowerCase();
    const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null);
    if (nums.length < 10) continue;

    if (posKw.some(k => colLower.includes(k))) {
      const negCount = nums.filter(n => n < 0).length;
      if (negCount > 0) {
        issues.push({
          id: `negative_${col}`, moduleId: "range_validity", category: "validity",
          severity: "medium", title: `[${col}] Negative Values Present`,
          description: `Field should not be negative but has ${negCount} negative values`,
          affectedColumns: [col], affectedRows: negCount,
          examples: nums.filter(n => n < 0).slice(0, 5),
          suggestion: "Verify negative value data", deduction: 2,
        });
      }
    }
    if (pctKw.some(k => colLower.includes(k))) {
      const oor = nums.filter(n => n < 0 || n > 100).length;
      if (oor > 0) {
        issues.push({
          id: `percent_range_${col}`, moduleId: "range_validity", category: "validity",
          severity: "high", title: `[${col}] Percentage Out of Range`,
          description: `Found ${oor} values outside 0-100 range`,
          affectedColumns: [col], affectedRows: oor,
          suggestion: "Percentage should be between 0-100", deduction: 3,
        });
      }
    }
  }
  return { moduleId: "range_validity", moduleName: "Numeric Range Validity", issues };
}

// ===================== Accuracy =====================

function scanOutliers(headers, rows, fieldStats) {
  const issues = [];
  const numFields = fieldStats.filter(f => ["integer", "float"].includes(f.inferredType));
  const idKw = ["id", "code", "编号", "编码", "no"];
  const iqrMultiplier = 2.0;

  for (const fs of numFields) {
    const col = fs.name;
    if (idKw.some(k => col.toLowerCase().endsWith(k))) continue;
    const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null);
    if (nums.length < 20) continue;

    const Q1 = U.quantile(nums, 0.25);
    const Q3 = U.quantile(nums, 0.75);
    const IQR = Q3 - Q1;
    if (IQR === 0) continue;

    const lower = Q1 - iqrMultiplier * IQR;
    const upper = Q3 + iqrMultiplier * IQR;
    const outliers = nums.filter(n => n < lower || n > upper);
    const pct = outliers.length / nums.length * 100;

    if (outliers.length > 0 && pct > 1) {
      const high = nums.filter(n => n > upper).length;
      const low = nums.filter(n => n < lower).length;
      let dir = "";
      if (high > 0 && low > 0) dir = ` (high: ${high}, low: ${low})`;
      else if (high > 0) dir = ` (all high, >${U.round(upper, 2)})`;
      else dir = ` (all low, <${U.round(lower, 2)})`;

      const sev = pct > 10 ? "high" : pct > 5 ? "medium" : "low";
      issues.push({
        id: `outlier_${col}`, moduleId: "outlier", category: "accuracy",
        severity: sev, title: `[${col}] Outliers Present`,
        description: `IQR×${iqrMultiplier} detected ${outliers.length} outliers (${U.round(pct, 1)}%)${dir}`,
        affectedColumns: [col], affectedRows: outliers.length,
        affectedPercentage: U.round(pct, 1),
        examples: outliers.slice(0, 5).map(v => U.round(v, 2)),
        suggestion: "Judge whether outliers need handling based on business context",
        deduction: U.round(Math.min(pct * 0.15, 4), 2),
      });
    }
  }
  return { moduleId: "outlier", moduleName: "Outlier Detection", issues };
}

function scanRareValues(headers, rows, fieldStats) {
  const issues = [];
  const catFields = fieldStats.filter(f => f.inferredType === "categorical" && f.uniqueCount < 50);
  const rarePct = 0.5;

  for (const fs of catFields) {
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v)).map(String);
    if (!vals.length) continue;
    const freq = U.countBy(vals);
    const threshold = vals.length * (rarePct / 100);
    const rares = Object.entries(freq).filter(([, c]) => c < threshold);
    if (rares.length > 0 && rares.length < 10) {
      const totalAffected = rares.reduce((s, [, c]) => s + c, 0);
      issues.push({
        id: `rare_value_${fs.name}`, moduleId: "rare_value", category: "accuracy",
        severity: "info", title: `[${fs.name}] Rare Values Present`,
        description: `Found ${rares.length} values with frequency <${rarePct}%`,
        affectedColumns: [fs.name], affectedRows: totalAffected,
        examples: rares.map(([v]) => v),
        suggestion: "May be typos or abnormal data", deduction: 0.5,
      });
    }
  }
  return { moduleId: "rare_value", moduleName: "Rare Value Detection", issues };
}

// ===================== Timeliness =====================

function scanTimeFreshness(headers, rows, fieldStats) {
  const issues = [];
  const dateFields = fieldStats.filter(f => ["date", "datetime"].includes(f.inferredType));
  const now = new Date();

  for (const fs of dateFields) {
    const col = fs.name;
    const dates = rows.map(r => U.tryParseDate(r[col])).filter(d => d !== null);
    if (!dates.length) continue;

    const futureCount = dates.filter(d => d > now).length;
    if (futureCount > 0 && futureCount < dates.length * 0.5) {
      issues.push({
        id: `future_date_${col}`, moduleId: "time_freshness", category: "timeliness",
        severity: "low", title: `[${col}] Contains Future Dates`,
        description: `Found ${futureCount} future date records`,
        affectedColumns: [col], affectedRows: futureCount,
        suggestion: "Confirm if future dates are correct", deduction: 1,
      });
    }

    const oldThreshold = new Date("1990-01-01");
    const oldCount = dates.filter(d => d < oldThreshold).length;
    if (oldCount > 0) {
      issues.push({
        id: `old_date_${col}`, moduleId: "time_freshness", category: "timeliness",
        severity: "low", title: `[${col}] Contains Abnormal Historical Dates`,
        description: `Found ${oldCount} records dated before 1990`,
        affectedColumns: [col], affectedRows: oldCount,
        suggestion: "Verify historical date data", deduction: 0.5,
      });
    }
  }
  return { moduleId: "time_freshness", moduleName: "Data Timeliness", issues };
}

// ===================== Consistency (new) =====================

function scanFullwidthChars(headers, rows) {
  const issues = [];
  const fwDigit = /[\uff10-\uff19]/;
  const fwLetter = /[\uff21-\uff3a\uff41-\uff5a]/;
  const fwPunct = /[\uff01\uff0c\uff0e\uff1a\uff1b\uff1f\u3001\u3002]/;
  const fwAny = /[\uff01-\uff5e\u3000-\u303f]/;

  const textCols = headers.filter(h => rows.some(r => typeof r[h] === "string"));
  for (const col of textCols) {
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v)).map(String);
    if (!vals.length) continue;
    let digitCount = 0, letterCount = 0, punctCount = 0, totalAffected = 0;
    const indices = [];
    vals.forEach((v, i) => {
      if (fwAny.test(v)) {
        totalAffected++;
        if (indices.length < 100) indices.push(i);
        if (fwDigit.test(v)) digitCount++;
        if (fwLetter.test(v)) letterCount++;
        if (fwPunct.test(v)) punctCount++;
      }
    });
    if (totalAffected === 0) continue;
    const pct = totalAffected / vals.length * 100;
    const parts = [];
    if (digitCount) parts.push(`digits: ${digitCount}`);
    if (letterCount) parts.push(`letters: ${letterCount}`);
    if (punctCount) parts.push(`punctuation: ${punctCount}`);
    const sev = pct > 30 ? "high" : pct > 5 ? "medium" : "low";
    issues.push({
      id: `fullwidth_${col}`, moduleId: "fullwidth_char", category: "consistency",
      severity: sev, title: `[${col}] Full-Width Characters Detected`,
      description: `${totalAffected} values (${U.round(pct, 1)}%) contain full-width characters (${parts.join(", ")})`,
      affectedColumns: [col], affectedRows: totalAffected,
      affectedPercentage: U.round(pct, 1), affectedRowIndices: indices,
      examples: vals.filter(v => fwAny.test(v)).slice(0, 5),
      suggestion: "Convert full-width characters to half-width for consistent processing",
      deduction: U.round(Math.min(pct * 0.1, 4), 2),
    });
  }
  return { moduleId: "fullwidth_char", moduleName: "Full-Width Character Detection", issues };
}

// ===================== Validity (new) =====================

function scanEncodingIssues(headers, rows, parseInfo) {
  const issues = [];
  const mojibakePatterns = [
    /\ufffd{2,}/,                             // Unicode replacement chars (any encoding)
    /[\u0080-\u009f]/,                        // C1 control chars (should never appear)
    // GBK/GB2312 read as UTF-8 (Chinese)
    /[\u00c0-\u00c3][\u00a0-\u00bf]{1,2}/,
    /\u00e4\u00b8[\u00a0-\u00bf]/,
    /\u00e6[\u00a0-\u00bf]{2}/,
    /\u00c2[\u00a0-\u00bf]/,
    // Shift_JIS read as UTF-8 (Japanese)
    /\u0082[\u00a0-\u00ff]/,
    /\u0083[\u00a0-\u00ff]/,
    // EUC-KR read as UTF-8 (Korean)
    /[\u00b0-\u00c8][\u00a1-\u00fe]/,
    // ISO-8859-1 / Windows-1252 read as UTF-8 (European accented text)
    /Ã[\u00a0-\u00bf]/,
    /Ã©|Ã¨|Ã¤|Ã¶|Ã¼|Ã±|Ã§|Ã¡|Ã³/,
    // Windows-1256 read as UTF-8 (Arabic)
    /[\u00c7\u00c8][\u00a0-\u00bf]{2,}/,
  ];

  if (parseInfo && parseInfo.mojibakeDetected) {
    issues.push({
      id: "encoding_global", moduleId: "encoding_issue", category: "validity",
      severity: "critical", title: "Suspected Encoding / Mojibake Issue",
      description: "File may have been read with incorrect encoding. Garbled character patterns detected during parsing.",
      suggestion: "Re-save the file as UTF-8 or specify the correct encoding",
      deduction: 10,
    });
    return { moduleId: "encoding_issue", moduleName: "Encoding / Mojibake Detection", issues };
  }

  const textCols = headers.filter(h => rows.some(r => typeof r[h] === "string"));
  for (const col of textCols) {
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v)).map(String).slice(0, 500);
    if (!vals.length) continue;
    let hitCount = 0;
    const indices = [];
    vals.forEach((v, i) => {
      if (mojibakePatterns.some(re => re.test(v))) {
        hitCount++;
        if (indices.length < 100) indices.push(i);
      }
    });
    if (hitCount === 0) continue;
    const pct = hitCount / vals.length * 100;
    if (pct < 2) continue;
    const sev = pct > 20 ? "critical" : pct > 5 ? "high" : "medium";
    issues.push({
      id: `encoding_${col}`, moduleId: "encoding_issue", category: "validity",
      severity: sev, title: `[${col}] Suspected Garbled Text (Mojibake)`,
      description: `${hitCount} values (${U.round(pct, 1)}%) contain character patterns typical of encoding errors`,
      affectedColumns: [col], affectedRows: hitCount,
      affectedPercentage: U.round(pct, 1), affectedRowIndices: indices,
      examples: vals.filter(v => mojibakePatterns.some(re => re.test(v))).slice(0, 5),
      suggestion: "Re-open the source file with correct encoding (e.g., GBK for Chinese, Shift_JIS for Japanese, EUC-KR for Korean, ISO-8859-1 for European, Windows-1256 for Arabic)",
      deduction: U.round(Math.min(pct * 0.3, 8), 2),
    });
  }
  return { moduleId: "encoding_issue", moduleName: "Encoding / Mojibake Detection", issues };
}

// ===================== Completeness (new) =====================

function scanMergedCellPattern(headers, rows, parseInfo) {
  const issues = [];
  if (!parseInfo || !parseInfo.hasMergedCells) {
    return { moduleId: "merged_cell_pattern", moduleName: "Merged Cell Pattern Detection", issues };
  }

  for (const col of headers) {
    const vals = rows.map(r => r[col]);
    let streakCount = 0, longestStreak = 0, currentStreak = 0, lastNonNull = -1;
    let mergePatternHits = 0;

    for (let i = 0; i < vals.length; i++) {
      if (U.isNullish(vals[i])) {
        currentStreak++;
      } else {
        if (currentStreak >= 2 && lastNonNull >= 0) {
          mergePatternHits++;
          longestStreak = Math.max(longestStreak, currentStreak);
        }
        if (currentStreak > 0) streakCount++;
        currentStreak = 0;
        lastNonNull = i;
      }
    }
    if (currentStreak >= 2 && lastNonNull >= 0) {
      mergePatternHits++;
      longestStreak = Math.max(longestStreak, currentStreak);
    }

    if (mergePatternHits < 2) continue;

    const nullCount = vals.filter(v => U.isNullish(v)).length;
    const pct = nullCount / vals.length * 100;
    issues.push({
      id: `merged_pattern_${col}`, moduleId: "merged_cell_pattern", category: "completeness",
      severity: "high",
      title: `[${col}] Null Pattern Suggests Merged Cells`,
      description: `${mergePatternHits} contiguous null blocks detected (longest: ${longestStreak} rows). These nulls likely originate from merged cells and should be forward-filled, not treated as missing data.`,
      affectedColumns: [col], affectedRows: nullCount,
      affectedPercentage: U.round(pct, 1),
      suggestion: "Forward-fill (propagate the value above) instead of mean/median imputation",
      deduction: U.round(Math.min(mergePatternHits * 0.5, 5), 2),
    });
  }
  return { moduleId: "merged_cell_pattern", moduleName: "Merged Cell Pattern Detection", issues };
}

// ===================== Uniqueness (new) =====================

function scanFuzzyDuplicates(headers, rows, fieldStats) {
  const issues = [];
  const catFields = fieldStats.filter(f =>
    (f.inferredType === "categorical" || f.inferredType === "string") &&
    f.uniqueCount > 1 && f.uniqueCount <= 200
  );

  function normalize(s) {
    return String(s).normalize("NFC").toLowerCase().trim()
      .replace(/[\s\u3000]+/g, " ")
      .replace(/[.\-_'"()（）【】\[\]«»""'']/g, "")
      .replace(/[\u0610-\u061a\u064b-\u065f\u0670]/g, "")  // Arabic diacritics (tashkeel)
      .replace(/[\u0300-\u036f]/g, "");                     // Latin combining diacritics (é→e)
  }

  for (const fs of catFields) {
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v)).map(String);
    const uniq = [...new Set(vals)];
    const normMap = {};
    for (const v of uniq) {
      const n = normalize(v);
      if (!normMap[n]) normMap[n] = [];
      normMap[n].push(v);
    }
    const fuzzyGroups = Object.values(normMap).filter(a => a.length > 1);
    const caseGroups = fuzzyGroups.filter(group => {
      const lower = new Set(group.map(v => v.toLowerCase()));
      return lower.size === 1;
    });
    const nonCaseGroups = fuzzyGroups.filter(group => {
      const lower = new Set(group.map(v => v.toLowerCase()));
      return lower.size > 1 || group.some(v => v !== v.trim() || /[\s\u3000]{2,}/.test(v));
    });

    if (nonCaseGroups.length === 0 && caseGroups.length === 0) continue;
    const extraGroups = nonCaseGroups.length;
    if (extraGroups === 0) continue;

    issues.push({
      id: `fuzzy_dup_${fs.name}`, moduleId: "fuzzy_duplicate", category: "uniqueness",
      severity: extraGroups > 5 ? "high" : "medium",
      title: `[${fs.name}] Near-Duplicate Values Detected`,
      description: `${extraGroups} groups of values differ only by whitespace, punctuation, or formatting`,
      affectedColumns: [fs.name],
      examples: nonCaseGroups.slice(0, 3).map(g => g.join(" / ")),
      suggestion: "Normalize values to a consistent format",
      deduction: U.round(Math.min(extraGroups * 0.5, 4), 2),
    });
  }
  return { moduleId: "fuzzy_duplicate", moduleName: "Near-Duplicate Value Detection", issues };
}

// ===================== Consistency (new) =====================

function scanNumberWithUnit(headers, rows, fieldStats) {
  const issues = [];
  const unitPatterns = [
    // Currency prefix: ¥ $ € £ ₩ ₹ ₽ ₺ R$ ﷼ CHF kr
    { re: /^[¥$€£₩₹₽₺﷼]\s*[\d,.]+$/, label: "currency prefix" },
    { re: /^(?:R\$|CHF|kr|SEK|NOK|DKK|AED|SAR|KRW|JPY|INR|RUB|TRY|BRL|MXN|PLN|CZK|HUF|ILS)\s*[\d,.]+$/i, label: "currency code prefix" },
    // Currency suffix
    { re: /^[\d,.]+\s*[¥$€£₩₹₽₺﷼]$/, label: "currency suffix" },
    { re: /^[\d,.]+\s*(?:元|块|角|分|圆)$/, label: "CNY unit" },
    { re: /^[\d,.]+\s*(?:円|万円)$/, label: "JPY unit" },
    { re: /^[\d,.]+\s*(?:원|만원)$/, label: "KRW unit" },
    { re: /^[\d,.]+\s*(?:ريال|درهم|دينار|جنيه|ليرة)$/, label: "MENA currency" },
    { re: /^[\d,.]+\s*(?:EUR|USD|GBP|CHF|kr|руб|₽|zł|Kč|Ft)$/i, label: "currency code suffix" },
    // Magnitude
    { re: /^[\d,.]+\s*[万亿千百kKmMbBtT]$/, label: "magnitude suffix" },
    { re: /^[\d,.]+\s*(?:万|億|兆)$/, label: "CJK magnitude" },
    { re: /^[\d,.]+\s*(?:만|억)$/, label: "Korean magnitude" },
    { re: /^[\d,.]+\s*(?:mil|mln|mrd|bn|tn)$/i, label: "EU magnitude" },
    // Percentage
    { re: /^[\d,.]+\s*%$/, label: "percentage" },
    // Measurement units (international)
    { re: /^[\d,.]+\s*(?:个|件|台|套|箱|吨|只|条|把|张|份)$/, label: "CJK counter" },
    { re: /^[\d,.]+\s*(?:kg|lb|oz|g|mg|ton|tonnes?)$/i, label: "weight" },
    { re: /^[\d,.]+\s*(?:ml|l|L|gal|fl\.?\s?oz)$/i, label: "volume" },
    { re: /^[\d,.]+\s*(?:mm|cm|m|km|in|ft|yd|mi|miles?)$/i, label: "length" },
    { re: /^[\d,.]+\s*(?:m²|m2|km²|km2|sqft|sq\.?\s?m|ha|acres?)$/i, label: "area" },
    { re: /^[\d,.]+\s*(?:°[CF]|℃|℉)$/, label: "temperature" },
  ];

  const strFields = fieldStats.filter(f => f.inferredType === "string" && f.uniqueCount > 5);
  for (const fs of strFields) {
    const vals = rows.map(r => r[fs.name]).filter(v => !U.isNullish(v)).map(String);
    if (vals.length < 10) continue;

    const labelCounts = {};
    let totalHits = 0;
    for (const v of vals) {
      const trimmed = v.trim();
      for (const { re, label } of unitPatterns) {
        if (re.test(trimmed)) {
          labelCounts[label] = (labelCounts[label] || 0) + 1;
          totalHits++;
          break;
        }
      }
    }
    const pct = totalHits / vals.length * 100;
    if (pct < 10) continue;

    const labels = Object.entries(labelCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([l]) => l).join(", ");

    issues.push({
      id: `num_unit_${fs.name}`, moduleId: "number_unit", category: "consistency",
      severity: pct > 50 ? "high" : "medium",
      title: `[${fs.name}] Numbers with Embedded Units`,
      description: `${totalHits} values (${U.round(pct, 1)}%) are numeric but include units (${labels}), preventing numeric analysis`,
      affectedColumns: [fs.name], affectedRows: totalHits,
      affectedPercentage: U.round(pct, 1),
      examples: vals.filter(v => unitPatterns.some(({ re }) => re.test(v.trim()))).slice(0, 5),
      suggestion: "Separate numeric values from units for proper analysis",
      deduction: U.round(Math.min(pct * 0.08, 5), 2),
    });
  }
  return { moduleId: "number_unit", moduleName: "Number-with-Unit Detection", issues };
}

function scanCrossColumnLogic(headers, rows, fieldStats) {
  const issues = [];
  const colLower = {};
  for (const h of headers) colLower[h] = h.toLowerCase();

  // Date pair checks — multilingual start/end keywords
  const startKw = [
    "start", "begin", "from", "since",
    "开始", "起始",                   // Chinese
    "開始",                          // Japanese
    "시작",                          // Korean
    "inicio", "desde",               // Spanish
    "début", "depuis",               // French
    "anfang", "beginn", "von",       // German
    "بداية", "من",                    // Arabic
  ];
  const endKw = [
    "end", "finish", "to", "until", "expir",
    "结束", "截止", "终止",            // Chinese
    "終了", "終わり",                  // Japanese
    "종료", "끝",                     // Korean
    "fin", "hasta",                  // Spanish
    "fin", "jusqu",                  // French
    "ende", "bis",                   // German
    "نهاية", "إلى",                   // Arabic
  ];

  const datePairs = [];
  const dateFields = fieldStats.filter(f => ["date", "datetime"].includes(f.inferredType));
  const dateNames = dateFields.map(f => f.name);
  for (let i = 0; i < dateNames.length; i++) {
    for (let j = i + 1; j < dateNames.length; j++) {
      const a = colLower[dateNames[i]], b = colLower[dateNames[j]];
      const aIsStart = startKw.some(k => a.includes(k));
      const aIsEnd = endKw.some(k => a.includes(k));
      const bIsStart = startKw.some(k => b.includes(k));
      const bIsEnd = endKw.some(k => b.includes(k));
      if (aIsStart && bIsEnd) datePairs.push([dateNames[i], dateNames[j]]);
      else if (bIsStart && aIsEnd) datePairs.push([dateNames[j], dateNames[i]]);
    }
  }

  for (const [startCol, endCol] of datePairs) {
    let violations = 0;
    const indices = [];
    rows.forEach((r, i) => {
      const s = U.tryParseDate(r[startCol]);
      const e = U.tryParseDate(r[endCol]);
      if (s && e && e < s) { violations++; if (indices.length < 100) indices.push(i); }
    });
    if (violations > 0) {
      issues.push({
        id: `date_order_${startCol}_${endCol}`, moduleId: "cross_column_logic", category: "consistency",
        severity: violations > rows.length * 0.05 ? "high" : "medium",
        title: `[${startCol}] > [${endCol}] — Date Order Violation`,
        description: `${violations} rows have start date after end date`,
        affectedColumns: [startCol, endCol], affectedRows: violations,
        affectedRowIndices: indices,
        suggestion: "Check if start/end dates are swapped",
        deduction: U.round(Math.min(violations / rows.length * 30, 5), 2),
      });
    }
  }

  // Numeric total checks
  const numFields = fieldStats.filter(f => ["integer", "float"].includes(f.inferredType));
  const numNames = numFields.map(f => f.name);
  const totalKw = [
    "total", "sum", "grand",
    "合计", "总计", "总额", "总和",             // Chinese
    "合計", "総計", "総額",                    // Japanese
    "합계", "총액", "총합",                     // Korean
    "total", "suma",                          // Spanish
    "total", "somme",                         // French
    "gesamt", "summe",                        // German
    "المجموع", "الإجمالي",                      // Arabic
  ];

  for (const tName of numNames) {
    const tLower = colLower[tName];
    if (!totalKw.some(k => tLower.includes(k))) continue;

    const candidates = numNames.filter(n => n !== tName && !totalKw.some(k => colLower[n].includes(k)));
    if (candidates.length < 2 || candidates.length > 5) continue;

    let matchCount = 0, mismatchCount = 0;
    const indices = [];
    rows.forEach((r, i) => {
      const totalVal = U.tryParseNumber(r[tName]);
      if (totalVal === null) return;
      const partSum = candidates.reduce((s, c) => {
        const v = U.tryParseNumber(r[c]);
        return v !== null ? s + v : s;
      }, 0);
      if (Math.abs(totalVal - partSum) < 0.01) matchCount++;
      else { mismatchCount++; if (indices.length < 100) indices.push(i); }
    });

    if (matchCount > 0 && mismatchCount > 0 && mismatchCount / (matchCount + mismatchCount) > 0.05) {
      issues.push({
        id: `sum_mismatch_${tName}`, moduleId: "cross_column_logic", category: "consistency",
        severity: "medium",
        title: `[${tName}] Sum Mismatch with Component Columns`,
        description: `${mismatchCount} rows where total does not equal sum of parts (${candidates.join(" + ")})`,
        affectedColumns: [tName, ...candidates], affectedRows: mismatchCount,
        affectedRowIndices: indices,
        suggestion: "Verify the calculation formula for the total column",
        deduction: U.round(Math.min(mismatchCount / rows.length * 20, 4), 2),
      });
    }
  }

  return { moduleId: "cross_column_logic", moduleName: "Cross-Column Logical Consistency", issues };
}

// ===================== Validity (new) =====================

function scanIdChecksum(headers, rows, fieldStats) {
  const issues = [];
  const idCardRe = /^\d{17}[\dXx]$/;
  const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
  const checkChars = "10X98765432";

  function validateIdCard(id) {
    const s = String(id);
    if (!idCardRe.test(s)) return false;
    let sum = 0;
    for (let i = 0; i < 17; i++) sum += parseInt(s[i], 10) * weights[i];
    return checkChars[sum % 11] === s[17].toUpperCase();
  }

  for (const fs of fieldStats) {
    if (!fs.detectedPatterns || !fs.detectedPatterns.includes("id_card_cn")) continue;
    const col = fs.name;
    const vals = rows.map(r => r[col]).filter(v => !U.isNullish(v)).map(String);
    if (!vals.length) continue;

    const idVals = vals.filter(v => idCardRe.test(v));
    if (idVals.length < 5) continue;

    let invalidCount = 0;
    const indices = [];
    idVals.forEach((v, i) => {
      if (!validateIdCard(v)) { invalidCount++; if (indices.length < 100) indices.push(i); }
    });

    if (invalidCount === 0) continue;
    const pct = invalidCount / idVals.length * 100;
    issues.push({
      id: `id_checksum_${col}`, moduleId: "id_checksum", category: "validity",
      severity: pct > 20 ? "high" : "medium",
      title: `[${col}] Invalid ID Card Checksums`,
      description: `${invalidCount} of ${idVals.length} ID card numbers fail checksum validation (${U.round(pct, 1)}%)`,
      affectedColumns: [col], affectedRows: invalidCount,
      affectedPercentage: U.round(pct, 1), affectedRowIndices: indices,
      suggestion: "Verify ID card numbers — these may be fabricated or mistyped",
      deduction: U.round(Math.min(pct * 0.1, 5), 2),
    });
  }
  return { moduleId: "id_checksum", moduleName: "ID Card Checksum Validation", issues };
}

// ===================== Accuracy (new) =====================

function scanValueUniformity(headers, rows, fieldStats) {
  const issues = [];
  const numFields = fieldStats.filter(f => ["integer", "float"].includes(f.inferredType));

  for (const fs of numFields) {
    const col = fs.name;
    const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null);
    if (nums.length < 20) continue;

    // Zero-variance: all values identical
    const uniq = new Set(nums);
    if (uniq.size === 1) {
      issues.push({
        id: `uniform_constant_${col}`, moduleId: "value_uniformity", category: "accuracy",
        severity: "medium",
        title: `[${col}] Constant Value — Zero Variance`,
        description: `All ${nums.length} values are identical (${[...uniq][0]}). This column carries no analytical information.`,
        affectedColumns: [col], affectedRows: nums.length,
        suggestion: "Consider excluding this column from analysis",
        deduction: 2,
      });
      continue;
    }

    // Dominant single value
    const freq = {};
    for (const n of nums) freq[n] = (freq[n] || 0) + 1;
    const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);
    const [topVal, topCount] = sorted[0];
    const topPct = topCount / nums.length * 100;

    if (topPct > 80 && nums.length > 50) {
      issues.push({
        id: `uniform_dominant_${col}`, moduleId: "value_uniformity", category: "accuracy",
        severity: "low",
        title: `[${col}] Dominant Repeated Value`,
        description: `${U.round(topPct, 1)}% of values are ${topVal} (${topCount}/${nums.length}). Low variance may indicate data collection issues.`,
        affectedColumns: [col], affectedRows: topCount,
        affectedPercentage: U.round(topPct, 1),
        suggestion: "Verify if the data source is recording values correctly",
        deduction: U.round(Math.min((topPct - 80) * 0.05, 2), 2),
      });
    }
  }
  return { moduleId: "value_uniformity", moduleName: "Value Uniformity Detection", issues };
}

// ===================== Main Scanner =====================

function scan(headers, rows, fieldStats, parseInfo) {
  const modules = [
    scanNullValues(headers, rows, fieldStats),
    scanEmptyStrings(headers, rows),
    scanRowCompleteness(headers, rows),
    scanMergedCellPattern(headers, rows, parseInfo || {}),
    scanDuplicateRows(headers, rows),
    scanPrimaryKey(headers, rows, fieldStats),
    scanFuzzyDuplicates(headers, rows, fieldStats),
    scanDataTypeConsistency(headers, rows, fieldStats),
    scanCaseConsistency(headers, rows, fieldStats),
    scanFullwidthChars(headers, rows),
    scanDateFormat(headers, rows, fieldStats),
    scanNumberWithUnit(headers, rows, fieldStats),
    scanCrossColumnLogic(headers, rows, fieldStats),
    scanFormatValidity(headers, rows, fieldStats),
    scanSpecialChars(headers, rows),
    scanEncodingIssues(headers, rows, parseInfo || {}),
    scanIdChecksum(headers, rows, fieldStats),
    scanRangeValidity(headers, rows, fieldStats),
    scanOutliers(headers, rows, fieldStats),
    scanRareValues(headers, rows, fieldStats),
    scanValueUniformity(headers, rows, fieldStats),
    scanTimeFreshness(headers, rows, fieldStats),
  ];

  const allIssues = [];
  for (const m of modules) {
    for (const issue of m.issues) allIssues.push(issue);
  }

  return { modules, issues: allIssues };
}

module.exports = { scan };
