/**
 * Earthquake Monitor - Main Entry (v1.1.0)
 * Real-time earthquake monitoring for China, Taiwan, and Japan
 * 
 * v1.1.0 Updates:
 * - Multi-language support (zh/en/ja)
 * - Enhanced location fuzzy matching (pinyin, abbreviations)
 * - Secure webhook storage
 * - Shared cache for performance
 */

const { getCENCData } = require('./src/cenc');
const { getCWAData } = require('./src/cwa');
const { getJMAData } = require('./src/jma');
const { calculateDistance } = require('./src/distance');
const { getConfig, setConfig, initConfig, parseLocation, CITY_COORDINATES } = require('./src/config');
const { startMonitor, stopMonitor, getStatus } = require('./src/monitor');
const { formatAlertMessage, detectLang } = require('./src/i18n');

/**
 * Normalize earthquake data from different sources
 */
function normalize(data, source) {
  if (!data || (Array.isArray(data) && data.length === 0)) return [];
  
  const items = Array.isArray(data) ? data : [data];
  
  return items.map(eq => {
    const normalized = {
      source,
      time: '',
      location: '',
      magnitude: 0,
      latitude: 0,
      longitude: 0,
      depth: 0,
      intensity: ''
    };
    
    if (source === 'CENC') {
      normalized.time = eq.time;
      normalized.location = eq.location || eq.placeName;
      normalized.magnitude = parseFloat(eq.magnitude);
      normalized.latitude = parseFloat(eq.latitude);
      normalized.longitude = parseFloat(eq.longitude);
      normalized.depth = parseFloat(eq.depth);
      normalized.intensity = eq.intensity;
      normalized.id = eq.EventID;
    } else if (source === 'CWA') {
      normalized.time = eq.OriginTime;
      normalized.location = eq.HypoCenter;
      normalized.magnitude = parseFloat(eq.Magunitude);
      normalized.latitude = parseFloat(eq.Latitude);
      normalized.longitude = parseFloat(eq.Longitude);
      normalized.depth = parseFloat(eq.Depth);
      normalized.intensity = eq.MaxIntensity;
      normalized.id = eq.ID;
      normalized.isWarning = true;
    } else if (source === 'JMA') {
      normalized.time = eq.time;
      normalized.location = eq.location;
      normalized.magnitude = parseFloat(eq.magnitude);
      normalized.latitude = parseFloat(eq.latitude);
      normalized.longitude = parseFloat(eq.longitude);
      normalized.depth = eq.depth;
      normalized.intensity = eq.shindo;
      normalized.id = eq.EventID || eq.no;
    }
    
    return normalized;
  });
}

/**
 * Initialize skill configuration
 * @param {Object} options - Configuration options
 * @param {string|Object} options.location - City name or coordinates
 * @param {number} [options.distanceThreshold=300] - Alert distance (km)
 * @param {number} [options.minMagnitude=3.0] - Minimum magnitude
 * @param {string} [options.language='zh'] - Language (zh/en/ja)
 * @param {Object} [options.sources] - Data source toggle {CENC: true, JMA: true, CWA: true}
 */
async function init(options = {}) {
  const config = await initConfig(options);
  
  let locationInfo = '';
  if (config.location && config.location.name) {
    locationInfo = `\n📍 Location: ${config.location.name} (${config.location.latitude}, ${config.location.longitude})`;
  }
  
  const langNames = { zh: '中文', en: 'English', ja: '日本語' };
  
  return {
    success: true,
    message: `✅ Earthquake Monitor initialized!\n🔔 Alert: Within ${config.notify.distanceThreshold}km, Mag ${config.notify.minMagnitude}+\n🌐 Language: ${langNames[config.language] || config.language}${locationInfo}\n\nUsage:\n- "earthquake" / "getAll()" - Get latest earthquakes\n- "getCENC()" - China earthquake data\n- "getJMA()" - Japan earthquake data\n- "getCWA()" - Taiwan earthquake data\n- "start()" - Start proactive monitoring\n- "config()" - View/modify configuration\n- "cities()" - List supported cities`,
    config
  };
}

/**
 * Get CENC (China) earthquake data
 */
async function getCENC(limit = 10) {
  const data = await getCENCData();
  return {
    source: 'CENC',
    sourceName: '中国地震台网',
    count: data.length,
    earthquakes: normalize(data, 'CENC').slice(0, limit)
  };
}

