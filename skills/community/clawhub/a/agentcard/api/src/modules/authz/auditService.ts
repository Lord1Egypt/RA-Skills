import { appLogger } from "../../utils/logger";
/**
 * Audit Service — structured logging for all sensitive actions.
 *
 * Records who/when/what/result/ip to authz_audit_log table.
 * Fail-open: audit failures never block the main operation.
 *
 * @module modules/authz/auditService
 */

import { query } from "../../db/db";

// ── Types ──────────────────────────────────────────────────

export type ActorType = "telegram_user" | "wallet_owner" | "system";
export type Decision = "allow" | "deny";

export interface AuditEntry {
    actorType: ActorType;
    actorId: string;
    action: string;
    resourceId?: string;
    decision: Decision;
    reason?: string;
    ipAddress?: string;
}

// ── Service ────────────────────────────────────────────────

export class AuditService {
    /** Log a sensitive action. Never throws — audit failures are logged to stderr. */
    static async log(entry: AuditEntry): Promise<void> {
        try {
            await query(
                `INSERT INTO authz_audit_log
           (actor_type, actor_id, action, resource_id, decision, reason, ip_address)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
                [
                    entry.actorType,
                    entry.actorId,
                    entry.action,
                    entry.resourceId ?? null,
                    entry.decision,
                    entry.reason ?? null,
                    entry.ipAddress ?? null,
                ]
            );
        } catch (error) {
            // Audit failures must never block the main operation
            appLogger.error({ err: error }, "[AUDIT] Failed to write audit log");
        }
    }

    /** Query recent audit entries for an actor. */
    static async getByActor(actorId: string, limit = 50): Promise<AuditEntry[]> {
        const rows = await query<{
            actor_type: string;
            actor_id: string;
            action: string;
            resource_id: string | null;
            decision: string;
            reason: string | null;
            ip_address: string | null;
            created_at: string;
        }>(
            `SELECT actor_type, actor_id, action, resource_id, decision, reason, ip_address, created_at
       FROM authz_audit_log
       WHERE actor_id = $1
       ORDER BY created_at DESC
       LIMIT $2`,
            [actorId, limit]
        );

        return rows.map((r) => ({
            actorType: r.actor_type as ActorType,
            actorId: r.actor_id,
            action: r.action,
            resourceId: r.resource_id ?? undefined,
            decision: r.decision as Decision,
            reason: r.reason ?? undefined,
            ipAddress: r.ip_address ?? undefined,
        }));
    }
}
