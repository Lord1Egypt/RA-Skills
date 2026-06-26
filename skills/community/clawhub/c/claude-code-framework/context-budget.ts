/**
 * Context Budget Manager - 上下文预算管理器
 * 
 * 参考 Claude Code 的四级压缩策略
 */

import { ContextBudget } from './handler';

export interface BudgetConfig {
  warningThreshold: number;  // 默认 0.80
  criticalThreshold: number;  // 默认 0.90
  blockThreshold: number;    // 默认 0.98
  defaultLimit: number;      // 默认 200000 tokens
}

export class ContextBudgetManager {
  private config: BudgetConfig;
  private currentUsage: {
    system: number;
    userContext: number;
    messages: number;
    output: number;
  };
  
  constructor(config?: Partial<BudgetConfig>) {
    this.config = {
      warningThreshold: config?.warningThreshold ?? 0.80,
      criticalThreshold: config?.criticalThreshold ?? 0.90,
      blockThreshold: config?.blockThreshold ?? 0.98,
      defaultLimit: config?.defaultLimit ?? 200000
    };
    
    this.currentUsage = {
      system: 8000,      // 示例值
      userContext: 4000, // 示例值
      messages: 0,       // 动态计算
      output: 20000      // 预留
    };
  }
  
  /**
   * 获取当前预算状态
   */
  getCurrent(): ContextBudget {
    const total = this.calculateTotal();
    const percentage = total / this.config.defaultLimit;
    
    let status: ContextBudget['status'];
    if (percentage >= this.config.blockThreshold) {
      status = 'BLOCKED';
    } else if (percentage >= this.config.criticalThreshold) {
      status = 'CRITICAL';
    } else if (percentage >= this.config.warningThreshold) {
      status = 'WARNING';
    } else {
      status = 'NORMAL';
    }
    
    return {
      percentage: Math.round(percentage * 100) / 100,
      used: total,
      limit: this.config.defaultLimit,
      status
    };
  }
  
  /**
   * 更新使用量
   */
  update(usage: Partial<typeof this.currentUsage>): void {
    Object.assign(this.currentUsage, usage);
  }
  
  /**
   * 检查是否需要压缩
   */
  needsCompaction(): { needed: boolean; level: string; reason: string } {
    const budget = this.getCurrent();
    
    if (budget.percentage >= this.config.blockThreshold) {
      return {
        needed: true,
        level: 'BLOCK',
        reason: 'Context exceeded block threshold'
      };
    }
    
    if (budget.percentage >= this.config.criticalThreshold) {
      return {
        needed: true,
        level: 'session-compact',
        reason: 'Context at critical level (90%+)'
      };
    }
    
    if (budget.percentage >= this.config.warningThreshold) {
      return {
        needed: true,
        level: 'micro-compact',
        reason: 'Context at warning level (80%+)'
      };
    }
    
    return { needed: false, level: 'none', reason: 'Context healthy' };
  }
  
  /**
   * 触发压缩（返回建议的压缩操作）
   */
  suggestCompaction(): { action: string; estimatedSavings: number } {
    const budget = this.getCurrent();
    
    if (budget.percentage >= this.config.blockThreshold) {
      return {
        action: 'FORCE_COMPACT',
        estimatedSavings: Math.floor(this.currentUsage.messages * 0.5)
      };
    }
    
    if (budget.percentage >= this.config.criticalThreshold) {
      return {
        action: 'SESSION_COMPACT',
        estimatedSavings: Math.floor(this.currentUsage.messages * 0.4)
      };
    }
    
    if (budget.percentage >= this.config.warningThreshold) {
      return {
        action: 'MICRO_COMPACT',
        estimatedSavings: Math.floor(this.currentUsage.messages * 0.2)
      };
    }
    
    return { action: 'NONE', estimatedSavings: 0 };
  }
  
  /**
   * 获取紧凑的进度条字符串
   */
  getProgressBar(length: number = 40): string {
    const budget = this.getCurrent();
    const filled = Math.floor(budget.percentage * length);
    const empty = length - filled;
    
    const statusIcon = {
      NORMAL: '✅',
      WARNING: '⚠️',
      CRITICAL: '🔥',
      BLOCKED: '🚫'
    }[budget.status];
    
    return `${statusIcon} [${'█'.repeat(filled)}${'░'.repeat(empty)}] ${Math.round(budget.percentage * 100)}%`;
  }
  
  /**
   * 获取详细分解
   */
  getBreakdown(): {
    system: { value: number; percentage: number };
    userContext: { value: number; percentage: number };
    messages: { value: number; percentage: number };
    output: { value: number; percentage: number };
    total: { value: number; percentage: number };
  } {
    const total = this.calculateTotal();
    
    const calc = (value: number) => ({
      value,
      percentage: Math.round(value / this.config.defaultLimit * 100)
    });
    
    return {
      system: calc(this.currentUsage.system),
      userContext: calc(this.currentUsage.userContext),
      messages: calc(this.currentUsage.messages),
      output: calc(this.currentUsage.output),
      total: calc(total)
    };
  }
  
  /**
   * 模拟压缩操作
   */
  simulateCompaction(level: 'micro' | 'auto' | 'session'): number {
    const savings = {
      micro: Math.floor(this.currentUsage.messages * 0.2),
      auto: Math.floor(this.currentUsage.messages * 0.4),
      session: Math.floor(this.currentUsage.messages * 0.6)
    }[level];
    
    return savings;
  }
  
  private calculateTotal(): number {
    return Object.values(this.currentUsage).reduce((a, b) => a + b, 0);
  }
  
  /**
   * 更新配置
   */
  updateConfig(config: Partial<BudgetConfig>): void {
    Object.assign(this.config, config);
  }
}
