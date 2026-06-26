#!/usr/bin/env node

import { createServer } from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import {
  loadTrustDb,
  checkEndpoint,
  checkPriceAnomaly,
  searchEndpoints,
  getDbStatus,
  loadConfig,
  saveConfig,
  computeScore,
  deriveWarnings,
} from "./trust-db.js";
import {
  queueReport,
  readPendingReports,
  getPendingStatus,
  submitPendingReports,
  pruneSentReports,
} from "./reporter.js";
import { syncHotlist } from "./hotlist-sync.js";

const PORT = parseInt(process.env.FRAUD_FILTER_PORT || "18921", 10);
const HOST = "127.0.0.1";

// Proxy detection — track if we've seen a request with forwarding headers,
// which would indicate the dashboard is being proxied to a public network.
let proxyDetected = false;

function checkForProxy(req) {
  if (proxyDetected) return;
  if (req.headers["x-forwarded-for"] || req.headers["x-real-ip"]) {
    proxyDetected = true;
    console.warn(
      "[fraud-filter] WARNING: Proxy headers detected on incoming request. " +
      "The dashboard may be exposed beyond localhost. " +
      "Ensure nginx or any reverse proxy is NOT forwarding external traffic to this port."
    );
  }
}

const DASHBOARD_PATH = resolve(
  new URL("./index.html", import.meta.url).pathname
);

function parseQuery(url) {
  const u = new URL(url, "http://localhost");
  const params = {};
  for (const [k, v] of u.searchParams) params[k] = v;
  return { pathname: u.pathname, params };
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
    req.on("error", reject);
  });
}

function json(res, data, status = 200) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body),
    // No CORS headers — this server binds to 127.0.0.1 only and has no
    // legitimate cross-origin callers. A wildcard would let any webpage read
    // trust data from a running dashboard via cross-origin fetch.
  });
  res.end(body);
}

function html(res, content, status = 200) {
  res.writeHead(status, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": Buffer.byteLength(content),
  });
  res.end(content);
}

function notFound(res) {
  json(res, { error: "not found" }, 404);
}

// --- Server ---

const server = createServer(async (req, res) => {
  checkForProxy(req);



  const { pathname, params } = parseQuery(req.url);

  try {
    // --- GET routes ---
    if (req.method === "GET") {
      // Dashboard
      if (pathname === "/" || pathname === "/index.html") {
        const dashboardHtml = readFileSync(DASHBOARD_PATH, "utf-8");
        html(res, dashboardHtml);
        return;
      }

      // Check a single endpoint
      if (pathname === "/api/check") {
        const url = params.url;
        if (!url) {
          json(res, { error: "url parameter required" }, 400);
          return;
        }
        const assessment = checkEndpoint(url);
        json(res, assessment);
        return;
      }

      // Check for price anomaly
      if (pathname === "/api/check-price") {
        const url = params.url;
        const price = params.price;
        if (!url || !price) {
          json(res, { error: "url and price parameters required" }, 400);
          return;
        }
        const result = checkPriceAnomaly(url, price);
        json(res, result);
        return;
      }

      // Search endpoints
      if (pathname === "/api/search") {
        const q = params.q || params.query || "";
        if (!q) {
          json(res, { error: "q parameter required" }, 400);
          return;
        }
        const results = searchEndpoints(q);
        json(res, { results, count: results.length });
        return;
      }

      // List all endpoints in trust DB
      if (pathname === "/api/endpoints") {
        const db = loadTrustDb();
        const entries = Object.entries(db.endpoints || {}).map(([hash, entry]) => ({
          hash,
          ...entry,
        }));

        // Sort by specified field
        const sortBy = params.sort || "score";
        const order = params.order === "asc" ? 1 : -1;
        entries.sort((a, b) => {
          const av = a[sortBy] ?? 0;
          const bv = b[sortBy] ?? 0;
          return (av - bv) * order;
        });

        // Pagination
        const limit = Math.min(parseInt(params.limit || "50", 10), 500);
        const offset = parseInt(params.offset || "0", 10);
        const page = entries.slice(offset, offset + limit);

        json(res, { endpoints: page, total: entries.length, offset, limit });
        return;
      }

      // Trust DB status
      if (pathname === "/api/status") {
        const status = getDbStatus();
        const pending = getPendingStatus();
        const config = loadConfig();
        json(res, {
          db: status,
          reports: pending,
          participation: {
            network_enabled: config.participate_in_network,
            auto_positive: config.auto_positive_signals,
          },
          security: {
            proxy_detected: proxyDetected,
          },
        });
        return;
      }

      // Pending reports
      if (pathname === "/api/reports") {
        const reports = readPendingReports();
        json(res, { reports, count: reports.length });
        return;
      }

      // Configuration
      if (pathname === "/api/config") {
        const config = loadConfig();
        // Don't expose install_id
        const { install_id, ...safeConfig } = config;
        json(res, safeConfig);
        return;
      }
    }

    // --- POST routes ---
    if (req.method === "POST") {
      const body = await readBody(req);
      let data;
      try {
        data = JSON.parse(body);
      } catch {
        json(res, { error: "invalid JSON" }, 400);
        return;
      }

      // Submit a report
      if (pathname === "/api/reports") {
        if (!data.endpoint_url) {
          json(res, { error: "endpoint_url required" }, 400);
          return;
        }
        const validOutcomes = ["success", "post_payment_failure", "pre_payment_failure"];
        if (!validOutcomes.includes(data.outcome)) {
          json(res, { error: `outcome must be one of: ${validOutcomes.join(", ")}` }, 400);
          return;
        }

        const result = queueReport({
          endpoint_url: data.endpoint_url,
          outcome: data.outcome,
          amount_usd: data.amount_usd || "0",
          skill_name: data.skill_name || null,
          reason: data.reason || null,
        });

        if (!result.queued) {
          json(res, { error: "duplicate report for this endpoint today", signal: result.signal }, 409);
          return;
        }

        json(res, { queued: true, signal: result.signal }, 201);
        return;
      }

      // Flush pending reports to server
      if (pathname === "/api/reports/flush") {
        const result = await submitPendingReports();
        json(res, result);
        return;
      }

      // Prune old sent reports
      if (pathname === "/api/reports/prune") {
        const result = pruneSentReports();
        json(res, result);
        return;
      }

      // Update configuration
      if (pathname === "/api/config") {
        const config = loadConfig();
        const allowedKeys = [
          "trust_db_url",
          "report_endpoint",
          "sync_interval_hours",
          "participate_in_network",
          "on_block",
          "on_caution",
        ];
        for (const key of allowedKeys) {
          if (key in data) {
            config[key] = data[key];
          }
        }
        saveConfig(config);
        const { install_id, ...safeConfig } = config;
        json(res, safeConfig);
        return;
      }
    }

    notFound(res);
  } catch (err) {
    console.error("Request error:", err);
    json(res, { error: "internal server error" }, 500);
  }
});

server.listen(PORT, HOST, () => {
  console.log(`fraud-filter dashboard running at http://${HOST}:${PORT}`);
});

// Sync hotlist on startup, then refresh every hour
syncHotlist();
setInterval(syncHotlist, 60 * 60 * 1000);
