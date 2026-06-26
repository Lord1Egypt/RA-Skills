/**
 * Analyzer Module - Efficiency analysis engine
 */

const { loadEvents, loadConfig } = require('../lib/storage');

function hasValidDurationEvent(event) {
  if (!event || !event.startTime || !event.endTime) {
    return false;
  }

  const duration = getDurationHours(event.startTime, event.endTime);
  return Number.isFinite(duration) && duration > 0;
}

function getPeriodDayCount(startDate, endDate) {
  const start = new Date(`${startDate}T00:00:00`);
  const end = new Date(`${endDate}T00:00:00`);
  const diffMs = end - start;

  return Math.max(1, Math.round(diffMs / (1000 * 60 * 60 * 24)) + 1);
}

/**
 * Parse time string to hours
 * @param {string} timeStr - Time string (HH:MM or ISO)
 * @returns {number} Hours
 */
function parseTimeToHours(timeStr) {
  if (!timeStr) return 0;
  
  // Handle ISO format
  if (timeStr.includes('T')) {
    const date = new Date(timeStr);
    return date.getHours() + date.getMinutes() / 60;
  }
  
  // Handle HH:MM format
  const [hours, minutes] = timeStr.split(':').map(Number);
  return hours + (minutes || 0) / 60;
}

/**
 * Get duration in hours between two times
 * @param {string} startTime - Start time
 * @param {string} endTime - End time
 * @returns {number} Duration in hours
 */
function getDurationHours(startTime, endTime) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  return (end - start) / (1000 * 60 * 60);
}

/**
 * Get time slot from time
 * @param {string} timeStr - Time string
 * @returns {string} Slot: morning, afternoon, evening, night
 */
function getTimeSlot(timeStr) {
  const hours = parseTimeToHours(timeStr);
  
  if (hours >= 6 && hours < 12) return 'morning';
  if (hours >= 12 && hours < 18) return 'afternoon';
  if (hours >= 18 && hours < 22) return 'evening';
  return 'night';
}

/**
 * Get time slot name in Chinese
 * @param {string} slot - Slot name
 * @returns {string} Chinese name
 */
function getTimeSlotName(slot) {
  const names = {
    morning: '上午',
    afternoon: '下午',
    evening: '傍晚',
    night: '夜晚'
  };
  return names[slot] || slot;
}

/**
 * Analyze efficiency for a specific category
 * @param {string} category - Category to analyze
 * @param {Array} events - Events to analyze (optional, loads from storage if not provided)
 * @returns {Object} Category analysis
 */
function analyzeCategory(category, events = null) {
  const targetEvents = events
    ? events.filter(event => event.category === category)
    : loadEvents({ category });
  
  if (targetEvents.length === 0) {
    return {
      category,
      totalCount: 0,
      totalDuration: 0,
      avgDuration: 0,
      bestDuration: 0,
      worstDuration: 0,
      completionRate: 0,
      efficiency: 0,
      trend: 'stable'
    };
  }

  const durationEvents = targetEvents.filter(hasValidDurationEvent);
  const durations = durationEvents.map(e => getDurationHours(e.startTime, e.endTime));
  const completed = targetEvents.filter(e => e.status === 'completed').length;

  if (durations.length === 0) {
    return {
      category,
      totalCount: targetEvents.length,
      totalDuration: 0,
      avgDuration: 0,
      bestDuration: 0,
      worstDuration: 0,
      completionRate: Math.round((completed / targetEvents.length) * 100),
      efficiency: 0,
      trend: 'stable'
    };
  }
  
  const totalDuration = durations.reduce((sum, d) => sum + d, 0);
  const avgDuration = totalDuration / durations.length;
  const bestDuration = Math.min(...durations);
  const worstDuration = Math.max(...durations);
  const completionRate = (completed / targetEvents.length) * 100;
  
  // Efficiency: higher is better (100 = best)
  // Compare avg to best: efficiency = (best / avg) * 100, capped at 100
  const efficiency = Math.min(100, Math.round((bestDuration / avgDuration) * 100));

  return {
    category,
    totalCount: targetEvents.length,
    totalDuration: Math.round(totalDuration * 100) / 100,
    avgDuration: Math.round(avgDuration * 100) / 100,
    bestDuration: Math.round(bestDuration * 100) / 100,
    worstDuration: Math.round(worstDuration * 100) / 100,
    completionRate: Math.round(completionRate),
    efficiency,
    trend: 'stable'
  };
}

