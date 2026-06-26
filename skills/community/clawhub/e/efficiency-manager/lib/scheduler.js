/**
 * Scheduler Module - Smart event scheduling
 */

const { loadEvents, loadConfig } = require('../lib/storage');
const { getTimeSlot, getTimeSlotName, analyzeCategory, findBestTimeSlots } = require('../lib/analyzer');

/**
 * Parse duration string to hours
 * @param {string} durationStr - Duration like "2h", "1.5h", "90m"
 * @returns {number} Hours
 */
function parseDuration(durationStr) {
  const str = durationStr.toLowerCase().trim();
  
  if (str.endsWith('h')) {
    return parseFloat(str.slice(0, -1));
  }
  
  if (str.endsWith('m') || str.endsWith('min')) {
    const mins = parseInt(str);
    return mins / 60;
  }
  
  // Try as plain number (assume hours)
  return parseFloat(str) || 1;
}

/**
 * Estimate category from description
 * @param {string} description - Event description
 * @returns {string} Estimated category
 */
function estimateCategory(description) {
  const desc = description.toLowerCase();
  
  const keywords = {
    work: ['工作', '写代码', '写文档', '开会', '办公', '代码', 'project', 'task'],
    study: ['学习', '读书', '看书', '课程', '学习', 'study', 'read'],
    exercise: ['运动', '跑步', '健身', '锻炼', '瑜伽', 'exercise', 'run', 'gym'],
    social: ['社交', '聚会', '聊天', '会友', 'social', 'meet'],
    family: ['家庭', '家人', '亲子', '陪娃', 'family'],
    entertainment: ['娱乐', '游戏', '电影', '视频', '看剧', 'game', 'movie'],
    chores: ['家务', '做饭', '购物', '清洁', 'chores', 'cook', 'shop'],
    rest: ['休息', '睡觉', '午休', 'break', 'sleep']
  };
  
  for (const [cat, words] of Object.entries(keywords)) {
    if (words.some(w => desc.includes(w))) {
      return cat;
    }
  }
  
  return 'other';
}

/**
 * Parse task string to event object
 * @param {string} taskStr - Task string like "写代码2h"
 * @returns {Object} Parsed task
 */
function parseTaskString(taskStr) {
  // Try to extract duration
  const durationMatch = taskStr.match(/(\d+\.?\d*)(h|hour|m|min)?/i);
  const duration = durationMatch ? parseDuration(durationMatch[0]) : 1;
  
  // Remove duration from description
  const description = taskStr.replace(durationMatch ? durationMatch[0] : '', '').trim() || taskStr;
  
  // Estimate category
  const category = estimateCategory(description);
  
  return {
    description,
    category,
    duration,
    notes: ''
  };
}

/**
 * Get optimal time slots for a category
 * @param {string} category - Category
 * @returns {Array} Preferred slots in order
 */
function getPreferredSlots(category) {
  const bestSlots = findBestTimeSlots(loadEvents());
  const categoryBest = bestSlots.filter(b => b.category === category);
  
  if (categoryBest.length > 0) {
    return categoryBest.map(b => b.slot);
  }
  
  // Default preferences based on category
  const defaults = {
    work: ['morning', 'afternoon'],
    study: ['morning', 'afternoon'],
    exercise: ['morning', 'evening'],
    social: ['evening', 'afternoon'],
    family: ['evening', 'afternoon'],
    entertainment: ['evening', 'night'],
    chores: ['morning', 'afternoon'],
    rest: ['night', 'afternoon'],
    other: ['afternoon', 'evening']
  };
  
  return defaults[category] || ['afternoon'];
}

/**
 * Get next available time slot
 * @param {string} fromTime - Start from time (HH:MM)
 * @param {number} durationHours - Duration in hours
 * @param {string} preferredSlot - Preferred slot
 * @returns {Object} Scheduled time
 */
function getNextSlot(fromTime, durationHours, preferredSlot) {
  const config = loadConfig();
  const dayStart = config.dayStartTime || '06:00';
  const dayEnd = config.dayEndTime || '23:00';
  
  let [hours, minutes] = (fromTime || dayStart).split(':').map(Number);
  
  // Convert to minutes from midnight
  let currentMinutes = hours * 60 + minutes;
  const durationMinutes = durationHours * 60;
  const endMinutes = parseInt(dayEnd.split(':')[0]) * 60;
  
  // Simple scheduling: just return the start time
  return {
    startTime: `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`,
    endTime: calculateEndTime(hours, minutes, durationMinutes)
  };
}

