/**
 * Reflection - Weekly/Monthly deep review
 *
 * Facilitates structured reflection and pattern recognition
 */

const stateManager = require('./state-manager');
const questions = require('./coaching-questions');

/**
 * Start reflection session
 */
async function startReflection(period = 'week') {
  try {
    const state = stateManager.loadState();
    const goals = stateManager.getActiveGoals(state);

    if (goals.length === 0) {
      return {
        type: 'no-goals',
        message: '目前没有活跃的目标来回顾。\n\n这段时间过得怎么样？有什么想分享的吗？'
      };
    }

    // Collect data from the period
    const periodData = await collectPeriodData(goals, period);

    // Analyze patterns
    const patterns = analyzePatterns(periodData, state);

    // Generate reflection prompts
    const response = buildReflectionResponse(periodData, patterns, period);

    // Update insights and record check-in — single save
    const updatedState = updateInsights(state, patterns);
    stateManager.recordCheckIn(updatedState, 'weekly');
    stateManager.saveState(updatedState);

    return {
      success: true,
      period,
      data: periodData,
      patterns,
      response
    };
  } catch (error) {
    console.error('Reflection error:', error);
    return {
      type: 'error',
      message: '反思模块出现错误，请稍后重试。',
      response: '反思模块出现错误，请稍后重试。'
    };
  }
}

/**
 * Collect data from the specified period
 */
async function collectPeriodData(goals, period) {
  const data = {
    period,
    goals: [],
    summary: {
      totalTasks: 0,
      completedTasks: 0,
      daysActive: 0,
      daysInactive: 0
    }
  };

  for (const goal of goals) {
    const taskContent = stateManager.loadTaskFile(goal.taskFile);
    if (!taskContent) continue;

    // Extract daily records for the period
    const records = extractDailyRecords(taskContent, period);

    // Calculate goal-specific metrics
    const metrics = calculateGoalMetrics(records);

    data.goals.push({
      id: goal.id,
      title: goal.title,
      records,
      metrics
    });

    // Update summary
    data.summary.totalTasks += metrics.totalTasks;
    data.summary.completedTasks += metrics.completedTasks;
    data.summary.daysActive += metrics.daysWithProgress;
  }

  return data;
}

/**
 * Extract daily records from task content
 */
function extractDailyRecords(content, period) {
  const records = [];

  // Match all daily record sections
  const recordPattern = /### (\d{4}-\d{2}-\d{2})\n\*\*计划：\*\*(.*?)\n\*\*实际：\*\*(.*?)\n\*\*反思：\*\*(.*?)\n\*\*明天调整：\*\*(.*?)\n/gs;

  let match;
  while ((match = recordPattern.exec(content)) !== null) {
    const date = new Date(match[1]);

    // Check if date is in period
    if (isInPeriod(date, period)) {
      records.push({
        date: match[1],
        plan: match[2].trim(),
        actual: match[3].trim(),
        reflection: match[4].trim(),
        tomorrow: match[5].trim()
      });
    }
  }

  return records;
}

/**
 * Check if date is within the specified period
 */
function isInPeriod(date, period) {
  const now = new Date();
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

  if (period === 'week') {
    return diffDays <= 7;
  } else if (period === 'month') {
    return diffDays <= 30;
  }

  return false;
}

/**
 * Calculate metrics for a goal
 */
function calculateGoalMetrics(records) {
  const metrics = {
    totalDays: records.length,
    daysWithProgress: 0,
    totalTasks: 0,
    completedTasks: 0,
    reflections: []
  };

  records.forEach(record => {
    if (record.actual && record.actual.length > 0) {
      metrics.daysWithProgress++;
    }

    if (record.reflection && record.reflection.length > 0) {
      metrics.reflections.push(record.reflection);
    }
  });

  return metrics;
}

/**
 * Analyze patterns from period data
 */
