#!/usr/bin/env node
"use strict";
const path = require("path");
const { parseFile } = require("./lib/parser");

function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    process.stderr.write("Usage: excel_parser.js <file_path>\n");
    process.stderr.write("Supported: .csv, .tsv, .xlsx, .xls\n");
    process.exit(1);
  }

  try {
    const resolved = path.resolve(filePath);
    const { headers, rows, parseInfo } = parseFile(resolved);

    const result = {
      headers,
      rowCount: rows.length,
      columnCount: headers.length,
      parseInfo,
      preview: rows.slice(0, 5),
    };

    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + "\n");
    process.exit(1);
  }
}

main();
