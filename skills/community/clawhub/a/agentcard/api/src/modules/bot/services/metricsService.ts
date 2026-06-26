/**
 * Bot/Portal Ops Metrics — aggregated metrics for monitoring dashboards.
 *
 * Exposes:
 *   - link success/deny rate
 *   - reveal-link usage
 *   - alert delivery latency p95
 *   - bot command usage counts
 *
 * @module modules/bot/services/metricsService
 */

import { query } from "../../../db/db";

// ── Types ──────────────────────────────────────────────────

export interface BotMetrics {
    links: {
        totalIssued: number;
        totalConsumed: number;
        totalExpired: number;
        totalRevoked: number;
        successRate: number;  // consumed / (consumed + expired + revoked)
        denyRate: number;     // denied decisions from audit log
    };
    reveals: {
        totalRequested: number;
        last24h: number;
    };
    alerts: {
        totalDelivered: number;
        totalFailed: number;
        totalSkipped: number;
        deliveryLatencyP95Ms: number | null;
    };
    audit: {
        totalActions: number;
        allowCount: number;
        denyCount: number;
        denyRate: number;
    };
    period: {
        from: string;
        to: string;
    };
}

// ── Service ────────────────────────────────────────────────

export class MetricsService {
    /**
     * Collect aggregated metrics for ops dashboard.
     * Defaults to last 24 hours.
     */
    static async collect(hoursBack = 24): Promise<BotMetrics> {
        const since = new Date(Date.now() - hoursBack * 3600_000).toISOString();
        const now = new Date().toISOString();

        // ── Link metrics ─────────────────────────────────────
        const linkData = await query<{
            status: string;
            count: string;
        }>(
            `SELECT status, COUNT(*) as count
       FROM telegram_link_tokens
       WHERE created_at >= $1
       GROUP BY status`,
            [since]
        ).catch(() => []);

        const linkCounts: Record<string, number> = {};
        for (const row of linkData) {
            linkCounts[row.status] = parseInt(row.count, 10);
        }

        const consumed = linkCounts["consumed"] ?? 0;
        const expired = linkCounts["expired"] ?? 0;
        const revoked = linkCounts["revoked"] ?? 0;
        const pending = linkCounts["pending"] ?? 0;
        const totalTokens = consumed + expired + revoked + pending;
        const denominator = consumed + expired + revoked;

        // ── Reveal metrics ───────────────────────────────────
        const revealData = await query<{ total: string; last24h: string }>(
            `SELECT
         COUNT(*) as total,
         COUNT(*) FILTER (WHERE created_at >= $1) as last24h
       FROM authz_audit_log
       WHERE action = 'card_reveal_requested'`,
            [since]
        ).catch(() => [{ total: "0", last24h: "0" }]);

        const reveals = revealData[0] ?? { total: "0", last24h: "0" };

        // ── Alert delivery metrics ───────────────────────────
        const alertData = await query<{
            delivery_status: string;
            count: string;
        }>(
            `SELECT delivery_status, COUNT(*) as count
       FROM bot_events
       WHERE created_at >= $1
       GROUP BY delivery_status`,
            [since]
        ).catch(() => []);

        const alertCounts: Record<string, number> = {};
        for (const row of alertData) {
            alertCounts[row.delivery_status] = parseInt(row.count, 10);
        }

        // Latency P95: time between event creation and message delivery
        const latencyData = await query<{ p95_ms: string }>(
            `SELECT
         PERCENTILE_CONT(0.95) WITHIN GROUP (
           ORDER BY EXTRACT(EPOCH FROM (bm.created_at - be.created_at)) * 1000
         ) as p95_ms
       FROM bot_events be
       JOIN bot_messages bm ON bm.correlation_id = be.idempotency_key
       WHERE be.created_at >= $1
         AND bm.status = 'sent'`,
            [since]
        ).catch(() => [{ p95_ms: null }]);

        const p95Ms = latencyData[0]?.p95_ms
            ? parseFloat(latencyData[0].p95_ms)
            : null;

        // ── Audit metrics ────────────────────────────────────
        const auditData = await query<{
            decision: string;
            count: string;
        }>(
            `SELECT decision, COUNT(*) as count
       FROM authz_audit_log
       WHERE created_at >= $1
       GROUP BY decision`,
            [since]
        ).catch(() => []);

        const auditCounts: Record<string, number> = {};
        for (const row of auditData) {
            auditCounts[row.decision] = parseInt(row.count, 10);
        }

        const allowCount = auditCounts["allow"] ?? 0;
        const denyCount = auditCounts["deny"] ?? 0;
        const totalAudit = allowCount + denyCount;

        return {
            links: {
                totalIssued: totalTokens,
                totalConsumed: consumed,
                totalExpired: expired,
                totalRevoked: revoked,
                successRate: denominator > 0 ? consumed / denominator : 0,
                denyRate: denominator > 0 ? (expired + revoked) / denominator : 0,
            },
            reveals: {
                totalRequested: parseInt(reveals.total, 10),
                last24h: parseInt(reveals.last24h, 10),
            },
            alerts: {
                totalDelivered: alertCounts["delivered"] ?? 0,
                totalFailed: alertCounts["failed"] ?? 0,
                totalSkipped: alertCounts["skipped"] ?? 0,
                deliveryLatencyP95Ms: p95Ms,
            },
            audit: {
                totalActions: totalAudit,
                allowCount,
                denyCount,
                denyRate: totalAudit > 0 ? denyCount / totalAudit : 0,
            },
            period: {
                from: since,
                to: now,
            },
        };
    }
}
