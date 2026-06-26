/**
 * Alert management
 */
import { prepare, nowUtc } from '../core/database.js';
/**
 * Get alerts since a given time
 */
export function getAlertsSince(since, watchlistIds) {
    let query = `
        SELECT id, watchlistId, snapshotId, type, source, title, detail, pushedAt, createdAt
        FROM alerts
        WHERE createdAt >= ?
    `;
    const params = [since];
    if (watchlistIds && watchlistIds.length > 0) {
        const placeholders = watchlistIds.map(() => '?').join(',');
        query += ` AND watchlistId IN (${placeholders})`;
        params.push(...watchlistIds);
    }
    query += ' ORDER BY createdAt DESC';
    const rows = prepare(query).all(...params);
    return rows.map(row => ({
        id: row.id,
        watchlistId: row.watchlistId,
        snapshotId: row.snapshotId,
        type: row.type,
        source: row.source,
        title: row.title,
        detail: row.detail,
        pushedAt: row.pushedAt,
        createdAt: row.createdAt,
    }));
}
/**
 * Get recent alerts (last N)
 */
export function getRecentAlerts(limit = 50) {
    const rows = prepare(`
        SELECT id, watchlistId, snapshotId, type, source, title, detail, pushedAt, createdAt
        FROM alerts
        ORDER BY createdAt DESC
        LIMIT ?
    `).all(limit);
    return rows.map(row => ({
        id: row.id,
        watchlistId: row.watchlistId,
        snapshotId: row.snapshotId,
        type: row.type,
        source: row.source,
        title: row.title,
        detail: row.detail,
        pushedAt: row.pushedAt,
        createdAt: row.createdAt,
    }));
}
/**
 * Get alerts for a specific watchlist
 */
export function getWatchlistAlerts(watchlistId, limit = 50) {
    const rows = prepare(`
        SELECT id, watchlistId, snapshotId, type, source, title, detail, pushedAt, createdAt
        FROM alerts
        WHERE watchlistId = ?
        ORDER BY createdAt DESC
        LIMIT ?
    `).all(watchlistId, limit);
    return rows.map(row => ({
        id: row.id,
        watchlistId: row.watchlistId,
        snapshotId: row.snapshotId,
        type: row.type,
        source: row.source,
        title: row.title,
        detail: row.detail,
        pushedAt: row.pushedAt,
        createdAt: row.createdAt,
    }));
}
/**
 * Mark alert as pushed
 */
export function markAlertPushed(alertId) {
    prepare('UPDATE alerts SET pushedAt = ? WHERE id = ?').run(nowUtc(), alertId);
}
/**
 * Get alert count by type
 */
export function getAlertCountByType(since) {
    let query = `
        SELECT type, COUNT(*) as count
        FROM alerts
    `;
    const rows = since
        ? prepare(`${query} WHERE createdAt >= ? GROUP BY type`).all(since)
        : prepare(`${query} GROUP BY type`).all();
    const result = {};
    for (const row of rows) {
        result[row.type] = row.count;
    }
    return result;
}
