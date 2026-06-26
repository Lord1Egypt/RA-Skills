/**
 * Amazon product scanning and change detection
 */
import type { AmazonSnapshot, AmazonProduct, Alert, ScanResult } from '../core/types.js';
/**
 * Get the previous Amazon snapshot for a watchlist item
 */
export declare function getPreviousAmazonSnapshot(watchlistId: string): AmazonSnapshot | null;
/**
 * Insert an Amazon snapshot
 */
export declare function insertAmazonSnapshot(watchlistId: string, product: AmazonProduct): string;
/**
 * Insert an alert
 */
export declare function insertAmazonAlert(watchlistId: string, snapshotId: string, alertType: Alert['type'], title: string, detail: Record<string, unknown>): void;
/**
 * Detect changes between current and previous Amazon data
 */
export declare function detectAmazonChanges(watchlistId: string, snapshotId: string, current: AmazonProduct, previous: AmazonSnapshot | null): number;
/**
 * Run a full Amazon scan on all active watchlist items
 */
export declare function runAmazonScan(): Promise<ScanResult>;
/**
 * Get all Amazon snapshots for a watchlist
 */
export declare function getAmazonSnapshots(watchlistId: string, limit?: number): AmazonSnapshot[];
