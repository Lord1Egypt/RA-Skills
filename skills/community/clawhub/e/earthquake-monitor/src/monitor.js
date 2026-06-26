/**
 * Earthquake Monitoring & Alert Module (v1.1.0)
 * - Fixed CWA data source integration
 * - Multi-language alert support
 * - Enhanced deduplication
 * - Webhook payload format support
 */

const { getCENCData, getCachedData: getCENCCached } = require('./cenc');
const { getCWAData, getCachedData: getCWACached } = require('./cwa');
const { getJMAData, getCachedData: getJMACached } = require('./jma');
const { calculateDistance } = require('./distance');
const { getConfig, setConfig } = require('./config');
const { formatAlertMessage, detectLang } = require('./i18n');

let monitorInterval = null;
let lastNotificationTime = 0;
const NOTIFICATION_COOLDOWN = 300000; // 5 minutes

// Track notified earthquake IDs (EventID level deduplication)
const notifiedEarthquakes = new Set();

/**
 * Generate unique earthquake ID
 */
function generateEarthquakeId(eq, source) {
  const time = eq.time || '';
  const mag = eq.magnitude || '0';
  const loc = eq.location || '';
  const depth = eq.depth || '0';
  return `${source}-${time}-${mag}-${loc}-${depth}`;
}

/**
 * Start earthquake monitoring
 * @param {Object} options - Configuration options
 * @param {Function} onAlert - Alert callback function
 * @param {number} interval - Check interval in ms (default 60000)
 */
async function startMonitor(options = {}, onAlert = null, interval = 60000) {
  const config = await getConfig();
  
  if (!config.notify.enabled) {
    return { success: false, message: 'Alerts disabled. Enable in config.' };
  }
  
  if (!config.location || !config.location.latitude) {
    return { success: false, message: 'Please set monitoring location first using init().' };
  }
  
  // Stop existing monitor if running
  if (monitorInterval) {
    stopMonitor();
  }
  
  console.log(`[Earthquake Monitor] Started: ${config.location.name}`);
  console.log(`[Earthquake Monitor] Alert: Within ${config.notify.distanceThreshold}km, Mag ${config.notify.minMagnitude}+`);
  console.log(`[Earthquake Monitor] Language: ${config.language}`);
  
  // Initial check
  await checkAndNotify(onAlert);
  
  // Set interval
  monitorInterval = setInterval(async () => {
    await checkAndNotify(onAlert);
  }, interval);
  
  return { 
    success: true, 
    message: `✅ Earthquake monitoring started!\n📍 Location: ${config.location.name}\n🔔 Alert: Within ${config.notify.distanceThreshold}km, Mag ${config.notify.minMagnitude}+\n⏰ Check interval: ${interval/1000}s\n🌐 Language: ${config.language}` 
  };
}

/**
 * Stop monitoring
 */
function stopMonitor() {
  if (monitorInterval) {
    clearInterval(monitorInterval);
    monitorInterval = null;
    console.log('[Earthquake Monitor] Stopped');
  }
  return { success: true, message: '✅ Monitoring stopped' };
}

/**
 * Check earthquakes and send notifications
 */
