---
name: broadlinkac
version: 5.1.0
identifier: oywq00008-cell-broadlinkac-for-agent-skill
description: 🎮 AI Agent 智能空调控制核心库 — 零 GUI 依赖，import 即用。支持 17 大品牌空调（格力/美的/海尔/大金等），直连 Broadlink RM 红外遥控器。百度+和风双天气源，中央气象台+NHC 双风暴源，多日期组定时模板，Markdown 日志，故障诊断。适配树莓派/NAS/OpenWRT/桌面全平台。
---

# BroadlinkAC — AI Agent Smart AC Controller v5.1.0

Cross-platform AC control library for Broadlink RM series IR blasters. **Zero GUI dependency** — designed for AI agents to clone, install, and control air conditioners programmatically. Now includes **IR learning** — teach the system codes from any original remote, no brand limits.

## ⚠️ Safety & Persistence

> **This skill writes durable state to the user's machine.** `init()` creates `~/.ac_controller/config.json` (API keys, device config, schedule templates) and starts a background scheduler daemon thread. The scheduler survives agent task completion — scheduled on/off times, auto-adjust, and storm auto-shutdown will continue to run autonomously. **Always confirm with the user before:**
> - Modifying or creating schedule templates
> - Enabling auto-adjust or typhoon auto-shutdown
> - Changing device configuration (brand, temperature rules, location)
>
> To fully disable automation: set `schedule_enabled=False` and `auto_adjust=False` for the device, then call `_cfg.save_config(_cfg.config)`.

## Quick Start (Agent)

```bash
git clone https://github.com/oywq00008-cell/BroadlinkAC-For-Agent.git
cd BroadlinkAC-For-Agent
pip install -r requirements-core.txt
```

```python
from broadlinkac_core import init, send_ac, fetch_weather

# One-time setup — all config persisted
init(
    baidu_key="your_baidu_key",       # Baidu weather (default)
    # or use QWeather:
    # api_key="your_qw_key", qw_host="https://xxx.re.qweatherapi.com",
    location={"lat": 22.54, "lon": 114.05, "name": "Shenzhen"},
    brand="Gree"
)

# Control AC
send_ac("on", "cool", 26, "auto")     # Turn on, cool 26°C, auto fan
send_ac("off", "cool", 26, "auto")    # Turn off

# Weather — dual source (Baidu default, falls back to QWeather)
weather = fetch_weather()              # Real-time temp, humidity, feels-like

# Storm threat — returns (distance_km, storm_name)
from broadlinkac_core import typhoon_threat_distance
dist, name = typhoon_threat_distance()
if dist < 100:
    send_ac("off", "cool", 26, "auto")  # Storm protection: auto-shutdown
```

## API Reference

### Setup
| Function | Description |
|----------|-------------|
| `init(baidu_key=None, api_key=None, qw_host=None, location=None, brand=None)` | Initialize config + start background scheduler. **Writes to `~/.ac_controller/config.json`**. Idempotent — safe to call multiple times. |

### AC Control (17 brands + IR learning)
| Function | Description |
|----------|-------------|
| `send_ac(power, mode, temp, fan)` | Send IR command. `power`: `"on"`/`"off"`. `mode`: `"cool"`/`"heat"`/`"dry"`/`"fan"`/`"auto"`. `temp`: 16-30. `fan`: `"auto"`/`"1"`/`"2"`/`"3"` |
| `decide_ac(outdoor_temp)` | Run temperature rules → returns `(target_temp, mode)` |
| `get_device()` | Get connected Broadlink device |

> `send_ac` covers the minimum universal set across all brands. For advanced features (turbo, swing, etc.), modify `ac_control.py` locally.

### IR Learning (support any brand)
| Function | Description |
|----------|-------------|
| `learn_one(host)` | Enter learning mode on Broadlink device, wait for IR signal → returns raw hex or `None` (timeout 45s) |
| `get_raw_code(name, power, mode, temp, fan)` | Look up learned hex code for a custom device |
| `load_custom_codes()` | Load all custom codes from `~/.ac_controller/custom_codes.json` |
| `save_custom_codes(data)` | Persist learned codes |
| `list_custom()` | List all custom device names |

> Use `ir_learner` to teach the system codes from any AC remote — no brand limits. Codes persist automatically and `send_ac` routes to learned codes when the current brand is a custom one.

### Weather & Alerts (Dual Source: Baidu + QWeather)
| Function | Description |
|----------|-------------|
| `fetch_weather()` | Current weather — auto-routes via Baidu/QWeather based on config |
| `fetch_weather_alerts()` | Local weather warnings — `[{headline, severity, description, ...}]` |

### Storm Tracking (Dual Source: China NMC + US NHC)
| Function | Description |
|----------|-------------|
| `fetch_typhoons()` | Active storms from NMC (NW Pacific) or NHC (Atlantic, configurable) |
| `fetch_typhoon_detail(typhoon_id)` | Detailed track + forecast points |
| `typhoon_threat_distance()` | **Agent-critical**: nearest storm distance (km) + name. < 100km = should shutdown. Never throws — returns `(99999, "")` on error |
| `calc_distance(lat1, lon1, lat2, lon2)` | Haversine distance |

