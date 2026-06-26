/**
 * cross-border-intel skill for OpenClaw
 *
 * A cross-border e-commerce intelligence assistant for tracking
 * Amazon ASINs and monitoring TikTok trends.
 */
// Core skill manifest
export const skill = {
    name: 'cross-border-intel',
    version: '0.1.0',
    description: '面向跨境卖家的选品与竞品情报助手，自动监控 Amazon ASIN 动态并追踪 TikTok 爆品趋势',
    installSlug: 'beansmile/skill-cross-border-intel',
    npmPackageName: '@beansmile/skill-cross-border-intel',
    owner: 'beansmile',
    category: 'business',
    icon: '🔍',
};
// Export core types and functions
export * from './core/index.js';
// Export watchlist management
export { addWatchlistItem, removeWatchlistItem, getWatchlistItem, listActiveWatchlists, listActiveAsinWatchlistRows, listActiveTiktokWatchlistRows, watchlistItemExists, ensureWatchlistItem, addAmazonWatchlistItem, addTiktokWatchlistItem, ensureAmazonWatchlistItem, ensureTiktokWatchlistItem, getActiveWatchlistIds, } from './watchlist/index.js';
// Export API client
export { apiGet, apiPost, apiPut, apiDelete, fetchAmazonProduct, searchTiktokVideos, } from './api/index.js';
// Export Amazon scanning
export { getPreviousAmazonSnapshot, insertAmazonSnapshot, detectAmazonChanges, insertAmazonAlert, runAmazonScan, getAmazonSnapshots, } from './amazon/index.js';
// Export TikTok scanning
export { hasTiktokHit, insertTiktokHit, insertTiktokAlert, buildTiktokAlertTitle, recordTiktokHitAndAlert, runTiktokKeywordScan, runTiktokScan, getTiktokHits, } from './tiktok/index.js';
// Export alerts
export { getAlertsSince, getRecentAlerts, getWatchlistAlerts, markAlertPushed, getAlertCountByType, } from './alerts/index.js';
// Export reporting
export { collectReportData, storeReport, getReport, getRecentReports, getAnalysisFramework, generateDailyReport, generateWeeklyReport, } from './reporting/index.js';
/**
 * Initialize the skill (called by OpenClaw on load)
 */
export async function initialize() {
    const { initDatabase } = await import('./core/index.js');
    await initDatabase();
}
/**
 * Health check for the skill
 */
export function healthCheck() {
    return {
        status: 'ok',
        version: skill.version,
    };
}
// Default export
export default {
    skill,
    initialize,
    healthCheck,
};
