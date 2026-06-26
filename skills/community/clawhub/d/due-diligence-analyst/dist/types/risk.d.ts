/**
 * 风险评估相关类型定义
 */
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type RiskCategory = 'financial' | 'legal' | 'operational' | 'market' | 'team' | 'compliance' | 'reputation';
export interface RiskItem {
    id: string;
    category: RiskCategory;
    level: RiskLevel;
    title: string;
    description: string;
    impact: string;
    likelihood: 'low' | 'medium' | 'high';
    mitigation?: string;
    identifiedAt: string;
}
export interface RiskAssessment {
    overallRating: 'A' | 'B' | 'C' | 'D' | 'F';
    overallScore: number;
    riskItems: RiskItem[];
    summary: {
        criticalCount: number;
        highCount: number;
        mediumCount: number;
        lowCount: number;
    };
    recommendations: string[];
    assessedAt: string;
}
//# sourceMappingURL=risk.d.ts.map