/**
 * Core types for cross-border-intel skill
 */
export type Platform = 'amazon' | 'tiktok';
export type SourceType = 'asin' | 'keyword';
export interface Watchlist {
    id: string;
    platform: Platform;
    sourceType: SourceType;
    value: string;
    domain: string;
    isActive: boolean;
    createdAt: string;
    updatedAt: string;
}
export interface AmazonProduct {
    asin: string;
    title?: string | null;
    currentPrice?: number | null;
    currency?: string | null;
    salesRank?: number | null;
    salesRankCategory?: string | null;
    reviewCount?: number | null;
    rating?: number | null;
    seller?: string | null;
    imageUrl?: string | null;
}
export interface AmazonSnapshot extends AmazonProduct {
    id: string;
    watchlistId: string;
    asin: string;
    title?: string | null;
    price?: number | null;
    currency?: string | null;
    salesRank?: number | null;
    bsr?: number | null;
    salesRankCategory?: string | null;
    bsrCategory?: string | null;
    reviewCount?: number | null;
    rating?: number | null;
    seller?: string | null;
    imageUrl?: string | null;
    snapshotDate: string;
    rawData?: string | null;
    createdAt: string;
}
export interface TikTokVideo {
    videoId: string;
    authorName?: string | null;
    description?: string | null;
    playCount?: number | null;
    likeCount?: number | null;
    commentCount?: number | null;
    shareCount?: number | null;
    publishTime?: string | null;
}
export interface TikTokHit extends TikTokVideo {
    id: string;
    watchlistId?: string | null;
    keyword: string;
    rawData?: string | null;
    createdAt: string;
}
export type AlertType = 'price_drop' | 'price_rise' | 'bsr_change' | 'review_spike' | 'listing_change' | 'tiktok_hit';
export interface Alert {
    id: string;
    watchlistId?: string | null;
    snapshotId?: string | null;
    type: AlertType;
    source: 'amazon' | 'tiktok';
    title: string;
    detail?: string | null;
    pushedAt?: string | null;
    createdAt: string;
}
export type ReportType = 'daily' | 'weekly';
export interface Report {
    id: string;
    reportType: ReportType;
    content: string;
    periodStart?: string | null;
    periodEnd?: string | null;
    summarySource: string;
    pushedAt?: string | null;
    createdAt: string;
}
export interface Job {
    id: string;
    jobType: string;
    cadence?: string | null;
    enabled: boolean;
    lastRunAt?: string | null;
    nextRunAt?: string | null;
    lockToken?: string | null;
    lockExpiresAt?: string | null;
    createdAt: string;
    updatedAt: string;
}
export interface ConfigValue {
    priceChangeThreshold?: number;
    bsrChangeThreshold?: number;
    tiktokViralPlays?: number;
    reportSummaryMode?: 'backend' | 'openclaw';
}
export interface ApiResponse<T = unknown> {
    success: boolean;
    data?: T;
    message?: string;
}
export interface AmazonProductResponse {
    product: AmazonProduct;
}
export interface TikTokSearchResponse {
    videos: TikTokVideo[];
}
export interface ScanResult {
    scannedCount: number;
    alertsCreated: number;
    errors: Array<{
        asin?: string;
        keyword?: string;
        message: string;
    }>;
    dbPath: string;
}
export interface TiktokScanResult {
    watchlistId: string;
    keyword: string;
    scannedVideos: number;
    newHits: number;
    alertsCreated: number;
}
export interface ReportData {
    reportType: ReportType;
    periodStart: string;
    periodEnd: string;
    alerts: Alert[];
    snapshots: AmazonSnapshot[];
    tiktokVideos: TikTokHit[];
    dbPath: string;
}
