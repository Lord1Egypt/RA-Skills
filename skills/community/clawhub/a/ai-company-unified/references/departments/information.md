# Information Services

> Department: information
> Skills in department: 1

## Information Services (v2.0.0)

## 3. Core Responsibilities

### 3.1 Location Service

#### 3.1.1 Supported Methods

| Method | Accuracy | Use Case | API Key Required |
|--------|----------|----------|-----------------|
| **GPS** | 3-10m | Outdoor, navigation | No |
| **System** | 10m-1km | Indoor/outdoor, OS-managed | No |
| **IP** | 1-50km | City-level, quick detection | No |
| **WiFi** | 10-100m | Indoor, urban environments | Optional |
| **Cellular** | 100m-3km | Rural, GPS-denied | Optional |
| **Triangulated** | Weighted centroid | Multi-method fusion | No |

#### 3.1.2 Triangulation Algorithm

```
Algorithm: Weighted-Centroid Triangulation

Input:  Set of (lat, lon, accuracy_m) tuples from available methods
Output: Fused (lat, lon, accuracy_m, confidence, sources)

Steps:
1. For each source i:
   weight_i = 1 / (accuracy_i ^ 2)
2. Normalize: w_i = weight_i / sum(all weights)
3. lat_fused  = sum(w_i * lat_i)
   lon_fused  = sum(w_i * lon_i)
4. accuracy_fused = sqrt(sum(w_i * (dist_i ^ 2)))  // weighted RMS residual
5. confidence = clamp(1.0 - accuracy_fused / 50000, 0.0, 1.0)
   // 50km = zero confidence, <10m = near 1.0
6. Return (lat_fused, lon_fused, accuracy_fused, confidence, source_map)
```

#### 3.1.3 Location Output Format

```json
{
  "latitude": 39.9042,
  "longitude": 116.4074,
  "accuracy_meters": 15,
  "confidence": 0.92,
  "method": "triangulated",
  "sources": {
    "gps": {"lat": 39.9045, "lon": 116.4071, "accuracy": 5, "weight": 0.6},
    "wifi": {"lat": 39.9039, "lon": 116.4078, "accuracy": 30, "weight": 0.3},
    "ip": {"lat": 39.9042, "lon": 116.4074, "accuracy": 5000, "weight": 0.1}
  },
  "timestamp": "2026-04-27T01:00:00Z"
}
```

#### 3.1.4 Fallback Chain

```
GPS → System → IP → WiFi → Cellular → Error(INFO_001)
```

Each step attempts for up to 5 seconds before proceeding to next method.

#### 3.1.5 Optional API Keys

```bash
export GOOGLE_GEOLOCATION_API_KEY="your-key"
export MLS_API_KEY="your-key"
export UNWIRED_API_KEY="your-key"
```

#### 3.1.6 Platform Notes

| Platform | Primary Method | Notes |
|----------|---------------|-------|
| Windows | GeoCoordinateWatcher | PowerShell WiFi+IP+GPS fusion |
| macOS | CoreLocation via locationd | System daemon |
| Linux | GeoClue2 via D-Bus | WiFi+cell fusion |

---

### 3.2 Weather Service

#### 3.2.1 Workflow

```
User Request → Geolocation → Weather Lookup → Multi-Source Fusion → Output
```

1. **Geolocation** — Use location service to get coordinates (full fallback chain)
2. **Weather lookup** — Query weather API with coordinates
3. **Multi-source fusion** — Combine multiple sources with confidence weighting
4. **Output** — Return structured weather data with confidence score

#### 3.2.2 Supported Weather Data

| Data Point | Type | Description |
|------------|------|-------------|
| Temperature | float | Current temp in Celsius |
| Conditions | string | sunny, cloudy, rainy, snowy, etc. |
| Humidity | int | Percentage 0-100 |
| Wind Speed | float | km/h |
| Wind Direction | string | Compass direction |
| Forecast | array | 3-7 day outlook |
| UV Index | int | UV radiation level 0-11+ |
| AQI | int | Air quality index |

#### 3.2.3 Weather Sources

| Source | API Key | Rate Limit | Coverage |
|--------|---------|-----------|----------|
| wttr.in | Not required | Generous | Global |
| Open-Meteo | Not required | 10K/day | Global |
| Custom API | Required | Per-provider | Per-provider |

#### 3.2.4 Weather Output Format

```json
{
  "location": {"lat": 39.9042, "lon": 116.4074, "city": "Beijing"},
  "current": {
    "temp_c": 18,
    "conditions": "partly cloudy",
    "humidity": 65,
    "wind_kmh": 12,
    "wind_dir": "NW",
    "uv_index": 5,
    "aqi": 72
  },
  "forecast": [
    {"date": "2026-04-28", "high_c": 22, "low_c": 14, "conditions": "sunny"},
    {"date": "2026-04-29", "high_c": 20, "low_c": 13, "conditions": "cloudy"}
  ],
  "confidence": 0.88,
  "source": "wttr.in",
  "cached": false,
  "cache_age_minutes": 0
}
```

#### 3.2.5 Error Handling

| Error | Action | Fallback |
|-------|--------|----------|
| No location available | Use IP-based location | Default to configured city |
| Weather API timeout | Retry with alternate source | Return partial data |
| All sources failed | Return Error(INFO_002) | Include last-known if available |
| Invalid coordinates | Return Error(INFO_005) | Suggest city-name input |

