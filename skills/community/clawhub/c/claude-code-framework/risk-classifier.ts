/**
 * Risk Classifier - 风险分类器
 * 
 * 从 Claude Code BASH 分类器提取的通用风险评估逻辑
 */

import { RiskLevel, ToolRiskAssessment } from './handler';
import { BUILTIN_RULES } from './handler';

export class riskClassifier {
  private rules: {
    auto: RegExp[];
    approve: RegExp[];
    block: RegExp[];
  };
  
  constructor(customRules?: {
    auto?: string[];
    approve?: string[];
    block?: string[];
  }) {
    // 编译正则表达式
    this.rules = {
      auto: (customRules?.auto ?? BUILTIN_RULES.auto).map(p => this.patternToRegex(p)),
      approve: (customRules?.approve ?? BUILTIN_RULES.approve).map(p => this.patternToRegex(p)),
      block: (customRules?.block ?? BUILTIN_RULES.block).map(p => this.patternToRegex(p))
    };
  }
  
  /**
   * 评估工具调用的风险等级
   */
  classify(tool: string, args: Record<string, any>): ToolRiskAssessment {
    const toolStr = tool.toLowerCase();
    const argsStr = JSON.stringify(args).toLowerCase();
    
    // 1. 检查 BLOCK 规则（最高优先级）
    for (const pattern of this.rules.block) {
      if (pattern.test(toolStr) || pattern.test(argsStr)) {
        return {
          tool,
          args,
          risk: RiskLevel.BLOCK,
          reason: `Matches blocked pattern: ${pattern}`,
          suggestion: 'This operation is not allowed for security reasons.'
        };
      }
    }
    
    // 2. 检查 APPROVE 规则
    for (const pattern of this.rules.approve) {
      if (pattern.test(toolStr) || pattern.test(argsStr)) {
        return {
          tool,
          args,
          risk: RiskLevel.APPROVE,
          reason: `Matches approval-required pattern: ${pattern}`,
          suggestion: 'This operation requires explicit approval.'
        };
      }
    }
    
    // 3. 检查 AUTO 规则
    for (const pattern of this.rules.auto) {
      if (pattern.test(toolStr)) {
        return {
          tool,
          args,
          risk: RiskLevel.AUTO,
          reason: `Matches auto-allow pattern: ${pattern}`
        };
      }
    }
    
    // 4. 默认：需要审批（保守策略）
    return {
      tool,
      args,
      risk: RiskLevel.APPROVE,
      reason: 'No matching rule found, defaulting to approval required',
      suggestion: 'Configure explicit rules for this tool if you want to change behavior.'
    };
  }
  
  /**
   * 批量分类
   */
  classifyMany(calls: { tool: string; args: Record<string, any> }[]): ToolRiskAssessment[] {
    return calls.map(call => this.classify(call.tool, call.args));
  }
  
  /**
   * 检查是否有任何高风险调用
   */
  hasHighRiskCalls(calls: { tool: string; args: Record<string, any> }[]): boolean {
    return calls.some(call => {
      const assessment = this.classify(call.tool, call.args);
      return assessment.risk === RiskLevel.BLOCK || assessment.risk === RiskLevel.APPROVE;
    });
  }
  
  /**
   * 将 glob 模式转换为正则表达式
   */
  private patternToRegex(pattern: string): RegExp {
    // 精确匹配
    if (!pattern.includes('*') && !pattern.includes('.')) {
      return new RegExp(`^${pattern}$`, 'i');
    }
    
    // 简单 glob
    const escaped = pattern
      .replace(/[.+^${}()|[\]\\]/g, '\\$&')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');
    
    return new RegExp(escaped, 'i');
  }
  
  /**
   * 添加自定义规则
   */
  addRule(risk: 'auto' | 'approve' | 'block', pattern: string): void {
    const regex = this.patternToRegex(pattern);
    this.rules[risk].push(regex);
  }
  
  /**
   * 获取当前规则列表
   */
  listRules(): { auto: string[]; approve: string[]; block: string[] } {
    return {
      auto: this.rules.auto.map(r => r.source),
      approve: this.rules.approve.map(r => r.source),
      block: this.rules.block.map(r => r.source)
    };
  }
}
