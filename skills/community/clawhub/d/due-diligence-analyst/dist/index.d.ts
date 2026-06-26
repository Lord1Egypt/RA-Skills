/**
 * Due Diligence Analyst - OpenClaw Skill
 * 主入口文件
 */
import type { Skill, SkillContext, SkillResponse } from './types/index.js';
export declare class DueDiligenceAnalyst implements Skill {
    id: string;
    name: string;
    version: string;
    description: string;
    private companyAgent;
    private reportAgent;
    private context?;
    constructor();
    initialize(context: SkillContext): Promise<void>;
    handle(message: string, context: SkillContext): Promise<SkillResponse>;
    shutdown(): Promise<void>;
    /**
     * 意图识别
     */
    private identifyIntent;
    /**
     * 从消息中提取公司名称
     */
    private extractCompanyName;
    /**
     * 处理公司分析请求
     */
    private handleCompanyAnalysis;
    /**
     * 处理快速尽调请求
     */
    private handleQuickDD;
    /**
     * 处理完整尽调请求
     */
    private handleFullDD;
    /**
     * 处理报告生成请求
     */
    private handleReportGeneration;
    /**
     * 处理通用查询
     */
    private handleGeneralQuery;
}
declare const _default: DueDiligenceAnalyst;
export default _default;
export type { Skill, SkillContext, SkillResponse } from './types/index.js';
export * from './types/index.js';
//# sourceMappingURL=index.d.ts.map