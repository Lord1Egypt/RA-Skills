/**
 * 尽调报告相关类型定义
 */
import type { CompanyProfile } from './company.js';
import type { RiskAssessment } from './risk.js';
export interface ExecutiveSummary {
    conclusion: string;
    rating: 'A' | 'B' | 'C' | 'D' | 'F';
    recommendation: 'proceed' | 'proceed_with_caution' | 'further_review' | 'pass';
    keyFindings: {
        strengths: string[];
        concerns: string[];
        criticalIssues: string[];
    };
    nextSteps: string[];
}
export interface DDReport {
    reportId: string;
    companyName: string;
    reportDate: string;
    reportType: 'quick' | 'standard' | 'comprehensive' | 'specialized';
    executiveSummary: ExecutiveSummary;
    companyProfile: CompanyProfile;
    riskAssessment: RiskAssessment;
    sections?: {
        financial?: unknown;
        legal?: unknown;
        business?: unknown;
        team?: unknown;
        market?: unknown;
    };
    appendices?: {
        title: string;
        content: string;
    }[];
    metadata: {
        analyst: string;
        version: string;
        confidential: boolean;
    };
}
export type ReportFormat = 'text' | 'markdown' | 'pdf' | 'docx' | 'html';
//# sourceMappingURL=report.d.ts.map