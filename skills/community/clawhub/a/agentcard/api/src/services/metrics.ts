import { appLogger } from "../utils/logger";
/**
 * Metrics Service — non-blocking, fail-open.
 *
 * Writes to `api_metrics` asynchronously. If Postgres insert fails,
 * it logs to stderr and does NOT propagate the error to the caller.
 * The payment flow is never degraded by metrics infrastructure.
 */
import { getPool } from "../db/db";

// ── Event types ────────────────────────────────────────────
export type MetricEvent =
    | "verify_ok"
    | "verify_error"
    | "settle_ok"
    | "settle_failed"
    | "replay_blocked"
    | "webhook_accepted"
    | "webhook_duplicate"
    | "webhook_sig_failure"
    | "request_create"
    | "request_fund"
    | "rollout_gated"
    | "rollout_kill_switch";

export interface MetricEntry {
    eventType: MetricEvent;
    latencyMs?: number;
    source?: string;         // e.g. '4payments' for webhooks
    metadata?: Record<string, unknown>;
}

// ── Non-blocking emitter ───────────────────────────────────

/**
 * Fire-and-forget metric write.
 * GUARANTEED to never throw — all errors swallowed to stderr.
 */
export function emitMetric(entry: MetricEntry): void {
    // Don't await — intentionally fire-and-forget
    writeMetric(entry).catch((err) => {
        // Fail-open: log and move on, never break the payment flow
        appLogger.error(
            `[metrics:fail-open] ${entry.eventType}: ${(err as Error).message ?? err}`
        );
    });
}

async function writeMetric(entry: MetricEntry): Promise<void> {
    try {
        let pool;
        try {
            pool = getPool();
        } catch {
            return; // inmemory mode or no DATABASE_URL — skip silently
        }

        await pool.query(
            `INSERT INTO api_metrics (event_type, latency_ms, source, metadata)
       VALUES ($1, $2, $3, $4)`,
            [
                entry.eventType,
                entry.latencyMs ?? null,
                entry.source ?? null,
                entry.metadata ? JSON.stringify(entry.metadata) : "{}",
            ]
        );
    } catch {
        // Swallow — fail-open guarantee. Caller's catch will also log.
        return;
    }
}

// ── Timer utility ──────────────────────────────────────────

export function startTimer(): () => number {
    const start = Date.now();
    return () => Date.now() - start;
}
