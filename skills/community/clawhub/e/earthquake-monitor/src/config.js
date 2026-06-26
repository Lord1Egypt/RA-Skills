/**
 * Configuration Management Module (v1.1.1)
 * - Enhanced location fuzzy matching (supports pinyin, abbreviations)
 * - Note: Encryption removed for ClawHub compatibility
 */

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');

// Default configuration
const DEFAULT_CONFIG = {
  initialized: false,
  location: {
    name: '大理',
    latitude: 25.6069,
    longitude: 100.2679
  },
  notify: {
    distanceThreshold: 300,
    minMagnitude: 3.0,
    enabled: true
  },
  language: 'zh', // Default language (zh/en/ja)
  sources: {
    CENC: true,
    JMA: true,
    CWA: true
  },
  webhook: null,
  lastEarthquakeIds: {
    CENC: '',
    CWA: '',
    JMA: ''
  }
};

// City coordinates with pinyin and abbreviations
const CITY_COORDINATES = {
  '大理': { name: '大理', pinyin: ['dali', 'dl'], abbr: 'DL', latitude: 25.6069, longitude: 100.2679 },
  '昆明': { name: '昆明', pinyin: ['kunming', 'km'], abbr: 'KM', latitude: 25.04, longitude: 102.71 },
  '丽江': { name: '丽江', pinyin: ['lijiang', 'lj'], abbr: 'LJ', latitude: 26.87, longitude: 100.23 },
  '北京': { name: '北京', pinyin: ['beijing', 'bj'], abbr: 'BJ', latitude: 39.90, longitude: 116.40 },
  '上海': { name: '上海', pinyin: ['shanghai', 'sh'], abbr: 'SH', latitude: 31.23, longitude: 121.47 },
  '广州': { name: '广州', pinyin: ['guangzhou', 'gz'], abbr: 'GZ', latitude: 23.12, longitude: 113.26 },
  '深圳': { name: '深圳', pinyin: ['shenzhen', 'sz'], abbr: 'SZ', latitude: 22.54, longitude: 114.06 },
  '成都': { name: '成都', pinyin: ['chengdu', 'cd'], abbr: 'CD', latitude: 30.57, longitude: 104.07 },
  '重庆': { name: '重庆', pinyin: ['chongqing', 'cq'], abbr: 'CQ', latitude: 29.55, longitude: 106.55 },
  '杭州': { name: '杭州', pinyin: ['hangzhou', 'hz'], abbr: 'HZ', latitude: 30.27, longitude: 120.15 },
  '西安': { name: '西安', pinyin: ['xian', 'xa'], abbr: 'XA', latitude: 34.27, longitude: 108.95 },
  '南京': { name: '南京', pinyin: ['nanjing', 'nj'], abbr: 'NJ', latitude: 32.06, longitude: 118.78 },
  '武汉': { name: '武汉', pinyin: ['wuhan', 'wh'], abbr: 'WH', latitude: 30.58, longitude: 114.29 },
  '台北': { name: '台北', pinyin: ['taipei', 'tb'], abbr: 'TB', latitude: 25.03, longitude: 121.56 },
  '东京': { name: '东京', pinyin: ['tokyo', 'dj'], abbr: 'DJ', latitude: 35.68, longitude: 139.69 },
  '大阪': { name: '大阪', pinyin: ['osaka', 'db'], abbr: 'DB', latitude: 34.69, longitude: 135.50 },
  '首尔': { name: '首尔', pinyin: ['seoul', 'se'], abbr: 'SE', latitude: 37.57, longitude: 126.98 },
  '香港': { name: '香港', pinyin: ['hongkong', 'hk'], abbr: 'HK', latitude: 22.32, longitude: 114.17 },
  '三亚': { name: '三亚', pinyin: ['sanya', 'sy'], abbr: 'SY', latitude: 18.25, longitude: 109.51 },
  '青岛': { name: '青岛', pinyin: ['qingdao', 'qd'], abbr: 'QD', latitude: 36.07, longitude: 120.37 }
};

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (e) {
    console.error('[Config] Load error:', e.message);
  }
  return { ...DEFAULT_CONFIG };
}

