# BirdWeather API Reference

Base URL: `https://app.birdweather.com/api/v1/stations/{token}`

All endpoints are GET, no authentication required. Tokens are public read-only identifiers.

## Endpoints

### `/stats`
Station detection statistics.

Params: `period` = `day` | `week` | `month`

Response:
```json
{ "detections": 363, "species": 18 }
```

---

### `/detections`
Recent individual detection events.

Params: `limit` (int, default 10), `cursor` (for pagination)

Response:
```json
{
  "detections": [{
    "id": 6528041142,
    "timestamp": "2026-04-02T09:02:28.000-07:00",
    "confidence": 0.561,
    "certainty": "almost_certain",
    "species": {
      "id": 134,
      "commonName": "House Finch",
      "scientificName": "Haemorhous mexicanus",
      "color": "#ff5a86",
      "thumbnailUrl": "https://media.birdweather.com/species/134/..."
    },
    "soundscape": {
      "url": "https://media.birdweather.com/soundscapes/..."
    }
  }]
}
```

`certainty` values: `almost_certain`, `very_likely`, `uncertain`

---

### `/species`
Species list for a time period, sorted by detection count.

Params: `period` = `day` | `week` | `month`, `limit` (int)

Response:
```json
{
  "species": [{
    "id": 134,
    "commonName": "House Finch",
    "scientificName": "Haemorhous mexicanus",
    "color": "#ff5a86",
    "thumbnailUrl": "https://...",
    "imageUrl": "https://...",
    "detections": { "total": 730 },
    "latestDetectionAt": "2026-04-02T09:01:07.000-07:00"
  }]
}
```

---

### `/weather`
Station metadata and live PUC sensor readings.

No params required.

Response:
```json
{
  "station": {
    "name": "station-name",
    "live": true
  },
  "weather": {
    "puc": {
      "temperature": 31.5,
      "humidity": 15.2,
      "barometricPressure": 1011.4,
      "aqi": 105.0,
      "eco2": 1105.0,
      "soundPressureLevel": 62.4,
      "voc": 0.163
    }
  }
}
```

`temperature` is in Celsius. Convert: `F = C * 9/5 + 32`  
`soundPressureLevel` is in dB SPL  
`aqi` follows US EPA scale (0–50 Good, 51–100 Moderate, 101–150 Sensitive, 151–200 Unhealthy)  
`puc` key is null if station is offline or has no PUC sensor  

---

## Notes

- Tokens are per-station, not per-user
- No rate limit documented but be reasonable (avoid <1 min polling)
- All timestamps are ISO 8601 with local timezone offset
- Species `color` is a hex string assigned by BirdWeather per species
- `thumbnailUrl` is a CDN-hosted JPEG, generally ~100×100px
