---
name: bardi-smart-home-tuya
description: "Mengontrol perangkat smart home Tuya melalui Cloud API, termasuk lampu, colokan, sensor, meteran, dan lainnya. Mendukung lampu pintar Bardi dengan fitur pengaturan warna, kecerahan (brightness), suhu warna putih, serta kontrol HSV. Selain itu, juga bisa digunakan untuk mengontrol perangkat Tuya secara umum (nyala/mati, cek status, kirim perintah DP) dan menemukan perangkat di jaringan lokal. Credential dibaca dari environment variable: TUYA_ACCESS_ID (required), TUYA_ACCESS_SECRET (required), TUYA_API_REGION (opsional, default: sg). Fitur ini cocok digunakan saat pengguna ingin menyalakan atau mematikan lampu, mengatur kecerahan, mengubah warna, mengecek status perangkat, memindai perangkat di jaringan lokal, atau memberikan perintah ke perangkat smart home Bardi/Tuya."
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠",
        "name": "bardi-smart-home-tuya",
        "description": "Mengontrol perangkat smart home Tuya melalui Cloud API, termasuk lampu, colokan, sensor, meteran, dan lainnya.",
        "requires": { "env": ["TUYA_ACCESS_ID", "TUYA_ACCESS_SECRET"], "pip": ["tinytuya"] },
        "primaryEnv": "TUYA_ACCESS_ID",
        "env":
          {
            "TUYA_ACCESS_ID":
              {
                "label": "Tuya Access ID",
                "description": "Cloud project Access ID from Tuya IoT Platform (iot.tuya.com)",
                "placeholder": "your-access-id",
                "required": true
              },
            "TUYA_ACCESS_SECRET":
              {
                "label": "Tuya Access Secret",
                "description": "Cloud project Access Secret from Tuya IoT Platform (iot.tuya.com)",
                "placeholder": "your-access-secret",
                "required": true
              },
            "TUYA_API_REGION":
              {
                "label": "Tuya API Region",
                "description": "Data center region: sg (default), us, eu, cn, in",
                "placeholder": "sg",
                "required": false
              }
          }
      }
  }
---

# Bardi-Tuya Smart Home

Control Tuya smart home devices via cloud API.

## Requirements

- `tinytuya` Python library installed
- Environment variables must be set:
  - `TUYA_ACCESS_ID` — Cloud project Access ID
  - `TUYA_ACCESS_SECRET` — Cloud project Access Secret
  - `TUYA_API_REGION` — Data center region (default: `sg`)

The skill will not function if TUYA_ACCESS_ID and TUYA_ACCESS_SECRET are missing.

## Setup

See [SETUP.md](SETUP.md) for detailed installation and configuration instructions.

## API Reference

See [references/api-reference.md](references/api-reference.md) for DP codes, color presets, HSV encoding, and device details.

## Scripts

Two scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `devices_control.py` | Device controller — lights, plugs, sensors, any Tuya device |
| `devices_scan.py` | Local network device discovery |

## Workflows

### Control Any Device

```bash
python3 scripts/devices_control.py <device_id> <command> [args]
```

### Light Commands

```bash
python3 scripts/devices_control.py <device_id> on
python3 scripts/devices_control.py <device_id> off
python3 scripts/devices_control.py <device_id> color blue
python3 scripts/devices_control.py <device_id> white 750 80
python3 scripts/devices_control.py <device_id> brightness 50
python3 scripts/devices_control.py <device_id> preset warm 50
```

### Generic Device Commands

```bash
python3 scripts/devices_control.py <device_id> status
python3 scripts/devices_control.py <device_id> detail
python3 scripts/devices_control.py <device_id> model
python3 scripts/devices_control.py <device_id> send bright_value 500
python3 scripts/devices_control.py discover
```

### Scan Local Network

```bash
python3 scripts/devices_scan.py [--timeout 10] [--verbose]
```

## Brightness Convention

User input is always 1–100 (percentage). Scripts convert to Tuya range (10–1000) internally:
- 100% → 1000
- 50% → 500
- 10% → 100

## Color Presets

Available presets: `red`, `orange`, `yellow`, `green`, `cyan`, `blue`, `purple`, `mauve`, `pink`, `warm`, `cool`

`warm` and `cool` use white mode with temperature control. All others use HSV color mode.
