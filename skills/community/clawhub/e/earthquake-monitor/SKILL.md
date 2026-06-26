---
name: earthquake-monitor
description: "🌋 Real-time earthquake monitoring for China, Taiwan, and Japan. CENC/CWA/JMA data with proactive alerting. v1.1.1 - Multi-language (zh/en/ja), pinyin location matching, optimized cache"
homepage: https://github.com/fungjcode/earthquake-monitor
metadata:
  openclaw:
    emoji: "🌋"
    requires:
      bins: ["curl"]
      node: ">=18"
---

# 🌋 Earthquake Monitor v1.1.1

Real-time earthquake monitoring for China (CENC), Taiwan (CWA), and Japan (JMA) with proactive alerting.

## v1.1.1 Changelog

### v1.1.1 (Security Fix)
- 🔒 **Security Update** - Removed encryption for ClawHub compatibility
- 📝 Added SECURITY.md documentation

### v1.1.0 Features
- 🌍 **Multi-language Support** - Alert messages in Chinese, English, and Japanese
- 📍 **Location Fuzzy Matching** - Supports pinyin (dali), abbreviations (DL), partial match (da)
- ⚡ **Performance Optimization** - Shared cache module with auto-cleanup
- ✅ **Fixed** Taiwan (CWA) data source integration
- ✅ **Improved** notification deduplication logic

---

## Quick Start

```javascript
// Initialize monitoring
await init({ location: "大理" })

// Get latest earthquakes
await getAll()

// Start proactive monitoring
await start()
```

---

## Data Sources

| Source | Region | Language (Alert) | Description |
|--------|--------|------------------|-------------|
| CENC | 🇨🇳 China | 中文 | China Earthquake Networks Center |
| CWA | 🇹🇼 Taiwan | 中文 | Central Weather Administration |
| JMA | 🇯🇵 Japan | 日本語 | Japan Meteorological Agency |

---

## API Reference

### init(options)
Initialize configuration.

```javascript
await init({
  location: "dali",           // City name (supports pinyin, abbreviations)
  distanceThreshold: 300,     // Alert distance in km
  minMagnitude: 3.0,         // Minimum magnitude
  language: 'zh',            // Language: zh/en/ja
  sources: {                // Toggle data sources
    CENC: true,
    JMA: true,
    CWA: true
  }
})
```

### getAll(options)
Get earthquakes from all sources.

```javascript
const result = await getAll({ limit: 5 })
// Returns: { earthquakes, totalCount, nearbyEarthquakes, hasAlert, alertMessage }
```

### getCENC(limit)
Get China earthquake data.

```javascript
const { earthquakes } = await getCENC(10)
```

### getJMA(limit)
Get Japan earthquake data.

```javascript
const { earthquakes } = await getJMA(10)
```

### getCWA()
Get Taiwan earthquake early warning data.

```javascript
const { earthquakes, isWarning } = await getCWA()
```

### start(options)
Start proactive monitoring with auto-alerts.

```javascript
await start({ interval: 60000 })  // Check every 60 seconds
```

### stop()
Stop monitoring.

```javascript
await stop()
```

### config(newConfig)
View or update configuration.

```javascript
// View
const cfg = await config()

// Update
await config({ language: 'en', minMagnitude: 4.0 })
```

### cities()
List all supported cities with coordinates.

```javascript
const { cities } = await cities()
```

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| location | string/object | 大理 | City name or {name, latitude, longitude} |
| distanceThreshold | number | 300 | Alert distance in km |
| minMagnitude | number | 3.0 | Minimum earthquake magnitude |
| language | string | zh | Alert language: zh/en/ja |
| sources.CENC | boolean | true | Enable China data |
| sources.JMA | boolean | true | Enable Japan data |
| sources.CWA | boolean | true | Enable Taiwan data |
| webhook | string | null | Encrypted webhook URL |

---

## Supported Cities (20+)

| City | Pinyin | Abbr | Coordinates |
|------|--------|------|-------------|
| 大理 | dali, dal, dl | DL | 25.61°N, 100.27°E |
| 北京 | beijing, bj, b | BJ | 39.90°N, 116.40°E |
| 上海 | shanghai, sh, s | SH | 31.23°N, 121.47°E |
| 昆明 | kunming, km, k | KM | 25.04°N, 102.71°E |
| 成都 | chengdu, cd, c | CD | 30.57°N, 104.07°E |
| 东京 | tokyo, dj, d | DJ | 35.68°N, 139.69°E |
| ... | ... | ... | ... |

### Location Matching Examples

All these return Beijing:
```javascript
await init({ location: '北京' })      // Chinese
await init({ location: 'beijing' })   // Full pinyin
await init({ location: 'bj' })        // Abbreviation
await init({ location: 'bei' })       // Partial match
```

---

## Multi-Language Alerts

Alert language is automatically selected based on earthquake source:

| Source | Language | Example |
|--------|----------|---------|
| CENC (China) | 中文 | ⚠️ 地震预警提醒！ |
| CWA (Taiwan) | 中文 | ⚠️ 地震预警提醒！ |
| JMA (Japan) | 日本語 | ⚠️ 地震アラート！ |

### Manual Language Override

```javascript
// Set preferred language (applies to alert format)
await init({ language: 'en' })

// All alerts will be in English regardless of source
```

### Alert Message Format

```
⚠️ Earthquake Alert!
📍 Epicenter near Dali:

1. 🔴 M7.6级 [中国地震台网]
   📍 汤加群岛
   📏 Distance: 5000km
   ⏰ 2026-03-24 12:37:50
   📊 Depth: 250km

Please stay safe!
```

---

## Security

Webhook URLs are encrypted using AES-256-CBC before storing in config file:

```javascript
// Set webhook (automatically encrypted)
await config({ webhook: 'https://oapi.dingtalk.com/robot/send?access_token=xxx' })

// Stored encrypted, decrypted only in memory
```

---

## Performance

### Shared Cache
- Reduces redundant API calls
- TTL-based expiration (1 minute default)
- Auto-cleanup every 5 minutes

### Parallel Fetching
- All three data sources fetched simultaneously
- Fast response time

---

## Return Format

```javascript
{
  timestamp: "2026-03-24T14:30:00.000Z",
  sources: [
    { source: "CENC", sourceName: "中国地震台网", count: 10, earthquakes: [...] },
    { source: "JMA", sourceName: "日本气象厅", count: 5, earthquakes: [...] }
  ],
  earthquakes: [...],      // Merged, sorted by time
  totalCount: 15,
  nearbyEarthquakes: [...], // Within distanceThreshold
  hasAlert: true/false,
  alertMessage: "..."       // Formatted alert string
}
```

---

## Notes

- 🌐 Data from official government agencies (CENC/CWA/JMA)
- 🔑 No API key required
- 📡 WebSocket + HTTP fallback
- 🔄 Auto-retry on failure

---

## Support

- Author: fungjcode
- GitHub: https://github.com/fungjcode/earthquake-monitor
- Report issues at: https://github.com/fungjcode/earthquake-monitor/issues
