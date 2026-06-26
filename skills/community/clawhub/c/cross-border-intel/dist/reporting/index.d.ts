/**
 * Report generation and management
 */
import type { Report, ReportData, ReportType } from '../core/types.js';
/**
 * Collect report data for a period
 */
export declare function collectReportData(reportType?: ReportType): ReportData;
/**
 * Store a report in the database
 */
export declare function storeReport(reportType: ReportType, content: string, periodStart: string, periodEnd: string, summarySource?: string): string;
/**
 * Get a report by ID
 */
export declare function getReport(reportId: string): Report | null;
/**
 * Get recent reports
 */
export declare function getRecentReports(limit?: number): Report[];
/**
 * Get the analysis framework prompt
 */
export declare function getAnalysisFramework(): string;
/**
 * Generate a daily report
 */
export declare function generateDailyReport(): ReportData;
/**
 * Generate a weekly report
 */
export declare function generateWeeklyReport(): ReportData;
