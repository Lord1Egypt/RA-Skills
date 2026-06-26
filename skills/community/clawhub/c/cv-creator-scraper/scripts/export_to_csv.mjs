#!/usr/bin/env node
// Export search results or collection data to CSV file (incremental append mode)
//
// Usage:
//   echo '<json>' | node {baseDir}/scripts/export_to_csv.mjs '{"output":"creators.csv"}'
//   node {baseDir}/scripts/search_creators.mjs '...' | node {baseDir}/scripts/export_to_csv.mjs '{"output":"creators.csv"}'
//
// Parameters:
//   output    — Output file path, default output.csv
//   mode      — Write mode: append (default) / overwrite

import { writeFileSync, appendFileSync, existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

function parseArgs() {
  const raw = process.argv[2];
  if (!raw) return {};
  try { return JSON.parse(raw); } catch { return {}; }
}

function flattenObject(obj, prefix = '') {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (Array.isArray(value)) {
      result[fullKey] = value.join('; ');
    } else if (value && typeof value === 'object') {
      Object.assign(result, flattenObject(value, fullKey));
    } else {
      result[fullKey] = value;
    }
  }
  return result;
}

function escapeCSV(value) {
  if (value === null || value === undefined) return '';
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function rowToCSV(headers, row) {
  return headers.map(h => escapeCSV(row[h])).join(',');
}

// Read JSON from stdin
let input = '';
for await (const chunk of process.stdin) {
  input += chunk;
}

let json;
try {
  json = JSON.parse(input);
} catch {
  console.error('Error: stdin input is not valid JSON');
  process.exit(1);
}

// Extract data array
let rows = [];
if (Array.isArray(json.data)) {
  rows = json.data;
} else if (json.data?.items && Array.isArray(json.data.items)) {
  rows = json.data.items;
} else if (Array.isArray(json)) {
  rows = json;
} else {
  console.error('Error: cannot extract data array from JSON');
  process.exit(1);
}

if (rows.length === 0) {
  console.error('Warning: data is empty, nothing to export');
  process.exit(0);
}

const params = parseArgs();
const outputPath = resolve(params.output || 'output.csv');
const mode = params.mode || 'append';

// Flatten all rows
const flatRows = rows.map(r => flattenObject(r));

// Collect all headers
const allHeaders = [...new Set(flatRows.flatMap(r => Object.keys(r)))];

const fileExists = existsSync(outputPath);

if (mode === 'overwrite' || !fileExists) {
  // Write header + data (BOM for Excel UTF-8 compatibility)
  const bom = '\ufeff';
  const headerLine = allHeaders.map(escapeCSV).join(',');
  const dataLines = flatRows.map(r => rowToCSV(allHeaders, r)).join('\n');
  writeFileSync(outputPath, bom + headerLine + '\n' + dataLines + '\n', 'utf-8');
  console.error(`[export] ${fileExists ? 'Overwritten' : 'Created'} ${outputPath}, wrote ${rows.length} rows`);
} else {
  // Incremental append: read existing headers
  const existingContent = readFileSync(outputPath, 'utf-8');
  const firstLine = existingContent.split('\n')[0].replace(/^\ufeff/, '');
  const existingHeaders = firstLine.split(',').map(h => h.replace(/^"|"$/g, ''));

  // Check for new columns
  const newHeaders = allHeaders.filter(h => !existingHeaders.includes(h));
  if (newHeaders.length > 0) {
    console.error(`[export] Warning: new data contains ${newHeaders.length} new column(s) (${newHeaders.join(', ')}), ignored during append`);
  }

  // Append using existing header order
  const dataLines = flatRows.map(r => rowToCSV(existingHeaders, r)).join('\n');
  appendFileSync(outputPath, dataLines + '\n', 'utf-8');
  console.error(`[export] Appended ${rows.length} rows to ${outputPath}`);
}

// Output summary to stdout
console.log(JSON.stringify({
  success: true,
  file: outputPath,
  rows_written: rows.length,
  mode: mode === 'overwrite' || !fileExists ? 'created' : 'appended',
  total_columns: allHeaders.length,
}, null, 2));
