#!/usr/bin/env node
"use strict";
const path = require("path");
const { parseFile } = require("./lib/parser");
const { profile } = require("./lib/profiler");
const { scan } = require("./lib/scanner");
const { calculate } = require("./lib/scorer");

function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    process.stderr.write("Usage: quality_scanner.js <file_path>\n");
    process.stderr.write("Returns JSON quality scan (modules, issues, score).\n");
    process.exit(1);
  }

  try {
    const resolved = path.resolve(filePath);
    const { headers, rows, parseInfo } = parseFile(resolved);
    const prof = profile(headers, rows);

    if (!prof.dataValidity.canProceed) {
      process.stdout.write(JSON.stringify({
        error: "data_not_suitable",
        message: prof.dataValidity.blockReason,
        dataValidity: prof.dataValidity,
      }, null, 2) + "\n");
      process.exit(0);
    }

    const { modules, issues } = scan(headers, rows, prof.fieldStats, parseInfo);
    const score = calculate(issues);

    process.stdout.write(JSON.stringify({
      fileName: path.basename(resolved),
      parseInfo,
      tableStats: prof.tableStats,
      fieldStats: prof.fieldStats,
      sampleData: prof.sampleData,
      dataValidity: prof.dataValidity,
      modules: modules.map(m => ({
        moduleId: m.moduleId,
        moduleName: m.moduleName,
        issueCount: m.issues.length,
      })),
      issues,
      score,
    }, null, 2) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + "\n");
    process.exit(1);
  }
}

main();
