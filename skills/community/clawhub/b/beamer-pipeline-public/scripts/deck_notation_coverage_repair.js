#!/usr/bin/env node
/**
 * deck_notation_coverage_repair.js — Deterministic notation_coverage repair
 *
 * Wraps slide_symbol_scanner.js for first_defined/used_slide_ids fixup, then
 * handles generic-index entries (e.g. \alpha_i) that cover specific subscripts
 * (\alpha_1, \alpha_2) but can't be matched literally in frame text.
 *
 * Usage:
 *   node deck_notation_coverage_repair.js <output-directory> [--dry-run]
 */

"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

function repairNotationCoverage(outputDirectory, options = {}) {
  const dryRun = options.dryRun !== false;
  const report = {
    summary: {
      output_directory: outputDirectory,
      dry_run: dryRun,
      scanner_applied: false,
      scanner_fixes: 0,
      generic_symbols_handled: 0,
      total_applied: 0,
      slides_json_modified: false,
    },
    scanner: null,
    generic: [],
  };

  const slidesPath = path.join(outputDirectory, "slides.json");
  if (!fs.existsSync(slidesPath)) {
    report.summary.error = "slides.json not found";
    return report;
  }

  const scannerScript = path.join(__dirname, "slide_symbol_scanner.js");
  const argv = [scannerScript, dryRun ? "--check" : "--fix", slidesPath];

  let scanner;
  try {
    scanner = spawnSync("node", argv, { encoding: "utf8", timeout: 60000 });
  } catch (err) {
    report.summary.error = `scanner_exec_failed: ${err.message}`;
    return report;
  }

  report.scanner = {
    stdout: (scanner.stdout || "").trim(),
    stderr: (scanner.stderr || "").trim(),
    exitCode: scanner.status ?? null,
  };

  if (scanner.status !== 0) {
    report.summary.error = `scanner_exit_code=${scanner.status}`;
    return report;
  }

  report.summary.scanner_applied = true;
  const scannerOutput = scanner.stdout || "";
  const fixMatches = scannerOutput.match(/(\d+)\s*total\s*fix/i);
  report.summary.scanner_fixes = fixMatches ? Number(fixMatches[1]) : 0;

  // ─── Handle generic-index entries ──────────────────────────────
  // Run detection even in dry-run to report what would change
  if (fs.existsSync(slidesPath)) {
    let slidesDoc;
    try {
      slidesDoc = JSON.parse(fs.readFileSync(slidesPath, "utf8"));
    } catch {
      // fall through to return
    }
    if (slidesDoc) {
      const notationCoverage = Array.isArray(slidesDoc.notation_coverage)
        ? slidesDoc.notation_coverage
        : [];

      if (notationCoverage.length > 0) {
        const genericHandled = handleGenericIndexEntries(notationCoverage, slidesDoc);
        report.summary.generic_symbols_handled = genericHandled;
        report.generic = genericHandled > 0
          ? notationCoverage
              .filter((e) => e && typeof e === "object" && e.status === "generic_placeholder")
              .map((e) => ({
                symbol: e.symbol,
                status: e.status,
                notes: e.notes,
              }))
          : [];

        if (!dryRun && genericHandled > 0) {
          slidesDoc.notation_coverage = notationCoverage;
          slidesDoc.notation_coverage_last_fixed_by = "deck_notation_coverage_repair";
          slidesDoc.notation_coverage_last_fixed_at = new Date().toISOString();
          fs.writeFileSync(slidesPath, JSON.stringify(slidesDoc, null, 2), "utf8");
          report.summary.slides_json_modified = true;
        }
      }
    }
  }

  report.summary.total_applied = report.summary.scanner_fixes + report.summary.generic_symbols_handled;
  return report;
}

/**
 * Generic-index symbols like \alpha_i, \beta_i carry semantic meaning ("any
 * family member") but cannot be matched literally against frame text where
 * only \alpha_1, \alpha_2 etc. appear. We mark these as status=generic_placeholder
 * so the validator skips literal visibility checks while preserving audit.
 */
function handleGenericIndexEntries(notationCoverage, slidesDoc) {
  const slides = Array.isArray(slidesDoc.slides) ? slidesDoc.slides : [];
  const handled = [];

  for (const entry of notationCoverage) {
    if (!entry || typeof entry !== "object") continue;
    const symbol = String(entry.symbol || "").trim();
    if (!symbol) continue;

    // Detect generic index patterns: \alpha_i, \beta_{i}, x_n, etc.
    const genericMatch = symbol.match(
      /^(?:\\([A-Za-z]+)|([A-Za-z]+)|([αβγδθφνμξεωΩΔ]))_\{?(i|j|k|n|m)\}?$/
    );
    if (!genericMatch) continue;

    const baseName = genericMatch[1] || genericMatch[2] || genericMatch[3];
    const genericIndex = genericMatch[4];

    // Find specific subscripts already tracked, e.g. \alpha_1, \alpha_2
    const specificSubscripts = notationCoverage.filter(
      (other) => other !== entry
        && other
        && typeof other === "object"
        && String(other.symbol || "").match(
          new RegExp(`^(?:\\\\${baseName}|${baseName})_\\{?(\\d+)\\}?$`)
        )
    );

    // Mark generic entry as placeholder so validator doesn't flag it
    if (specificSubscripts.length > 0 && entry.status !== "generic_placeholder") {
      const specificIds = specificSubscripts
        .flatMap((e) => Array.isArray(e.used_slide_ids) ? e.used_slide_ids : [])
        .filter(Boolean);
      entry.status = "generic_placeholder";
      entry.notes = (entry.notes ? entry.notes + "; " : "")
        + `covers specific subscripts: ${specificSubscripts.map((e) => e.symbol).join(", ")}`;
      // Inherit used_slide_ids union from specific subscripts
      if (specificIds.length > 0) {
        entry.used_slide_ids = [...new Set(specificIds.map(String))];
      }
      handled.push(symbol);
    }
  }

  return handled.length;
}

// ─── CLI ────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  let dryRun = false;
  let outputDir = "";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--dry-run") dryRun = true;
    else if (!args[i].startsWith("--")) outputDir = args[i];
  }

  if (!outputDir) {
    console.error("Usage: node deck_notation_coverage_repair.js <output-directory> [--dry-run]");
    process.exit(1);
  }

  if (!fs.existsSync(outputDir) || !fs.statSync(outputDir).isDirectory()) {
    console.error("Directory not found:", outputDir);
    process.exit(1);
  }

  const report = repairNotationCoverage(outputDir, { dryRun });
  console.log(JSON.stringify(report, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = { repairNotationCoverage, handleGenericIndexEntries };
