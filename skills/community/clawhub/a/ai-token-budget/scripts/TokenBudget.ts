// ============================================================
// TokenBudget — 每个 Agent 的智能油耗表
// v0.1 — 2026-05-21
//
// 用法:
//   const budget = new TokenBudget({ dailyLimit: 100000 })
//   const ok = budget.canSpend({ type: 'deep_reasoning', estimatedTokens: 8000, priority: 'high' })
//   const model = budget.selectModel(task.type)
//   // ... 调LLM ...
//   budget.recordSpend('分析提问', 8000, model)
// ============================================================

interface BudgetConfig {
  dailyLimit: number
  monthlyLimit: number
  perTaskLimit: number
  autoDowngrade: boolean
  alertThreshold: number          // 剩余比例预警（0.1 = 剩余10%时预警）
  preferredTier: 'PREMIUM' | 'STANDARD' | 'CHEAP'
}

interface TaskRequest {
  type: string
  estimatedTokens: number
  priority: 'high' | 'medium' | 'low'
}

interface SpendLog {
  timestamp: string
  task: string
  tokens: number
  model: string
}

interface BudgetStats {
  usedToday: number
  usedThisMonth: number
  dailyRemaining: number
  dailyPercent: string
  todayCost: number
  monthlyCost: number
  log: SpendLog[]
}

// 模型等级 & 单价（元/百万token）
const MODEL_TIERS: Record<string, { name: string; costPerMillion: number; suitableFor: string[] }> = {
  PREMIUM: {
    name: 'DeepSeek V4 Reasoning',
    costPerMillion: 8,
    suitableFor: ['deep_reasoning', 'analysis', 'coding', 'zhuge', 'fate']
  },
  STANDARD: {
    name: 'DeepSeek V4 Fast',
    costPerMillion: 2,
    suitableFor: ['drafting', 'summarize', 'translate', 'general', 'chat']
  },
  CHEAP: {
    name: 'DeepSeek V3 Lite / 小艺免费',
    costPerMillion: 0,
    suitableFor: ['greeting', 'simple_qa', 'formatting', 'echo', 'echo_task']
  }
}

const CHEAP_TASK_TYPES = new Set(MODEL_TIERS.CHEAP.suitableFor)

class TokenBudget {
  private config: BudgetConfig
  private usedToday: number = 0
  private usedThisMonth: number = 0
  private log: SpendLog[] = []

  constructor(config?: Partial<BudgetConfig>) {
    this.config = {
      dailyLimit: 100000,
      monthlyLimit: 3000000,
      perTaskLimit: 50000,
      autoDowngrade: true,
      alertThreshold: 0.1,
      preferredTier: 'STANDARD',
      ...config
    }
  }

  // ============================================================
  // 核心方法：Agent 调 LLM 前必须调这个
  // ============================================================

  canSpend(task: TaskRequest): { allow: boolean; suggestion?: string; model?: string } {
    // 1. 单次任务超额检查
    if (task.estimatedTokens > this.config.perTaskLimit) {
      return {
        allow: false,
        suggestion: `单次任务估算 ${task.estimatedTokens} token 超过单次限额 ${this.config.perTaskLimit}，建议拆分`
      }
    }

    // 2. 每日限额检查
    const projected = this.usedToday + task.estimatedTokens
    if (projected > this.config.dailyLimit) {
      if (this.config.autoDowngrade && CHEAP_TASK_TYPES.has(task.type)) {
        // 自动降级到免费模型
        return {
          allow: true,
          suggestion: '日预算将超限，自动降级到免费模型',
          model: MODEL_TIERS.CHEAP.name
        }
      }
      if (this.config.autoDowngrade && task.priority === 'low') {
        return {
          allow: false,
          suggestion: `日预算不足（今日已用 ${this.usedToday}/${this.config.dailyLimit}），低优先级任务已跳过`
        }
      }
      return {
        allow: false,
        suggestion: `日预算不足（今日已用 ${this.usedToday}/${this.config.dailyLimit}），请充值或调整配置`
      }
    }

    return { allow: true }
  }

  // ============================================================
  // 智能选模型：预算充足 → 高精度，紧张 → 低成本
  // ============================================================

  selectModel(taskType: string): string {
    const remaining = this.config.dailyLimit - this.usedToday
    const remainingRatio = this.config.dailyLimit > 0 ? remaining / this.config.dailyLimit : 0

    // 预算充裕（剩余 > 30%）→ 用默认等级
    if (remainingRatio > 0.3) {
      return MODEL_TIERS[this.config.preferredTier].name
    }

    // 预算紧张（剩余 10-30%）→ 中等任务降级
    if (remainingRatio > this.config.alertThreshold) {
      return MODEL_TIERS.STANDARD.name
    }

    // 预算预警（剩余 < 10%）→ 除非是支持的高优任务类型，否则全走免费
    if (CHEAP_TASK_TYPES.has(taskType)) {
      return MODEL_TIERS.CHEAP.name
    }
    // 非免费类型 → 至少给STANDARD
    return MODEL_TIERS.STANDARD.name
  }

  // ============================================================
  // 记账
  // ============================================================

  recordSpend(task: string, tokens: number, model: string): void {
    this.usedToday += tokens
    this.usedThisMonth += tokens
    this.log.push({
      timestamp: new Date().toISOString(),
      task,
      tokens,
      model
    })
  }

  // ============================================================
  // 统计
  // ============================================================

  getStats(): BudgetStats {
    return {
      usedToday: this.usedToday,
      usedThisMonth: this.usedThisMonth,
      dailyRemaining: Math.max(0, this.config.dailyLimit - this.usedToday),
      dailyPercent: this.config.dailyLimit > 0
        ? Math.round((this.usedToday / this.config.dailyLimit) * 100) + '%'
        : '0%',
      todayCost: this.calculateCost(this.usedToday),
      monthlyCost: this.calculateCost(this.usedThisMonth),
      log: this.log.slice(-50)
    }
  }

  resetDaily(): void {
    this.usedToday = 0
  }

  reset(): void {
    this.usedToday = 0
    this.usedThisMonth = 0
    this.log = []
  }

  private calculateCost(tokens: number): number {
    // 按混合模型估算，约 2 元/百万token（STANDARD 为主）
    return Math.round((tokens / 1000000) * 2 * 100) / 100
  }
}

// ============================================================
// 导出
// ============================================================

export { TokenBudget, BudgetConfig, TaskRequest, BudgetStats, MODEL_TIERS }
export default TokenBudget
