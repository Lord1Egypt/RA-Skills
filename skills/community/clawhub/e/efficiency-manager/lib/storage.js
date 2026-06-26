/**
 * Storage Module - Local data persistence
 * 
 * 已修复：旧数据兼容性处理
 * - 处理缺失 startTime/endTime 的旧记录
 * - 处理使用 from/to/date 代替 startTime/endTime 的记录
 * - 处理使用 title 代替 description 的记录
 * - 处理使用中文 category 的记录
 */

const fs = require('fs');
const path = require('path');

// Simple UUID v4 generator (no external dependency)
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

const STORAGE_DIR = path.join(process.env.HOME, '.openclaw', 'efficiency-manager');
const DATA_DIR = path.join(STORAGE_DIR, 'data');
const EVENTS_FILE = path.join(DATA_DIR, 'events.json');
const CONFIG_FILE = path.join(STORAGE_DIR, 'config.json');

// Default categories with best durations (in hours)
const DEFAULT_CATEGORIES = {
  work: { name: '工作', bestDuration: 1.8 },
  study: { name: '学习', bestDuration: 1.0 },
  exercise: { name: '运动', bestDuration: 0.75 },
  social: { name: '社交', bestDuration: 1.5 },
  family: { name: '家庭', bestDuration: 1.5 },
  rest: { name: '休息', bestDuration: 0.5 },
  entertainment: { name: '娱乐', bestDuration: 1.2 },
  chores: { name: '家务', bestDuration: 1.0 },
  other: { name: '其他', bestDuration: 1.0 }
};

// 中文分类映射到标准分类
const CATEGORY_MAPPING = {
  '工作': 'work',
  '学习': 'study',
  '阅读': 'study',
  '运动': 'exercise',
  '健身': 'exercise',
  '社交': 'social',
  '朋友': 'social',
  '休息': 'rest',
  '睡觉': 'rest',
  '娱乐': 'entertainment',
  '游戏': 'entertainment',
  '家务': 'chores',
  '打扫': 'chores',
  '其他': 'other',
  '生活': 'other',
  '生活/采购': 'chores',
  '生活/清洁': 'chores',
  '休息/生活': 'rest',
  '资讯': 'entertainment',
  '资讯/休息': 'entertainment',
  '出行': 'other',
  '社交/生活': 'social',
  '家庭': 'family'
};

const DEFAULT_CONFIG = {
  dayStartTime: '06:00',
  dayEndTime: '23:00',
  reportTime: '22:00',
  categories: DEFAULT_CATEGORIES,
  benchmarkSource: 'local'
};

/**
 * Initialize storage directories and files
 */
function initStorage() {
  if (!fs.existsSync(STORAGE_DIR)) {
    fs.mkdirSync(STORAGE_DIR, { recursive: true });
  }
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(EVENTS_FILE)) {
    fs.writeFileSync(EVENTS_FILE, JSON.stringify([], null, 2));
  }
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2));
  }
}

/**
 * 标准化事件数据，处理旧数据格式
 * @param {Object} event - 原始事件数据
 * @returns {Object} 标准化后的事件数据
 */
function normalizeEvent(event) {
  if (!event || typeof event !== 'object') {
    return null;
  }

  const normalized = { ...event };

  // 处理 title -> description
  if (!normalized.description && normalized.title) {
    normalized.description = normalized.title;
  }

  // 处理中文分类 -> 标准分类
  if (normalized.category && CATEGORY_MAPPING[normalized.category]) {
    normalized.category = CATEGORY_MAPPING[normalized.category];
  }

  // 处理 from/to/date -> startTime/endTime
  if (!normalized.startTime && normalized.from && normalized.date) {
    // 处理 from 格式: "09:00" 或 "9:00"
    const time = normalized.from.padStart(5, '0');
    normalized.startTime = `${normalized.date}T${time}:00`;
  }

  if (!normalized.endTime && normalized.to && normalized.date) {
    const time = normalized.to.padStart(5, '0');
    normalized.endTime = `${normalized.date}T${time}:00`;
  }

  // 处理 durationMin -> duration
  if (normalized.durationMin && !normalized.duration) {
    normalized.duration = normalized.durationMin / 60;
  }

  // 处理 "2026-03-25 08:15" 格式（空格代替 T）
  if (normalized.startTime && normalized.startTime.includes(' ') && !normalized.startTime.includes('T')) {
    normalized.startTime = normalized.startTime.replace(' ', 'T');
  }
  if (normalized.endTime && normalized.endTime.includes(' ') && !normalized.endTime.includes('T')) {
    normalized.endTime = normalized.endTime.replace(' ', 'T');
  }

  // 确保有 id
  if (!normalized.id) {
    normalized.id = uuidv4();
  }

  // 确保有 status
  if (!normalized.status) {
    normalized.status = 'completed';
  }

  // 确保有 createdAt
  if (!normalized.createdAt) {
    normalized.createdAt = new Date().toISOString();
  }

  return normalized;
}

/**
 * 从事件中提取日期（处理各种格式）
 * @param {Object} event - 事件对象
 * @returns {string|null} 日期字符串 YYYY-MM-DD 或 null
 */
