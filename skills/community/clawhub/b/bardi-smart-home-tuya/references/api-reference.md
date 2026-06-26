# API Reference — Bardi-Tuya Smart Home

## Authentication

All cloud requests use Tuya IoT Platform credentials via the `tinytuya` library.

Environment variables:
- `TUYA_ACCESS_ID` — Cloud project access ID
- `TUYA_ACCESS_SECRET` — Cloud project access secret
- `TUYA_API_REGION` — Data center region (sg, cn, us, eu, in)

## API Response Format

Success:
```json
{
  "success": true,
  "t": 1774749812359,
  "result": [ ... ]
}
```

Error:
```json
{
  "success": false,
  "code": 1010,
  "msg": "token invalid"
}
```

### Common Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 1010 | Token invalid | Check Access ID and Secret |
| 1108 | URI path invalid | Update tinytuya library |
| 1106 | Permission denied | Enable required API group in Tuya console |
| 2003 | Device not found | Verify device is linked to your account |

## Device Control DP Codes

### Lights (RGBWW, White, LED Strips)

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `switch_led` | bool | true/false | Power on/off |
| `work_mode` | enum | white/colour/scene/music | Light mode |
| `bright_value` | value | 10–1000 | Brightness |
| `temp_value` | value | 0–1000 | Color temperature (warm↔cool) |
| `colour_data` | string | 12-char hex | HSV color encoded |
| `scene_data` | string | hex | Scene configuration |

### Smart Plugs and Switches

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `switch` | bool | true/false | Power on/off |
| `switch_1` | bool | true/false | Socket 1 (multi-socket) |
| `switch_2` | bool | true/false | Socket 2 |
| `countdown_1` | value | 0–86400 | Auto-off timer (seconds) |

### Smart Meters and Energy Monitors

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `switch` | bool | true/false | Power on/off |
| `cur_current` | value | — | Current (mA) |
| `cur_power` | value | — | Power (W) |
| `cur_voltage` | value | — | Voltage (V × 10) |

### Sensors (Temperature, Humidity, Motion)

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `va_temperature` | value | — | Temperature (°C × 10) |
| `va_humidity` | value | — | Humidity (%) |
| `pir` | enum | pir/nopir/noalarm | Motion detection |

### Curtains and Blinds

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `control` | enum | open/stop/close | Movement |
| `percent_control` | value | 0–100 | Position percentage |

### Cameras

| Code | Type | Range | Description |
|------|------|-------|-------------|
| `basic_private` | bool | true/false | Privacy mode |
| `basic_flip` | bool | true/false | Image flip |
| `basic_osd` | bool | true/false | On-screen display |

## HSV Color Encoding

The `colour_data` field stores HSV as a 12-character hex string: `HHHHSSSSVVVV`

| Segment | Position | Value | Hex Range |
|---------|----------|-------|-----------|
| Hue | chars 0–3 | 0–360 | `0000`–`0168` |
| Saturation | chars 4–7 | 0–1000 | `0000`–`03E8` |
| Value | chars 8–11 | 0–1000 | `0000`–`03E8` |

### Example Conversions

| Color | H | S | V | Hex |
|-------|---|---|---|-----|
| Red | 0 | 1000 | 1000 | `000003e803e8` |
| Blue | 240 | 1000 | 1000 | `00f003e803e8` |
| Green | 120 | 1000 | 1000 | `007803e803e8` |
| Purple | 280 | 1000 | 1000 | `011803e803e8` |
| Mauve | 300 | 350 | 1000 | `012c015e03e8` |
| Pink | 330 | 1000 | 1000 | `014a03e803e8` |

### Python Conversion

```python
def hsv_to_hex(h, s, v):
    return f"{h:04x}{s:04x}{v:04x}"

def hex_to_hsv(hex_str):
    h = int(hex_str[0:4], 16)
    s = int(hex_str[4:8], 16)
    v = int(hex_str[8:12], 16)
    return h, s, v
```

## Color Presets Reference

| Preset | Mode | H | S | V / Temp | Description |
|--------|------|---|---|----------|-------------|
| red | colour | 0 | 1000 | 1000 | Pure red |
| orange | colour | 30 | 1000 | 1000 | Orange |
| yellow | colour | 60 | 1000 | 1000 | Yellow |
| green | colour | 120 | 1000 | 1000 | Green |
| cyan | colour | 180 | 1000 | 1000 | Cyan |
| blue | colour | 240 | 1000 | 1000 | Blue |
| purple | colour | 280 | 1000 | 1000 | Purple |
| mauve | colour | 300 | 350 | 1000 | Soft mauve |
| pink | colour | 330 | 1000 | 1000 | Pink |
| warm | white | — | — | temp=500 | Warm white |
| cool | white | — | — | temp=1000 | Cool white |

## Brightness Preservation

When changing brightness while in color mode, the script:
1. Queries current device status
2. Reads `work_mode` and `colour_data`
3. If mode is `colour`, extracts H and S from hex
4. Constructs new `colour_data` with updated V value
5. Sends both `work_mode` and new `colour_data` together

This preserves the current color while only changing brightness.

## Known Devices

| Device ID | Type | Switch Code | Features |
|-----------|------|-------------|----------|
| `a329cdc779d3d97b38vjyf` | BARDI 12w RGBWW Bulb | `switch_led` | Color, brightness, temperature, presets |
| `a343f3ea1a921b3df2qanr` | Smart Meter Protector | `switch` | Power monitoring |
