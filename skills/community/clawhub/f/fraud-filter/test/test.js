import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

import {
  sha256,
  normalizeUrl,
  hashEndpoint,
  extractHint,
  loadTrustDb,
  lookupEndpoint,
  checkEndpoint,
  scoreToRecommendation,
  checkPriceAnomaly,
  computeScore,
  deriveWarnings,
  getDbStatus,
  loadConfig,
  saveConfig,
  getReporterHash,
  bucketPrice,
  searchEndpoints,
} from "../server/trust-db.js";

import {
  buildSignal,
  queueReport,
  readPendingReports,
  getPendingStatus,
  pruneSentReports,
} from "../server/reporter.js";

// --- Sample trust DB for testing ---
const SAMPLE_DB = {
  version: "2026-03-15",
  generated_at: "2026-03-15T04:00:00Z",
  endpoint_count: 3,
  endpoints: {},
};

// We'll compute real hashes for test URLs
const TEST_URLS = {
  good: "https://api.stockdata.xyz/report/AAPL",
  bad: "https://shady-data.xyz/api/v2",
  new_ep: "https://brand-new.xyz/api",
};

describe("trust-db: hashing", () => {
  it("sha256 produces consistent hex output", () => {
    const h1 = sha256("test");
    const h2 = sha256("test");
    assert.equal(h1, h2);
    assert.equal(h1.length, 64);
  });

  it("normalizeUrl lowercases and strips query/fragment", () => {
    assert.equal(
      normalizeUrl("https://API.Example.COM/path?key=val#frag"),
      "https://api.example.com/path"
    );
  });

  it("normalizeUrl removes trailing slash", () => {
    assert.equal(
      normalizeUrl("https://example.com/path/"),
      "https://example.com/path"
    );
  });

  it("normalizeUrl keeps root slash", () => {
    const result = normalizeUrl("https://example.com/");
    assert.ok(result.endsWith("/"));
  });

  it("hashEndpoint produces consistent hashes for same URL", () => {
    const h1 = hashEndpoint("https://example.com/api");
    const h2 = hashEndpoint("https://EXAMPLE.COM/api");
    assert.equal(h1, h2);
  });

  it("hashEndpoint produces different hashes for different URLs", () => {
    const h1 = hashEndpoint("https://example.com/api");
    const h2 = hashEndpoint("https://example.com/other");
    assert.notEqual(h1, h2);
  });

  it("extractHint returns hostname only", () => {
    assert.equal(extractHint("https://api.example.com/path/to/resource?q=1"), "api.example.com");
  });
});

describe("trust-db: score computation", () => {
  const now = new Date("2026-03-15T12:00:00Z");

  it("computes high score for reliable endpoint", () => {
    const entry = {
      report_count: 347,
      success_rate: 0.97,
      price_p10_usd: 0.02,
      price_p90_usd: 0.05,
      first_seen: "2026-01-20",
      last_failure: "2026-03-01",
    };
    const score = computeScore(entry, now);
    assert.ok(score >= 80, `Expected >= 80, got ${score}`);
  });

  it("computes low score for unreliable endpoint", () => {
    const entry = {
      report_count: 12,
      success_rate: 0.42,
      price_p10_usd: 0.05,
      price_p90_usd: 2.00,
      first_seen: "2026-03-10",
      last_failure: "2026-03-15",
    };
    const score = computeScore(entry, now);
    assert.ok(score <= 35, `Expected <= 35, got ${score}`);
  });

  it("returns null for zero reports", () => {
    assert.equal(computeScore({ report_count: 0 }), null);
  });

  it("penalizes recent failures", () => {
    const base = {
      report_count: 100,
      success_rate: 0.95,
      price_p10_usd: 0.01,
      price_p90_usd: 0.02,
      first_seen: "2025-01-01",
    };
    const noFail = computeScore({ ...base, last_failure: null }, now);
    const recentFail = computeScore({ ...base, last_failure: "2026-03-15" }, now);
    assert.ok(noFail > recentFail, `No fail (${noFail}) should be > recent fail (${recentFail})`);
  });

  it("penalizes volatile pricing", () => {
    const stable = {
      report_count: 100, success_rate: 0.95,
      price_p10_usd: 0.04, price_p90_usd: 0.06,
      first_seen: "2025-01-01",
    };
    const volatile = {
      ...stable,
      price_p10_usd: 0.01, price_p90_usd: 1.00,
    };
    const s1 = computeScore(stable, now);
    const s2 = computeScore(volatile, now);
    assert.ok(s1 > s2, `Stable (${s1}) should be > volatile (${s2})`);
  });

  it("penalizes new endpoints", () => {
    const old = {
      report_count: 50, success_rate: 0.95,
      price_p10_usd: 0.01, price_p90_usd: 0.02,
      first_seen: "2025-01-01",
    };
    const young = { ...old, first_seen: "2026-03-14" };
    const s1 = computeScore(old, now);
    const s2 = computeScore(young, now);
    assert.ok(s1 > s2, `Old (${s1}) should be > young (${s2})`);
  });

  it("clamps score to 0-100", () => {
    const perfect = {
      report_count: 10000, success_rate: 1.0,
      price_p10_usd: 0.01, price_p90_usd: 0.02,
      first_seen: "2024-01-01",
    };
    const terrible = {
      report_count: 10000, success_rate: 0.0,
      price_p10_usd: 0.01, price_p90_usd: 100,
      first_seen: "2026-03-15", last_failure: "2026-03-15",
    };
    assert.ok(computeScore(perfect, now) <= 100);
    assert.ok(computeScore(terrible, now) >= 0);
  });
});

