#!/usr/bin/env node

import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const FETCH_SCRIPT = path.join(SCRIPT_DIR, "fetch_events.mjs");
const REPORT_SCRIPT = path.join(SCRIPT_DIR, "generate_report.mjs");

function usage(exitCode = 2) {
  console.error(
    [
      "Usage: run_full_report.mjs [options]",
      "",
      "Options:",
      "  --report-date <YYYY-MM-DD>  Report date (optional)",
      "  --recent-days <n>           Recent day window (default: 1, bounds: 1-7)",
      "  --max-page <n>              Max pages (default: 5 daily / 25 range)",
      "  --page-size <n>             Page size (default: 10)",
      "  --timeout-seconds <n>       Request timeout (default: 15)",
      "  --retry <n>                 Retry times (default: 3)",
      "  --delay-seconds <n>         Delay between page requests (default: 0)",
      "  --top-n <n>                 Render cap; 0 means all (default: 0)",
      "  -h, --help                  Show this help",
    ].join("\n")
  );
  process.exit(exitCode);
}

function parseArgs(argv) {
  const options = {
    reportDate: "",
    recentDays: "1",
    maxPage: "5",
    pageSize: "10",
    timeoutSeconds: "15",
    retry: "3",
    delaySeconds: "0",
    topN: "0",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") usage(0);

    if (arg === "--report-date") {
      options.reportDate = argv[i + 1] ?? "";
      i += 1;
      continue;
    }
    if (arg === "--recent-days") {
      options.recentDays = argv[i + 1] ?? options.recentDays;
      i += 1;
      continue;
    }
    if (arg === "--max-page") {
      options.maxPage = argv[i + 1] ?? options.maxPage;
      i += 1;
      continue;
    }
    if (arg === "--page-size") {
      options.pageSize = argv[i + 1] ?? options.pageSize;
      i += 1;
      continue;
    }
    if (arg === "--timeout-seconds") {
      options.timeoutSeconds = argv[i + 1] ?? options.timeoutSeconds;
      i += 1;
      continue;
    }
    if (arg === "--retry") {
      options.retry = argv[i + 1] ?? options.retry;
      i += 1;
      continue;
    }
    if (arg === "--delay-seconds") {
      options.delaySeconds = argv[i + 1] ?? options.delaySeconds;
      i += 1;
      continue;
    }
    if (arg === "--top-n") {
      options.topN = argv[i + 1] ?? options.topN;
      i += 1;
      continue;
    }
    console.error(`Unknown arg: ${arg}`);
    usage();
  }

  return options;
}

function run(options) {
  return new Promise((resolve, reject) => {
    const fetchArgs = [
      FETCH_SCRIPT,
      "--recent-days",
      options.recentDays,
      "--max-page",
      options.maxPage,
      "--page-size",
      options.pageSize,
      "--timeout-seconds",
      options.timeoutSeconds,
      "--retry",
      options.retry,
      "--delay-seconds",
      options.delaySeconds,
      "--stdout-json",
    ];
    if (options.reportDate) {
      fetchArgs.push("--report-date", options.reportDate);
    }

    const reportArgs = [
      REPORT_SCRIPT,
      "--input-json",
      "-",
      "--top-n",
      options.topN,
      "--stdout",
    ];

    const fetchProc = spawn(process.execPath, fetchArgs, {
      stdio: ["ignore", "pipe", "pipe"],
    });
    const reportProc = spawn(process.execPath, reportArgs, {
      stdio: ["pipe", "pipe", "pipe"],
    });

    fetchProc.stdout.pipe(reportProc.stdin);
    fetchProc.stderr.pipe(process.stderr);
    reportProc.stdout.pipe(process.stdout);
    reportProc.stderr.pipe(process.stderr);

    let fetchCode = null;
    let reportCode = null;

    const maybeDone = () => {
      if (fetchCode === null || reportCode === null) return;
      if (fetchCode !== 0) {
        reject(new Error(`fetch step failed with code ${fetchCode}`));
        return;
      }
      if (reportCode !== 0) {
        reject(new Error(`report step failed with code ${reportCode}`));
        return;
      }
      resolve();
    };

    fetchProc.on("error", (err) => reject(err));
    reportProc.on("error", (err) => reject(err));
    fetchProc.on("close", (code) => {
      fetchCode = code ?? 1;
      maybeDone();
    });
    reportProc.on("close", (code) => {
      reportCode = code ?? 1;
      maybeDone();
    });
  });
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  await run(options);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});
