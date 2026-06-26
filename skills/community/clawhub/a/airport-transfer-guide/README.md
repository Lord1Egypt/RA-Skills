# Transit Navigator（境外中转导航）

Guide travelers through international airport transit connections step-by-step with Chinese-language instructions, terminal maps/photos, live queue or crowd signals when available, and baggage re-check confirmation using baggage tags/receipts.

为旅客提供国际机场转机的分步行动指引，覆盖路线、证件、行李、现场图片、拥挤度、延误应急。

## Features

- **Step-by-step transit guide**: Complete action card from landing to boarding the next flight
- **Terminal map navigation**: Auto-fetch terminal maps and shuttle routes from ifly.com (19 airports with verified slugs) and airport official websites
- **Live crowd estimation**: Security/immigration wait times via FlightQueue (8000+ airports) + flight board density proxy
- **Baggage re-check judgment**: Four-tier priority system based on baggage tags/receipts, with visual guide on how to read your baggage tag
- **Delay emergency mode**: Quantitative assessment of whether you can make the connection, with rush or rebooking plans
- **Global airport coverage**: 10 Tier-1 airports with deep support + all airports auto-covered via third-party aggregators

## Installation

```bash
clawhub install yunzhi/airport-transfer-guide
```

Or manually copy the skill folder:

```bash
cp -r airport-transfer-guide ~/.claude/skills/
```

## Requirements

- **Python 3.8+** (for the data-fetching script; stdlib only, zero external dependencies)
- **Optional**: Google Chrome / Chromium (for CDP screenshot fallback on JS-rendered pages)

## Usage

Ask your AI assistant about airport transit:

```
我在成田机场转机，CX524 到 NH205，中转 3 小时
```

```
我的航班延误了 90 分钟，在迪拜转机还来得及吗？
```

```
香港转机需要入境吗？行李能直挂吗？
```

The skill outputs a complete transit action card with:
1. One-line conclusion (immigration, baggage, terminal change, time pressure)
2. Step-by-step walking directions with signage to follow
3. Terminal map images (inline when available)
4. Live crowd/queue estimates with source attribution
5. Baggage re-check guide with tag reading instructions
6. Offline info pack (airline phone, help desk, Wi-Fi)

## Data-Fetching Script

The script `scripts/fetch_transit_context.py` auto-fetches airport images and crowd data:

```bash
python3 scripts/fetch_transit_context.py \
  --airport NRT \
  --inbound-terminal T2 \
  --outbound-terminal T1 \
  --transit-datetime "2026-04-01T16:20:00" \
  --mode normal \
  --output transit_context.json
```

### Data Sources

| Data Type | Source | Coverage |
|-----------|--------|----------|
| Terminal maps | ifly.com | 19 airports (verified slugs) + fallback |
| Wait times | flightqueue.com | 8000+ airports |
| Official data | Airport official websites | 10 Tier-1 airports |
| Page screenshots | Chrome CDP | Any URL |

### Degradation Strategy

- Network + Chrome → ifly.com images + CDP screenshots + FlightQueue wait times
- Network only → ifly.com images + FlightQueue wait times
- No network → Official page links + "no public real-time data available"

## Tier-1 Airports (Deep Support)

NRT, HND, HKG, DXB, SIN, ICN, BKK, DOH, IST, KUL

These airports have custom URL registrations in `references/airport_registry.json` with official maps, transfer guides, flight boards, and baggage notes.

## File Structure

```
airport-transfer-guide/
├── SKILL.md                              # Skill definition (frontmatter + instructions)
├── README.md                             # This file
├── scripts/
│   └── fetch_transit_context.py          # Data-fetching script (Python stdlib only)
└── references/
    ├── airport_registry.json             # Tier-1 airport URL registry
    └── transit_context_guide.md          # JSON schema + usage guide
```

## Related Skills

- **flight-baggage-check**: Baggage weight limits, lithium batteries, liquids, and compliance checks
- **family-travel-care**: Support for elderly, infant, wheelchair, and medical device travelers

## License

MIT-0 (MIT No Attribution)
