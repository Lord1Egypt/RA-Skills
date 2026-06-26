/**
 * Due Diligence Analyst - OpenClaw Skill
 * 主入口文件
 */
import { CompanyProfileAgent } from './agents/company-agent.js';
import { ReportAgent } from './agents/report-agent.js';
export class DueDiligenceAnalyst {
    id = 'due-diligence-analyst';
    name = 'Due Diligence Analyst';
    version = '0.1.0';
    description = 'AI-powered due diligence analysis for investment decisions';
    companyAgent;
    reportAgent;
    context;
    constructor() {
        this.companyAgent = new CompanyProfileAgent();
        this.reportAgent = new ReportAgent();
    }
    async initialize(context) {
        console.log('[DD Analyst] Initializing...');
        this.context = context;
        await this.companyAgent.initialize(context);
        await this.reportAgent.initialize(context);
        console.log('[DD Analyst] Initialized successfully');
    }
    async handle(message, context) {
        console.log(`[DD Analyst] Handling message: ${message}`);
        try {
            // 意图识别
            const intent = await this.identifyIntent(message, context);
            // 根据意图路由到不同的 Agent
            switch (intent.type) {
                case 'company_analysis':
                    return await this.handleCompanyAnalysis(intent.params.companyName, context);
                case 'quick_dd':
                    return await this.handleQuickDD(intent.params.companyName, context);
                case 'full_dd':
                    return await this.handleFullDD(intent.params.companyName, context);
                case 'report_generation':
                    return await this.handleReportGeneration(intent.params, context);
                case 'general_query':
                default:
                    return await this.handleGeneralQuery(message, context);
            }
        }
        catch (error) {
            console.error('[DD Analyst] Error:', error);
            return {
                type: 'error',
                content: `处理请求时出错: ${error instanceof Error ? error.message : '未知错误'}`,
            };
        }
    }
    async shutdown() {
        console.log('[DD Analyst] Shutting down');
    }
    /**
     * 意图识别
     */
    async identifyIntent(message, context) {
        const lowerMessage = message.toLowerCase();
        // 简单的关键词匹配（后续可以用 LLM 增强）
        if (lowerMessage.includes('analyze') || lowerMessage.includes('分析')) {
            const companyName = this.extractCompanyName(message);
            return {
                type: 'company_analysis',
                params: { companyName },
            };
        }
        if (lowerMessage.includes('quick dd') || lowerMessage.includes('快速尽调')) {
            const companyName = this.extractCompanyName(message);
            return {
                type: 'quick_dd',
                params: { companyName },
            };
        }
        if (lowerMessage.includes('full dd') ||
            lowerMessage.includes('complete dd') ||
            lowerMessage.includes('完整尽调') ||
            lowerMessage.includes('全面尽调')) {
            const companyName = this.extractCompanyName(message);
            return {
                type: 'full_dd',
                params: { companyName },
            };
        }
        if (lowerMessage.includes('report') || lowerMessage.includes('报告')) {
            return {
                type: 'report_generation',
                params: { request: message },
            };
        }
        return {
            type: 'general_query',
            params: { query: message },
        };
    }
    /**
     * 从消息中提取公司名称
     */
    extractCompanyName(message) {
        // 简单实现：移除常见关键词后的剩余部分
        const cleaned = message
            .replace(/analyze|分析|quick dd|full dd|快速尽调|完整尽调|全面尽调|company|公司|：|:/gi, '')
            .trim();
        return cleaned || '未指定公司';
    }
    /**
     * 处理公司分析请求
     */
    async handleCompanyAnalysis(companyName, context) {
        console.log(`[DD Analyst] Analyzing company: ${companyName}`);
        return await this.companyAgent.analyzeCompany(companyName, context);
    }
    /**
     * 处理快速尽调请求
     */
    async handleQuickDD(companyName, context) {
        console.log(`[DD Analyst] Quick DD for: ${companyName}`);
        // 执行快速分析
        const companyProfile = await this.companyAgent.analyzeCompany(companyName, context);
        // 生成简化报告
        const report = await this.reportAgent.generateQuickReport(companyName, context);
        return report;
    }
    /**
     * 处理完整尽调请求
     */
    async handleFullDD(companyName, context) {
        console.log(`[DD Analyst] Full DD for: ${companyName}`);
        return {
            type: 'text',
            content: `完整尽调功能开发中...\n\n完整尽调将包括：\n- 公司信息分析\n- 财务尽调\n- 法律合规检查\n- 业务分析\n- 团队背调\n- 市场分析\n- 风险评估\n- 详细报告生成\n\n当前版本仅支持快速尽调和公司信息分析。`,
        };
    }
    /**
     * 处理报告生成请求
     */
    async handleReportGeneration(params, context) {
        return {
            type: 'text',
            content: '报告生成功能开发中...\n\n未来将支持：\n- PDF 格式报告\n- Word 文档\n- Excel 数据表\n- PowerPoint 演示',
        };
    }
    /**
     * 处理通用查询
     */
    async handleGeneralQuery(message, context) {
        const response = await context.llm.chat({
            system: `你是一位专业的尽职调查分析师，拥有丰富的投资和并购经验。

你的职责包括：
- 分析目标公司的基本情况
- 评估财务健康状况
- 识别法律和合规风险
- 分析商业模式和市场地位
- 评估管理团队
- 提供风险评估和投资建议

请以专业、客观、严谨的方式回答用户的问题。

可用功能：
- "分析公司：[公司名]" - 分析公司基本信息
- "快速尽调：[公司名]" - 执行快速尽职调查
- "完整尽调：[公司名]" - 执行全面尽职调查（开发中）

请始终提醒用户：尽调结果仅供参考，不构成专业投资建议，关键信息需自行核实。`,
            messages: [
                {
                    role: 'user',
                    content: message,
                },
            ],
        });
        return {
            type: 'text',
            content: response.content,
        };
    }
}
// 导出默认实例
export default new DueDiligenceAnalyst();
export * from './types/index.js';
//# sourceMappingURL=index.js.map