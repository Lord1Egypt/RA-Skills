/**
 * 成本优化器
 * 
 * 层级：Layer 10 - Efficiency Layer
 * 功能：视频生成成本优化、预算控制、资源调度优化
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

// ============== 类型定义 ==============

/**
 * 成本明细
 */
export interface CostBreakdown {
  /** 基础成本 */
  baseCost: number;
  /** 分辨率加成 */
  resolutionMultiplier: number;
  /** 时长加成 */
  durationMultiplier: number;
  /** 音频加成 */
  audioMultiplier: number;
  /** 总成本 */
  totalCost: number;
}

/**
 * 预算配置
 */
export interface BudgetConfig {
  /** 每日预算 */
  dailyBudget: number;
  /** 每请求预算上限 */
  maxCostPerRequest: number;
  /** 预算警告阈值 (80%) */
  warningThreshold: number;
  /** 预算阻止阈值 (100%) */
  blockThreshold: number;
  /** 预算重置时间 */
  budgetResetHour: number;
}

/**
 * 成本优化策略
 */
export type CostOptimizationStrategy =
  | 'quality_priority' // 质量优先
  | 'cost_priority' // 成本优先
  | 'balanced'; // 平衡模式

/**
 * 优化建议
 */
export interface OptimizationSuggestion {
  /** 建议类型 */
  type: 'resolution_downgrade' | 'duration_reduction' | 'batch_processing' | 'off_peak';
  /** 建议描述 */
  description: string;
  /** 预计节省 */
  estimatedSavings: number;
  /** 影响评估 */
  impact: 'none' | 'low' | 'medium' | 'high';
}

/**
 * 使用统计
 */
export interface UsageStats {
  /** 今日已用预算 */
  spentToday: number;
  /** 今日剩余预算 */
  remainingToday: number;
  /** 今日请求数 */
  requestsToday: number;
  /** 平均单次成本 */
  avgCostPerRequest: number;
  /** 预算使用率 */
  budgetUtilization: number;
}

// ============== 默认配置 ==============

const DEFAULT_BUDGET_CONFIG: BudgetConfig = {
  dailyBudget: 100, // $100/天
  maxCostPerRequest: 0.1, // $0.1/请求
  warningThreshold: 0.8,
  blockThreshold: 1.0,
  budgetResetHour: 0, // 午夜重置
};

const RESOLUTION_COSTS: Record<string, number> = {
  '480P': 1.0,
  '720P': 1.5,
  '1080P': 2.0,
};

const BASE_COST = 0.02; // $0.02 基础成本

// ============== 核心类 ==============

/**
 * 成本优化器
 */
export class CostOptimizer {
  private budgetConfig: BudgetConfig;
  private spentToday: number = 0;
  private requestsToday: number = 0;
  private lastResetDate: string = new Date().toDateString();

  constructor(budgetConfig: Partial<BudgetConfig> = {}) {
    this.budgetConfig = { ...DEFAULT_BUDGET_CONFIG, ...budgetConfig };
  }

  /**
   * 计算成本明细
   */
  calculateCost(
    durationSeconds: number = 5,
    resolution: '480P' | '720P' | '1080P' = '1080P',
    hasAudio: boolean = false
  ): CostBreakdown {
    const baseCost = BASE_COST;
    const resolutionMultiplier = RESOLUTION_COSTS[resolution] || 1.0;
    const durationMultiplier = durationSeconds / 5; // 基准 5 秒
    const audioMultiplier = hasAudio ? 1.3 : 1.0;

    const totalCost =
      baseCost * resolutionMultiplier * durationMultiplier * audioMultiplier;

    return {
      baseCost,
      resolutionMultiplier,
      durationMultiplier,
      audioMultiplier,
      totalCost: Math.round(totalCost * 1000) / 1000,
    };
  }

  /**
   * 检查预算
   */
  checkBudget(estimatedCost: number): {
    allowed: boolean;
    reason?: string;
    remainingBudget?: number;
  } {
    // 检查日期是否需要重置
    this.checkDateReset();

    // 检查单请求预算
    if (estimatedCost > this.budgetConfig.maxCostPerRequest) {
      return {
        allowed: false,
        reason: `Cost $${estimatedCost.toFixed(3)} exceeds max $${this.budgetConfig.maxCostPerRequest}`,
      };
    }

    // 检查每日预算
    const utilization = this.spentToday / this.budgetConfig.dailyBudget;

    if (utilization >= this.budgetConfig.blockThreshold) {
      return {
        allowed: false,
        reason: `Daily budget exhausted ($${this.spentToday.toFixed(2)} / $${this.budgetConfig.dailyBudget})`,
      };
    }

    if (utilization >= this.budgetConfig.warningThreshold) {
      console.warn(
        `[Cost Optimizer] ⚠️ Budget warning: ${Math.round(utilization * 100)}% used`
      );
    }

    return {
      allowed: true,
      remainingBudget: this.budgetConfig.dailyBudget - this.spentToday,
    };
  }

