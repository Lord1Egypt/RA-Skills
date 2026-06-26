/**
 * TikTok video scanning and hit detection
 */
import type { TikTokVideo, TikTokHit, TiktokScanResult } from '../core/types.js';
/**
 * Check if a TikTok video has already been recorded
 */
export declare function hasTiktokHit(watchlistId: string, videoId: string): boolean;
/**
 * Insert a TikTok hit
 */
export declare function insertTiktokHit(watchlistId: string, keyword: string, video: TikTokVideo): string;
/**
 * Insert a TikTok alert
 */
export declare function insertTiktokAlert(watchlistId: string, title: string, detail: Record<string, unknown>): void;
/**
 * Build alert title for TikTok hit
 */
export declare function buildTiktokAlertTitle(keyword: string, authorName: string | null | undefined, description: string | null | undefined): string;
/**
 * Record a TikTok hit and create an alert if it's new
 */
export declare function recordTiktokHitAndAlert(watchlistId: string, keyword: string, video: TikTokVideo): boolean;
/**
 * Process TikTok scan results for a keyword
 */
export declare function runTiktokKeywordScan(watchlistId: string, keyword: string, count?: number): Promise<TiktokScanResult>;
/**
 * Run a full TikTok scan on all active watchlist keywords
 */
export declare function runTiktokScan(): Promise<{
    totalResults: TiktokScanResult[];
    totalNewHits: number;
}>;
/**
 * Get all TikTok hits for a watchlist
 */
export declare function getTiktokHits(watchlistId: string, limit?: number): TikTokHit[];