/**
 * Get CWA (Taiwan) earthquake early warning data
 */
async function getCWA() {
  const data = await getCWAData();
  if (!data) {
    return { source: 'CWA', sourceName: '台湾中央气象署', count: 0, earthquakes: [] };
  }
  return {
    source: 'CWA',
    sourceName: '台湾中央气象署',
    count: 1,
    earthquakes: normalize([data], 'CWA'),
    isWarning: true
  };
}

/**
 * Get JMA (Japan) earthquake data
 */
async function getJMA(limit = 10) {
  const data = await getJMAData();
  return {
    source: 'JMA',
    sourceName: '日本气象厅',
    count: data.length,
    earthquakes: normalize(data, 'JMA').slice(0, limit)
  };
}

/**
 * Get all earthquake data from all sources
 * @param {Object} options - Query options
 * @param {number} [options.limit=5] - Results per source
 * @param {boolean} [options.checkMyLocation=true] - Check if affecting monitored location
 */
async function getAll(options = {}) {
  const { limit = 5, checkMyLocation = true } = options;
  
  const [cenc, cwa, jma] = await Promise.allSettled([
    getCENC(limit),
    getCWA(),
    getJMA(limit)
  ]);
  
  const results = { timestamp: new Date().toISOString(), sources: [] };
  
  if (cenc.status === 'fulfilled') results.sources.push(cenc.value);
  if (cwa.status === 'fulfilled' && cwa.value.count > 0) results.sources.push(cwa.value);
  if (jma.status === 'fulfilled') results.sources.push(jma.value);
  
  // Merge all earthquakes
  const allEarthquakes = results.sources
    .flatMap(s => s.earthquakes.map(eq => ({...eq, sourceName: s.sourceName})))
    .sort((a, b) => new Date(b.time) - new Date(a.time))
    .slice(0, 15);
  
  results.earthquakes = allEarthquakes;
  results.totalCount = allEarthquakes.length;
  
  // Check if affecting monitored location
  if (checkMyLocation) {
    const config = await getConfig();
    if (config.location && config.notify.enabled) {
      const lang = config.language || 'zh';
      
      const nearby = allEarthquakes.filter(eq => {
        const dist = calculateDistance(
          config.location.latitude, config.location.longitude,
          eq.latitude, eq.longitude
        );
        eq.distance = dist;
        return dist <= config.notify.distanceThreshold && eq.magnitude >= config.notify.minMagnitude;
      });
      
      results.nearbyEarthquakes = nearby;
      results.hasAlert = nearby.length > 0;
      if (nearby.length > 0) {
        results.alertMessage = formatAlertMessage(nearby, config.location.name, lang);
      }
    }
  }
  
  return results;
}

/**
 * List supported cities
 */
async function cities() {
  const cityList = Object.entries(CITY_COORDINATES).map(([name, data]) => ({
    name,
    pinyin: data.pinyin.join(', '),
    abbr: data.abbr,
    latitude: data.latitude,
    longitude: data.longitude
  }));
  
  return {
    count: cityList.length,
    cities: cityList
  };
}

/**
 * Start proactive monitoring
 * @param {Object} options - Monitoring options
 * @param {number} [options.interval=60000] - Check interval in ms
 */
async function start(options = {}) {
  return await startMonitor(options);
}

/**
 * Stop monitoring
 */
async function stop() {
  return stopMonitor();
}

/**
 * Get/set configuration
 * @param {Object} [newConfig] - New configuration
 */
async function config(newConfig = null) {
  if (newConfig) {
    // Support location string for convenience
    if (typeof newConfig.location === 'string') {
      const parsed = parseLocation(newConfig.location);
      if (parsed) {
        newConfig.location = parsed;
      }
    }
    const config = await setConfig(newConfig);
    return { success: true, message: '✅ Configuration updated', config };
  }
  return await getConfig();
}

/**
 * Get monitoring status
 */
async function status() {
  return getStatus();
}

/**
 * Legacy alias for backward compatibility
 */
const getAllEarthquakes = getAll;

module.exports = {
  init,
  getCENC,
  getCWA,
  getJMA,
  getAll,
  getAllEarthquakes, // Legacy alias
  cities,
  start,
  stop,
  config,
  status,
  parseLocation, // Export for advanced usage
  CITY_COORDINATES // Export city list
};