### Logger
| Function | Description |
|----------|-------------|
| `write_log(category, msg)` | Append daily operation log (thread-safe) |
| `read_log(date_str)` | Read log by date |
| `get_log_dates()` | List dates with logs |

## Supported AC Brands (17)

**hvac_ir:** Gree, Midea, Hisense, Daikin, Mitsubishi, Hitachi, Fujitsu, Ballu, Carrier MCA, Hyundai, Fuego

**Custom protocols:** Haier, AUX, Panasonic (ported from IRremoteESP8266 C++)

**Multi-brand mappings:** Xiaomi, Hualing → Midea protocol; Carrier NQV → Carrier MCA

Select in Settings or pass `brand=` to `init()`. Supports Chinese and English names.

## Weather Providers

| Provider | Free Tier | Features |
|----------|-----------|----------|
| Baidu (default) | 5,000 calls/day | Real-time + forecast + alerts |
| QWeather | 50,000 calls/month | Real-time + forecast + alerts |

## Key Design

- `import broadlinkac_core` has **zero side effects** — no I/O, no threads
- `init()` is idempotent — safe to call multiple times
- Config auto-persisted to `~/.ac_controller/config.json` (atomic write)
- Runs on any device with Python 3.9+ (macOS/Windows/Linux/Raspberry Pi)
- `typhoon_threat_distance()` never throws — returns `(99999, "")` on any error
- Thread-safe logging with `threading.Lock`

## Common Agent Tasks

### "Is there a storm nearby? Should I turn off the AC?"
```python
from broadlinkac_core import init, typhoon_threat_distance, send_ac
init()
dist, name = typhoon_threat_distance()
if dist < 100:
    send_ac("off", "cool", 26, "auto")
    print(f"⚠️ {name} only {dist}km away — AC shut down for safety")
```

### "Turn on the AC and auto-adjust based on outdoor temperature"
```python
from broadlinkac_core import init, fetch_weather, decide_ac, send_ac
init()
w = fetch_weather()
if w:
    target, mode = decide_ac(float(w["temp"]))
    send_ac("on", mode, target, "auto")
```

### "What's the weather and are there any alerts?"
```python
from broadlinkac_core import init, fetch_weather, fetch_weather_alerts
init()
w = fetch_weather()
alerts, provider = fetch_weather_alerts()
for a in alerts:
    print(f"[{a['severity']}] {a['headline']}")
```

### "Learn IR codes for a custom AC brand"
```python
from broadlinkac_core.ir_learner import learn_one, save_learned_codes, get_raw_code

# Learn "OFF" signal
hex_off = learn_one("192.168.1.100")  # Broadlink device IP
save_learned_codes("MyAC", "gree", {"关机": hex_off})

# Learn "Cool 26°C Auto Fan"
hex_cool = learn_one("192.168.1.100")
save_learned_codes("MyAC", "gree", {"开机_制冷_26°C_自动": hex_cool})

# Send learned code
send_ac("on", "cool", 26, "auto")  # Routes to learned hex automatically
```

## Scheduling & Automation

> ⚠️ **All schedule changes are persistent** — they survive Python process exit and will be executed by the background scheduler daemon. Always confirm with the user before enabling or modifying schedules.

The background scheduler starts automatically after `init()`. Agent can read/write config directly.

### Read current schedule
```python
from broadlinkac_core import init
init()
dev = _cfg.config["devices"]["your_mac"]
print(dev.get("active_template"))     # Current template name
print(dev.get("schedule_enabled"))    # True/False
```

### Enable/disable schedule
```python
import broadlinkac_core.config as _cfg
from broadlinkac_core import init
init()
dev = _cfg.config["devices"]["your_mac"]
dev["schedule_enabled"] = True
_cfg.save_config(_cfg.config)
```

### Create a schedule template (multi-group)
```python
templates = _cfg.config.setdefault("schedule_templates", {})
templates["工作日"] = {
    "groups": [{
        "days": [1, 2, 3, 4, 5],         # Monday-Friday
        "slots": [{
            "on": "08:00", "on_enabled": True,
            "off": "18:00", "off_enabled": True
        }]
    }]
}
dev["active_template"] = "工作日"
_cfg.save_config(_cfg.config)
```

### Enable auto-adjust (every 2 hours based on outdoor temp)
```python
dev["auto_adjust"] = True
_cfg.save_config(_cfg.config)
```

## Desktop GUI

Pre-built installers (Windows/macOS/Linux), auto-built by GitHub Actions. Download from [Releases](https://github.com/oywq00008-cell/BroadlinkAC-For-Agent/releases/latest).

## OpenWRT Router Plugin

7×24 unattended AC control on OpenWRT routers. See [BroadlinkAC-OpenWRT](https://github.com/oywq00008-cell/BroadlinkAC-OpenWRT).
