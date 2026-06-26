/**
 * Company Profile Agent
 * 负责公司基本信息分析
 */
import type { SkillContext, SkillResponse } from '../types/index.js';
export declare class CompanyProfileAgent {
    private context?;
    initialize(context: SkillContext): Promise<void>;
    /**
     * 分析公司基本信息
     */
    analyzeCompany(companyName: string, context: SkillContext): Promise<SkillResponse>;
    /**
     * 收集公司信息（占位实现）
     * 未来集成企查查/天眼查 API
     */
    private collectCompanyData;
    /**
     * 分析股权结构
     */
    private analyzeShareholderStructure;
    /**
     * 识别关联方
     */
    private identifyRelatedParties;
    /**
     * 分析历史变更
     */
    private analyzeHistoricalChanges;
}
//# sourceMappingURL=company-agent.d.ts.map