describe("trust-db: recommendations", () => {
  it("maps scores to correct recommendations", () => {
    assert.equal(scoreToRecommendation(94), "allow");
    assert.equal(scoreToRecommendation(70), "allow");
    assert.equal(scoreToRecommendation(69), "caution");
    assert.equal(scoreToRecommendation(40), "caution");
    assert.equal(scoreToRecommendation(39), "block");
    assert.equal(scoreToRecommendation(0), "block");
  });
});

describe("trust-db: warnings", () => {
  const now = new Date("2026-03-15T12:00:00Z");

  it("flags high failure rate", () => {
    const w = deriveWarnings({ success_rate: 0.5, report_count: 100 }, now);
    assert.ok(w.includes("high_failure_rate"));
  });

  it("flags volatile pricing", () => {
    const w = deriveWarnings({ success_rate: 0.9, price_p10_usd: 0.01, price_p90_usd: 1.00, report_count: 100 }, now);
    assert.ok(w.includes("volatile_pricing"));
  });

  it("flags recent complaints", () => {
    const w = deriveWarnings({ success_rate: 0.9, last_failure: "2026-03-14", report_count: 100 }, now);
    assert.ok(w.includes("recent_complaints"));
  });

  it("flags new endpoints", () => {
    const w = deriveWarnings({ success_rate: 0.9, first_seen: "2026-03-10", report_count: 100 }, now);
    assert.ok(w.includes("new_endpoint"));
  });

  it("flags limited data", () => {
    const w = deriveWarnings({ success_rate: 0.9, report_count: 3 }, now);
    assert.ok(w.includes("limited_data"));
  });

  it("returns no warnings for healthy endpoint", () => {
    const w = deriveWarnings({
      success_rate: 0.95, report_count: 100,
      price_p10_usd: 0.01, price_p90_usd: 0.02,
      first_seen: "2025-01-01", last_failure: "2025-01-01",
    }, now);
    assert.equal(w.length, 0);
  });
});