function analyzePatterns(periodData, state) {
  const patterns = {
    consistency: {
      level: 'unknown',
      observation: ''
    },
    productivity: {
      bestDays: [],
      worstDays: [],
      observation: ''
    },
    blockers: [],
    successes: []
  };

  // Analyze consistency
  const totalDays = getPeriodDays(periodData.period);
  const activeDays = periodData.summary.daysActive;
  const consistencyRate = activeDays / totalDays;

  if (consistencyRate >= 0.8) {
    patterns.consistency.level = 'high';
    patterns.consistency.observation = `${periodData.period === 'week' ? '这周' : '这个月'}你保持了很高的执行频率 (${Math.round(consistencyRate * 100)}%)`;
  } else if (consistencyRate >= 0.5) {
    patterns.consistency.level = 'medium';
    patterns.consistency.observation = `${periodData.period === 'week' ? '这周' : '这个月'}有一半时间在推进`;
  } else {
    patterns.consistency.level = 'low';
    patterns.consistency.observation = `${periodData.period === 'week' ? '这周' : '这个月'}的执行频率较低`;
  }

  // Extract common blockers from reflections
  const allReflections = periodData.goals.flatMap(g => g.metrics.reflections);
  const blockerKeywords = ['会议', '打断', '分心', '累', '没时间', '拖延'];

  blockerKeywords.forEach(keyword => {
    const count = allReflections.filter(r => r.includes(keyword)).length;
    if (count >= 2) {
      patterns.blockers.push(`${keyword} (出现 ${count} 次)`);
    }
  });

  // Identify successes
  const successKeywords = ['完成', '突破', '顺利', '高效'];
  successKeywords.forEach(keyword => {
    const count = allReflections.filter(r => r.includes(keyword)).length;
    if (count >= 2) {
      patterns.successes.push(`${keyword} (出现 ${count} 次)`);
    }
  });

  return patterns;
}

/**
 * Get number of days in period
 */
function getPeriodDays(period) {
  return period === 'week' ? 7 : 30;
}

/**
 * Build reflection response
 */
function buildReflectionResponse(data, patterns, period) {
  const periodName = period === 'week' ? '本周' : '本月';

  let response = `# 📊 ${periodName}回顾\n\n`;

  // Summary
  response += `## 总览\n\n`;
  response += `- **活跃天数：** ${data.summary.daysActive} / ${getPeriodDays(period)} 天\n`;
  response += `- **执行率：** ${Math.round(data.summary.daysActive / getPeriodDays(period) * 100)}%\n`;
  response += `- **进行中的目标：** ${data.goals.length} 个\n\n`;

  // Patterns
  response += `## 🔍 模式发现\n\n`;
  response += `**一致性：** ${patterns.consistency.observation}\n\n`;

  if (patterns.blockers.length > 0) {
    response += `**常见障碍：**\n`;
    patterns.blockers.forEach(b => {
      response += `- ${b}\n`;
    });
    response += '\n';
  }

  if (patterns.successes.length > 0) {
    response += `**成功因素：**\n`;
    patterns.successes.forEach(s => {
      response += `- ${s}\n`;
    });
    response += '\n';
  }

  // Goals breakdown
  response += `## 📝 各目标进展\n\n`;
  data.goals.forEach(goal => {
    response += `### ${goal.title}\n`;
    response += `- 活跃 ${goal.metrics.daysWithProgress} 天\n`;
    if (goal.metrics.reflections.length > 0) {
      response += `- 最近反思：${goal.metrics.reflections[goal.metrics.reflections.length - 1]}\n`;
    }
    response += '\n';
  });

  // Reflection questions
  response += `---\n\n## 💭 反思问题\n\n`;
  response += `${questions.getReflectionQuestion('review')}\n\n`;
  response += `${questions.getReflectionQuestion('learning')}\n\n`;
  response += `${questions.getReflectionQuestion('forward')}\n\n`;

  response += `---\n\n`;
  response += `_花点时间思考这些问题。你的回答会帮助我更好地支持你。_`;

  return response;
}

/**
 * Update insights based on patterns
 */
function updateInsights(state, patterns) {
  // Add common blockers to insights
  patterns.blockers.forEach(blocker => {
    const blockerText = blocker.split(' (')[0]; // Remove count
    if (!state.insights.commonBlockers.includes(blockerText)) {
      state.insights.commonBlockers.push(blockerText);
    }
  });

  // Add success patterns
  patterns.successes.forEach(success => {
    const successText = success.split(' (')[0];
    if (!state.insights.successPatterns.includes(successText)) {
      state.insights.successPatterns.push(successText);
    }
  });

  // Keep only recent insights (max 10 each)
  state.insights.commonBlockers = state.insights.commonBlockers.slice(-10);
  state.insights.successPatterns = state.insights.successPatterns.slice(-10);

  return state;
}

/**
 * Process reflection answer
 */
async function processReflectionAnswer(question, answer) {
  try {
    const state = stateManager.loadState();

    // Store insight based on question type
    if (question.includes('学到')) {
      stateManager.addInsight(state, 'successPatterns', answer);
    } else if (question.includes('障碍') || question.includes('挑战')) {
      stateManager.addInsight(state, 'commonBlockers', answer);
    }

    stateManager.saveState(state);

    return {
      success: true,
      message: '谢谢分享。这些洞察会帮助我更好地支持你。'
    };
  } catch (error) {
    console.error('processReflectionAnswer error:', error);
    return {
      success: false,
      message: '保存反思时出现错误，请稍后重试。'
    };
  }
}

module.exports = {
  startReflection,
  processReflectionAnswer
};