/**
 * Analyze time slot efficiency for each category
 * @param {Array} events - Events to analyze
 * @returns {Array} Time slot analyses
 */
function analyzeTimeSlots(events) {
  const slotData = {};
  
  events.filter(hasValidDurationEvent).forEach(event => {
    const slot = getTimeSlot(event.startTime);
    const duration = getDurationHours(event.startTime, event.endTime);
    const key = `${slot}_${event.category}`;
    
    if (!slotData[key]) {
      slotData[key] = {
        slot,
        category: event.category,
        durations: [],
        count: 0
      };
    }
    
    slotData[key].durations.push(duration);
    slotData[key].count++;
  });
  
  return Object.values(slotData).map(data => {
    const avg = data.durations.reduce((s, d) => s + d, 0) / data.durations.length;
    return {
      slot: data.slot,
      category: data.category,
      avgDuration: Math.round(avg * 100) / 100,
      count: data.count,
      efficiency: Math.round((1 / avg) * 100) // Lower avg = higher efficiency
    };
  });
}

/**
 * Find best time slots for each category
 * @param {Array} events - Events to analyze
 * @returns {Array} Best time slots
 */
function findBestTimeSlots(events) {
  const slotAnalysis = analyzeTimeSlots(events);

  if (slotAnalysis.length === 0) {
    return [];
  }
  
  // Group by category
  const byCategory = {};
  slotAnalysis.forEach(sa => {
    if (!byCategory[sa.category]) {
      byCategory[sa.category] = [];
    }
    byCategory[sa.category].push(sa);
  });
  
  // Find best slot for each category
  const result = [];
  Object.entries(byCategory).forEach(([category, slots]) => {
    const best = slots.reduce((a, b) => (a.efficiency > b.efficiency ? a : b));
    result.push({
      category,
      slot: best.slot,
      slotName: getTimeSlotName(best.slot),
      efficiency: best.efficiency,
      avgDuration: best.avgDuration
    });
  });
  
  return result.sort((a, b) => b.efficiency - a.efficiency);
}

/**
 * Generate suggestions based on analysis
 * @param {Object} analysis - Full analysis result
 * @returns {Array} Suggestions
 */
function generateSuggestions(analysis) {
  const suggestions = [];
  const config = loadConfig();
  
  // Category-based suggestions
  analysis.categoryBreakdown.forEach(cat => {
    if (cat.totalCount < 2) return;
    
    // Efficiency suggestion
    if (cat.efficiency < 70) {
      suggestions.push({
        type: 'optimization',
        priority: 'high',
        title: `${cat.category} 效率可提升`,
        description: `你的${cat.category}类任务平均耗时${cat.avgDuration}h，最佳只需${cat.bestDuration}h，还有优化空间。`,
        actionSteps: [
          '分析最佳案例的具体做法',
          '识别导致效率低下的干扰因素',
          '尝试在最佳时间段进行此类任务'
        ]
      });
    }
    
    // Best time suggestion
    const bestSlot = analysis.bestTimeSlots.find(b => b.category === cat.category);
    if (bestSlot) {
      suggestions.push({
        type: 'schedule',
        priority: 'medium',
        title: `${cat.category} 建议安排在${bestSlot.slotName}`,
        description: `数据显示你在${bestSlot.slotName}做${cat.category}类事情效率最高。`,
        actionSteps: [
          `将${cat.category}类任务安排在${bestSlot.slotName}时段`
        ]
      });
    }
  });
  
  // Time-based suggestions
  const totalHours = analysis.summary.totalHours;
  if (totalHours > 10) {
    suggestions.push({
      type: 'optimization',
      priority: 'high',
      title: '注意劳逸结合',
      description: '今日专注时长超过10小时，长时间工作会降低效率。',
      actionSteps: [
        '每工作2小时休息15分钟',
        '适当增加运动和休息时间',
        '确保充足睡眠'
      ]
    });
  }
  
  // Completion rate suggestion
  if (analysis.summary.completionRate < 70) {
    suggestions.push({
      type: 'optimization',
      priority: 'medium',
      title: '提高任务完成率',
      description: `当前完成率为${Math.round(analysis.summary.completionRate)}%，建议设置更合理的目标。`,
      actionSteps: [
        '将大任务拆分为小任务',
        '优先完成重要且紧急的事项',
        '记录中断原因以便改进'
      ]
    });
  }
  
  return suggestions.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
}

