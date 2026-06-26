---
name: beach-safety
version: 1.1.1
description: Comprehensive beach surf conditions via mcporter MCP call. Use when asked about surf, waves, swim conditions, rip currents, or beach safety at any beach worldwide.
---

# Beach Safety

Get surf/weather conditions for any beach using the `beach-safety` MCP server.

## Quick Usage

```bash
mcporter call beach-safety get_beach_report --args '{"beach_name": "Waikiki"}'
mcporter call beach-safety get_beach_report --args '{"beach_name": "Hapuna Beach, Hawaii"}'
```

## Tools Available

| Tool | Use Case |
|------|----------|
| `get_beach_report` | Full text report — waves, swell, wind, UV, safety score, recommendations |
| `get_beach_json` | Same data as JSON for programmatic use |
| `get_surf_forecast` | Surf-specific: wave height, swell, period, direction, rip risk |
| `get_uv_forecast` | UV index with sun protection guidance |

## Safety Score

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Generally safe | Enjoy with normal precautions |
| 7-8 | Minor concerns | Caution advised |
| 4-6 | Caution | Swim near lifeguard |
| 1-3 | Dangerous | **Stay out of the water** |

## Reporting Style

**Always include BOTH current UV and daily max UV** in surf summaries. The API returns them as `current=X (daily max=Y)`. Never just say "UV max" — say "UV current=X (daily max=Y)" so the user knows if it's day or night at the beach.

## Installation (Universal)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

(Requires Python 3.10+ and `httpx>=0.27.0`)

### 2. Find your install path

After `clawhub install beach-safety`, the skill lands in your skills directory (e.g. `~/.openclaw/workspace/skills/beach-safety/`). The MCP server is at:

```
<install-dir>/src/server.py
```

For example, if you installed into `~/.openclaw/workspace/skills/`:

```bash
# Confirm the path
ls ~/.openclaw/workspace/skills/beach-safety/src/server.py
```

### 3. Add to mcporter

Add this to your mcporter config (e.g. `~/.openclaw/workspace/config/mcporter.json`):

```json
{
  "mcpServers": {
    "beach-safety": {
      "command": "python3",
      "args": ["<path-to>/src/server.py"]
    }
  }
}
```

Replace `<path-to>` with the actual install location from step 2.

### 4. Test

```bash
mcporter call beach-safety get_beach_report --args '{"beach_name": "Waikiki"}'
```

## Data Sources (all free — no API keys)

| Source | Data |
|--------|------|
| OpenStreetMap / Photons | Beach name → coordinates |
| Open-Meteo Marine | Wave height, swell, ocean currents |
| Open-Meteo Weather | Air temp, wind, precipitation, UV index |
| NOAA NWS | Rip current risk, surf zone forecast (US only) |

## Notes

- Works for any beach worldwide — just name it
- NOAA surf zone data is most detailed for US coasts
- Open-Meteo marine data covers global oceans
- Some less-famous beaches may not resolve — try adding country/state (e.g. "Kuta Beach, Bali, Indonesia")
- Beach name → coordinates powered by OpenStreetMap + Photons (free)
