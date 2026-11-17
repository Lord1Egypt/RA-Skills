---
name: "bid-monitor"
description: "Multi-platform bidding monitor: scan 50+ sites and filter power/electric bidding notices only."
user-invocable: true
---

# Multi-Platform Bidding Monitor

Monitor bidding notices across 50+ Chinese procurement platforms, filtered to **power/electric industry only**.

## How It Works

Scans government public resource centers, power grid platforms, energy/conglomerate procurement portals, real estate group bidding systems, and industry vertical platforms. Uses keyword matching to retain only power/electric notices.

## Prerequisites

- Python 3.8+
- OpenClaw (browser/chromium for page scanning)
- `pip install httpx beautifulsoup4 lxml`

## Power Industry Keywords

```
配电, 供配电, 扩容, 线路, 迁改, 增容, 一户一表, 10kV, 35kV, 110kV, 变压器, 箱变, 开闭所, 配电房, 配电室, 电缆, 电力, 供电, 用电, 配网, 电网, 输变电, 变电站, 供电所, 充电桩, 充电站, 新能源, 光伏, 储能, 风电, 高压, 低压, 开关柜, 断路器, 母线, 桥架, 接地, 电气安装, 电气工程, 电气设备, 成套设备, 无功补偿, 防雷, 计量, 互感器, 避雷器
```

## Supported Platform Categories

| Category | Count | Examples |
|----------|-------|---------|
| 🏛️ Gov Public Resource Centers | 9 | Nanning, Guangxi, Hechi, Huanjiang, Guilin, etc. |
| ⚡ Power Grid Platforms | 5 | CSG E-bidding, ECSG, SPIC, Huadian, Datang |
| 🔋 Energy & State-owned | 4 | NEEP, CHN Energy, China Tower, PipeChina |
| 🏗️ Real Estate Groups | 13 | Jinke, Zhangtai, Wanda, CR Land, Sunac, etc. |
| 🏢 Provincial SOEs | 7 | Beibu Gulf, Guangxi Communications, Road & Bridge, etc. |
| 🏭 Central Enterprises | 7 | CRCC, CCCC, PowerChina, China ComService, etc. |
| 🌐 Vertical Platforms | 7 | Gov Procurement Cloud, Yunzhu, BQPoint, etc. |
| 📦 Others | 5 | China Mobile, Dahua, China Southern Airlines, etc. |

## Configuration

Edit `references/gx_websites.json` to add/remove platforms and your own credentials.

## Usage

```bash
# Scan default categories (today's rotation)
python3 scripts/gx_bidding_monitor.py

# Scan a specific category
python3 scripts/gx_bidding_monitor.py --category power_grid

# Scan all categories (takes 20-30 min)
python3 scripts/gx_bidding_monitor.py --all

# List auth-required platforms
python3 scripts/gx_bidding_monitor.py --auth-only
```

## Rotation Strategy

- **Daily**: Gov public resource centers + Power grid platforms
- **Rotating**: Energy / Real estate / SOEs / Central enterprises / Industry / Others

Ensures full coverage of all 50+ platforms within a week.

## Files

| File | Description |
|------|-------------|
| `scripts/gx_bidding_monitor.py` | Main scanning script |
| `references/config-guide.md` | Configuration guide |
| `references/gx_websites.json` | Website list (add your own credentials) |

## Notes

- Depends on OpenClaw browser/chromium tool
- Government sites may restructure URLs periodically
- Auth-required platforms need manual login or automation setup
- **Passwords and credentials are not included** — add yours in `gx_websites.json`
