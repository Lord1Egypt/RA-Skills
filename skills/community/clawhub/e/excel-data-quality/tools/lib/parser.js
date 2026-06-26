"use strict";
const fs = require("fs");
const path = require("path");
const XLSX = require("xlsx");

function parseFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".csv" || ext === ".tsv") return parseCsv(filePath, ext);
  if (ext === ".xlsx" || ext === ".xls") return parseExcel(filePath);
  throw new Error(`Unsupported file type: ${ext}. Supported: .csv, .tsv, .xlsx, .xls`);
}

function parseCsv(filePath, ext) {
  const parseInfo = { fileType: "csv", encoding: null, delimiter: null, hasHeader: true, warnings: [] };

  const buf = fs.readFileSync(filePath);
  let encoding = "utf-8";
  if (buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF) encoding = "utf-8";
  else if (buf[0] === 0xFF && buf[1] === 0xFE) encoding = "utf-16le";
  else if (buf[0] === 0xFE && buf[1] === 0xFF) encoding = "utf-16be";
  parseInfo.encoding = encoding;

  const wb = XLSX.readFile(filePath, { type: "file", codepage: 65001, raw: true, cellDates: false });
  const sheetName = wb.SheetNames[0];
  const sheet = wb.Sheets[sheetName];
  if (!sheet) throw new Error("Empty file — no data found");

  const jsonData = XLSX.utils.sheet_to_json(sheet, { defval: null, raw: true });
  if (!jsonData.length) {
    const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: null });
    if (rawData.length > 0) {
      parseInfo.hasHeader = false;
      parseInfo.warnings.push("No header detected, using row indices as column names");
      const headers = rawData[0].map((_, i) => `Column_${i + 1}`);
      const rows = rawData.slice(1).map(r => {
        const obj = {};
        headers.forEach((h, i) => { obj[h] = r[i] != null ? r[i] : null; });
        return obj;
      });
      return buildResult(headers, rows, parseInfo);
    }
    throw new Error("Empty file — no data found");
  }

  const headers = Object.keys(jsonData[0]);
  const unnamedCount = headers.filter(h => /^__EMPTY/.test(h) || /^Unnamed/.test(h)).length;
  if (unnamedCount === headers.length && jsonData.length > 0) {
    parseInfo.hasHeader = false;
    parseInfo.warnings.push("All columns unnamed, treating first row as data");
  }

  parseInfo.delimiter = ext === ".tsv" ? "\t" : ",";
  return buildResult(headers, jsonData, parseInfo);
}

function parseExcel(filePath) {
  const parseInfo = {
    fileType: "excel", sheetNames: [], activeSheet: null,
    hasMergedCells: false, mergedCellsCount: 0, warnings: [],
  };

  const wb = XLSX.readFile(filePath, { cellDates: true, cellNF: true });
  parseInfo.sheetNames = wb.SheetNames;
  const sheetName = wb.SheetNames[0];
  parseInfo.activeSheet = sheetName;
  const sheet = wb.Sheets[sheetName];
  if (!sheet) throw new Error("Empty workbook — no sheets found");

  if (sheet["!merges"] && sheet["!merges"].length > 0) {
    parseInfo.hasMergedCells = true;
    parseInfo.mergedCellsCount = sheet["!merges"].length;
    parseInfo.warnings.push(`Detected ${sheet["!merges"].length} merged cell regions (auto-filled by SheetJS)`);
  }

  if (wb.SheetNames.length > 1) {
    parseInfo.warnings.push(`Workbook has ${wb.SheetNames.length} sheets, analyzing first: ${sheetName}`);
  }

  const jsonData = XLSX.utils.sheet_to_json(sheet, { defval: null, raw: false });
  if (!jsonData.length) throw new Error("Sheet is empty — no data found");

  let headers = Object.keys(jsonData[0]);
  headers = ensureUniqueHeaders(headers);
  const rows = jsonData.map(row => {
    const obj = {};
    headers.forEach((h, i) => { obj[h] = row[Object.keys(row)[i]] != null ? row[Object.keys(row)[i]] : null; });
    return obj;
  });

  return buildResult(headers, rows, parseInfo);
}

function ensureUniqueHeaders(headers) {
  const seen = {};
  return headers.map(h => {
    const key = h == null ? "Column" : String(h);
    if (seen[key] != null) {
      seen[key]++;
      return `${key}_${seen[key]}`;
    }
    seen[key] = 0;
    return key;
  });
}

function buildResult(headers, rows, parseInfo) {
  parseInfo.rowCount = rows.length;
  parseInfo.columnCount = headers.length;
  parseInfo.mojibakeDetected = detectMojibake(headers, rows);
  return { headers, rows, parseInfo };
}

function detectMojibake(headers, rows) {
  const mojibakeRe = /[\ufffd]{2,}|[\u00c0-\u00c3][\u00a0-\u00bf]{1,2}|[\u0080-\u009f]/;
  let hits = 0;
  const sample = rows.slice(0, 100);
  for (const row of sample) {
    for (const h of headers) {
      const v = row[h];
      if (typeof v === "string" && mojibakeRe.test(v)) { hits++; break; }
    }
  }
  return hits > sample.length * 0.1;
}

module.exports = { parseFile };
