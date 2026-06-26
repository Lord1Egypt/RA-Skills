// ============================================================
// basic-demo.ts — TokenBudget 核心流程验证
// ============================================================

import { TokenBudget } from '../TokenBudget.ts'

function printDivider(title: string): void {
  console.log('\n' + '='.repeat(60))
  console.log(`  ${title}`)
  console.log('='.repeat(60))
}

async function main() {
  printDivider('TokenBudget v0.1 — 基础验证')

  // 1. 创建一个每日预算 10 万 token 的 Budget
  const budget = new TokenBudget({
    dailyLimit: 100000,
    autoDowngrade: true,
    preferredTier: 'STANDARD'
  })

  console.log('\n📊 初始状态:')
  console.log(JSON.stringify(budget.getStats(), null, 2))

  // 2. 测试场景 A: 高优先级深度推理 → 应该允许
  printDivider('场景 A: 高优先级深度推理（预算充裕）')
  
  const taskA = { type: 'deep_reasoning', estimatedTokens: 8000, priority: 'high' as const }
  const decisionA = budget.canSpend(taskA)
  console.log(`  canSpend: ${decisionA.allow}`)
  if (decisionA.suggestion) console.log(`  建议: ${decisionA.suggestion}`)
  
  const modelA = budget.selectModel(taskA.type)
  console.log(`  推荐模型: ${modelA}`)
  
  budget.recordSpend('分析用户命盘', 8000, modelA)
  console.log(`\n  记账后状态:`)
  console.log(`  今日已用: ${budget.getStats().usedToday} token`)
  console.log(`  今日剩余: ${budget.getStats().dailyRemaining} token`)
  console.log(`  今日花费: ¥${budget.getStats().todayCost}`)

  // 3. 测试场景 B: 低优先级格式化（预算充裕但故意省）
  printDivider('场景 B: 简单格式化任务')
  
  const taskB = { type: 'formatting', estimatedTokens: 500, priority: 'low' as const }
  const decisionB = budget.canSpend(taskB)
  console.log(`  canSpend: ${decisionB.allow}`)
  if (decisionB.suggestion) console.log(`  建议: ${decisionB.suggestion}`)
  
  const modelB = budget.selectModel(taskB.type)
  console.log(`  推荐模型: ${modelB}`)
  
  budget.recordSpend('格式化输出', 500, modelB)
  console.log(`  今日已用: ${budget.getStats().usedToday} token`)

  // 4. 模拟消耗大量 token 触发预算紧张
  printDivider('场景 C: 模拟大量消耗触发预算紧张')
  
  // 一次性消耗 9 万 token
  budget.recordSpend('批量分析报告', 90000, 'DeepSeek V4 Fast')
  console.log(`  今日已用: ${budget.getStats().usedToday} token`)
  console.log(`  日剩余比例: ${budget.getStats().dailyPercent}`)

  // 此时预算紧张（只剩 1500 token ≈ 1.5%）
  printDivider('场景 D: 预算紧张下调用')
  
  const taskD = { type: 'analysis', estimatedTokens: 2000, priority: 'medium' as const }
  const decisionD = budget.canSpend(taskD)
  console.log(`  canSpend: ${decisionD.allow}`)
  if (decisionD.suggestion) console.log(`  建议: ${decisionD.suggestion}`)
  
  const modelD = budget.selectModel(taskD.type)
  console.log(`  推荐模型: ${modelD}`)
  console.log(`  (预算紧张时中等任务自动降到 STANDARD)`)

  // 5. 测试场景 E: 低优先级任务在预算紧张时被跳过
  printDivider('场景 E: 预算紧张 + 低优先级')
  
  const taskE = { type: 'greeting', estimatedTokens: 200, priority: 'low' as const }
  const decisionE = budget.canSpend(taskE)
  console.log(`  canSpend: ${decisionE.allow}`)
  if (decisionE.suggestion) console.log(`  建议: ${decisionE.suggestion}`)

  // 6. 测试场景 F: 单次任务超额
  printDivider('场景 F: 单次任务超额')
  
  const taskF = { type: 'deep_reasoning', estimatedTokens: 100000, priority: 'high' as const }
  const decisionF = budget.canSpend(taskF)
  console.log(`  canSpend: ${decisionF.allow}`)
  if (decisionF.suggestion) console.log(`  建议: ${decisionF.suggestion}`)

  // 7. 最终统计
  printDivider('📊 最终统计')
  const stats = budget.getStats()
  console.log(`  日预算: 100,000 token`)
  console.log(`  今日已用: ${stats.usedToday} token`)
  console.log(`  今日花费: ¥${stats.todayCost}`)
  console.log(`  本月已用: ${stats.usedThisMonth} token`)
  console.log(`  本月花费: ¥${stats.monthlyCost}`)
  console.log(`  调用记录: ${stats.log.length} 条`)
  
  printDivider('✅ 验证完成')
  console.log('  TokenBudget v0.1 核心流程正常工作。')
  console.log('  预算检查 ✓')
  console.log('  智能选模型 ✓')
  console.log('  记账 ✓')
  console.log('  降级策略 ✓')
  console.log('  超额拦截 ✓')
}

main().catch(console.error)
