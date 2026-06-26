/**
 * Progress Check - Coaching-style accountability
 *
 * Reviews task progress and provides coaching feedback
 */

const stateManager = require('./state-manager');
const questions = require('./coaching-questions');

// --- ASCII visualization helpers ---

/**
 * Generate an ASCII progress bar
 */
function progressBar(percent, width = 20) {
  const clamped = Math.max(0, Math.min(100, percent));
  const filled = Math.round((clamped / 100) * width);
  const empty = width - filled;
  return '\u2588'.repeat(filled) + '\u2591'.repeat(empty) + ` ${clamped}%`;
}

/**
 * Generate a 7-day weekly activity chart
 */
function weeklyChart(days) {
  // days: array of 7 booleans (Mon-Sun), true = active
  const labels = ['一', '二', '三', '四', '五', '六', '日'];
  return days.map((active, i) => `${labels[i]}${active ? '█' : '░'}`).join(' ');
}

/**
 * Main progress check function
 */
async function checkProgress(options = {}) {
  try {
    const state = stateManager.loadState();
    const activeGoals = stateManager.getActiveGoals(state);

    if (activeGoals.length === 0) {
      return {
        type: 'no-goals',
        message: '目前没有活跃的目标。想设定一个新目标吗？',
        suggestion: '说 "帮我设定一个目标" 开始',
        response: '目前没有活跃的目标。想设定一个新目标吗？\n\n说 "帮我设定一个目标" 开始'
      };
    }

    // Check progress for each active goal
    const progressReports = await Promise.all(
      activeGoals.map(goal => checkGoalProgress(goal, state))
    );

    // Update momentum based on overall progress
    const overallStatus = calculateOverallStatus(progressReports);
    const updatedState = stateManager.updateMomentum(state, overallStatus);

    // Check milestones
    const milestoneAlerts = stateManager.getMilestoneAlerts(updatedState);

    // Check achievements
    const newAchievements = stateManager.checkAchievements(updatedState);

    // Mark milestone alerts as notified
    for (const alert of milestoneAlerts) {
      stateManager.markMilestoneNotified(updatedState, alert.goalId, alert.milestone.id, alert.type);
    }

    stateManager.saveState(updatedState);

    // Generate coaching response
    let response = buildProgressResponse(progressReports, updatedState, options);

    // Append milestone check-ins (persona-aware, conversational)
    if (milestoneAlerts.length > 0) {
      const persona = updatedState.user.preferences.coachingStyle || 'balanced';
      response += '\n\n---\n\n';
      for (const alert of milestoneAlerts) {
        const vars = {
          goal: alert.goalTitle,
          milestone: alert.milestone.title,
          days: alert.daysOverdue,
          hours: alert.hoursLeft
        };
        response += questions.getMilestoneMessage(persona, alert.type, vars) + '\n';
      }
    }

    // Append achievement notifications
    if (newAchievements.length > 0) {
      response += '\n\n---\n\n';
      for (const a of newAchievements) {
        response += `${a.icon} **成就解锁：${a.name}** — ${a.description}\n`;
      }
    }

    return {
      success: true,
      momentum: updatedState.momentum,
      reports: progressReports,
      milestoneAlerts,
      response
    };
  } catch (error) {
    console.error('checkProgress error:', error);
    return {
      success: false,
      response: '进度检查时出现错误，请稍后重试。'
    };
  }
}

/**
 * Check progress for a single goal
 */
async function checkGoalProgress(goal, state) {
  const taskContent = stateManager.loadTaskFile(goal.taskFile);

  if (!taskContent) {
    return {
      goalId: goal.id,
      title: goal.title,
      status: 'error',
      message: '无法读取任务文件'
    };
  }

  // Parse task content to determine progress
  const progress = parseTaskProgress(taskContent);

  // Determine status
  const status = determineStatus(progress, goal);

  return {
    goalId: goal.id,
    title: goal.title,
    status: status,
    progress: progress,
    taskFile: goal.taskFile,
    createdAt: goal.createdAt,
    targetDate: goal.targetDate
  };
}

