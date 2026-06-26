/**
 * Watchlist management
 */
import type { Platform, SourceType, Watchlist } from '../core/types.js';
/**
 * Add a watchlist item
 */
export declare function addWatchlistItem(platform: Platform, sourceType: SourceType, value: string, domain?: string): Watchlist;
/**
 * Remove a watchlist item by ID
 */
export declare function removeWatchlistItem(id: string): void;
/**
 * Get watchlist item by ID
 */
export declare function getWatchlistItem(id: string): Watchlist | null;
/**
 * List all active watchlist items for a platform
 */
export declare function listActiveWatchlists(platform: Platform): Watchlist[];
/**
 * List all active Amazon ASIN watchlist items (returns raw data for scanning)
 */
export declare function listActiveAsinWatchlistRows(): Array<{
    id: string;
    value: string;
    domain: string;
}>;
/**
 * List all active TikTok keyword watchlist items
 */
export declare function listActiveTiktokWatchlistRows(): Array<{
    id: string;
    value: string;
}>;
/**
 * Check if a watchlist item exists
 */
export declare function watchlistItemExists(platform: Platform, sourceType: SourceType, value: string, domain?: string): number;
/**
 * Ensure a watchlist item exists, or add it if it doesn't
 */
export declare function ensureWatchlistItem(platform: Platform, sourceType: SourceType, value: string, domain?: string): Watchlist;
/**
 * Convenience: Add an Amazon ASIN to watchlist
 */
export declare function addAmazonWatchlistItem(asin: string, domain?: string): Watchlist;
/**
 * Convenience: Add a TikTok keyword to watchlist
 */
export declare function addTiktokWatchlistItem(keyword: string): Watchlist;
/**
 * Convenience: Ensure an Amazon ASIN is in watchlist
 */
export declare function ensureAmazonWatchlistItem(asin: string, domain?: string): Watchlist;
/**
 * Convenience: Ensure a TikTok keyword is in watchlist
 */
export declare function ensureTiktokWatchlistItem(keyword: string): Watchlist;
/**
 * Get all active watchlist IDs
 */
export declare function getActiveWatchlistIds(): string[];
