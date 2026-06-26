/**
 * Admin Status Collector — gathers system metrics for /status command.
 *
 * Data sources:
 * - Stellar Horizon API → Treasury USDC balance
 * - 4Payments API → Account balance
 * - PostgreSQL → Cards, clients, webhooks, revenue
 *
 * All queries are fail-safe: return null on error to avoid crashing /status.
 *
 * @module modules/admin/statusCollector
 */

import { env } from "../../config/env";
import { query } from "../../db/db";
import { getFourPaymentsClient } from "../../services/fourPaymentsClient";
import { appLogger } from "../../utils/logger";

// ── Types ──────────────────────────────────────────────────

export interface AdminStatus {
    finances: {
        treasuryUsdc: number | null;
        fourPaymentsBalance: number | null;
        totalRevenue: number | null;
        totalVolume: number | null;
    };
    clients: {
        total: number | null;
        linked: number | null;
        daaToday: number | null;
        daa7d: number | null;
    };
    cards: {
        total: number | null;
        active: number | null;
        frozen: number | null;
        last24h: number | null;
    };
    system: {
        uptimeSeconds: number;
        memoryMb: number;
        nodeVersion: string;
        webhooks24h: number | null;
        lastWebhookAgo: string | null;
        errors24h: number | null;
    };
}

// ── Collectors ─────────────────────────────────────────────

/**
 * Fetch Treasury USDC balance from Stellar Horizon API.
 * GET {HORIZON_URL}/accounts/{address}
 */
async function getTreasuryBalance(): Promise<number | null> {
    try {
        const url = `${env.STELLAR_HORIZON_URL}/accounts/${env.STELLAR_TREASURY_ADDRESS}`;
        const res = await fetch(url, {
            headers: { Accept: "application/json" },
            signal: AbortSignal.timeout(5000),
        });

        if (!res.ok) return null;

        const data = (await res.json()) as {
            balances: Array<{
                asset_type: string;
                asset_code?: string;
                asset_issuer?: string;
                balance: string;
            }>;
        };

        // Find USDC balance (classic or SAC)
        const usdc = data.balances.find(
            (b) =>
                b.asset_code === "USDC" &&
                (b.asset_type === "credit_alphanum4" || b.asset_type === "credit_alphanum12")
        );

        return usdc ? parseFloat(usdc.balance) : 0;
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] Treasury balance fetch failed");
        return null;
    }
}

/**
 * Fetch 4Payments account balance.
 */
async function get4PaymentsBalance(): Promise<number | null> {
    try {
        const fp = getFourPaymentsClient();
        const result = await fp.getAccountBalance();
        return result.balance;
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] 4Payments balance fetch failed");
        return null;
    }
}

/**
 * Card statistics from the cards table.
 */
async function getCardStats(): Promise<{
    total: number | null;
    active: number | null;
    frozen: number | null;
    last24h: number | null;
    uniqueWallets: number | null;
    totalVolume: number | null;
    totalRevenue: number | null;
}> {
    try {
        const rows = await query<{
            total: string;
            active: string;
            frozen: string;
            last24h: string;
            unique_wallets: string;
            total_volume: string;
            total_revenue: string;
        }>(`
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE status = 'active') as active,
                COUNT(*) FILTER (WHERE status = 'frozen') as frozen,
                COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '24 hours') as last24h,
                COUNT(DISTINCT wallet_address) as unique_wallets,
                COALESCE(SUM(initial_amount), 0) as total_volume,
                COALESCE(SUM(balance - initial_amount), 0) as total_revenue
            FROM cards
        `);

        const r = rows[0];
        return {
            total: parseInt(r.total, 10),
            active: parseInt(r.active, 10),
            frozen: parseInt(r.frozen, 10),
            last24h: parseInt(r.last24h, 10),
            uniqueWallets: parseInt(r.unique_wallets, 10),
            totalVolume: parseFloat(r.total_volume),
            totalRevenue: parseFloat(r.total_revenue),
        };
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] Card stats query failed");
        return {
            total: null,
            active: null,
            frozen: null,
            last24h: null,
            uniqueWallets: null,
            totalVolume: null,
            totalRevenue: null,
        };
    }
}

/**
 * Linked Telegram accounts count.
 */
async function getLinkedAccounts(): Promise<number | null> {
    try {
        const rows = await query<{ count: string }>(
            `SELECT COUNT(*) as count FROM owner_telegram_links WHERE status = 'active'`
        );
        return parseInt(rows[0].count, 10);
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] Telegram bindings query failed");
        return null;
    }
}

/**
 * Webhook event stats from last 24 hours.
 */
async function getWebhookStats(): Promise<{
    count24h: number | null;
    lastAgo: string | null;
    errors24h: number | null;
}> {
    try {
        const rows = await query<{
            total: string;
            last_received: string | null;
        }>(`
            SELECT
                COUNT(*) FILTER (WHERE received_at >= NOW() - INTERVAL '24 hours') as total,
                MAX(received_at) as last_received
            FROM webhook_events
        `);

        const r = rows[0];
        const count24h = parseInt(r.total, 10);

        let lastAgo: string | null = null;
        if (r.last_received) {
            const diffMs = Date.now() - new Date(r.last_received).getTime();
            const mins = Math.floor(diffMs / 60000);
            if (mins < 60) {
                lastAgo = `${mins}m ago`;
            } else {
                const hours = Math.floor(mins / 60);
                lastAgo = `${hours}h ${mins % 60}m ago`;
            }
        }

        return { count24h, lastAgo, errors24h: 0 };
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] Webhook stats query failed");
        return { count24h: null, lastAgo: null, errors24h: null };
    }
}