/**
 * Parse task file to extract progress information
 * Supports [x] and [X], strips code blocks before matching
 */
function parseTaskProgress(content) {
  // Strip fenced code blocks so checkboxes inside ``` ``` are not counted
  const stripped = content.replace(/```[\s\S]*?```/g, '');

  // Count completed vs total tasks (case-insensitive x)
  const totalTasks = (stripped.match(/- \[[ xX]\]/g) || []).length;
  const completedTasks = (stripped.match(/- \[[xX]\]/g) || []).length;

  // Extract last daily record
  const dailyRecordMatch = content.match(/### (\d{4}-\d{2}-\d{2})\n\*\*计划：\*\*(.*?)\n\*\*实际：\*\*(.*?)\n/s);

  let lastRecord = null;
  if (dailyRecordMatch) {
    lastRecord = {
      date: dailyRecordMatch[1],
      plan: dailyRecordMatch[2].trim(),
      actual: dailyRecordMatch[3].trim()
    };
  }

  // Extract progress percentage if exists
  const progressMatch = content.match(/(\d+)%/);
  const percentComplete = progressMatch ? parseInt(progressMatch[1]) :
                          totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return {
    totalTasks,
    completedTasks,
    percentComplete,
    lastRecord
  };
}

/**
 * Determine task status
 */
function determineStatus(progress, goal) {
  const { lastRecord, completedTasks, totalTasks } = progress;

  // Check if any progress today
  const today = new Date().toISOString().split('T')[0];
  const hasProgressToday = lastRecord && lastRecord.date === today && lastRecord.actual.length > 0;

  if (hasProgressToday) {
    if (completedTasks === totalTasks && totalTasks > 0) {
      return 'completed';
    }
    return 'partial';
  }

  // No progress today
  const daysSinceCreation = Math.floor(
    (Date.now() - new Date(goal.createdAt).getTime()) / (1000 * 60 * 60 * 24)
  );

  if (daysSinceCreation > 7 && completedTasks === 0) {
    return 'stuck';
  }

  return 'notStarted';
}

/**
 * Calculate overall status from all reports
 */
function calculateOverallStatus(reports) {
  const statuses = reports.map(r => r.status);

  // If any completed today, it's a success
  if (statuses.includes('completed') || statuses.includes('partial')) {
    return 'success';
  }

  // If any stuck, it's concerning
  if (statuses.includes('stuck')) {
    return 'miss';
  }

  // Otherwise neutral
  return 'miss';
}

/**
 * Build coaching response based on progress
 */
function buildProgressResponse(reports, state, options = {}) {
  const { momentum } = state;
  const tone = questions.getToneForMomentum(momentum.current);

  // Choose greeting based on momentum — apply persona if available
  let greeting;
  if (questions.getPersonaTone) {
    const persona = state.user.preferences.coachingStyle || 'balanced';
    const personaTone = questions.getPersonaTone(persona, momentum.current);
    greeting = personaTone ? questions.pickRandom(personaTone.greeting) : questions.pickRandom(tone.greeting);
  } else {
    greeting = questions.pickRandom(tone.greeting);
  }

  // Build response for each goal
  const goalResponses = reports.map(report => {
    return buildGoalResponse(report, momentum, options);
  }).filter(r => r); // Remove nulls

  // Combine into final message
  let message = '';

  if (options.timeOfDay === 'morning') {
    message = buildMorningMessage(reports, state, greeting);
  } else if (options.timeOfDay === 'evening') {
    message = buildEveningMessage(reports, state, greeting);
  } else {
    // General check
    message = `${greeting}\n\n${goalResponses.join('\n\n---\n\n')}`;
  }

  return message;
}

/**
 * Build response for a single goal
 */
function buildGoalResponse(report, momentum, options) {
  const { status, title, progress } = report;

  if (status === 'completed') {
    const question = questions.getProgressQuestion('completed', { task: title });
    return `✅ **${title}**\n${progressBar(progress.percentComplete)}\n\n${question}`;
  }

  if (status === 'partial') {
    const { percentComplete } = progress;
    const question = questions.getProgressQuestion('partial', {
      percent: percentComplete,
      context: '考虑到其他事情'
    });
    return `🟡 **${title}** (${percentComplete}%)\n${progressBar(percentComplete)}\n\n${question}`;
  }

  if (status === 'notStarted') {
    const question = questions.getProgressQuestion('notStarted', { task: title });
    return `⚪ **${title}**\n\n${question}`;
  }

  if (status === 'stuck') {
    const question = questions.getProgressQuestion('stuck');
    return `💬 **${title}**\n\n${question}`;
  }

  return null;
}

/**
 * Build morning check-in message
 */
function buildMorningMessage(reports, state, greeting) {
  const activeGoals = reports.filter(r => r.status !== 'completed');

  if (activeGoals.length === 0) {
    return `${greeting}\n\n所有目标都已完成！🎉\n\n准备好设定新的目标了吗？`;
  }

  const goalList = activeGoals.map(r => `- ${r.title}`).join('\n');

  return `${greeting}\n\n**今天的目标：**\n${goalList}\n\n从哪个开始？`;
}

/**
 * Build evening check-in message
 */
function buildEveningMessage(reports, state, greeting) {
  const completed = reports.filter(r => r.status === 'completed');
  const partial = reports.filter(r => r.status === 'partial');
  const notStarted = reports.filter(r => r.status === 'notStarted');

  let message = `${greeting}\n\n**今日回顾：**\n\n`;

  if (completed.length > 0) {
    message += `✅ 完成 ${completed.length} 个\n`;
    completed.forEach(r => {
      message += `   - ${r.title}\n`;
    });
    message += '\n';
  }

  if (partial.length > 0) {
    message += `🟡 进行中 ${partial.length} 个\n`;
    partial.forEach(r => {
      message += `   - ${r.title} (${r.progress.percentComplete}%)\n`;
    });
    message += '\n';
  }

  if (notStarted.length > 0) {
    message += `⚪ 未开始 ${notStarted.length} 个\n\n`;
  }

  // Add coaching question
  if (completed.length === reports.length && reports.length > 0) {
    // All completed
    message += questions.getProgressQuestion('completed', { task: '所有任务' });
  } else if (completed.length > 0) {
    // Some completed
    message += '不错的进展！明天想继续保持这个节奏吗？';
  } else if (notStarted.length === reports.length) {
    // Nothing started
    message += questions.getProgressQuestion('notStarted', { task: '今天的任务' });
  } else {
    // Mixed
    message += '今天遇到了什么挑战？明天想怎么调整？';
  }

  return message;
}

/**
 * Quick progress summary
 */
function getProgressSummary() {
  const state = stateManager.loadState();
  const activeGoals = stateManager.getActiveGoals(state);

  return {
    totalGoals: activeGoals.length,
    momentum: state.momentum.current,
    consecutiveDays: state.momentum.consecutiveDays,
    lastSuccess: state.momentum.lastSuccess
  };
}

/**
 * Update task progress manually
 */
async function updateProgress(goalId, progressData) {
  try {
    const state = stateManager.loadState();
    const goal = state.goals.find(g => g.id === goalId);

    if (!goal) {
      return { error: 'Goal not found' };
    }

    // Load task file
    let content = stateManager.loadTaskFile(goal.taskFile);

    // Add today's record
    const today = new Date().toISOString().split('T')[0];
    const recordEntry = `
### ${today}
**计划：** ${progressData.plan || ''}
**实际：** ${progressData.actual || ''}
**反思：** ${progressData.reflection || ''}
**明天调整：** ${progressData.tomorrow || ''}
    `.trim();

    // Insert at the daily record section
    content = content.replace(
      /(## 📝 每日记录)/,
      `$1\n\n${recordEntry}`
    );

    // Save
    stateManager.saveTaskFile(goal.taskFile, content);

    return {
      success: true,
      message: '进度已更新！'
    };
  } catch (error) {
    console.error('updateProgress error:', error);
    return {
      success: false,
      message: '更新进度时出现错误，请稍后重试。'
    };
  }
}

module.exports = {
  checkProgress,
  getProgressSummary,
  updateProgress,
  progressBar,
  weeklyChart
};
