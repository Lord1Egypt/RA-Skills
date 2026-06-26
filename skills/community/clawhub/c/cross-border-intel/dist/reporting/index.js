/**
 * Report generation and management
 */
import { prepare, generateLocalId, nowUtc } from '../core/database.js';
import { getActiveWatchlistIds } from '../watchlist/index.js';
import { getAlertsSince } from '../alerts/index.js';
/**
 * Get date N days ago in UTC
 */
function getDateDaysAgo(days) {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
}
/**
 * Get datetime N days ago in UTC
 */
function getDateTimeDaysAgo(days) {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString();
}
/**
 * Collect report data for a period
 */
export function collectReportData(reportType = 'daily') {
    // Calculate period
    const periodEnd = new Date().toISOString().split('T')[0];
    let periodStart;
    let createdAfter;
    if (reportType === 'weekly') {
        periodStart = getDateDaysAgo(7);
        createdAfter = getDateTimeDaysAgo(7);
    }
    else {
        periodStart = getDateDaysAgo(1);
        createdAfter = getDateTimeDaysAgo(1);
    }
    // Get active watchlist IDs
    const activeIds = getActiveWatchlistIds();
    let alerts = [];
    let snapshots = [];
    let tiktokVideos = [];
    if (activeIds.length > 0) {
        // Get alerts
        alerts = getAlertsSince(createdAfter, activeIds);
        // Get snapshots
        const snapshotPlaceholders = activeIds.map(() => '?').join(',');
        const snapshotRows = prepare(`
            SELECT
                id, watchlistId, asin, title, price, currency, bsr, bsrCategory,
                reviewCount, rating, seller, imageUrl, snapshotDate, rawData, createdAt
            FROM amazon_snapshots
            WHERE createdAt >= ? AND watchlistId IN (${snapshotPlaceholders})
            ORDER BY createdAt DESC
        `).all(createdAfter, ...activeIds);
        snapshots = snapshotRows.map(row => ({
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
        // Get TikTok hits
        const tiktokPlaceholders = activeIds.map(() => '?').join(',');
        const tiktokRows = prepare(`
            SELECT
                id, watchlistId, keyword, videoId, authorName, description,
                playCount, likeCount, commentCount, shareCount, publishTime, rawData, createdAt
            FROM tiktok_hits
            WHERE createdAt >= ? AND watchlistId IN (${tiktokPlaceholders})
            ORDER BY createdAt DESC
        `).all(createdAfter, ...activeIds);
        tiktokVideos = tiktokRows.map(row => ({
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
    return {
        reportType,
        periodStart,
        periodEnd,
        alerts,
        snapshots,
        tiktokVideos,
        dbPath: process.env.INTEL_DB_PATH || '',
    };
}
/**
 * Store a report in the database
 */
export function storeReport(reportType, content, periodStart, periodEnd, summarySource = 'openclaw') {
    const reportId = generateLocalId();
    const now = nowUtc();
    prepare(`
        INSERT INTO reports (id, reportType, content, periodStart, periodEnd, summarySource, createdAt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(reportId, reportType, content, periodStart, periodEnd, summarySource, now);
    return reportId;
}
/**
 * Get a report by ID
 */
export function getReport(reportId) {
    const row = prepare(`
        SELECT id, reportType, content, periodStart, periodEnd, summarySource, pushedAt, createdAt
        FROM reports
        WHERE id = ?
        LIMIT 1
    `).get(reportId);
    if (!row) {
        return null;
    }
    return {
        id: row.id,
        reportType: row.reportType,
        content: row.content,
        periodStart: row.periodStart,
        periodEnd: row.periodEnd,
        summarySource: row.summarySource,
        pushedAt: row.pushedAt,
        createdAt: row.createdAt,
    };
}
/**
 * Get recent reports
 */
export function getRecentReports(limit = 10) {
    const rows = prepare(`
        SELECT id, reportType, content, periodStart, periodEnd, summarySource, pushedAt, createdAt
        FROM reports
        ORDER BY createdAt DESC
        LIMIT ?
    `).all(limit);
    return rows.map(row => ({
        id: row.id,
        reportType: row.reportType,
        content: row.content,
        periodStart: row.periodStart,
        periodEnd: row.periodEnd,
        summarySource: row.summarySource,
        pushedAt: row.pushedAt,
        createdAt: row.createdAt,
    }));
}
/**
 * Get the analysis framework prompt
 */
export function getAnalysisFramework() {
    return `# 跨境电商情报分析框架

你是一位专业的跨境电商竞品分析师。请根据收到的数据，按照以下框架进行深入分析：

## 一、数据概览
- 统计本周期内的告警数量、快照数量、TikTok视频数量
- 识别数据中最值得关注的 3 个异常/亮点

## 二、Amazon 竞品深度分析
### 价格动向
- 识别价格变动的产品（涨价/降价）
- 分析价格变动可能的原因（清仓、促销、竞争等）
- 给出应对建议（跟进、观望、避开）

### BSR排名变化
- 识别排名显著上升/下降的产品
- 分析排名变化背后的趋势
- 判断品类热度的变化

### Review & 评分
- 识别评论激增或评分突变的产品
- 分析用户反馈的变化趋势
- 挖掘潜在的产品问题或机会

## 三、TikTok 趋势洞察
### 热门关键词
- 识别播放量最高的关键词
- 分析这些关键词背后的需求趋势
- 判断是否值得跟进

### 视频内容分析
- 总结高播放量视频的共同特点
- 识别有效的带货内容形式
- 给出内容创作建议

## 四、Amazon × TikTok 联动分析
- 识别 Amazon 上的产品和 TikTok 热门的关联
- 分析 TikTok 趋势对 Amazon 选品的启示
- 给出跨平台运营建议

## 五、行动建议
- 本周期最值得跟进的 3 个产品/关键词
- 下周需要重点关注的指标
- 具体的操作建议（如：增加某类目的监控、调整价格策略等）

## 输出要求
- 用中文撰写
- 语调专业、简洁、可执行
- 每个观点都要有数据支撑
- 如果数据不足，明确指出"数据不足，无法判断"
- 最后给出"今日/本周行动清单"`;
}
/**
 * Generate a daily report
 */
export function generateDailyReport() {
    return collectReportData('daily');
}
/**
 * Generate a weekly report
 */
export function generateWeeklyReport() {
    return collectReportData('weekly');
}