/**
 * Generate full efficiency report
 * @param {string} period - Period: daily, weekly, monthly
 * @param {string} date - Date (YYYY-MM-DD) or week/month identifier
 * @returns {Object} Full report
 */
function generateReport(period, date) {
  const now = new Date();
  let startDate, endDate;
  
  if (period === 'daily') {
    const targetDate = date || now.toISOString().split('T')[0];
    startDate = targetDate;
    endDate = targetDate;
  } else if (period === 'weekly') {
    const weekStart = date ? new Date(date) : now;
    const day = weekStart.getDay();
    const diff = weekStart.getDate() - day + (day === 0 ? -6 : 1);
    weekStart.setDate(diff);
    startDate = weekStart.toISOString().split('T')[0];
    endDate = new Date(weekStart.getTime() + 6 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  } else if (period === 'monthly') {
    const [year, month] = (date || now.toISOString().slice(0, 7)).split('-');
    startDate = `${year}-${month}-01`;
    const lastDay = new Date(year, month, 0).getDate();
    endDate = `${year}-${month}-${lastDay}`;
  }
  
  const events = loadEvents({ startDate, endDate });
  const validDurationEvents = events.filter(hasValidDurationEvent);
  const periodDayCount = getPeriodDayCount(startDate, endDate);
  
  // Calculate summary
  const durations = validDurationEvents.map(e => getDurationHours(e.startTime, e.endTime));
  const totalHours = durations.reduce((sum, d) => sum + d, 0);
  const completed = events.filter(e => e.status === 'completed').length;
  const completionRate = events.length > 0 ? (completed / events.length) * 100 : 0;
  
  // Get unique categories
  const categories = [...new Set(events.map(e => e.category))];
  
  // Analyze each category
  const categoryBreakdown = categories.map(cat => analyzeCategory(cat, events));
  
  // Time analysis
  const bestTimeSlots = findBestTimeSlots(events);
  
  // Generate suggestions
  const suggestions = generateSuggestions({
    summary: {
      totalEvents: events.length,
      totalHours: Math.round(totalHours * 100) / 100,
      avgDailyHours: totalHours / periodDayCount,
      completionRate
    },
    categoryBreakdown,
    bestTimeSlots
  });
  
  return {
    period,
    dateRange: { start: startDate, end: endDate },
    summary: {
      totalEvents: events.length,
      totalHours: Math.round(totalHours * 100) / 100,
      avgDailyHours: Math.round((totalHours / periodDayCount) * 100) / 100,
      completionRate: Math.round(completionRate)
    },
    categoryBreakdown,
    bestTimeSlots,
    suggestions,
    events: events.slice(0, 10) // Include recent events
  };
}

/**
 * Get efficiency comparison data
 * @param {string} category - Category
 * @returns {Object} Comparison data
 */
function getEfficiencyComparison(category) {
  const analysis = analyzeCategory(category);
  const config = loadConfig();
  const categoryConfig = config.categories[category] || {};
  
  return {
    category,
    yourAvg: analysis.avgDuration,
    yourBest: analysis.bestDuration,
    globalAvg: categoryConfig.bestDuration || 1.5, // Default reference
    efficiency: analysis.efficiency
  };
}

module.exports = {
  analyzeCategory,
  analyzeTimeSlots,
  findBestTimeSlots,
  generateSuggestions,
  generateReport,
  getEfficiencyComparison,
  getTimeSlot,
  getTimeSlotName,
  getDurationHours,
  parseTimeToHours
};
