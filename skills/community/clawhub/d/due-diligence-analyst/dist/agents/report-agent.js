/**
 * Report Agent
 * 负责尽调报告生成
 */
export class ReportAgent {
    context;
    async initialize(context) {
        this.context = context;
        console.log('[Report Agent] Initialized');
    }
    /**
     * 生成快速尽调报告
     */
    async generateQuickReport(companyName, context) {
        console.log(`[Report Agent] Generating quick DD report for: ${companyName}`);
        try {
            const response = await context.llm.chat({
                system: `你是一位专业的尽职调查报告撰写专家。请为目标公司生成一份快速尽调报告。

报告结构：

# 【公司名称】快速尽调报告

## 执行摘要
- 总体评级：A/B/C/D/F
- 基本结论：可投资/需谨慎/建议pass
- 关键发现（优势、风险、重大问题）

## 1. 公司概况
- 基本信息
- 股权结构
- 关联方

## 2. 快速风险评估
- 财务风险
- 法律风险
- 经营风险
- 其他风险

## 3. 关键指标
- 业务指标
- 财务指标（如有数据）

## 4. 后续建议
- 需要深入调查的方面
- 需要关注的风险点

---
**报告性质**：快速尽调，仅供初步决策参考

输出格式：使用清晰的 Markdown 格式，包含表格、列表和评级标记。`,
                messages: [
                    {
                        role: 'user',
                        content: `请为以下公司生成快速尽调报告：${companyName}`,
                    },
                ],
            });
            // 添加元信息
            const metadata = `\n\n---\n\n` +
                `**报告信息**\n` +
                `- 报告类型：快速尽调\n` +
                `- 生成时间：${new Date().toISOString()}\n` +
                `- 分析工具：Due Diligence Analyst v0.1.0\n` +
                `- 数据来源：公开信息 + AI 分析\n\n` +
                `**⚠️ 重要提示**\n` +
                `- 本报告基于有限信息的快速分析，仅供参考\n` +
                `- 关键决策前请进行完整尽职调查\n` +
                `- 建议核实所有关键数据和结论\n` +
                `- 本报告不构成专业投资建议`;
            return {
                type: 'text',
                content: response.content + metadata,
            };
        }
        catch (error) {
            console.error('[Report Agent] Error:', error);
            return {
                type: 'error',
                content: `生成报告时出错: ${error instanceof Error ? error.message : '未知错误'}`,
            };
        }
    }
    /**
     * 生成完整尽调报告（开发中）
     */
    async generateFullReport(companyName, context) {
        return {
            type: 'text',
            content: '完整尽调报告功能开发中...',
        };
    }
    /**
     * 生成专项报告（开发中）
     */
    async generateSpecializedReport(companyName, reportType, context) {
        return {
            type: 'text',
            content: `${reportType} 专项报告功能开发中...`,
        };
    }
    /**
     * 格式化报告为 Markdown
     */
    formatMarkdown(report) {
        const md = `# ${report.companyName} 尽职调查报告

**报告编号**: ${report.reportId}
**报告日期**: ${report.reportDate}
**报告类型**: ${report.reportType}

---

## 执行摘要

**总体评级**: ${report.executiveSummary.rating}
**投资建议**: ${report.executiveSummary.recommendation}

### 结论
${report.executiveSummary.conclusion}

### 关键发现

**✅ 优势**:
${report.executiveSummary.keyFindings.strengths.map(s => `- ${s}`).join('\n')}

**⚠️ 关注点**:
${report.executiveSummary.keyFindings.concerns.map(c => `- ${c}`).join('\n')}

${report.executiveSummary.keyFindings.criticalIssues.length > 0 ? `
**🔴 重大问题**:
${report.executiveSummary.keyFindings.criticalIssues.map(i => `- ${i}`).join('\n')}
` : ''}

### 后续建议
${report.executiveSummary.nextSteps.map((s, i) => `${i + 1}. ${s}`).join('\n')}

---

## 详细分析

... (详细章节)

---

**报告元信息**
- 分析师: ${report.metadata.analyst}
- 版本: ${report.metadata.version}
- 机密级别: ${report.metadata.confidential ? '机密' : '非机密'}
`;
        return md;
    }
    /**
     * 导出为 PDF（占位实现）
     */
    async exportToPDF(report) {
        // TODO: 实现 PDF 导出
        throw new Error('PDF export not implemented yet');
    }
    /**
     * 导出为 Word（占位实现）
     */
    async exportToWord(report) {
        // TODO: 实现 Word 导出
        throw new Error('Word export not implemented yet');
    }
}
//# sourceMappingURL=report-agent.js.map