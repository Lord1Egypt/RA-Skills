/**
 * Amazon product scanning and change detection
 */
import { prepare, generateLocalId, nowUtc, todayUtc, getConfigValue } from '../core/database.js';
import { listActiveAsinWatchlistRows } from '../watchlist/index.js';
import { fetchAmazonProduct } from '../api/index.js';
/**
 * Get the previous Amazon snapshot for a watchlist item
 */
export function getPreviousAmazonSnapshot(watchlistId) {
    const row = prepare(`
        SELECT
            id, watchlistId, asin, title, price, currency, bsr, bsrCategory,
            reviewCount, rating, seller, imageUrl, snapshotDate, rawData, createdAt
        FROM amazon_snapshots
        WHERE watchlistId = ?
        ORDER BY createdAt DESC
        LIMIT 1
    `).get(watchlistId);
    if (!row) {
        return null;
    }
    return {
        id: row.id,
        watchlistId: row.watchlistId,
        asin: row.asin,
        title: row.title,
        price: row.price,
        currency: row.currency,
        salesRank: row.bsr,
        salesRankCategory: row.bsrCategory,
        bsrCategory: row.bsrCategory,
        reviewCount: row.reviewCount,
        rating: row.rating,
        seller: row.seller,
        imageUrl: row.imageUrl,
        snapshotDate: row.snapshotDate,
        rawData: row.rawData,
        createdAt: row.createdAt,
    };
}
/**
 * Insert an Amazon snapshot
 */
export function insertAmazonSnapshot(watchlistId, product) {
    const snapshotId = generateLocalId();
    const now = nowUtc();
    const today = todayUtc();
    const rawData = JSON.stringify(product);
    prepare(`
        INSERT INTO amazon_snapshots (
            id, watchlistId, asin, title, price, currency, bsr, bsrCategory,
            reviewCount, rating, seller, imageUrl, snapshotDate, rawData, createdAt
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(snapshotId, watchlistId, product.asin, product.title || null, product.currentPrice || null, product.currency || null, product.salesRank || null, product.salesRankCategory || null, product.reviewCount || null, product.rating || null, product.seller || null, product.imageUrl || null, today, rawData, now);
    return snapshotId;
}
/**
 * Calculate absolute percentage change
 */
function absolutePercentChange(current, previous) {
    if (previous === 0) {
        return 0;
    }
    const delta = Math.abs(current - previous);
    return Math.floor((delta * 100) / previous);
}
/**
 * Insert an alert
 */
export function insertAmazonAlert(watchlistId, snapshotId, alertType, title, detail) {
    const alertId = generateLocalId();
    const now = nowUtc();
    prepare(`
        INSERT INTO alerts (id, watchlistId, snapshotId, type, source, title, detail, createdAt)
        VALUES (?, ?, ?, ?, 'amazon', ?, ?, ?)
    `).run(alertId, watchlistId, snapshotId, alertType, title, JSON.stringify(detail), now);
}
/**
 * Detect changes between current and previous Amazon data
 */
export function detectAmazonChanges(watchlistId, snapshotId, current, previous) {
    if (!previous) {
        return 0;
    }
    let alertsCreated = 0;
    const priceThreshold = parseInt(getConfigValue('priceChangeThreshold', '5'), 10);
    const bsrThreshold = parseInt(getConfigValue('bsrChangeThreshold', '30'), 10);
    const currentPrice = current.currentPrice || 0;
    const previousPrice = previous.price || 0;
    const currentBsr = current.salesRank || 0;
    const previousBsr = previous.bsr || 0;
    const currentReviews = current.reviewCount || 0;
    const previousReviews = previous.reviewCount || 0;
    const currentTitle = current.title || '';
    const previousTitle = previous.title || '';
    // Price change detection
    if (previousPrice > 0 && currentPrice > 0) {
        const changePercent = absolutePercentChange(currentPrice, previousPrice);
        if (changePercent >= priceThreshold) {
            if (currentPrice < previousPrice) {
                insertAmazonAlert(watchlistId, snapshotId, 'price_drop', 'Amazon price dropped', {
                    previousPrice,
                    currentPrice,
                    changePercent,
                });
            }
            else {
                insertAmazonAlert(watchlistId, snapshotId, 'price_rise', 'Amazon price increased', {
                    previousPrice,
                    currentPrice,
                    changePercent,
                });
            }
            alertsCreated++;
        }
    }
    // BSR change detection
    if (previousBsr > 0 && currentBsr > 0) {
        const changePercent = absolutePercentChange(currentBsr, previousBsr);
        if (changePercent >= bsrThreshold) {
            insertAmazonAlert(watchlistId, snapshotId, 'bsr_change', 'Amazon BSR changed significantly', {
                previousBsr,
                currentBsr,
                changePercent,
            });
            alertsCreated++;
        }
    }
    // Review spike detection
    if (currentReviews > previousReviews && (currentReviews - previousReviews) >= 20) {
        insertAmazonAlert(watchlistId, snapshotId, 'review_spike', 'Amazon review count increased', {
            previousReviewCount: previousReviews,
            currentReviewCount: currentReviews,
            newReviews: currentReviews - previousReviews,
        });
        alertsCreated++;
    }
    // Title change detection
    if (currentTitle && previousTitle && currentTitle !== previousTitle) {
        insertAmazonAlert(watchlistId, snapshotId, 'listing_change', 'Amazon listing title changed', {
            previousTitle,
            currentTitle,
        });
        alertsCreated++;
    }
    return alertsCreated;
}
/**
 * Run a full Amazon scan on all active watchlist items
 */
export async function runAmazonScan() {
    const watchlistItems = listActiveAsinWatchlistRows();
    let scannedCount = 0;
    let alertsCreated = 0;
    const errors = [];
    for (const item of watchlistItems) {
        try {
            const product = await fetchAmazonProduct(item.value, item.domain);
            const previous = getPreviousAmazonSnapshot(item.id);
            const snapshotId = insertAmazonSnapshot(item.id, product);
            const created = detectAmazonChanges(item.id, snapshotId, product, previous);
            scannedCount++;
            alertsCreated += created;
        }
        catch (error) {
            errors.push({
                asin: item.value,
                message: error.message,
            });
        }
    }
    return {
        scannedCount,
        alertsCreated,
        errors,
        dbPath: process.env.INTEL_DB_PATH || '',
    };
}
/**
 * Get all Amazon snapshots for a watchlist
 */
export function getAmazonSnapshots(watchlistId, limit = 100) {
    const rows = prepare(`
        SELECT
            id, watchlistId, asin, title, price, currency, bsr, bsrCategory,
            reviewCount, rating, seller, imageUrl, snapshotDate, rawData, createdAt
        FROM amazon_snapshots
        WHERE watchlistId = ?
        ORDER BY createdAt DESC
        LIMIT ?
    `).all(watchlistId, limit);
    return rows.map(row => ({
        id: row.id,
        watchlistId: row.watchlistId,
        asin: row.asin,
        title: row.title,
        price: row.price,
        currency: row.currency,
        salesRank: row.bsr,
        salesRankCategory: row.bsrCategory,
        bsrCategory: row.bsrCategory,
        reviewCount: row.reviewCount,
        rating: row.rating,
        seller: row.seller,
        imageUrl: row.imageUrl,
        snapshotDate: row.snapshotDate,
        rawData: row.rawData,
        createdAt: row.createdAt,
    }));
}