  /**
   * 记录支出
   */
  recordExpense(cost: number): void {
    this.checkDateReset();
    this.spentToday += cost;
    this.requestsToday++;
  }

  /**
   * 获取使用统计
   */
  getUsageStats(): UsageStats {
    this.checkDateReset();

    return {
      spentToday: Math.round(this.spentToday * 100) / 100,
      remainingToday: Math.round((this.budgetConfig.dailyBudget - this.spentToday) * 100) / 100,
      requestsToday: this.requestsToday,
      avgCostPerRequest:
        this.requestsToday > 0
          ? Math.round((this.spentToday / this.requestsToday) * 1000) / 1000
          : 0,
      budgetUtilization: Math.round((this.spentToday / this.budgetConfig.dailyBudget) * 100) / 100,
    };
  }

  /**
   * 获取优化建议
   */
  getSuggestions(
    currentResolution: string,
    currentDuration: number
  ): OptimizationSuggestion[] {
    const suggestions: OptimizationSuggestion[] = [];

    // 分辨率降级建议
    if (currentResolution === '1080P') {
      const savings = this.calculateCost(currentDuration, '1080P').totalCost -
        this.calculateCost(currentDuration, '720P').totalCost;
      suggestions.push({
        type: 'resolution_downgrade',
        description: '从 1080P 降级到 720P 可节省成本',
        estimatedSavings: Math.round(savings * 100) / 100,
        impact: 'medium',
      });
    }

    // 时长缩减建议
    if (currentDuration > 10) {
      const savings = this.calculateCost(currentDuration, currentResolution as any).totalCost -
        this.calculateCost(10, currentResolution as any).totalCost;
      suggestions.push({
        type: 'duration_reduction',
        description: `时长从${currentDuration}秒缩减到 10 秒`,
        estimatedSavings: Math.round(savings * 100) / 100,
        impact: 'high',
      });
    }

    // 批处理建议
    if (this.requestsToday > 50) {
      suggestions.push({
        type: 'batch_processing',
        description: '启用批处理可提升 30% 效率',
        estimatedSavings: Math.round(this.spentToday * 0.3 * 100) / 100,
        impact: 'medium',
      });
    }

    // 非高峰时段建议
    const hour = new Date().getHours();
    if (hour >= 9 && hour <= 18) {
      suggestions.push({
        type: 'off_peak',
        description: '非高峰时段 (9:00-18:00) 可能有更低成本',
        estimatedSavings: 0, // 仅为建议，无实际节省
        impact: 'low',
      });
    }

    return suggestions.sort((a, b) => b.estimatedSavings - a.estimatedSavings);
  }

  /**
   * 根据策略优化请求
   */
  optimizeRequest(
    request: any,
    strategy: CostOptimizationStrategy
  ): { optimized: any; savings: number } {
    let optimized = { ...request };
    let savings = 0;

    if (strategy === 'cost_priority') {
      // 成本优先：降级分辨率，缩短时长
      if (optimized.resolution === '1080P') {
        optimized.resolution = '720P';
        savings += this.calculateCost(optimized.durationSeconds || 5, '1080P').totalCost -
          this.calculateCost(optimized.durationSeconds || 5, '720P').totalCost;
      }
      if (optimized.durationSeconds > 10) {
        optimized.durationSeconds = 10;
      }
    } else if (strategy === 'balanced') {
      // 平衡模式：适度优化
      if (optimized.durationSeconds > 15) {
        optimized.durationSeconds = 15;
      }
    }
    // quality_priority: 不做优化

    return {
      optimized,
      savings: Math.round(savings * 100) / 100,
    };
  }

  /**
   * 重置预算 (日期变更时)
   */
  private checkDateReset(): void {
    const today = new Date().toDateString();
    if (today !== this.lastResetDate) {
      this.spentToday = 0;
      this.requestsToday = 0;
      this.lastResetDate = today;
      console.log('[Cost Optimizer] 📅 Daily budget reset');
    }
  }

  /**
   * 手动重置预算
   */
  resetBudget(): void {
    this.spentToday = 0;
    this.requestsToday = 0;
    console.log('[Cost Optimizer] 🔄 Budget manually reset');
  }
}

// ============== 导出 ==============

export default CostOptimizer;
