#!/usr/bin/env node
"use strict";
const path = require("path");
const { parseFile } = require("./lib/parser");
const { profile } = require("./lib/profiler");

function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    process.stderr.write("Usage: data_profiler.js <file_path>\n");
    process.stderr.write("Returns JSON data profile (table stats, field stats, sample data, validity).\n");
    process.exit(1);
  }

  try {
    const resolved = path.resolve(filePath);
    const { headers, rows, parseInfo } = parseFile(resolved);
    const result = profile(headers, rows);
    result.parseInfo = parseInfo;
    result.fileName = path.basename(resolved);

    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + "\n");
    process.exit(1);
  }
}

main();
