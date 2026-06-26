/**
 * Ops Dashboard Routes — secured with OPS_API_KEY + IP allowlist.
 *
 * GET /ops/metrics    — aggregated metrics (no PII, no wallet/tx data)
 * GET /ops/rollout    — current rollout state + health determination
 *
 * Security: double contour —
 *   1. Bearer token matching OPS_API_KEY
 *   2. IP allowlist from OPS_IP_ALLOWLIST (comma-separated)
 *   3. No raw PII: wallet addresses, tx hashes are never returned
 */
import { Router, type Request, type Response, type NextFunction } from "express";
import { env } from "../config/env";
import { query } from "../db/db";

export const opsRouter = Router();

// ── Security middleware ────────────────────────────────────

function opsAuth(req: Request, res: Response, next: NextFunction): void {
    // Layer 1: API key
    if (!env.OPS_API_KEY) {
        res.status(503).json({ error: "Ops dashboard not configured" });
        return;
    }

    const authHeader = req.header("Authorization");
    const token = authHeader?.startsWith("Bearer ")
        ? authHeader.slice(7)
        : req.query.key as string | undefined;

    if (token !== env.OPS_API_KEY) {
        res.status(401).json({ error: "Unauthorized" });
        return;
    }

    // Layer 2: IP allowlist
    if (env.OPS_IP_ALLOWLIST) {
        const allowed = env.OPS_IP_ALLOWLIST.split(",").map(s => s.trim());
        const clientIp =
            req.header("x-forwarded-for")?.split(",")[0]?.trim() ??
            req.socket.remoteAddress ??
            "";

        if (!allowed.includes(clientIp) && !allowed.includes("*")) {
            res.status(403).json({ error: "Forbidden" });
            return;
        }
    }

    next();
}

opsRouter.use(opsAuth);

// ── Alert thresholds ───────────────────────────────────────

const THRESHOLDS = {
    verify_error_rate_pct: 5,              // > 5% in window → rollback
    settle_failed_rate_pct: 2,             // > 2% in window → rollback
    webhook_sig_failure_rate_pct: 0.5,     // trusted-source only (4payments), rate-based
    replay_duplicates_max: 0,              // hard-stop: any replay = rollback
    p95_create_ms: 15_000,                 // p95 latency SLO
    p95_fund_ms: 15_000,
    window_minutes: 15                     // evaluation window
} as const;

// ── GET /ops/metrics ───────────────────────────────────────

