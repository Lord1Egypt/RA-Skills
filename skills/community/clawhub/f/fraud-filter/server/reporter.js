import { readFileSync, appendFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { hashEndpoint, extractHint, bucketPrice, getReporterHash, loadConfig } from "./trust-db.js";

const DEFAULT_PENDING_PATH = resolve(
  process.env.FRAUD_FILTER_PENDING ||
    new URL("../data/pending-reports.jsonl", import.meta.url).pathname
);

// --- Signal Construction ---

/**
 * Build an anonymous signal from a transaction report.
 *
 * @param {object} report
 * @param {string} report.endpoint_url - The full endpoint URL
 * @param {string} report.outcome - "success" | "post_payment_failure" | "pre_payment_failure"
 * @param {string|number} report.amount_usd - Transaction amount in USD
 * @param {string} [configPath] - Path to config for reporter hash
 * @returns {object} Anonymous signal ready for submission
 */
export function buildSignal(report, configPath) {
  const reporterHash = getReporterHash(configPath);
  const today = new Date().toISOString().slice(0, 10);

  return {
    endpoint_hash: "sha256:" + hashEndpoint(report.endpoint_url),
    outcome: report.outcome,
    amount_range: bucketPrice(report.amount_usd),
    timestamp_bucket: today,
    reporter_hash: reporterHash,
    skill_name: report.skill_name || null,
    reason: report.reason || null,
  };
}

// --- Pending Reports Queue ---

/**
 * Queue a report for later submission.
 * Deduplicates: one signal per reporter + endpoint + day + outcome.
 */
export function queueReport(report, pendingPath = DEFAULT_PENDING_PATH, configPath) {
  const signal = buildSignal(report, configPath);

  // Check for duplicates in pending queue
  const pending = readPendingReports(pendingPath);
  const isDup = pending.some(
    (p) =>
      p.endpoint_hash === signal.endpoint_hash &&
      p.outcome === signal.outcome &&
      p.timestamp_bucket === signal.timestamp_bucket &&
      p.reporter_hash === signal.reporter_hash
  );

  if (isDup) {
    return { queued: false, reason: "duplicate", signal };
  }

  const dir = dirname(pendingPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  const entry = {
    ...signal,
    queued_at: new Date().toISOString(),
    status: "pending",
    endpoint_hint: extractHint(report.endpoint_url),
    skill_name: report.skill_name || null,
    reason: report.reason || null,
  };

  appendFileSync(pendingPath, JSON.stringify(entry) + "\n", { mode: 0o600 });
  return { queued: true, signal };
}

/**
 * Read all pending reports from the queue.
 */
export function readPendingReports(pendingPath = DEFAULT_PENDING_PATH) {
  if (!existsSync(pendingPath)) return [];
  const content = readFileSync(pendingPath, "utf-8").trimEnd();
  if (!content) return [];
  return content.split("\n").map((line) => {
    try {
      return JSON.parse(line);
    } catch {
      return null;
    }
  }).filter(Boolean);
}

/**
 * Get count of pending reports by status.
 */
export function getPendingStatus(pendingPath = DEFAULT_PENDING_PATH) {
  const reports = readPendingReports(pendingPath);
  const pending = reports.filter((r) => r.status === "pending").length;
  const sent = reports.filter((r) => r.status === "sent").length;
  const failed = reports.filter((r) => r.status === "failed").length;
  return { total: reports.length, pending, sent, failed };
}

/**
 * Submit all pending reports to the reporting endpoint.
 * Returns { submitted, failed, skipped } counts.
 */
export async function submitPendingReports(pendingPath = DEFAULT_PENDING_PATH, configPath) {
  const config = loadConfig(configPath);

  if (!config.participate_in_network) {
    return { submitted: 0, failed: 0, skipped: 0, reason: "network_participation_disabled" };
  }

  const reports = readPendingReports(pendingPath);
  const pendingReports = reports.filter((r) => r.status === "pending");

  if (pendingReports.length === 0) {
    return { submitted: 0, failed: 0, skipped: 0 };
  }

  let submitted = 0;
  let failed = 0;

  for (const report of pendingReports) {
    try {
      const body = {
        endpoint_hash:   report.endpoint_hash,
        outcome:         report.outcome,
        amount_range:    report.amount_range,
        timestamp_bucket: report.timestamp_bucket,
        reporter_hash:   report.reporter_hash,
      };
      if (report.skill_name) body.skill_name = report.skill_name;
      if (report.reason) body.reason = report.reason;

      const response = await fetch(config.report_endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        report.status = "sent";
        report.sent_at = new Date().toISOString();
        submitted++;
      } else {
        report.status = "failed";
        report.error = `HTTP ${response.status}`;
        failed++;
      }
    } catch (err) {
      report.status = "failed";
      report.error = err.message;
      failed++;
    }
  }

  // Rewrite the pending file with updated statuses
  const dir = dirname(pendingPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const lines = reports.map((r) => JSON.stringify(r)).join("\n") + "\n";
  writeFileSync(pendingPath, lines, { mode: 0o600 });

  return { submitted, failed, skipped: 0 };
}

/**
 * Clear reports that have been successfully sent (older than 7 days).
 */
export function pruneSentReports(pendingPath = DEFAULT_PENDING_PATH) {
  const reports = readPendingReports(pendingPath);
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);

  const kept = reports.filter((r) => {
    if (r.status !== "sent") return true;
    if (!r.sent_at) return true;
    return new Date(r.sent_at) > cutoff;
  });

  const pruned = reports.length - kept.length;

  if (pruned > 0) {
    const dir = dirname(pendingPath);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    const lines = kept.length > 0 ? kept.map((r) => JSON.stringify(r)).join("\n") + "\n" : "";
    writeFileSync(pendingPath, lines, { mode: 0o600 });
  }

  return { pruned, remaining: kept.length };
}
