import { createHash, randomBytes } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";

const DEFAULT_HOTLIST_PATH = resolve(
  process.env.FRAUD_FILTER_HOTLIST ||
    new URL("../data/hotlist.json", import.meta.url).pathname
);

function loadHotlistCache(hotlistPath = DEFAULT_HOTLIST_PATH) {
  if (!existsSync(hotlistPath)) return new Set();
  try {
    const data = JSON.parse(readFileSync(hotlistPath, "utf-8"));
    return new Set(data.blocked || []);
  } catch {
    return new Set();
  }
}

const DEFAULT_DB_PATH = resolve(
  process.env.FRAUD_FILTER_DB ||
    new URL("../data/trust.json", import.meta.url).pathname
);

const DEFAULT_CONFIG_PATH = resolve(
  process.env.FRAUD_FILTER_CONFIG ||
    new URL("../data/config.json", import.meta.url).pathname
);

// --- Hashing ---

export function sha256(data) {
  return createHash("sha256").update(data).digest("hex");
}

/**
 * Normalize an endpoint URL for consistent hashing.
 * - Lowercase scheme and hostname
 * - Remove default ports
 * - Remove trailing slashes
 * - Remove query parameters and fragments
 */
export function normalizeUrl(url) {
  try {
    const u = new URL(url);
    u.search = "";
    u.hash = "";
    let href = u.href;
    // Remove trailing slash (unless it's just the origin root)
    if (href.endsWith("/") && u.pathname !== "/") {
      href = href.slice(0, -1);
    }
    return href;
  } catch {
    // If URL parsing fails, lowercase and return as-is
    return url.toLowerCase().replace(/[?#].*$/, "").replace(/\/+$/, "");
  }
}

/**
 * Compute the SHA-256 hash of a normalized endpoint URL.
 */
export function hashEndpoint(url) {
  return sha256(normalizeUrl(url));
}

/**
 * Extract just the hostname from a URL (for url_hint field).
 */
export function extractHint(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

// --- Trust Database ---

/**
 * Load the trust database from disk.
 * Returns { version, generated_at, endpoint_count, endpoints } or a default empty DB.
 */
export function loadTrustDb(dbPath = DEFAULT_DB_PATH) {
  if (!existsSync(dbPath)) {
    return { version: null, generated_at: null, endpoint_count: 0, endpoints: {} };
  }
  try {
    return JSON.parse(readFileSync(dbPath, "utf-8"));
  } catch {
    return { version: null, generated_at: null, endpoint_count: 0, endpoints: {} };
  }
}

/**
 * Look up an endpoint by URL in the trust database.
 * Returns the endpoint record or null if not found.
 */
export function lookupEndpoint(url, dbPath = DEFAULT_DB_PATH) {
  const db = loadTrustDb(dbPath);
  const hash = hashEndpoint(url);
  const entry = db.endpoints[hash] || null;
  return entry;
}

/**
 * Check an endpoint and return a full trust assessment.
 * This is the primary interface for spend-ledger integration.
 */
export function checkEndpoint(url, dbPath = DEFAULT_DB_PATH) {
  const hash = hashEndpoint(url);

  // Hotlist check first — recent surge of failure reports overrides stored score
  const hotlist = loadHotlistCache();
  if (hotlist.has(hash)) {
    return {
      endpoint: url,
      endpoint_hash: hash,
      known: true,
      warnings: ["hotlisted"],
      recommendation: "block",
      hotlisted: true,
    };
  }

  const entry = lookupEndpoint(url, dbPath);

  if (!entry) {
    // Unknown endpoints get an all-clear — absence of data is not a signal.
    // Blocking unknown endpoints would make the skill unusable as the agent
    // payment ecosystem grows.
    return {
      endpoint: url,
      endpoint_hash: hash,
      known: false,
      report_count: 0,
      warnings: [],
      recommendation: "allow",
    };
  }

  return {
    endpoint: url,
    endpoint_hash: hash,
    known: true,
    report_count: entry.report_count,
    success_rate: entry.success_rate,
    median_price: String(entry.median_price_usd),
    price_range: {
      p10: String(entry.price_p10_usd),
      p90: String(entry.price_p90_usd),
    },
    last_failure: entry.last_failure || null,
    warnings: entry.warnings || [],
    score: entry.score,
    recommendation: scoreToRecommendation(entry.score),
  };
}

/**
 * Map a trust score to a recommendation string.
 */
export function scoreToRecommendation(score) {
  if (score >= 70) return "allow";
  if (score >= 40) return "caution";
  return "block";
}

/**
 * Check if the price for an endpoint is anomalous.
 * Returns { anomalous, reason } or { anomalous: false }.
 */
export function checkPriceAnomaly(url, priceUsd, dbPath = DEFAULT_DB_PATH) {
  const entry = lookupEndpoint(url, dbPath);
  if (!entry || !entry.median_price_usd) {
    return { anomalous: false, reason: null };
  }

  const price = parseFloat(priceUsd);
  const median = entry.median_price_usd;
  const p90 = entry.price_p90_usd;

  if (price > p90 * 2) {
    // High price AND a low trust score suggests a scam; high price on a
    // trusted endpoint is more likely surge pricing or a large request.
    const anomalyType = (entry.score != null && entry.score < 60) ? "suspicious" : "market_outlier";
    return {
      anomalous: true,
      anomaly_type: anomalyType,
      reason: anomalyType === "suspicious"
        ? `Price $${price.toFixed(4)} is more than 2x the p90 ($${p90.toFixed(4)}) on a low-trust endpoint`
        : `Price $${price.toFixed(4)} is more than 2x the p90 ($${p90.toFixed(4)}) — likely surge pricing or large request`,
      price,
      median,
      p90,
    };
  }

  if (price > median * 3) {
    const anomalyType = (entry.score != null && entry.score < 60) ? "suspicious" : "market_outlier";
    return {
      anomalous: true,
      anomaly_type: anomalyType,
      reason: anomalyType === "suspicious"
        ? `Price $${price.toFixed(4)} is more than 3x the median ($${median.toFixed(4)}) on a low-trust endpoint`
        : `Price $${price.toFixed(4)} is more than 3x the median ($${median.toFixed(4)}) — likely surge pricing or large request`,
      price,
      median,
      p90,
    };
  }

  return { anomalous: false, reason: null };
}

// --- Score Calculation ---

/**
 * Compute a trust score (0-100) from endpoint data.
 * This is the reference implementation of the score formula documented in signal-format.md.
 */
export function computeScore(entry, now = new Date()) {
  if (!entry || entry.report_count === 0) return null;

  // Base
  let score = 50;

  // Success factor: (success_rate - 0.5) * 80 → range -40 to +40
  const successRate = entry.success_rate ?? 1.0;
  score += (successRate - 0.5) * 80;

  // Volume factor: min(10, log10(report_count) * 5)
  const reportCount = entry.report_count || 1;
  score += Math.min(10, Math.log10(reportCount) * 5);

  // Recency penalty: up to -20 for failures within 7 days
  if (entry.last_failure) {
    const failDate = new Date(entry.last_failure);
    const daysSinceFailure = (now - failDate) / (1000 * 60 * 60 * 24);
    if (daysSinceFailure < 7) {
      score += -20 + daysSinceFailure * (20 / 7);
    }
  }

  // Stability factor: based on price volatility
  const p10 = entry.price_p10_usd || 0;
  const p90 = entry.price_p90_usd || 0;
  if (p10 > 0) {
    const ratio = p90 / p10;
    if (ratio > 5) score -= 10;
    else if (ratio > 3) score -= 5;
  }

  // Age factor: new endpoints penalized for up to 30 days
  if (entry.first_seen) {
    const firstSeen = new Date(entry.first_seen);
    const daysActive = (now - firstSeen) / (1000 * 60 * 60 * 24);
    if (daysActive < 30) {
      score += -15 + daysActive * 0.5;
    }
  }

  return Math.round(Math.max(0, Math.min(100, score)));
}

/**
 * Derive warning flags from endpoint data.
 */
export function deriveWarnings(entry, now = new Date()) {
  const warnings = [];

  if ((entry.success_rate ?? 1) < 0.7) {
    warnings.push("high_failure_rate");
  }

  const p10 = entry.price_p10_usd || 0;
  const p90 = entry.price_p90_usd || 0;
  if (p10 > 0 && p90 / p10 > 5) {
    warnings.push("volatile_pricing");
  }

  if (entry.last_failure) {
    const daysSince = (now - new Date(entry.last_failure)) / (1000 * 60 * 60 * 24);
    if (daysSince < 3) {
      warnings.push("recent_complaints");
    }
  }

  if (entry.first_seen) {
    const daysActive = (now - new Date(entry.first_seen)) / (1000 * 60 * 60 * 24);
    if (daysActive < 14) {
      warnings.push("new_endpoint");
    }
  }

  if ((entry.report_count || 0) < 5) {
    warnings.push("limited_data");
  }

  return warnings;
}

// --- Trust DB Status ---

/**
 * Get status information about the local trust database.
 */
export function getDbStatus(dbPath = DEFAULT_DB_PATH) {
  if (!existsSync(dbPath)) {
    return {
      exists: false,
      version: null,
      generated_at: null,
      endpoint_count: 0,
      file_size_bytes: 0,
      last_sync: null,
      age_hours: null,
    };
  }

  const db = loadTrustDb(dbPath);
  const stat = statSync(dbPath);
  const ageMs = Date.now() - stat.mtimeMs;

  return {
    exists: true,
    version: db.version || null,
    generated_at: db.generated_at || null,
    endpoint_count: db.endpoint_count || Object.keys(db.endpoints || {}).length,
    file_size_bytes: stat.size,
    last_sync: stat.mtime.toISOString(),
    age_hours: Math.round((ageMs / (1000 * 60 * 60)) * 10) / 10,
  };
}

// --- Configuration ---

const DEFAULT_CONFIG = {
  trust_db_url: "https://api.fraud-filter.com/trust.json",
  report_endpoint: "https://api.fraud-filter.com/reports",
  sync_interval_hours: 24,
  participate_in_network: false,  // true to enable network report submission
  sync_hotlist: true,             // false to disable hourly hotlist download (e.g. air-gapped)
  on_block: "block",    // "block" | "warn" — action when recommendation is block
  on_caution: "warn",   // "warn" | "block" | "allow" — action when recommendation is caution
  install_id: null,
};

/**
 * Load fraud-filter configuration, merging with defaults.
 */
export function loadConfig(configPath = DEFAULT_CONFIG_PATH) {
  let stored = {};
  if (existsSync(configPath)) {
    try {
      stored = JSON.parse(readFileSync(configPath, "utf-8"));
    } catch {
      stored = {};
    }
  }
  const config = { ...DEFAULT_CONFIG, ...stored };

  // Generate install_id on first run
  if (!config.install_id) {
    config.install_id = randomBytes(16).toString("hex");
    saveConfig(config, configPath);
  }

  return config;
}

/**
 * Save configuration to disk.
 */
export function saveConfig(config, configPath = DEFAULT_CONFIG_PATH) {
  const dir = dirname(configPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(configPath, JSON.stringify(config, null, 2) + "\n", { mode: 0o600 });
}

/**
 * Get the reporter hash (one-way hash of the install ID).
 */
export function getReporterHash(configPath = DEFAULT_CONFIG_PATH) {
  const config = loadConfig(configPath);
  return "sha256:" + sha256(config.install_id);
}

// --- Price Bucketing ---

/**
 * Bucket a price into an anonymous range for signal reporting.
 */
export function bucketPrice(amountUsd) {
  const v = parseFloat(amountUsd);
  if (isNaN(v) || v <= 0) return "0";
  if (v <= 0.01) return "0.001-0.01";
  if (v <= 0.10) return "0.01-0.10";
  if (v <= 1.00) return "0.10-1.00";
  if (v <= 10.00) return "1.00-10.00";
  if (v <= 100.00) return "10.00-100.00";
  return "100.00+";
}

// --- Search ---

/**
 * Search endpoints in the trust database by hostname hint or hash prefix.
 */
export function searchEndpoints(query, dbPath = DEFAULT_DB_PATH) {
  const db = loadTrustDb(dbPath);
  const q = query.toLowerCase();
  const results = [];

  for (const [hash, entry] of Object.entries(db.endpoints || {})) {
    if (
      hash.toLowerCase().startsWith(q) ||
      (entry.url_hint || "").toLowerCase().includes(q)
    ) {
      results.push({ hash, ...entry });
    }
  }

  return results.sort((a, b) => (b.report_count || 0) - (a.report_count || 0));
}
