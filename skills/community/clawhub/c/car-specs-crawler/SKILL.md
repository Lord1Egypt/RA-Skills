---
name: car-specs-crawler
description: Fetch car specifications from Chinese automotive websites (懂车帝 dongchedi.com and 汽车之家 autohome.com.cn). Use when the user needs to collect vehicle configuration data such as price, dimensions, battery capacity, range, seating layout, or top speed. Triggers on requests like "crawl car specs", "fetch vehicle parameters", "get car configuration", "爬取汽车配置", "获取车型参数", or when building car comparison PPTs/reports that need real-time data from auto websites.
---

# Car Specs Crawler

## Overview

This skill provides a Python script that crawls car specifications from major Chinese automotive websites (懂车帝, 汽车之家). It searches by car model name, extracts key parameters, and outputs them as JSON or markdown tables for use in comparison reports, PPTs, or spreadsheets.

## Supported Parameters

The crawler extracts these common fields when available:
- **价格** (Price / MSRP)
- **能源类型** (Energy type: EV, PHEV, ICE, etc.)
- **座位** (Seating layout)
- **车身尺寸** (Dimensions L×W×H in mm)
- **轴距** (Wheelbase)
- **最高车速** (Top speed)
- **电池容量** (Battery capacity in kWh)
- **续航** (CLTC/NEDC/WLTP range in km)
- **电机功率** (Motor power in kW)
- **扭矩** (Torque in N·m)
- **百公里加速** (0-100 km/h acceleration)
- **充电时间** (Charging time)

## Usage

### Basic: Single Car

```bash
python3 scripts/fetch-car-specs.py "小米YU7 Pro"
```

### Compare Multiple Cars

```bash
python3 scripts/fetch-car-specs.py "华为问界M7 纯电" "小米YU7 Pro" "特斯拉Model Y"
```

### Output as JSON

```bash
python3 scripts/fetch-car-specs.py "小米YU7 Pro" --format json
```

### Specify Source

```bash
# Only 懂车帝
python3 scripts/fetch-car-specs.py "小米YU7 Pro" --source dongchedi

# Only 汽车之家
python3 scripts/fetch-car-specs.py "小米YU7 Pro" --source autohome
```

### Save to File

```bash
python3 scripts/fetch-car-specs.py "小米YU7 Pro" --format json --output specs.json
```

## Integration Workflow (for PPT/Report Building)

When building a car comparison PPT or report:

1. **Run the crawler** for each car model:
   ```bash
   python3 scripts/fetch-car-specs.py "车型A" "车型B" --format table
   ```

2. **Parse the markdown table** output and feed it into the report/PPT builder.

3. **Cross-check with official websites** if critical specs are missing — the crawler falls back between sources automatically.

## Notes

- The script uses `requests` + `lxml` (standard packages, usually pre-installed).
- If a source site changes its HTML structure, the XPath selectors may need updating.
- Rate limiting: the script sleeps 0.5s between requests to be polite to the target sites.
- Some fields may be missing if the source page does not display them.

## Resources

### `scripts/fetch-car-specs.py`
The main crawler script. Run directly with car model names as arguments.

### `references/xpath-patterns.md` (optional)
If the target sites change their HTML structure, update the XPath selectors in this reference file, then patch the script accordingly.