function getEventDate(event) {
  if (!event) return null;

  // 优先使用 startTime
  if (event.startTime) {
    const date = event.startTime.split('T')[0];
    if (date && date.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return date;
    }
  }

  // 使用 date 字段
  if (event.date && event.date.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return event.date;
  }

  // 使用 createdAt
  if (event.createdAt) {
    const date = event.createdAt.split('T')[0];
    if (date && date.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return date;
    }
  }

  return null;
}

/**
 * Load all events with optional query filters
 * @param {Object} query - Query filters
 * @param {string} query.category - Filter by category
 * @param {string} query.date - Filter by date (YYYY-MM-DD)
 * @param {string} query.startDate - Start date for range
 * @param {string} query.endDate - End date for range
 * @returns {Array} Filtered events
 */
function loadEvents(query = {}) {
  initStorage();
  try {
    const data = fs.readFileSync(EVENTS_FILE, 'utf8');
    let events = JSON.parse(data);

    // 标准化所有事件（处理旧数据格式）
    events = events.map(normalizeEvent).filter(e => e !== null);

    if (query.category) {
      // 同时匹配标准分类和中文分类
      const targetCategory = CATEGORY_MAPPING[query.category] || query.category;
      events = events.filter(e => e.category === targetCategory || e.category === query.category);
    }

    if (query.date) {
      const targetDate = query.date;
      events = events.filter(e => {
        const eventDate = getEventDate(e);
        return eventDate === targetDate;
      });
    }

    if (query.startDate && query.endDate) {
      events = events.filter(e => {
        const eventDate = getEventDate(e);
        return eventDate && eventDate >= query.startDate && eventDate <= query.endDate;
      });
    }

    return events.sort((a, b) => {
      const dateA = a.startTime || a.createdAt || '';
      const dateB = b.startTime || b.createdAt || '';
      return new Date(dateB) - new Date(dateA);
    });
  } catch (e) {
    console.error('Failed to load events:', e.message);
    return [];
  }
}

/**
 * Save an event (create or update)
 * @param {Object} eventData - Event data
 * @returns {Object} Saved event
 */
function saveEvent(eventData) {
  initStorage();
  const events = loadEvents();

  const now = new Date().toISOString();
  const event = {
    id: eventData.id || uuidv4(),
    description: eventData.description,
    category: eventData.category,
    startTime: eventData.startTime,
    endTime: eventData.endTime,
    status: eventData.status || 'completed',
    notes: eventData.notes || '',
    tags: eventData.tags || [],
    createdAt: eventData.createdAt || now,
    updatedAt: now
  };

  const existingIndex = events.findIndex(e => e.id === event.id);
  if (existingIndex >= 0) {
    events[existingIndex] = { ...events[existingIndex], ...event, updatedAt: now };
  } else {
    events.push(event);
  }

  fs.writeFileSync(EVENTS_FILE, JSON.stringify(events, null, 2));
  return event;
}

/**
 * Delete an event by ID
 * @param {string} id - Event ID
 * @returns {boolean} Success
 */
function deleteEvent(id) {
  initStorage();
  const events = loadEvents();
  const filtered = events.filter(e => e.id !== id);

  if (filtered.length === events.length) {
    return false;
  }

  fs.writeFileSync(EVENTS_FILE, JSON.stringify(filtered, null, 2));
  return true;
}

/**
 * Delete all events
 */
function deleteAllEvents() {
  initStorage();
  fs.writeFileSync(EVENTS_FILE, JSON.stringify([], null, 2));
}

/**
 * Load user configuration
 * @returns {Object} User config
 */
function loadConfig() {
  initStorage();
  try {
    const data = fs.readFileSync(CONFIG_FILE, 'utf8');
    const parsed = JSON.parse(data);

    return {
      ...DEFAULT_CONFIG,
      ...parsed,
      categories: {
        ...DEFAULT_CATEGORIES,
        ...(parsed.categories || {})
      }
    };
  } catch (e) {
    return DEFAULT_CONFIG;
  }
}

/**
 * Save user configuration
 * @param {Object} config - Config to save
 */
function saveConfig(config) {
  initStorage();
  const current = loadConfig();
  const merged = { ...current, ...config };
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(merged, null, 2));
}

/**
 * Get event by ID
 * @param {string} id - Event ID
 * @returns {Object|null} Event
 */
function getEventById(id) {
  const events = loadEvents();
  return events.find(e => e.id === id) || null;
}

/**
 * Get events by date range
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Array} Events
 */
function getEventsByDateRange(startDate, endDate) {
  return loadEvents({ startDate, endDate });
}

/**
 * Get dates that have events (for a month)
 * @param {number} year - Year
 * @param {number} month - Month (1-12)
 * @returns {Array} Dates with events
 */
function getEventDates(year, month) {
  const startDate = `${year}-${String(month).padStart(2, '0')}-01`;
  const endDate = `${year}-${String(month).padStart(2, '0')}-31`;
  const events = getEventsByDateRange(startDate, endDate);
  const dates = [...new Set(events.map(e => getEventDate(e)).filter(d => d))];
  return dates.sort();
}

module.exports = {
  initStorage,
  loadEvents,
  saveEvent,
  deleteEvent,
  deleteAllEvents,
  loadConfig,
  saveConfig,
  getEventById,
  getEventsByDateRange,
  getEventDates,
  normalizeEvent,
  getEventDate,
  DEFAULT_CATEGORIES,
  DEFAULT_CONFIG
};
