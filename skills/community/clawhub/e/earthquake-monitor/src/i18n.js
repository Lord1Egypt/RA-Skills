/**
 * Internationalization (i18n) Module
 * Multi-language support for earthquake alerts
 */

const translations = {
  zh: {
    alertTitle: '⚠️ 地震预警提醒！',
    alertSubtitle: '📍 震中距离 {location} 较近：\n',
    magnitude: '震级',
    location: '震源',
    distance: '距离约',
    time: '时间',
    depth: '震源深度',
    source: '来源',
    safetyNotice: '请注意安全！',
    noEarthquake: '暂无地震信息',
    monitoring: '监控中',
    lastCheck: '最后检查',
    unit: {
      km: 'km',
      magnitude: '级'
    }
  },
  en: {
    alertTitle: '⚠️ Earthquake Alert!',
    alertSubtitle: '📍 Epicenter near {location}:\n',
    magnitude: 'Magnitude',
    location: 'Location',
    distance: 'Distance',
    time: 'Time',
    depth: 'Depth',
    source: 'Source',
    safetyNotice: 'Please stay safe!',
    noEarthquake: 'No earthquake information',
    monitoring: 'Monitoring',
    lastCheck: 'Last check',
    unit: {
      km: 'km',
      magnitude: ''
    }
  },
  ja: {
    alertTitle: '⚠️ 地震アラート！',
    alertSubtitle: '📍 震源地が {location} の近く:\n',
    magnitude: 'マグニチュード',
    location: '場所',
    distance: '距離',
    time: '時刻',
    depth: '震源深度',
    source: '情報源',
    safetyNotice: '安全にお気をつけて！',
    noEarthquake: '地震情報なし',
    monitoring: '監視中',
    lastCheck: '最終確認',
    unit: {
      km: 'km',
      magnitude: ''
    }
  }
};

// Language detection based on source
const sourceLangMap = {
  'CENC': 'zh',
  '中国地震台网': 'zh',
  '台湾中央气象署': 'zh',
  'CWA': 'zh',
  'JMA': 'ja',
  '日本气象厅': 'ja'
};

/**
 * Get translation for a key
 * @param {string} lang - Language code (zh/en/ja)
 * @param {string} key - Translation key
 * @param {Object} params - Parameters for placeholder replacement
 */
function t(lang, key, params = {}) {
  const langData = translations[lang] || translations.zh;
  let text = langData[key] || translations.zh[key] || key;
  
  // Replace placeholders like {location}
  for (const [param, value] of Object.entries(params)) {
    text = text.replace(new RegExp(`\\{${param}\\}`, 'g'), value);
  }
  
  return text;
}

/**
 * Detect language based on earthquake source
 * @param {string} source - Data source name
 */
function detectLang(source) {
  return sourceLangMap[source] || 'zh';
}

/**
 * Format alert message in specific language
 * @param {Array} earthquakes - Array of earthquake objects
 * @param {string} locationName - Location name
 * @param {string} lang - Language code
 */
function formatAlertMessage(earthquakes, locationName, lang = 'zh') {
  const lines = [t(lang, 'alertTitle')];
  lines.push(t(lang, 'alertSubtitle', { location: locationName }), '');
  
  earthquakes.forEach((eq, i) => {
    const emoji = eq.magnitude >= 5 ? '🔴' : eq.magnitude >= 4 ? '🟠' : '🟡';
    const eqLang = detectLang(eq.sourceName || eq.source);
    const units = translations[eqLang]?.unit || translations.zh.unit;
    
    lines.push(`${i + 1}. ${emoji} M${eq.magnitude}${units.magnitude} [${eq.sourceName || eq.source}]`);
    lines.push(`   📍 ${eq.location}`);
    lines.push(`   📏 ${t(eqLang, 'distance')}: ${Math.round(eq.distance)}${units.km}`);
    lines.push(`   ⏰ ${eq.time}`);
    if (eq.depth) lines.push(`   📊 ${t(eqLang, 'depth')}: ${eq.depth}${units.km}`);
    lines.push('');
  });
  
  lines.push(t(lang, 'safetyNotice'));
  return lines.join('\n');
}

module.exports = { t, detectLang, formatAlertMessage, translations };
