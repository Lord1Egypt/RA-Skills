# Victron VRM API Quick Reference

Fast lookup for common VRM API endpoints and patterns.

## Authentication

All requests require the `X-Authorization` header:

```bash
curl -H "X-Authorization: Token YOUR_TOKEN" https://vrmapi.victronenergy.com/v2/...
```

**Get your token**: https://vrm.victronenergy.com/access-tokens

## Base URL

```
https://vrmapi.victronenergy.com/v2
```

## Common Endpoints

### Installation Info

```
GET /v2/installations/{id}
GET /v2/installations/{id}/widgets
GET /v2/installations/{id}/widgets/{widgetName}/latest?instance={instance}
GET /v2/installations/{id}/alarms?limit=10
GET /v2/installations/{id}/diagnostics
```

### User Info

```
GET /v2/users/me
GET /v2/users/me/installations
```

### Stats (Historical Data)

```
GET /v2/installations/{id}/stats?type=custom&attributeCodes[]=51&interval=hours&start={unix_ts}&end={unix_ts}
```

## Key Patterns

### Find SmartShunt Instance

Query alarms endpoint to see all connected devices:

```bash
curl -H "X-Authorization: Token TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/alarms?limit=1" | \
  jq '.devices[] | select(.deviceName == "Battery Monitor") | .instance'
```

### Fetch Battery Data

Use BatterySummary widget with instance parameter:

```bash
curl -H "X-Authorization: Token TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/widgets/BatterySummary/latest?instance=279"
```

Response includes:
- `records.data` — Actual values (voltage, current, SOC, etc.)
- `records.meta` — Attribute definitions (format, unit, description)
- `records.attributeOrder` — Order of attributes

### Extract a Specific Metric

```bash
# Get just SOC (attribute 51)
curl ... | jq '.records.data["51"].valueFloat'

# Get formatted value with unit
curl ... | jq '.records.data["51"].formattedValue'
```

### Get Active Alarms

```bash
curl -H "X-Authorization: Token TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/alarms?limit=10"
```

Filter for active-only:

```bash
jq '.alarms[] | select(.active[1] == 1)'
```

### Get Diagnostics (All Devices)

```bash
curl -H "X-Authorization: Token TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/diagnostics" | \
  jq '.records[] | {Device, code, description, formattedValue}'
```

Filter by device:

```bash
# Solar charger only
jq '.records[] | select(.Device == "Solar Charger")'

# Inverter/VE.Bus only
jq '.records[] | select(.Device | test("VE.Bus"))'
```

## Response Structure

### Widget Data

```json
{
  "success": true,
  "records": {
    "data": {
      "47": {
        "code": "V",
        "idDataAttribute": 47,
        "value": "14.17",
        "valueFloat": 14.17,
        "dataType": "float",
        "formattedValue": "14.17 V",
        "secondsAgo": 241
      },
      // ... more attributes
    },
    "meta": {
      "47": {
        "code": "V",
        "description": "Voltage",
        "formatWithUnit": "%.2F V",
        "unit": "V"
      },
      // ... more metadata
    },
    "attributeOrder": [47, 49, 51, ...]
  }
}
```

### Alarms

```json
{
  "success": true,
  "alarms": [
    {
      "idSite": 472601,
      "instance": 276,
      "alarmEnabled": 1,
      "active": [0, 1],  // [inactive, active]
      "meta_info": {
        "name": "VE.Bus System [276]",
        "dataAttribute": "Active input",
        "icon": "device-ve-bus"
      }
    }
  ],
  "devices": [
    {
      "idSite": 472601,
      "instance": 0,
      "deviceName": "Gateway",
      "productName": "Cerbo GX",
      "firmwareVersion": "v3.70",
      "secondsAgo": 123,
      "isValid": 1
    }
  ]
}
```

### Diagnostics

```json
{
  "success": true,
  "records": [
    {
      "Device": "Solar Charger",
      "instance": 279,
      "code": "PVP",
      "description": "PV power",
      "formattedValue": "1 W",
      "rawValue": "1"
    }
  ]
}
```

## Common Mistakes

❌ Using `Authorization: Bearer` instead of `X-Authorization: Token`

❌ Forgetting the `?instance=` parameter (returns empty data)

❌ Querying `/lastLogData` (not supported in this API version)

❌ Using widget name without instance (only returns metadata)

## Rate Limiting

- ~10 requests/second is safe
- Monitor `429 Too Many Requests` responses
- Implement exponential backoff on rate limit errors

## Troubleshooting

### Empty Data Section

```json
{
  "records": {
    "data": {
      "hasOldData": false,
      "secondsAgo": {"value": 0}
    }
  }
}
```

**Fix**: Add `?instance=INSTANCE_NUMBER` to widget URL

### "Child Not Found" Error

```json
{
  "success": false,
  "errors": "Child \"BatterySummary\" not found."
}
```

**Fix**: Check installation ID, verify device is online in VRM dashboard

### Missing Metrics

Some installations may not report certain metrics. Check:
1. Device firmware version
2. Device online status in VRM
3. Metric availability on device
4. Installation age/setup date

## Testing Queries

### Get Your User ID

```bash
curl -H "X-Authorization: Token TOKEN" \
  https://vrmapi.victronenergy.com/v2/users/me | jq '.user.id'
```

### List All Your Installations

```bash
curl -H "X-Authorization: Token TOKEN" \
  https://vrmapi.victronenergy.com/v2/users/me/installations | \
  jq '.records[] | {id, name}'
```

### Check Installation Status

```bash
curl -H "X-Authorization: Token TOKEN" \
  https://vrmapi.victronenergy.com/v2/installations/{id}/alarms?limit=1 | \
  jq '.devices[] | {deviceName, lastConnection, isValid}'
```

## Useful Links

- **VRM API Docs**: https://vrm-api-docs.victronenergy.com/
- **Access Tokens**: https://vrm.victronenergy.com/access-tokens
- **Your Installations**: https://vrm.victronenergy.com/
- **Community**: https://community.victronenergy.com/
- **Reference Implementation**: https://github.com/dirkjanfaber/victron-vrm-api
