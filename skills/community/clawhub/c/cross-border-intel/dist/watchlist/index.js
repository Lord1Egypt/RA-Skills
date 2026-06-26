/**
 * Watchlist management
 */
import { prepare, generateLocalId, nowUtc } from '../core/database.js';
/**
 * Add a watchlist item
 */
export function addWatchlistItem(platform, sourceType, value, domain = 'com') {
    // Validation
    if (platform !== 'amazon' && platform !== 'tiktok') {
        throw new Error('Platform must be amazon or tiktok');
    }
    if (sourceType !== 'asin' && sourceType !== 'keyword') {
        throw new Error('sourceType must be asin or keyword');
    }
    if (platform === 'amazon' && sourceType !== 'asin') {
        throw new Error('Amazon watchlist items must use sourceType asin');
    }
    if (platform === 'tiktok' && sourceType !== 'keyword') {
        throw new Error('TikTok watchlist items must use sourceType keyword');
    }
    if (!value) {
        throw new Error('value is required');
    }
    // Normalize ASIN to uppercase
    let normalizedValue = value;
    if (sourceType === 'asin') {
        normalizedValue = value.toUpperCase();
    }
    // Clear domain for TikTok
    let normalizedDomain = domain;
    if (platform === 'tiktok') {
        normalizedDomain = '';
    }
    const id = generateLocalId();
    const now = nowUtc();
    prepare(`
        INSERT INTO watchlists (id, platform, sourceType, value, domain, isActive, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    `).run(id, platform, sourceType, normalizedValue, normalizedDomain, now, now);
    return {
        id,
        platform,
        sourceType,
        value: normalizedValue,
        domain: normalizedDomain,
        isActive: true,
        createdAt: now,
        updatedAt: now,
    };
}
/**
 * Remove a watchlist item by ID
 */
export function removeWatchlistItem(id) {
    prepare('DELETE FROM watchlists WHERE id = ?').run(id);
}
/**
 * Get watchlist item by ID
 */
export function getWatchlistItem(id) {
    const row = prepare(`
        SELECT id, platform, sourceType, value, domain, isActive, createdAt, updatedAt
        FROM watchlists
        WHERE id = ?
        LIMIT 1
    `).get(id);
    if (!row) {
        return null;
    }
    return {
        id: row.id,
        platform: row.platform,
        sourceType: row.sourceType,
        value: row.value,
        domain: row.domain,
        isActive: Boolean(row.isActive),
        createdAt: row.createdAt,
        updatedAt: row.updatedAt,
    };
}
/**
 * List all active watchlist items for a platform
 */
export function listActiveWatchlists(platform) {
    const rows = prepare(`
        SELECT id, platform, sourceType, value, domain, isActive, createdAt, updatedAt
        FROM watchlists
        WHERE platform = ? AND isActive = 1
        ORDER BY createdAt ASC
    `).all(platform);
    return rows.map(row => ({
        id: row.id,
        platform: row.platform,
        sourceType: row.sourceType,
        value: row.value,
        domain: row.domain,
        isActive: Boolean(row.isActive),
        createdAt: row.createdAt,
        updatedAt: row.updatedAt,
    }));
}
/**
 * List all active Amazon ASIN watchlist items (returns raw data for scanning)
 */
export function listActiveAsinWatchlistRows() {
    return prepare(`
        SELECT id, value, domain
        FROM watchlists
        WHERE platform = 'amazon' AND sourceType = 'asin' AND isActive = 1
        ORDER BY createdAt ASC
    `).all();
}
/**
 * List all active TikTok keyword watchlist items
 */
export function listActiveTiktokWatchlistRows() {
    return prepare(`
        SELECT id, value
        FROM watchlists
        WHERE platform = 'tiktok' AND sourceType = 'keyword' AND isActive = 1
        ORDER BY createdAt ASC
    `).all();
}
/**
 * Check if a watchlist item exists
 */
export function watchlistItemExists(platform, sourceType, value, domain = 'com') {
    let normalizedDomain = domain;
    if (platform === 'tiktok') {
        normalizedDomain = '';
    }
    const row = prepare(`
        SELECT COUNT(*) as count
        FROM watchlists
        WHERE platform = ? AND sourceType = ? AND value = ? AND domain = ?
    `).get(platform, sourceType, value, normalizedDomain);
    return row.count;
}
/**
 * Ensure a watchlist item exists, or add it if it doesn't
 */
export function ensureWatchlistItem(platform, sourceType, value, domain = 'com') {
    const exists = watchlistItemExists(platform, sourceType, value, domain);
    if (exists > 0) {
        let normalizedDomain = domain;
        if (platform === 'tiktok') {
            normalizedDomain = '';
        }
        const row = prepare(`
            SELECT id, platform, sourceType, value, domain, isActive, createdAt, updatedAt
            FROM watchlists
            WHERE platform = ? AND sourceType = ? AND value = ? AND domain = ?
            ORDER BY createdAt DESC
            LIMIT 1
        `).get(platform, sourceType, value, normalizedDomain);
        return {
            id: row.id,
            platform: row.platform,
            sourceType: row.sourceType,
            value: row.value,
            domain: row.domain,
            isActive: Boolean(row.isActive),
            createdAt: row.createdAt,
            updatedAt: row.updatedAt,
        };
    }
    return addWatchlistItem(platform, sourceType, value, domain);
}
/**
 * Convenience: Add an Amazon ASIN to watchlist
 */
export function addAmazonWatchlistItem(asin, domain = 'com') {
    return addWatchlistItem('amazon', 'asin', asin, domain);
}
/**
 * Convenience: Add a TikTok keyword to watchlist
 */
export function addTiktokWatchlistItem(keyword) {
    return addWatchlistItem('tiktok', 'keyword', keyword, '');
}
/**
 * Convenience: Ensure an Amazon ASIN is in watchlist
 */
export function ensureAmazonWatchlistItem(asin, domain = 'com') {
    return ensureWatchlistItem('amazon', 'asin', asin, domain);
}
/**
 * Convenience: Ensure a TikTok keyword is in watchlist
 */
export function ensureTiktokWatchlistItem(keyword) {
    return ensureWatchlistItem('tiktok', 'keyword', keyword, '');
}
/**
 * Get all active watchlist IDs
 */
export function getActiveWatchlistIds() {
    const rows = prepare(`
        SELECT id FROM watchlists WHERE isActive = 1
    `).all();
    return rows.map(r => r.id);
}
