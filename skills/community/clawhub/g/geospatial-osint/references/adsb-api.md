# ADS-B Exchange API Reference

## Overview

ADS-B Exchange provides free access to global flight data. Registration required.

## Authentication

1. Register at https://www.adsbexchange.com/
2. Get API key from account page
3. Include in header: `Authorization: Bearer YOUR_API_KEY`

## Endpoints

### Aircraft in Region

```
GET https://adsbexchange.com/api/aircraft/{lat}/{lon}/{dist}/
```

**Parameters:**
- `lat`: Latitude center
- `lon`: Longitude center  
- `dist`: Radius in nautical miles

**Response:**
```json
{
  "ac": [
    {
      "icao": "abc123",
      "call": "BA249",
      "lat": 51.4700,
      "lon": -0.4543,
      "alt": 37000,
      "gs": 485,
      "track": 90,
      "ts": "2026-03-05T18:30:00Z"
    }
  ],
  "ctime": 1234567890,
  "msg": ""
}
```

### All US Aircraft

```
GET https://adsbexchange.com/api/aircraft/
```

### Military Aircraft

```
GET https://adsbexchange.com/api/military/
```

### Flights by Route

```
GET https://adsbexchange.com/api/routes/{origin}/{dest}/
```

## Rate Limits

- Free: 1000 requests/hour
- Paid: Higher limits available

## Tips

- Filter by `alt` for altitude bands
- Use `gs` for ground speed (knots)
- `track` is heading in degrees (0-360)
- `ts` is timestamp of last update