describe("trust-db: lookup and check", () => {
  let tmpDir;
  let dbPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-test-"));
    dbPath = join(tmpDir, "trust.json");

    // Create a test DB with real hashes
    const goodHash = hashEndpoint(TEST_URLS.good);
    const badHash = hashEndpoint(TEST_URLS.bad);

    const db = {
      ...SAMPLE_DB,
      endpoints: {
        [goodHash]: {
          url_hint: "stockdata.xyz",
          report_count: 347,
          success_rate: 0.97,
          median_price_usd: 0.03,
          price_p10_usd: 0.02,
          price_p90_usd: 0.05,
          first_seen: "2026-01-20",
          last_success: "2026-03-15",
          last_failure: "2026-03-14",
          failure_types: { post_payment: 8, pre_payment: 3 },
          warnings: [],
          score: 94,
        },
        [badHash]: {
          url_hint: "shady-data.xyz",
          report_count: 12,
          success_rate: 0.42,
          median_price_usd: 0.50,
          price_p10_usd: 0.05,
          price_p90_usd: 2.00,
          first_seen: "2026-03-10",
          last_success: "2026-03-12",
          last_failure: "2026-03-15",
          failure_types: { post_payment: 7, pre_payment: 0 },
          warnings: ["high_failure_rate", "volatile_pricing"],
          score: 23,
        },
      },
    };
    writeFileSync(dbPath, JSON.stringify(db));
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("looks up known endpoint", () => {
    const entry = lookupEndpoint(TEST_URLS.good, dbPath);
    assert.ok(entry);
    assert.equal(entry.url_hint, "stockdata.xyz");
    assert.equal(entry.score, 94);
  });

  it("returns null for unknown endpoint", () => {
    const entry = lookupEndpoint("https://unknown.example.com/api", dbPath);
    assert.equal(entry, null);
  });

  it("checkEndpoint returns full assessment for known endpoint", () => {
    const result = checkEndpoint(TEST_URLS.good, dbPath);
    assert.equal(result.known, true);
    assert.equal(result.score, 94);
    assert.equal(result.recommendation, "allow");
    assert.equal(result.success_rate, 0.97);
    assert.equal(result.median_price, "0.03");
  });

  it("checkEndpoint returns allow for unknown endpoint", () => {
    const result = checkEndpoint(TEST_URLS.new_ep, dbPath);
    assert.equal(result.known, false);
    assert.equal(result.recommendation, "allow");
  });

  it("checkEndpoint returns block for bad endpoint", () => {
    const result = checkEndpoint(TEST_URLS.bad, dbPath);
    assert.equal(result.known, true);
    assert.equal(result.recommendation, "block");
    assert.equal(result.score, 23);
  });

  it("detects price anomaly", () => {
    const result = checkPriceAnomaly(TEST_URLS.good, "0.50", dbPath);
    assert.equal(result.anomalous, true);
    assert.ok(result.reason.includes("more than"));
  });

  it("accepts normal price", () => {
    const result = checkPriceAnomaly(TEST_URLS.good, "0.03", dbPath);
    assert.equal(result.anomalous, false);
  });

  it("search finds by hostname", () => {
    const results = searchEndpoints("stockdata", dbPath);
    assert.equal(results.length, 1);
    assert.equal(results[0].url_hint, "stockdata.xyz");
  });

  it("search returns empty for unknown query", () => {
    const results = searchEndpoints("nonexistent", dbPath);
    assert.equal(results.length, 0);
  });
});

describe("trust-db: price bucketing", () => {
  it("buckets prices correctly", () => {
    assert.equal(bucketPrice("0.005"), "0.001-0.01");
    assert.equal(bucketPrice("0.05"), "0.01-0.10");
    assert.equal(bucketPrice("0.50"), "0.10-1.00");
    assert.equal(bucketPrice("5.00"), "1.00-10.00");
    assert.equal(bucketPrice("50.00"), "10.00-100.00");
    assert.equal(bucketPrice("500.00"), "100.00+");
  });

  it("handles zero and negative", () => {
    assert.equal(bucketPrice("0"), "0");
    assert.equal(bucketPrice("-1"), "0");
  });
});

describe("trust-db: config", () => {
  let tmpDir;
  let configPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-config-test-"));
    configPath = join(tmpDir, "config.json");
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("generates install_id on first load", () => {
    const config = loadConfig(configPath);
    assert.ok(config.install_id);
    assert.equal(config.install_id.length, 32); // 16 bytes hex
    assert.equal(config.participate_in_network, false);
  });

  it("preserves install_id across loads", () => {
    const c1 = loadConfig(configPath);
    const c2 = loadConfig(configPath);
    assert.equal(c1.install_id, c2.install_id);
  });

  it("saves and loads config", () => {
    const config = loadConfig(configPath);
    config.participate_in_network = true;
    saveConfig(config, configPath);
    const loaded = loadConfig(configPath);
    assert.equal(loaded.participate_in_network, true);
  });

  it("reporter hash is deterministic", () => {
    const h1 = getReporterHash(configPath);
    const h2 = getReporterHash(configPath);
    assert.equal(h1, h2);
    assert.ok(h1.startsWith("sha256:"));
  });
});

describe("trust-db: DB status", () => {
  it("reports non-existent DB", () => {
    const status = getDbStatus("/tmp/nonexistent-trust-db-path.json");
    assert.equal(status.exists, false);
    assert.equal(status.endpoint_count, 0);
  });

  it("reports existing DB stats", () => {
    const tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-status-test-"));
    const dbPath = join(tmpDir, "trust.json");
    writeFileSync(dbPath, JSON.stringify(SAMPLE_DB));

    const status = getDbStatus(dbPath);
    assert.equal(status.exists, true);
    assert.equal(status.version, "2026-03-15");
    assert.ok(status.file_size_bytes > 0);
    assert.ok(status.age_hours != null);

    rmSync(tmpDir, { recursive: true, force: true });
  });
});