function saveConfig(config) {
  try {
    const dir = path.dirname(CONFIG_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
    return true;
  } catch (e) {
    console.error('[Config] Save error:', e.message);
    return false;
  }
}

/**
 * Enhanced location parsing with pinyin and abbreviation support
 */
function parseLocation(cityName) {
  if (!cityName) return null;
  const normalized = cityName.trim().toLowerCase();
  
  // Direct match
  if (CITY_COORDINATES[normalized]) {
    const city = CITY_COORDINATES[normalized];
    return { name: city.name, latitude: city.latitude, longitude: city.longitude };
  }
  
  // Search by pinyin or abbreviation
  for (const [name, city] of Object.entries(CITY_COORDINATES)) {
    // Match pinyin
    if (city.pinyin.some(py => py.toLowerCase() === normalized)) {
      return { name: city.name, latitude: city.latitude, longitude: city.longitude };
    }
    // Match abbreviation
    if (city.abbr.toLowerCase() === normalized) {
      return { name: city.name, latitude: city.latitude, longitude: city.longitude };
    }
    // Partial match (contains)
    if (city.pinyin.some(py => py.toLowerCase().includes(normalized)) || 
        normalized.includes(city.name.toLowerCase())) {
      return { name: city.name, latitude: city.latitude, longitude: city.longitude };
    }
    // Chinese character partial match
    if (name.includes(normalized) || normalized.includes(name)) {
      return { name: city.name, latitude: city.latitude, longitude: city.longitude };
    }
  }
  
  // Try to parse as coordinates directly
  const coords = normalized.match(/^([-\d.]+)[,\s]+([-\d.]+)$/);
  if (coords) {
    const lat = parseFloat(coords[1]);
    const lon = parseFloat(coords[2]);
    if (isValidCoordinates(lat, lon)) {
      return { name: `${lat.toFixed(2)},${lon.toFixed(2)}`, latitude: lat, longitude: lon };
    }
  }
  
  return null;
}

function isValidCoordinates(lat, lon) {
  return lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180 && !isNaN(lat) && !isNaN(lon);
}

async function getConfig() {
  return loadConfig();
}

async function setConfig(newConfig) {
  const config = loadConfig();
  
  if (newConfig.location) {
    if (typeof newConfig.location === 'string') {
      const parsed = parseLocation(newConfig.location);
      if (parsed) config.location = parsed;
    } else if (newConfig.location.latitude && newConfig.location.longitude) {
      if (isValidCoordinates(newConfig.location.latitude, newConfig.location.longitude)) {
        config.location = {
          name: newConfig.location.name || config.location.name,
          latitude: newConfig.location.latitude,
          longitude: newConfig.location.longitude
        };
      }
    }
  }
  
  if (newConfig.notify) {
    config.notify = { ...config.notify, ...newConfig.notify };
  }
  
  if (newConfig.language && ['zh', 'en', 'ja'].includes(newConfig.language)) {
    config.language = newConfig.language;
  }
  
  if (newConfig.sources) {
    config.sources = { ...config.sources, ...newConfig.sources };
  }
  
  if (newConfig.webhook !== undefined) {
    config.webhook = newConfig.webhook;
  }
  
  config.initialized = true;
  saveConfig(config);
  return config;
}

async function initConfig(options = {}) {
  const config = loadConfig();
  
  // Set location
  if (options.location) {
    if (typeof options.location === 'string') {
      const parsed = parseLocation(options.location);
      if (parsed) config.location = parsed;
    } else if (options.location.latitude && options.location.longitude) {
      if (isValidCoordinates(options.location.latitude, options.location.longitude)) {
        config.location = {
          name: options.location.name || '',
          latitude: options.location.latitude,
          longitude: options.location.longitude
        };
      }
    }
  } else {
    config.location = { name: '大理', latitude: 25.6069, longitude: 100.2679 };
  }
  
  if (options.distanceThreshold) config.notify.distanceThreshold = options.distanceThreshold;
  if (options.minMagnitude) config.notify.minMagnitude = options.minMagnitude;
  if (options.language && ['zh', 'en', 'ja'].includes(options.language)) {
    config.language = options.language;
  }
  if (options.sources) {
    config.sources = { ...config.sources, ...options.sources };
  }
  
  config.notify.enabled = true;
  config.initialized = true;
  
  saveConfig(config);
  return config;
}

async function updateLastIds(ids) {
  const config = loadConfig();
  config.lastEarthquakeIds = { ...config.lastEarthquakeIds, ...ids };
  saveConfig(config);
}

module.exports = {
  getConfig,
  setConfig,
  initConfig,
  updateLastIds,
  parseLocation,
  isValidCoordinates,
  CITY_COORDINATES,
  DEFAULT_CONFIG
};
