#!/usr/bin/env node
/**
 * Cognitive Brain - 目标管理模块
 * 追踪和管理用户目标
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('goal_management');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const GOALS_PATH = path.join(SKILL_DIR, '.goals.json');

// 目标存储
let goals = {
  active: [],
  completed: [],
  archived: []
};

/**
 * 加载目标
 */
function load() {
  try {
    if (fs.existsSync(GOALS_PATH)) {
      goals = JSON.parse(fs.readFileSync(GOALS_PATH, 'utf8'));
    }
  } catch (e) { console.error("[goal] 错误:", e.message);
    goals = { active: [], completed: [], archived: [] };
  }
}

/**
 * 保存目标
 */
function save() {
  try {
    fs.writeFileSync(GOALS_PATH, JSON.stringify(goals, null, 2));
  } catch (e) { console.error("[goal] 错误:", e.message);
    // ignore
  }
}

/**
 * 创建目标
 */
function createGoal(description, options = {}) {
  load();

  const goal = {
    id: `goal_${Date.now()}`,
    description,
    status: 'active',
    priority: options.priority || 'medium',  // high, medium, low
    category: options.category || 'general',
    progress: 0,  // 0-100
    milestones: options.milestones || [],
    subGoals: [],
    relatedEntities: options.entities || [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
    targetDate: options.targetDate || null,
    metadata: options.metadata || {}
  };

  // 如果有里程碑，初始化
  if (goal.milestones.length > 0) {
    goal.milestones = goal.milestones.map((m, i) => ({
      id: `ms_${goal.id}_${i}`,
      description: m.description || m,
      completed: false,
      completedAt: null
    }));
  }

  goals.active.push(goal);
  save();

  return goal;
}

/**
 * 更新目标进度
 */
function updateProgress(goalId, progress, note = null) {
  load();

  const goal = goals.active.find(g => g.id === goalId);
  if (!goal) {
    return null;
  }

  goal.progress = Math.min(100, Math.max(0, progress));
  goal.updatedAt = Date.now();

  if (note) {
    goal.notes = goal.notes || [];
    goal.notes.push({ note, timestamp: Date.now() });
  }

  // 自动完成
  if (goal.progress >= 100) {
    goal.status = 'completed';
    goal.completedAt = Date.now();
    goals.active = goals.active.filter(g => g.id !== goalId);
    goals.completed.push(goal);
  }

  save();
  return goal;
}

/**
 * 完成里程碑
 */
function completeMilestone(goalId, milestoneId) {
  load();

  const goal = goals.active.find(g => g.id === goalId);
  if (!goal) {
    return null;
  }

  const milestone = goal.milestones.find(m => m.id === milestoneId);
  if (!milestone) {
    return null;
  }

  milestone.completed = true;
  milestone.completedAt = Date.now();

  // 更新进度
  const completedCount = goal.milestones.filter(m => m.completed).length;
  goal.progress = goal.milestones.length > 0 
    ? Math.round((completedCount / goal.milestones.length) * 100) 
    : (completedCount > 0 ? 100 : 0);
  goal.updatedAt = Date.now();

  save();
  return goal;
}

/**
 * 添加子目标
 */
function addSubGoal(parentGoalId, description) {
  load();

  const parent = goals.active.find(g => g.id === parentGoalId);
  if (!parent) {
    return null;
  }

  const subGoal = {
    id: `sub_${Date.now()}`,
    description,
    completed: false,
    createdAt: Date.now()
  };

  parent.subGoals.push(subGoal);
  parent.updatedAt = Date.now();
  save();

  return subGoal;
}

/**
 * 取消目标
 */
function cancelGoal(goalId, reason = null) {
  load();

  const goal = goals.active.find(g => g.id === goalId);
  if (!goal) {
    return null;
  }

  goal.status = 'cancelled';
  goal.cancelledAt = Date.now();
  goal.cancelReason = reason;
  goal.updatedAt = Date.now();

  goals.active = goals.active.filter(g => g.id !== goalId);
  goals.archived.push(goal);
  save();

  return goal;
}

/**
 * 获取活跃目标
 */
function getActiveGoals(category = null) {
  load();

  let active = goals.active;

  if (category) {
    active = active.filter(g => g.category === category);
  }

  return active.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
}

/**
 * 获取目标进度摘要
 */
function getProgressSummary() {
  load();

  const summary = {
    total: goals.active.length + goals.completed.length,
    active: goals.active.length,
    completed: goals.completed.length,
    byCategory: {},
    byPriority: {},
    avgProgress: 0
  };

  // 统计活跃目标
  for (const goal of goals.active) {
    summary.byCategory[goal.category] = (summary.byCategory[goal.category] || 0) + 1;
    summary.byPriority[goal.priority] = (summary.byPriority[goal.priority] || 0) + 1;
    summary.avgProgress += goal.progress;
  }

  if (goals.active.length > 0) {
    summary.avgProgress = Math.round(summary.avgProgress / goals.active.length);
  }

  return summary;
}

/**
 * 检查目标关联
 */
function checkGoalRelevance(context) {
  load();

  const relevant = [];

  for (const goal of goals.active) {
    // 检查实体关联
    if (context.entities) {
      const matchingEntities = goal.relatedEntities.filter(e =>
        context.entities.includes(e)
      );
      if (matchingEntities.length > 0) {
        relevant.push({
          goal,
          relevance: 'entity_match',
          matchingEntities
        });
      }
    }

    // 检查关键词关联
    if (context.keywords) {
      const keywords = goal.description.toLowerCase().split(/\s+/);
      const matching = context.keywords.filter(k =>
        keywords.some(kw => kw.includes(k.toLowerCase()))
      );
      if (matching.length > 0) {
        relevant.push({
          goal,
          relevance: 'keyword_match',
          matchingKeywords: matching
        });
      }
    }
  }

  return relevant;
}

/**
 * 获取即将到期的目标
 */
function getUpcomingDeadlines(days = 7) {
  load();

  const now = Date.now();
  const cutoff = now + days * 24 * 60 * 60 * 1000;

  return goals.active
    .filter(g => g.targetDate && g.targetDate <= cutoff)
    .sort((a, b) => a.targetDate - b.targetDate);
}

/**
 * 生成目标报告
 */
function generateReport() {
  load();

  const lines = [
    '📊 目标报告',
    '='.repeat(50),
    '',
    `活跃目标: ${goals.active.length}`,
    `已完成: ${goals.completed.length}`,
    `已归档: ${goals.archived.length}`,
    ''
  ];

  if (goals.active.length > 0) {
    lines.push('🎯 活跃目标:');
    for (const goal of goals.active) {
      const progress = '█'.repeat(Math.floor(goal.progress / 10)) +
                       '░'.repeat(10 - Math.floor(goal.progress / 10));
      lines.push(`   [${progress}] ${goal.progress}% - ${goal.description}`);
      if (goal.milestones.length > 0) {
        const completed = goal.milestones.filter(m => m.completed).length;
        lines.push(`      里程碑: ${completed}/${goal.milestones.length}`);
      }
    }
  }

  return lines.join('\n');
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'create':
      if (args[0]) {
        const goal = createGoal(args.join(' '), { priority: 'medium' });
        console.log('✅ 目标创建:', goal.id);
      }
      break;

    case 'list':
      const active = getActiveGoals(args[0]);
      console.log('📋 活跃目标:');
      active.forEach(g => {
        console.log(`   [${g.priority}] ${g.progress}% - ${g.description}`);
      });
      break;

    case 'progress':
      if (args[0] && args[1]) {
        const goal = updateProgress(args[0], parseInt(args[1]));
        if (goal) {
          console.log(`✅ 进度更新: ${goal.progress}%`);
        }
      }
      break;

    case 'summary':
      console.log(JSON.stringify(getProgressSummary(), null, 2));
      break;

    case 'report':
      console.log(generateReport());
      break;

    default:
      console.log(`
目标管理模块

用法:
  node goal_management.cjs create <description>  # 创建目标
  node goal_management.cjs list [category]       # 列出目标
  node goal_management.cjs progress <id> <0-100> # 更新进度
  node goal_management.cjs summary               # 进度摘要
  node goal_management.cjs report                # 生成报告
      `);
  }
}

main();

// 导出模块
module.exports = {
  createGoal,
  updateProgress,
  completeGoal,
  deleteGoal,
  getActiveGoals,
  getProgressSummary,
  generateReport,
  load,
  save
};