describe("reporter: signal construction", () => {
  let tmpDir;
  let configPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-reporter-test-"));
    configPath = join(tmpDir, "config.json");
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("builds anonymous signal from report", () => {
    const signal = buildSignal({
      endpoint_url: "https://api.example.com/data",
      outcome: "post_payment_failure",
      amount_usd: "0.05",
    }, configPath);

    assert.ok(signal.endpoint_hash.startsWith("sha256:"));
    assert.equal(signal.outcome, "post_payment_failure");
    assert.equal(signal.amount_range, "0.01-0.10");
    assert.equal(signal.timestamp_bucket, new Date().toISOString().slice(0, 10));
    assert.ok(signal.reporter_hash.startsWith("sha256:"));
  });

  it("hashes endpoint URL in signal", () => {
    const s1 = buildSignal({ endpoint_url: "https://api.example.com/data", outcome: "success", amount_usd: "0" }, configPath);
    const s2 = buildSignal({ endpoint_url: "https://API.Example.COM/data", outcome: "success", amount_usd: "0" }, configPath);
    assert.equal(s1.endpoint_hash, s2.endpoint_hash); // Same URL, different case
  });
});

describe("reporter: queue and pending", () => {
  let tmpDir;
  let pendingPath;
  let configPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-queue-test-"));
    pendingPath = join(tmpDir, "pending.jsonl");
    configPath = join(tmpDir, "config.json");
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("queues a report", () => {
    const result = queueReport({
      endpoint_url: "https://api.example.com/data",
      outcome: "post_payment_failure",
      amount_usd: "0.05",
    }, pendingPath, configPath);

    assert.equal(result.queued, true);
    assert.ok(result.signal.endpoint_hash);
  });

  it("deduplicates same report on same day", () => {
    const result = queueReport({
      endpoint_url: "https://api.example.com/data",
      outcome: "post_payment_failure",
      amount_usd: "0.05",
    }, pendingPath, configPath);

    assert.equal(result.queued, false);
    assert.equal(result.reason, "duplicate");
  });

  it("allows different outcome for same endpoint", () => {
    const result = queueReport({
      endpoint_url: "https://api.example.com/data",
      outcome: "success",
      amount_usd: "0.03",
    }, pendingPath, configPath);

    assert.equal(result.queued, true);
  });

  it("allows same outcome for different endpoint", () => {
    const result = queueReport({
      endpoint_url: "https://other.example.com/api",
      outcome: "post_payment_failure",
      amount_usd: "1.00",
    }, pendingPath, configPath);

    assert.equal(result.queued, true);
  });

  it("reads pending reports", () => {
    const reports = readPendingReports(pendingPath);
    assert.equal(reports.length, 3);
    assert.equal(reports[0].status, "pending");
  });

  it("gets pending status counts", () => {
    const status = getPendingStatus(pendingPath);
    assert.equal(status.total, 3);
    assert.equal(status.pending, 3);
    assert.equal(status.sent, 0);
  });

  it("handles empty pending file", () => {
    const emptyPath = join(tmpDir, "empty.jsonl");
    const reports = readPendingReports(emptyPath);
    assert.deepEqual(reports, []);
  });
});

describe("reporter: pruning", () => {
  let tmpDir;
  let pendingPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-prune-test-"));
    pendingPath = join(tmpDir, "pending.jsonl");

    // Write some test reports
    const reports = [
      { endpoint_hash: "sha256:aaa", outcome: "success", status: "sent", sent_at: "2026-03-01T00:00:00Z" },
      { endpoint_hash: "sha256:bbb", outcome: "success", status: "sent", sent_at: new Date().toISOString() },
      { endpoint_hash: "sha256:ccc", outcome: "post_payment_failure", status: "pending" },
    ];
    writeFileSync(pendingPath, reports.map(r => JSON.stringify(r)).join("\n") + "\n");
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("prunes old sent reports", () => {
    const result = pruneSentReports(pendingPath);
    assert.equal(result.pruned, 1); // Only the old one
    assert.equal(result.remaining, 2);
  });

  it("keeps recent sent and pending reports", () => {
    const reports = readPendingReports(pendingPath);
    assert.equal(reports.length, 2);
    assert.ok(reports.some(r => r.status === "sent"));
    assert.ok(reports.some(r => r.status === "pending"));
  });
});