opsRouter.get("/metrics", async (_req, res) => {
    try {
        const windowMin = THRESHOLDS.window_minutes;

        // Aggregated counts in window — NO raw rows, NO PII
        const [counts] = await query<{
            event_type: string;
            count: string;
        }>(
            `SELECT event_type, COUNT(*)::text as count
       FROM api_metrics
       WHERE created_at > now() - interval '${windowMin} minutes'
       GROUP BY event_type
       ORDER BY event_type`
        ).then(rows => [rows]);

        // Trusted-source webhook sig failures (only 4payments, ignore external noise)
        const [trustedWebhookCounts] = await query<{
            event_type: string;
            count: string;
        }>(
            `SELECT event_type, COUNT(*)::text as count
       FROM api_metrics
       WHERE source = '4payments'
         AND event_type IN ('webhook_sig_failure', 'webhook_accepted', 'webhook_duplicate')
         AND created_at > now() - interval '${windowMin} minutes'
       GROUP BY event_type`
        ).then(rows => [rows]);

        // Top-5 error reasons (for checkpoint report)
        const top5Reasons = await query<{
            reason: string;
            count: string;
        }>(
            `SELECT metadata->>'reason' as reason, COUNT(*)::text as count
       FROM api_metrics
       WHERE event_type IN ('verify_error', 'settle_failed')
         AND metadata->>'reason' IS NOT NULL
         AND created_at > now() - interval '${windowMin} minutes'
       GROUP BY metadata->>'reason'
       ORDER BY COUNT(*) DESC
       LIMIT 5`
        );

        // p95 latencies for create/fund
        const [latencies] = await query<{
            event_type: string;
            p50: string;
            p95: string;
            p99: string;
        }>(
            `SELECT event_type,
              percentile_cont(0.50) WITHIN GROUP (ORDER BY latency_ms)::integer::text as p50,
              percentile_cont(0.95) WITHIN GROUP (ORDER BY latency_ms)::integer::text as p95,
              percentile_cont(0.99) WITHIN GROUP (ORDER BY latency_ms)::integer::text as p99
       FROM api_metrics
       WHERE event_type IN ('request_create', 'request_fund')
         AND latency_ms IS NOT NULL
         AND created_at > now() - interval '${windowMin} minutes'
       GROUP BY event_type`
        ).then(rows => [rows]);

        // Compute rates
        const countMap = new Map(counts.map(c => [c.event_type, Number(c.count)]));

        const verifyTotal = (countMap.get("verify_ok") ?? 0) + (countMap.get("verify_error") ?? 0);
        const settleTotal = (countMap.get("settle_ok") ?? 0) + (countMap.get("settle_failed") ?? 0);
        // Trusted-source webhook counts (4payments only)
        const trustedMap = new Map(trustedWebhookCounts.map(c => [c.event_type, Number(c.count)]));
        const trustedWebhookTotal = (trustedMap.get("webhook_accepted") ?? 0) +
            (trustedMap.get("webhook_duplicate") ?? 0) +
            (trustedMap.get("webhook_sig_failure") ?? 0);

        const verifyErrorRate = verifyTotal > 0
            ? ((countMap.get("verify_error") ?? 0) / verifyTotal * 100)
            : 0;
        const settleFailedRate = settleTotal > 0
            ? ((countMap.get("settle_failed") ?? 0) / settleTotal * 100)
            : 0;
        // Rate from trusted source only — not all incoming noise
        const webhookSigFailureRate = trustedWebhookTotal > 0
            ? ((trustedMap.get("webhook_sig_failure") ?? 0) / trustedWebhookTotal * 100)
            : 0;
        const replayDuplicates = countMap.get("replay_blocked") ?? 0;

        // p95 lookup
        const latencyMap = new Map(latencies.map(l => [l.event_type, l]));
        const createP95 = Number(latencyMap.get("request_create")?.p95 ?? 0);
        const fundP95 = Number(latencyMap.get("request_fund")?.p95 ?? 0);

        // Alert evaluation
        const alerts: string[] = [];
        if (verifyErrorRate > THRESHOLDS.verify_error_rate_pct)
            alerts.push(`verify_error_rate ${verifyErrorRate.toFixed(1)}% > ${THRESHOLDS.verify_error_rate_pct}%`);
        if (settleFailedRate > THRESHOLDS.settle_failed_rate_pct)
            alerts.push(`settle_failed_rate ${settleFailedRate.toFixed(1)}% > ${THRESHOLDS.settle_failed_rate_pct}%`);
        if (webhookSigFailureRate > THRESHOLDS.webhook_sig_failure_rate_pct)
            alerts.push(`trusted_webhook_sig_failure_rate ${webhookSigFailureRate.toFixed(2)}% > ${THRESHOLDS.webhook_sig_failure_rate_pct}%`);
        if (replayDuplicates > THRESHOLDS.replay_duplicates_max)
            alerts.push(`replay_duplicates ${replayDuplicates} > ${THRESHOLDS.replay_duplicates_max} (HARD STOP)`);
        if (createP95 > THRESHOLDS.p95_create_ms)
            alerts.push(`p95_create ${createP95}ms > ${THRESHOLDS.p95_create_ms}ms`);
        if (fundP95 > THRESHOLDS.p95_fund_ms)
            alerts.push(`p95_fund ${fundP95}ms > ${THRESHOLDS.p95_fund_ms}ms`);

        const health = alerts.length === 0 ? "GREEN" : "RED";

        res.json({
            timestamp: new Date().toISOString(),
            windowMinutes: windowMin,
            health,
            alerts,
            rollback_recommended: alerts.length > 0,
            counts: Object.fromEntries(countMap),
            rates: {
                verify_error_rate_pct: Number(verifyErrorRate.toFixed(2)),
                settle_failed_rate_pct: Number(settleFailedRate.toFixed(2)),
                trusted_webhook_sig_failure_rate_pct: Number(webhookSigFailureRate.toFixed(2)),
                replay_duplicates: replayDuplicates,
            },
            top5_error_reasons: top5Reasons,
            latencies: {
                create: latencyMap.get("request_create") ?? null,
                fund: latencyMap.get("request_fund") ?? null,
            },
            thresholds: THRESHOLDS,
            rollout: {
                enabled: env.ROLLOUT_ENABLED === "true",
                pct: env.ROLLOUT_PCT,
            },
        });
    } catch (error) {
        res.status(500).json({
            error: "Failed to query metrics",
            detail: (error as Error).message
        });
    }
});

