/**
 * Alert management
 */
import type { Alert } from '../core/types.js';
/**
 * Get alerts since a given time
 */
export declare function getAlertsSince(since: string, watchlistIds?: string[]): Alert[];
/**
 * Get recent alerts (last N)
 */
export declare function getRecentAlerts(limit?: number): Alert[];
/**
 * Get alerts for a specific watchlist
 */
export declare function getWatchlistAlerts(watchlistId: string, limit?: number): Alert[];
/**
 * Mark alert as pushed
 */
export declare function markAlertPushed(alertId: string): void;
/**
 * Get alert count by type
 */
export declare function getAlertCountByType(since?: string): Record<string, number>;
