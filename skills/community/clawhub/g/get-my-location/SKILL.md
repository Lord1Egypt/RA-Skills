---
name: get-my-location
description: Get current IP location info (country, province, city, coordinates) with multi-source fallback. No API key required.
trigger_patterns:
  - "get my location"
  - "where am i"
  - "my ip location"
  - "获取我的位置"
  - "查我的位置"
  - "我的位置信息"
  - "我在哪里"
  - "我这里的位置"
  - "查询本机IP位置"
---

# Get My Location

Get current or specified IP geolocation with three-tier fallback, no API key required.

## Usage

```bash
# Current IP location
python scripts/location.py

# Query specific IP
python scripts/location.py 8.8.8.8
python scripts/location.py 240e:43d:3d08:33c8:18a2:e45b:ce7a:67de

# JSON output (programmatic use)
python scripts/location.py --json
python scripts/location.py 8.8.8.8 --json
```

## Fallback Chain

| Priority | API | Key Required | Limit |
|----------|-----|-------------|-------|
| 1 | freegeoip.app | No | None |
| 2 | api.ipbase.com | No | 10k/mo |
| 3 | ip-api.com | No | 45/min |

Each API retries **3 times** with 1s delay before falling back to the next.

## Output

**Human-readable:**
```
📍 你的位置信息
  IP 地址: 222.89.92.62
  国家:   China
  省份:   Henan
  城市:   Xinxiang
  邮编:   453000
  坐标:   35.308777, 113.867203
  时区:   Asia/Shanghai
  数据源: freegeoip.app
```

**JSON** (`--json`):
```json
{
  "ip": "222.89.92.62",
  "country_code": "CN",
  "country_name": "China",
  "region_name": "Henan",
  "city": "Xinxiang",
  "zip_code": "453000",
  "latitude": 35.30877685546875,
  "longitude": 113.86720275878906,
  "time_zone": "Asia/Shanghai"
}
```

## Python Requirements

- **Python 3.6+** (stdlib only — `urllib`, `json`, `sys`)
- No pip packages needed
- Works on Windows / macOS / Linux

## When to Use

- User says "my location", "where am i", "get my location"
- User says "获取我的位置", "我的位置", "我在哪里", etc.
- Need IP-based geolocation for any purpose

## Notes

- IPv4 and IPv6 supported
- Accuracy varies: typically city-level (some countries support district-level)
- For freegeoip/ipbase: freegeoip.app redirects to api.ipbase.com (same data)
- Exit code 0 on success, 1 if all sources fail