#### 3.2.6 Cache Policy

| Parameter | Value |
|-----------|-------|
| Cache duration | 30 minutes |
| Cache key | `${lat},${lon}` rounded to 2 decimals |
| Cache invalidation | On explicit refresh request |
| Stale cache behavior | Serve stale with `cached: true, cache_age_minutes: N` |

---

### 3.3 Time Service

#### 3.3.1 Source Priority

| Priority | Source | Accuracy | Latency | Base Confidence |
|----------|--------|----------|---------|----------------|
| 1 | System clock | OS-dependent | Instant | 0.85 |
| 2 | NTP | +/-10ms | 50-200ms | 0.98 |
| 3 | Web API (worldtimeapi, etc.) | +/-500ms | 100-500ms | 0.92 |

#### 3.3.2 Time Fusion Workflow

```
1. Query system clock (instant, baseline)
2. If precision needed or system clock suspected drift:
   a. Query NTP server (pool.ntp.org)
   b. If NTP fails, query web time API (worldtimeapi.org)
3. Compute offset between sources
4. Score confidence based on source agreement
5. Return unified result
```

#### 3.3.3 Confidence Scoring

| Scenario | Confidence Calculation |
|----------|----------------------|
| System only | 0.85 |
| System + NTP agree (offset < 100ms) | 0.98 |
| System + NTP disagree (offset > 100ms) | 0.80, flag drift warning |
| System + Web API agree | 0.92 |
| All three agree | 0.99 |
| NTP failed, Web API fallback | 0.90 |

#### 3.3.4 Time Output Format

```json
{
  "datetime": "2026-04-27T01:55:00+08:00",
  "timestamp": 1742790900,
  "timezone": "Asia/Hong_Kong",
  "utc_offset_hours": 8,
  "sources": ["system", "ntp"],
  "confidence": 0.96,
  "accuracy_ms": 15,
  "drift_warning": false
}
```

#### 3.3.5 Voice Output (Optional)

When TTS is available and requested, format time as natural language:
- "It is 1:55 AM, Sunday, April 27th."
- Timezone-aware formatting per user locale.

---

### 3.4 Coordination Logic

#### 3.4.1 Request Routing

```
User query
  → Parse intent (location/weather/time/combined)
  → Route to service(s)
  → Execute with fallback chains
  → Fuse results if multiple services
  → Compute overall confidence
  → Return structured output
```

#### 3.4.2 Intent-to-Service Mapping

| Intent Keywords | Service |
|----------------|---------|
| "where", "location", "coordinates", "GPS", "locate" | location |
| "weather", "forecast", "rain", "temperature", "sunny" | weather |
| "time", "clock", "date", "when", "hour" | time |
| Multiple / ambiguous | all (sequential execution) |

#### 3.4.3 Combined Query Output

```json
{
  "service_type": "all",
  "data": {
    "location": { "...": "location output" },
    "weather": { "...": "weather output" },
    "time": { "...": "time output" }
  },
  "overall_confidence": 0.90,
  "timestamp": "2026-04-27T01:55:00Z"
}
```

Overall confidence = minimum confidence across all sub-results.

---

## 4. Constraints

| Constraint | Description |
|-----------|-------------|
| No persistent location storage | Coordinates must not be stored unless user explicitly requests |
| No credential logging | API keys must never appear in output or logs |
| Rate-limit compliance | Respect external API rate limits; implement backoff |
| Privacy-first | Do not log coordinates without user request |
| Fallback mandatory | Every service must have a fallback chain; never return bare error |
| Cache TTL enforced | Weather cache max 30 minutes; no stale data served silently |
| Confidence required | Every result must include confidence score 0-1 |
| Response time budget | Total response time must not exceed 10 seconds |

---

## 5. Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Location accuracy (triangulated) | < 100m | RMS residual from ground truth |
| Weather data freshness | < 30 min cache | Cache age at response time |
| Time accuracy (NTP-synced) | < 1s offset | NTP offset measurement |
| Confidence score calibration | +/-0.05 of actual | Historical accuracy vs. confidence |
| Fallback success rate | > 95% | % of requests returning valid data |
| Response time (single service) | < 5s | P95 latency |
| Response time (combined query) | < 10s | P95 latency |
| Error rate | < 1% | % of requests returning INFO_xxx errors |

---

## 6. Integration Points

| Integration | Description |
|-------------|-------------|
| ai-company-hq | Report service health, coordinate with other departments |
| ai-company-harness | Engineering compliance (L1-L6), quality gates |
| External APIs | wttr.in, Open-Meteo, worldtimeapi.org, NTP servers |
| TTS systems | Voice output for time service (optional) |
| Node devices | GPS/WiFi/Cellular location sources via companion apps |

---

## 7. Error Code Reference

| Code | Message | Recovery |
|------|---------|----------|
| INFO_001 | No location source available | Try manual city input |
| INFO_002 | Weather API request failed | Retry with alternate source |
| INFO_003 | Time source unavailable | Use system clock as fallback |
| INFO_004 | Required API credentials missing | Configure API keys in environment |
| INFO_005 | Invalid coordinates format | Use "lat,lon" format (e.g. "39.9,116.4") |

---

*End of method-patterns.md. Return to [SKILL.md](../SKILL.md) for index and quick reference.*

---

