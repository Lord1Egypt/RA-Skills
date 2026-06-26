# Victron Attribute Codes Reference

Quick lookup for common battery and system attributes in Victron widgets.

## Battery Monitor (SmartShunt) — Widget: BatterySummary

| Code | Attribute ID | Description | Unit | Example |
|------|--------------|-------------|------|---------|
| V | 47 | Battery Voltage | V | 14.17 |
| VS | 48 | Starter Battery Voltage | V | 14.20 |
| I | 49 | Battery Current | A | 3.50 |
| CE | 50 | Consumed Amphours | Ah | 0.00 |
| SOC | 51 | State of Charge | % | 100.0 |
| TTG | 52 | Time to Go | h | 0.00 |
| Relay | 54 | Relay Status | - | On/Off |
| BT | 115 | Battery Temperature | °F | 72 |
| VM | 116 | Mid-point Voltage | V | 7.08 |
| VMD | 117 | Mid-point Deviation | % | 0.1 |
| AL | 119 | Low Voltage Alarm | - | No alarm |
| AH | 120 | High Voltage Alarm | - | No alarm |
| ALS | 121 | Low Starter Voltage Alarm | - | No alarm |
| AHS | 122 | High Starter Voltage Alarm | - | No alarm |
| ASoc | 123 | Low SOC Alarm | - | No alarm |
| ALT | 124 | Low Temperature Alarm | - | No alarm |
| AHT | 125 | High Temperature Alarm | - | No alarm |
| AM | 126 | Mid-voltage Alarm | - | No alarm |
| ALF | 155 | Low Fused Voltage Alarm | - | No alarm |
| AHF | 156 | High Fused Voltage Alarm | - | No alarm |
| AFB | 157 | Fuse Blown Alarm | - | No alarm |
| AHIT | 158 | High Internal Temp Alarm | - | No alarm |
| mcV | 173 | Minimum Cell Voltage | V | 3.40 |
| McV | 174 | Maximum Cell Voltage | V | 3.50 |
| eRelay | 182 | External Relay | - | Open/Closed |

## Solar Charger (MPPT) — From Diagnostics

| Code | Description | Unit | Example |
|------|-------------|------|---------|
| PVP | PV Power | W | 168 |
| PVV | PV Voltage | V | 18.6 |
| PVI | PV Current | A | 9.2 |
| YT | Yield Today | kWh | 0.59 |
| YY | Yield Yesterday | kWh | 0.74 |
| YU | User Yield (Lifetime) | kWh | 9.69 |
| MCPT | Max Charge Power Today | W | 168 |
| MCPY | Max Charge Power Yesterday | W | 120 |
| ScW | Battery Watts (Charger) | W | -1 |
| ScI | Charger Current | A | -0.1 |
| ScV | Charger Voltage | V | 14.2 |
| ScS | Charge State | - | Float |
| ScMm | MPPT State | - | Voltage/Current Limited |
| Scs | Charger On/Off | - | On |

## VE.Bus System (Inverter/Charger) — From Diagnostics

| Code | Description | Unit | Example |
|------|-------------|------|---------|
| IV1 | AC Input 1 Voltage | V | 121.4 |
| IV2 | AC Input 2 Voltage | V | - |
| OV1 | AC Output 1 Voltage | V | 120 |
| ePR | Phase Rotation | - | Ok |
| rt | Relay Test Status | - | OK |
| vvv | VE.Bus Firmware Version | - | 508 |

## Device Status — From Alarms Endpoint

Returns active alarms with device metadata:

```json
{
  "name": "Device Name",
  "device_name": "SmartShunt 500A",
  "product_name": "Battery Monitor",
  "firmware_version": "v4.19",
  "serial_number": "HQ2203NCX9H",
  "instance": 279,
  "lastConnection": 1773105960,
  "secondsAgo": 123
}
```

## Tips for Querying

### Get Battery Data with Instance

```bash
curl -H "X-Authorization: Token YOUR_TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/widgets/BatterySummary/latest?instance=279"
```

Returns all battery attributes in `records.data`:

```json
{
  "records": {
    "data": {
      "47": {"formattedValue": "14.17 V", "valueFloat": 14.17},
      "49": {"formattedValue": "3.50 A", "valueFloat": 3.50},
      "51": {"formattedValue": "100.0 %", "valueFloat": 100.0},
      ...
    }
  }
}
```

### Get Diagnostic Data

```bash
curl -H "X-Authorization: Token YOUR_TOKEN" \
  "https://vrmapi.victronenergy.com/v2/installations/{id}/diagnostics"
```

Returns all device diagnostics with `code`, `description`, `formattedValue`.

### Filter by Device

```bash
# Get only Solar Charger data
jq '.records[] | select(.Device | test("Solar"))'

# Get only Inverter data
jq '.records[] | select(.Device | test("VE.Bus"))'
```

## Common Queries

**Battery SOC%**: `records.data["51"].valueFloat`

**Solar Power Now**: Diagnostics → Search for code "PVP"

**AC Input Voltage**: Diagnostics → Search for code "IV1" or "IV2"

**Today's Solar Yield**: Diagnostics → Search for code "YT"

**Active Alarms**: `/v2/installations/{id}/alarms` → filter by `active[1] == 1`