async function checkAndNotify(onAlert) {
  const config = await getConfig();
  if (!config.notify.enabled) return;
  
  try {
    // Fetch all data sources in parallel
    const [cencData, cwaData, jmaData] = await Promise.allSettled([
      config.sources.CENC !== false ? getCENCCached() : Promise.resolve([]),
      config.sources.CWA !== false ? getCWACached() : Promise.resolve(null),
      config.sources.JMA !== false ? getJMACached() : Promise.resolve([])
    ]);
    
    const earthquakes = [];
    const now = Date.now();
    
    // Process CENC data (China)
    if (cencData.status === 'fulfilled' && cencData.value.length > 0) {
      for (const eq of cencData.value) {
        const id = generateEarthquakeId({
          time: eq.time,
          magnitude: eq.magnitude,
          location: eq.location,
          depth: eq.depth
        }, 'CENC');
        
        if (!notifiedEarthquakes.has(id) && eq.time !== config.lastEarthquakeIds?.CENC) {
          earthquakes.push({
            source: 'CENC',
            sourceName: '中国地震台网',
            id,
            EventID: eq.EventID,
            time: eq.time,
            location: eq.location,
            magnitude: parseFloat(eq.magnitude),
            latitude: parseFloat(eq.latitude),
            longitude: parseFloat(eq.longitude),
            depth: parseFloat(eq.depth),
            intensity: eq.intensity
          });
        }
      }
    }
    
    // Process CWA data (Taiwan)
    if (cwaData.status === 'fulfilled' && cwaData.value && cwaData.value.ID) {
      const eq = cwaData.value;
      const id = generateEarthquakeId({
        time: eq.OriginTime,
        magnitude: eq.Magunitude,
        location: eq.HypoCenter,
        depth: eq.Depth
      }, 'CWA');
      
      if (!notifiedEarthquakes.has(id) && eq.OriginTime !== config.lastEarthquakeIds?.CWA) {
        earthquakes.push({
          source: 'CWA',
          sourceName: '台湾中央气象署',
          id,
          EventID: eq.ID,
          time: eq.OriginTime,
          location: eq.HypoCenter,
          magnitude: parseFloat(eq.Magunitude),
          latitude: parseFloat(eq.Latitude),
          longitude: parseFloat(eq.Longitude),
          depth: parseFloat(eq.Depth),
          intensity: eq.MaxIntensity
        });
      }
    }
    
    // Process JMA data (Japan)
    if (jmaData.status === 'fulfilled' && jmaData.value.length > 0) {
      for (const eq of jmaData.value) {
        const id = generateEarthquakeId({
          time: eq.time,
          magnitude: eq.magnitude,
          location: eq.location,
          depth: eq.depth
        }, 'JMA');
        
        if (!notifiedEarthquakes.has(id) && eq.time !== config.lastEarthquakeIds?.JMA) {
          earthquakes.push({
            source: 'JMA',
            sourceName: '日本气象厅',
            id,
            EventID: eq.EventID || eq.no,
            time: eq.time,
            location: eq.location,
            magnitude: parseFloat(eq.magnitude),
            latitude: parseFloat(eq.latitude),
            longitude: parseFloat(eq.longitude),
            depth: eq.depth,
            intensity: eq.shindo
          });
        }
      }
    }
    
    // No new earthquakes
    if (earthquakes.length === 0) return;
    
    // Sort by time
    earthquakes.sort((a, b) => new Date(b.time) - new Date(a.time));
    
    // Update last earthquake IDs
    const newConfig = { ...config };
    newConfig.lastEarthquakeIds = {
      CENC: earthquakes.find(e => e.source === 'CENC')?.EventID || config.lastEarthquakeIds?.CENC || '',
      CWA: earthquakes.find(e => e.source === 'CWA')?.EventID || config.lastEarthquakeIds?.CWA || '',
      JMA: earthquakes.find(e => e.source === 'JMA')?.EventID || config.lastEarthquakeIds?.JMA || ''
    };
    await setConfig(newConfig);
    
    // Filter by distance and magnitude
    const alerts = earthquakes.filter(eq => {
      const dist = calculateDistance(
        config.location.latitude,
        config.location.longitude,
        eq.latitude,
        eq.longitude
      );
      eq.distance = dist;
      return dist <= config.notify.distanceThreshold && 
             eq.magnitude >= config.notify.minMagnitude;
    });
    
    // Send notification
    if (alerts.length > 0 && now - lastNotificationTime > NOTIFICATION_COOLDOWN) {
      lastNotificationTime = now;
      
      // Add to notified set
      alerts.forEach(eq => notifiedEarthquakes.add(eq.id));
      
      // Get language for message formatting
      const lang = config.language || 'zh';
      const message = formatAlertMessage(alerts, config.location.name, lang);
      const webhookPayload = formatWebhookPayload(alerts, config.location.name);
      
      if (onAlert) {
        onAlert({ alerts, message, webhookPayload, lang });
      }
      
      console.log(`[Earthquake Monitor] Alert sent: ${alerts.length} earthquake(s)`);
    }
    
  } catch (e) {
    console.error('[Earthquake Monitor] Check failed:', e.message);
  }
}

/**
 * Format webhook payload for DingTalk/Feishu
 */
function formatWebhookPayload(earthquakes, locationName) {
  return {
    msgtype: 'news',
    news: {
      articles: [{
        title: `⚠️ Earthquake Alert - M${earthquakes[0]?.magnitude} near ${locationName}`,
        description: earthquakes.map((eq, i) => 
          `${i + 1}. ${eq.location} M${eq.magnitude} - ${Math.round(eq.distance)}km away`
        ).join('\n'),
        url: 'https://www.ceic.ac.cn/'
      }]
    }
  };
}

/**
 * Get monitoring status
 */
function getStatus() {
  return {
    isRunning: monitorInterval !== null,
    lastNotification: lastNotificationTime > 0 ? new Date(lastNotificationTime).toISOString() : null,
    notifiedCount: notifiedEarthquakes.size
  };
}

module.exports = {
  startMonitor,
  stopMonitor,
  checkAndNotify,
  getStatus
};
