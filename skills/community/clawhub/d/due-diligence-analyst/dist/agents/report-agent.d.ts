/**
 * Report Agent
 * 负责尽调报告生成
 */
import type { SkillContext, SkillResponse } from '../types/index.js';
export declare class ReportAgent {
    private context?;
    initialize(context: SkillContext): Promise<void>;
    /**
     * 生成快速尽调报告
     */
    generateQuickReport(companyName: string, context: SkillContext): Promise<SkillResponse>;
    /**
     * 生成完整尽调报告（开发中）
     */
    generateFullReport(companyName: string, context: SkillContext): Promise<SkillResponse>;
    /**
     * 生成专项报告（开发中）
     */
    generateSpecializedReport(companyName: string, reportType: 'financial' | 'legal' | 'business' | 'team', context: SkillContext): Promise<SkillResponse>;
    /**
     * 格式化报告为 Markdown
     */
    private formatMarkdown;
    /**
     * 导出为 PDF（占位实现）
     */
    private exportToPDF;
    /**
     * 导出为 Word（占位实现）
     */
    private exportToWord;
}
//# sourceMappingURL=report-agent.d.ts.map