describe("server API", () => {
  let serverProcess;
  let tmpDir;
  const port = 18922; // Different port for tests

  before(async () => {
    tmpDir = mkdtempSync(join(tmpdir(), "fraud-filter-server-test-"));

    // Create a test trust DB with real hashes
    const goodHash = hashEndpoint(TEST_URLS.good);
    const badHash = hashEndpoint(TEST_URLS.bad);
    const testDb = {
      version: "2026-03-15",
      generated_at: "2026-03-15T04:00:00Z",
      endpoint_count: 2,
      endpoints: {
        [goodHash]: {
          url_hint: "stockdata.xyz",
          report_count: 347, success_rate: 0.97,
          median_price_usd: 0.03, price_p10_usd: 0.02, price_p90_usd: 0.05,
          first_seen: "2026-01-20", last_success: "2026-03-15", last_failure: "2026-03-14",
          failure_types: { post_payment: 8, pre_payment: 3 },
          warnings: [], score: 94,
        },
        [badHash]: {
          url_hint: "shady-data.xyz",
          report_count: 12, success_rate: 0.42,
          median_price_usd: 0.50, price_p10_usd: 0.05, price_p90_usd: 2.00,
          first_seen: "2026-03-10", last_success: "2026-03-12", last_failure: "2026-03-15",
          failure_types: { post_payment: 7, pre_payment: 0 },
          warnings: ["high_failure_rate", "volatile_pricing"], score: 23,
        },
      },
    };
    writeFileSync(join(tmpDir, "trust.json"), JSON.stringify(testDb));

    const { spawn } = await import("node:child_process");
    serverProcess = spawn("node", ["server/server.js"], {
      cwd: join(import.meta.url.replace("file://", ""), "../../"),
      env: {
        ...process.env,
        FRAUD_FILTER_PORT: String(port),
        FRAUD_FILTER_DB: join(tmpDir, "trust.json"),
        FRAUD_FILTER_PENDING: join(tmpDir, "pending.jsonl"),
        FRAUD_FILTER_CONFIG: join(tmpDir, "config.json"),
      },
    });
    await new Promise((r) => setTimeout(r, 500));
  });

  after(() => {
    if (serverProcess) serverProcess.kill();
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("GET /api/check returns trust assessment for known endpoint", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/check?url=${encodeURIComponent(TEST_URLS.good)}`);
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.equal(data.known, true);
    assert.equal(data.score, 94);
    assert.equal(data.recommendation, "allow");
  });

  it("GET /api/check returns allow for unknown endpoint", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/check?url=${encodeURIComponent(TEST_URLS.new_ep)}`);
    const data = await res.json();
    assert.equal(data.known, false);
    assert.equal(data.recommendation, "allow");
  });

  it("GET /api/check requires url parameter", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/check`);
    assert.equal(res.status, 400);
  });

  it("GET /api/search finds endpoints by hostname", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/search?q=stockdata`);
    const data = await res.json();
    assert.equal(data.count, 1);
    assert.equal(data.results[0].url_hint, "stockdata.xyz");
  });

  it("GET /api/endpoints returns paginated list", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/endpoints?sort=score&order=desc`);
    const data = await res.json();
    assert.equal(data.total, 2);
    assert.ok(data.endpoints[0].score >= data.endpoints[1].score);
  });

  it("GET /api/status returns DB and report status", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/status`);
    const data = await res.json();
    assert.ok(data.db);
    assert.ok(data.reports);
    assert.ok(data.participation);
    assert.equal(data.db.exists, true);
    assert.equal(data.db.endpoint_count, 2);
  });

  it("POST /api/reports queues a report", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/reports`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint_url: TEST_URLS.bad,
        outcome: "post_payment_failure",
        amount_usd: "0.50",
      }),
    });
    assert.equal(res.status, 201);
    const data = await res.json();
    assert.equal(data.queued, true);
    assert.ok(data.signal.endpoint_hash);
  });

  it("POST /api/reports rejects duplicate", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/reports`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint_url: TEST_URLS.bad,
        outcome: "post_payment_failure",
        amount_usd: "0.50",
      }),
    });
    assert.equal(res.status, 409);
  });

  it("POST /api/reports validates outcome", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/reports`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint_url: TEST_URLS.bad,
        outcome: "invalid_outcome",
      }),
    });
    assert.equal(res.status, 400);
  });

  it("GET /api/reports lists pending reports", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/reports`);
    const data = await res.json();
    assert.ok(data.count >= 1);
  });

  it("GET /api/config returns config without install_id", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/config`);
    const data = await res.json();
    assert.ok(!data.install_id);
    assert.ok("participate_in_network" in data);
  });

  it("POST /api/config updates settings", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ participate_in_network: true }),
    });
    const data = await res.json();
    assert.equal(data.participate_in_network, true);
  });

  it("GET /api/check-price detects anomaly", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/check-price?url=${encodeURIComponent(TEST_URLS.good)}&price=0.50`);
    const data = await res.json();
    assert.equal(data.anomalous, true);
  });
});
