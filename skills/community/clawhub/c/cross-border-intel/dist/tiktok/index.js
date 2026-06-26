/**
 * TikTok video scanning and hit detection
 */
import { prepare, generateLocalId, nowUtc } from '../core/database.js';
import { listActiveTiktokWatchlistRows } from '../watchlist/index.js';
import { searchTiktokVideos } from '../api/index.js';
/**
 * Check if a TikTok video has already been recorded
 */
export function hasTiktokHit(watchlistId, videoId) {
    const row = prepare(`
        SELECT COUNT(*) as count
        FROM tiktok_hits
        WHERE watchlistId = ? AND videoId = ?
        LIMIT 1
    `).get(watchlistId, videoId);
    return row.count > 0;
}
/**
 * Insert a TikTok hit
 */
export function insertTiktokHit(watchlistId, keyword, video) {
    const hitId = generateLocalId();
    const now = nowUtc();
    const rawData = JSON.stringify(video);
    prepare(`
        INSERT INTO tiktok_hits (
            id, watchlistId, keyword, videoId, authorName, description,
            playCount, likeCount, commentCount, shareCount, publishTime, rawData, createdAt
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(hitId, watchlistId, keyword, video.videoId, video.authorName || null, video.description || null, video.playCount || null, video.likeCount || null, video.commentCount || null, video.shareCount || null, video.publishTime || null, rawData, now);
    return hitId;
}
/**
 * Insert a TikTok alert
 */
export function insertTiktokAlert(watchlistId, title, detail) {
    const alertId = generateLocalId();
    const now = nowUtc();
    prepare(`
        INSERT INTO alerts (id, watchlistId, type, source, title, detail, createdAt)
        VALUES (?, ?, 'tiktok_hit', 'tiktok', ?, ?, ?)
    `).run(alertId, watchlistId, title, JSON.stringify(detail), now);
}
/**
 * Build alert title for TikTok hit
 */
export function buildTiktokAlertTitle(keyword, authorName, description) {
    const summary = description || authorName || '';
    if (summary) {
        const truncated = summary.substring(0, 80);
        return `New TikTok hit for ${keyword}: ${truncated}`;
    }
    return `New TikTok hit for ${keyword}`;
}
/**
 * Record a TikTok hit and create an alert if it's new
 */
export function recordTiktokHitAndAlert(watchlistId, keyword, video) {
    // Check if already exists
    if (hasTiktokHit(watchlistId, video.videoId)) {
        return false;
    }
    // Insert the hit
    insertTiktokHit(watchlistId, keyword, video);
    // Create alert
    const title = buildTiktokAlertTitle(keyword, video.authorName, video.description);
    const detail = {
        keyword,
        videoId: video.videoId,
        authorName: video.authorName,
        description: video.description,
        publishTime: video.publishTime,
        playCount: video.playCount || 0,
        likeCount: video.likeCount || 0,
        commentCount: video.commentCount || 0,
        shareCount: video.shareCount || 0,
    };
    insertTiktokAlert(watchlistId, title, detail);
    return true;
}
/**
 * Process TikTok scan results for a keyword
 */
export async function runTiktokKeywordScan(watchlistId, keyword, count = 20) {
    const videos = await searchTiktokVideos(keyword, count);
    let newHits = 0;
    let alertsCreated = 0;
    for (const video of videos) {
        const created = recordTiktokHitAndAlert(watchlistId, keyword, video);
        if (created) {
            newHits++;
            alertsCreated++;
        }
    }
    return {
        watchlistId,
        keyword,
        scannedVideos: videos.length,
        newHits,
        alertsCreated,
    };
}
/**
 * Run a full TikTok scan on all active watchlist keywords
 */
export async function runTiktokScan() {
    const watchlistItems = listActiveTiktokWatchlistRows();
    const results = [];
    let totalNewHits = 0;
    for (const item of watchlistItems) {
        const result = await runTiktokKeywordScan(item.id, item.value);
        results.push(result);
        totalNewHits += result.newHits;
    }
    return {
        totalResults: results,
        totalNewHits,
    };
}
/**
 * Get all TikTok hits for a watchlist
 */
export function getTiktokHits(watchlistId, limit = 100) {
    const rows = prepare(`
        SELECT
            id, watchlistId, keyword, videoId, authorName, description,
            playCount, likeCount, commentCount, shareCount, publishTime, rawData, createdAt
        FROM tiktok_hits
        WHERE watchlistId = ?
        ORDER BY createdAt DESC
        LIMIT ?
    `).all(watchlistId, limit);
    return rows.map(row => ({
        id: row.id,
        watchlistId: row.watchlistId,
        keyword: row.keyword,
        videoId: row.videoId,
        authorName: row.authorName,
        description: row.description,
        playCount: row.playCount,
        likeCount: row.likeCount,
        commentCount: row.commentCount,
        shareCount: row.shareCount,
        publishTime: row.publishTime,
        rawData: row.rawData,
        createdAt: row.createdAt,
    }));
}