/**
 * Daily Active Agents — unique wallets active today and in last 7 days.
 */
async function getDailyActiveAgents(): Promise<{ today: number | null; last7d: number | null }> {
    try {
        const rows = await query<{ daa_today: string; daa_7d: string }>(`
            SELECT
                COUNT(DISTINCT wallet_address) FILTER (WHERE request_date = CURRENT_DATE) as daa_today,
                COUNT(DISTINCT wallet_address) FILTER (WHERE request_date >= CURRENT_DATE - INTERVAL '7 days') as daa_7d
            FROM api_activity
        `);
        return {
            today: parseInt(rows[0].daa_today, 10),
            last7d: parseInt(rows[0].daa_7d, 10),
        };
    } catch (err) {
        appLogger.error({ err }, "[StatusCollector] DAA query failed");
        return { today: null, last7d: null };
    }
}

// ── Main Collector ─────────────────────────────────────────

/**
 * Collect all status data in parallel. Each source is independent
 * and fail-safe — a failed source returns null, doesn't block others.
 */
export async function collectStatus(): Promise<AdminStatus> {
    const [
        treasuryUsdc,
        fpBalance,
        cardStats,
        linkedAccounts,
        webhookStats,
        daa,
    ] = await Promise.all([
        getTreasuryBalance(),
        get4PaymentsBalance(),
        getCardStats(),
        getLinkedAccounts(),
        getWebhookStats(),
        getDailyActiveAgents(),
    ]);

    return {
        finances: {
            treasuryUsdc,
            fourPaymentsBalance: fpBalance,
            totalRevenue: cardStats.totalRevenue,
            totalVolume: cardStats.totalVolume,
        },
        clients: {
            total: cardStats.uniqueWallets,
            linked: linkedAccounts,
            daaToday: daa.today,
            daa7d: daa.last7d,
        },
        cards: {
            total: cardStats.total,
            active: cardStats.active,
            frozen: cardStats.frozen,
            last24h: cardStats.last24h,
        },
        system: {
            uptimeSeconds: process.uptime(),
            memoryMb: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
            nodeVersion: process.version,
            webhooks24h: webhookStats.count24h,
            lastWebhookAgo: webhookStats.lastAgo,
            errors24h: webhookStats.errors24h,
        },
    };
}

// ── Formatter ──────────────────────────────────────────────

function fmt(n: number | null, prefix = "$"): string {
    if (n === null) return "⚠️ N/A";
    if (prefix === "$") return `$${n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    return n.toLocaleString("en-US");
}

function fmtNum(n: number | null): string {
    if (n === null) return "⚠️ N/A";
    return n.toLocaleString("en-US");
}

/**
 * Format collected status data as a Telegram HTML message.
 */
export function formatStatusMessage(s: AdminStatus): string {
    const hours = Math.floor(s.system.uptimeSeconds / 3600);
    const mins = Math.floor((s.system.uptimeSeconds % 3600) / 60);

    return (
        `📊 <b>ASG Card — System Status</b>\n\n` +

        `💰 <b>Finances</b>\n` +
        `├ Treasury: ${s.finances.treasuryUsdc !== null ? fmt(s.finances.treasuryUsdc, "$") + " USDC" : "⚠️ N/A"}\n` +
        `├ 4Payments: ${fmt(s.finances.fourPaymentsBalance)}\n` +
        `├ Revenue: ${fmt(s.finances.totalRevenue)}\n` +
        `└ Volume: ${fmt(s.finances.totalVolume)}\n\n` +

        `👥 <b>Clients & Cards</b>\n` +
        `├ Wallets: ${fmtNum(s.clients.total)}\n` +
        `├ TG Linked: ${fmtNum(s.clients.linked)}\n` +
        `├ DAA (today): ${fmtNum(s.clients.daaToday)}\n` +
        `├ DAA (7d): ${fmtNum(s.clients.daa7d)}\n` +
        `├ Cards total: ${fmtNum(s.cards.total)}\n` +
        `├ Active: ${fmtNum(s.cards.active)}\n` +
        `├ Frozen: ${fmtNum(s.cards.frozen)}\n` +
        `└ Cards 24h: +${fmtNum(s.cards.last24h)}\n\n` +

        `🔗 <b>System</b>\n` +
        `├ Uptime: ${hours}h ${mins}m\n` +
        `├ Memory: ${s.system.memoryMb} MB\n` +
        `├ Node: ${s.system.nodeVersion}\n` +
        `├ Webhooks 24h: ${fmtNum(s.system.webhooks24h)}\n` +
        `├ Last webhook: ${s.system.lastWebhookAgo ?? "never"}\n` +
        `└ Errors 24h: ${fmtNum(s.system.errors24h)}`
    );
}
