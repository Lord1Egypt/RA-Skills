/**
 * 审查报告生成器
 * 生成Markdown、HTML格式的代码审查报告
 */

export class ReportGenerator {
  /**
   * 生成审查报告
   */
  static async execute(args, context) {
    const { 
      reviewResults, 
      format = 'markdown',
      includeDetails = true,
      options = {} 
    } = args;
    
    console.log(`📄 生成${format.toUpperCase()}格式审查报告...`);
    
    try {
      // 验证输入
      if (!reviewResults) {
        throw new Error('需要提供reviewResults参数');
      }
      
      let report;
      
      // 根据格式生成报告
      switch (format.toLowerCase()) {
        case 'markdown':
          report = ReportGenerator.generateMarkdownReport(reviewResults, includeDetails, options);
          break;
          
        case 'html':
          report = ReportGenerator.generateHTMLReport(reviewResults, includeDetails, options);
          break;
          
        case 'json':
          report = ReportGenerator.generateJSONReport(reviewResults, includeDetails, options);
          break;
          
        default:
          throw new Error(`不支持的格式: ${format}，支持: markdown, html, json`);
      }
      
      console.log(`✅ 报告生成完成: ${report.summary?.fileName || '未命名'}`);
      
      return {
        success: true,
        report,
        metadata: {
          format,
          generatedAt: new Date().toISOString(),
          size: ReportGenerator.calculateReportSize(report),
          includes: {
            details: includeDetails,
            recommendations: options.includeRecommendations !== false,
            suggestions: options.includeSuggestions !== false
          }
        }
      };
      
    } catch (error) {
      console.error('❌ 报告生成失败:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'REPORT_GENERATION_ERROR'
        }
      };
    }
  }
  
  /**
   * 生成Markdown报告
   */
  static generateMarkdownReport(results, includeDetails = true, options = {}) {
    const timestamp = new Date().toISOString();
    const fileName = results.summary?.filePath || 'code-review-report.md';
    
    let markdown = `# 代码审查报告\n\n`;
    
    // 报告头部
    markdown += `## 📋 报告概览\n\n`;
    markdown += `- **文件**: ${results.summary?.filePath || '未指定'}\n`;
    markdown += `- **生成时间**: ${timestamp}\n`;
    markdown += `- **总体评分**: ${results.summary?.overallScore || 0}/100\n`;
    markdown += `- **等级**: ${results.summary?.grade || 'N/A'}\n`;
    markdown += `- **代码行数**: ${results.summary?.linesOfCode || 0}\n`;
    markdown += `- **问题总数**: ${ReportGenerator.countTotalIssues(results) || 0}\n\n`;
    
    // 评分摘要
    markdown += `## 📊 评分摘要\n\n`;
    
    if (results.analysis) {
      markdown += `### 代码质量\n`;
      markdown += `- 评分: ${results.analysis.quality?.score || 0}/100\n`;
      markdown += `- 问题: ${results.analysis.quality?.issues?.length || 0} 个\n\n`;
      
      if (results.analysis.security?.enabled !== false) {
        markdown += `### 安全性\n`;
        markdown += `- 评分: ${results.analysis.security?.score || 0}/100\n`;
        markdown += `- 问题: ${results.analysis.security?.issues?.length || 0} 个\n\n`;
      }
      
      if (results.analysis.performance?.enabled !== false) {
        markdown += `### 性能\n`;
        markdown += `- 评分: ${results.analysis.performance?.score || 0}/100\n`;
        markdown += `- 问题: ${results.analysis.performance?.issues?.length || 0} 个\n\n`;
      }
    }
    
    // 关键问题
    const criticalIssues = ReportGenerator.getCriticalIssues(results);
    if (criticalIssues.length > 0) {
      markdown += `## 🚨 关键问题 (需要立即修复)\n\n`;
      
      criticalIssues.forEach((issue, index) => {
        markdown += `### ${index + 1}. ${issue.message}\n`;
        markdown += `- **位置**: 第 ${issue.line} 行\n`;
        markdown += `- **严重程度**: ${issue.severity}\n`;
        markdown += `- **建议**: ${issue.suggestion || '参考最佳实践'}\n\n`;
        
        if (issue.codeSnippet) {
          markdown += `\`\`\`\n${issue.codeSnippet}\n\`\`\`\n\n`;
        }
      });
    }
    
    // AI建议
    if (results.recommendations?.ai?.length > 0 && options.includeRecommendations !== false) {
      markdown += `## 🧠 AI智能建议\n\n`;
      
      results.recommendations.ai.forEach((rec, index) => {
        markdown += `### ${index + 1}. ${rec.title}\n`;
        markdown += `- **优先级**: ${rec.priority}\n`;
        markdown += `- **描述**: ${rec.description}\n`;
        
        if (rec.suggestion) {
          markdown += `- **具体建议**: ${rec.suggestion}\n`;
        }
        
        if (rec.codeExample) {
          markdown += `\n**代码示例**:\n\n\`\`\`\n${rec.codeExample}\n\`\`\`\n`;
        }
        
        markdown += '\n';
      });
    }
    
    // 详细问题列表（可选）
    if (includeDetails) {
      markdown += `## 🔍 详细问题列表\n\n`;
      
      ['quality', 'security', 'performance'].forEach(category => {
        const categoryData = results.analysis?.[category];
        if (categoryData && categoryData.issues?.length > 0) {
          markdown += `### ${ReportGenerator.getCategoryName(category)}\n\n`;
          
          categoryData.issues.forEach((issue, idx) => {
            markdown += `${idx + 1}. **${issue.message}**\n`;
            markdown += `   - 行号: ${issue.line || 'N/A'}\n`;
            markdown += `   - 严重程度: ${issue.severity || 'info'}\n`;
            if (issue.suggestion) {
              markdown += `   - 建议: ${issue.suggestion}\n`;
            }
            markdown += '\n';
          });
        }
      });
    }
    
    // 改进建议
    markdown += `## 🛠️ 改进计划\n\n`;
    
    if (results.recommendations?.priority?.length > 0) {
      markdown += `### 优先级排序\n\n`;
      
      results.recommendations.priority.forEach((item, index) => {
        markdown += `${index + 1}. **${item.priority.toUpperCase()}**: ${item.message || '未指定'}\n`;
        if (item.suggestion) {
          markdown += `   - 建议: ${item.suggestion}\n`;
        }
        markdown += '\n';
      });
    }
    
    // 最佳实践
    markdown += `## 📚 最佳实践参考\n\n`;
    markdown += `1. **代码质量**: 遵循编码规范，保持代码简洁清晰\n`;
    markdown += `2. **安全性**: 验证所有输入，避免硬编码敏感信息\n`;
    markdown += `3. **性能**: 避免不必要的计算，优化关键路径\n`;
    markdown += `4. **可维护性**: 添加适当注释，保持函数单一职责\n`;
    markdown += `5. **可测试性**: 编写单元测试，确保代码质量\n\n`;
    
    // 报告脚注
    markdown += `---\n\n`;
    markdown += `*本报告由 AI Code Review Assistant 生成*\n`;
    markdown += `*生成工具: AstronClaw Skill - Code Review Assistant*\n`;
    markdown += `*报告版本: 1.0.0*\n`;
    
    return {
      content: markdown,
      format: 'markdown',
      fileName: fileName.endsWith('.md') ? fileName : `${fileName}.md`,
      size: markdown.length,
      sections: ReportGenerator.extractSections(markdown)
    };
  }
  
  /**
   * 生成HTML报告
   */
  static generateHTMLReport(results, includeDetails = true, options = {}) {
    const markdownReport = ReportGenerator.generateMarkdownReport(results, includeDetails, options);
    const markdown = markdownReport.content;
    
    // 简单的Markdown转HTML（实际实现应使用更完善的转换器）
    let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码审查报告 - ${results.summary?.filePath || '未命名'}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; color: #333; }
        h1, h2, h3, h4 { color: #2c3e50; margin-top: 1.5em; }
        h1 { border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { border-bottom: 1px solid #ddd; padding-bottom: 5px; }
        .critical { color: #e74c3c; font-weight: bold; }
        .warning { color: #f39c12; }
        .info { color: #3498db; }
        .success { color: #27ae60; }
        .score { font-size: 2em; font-weight: bold; margin: 10px 0; }
        .score-excellent { color: #27ae60; }
        .score-good { color: #2ecc71; }
        .score-average { color: #f39c12; }
        .score-poor { color: #e74c3c; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .code-block { background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; overflow-x: auto; }
        .summary-card { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .recommendation { background: #e8f4fc; border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; border-radius: 4px; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }
        @media print { body { max-width: none; } .no-print { display: none; } }
    </style>
</head>
<body>
    <h1>📋 代码审查报告</h1>
    
    <div class="summary-card">
        <h2>报告概览</h2>
        <p><strong>文件:</strong> ${results.summary?.filePath || '未指定'}</p>
        <p><strong>生成时间:</strong> ${new Date().toISOString()}</p>
        <p><strong>总体评分:</strong> 
            <span class="score ${ReportGenerator.getScoreClass(results.summary?.overallScore || 0)}">
                ${results.summary?.overallScore || 0}/100
            </span>
        </p>
        <p><strong>等级:</strong> ${results.summary?.grade || 'N/A'}</p>
        <p><strong>代码行数:</strong> ${results.summary?.linesOfCode || 0}</p>
        <p><strong>问题总数:</strong> ${ReportGenerator.countTotalIssues(results) || 0}</p>
    </div>
`;
    
    // 添加评分摘要表格
    html += `
    <h2>📊 评分摘要</h2>
    <table>
        <thead>
            <tr>
                <th>类别</th>
                <th>评分</th>
                <th>问题数</th>
                <th>状态</th>
            </tr>
        </thead>
        <tbody>`;
    
    if (results.analysis) {
      html += `
            <tr>
                <td><strong>代码质量</strong></td>
                <td>${results.analysis.quality?.score || 0}/100</td>
                <td>${results.analysis.quality?.issues?.length || 0}</td>
                <td class="${ReportGenerator.getStatusClass(results.analysis.quality?.score || 0)}">
                    ${ReportGenerator.getStatusText(results.analysis.quality?.score || 0)}
                </td>
            </tr>`;
      
      if (results.analysis.security?.enabled !== false) {
        html += `
            <tr>
                <td><strong>安全性</strong></td>
                <td>${results.analysis.security?.score || 0}/100</td>
                <td>${results.analysis.security?.issues?.length || 0}</td>
                <td class="${this.getStatusClass(results.analysis.security?.score || 0)}">
                    ${this.getStatusText(results.analysis.security?.score || 0)}
                </td>
            </tr>`;
      }
      
      if (results.analysis.performance?.enabled !== false) {
        html += `
            <tr>
                <td><strong>性能</strong></td>
                <td>${results.analysis.performance?.score || 0}/100</td>
                <td>${results.analysis.performance?.issues?.length || 0}</td>
                <td class="${this.getStatusClass(results.analysis.performance?.score || 0)}">
                    ${this.getStatusText(results.analysis.performance?.score || 0)}
                </td>
            </tr>`;
      }
    }
    
    html += `
        </tbody>
    </table>`;
    
    // 添加关键问题部分
    const criticalIssues = this.getCriticalIssues(results);
    if (criticalIssues.length > 0) {
      html += `
    <h2 class="critical">🚨 关键问题 (需要立即修复)</h2>`;
      
      criticalIssues.forEach((issue, index) => {
        html += `
    <div class="recommendation">
        <h3>${index + 1}. ${issue.message}</h3>
        <p><strong>位置:</strong> 第 ${issue.line} 行</p>
        <p><strong>严重程度:</strong> <span class="critical">${issue.severity}</span></p>
        <p><strong>建议:</strong> ${issue.suggestion || '参考最佳实践'}</p>`;
        
        if (issue.codeSnippet) {
          html += `
        <div class="code-block">
            <pre>${issue.codeSnippet}</pre>
        </div>`;
        }
        
        html += `
    </div>`;
      });
    }
    
    // 报告脚注
    html += `
    <div class="footer">
        <p>本报告由 <strong>AI Code Review Assistant</strong> 生成</p>
        <p>生成工具: AstronClaw Skill - Code Review Assistant v1.0.0</p>
        <p class="no-print">报告ID: ${Date.now().toString(36)}</p>
    </div>
</body>
</html>`;
    
    return {
      content: html,
      format: 'html',
      fileName: results.summary?.filePath ? 
        `${results.summary.filePath.replace(/\.[^/.]+$/, "")}-report.html` : 
        'code-review-report.html',
      size: html.length
    };
  }
  
  /**
   * 生成JSON报告
   */
  static generateJSONReport(results, includeDetails = true, options = {}) {
    const report = {
      metadata: {
        generator: 'AI Code Review Assistant',
        version: '1.0.0',
        generatedAt: new Date().toISOString(),
        format: 'json'
      },
      summary: results.summary || {},
      analysis: includeDetails ? results.analysis : undefined,
      recommendations: options.includeRecommendations !== false ? results.recommendations : undefined,
      statistics: {
        totalIssues: this.countTotalIssues(results),
        criticalIssues: this.getCriticalIssues(results).length,
        analysisTime: results.metadata?.analysisTime
      }
    };
    
    return {
      content: JSON.stringify(report, null, 2),
      format: 'json',
      fileName: results.summary?.filePath ? 
        `${results.summary.filePath.replace(/\.[^/.]+$/, "")}-report.json` : 
        'code-review-report.json',
      size: JSON.stringify(report).length
    };
  }
  
  /**
   * 统计总问题数
   */
  static countTotalIssues(results) {
    let total = 0;
    
    if (results.analysis) {
      ['quality', 'security', 'performance'].forEach(category => {
        if (results.analysis[category]?.issues) {
          total += results.analysis[category].issues.length;
        }
      });
    }
    
    return total;
  }
  
  /**
   * 获取关键问题
   */
  static getCriticalIssues(results) {
    const criticalIssues = [];
    
    if (results.analysis) {
      ['quality', 'security', 'performance'].forEach(category => {
        const issues = results.analysis[category]?.issues || [];
        issues.forEach(issue => {
          if (issue.severity === 'critical' || issue.severity === 'high') {
            criticalIssues.push({
              ...issue,
              category
            });
          }
        });
      });
    }
    
    return criticalIssues;
  }
  
  /**
   * 获取类别名称
   */
  static getCategoryName(category) {
    const names = {
      quality: '代码质量',
      security: '安全性',
      performance: '性能'
    };
    
    return names[category] || category;
  }
  
  /**
   * 提取章节
   */
  static extractSections(markdown) {
    const sections = [];
    const lines = markdown.split('\n');
    
    lines.forEach(line => {
      if (line.startsWith('## ')) {
        sections.push(line.replace('## ', '').trim());
      }
    });
    
    return sections;
  }
  
  /**
   * 计算报告大小
   */
  static calculateReportSize(report) {
    if (typeof report.content === 'string') {
      return report.content.length;
    }
    return 0;
  }
  
  /**
   * 获取评分CSS类
   */
  static getScoreClass(score) {
    if (score >= 90) return 'score-excellent';
    if (score >= 80) return 'score-good';
    if (score >= 70) return 'score-average';
    return 'score-poor';
  }
  
  /**
   * 获取状态CSS类
   */
  static getStatusClass(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'critical';
  }
  
  /**
   * 获取状态文本
   */
  static getStatusText(score) {
    if (score >= 90) return '优秀';
    if (score >= 80) return '良好';
    if (score >= 70) return '中等';
    if (score >= 60) return '及格';
    return '需要改进';
  }
}