// ── GET /ops/rollout ───────────────────────────────────────

opsRouter.get("/rollout", async (_req, res) => {
    try {
        // Recent payment counts (last 24h) — no PII
        const [stats] = await query<{
            status: string;
            count: string;
        }>(
            `SELECT status, COUNT(*)::text as count
       FROM payments
       WHERE created_at > now() - interval '24 hours'
       GROUP BY status
       ORDER BY status`
        ).then(rows => [rows]);

        // Webhook stats
        const [webhookStats] = await query<{
            event_type: string;
            count: string;
        }>(
            `SELECT event_type, COUNT(*)::text as count
       FROM webhook_events
       WHERE processed_at > now() - interval '24 hours'
       GROUP BY event_type
       ORDER BY event_type`
        ).then(rows => [rows]);

        res.json({
            timestamp: new Date().toISOString(),
            rollout: {
                enabled: env.ROLLOUT_ENABLED === "true",
                pct: env.ROLLOUT_PCT,
                kill_switch_active: env.ROLLOUT_ENABLED !== "true",
            },
            last24h: {
                payments: Object.fromEntries(stats.map(s => [s.status, Number(s.count)])),
                webhooks: Object.fromEntries(webhookStats.map(s => [s.event_type, Number(s.count)])),
            },
        });
    } catch (error) {
        res.status(500).json({
            error: "Failed to query rollout stats",
            detail: (error as Error).message
        });
    }
});

// ── POST /ops/nonce-cleanup ───────────────────────────────

import { appLogger } from "../utils/logger";

opsRouter.post("/nonce-cleanup", async (req, res) => {
    const retentionHours = Number(req.query.retention_hours) || 24;
    const batchLimit = Number(req.query.batch_limit) || 10000;

    const start = Date.now();
    try {
        const rows = await query<{ deleted_count: string }>(
            `SELECT * FROM cleanup_expired_nonces($1, $2)`,
            [retentionHours, batchLimit]
        );

        const deletedCount = Number(rows[0]?.deleted_count ?? 0);
        const latencyMs = Date.now() - start;

        appLogger.info({
            event: "nonce_cleanup",
            deletedCount,
            retentionHours,
            batchLimit,
            latencyMs,
        }, `[OPS] Nonce cleanup: deleted ${deletedCount} expired nonces in ${latencyMs}ms`);

        res.json({
            timestamp: new Date().toISOString(),
            deleted_count: deletedCount,
            retention_hours: retentionHours,
            batch_limit: batchLimit,
            latency_ms: latencyMs,
        });
    } catch (error) {
        const latencyMs = Date.now() - start;
        appLogger.error({ err: error, latencyMs }, "[OPS] Nonce cleanup failed");
        res.status(500).json({
            error: "Nonce cleanup failed",
            detail: (error as Error).message,
        });
    }
});
