#!/usr/bin/env node

/**
 * 反思引擎 - 从宏观角度分析学习进度和方向
 * 
 * 功能：
 * 1. 生成每日反思报告
 * 2. 生成每周反思报告
 * 3. 识别改进点
 * 4. 生成新学习方向
 * 
 * 用法：
 *   node reflection.js [command]
 *   
 * 命令：
 *   daily       - 生成每日反思报告
 *   weekly      - 生成每周反思报告
 *   both        - 生成每日 + 每周报告
 */

const fs = require('fs');
const path = require('path');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const QUEUE_PATH = path.join(WORKSPACE, 'tasks/queue.json');
const PATTERNS_PATH = path.join(WORKSPACE, 'instincts/patterns.jsonl');
const COMPLETED_PATH = path.join(WORKSPACE, 'tasks/completed.jsonl');
const REFLECTIONS_DIR = path.join(WORKSPACE, 'memory/reflections');

/**
 * 加载任务队列
 */
function loadQueue() {
  try {
    const data = fs.readFileSync(QUEUE_PATH, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return null;
  }
}

/**
 * 加载所有模式
 */
function loadPatterns() {
  if (!fs.existsSync(PATTERNS_PATH)) {
    return [];
  }
  const content = fs.readFileSync(PATTERNS_PATH, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.trim());
  return lines.map(line => {
    try {
      return JSON.parse(line);
    } catch (error) {
      return null;
    }
  }).filter(p => p !== null);
}

/**
 * 加载已完成任务
 */
function loadCompletedTasks() {
  if (!fs.existsSync(COMPLETED_PATH)) {
    return [];
  }
  const content = fs.readFileSync(COMPLETED_PATH, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.trim());
  return lines.map(line => {
    try {
      return JSON.parse(line);
    } catch (error) {
      return null;
    }
  }).filter(t => t !== null);
}

/**
 * 生成每日反思报告
 */
function generateDailyReflection() {
  console.log('\n🤔 生成每日反思报告...\n');
  
  const queue = loadQueue();
  const patterns = loadPatterns();
  const completed = loadCompletedTasks();
  
  if (!queue) {
    console.error('❌ 无法加载任务队列');
    return;
  }
  
  const today = new Date().toISOString().split('T')[0];
  const todayStart = new Date(today + 'T00:00:00+08:00').getTime();
  const todayEnd = todayStart + 24 * 60 * 60 * 1000;
  
  // 筛选今日完成的任务
  const todayCompleted = completed.filter(t => {
    const completedAt = new Date(t.completedAt).getTime();
    return completedAt >= todayStart && completedAt < todayEnd;
  });
  
  // 筛选今日提取的模式
  const todayPatterns = patterns.filter(p => {
    const createdAt = new Date(p.createdAt).getTime();
    return createdAt >= todayStart && createdAt < todayEnd;
  });
  
  // 统计数据
  const stats = {
    totalTasks: queue.stats.totalTasks,
    completedToday: todayCompleted.length,
    pendingTasks: queue.stats.pendingTasks,
    totalPatterns: patterns.length,
    patternsToday: todayPatterns.length,
    highConfidence: patterns.filter(p => p.confidence >= 0.7).length,
    mediumConfidence: patterns.filter(p => p.confidence >= 0.4 && p.confidence < 0.7).length,
    lowConfidence: patterns.filter(p => p.confidence < 0.4).length,
    skillsCreated: patterns.filter(p => p.convertedToSkill).length
  };
  
  // 生成报告
  const report = `
# 📔 每日反思报告

**日期**: ${today}  
**生成时间**: ${new Date().toISOString()}

---

## 📊 今日概览

| 指标 | 数值 |
|------|------|
| 完成任务数 | ${stats.completedToday} |
| 提取模式数 | ${stats.patternsToday} |
| 待办任务数 | ${stats.pendingTasks} |
| 总模式数 | ${stats.totalPatterns} |
| 高自信模式 | ${stats.highConfidence} |
| 中自信模式 | ${stats.mediumConfidence} |
| 低自信模式 | ${stats.lowConfidence} |
| 已创建技能 | ${stats.skillsCreated} |

---

## ✅ 完成的任务

${todayCompleted.length > 0 ? todayCompleted.map((t, i) => `
### ${i + 1}. ${t.title}
- **完成时间**: ${new Date(t.completedAt).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
- **耗时**: ${(t.duration / 1000).toFixed(1)} 秒
- **结果**: ${t.result?.message || '成功'}
`).join('\n') : '*今日暂无完成任务*'}

---

## 💡 提取的模式

${todayPatterns.length > 0 ? todayPatterns.map((p, i) => `
### ${i + 1}. ${p.title}
- **自信度**: ${p.confidence.toFixed(3)}
- **类型**: ${p.type}
- **分类**: ${p.category}
`).join('\n') : '*今日暂无提取模式*'}

---

## 🎯 做得好的（保持）

${generateWhatWentWell(todayCompleted, todayPatterns, stats)}

---

## ⚠️ 需要改进的（优化）

${generateWhatNeedsImprovement(todayCompleted, todayPatterns, stats, queue)}

---

## 🚨 遇到的问题和解决方案

${generateProblemsAndSolutions(todayCompleted)}

---

## 📈 学习方向建议

${generateLearningSuggestions(queue, patterns, stats)}

---

## 🎯 明日计划

基于今日反思，建议明日优先：

1. **继续执行**: ${queue.tasks.find(t => t.status === 'in_progress')?.title || '下一个 P0 任务'}
2. **提升自信度**: 重复使用已有模式，提升自信度到 0.7+
3. **技能创建**: 当模式自信度>0.7 时，自动创建技能
4. **学习新方向**: ${getTopLearningDirection(patterns)}

---

**反思完成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
  
  // 保存报告
  const reportPath = path.join(REFLECTIONS_DIR, `daily-${today}.md`);
  fs.writeFileSync(reportPath, report);
  
  console.log(`✅ 每日反思报告已生成：${reportPath}`);
  console.log(`\n📊 今日完成：${stats.completedToday} 个任务，${stats.patternsToday} 个模式`);
  
  return report;
}

/**
 * 生成每周反思报告
 */
function generateWeeklyReflection() {
  console.log('\n📊 生成每周反思报告...\n');
  
  const now = new Date();
  const weekStart = getWeekStart(now);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekEnd.getDate() + 7);
  
  const weekNum = getWeekNumber(now);
  const year = now.getFullYear();
  
  const queue = loadQueue();
  const patterns = loadPatterns();
  const completed = loadCompletedTasks();
  
  // 筛选本周完成的任务
  const weekCompleted = completed.filter(t => {
    const completedAt = new Date(t.completedAt).getTime();
    return completedAt >= weekStart.getTime() && completedAt < weekEnd.getTime();
  });
  
  // 统计
  const stats = {
    totalTasksCompleted: weekCompleted.length,
    totalPatterns: patterns.length,
    highConfidence: patterns.filter(p => p.confidence >= 0.7).length,
    averageConfidence: patterns.length > 0 
      ? (patterns.reduce((sum, p) => sum + p.confidence, 0) / patterns.length).toFixed(3)
      : 0,
    skillsCreated: patterns.filter(p => p.convertedToSkill).length,
    categories: categorizePatterns(patterns)
  };
  
  // 生成报告
  const report = `
# 📊 每周反思报告

**周数**: ${year}-W${weekNum.toString().padStart(2, '0')}  
**日期范围**: ${formatDate(weekStart)} - ${formatDate(weekEnd)}  
**生成时间**: ${new Date().toISOString()}

---

## 📊 本周概览

| 指标 | 数值 |
|------|------|
| 完成任务数 | ${stats.totalTasksCompleted} |
| 总模式数 | ${stats.totalPatterns} |
| 高自信模式 | ${stats.highConfidence} |
| 平均自信度 | ${stats.averageConfidence} |
| 已创建技能 | ${stats.skillsCreated} |

---

## 📈 模式分类统计

${Object.entries(stats.categories).map(([category, count]) => `- **${category}**: ${count} 个模式`).join('\n') || '*暂无模式*'}

---

## 🎯 本周成就

${generateWeeklyAchievements(weekCompleted, patterns, stats)}

---

## 📉 本周遗憾

${generateWeeklyRegrets(weekCompleted, queue)}

---

## 💡 关键洞察

${generateKeyInsights(patterns, stats)}

---

## 🚀 下周计划

基于本周反思，建议下周优先：

1. **核心目标**: ${getTopPriority(queue, patterns)}
2. **技能提升**: 将中自信模式提升到高自信
3. **知识沉淀**: 创建更多可复用技能
4. **学习方向**: ${getTopLearningDirection(patterns)}

---

**反思完成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
`;
  
  // 保存报告
  const reportPath = path.join(REFLECTIONS_DIR, `weekly-${year}-W${weekNum.toString().padStart(2, '0')}.md`);
  fs.writeFileSync(reportPath, report);
  
  console.log(`✅ 每周反思报告已生成：${reportPath}`);
  console.log(`\n📊 本周完成：${stats.totalTasksCompleted} 个任务，${stats.totalPatterns} 个模式`);
  
  return report;
}

/**
 * 辅助函数：生成做得好的部分
 */
function generateWhatWentWell(completed, patterns, stats) {
  const points = [];
  
  if (stats.completedToday > 0) {
    points.push(`✅ 完成了 ${stats.completedToday} 个任务，保持执行力`);
  }
  
  if (stats.patternsToday > 0) {
    points.push(`✅ 从任务中提取了 ${stats.patternsToday} 个模式，善于总结`);
  }
  
  if (stats.highConfidence > 0) {
    points.push(`✅ 拥有 ${stats.highConfidence} 个高自信模式，知识可靠`);
  }
  
  if (stats.skillsCreated > 0) {
    points.push(`✅ 创建了 ${stats.skillsCreated} 个技能，将经验转化为能力`);
  }
  
  if (points.length === 0) {
    return '*今日暂无亮点，明天继续努力！*';
  }
  
  return points.map(p => `- ${p}`).join('\n');
}

/**
 * 辅助函数：生成需要改进的部分
 */
function generateWhatNeedsImprovement(completed, patterns, stats, queue) {
  const points = [];
  
  if (stats.completedToday === 0) {
    points.push(`⚠️  今日未完成任务，需要提高执行力`);
  }
  
  if (stats.patternsToday === 0 && stats.completedToday > 0) {
    points.push(`⚠️  完成任务但未提取模式，需要加强总结`);
  }
  
  if (stats.lowConfidence > stats.highConfidence) {
    points.push(`⚠️  低自信模式多于高自信，需要更多实践验证`);
  }
  
  if (queue && queue.stats.pendingTasks > 10) {
    points.push(`⚠️  待办任务过多（${queue.stats.pendingTasks}个），需要优先排序`);
  }
  
  if (points.length === 0) {
    return '*今日表现优秀，继续保持！*';
  }
  
  return points.map(p => `- ${p}`).join('\n');
}

/**
 * 辅助函数：生成问题和解决方案
 */
function generateProblemsAndSolutions(completed) {
  if (completed.length === 0) {
    return '*今日暂无问题*';
  }
  
  const failed = completed.filter(t => !t.result?.success);
  
  if (failed.length === 0) {
    return '*今日任务全部成功，无问题*';
  }
  
  return failed.map(t => `
### 问题：${t.title}
- **原因**: ${t.result?.message || '未知'}
- **解决方案**: 待分析
- **预防措施**: 待制定
`).join('\n');
}

/**
 * 辅助函数：生成学习方向建议
 */
function generateLearningSuggestions(queue, patterns, stats) {
  const suggestions = [];
  
  // 基于任务队列
  const pendingP0 = queue.tasks.filter(t => t.status === 'pending' && t.priority === 'P0');
  if (pendingP0.length > 0) {
    suggestions.push(`1. **优先完成 P0 任务**: ${pendingP0[0].title}`);
  }
  
  // 基于模式分类
  const categoryCount = categorizePatterns(patterns);
  const weakestCategory = Object.entries(categoryCount).sort((a, b) => a[1] - b[1])[0];
  if (weakestCategory) {
    suggestions.push(`2. **加强${weakestCategory[0]}领域**: 当前只有${weakestCategory[1]}个模式`);
  }
  
  // 基于自信度
  const mediumPatterns = patterns.filter(p => p.confidence >= 0.4 && p.confidence < 0.7);
  if (mediumPatterns.length > 0) {
    suggestions.push(`3. **提升中自信模式**: ${mediumPatterns.length}个模式需要更多实践`);
  }
  
  if (suggestions.length === 0) {
    return '*暂无特别建议，按当前计划执行*';
  }
  
  return suggestions.join('\n');
}

/**
 * 辅助函数：获取顶级学习方向
 */
function getTopLearningDirection(patterns) {
  if (patterns.length === 0) {
    return '继续执行当前任务，积累经验';
  }
  
  const categoryCount = categorizePatterns(patterns);
  const topCategory = Object.entries(categoryCount).sort((a, b) => b[1] - a[1])[0];
  
  if (topCategory) {
    return `继续深化${topCategory[0]}领域，已有${topCategory[1]}个模式基础`;
  }
  
  return '探索新领域，扩展能力边界';
}

/**
 * 辅助函数：分类统计模式
 */
function categorizePatterns(patterns) {
  const categories = {};
  patterns.forEach(p => {
    const category = p.category || 'general';
    categories[category] = (categories[category] || 0) + 1;
  });
  return categories;
}

/**
 * 辅助函数：生成周成就
 */
function generateWeeklyAchievements(completed, patterns, stats) {
  const achievements = [];
  
  if (stats.totalTasksCompleted > 0) {
    achievements.push(`✅ 完成了 ${stats.totalTasksCompleted} 个任务`);
  }
  
  if (stats.totalPatterns > 0) {
    achievements.push(`✅ 提取了 ${stats.totalPatterns} 个模式`);
  }
  
  if (stats.highConfidence > 0) {
    achievements.push(`✅ 拥有 ${stats.highConfidence} 个高自信模式`);
  }
  
  if (stats.skillsCreated > 0) {
    achievements.push(`✅ 创建了 ${stats.skillsCreated} 个技能`);
  }
  
  if (achievements.length === 0) {
    return '*本周暂无成就，下周继续努力*';
  }
  
  return achievements.map(a => `- ${a}`).join('\n');
}

/**
 * 辅助函数：生成周遗憾
 */
function generateWeeklyRegrets(completed, queue) {
  const regrets = [];
  
  const pendingCount = queue.stats.pendingTasks;
  if (pendingCount > 5) {
    regrets.push(`⚠️  还有 ${pendingCount} 个待办任务未完成`);
  }
  
  const lowConfidence = queue.tasks.filter(t => t.status === 'blocked').length;
  if (lowConfidence > 0) {
    regrets.push(`⚠️  有 ${lowConfidence} 个任务被阻塞`);
  }
  
  if (regrets.length === 0) {
    return '*本周无遗憾，表现优秀*';
  }
  
  return regrets.map(r => `- ${r}`).join('\n');
}

/**
 * 辅助函数：生成关键洞察
 */
function generateKeyInsights(patterns, stats) {
  if (patterns.length === 0) {
    return '*暂无足够数据生成洞察*';
  }
  
  const insights = [];
  
  // 自信度洞察
  if (stats.averageConfidence > 0.6) {
    insights.push(`💡 整体知识质量较高（平均自信度${stats.averageConfidence}）`);
  } else if (stats.averageConfidence < 0.4) {
    insights.push(`💡 需要更多实践验证知识（平均自信度${stats.averageConfidence}）`);
  }
  
  // 分类洞察
  const categoryCount = categorizePatterns(patterns);
  const topCategory = Object.entries(categoryCount).sort((a, b) => b[1] - a[1])[0];
  if (topCategory) {
    insights.push(`💡 ${topCategory[0]}是主要优势领域（${topCategory[1]}个模式）`);
  }
  
  if (insights.length === 0) {
    return '*暂无特别洞察*';
  }
  
  return insights.join('\n');
}

/**
 * 辅助函数：获取顶级优先级
 */
function getTopPriority(queue, patterns) {
  const pendingP0 = queue.tasks.filter(t => t.status === 'pending' && t.priority === 'P0');
  if (pendingP0.length > 0) {
    return pendingP0[0].title;
  }
  return '继续当前任务';
}

/**
 * 辅助函数：获取周起始日期
 */
function getWeekStart(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.setDate(diff));
}

/**
 * 辅助函数：获取周数
 */
function getWeekNumber(date) {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + 4 - (d.getDay() || 7));
  const yearStart = new Date(d.getFullYear(), 0, 1);
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

/**
 * 辅助函数：格式化日期
 */
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'both';
  
  // 确保反思目录存在
  if (!fs.existsSync(REFLECTIONS_DIR)) {
    fs.mkdirSync(REFLECTIONS_DIR, { recursive: true });
    console.log(`📁 创建反思目录：${REFLECTIONS_DIR}\n`);
  }
  
  switch (command) {
    case 'daily':
      generateDailyReflection();
      break;
    case 'weekly':
      generateWeeklyReflection();
      break;
    case 'both':
      generateDailyReflection();
      console.log('');
      generateWeeklyReflection();
      break;
    default:
      console.log('用法：node reflection.js [command]');
      console.log('\n命令:');
      console.log('  daily   - 生成每日反思报告');
      console.log('  weekly  - 生成每周反思报告');
      console.log('  both    - 生成每日 + 每周报告（默认）');
  }
}

// 运行主函数
main().catch(error => {
  console.error('❌ 反思引擎错误:', error.message);
  console.error(error.stack);
  process.exit(1);
});
