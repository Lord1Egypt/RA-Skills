/**
 * cross-border-intel skill for OpenClaw
 *
 * A cross-border e-commerce intelligence assistant for tracking
 * Amazon ASINs and monitoring TikTok trends.
 */
export declare const skill: {
    name: string;
    version: string;
    description: string;
    installSlug: string;
    npmPackageName: string;
    owner: string;
    category: string;
    icon: string;
};
export * from './core/index.js';
export { addWatchlistItem, removeWatchlistItem, getWatchlistItem, listActiveWatchlists, listActiveAsinWatchlistRows, listActiveTiktokWatchlistRows, watchlistItemExists, ensureWatchlistItem, addAmazonWatchlistItem, addTiktokWatchlistItem, ensureAmazonWatchlistItem, ensureTiktokWatchlistItem, getActiveWatchlistIds, } from './watchlist/index.js';
export { apiGet, apiPost, apiPut, apiDelete, fetchAmazonProduct, searchTiktokVideos, } from './api/index.js';
export { getPreviousAmazonSnapshot, insertAmazonSnapshot, detectAmazonChanges, insertAmazonAlert, runAmazonScan, getAmazonSnapshots, } from './amazon/index.js';
export { hasTiktokHit, insertTiktokHit, insertTiktokAlert, buildTiktokAlertTitle, recordTiktokHitAndAlert, runTiktokKeywordScan, runTiktokScan, getTiktokHits, } from './tiktok/index.js';
export { getAlertsSince, getRecentAlerts, getWatchlistAlerts, markAlertPushed, getAlertCountByType, } from './alerts/index.js';
export { collectReportData, storeReport, getReport, getRecentReports, getAnalysisFramework, generateDailyReport, generateWeeklyReport, } from './reporting/index.js';
/**
 * Initialize the skill (called by OpenClaw on load)
 */
export declare function initialize(): Promise<void>;
/**
 * Health check for the skill
 */
export declare function healthCheck(): {
    status: string;
    version: string;
};
declare const _default: {
    skill: {
        name: string;
        version: string;
        description: string;
        installSlug: string;
        npmPackageName: string;
        owner: string;
        category: string;
        icon: string;
    };
    initialize: typeof initialize;
    healthCheck: typeof healthCheck;
};
export default _default;