/**
 * Calculate end time
 * @param {number} hours - Start hours
 * @param {number} minutes - Start minutes
 * @param {number} durationMinutes - Duration in minutes
 * @returns {string} End time (HH:MM)
 */
function calculateEndTime(hours, minutes, durationMinutes) {
  const totalMinutes = hours * 60 + minutes + durationMinutes;
  const endHours = Math.floor(totalMinutes / 60) % 24;
  const endMinutes = totalMinutes % 60;
  return `${String(endHours).padStart(2, '0')}:${String(endMinutes).padStart(2, '0')}`;
}

/**
 * Schedule multiple tasks
 * @param {Array} tasks - Array of task objects or strings
 * @param {Object} options - Scheduling options
 * @returns {Object} Schedule result
 */
function scheduleTasks(tasks, options = {}) {
  const config = loadConfig();
  const dayStart = config.dayStartTime || '06:00';
  
  // Parse tasks if they're strings
  const parsedTasks = tasks.map(t => {
    if (typeof t === 'string') {
      return parseTaskString(t);
    }
    return t;
  });
  
  const schedule = [];
  let currentTime = dayStart;
  const categoryDistribution = {};
  const warnings = [];
  
  parsedTasks.forEach((task, index) => {
    const preferredSlots = getPreferredSlots(task.category);
    
    // For simplicity, just use current time
    const slot = getNextSlot(currentTime, task.duration, preferredSlots[0]);
    
    const scheduledItem = {
      event: {
        description: task.description,
        category: task.category,
        duration: task.duration
      },
      startTime: slot.startTime,
      endTime: slot.endTime,
      reason: getScheduleReason(task.category, preferredSlots)
    };
    
    schedule.push(scheduledItem);
    
    // Track distribution
    categoryDistribution[task.category] = (categoryDistribution[task.category] || 0) + task.duration;
    
    // Move current time
    currentTime = slot.endTime;
  });
  
  const totalDuration = parsedTasks.reduce((sum, t) => sum + t.duration, 0);
  
  // Check if schedule exceeds day end
  const [lastEndHour] = schedule[schedule.length - 1]?.endTime.split(':').map(Number) || [0];
  if (lastEndHour > parseInt(config.dayEndTime?.split(':')[0] || 23)) {
    warnings.push('建议的任务安排可能超出您的正常工作时段，请适当调整。');
  }
  
  return {
    schedule,
    totalDuration: Math.round(totalDuration * 100) / 100,
    categoryDistribution,
    warnings
  };
}

/**
 * Get reason for schedule decision
 * @param {string} category - Task category
 * @param {Array} preferredSlots - Preferred time slots
 * @returns {string} Reason
 */
function getScheduleReason(category, preferredSlots) {
  const slotName = preferredSlots[0] ? getTimeSlotName(preferredSlots[0]) : '下午';
  
  const reasons = {
    work: `根据您的历史数据，工作任务安排在${slotName}效率最高`,
    study: `学习任务在${slotName}时段更容易保持专注`,
    exercise: `运动安排在${slotName}有助于保持体能`,
    social: `社交活动适合安排在${slotName}`,
    family: `家庭相关事项安排在${slotName}通常更稳妥`,
    entertainment: `娱乐时间建议安排在${slotName}作为放松`,
    chores: `家务事建议在${slotName}集中处理`,
    rest: `休息安排在${slotName}最为合适`
  };
  
  return reasons[category] || `该任务安排在${slotName}时段`;
}

/**
 * Optimize existing schedule
 * @param {Array} events - Existing events
 * @returns {Object} Optimization suggestions
 */
function optimizeSchedule(events) {
  const bestSlots = findBestTimeSlots(events);
  const suggestions = [];
  
  events.forEach(event => {
    const best = bestSlots.find(b => b.category === event.category);
    if (best) {
      const currentSlot = getTimeSlot(event.startTime);
      if (currentSlot !== best.slot) {
        suggestions.push({
          eventId: event.id,
          description: event.description,
          current: getTimeSlotName(currentSlot),
          recommended: best.slotName,
          reason: `在${best.slotName}进行此类活动效率更高`
        });
      }
    }
  });
  
  return {
    suggestions,
    count: suggestions.length
  };
}

module.exports = {
  scheduleTasks,
  parseTaskString,
  estimateCategory,
  getPreferredSlots,
  optimizeSchedule,
  parseDuration
};
