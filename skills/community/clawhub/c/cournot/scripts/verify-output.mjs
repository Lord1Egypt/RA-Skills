#!/usr/bin/env node

import { readFileSync, realpathSync } from "node:fs";
import { createHash } from "node:crypto";
import { DIVERGENCE_PAGE_SIZE } from "./divergence-pages.mjs";

// Check immutable data rows; the agent owns headings and explanatory prose.
try {
  const [sourcePath, draftPath, ...extra] = process.argv.slice(2);
  if (!sourcePath || !draftPath || extra.length) {
    throw new Error("Usage: verify-output.mjs <client-result.json> <final-draft.md>");
  }
  if (realpathSync(sourcePath) === realpathSync(draftPath)) {
    throw new Error("Use separate client-result and final-draft files.");
  }
  const result = JSON.parse(readFileSync(sourcePath, "utf8"));
  const draft = readFileSync(draftPath);
  if (result.state !== "complete" || typeof result.rows_markdown !== "string") {
    throw new Error("A successful client result with rows_markdown is required.");
  }
  const lines = draft.toString("utf8").split(/\r?\n/);
  if (!draft.toString("utf8").trim()) throw new Error("The final draft is empty.");
  const expected = result.rows_markdown ? result.rows_markdown.split("\n") : [];
  if (expected.length > DIVERGENCE_PAGE_SIZE) {
    throw new Error("Display only the current page, at most 20 markets per reply. Read the saved snapshot with divergence-page.");
  }
  const positions = lines.flatMap((line, index) => /^\|\s*\d+\s*\|/.test(line) ? [index] : []);
  const actual = positions.map(index => lines[index]);
  if (actual.length !== expected.length || actual.some((line, index) => line !== expected[index])) {
    throw Object.assign(new Error("Data rows differ from the client result. Restore every original row and URL before sending."),
      { code: "OUTPUT_MISMATCH" });
  }
  if (positions.length) {
    const first = positions[0];
    const header = (lines[first - 2] || "").trim().split(/(?<!\\)\|/);
    if (positions.some((position, index) => position !== first + index) ||
        !/^\|(?:\s*:?-{3,}:?\s*\|){9}\s*$/.test(lines[first - 1] || "") ||
        header.length !== 11 || header[0] || header[10] || header.slice(1, -1).some(cell => !cell.trim())) {
      throw new Error("Use one nine-column Markdown table with consecutive original data rows.");
    }
    if (lines[positions.at(-1) + 1]?.trim()) {
      throw new Error("Insert a blank line after the data rows so the footer renders outside the table.");
    }
  }
  console.error(JSON.stringify({ verified: true, rows: expected.length, bytes: draft.length,
    rows_sha256: createHash("sha256").update(result.rows_markdown).digest("hex"),
    sha256: createHash("sha256").update(draft).digest("hex") }));
  process.stdout.write(draft);
} catch (error) {
  console.error(JSON.stringify({ verified: false, code: error.code || "OUTPUT_CHECK_FAILED", message: error.message,
    ...(error.line ? { line: error.line } : {}) }));
  process.exitCode = 1;
}
