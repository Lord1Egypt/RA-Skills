import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { formatDivergenceRows, validateDivergenceLimit, validateDivergenceLabels } from "./divergence-flow.mjs";

export const DIVERGENCE_PAGE_SIZE = 20;

function invalidPage(message) {
  throw Object.assign(new Error(message), { code: "INVALID_INPUT" });
}

function pageResult(result, request, page, snapshotFile, fromCache) {
  const rows = result.rows_markdown ? result.rows_markdown.split("\n") : [];
  const totalPages = Math.max(1, Math.ceil(rows.length / DIVERGENCE_PAGE_SIZE));
  if (!Number.isInteger(page) || page < 1 || page > totalPages) invalidPage(`Page must be an integer from 1 to ${totalPages}`);
  const start = (page - 1) * DIVERGENCE_PAGE_SIZE;
  // Only this page's rendered rows enter model context. The full snapshot stays on disk.
  const { items, ...timestamps } = result.response.data.divergence;
  return {
    ...result,
    response: { ...result.response, data: { ...result.response.data, divergence: timestamps } },
    rows_markdown: rows.slice(start, start + DIVERGENCE_PAGE_SIZE).join("\n"),
    pagination: {
      page, page_size: DIVERGENCE_PAGE_SIZE, total_items: rows.length, total_pages: totalPages,
      requested_limit: request.limit ?? 10, from_cache: fromCache,
      ...(snapshotFile ? { snapshot_file: snapshotFile } : {}),
    },
  };
}

export function firstDivergencePage(result, request) {
  let snapshotFile;
  if (result.response.data.divergence.items.length > DIVERGENCE_PAGE_SIZE) {
    snapshotFile = join(mkdtempSync(join(tmpdir(), "cournot-divergence-")), "snapshot.json");
    writeFileSync(snapshotFile, JSON.stringify({ version: 1, result, request }), { mode: 0o600, flag: "wx" });
  }
  return pageResult(result, request, 1, snapshotFile, false);
}

export function readDivergencePage(snapshotFile, page) {
  if (!Number.isInteger(page) || page < 1 || page > 5) invalidPage("Page must be an integer from 1 to 5");
  if (typeof snapshotFile !== "string" || !snapshotFile.trim()) invalidPage("Provide the saved divergence snapshot file");
  let snapshot;
  try { snapshot = JSON.parse(readFileSync(snapshotFile, "utf8")); }
  catch { invalidPage("Saved divergence snapshot is unavailable or invalid; do not query again automatically"); }
  if (snapshot?.version !== 1 || snapshot.result?.state !== "complete" || !snapshot.request) {
    invalidPage("Invalid saved divergence snapshot; do not query again automatically");
  }
  validateDivergenceLimit(snapshot.request.limit);
  validateDivergenceLabels(snapshot.request.labels);
  const rows = formatDivergenceRows(snapshot.result.response, snapshot.request);
  if (rows !== snapshot.result.rows_markdown) invalidPage("Saved divergence rows do not match their source data");
  return pageResult(snapshot.result, snapshot.request, page, snapshotFile, true);
}
