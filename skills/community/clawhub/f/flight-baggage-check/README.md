# Flight Baggage Check（行李合规检查）

Check airline baggage compliance, carry-on vs checked rules, excess baggage, and the cheapest compliant packing plan.

把"这个能不能带""超重了怎么办"直接整理成可执行结论，不绕弯。

## Features

- **Item-by-item compliance check**: Instant pass/fail judgment for each item (liquids, aerosols, batteries, drones, sports gear, etc.)
- **Weight overcheck detection**: Automatically flags overweight baggage and calculates excess
- **Cost-optimized solutions**: Ranks solutions by cost — free options first, then paid options from cheapest to most expensive
- **Battery Wh calculation**: Automatic watt-hour calculation for power banks, drone batteries, and lithium cells
- **Multi-leg flight support**: Checks rules for the most restrictive leg
- **Airline-specific rules**: Covers major airlines with IATA fallback for unknown carriers
- **Structured output**: Three-section format (Compliance Verdict → Recommended Plan → Special Notes)

## Installation

```bash
clawhub install yunzhi/flight-baggage-check
```

Or manually copy the skill folder:

```bash
cp -r flight-baggage-check ~/.claude/skills/
```

## Usage

Ask your AI assistant about baggage rules:

```
我坐国泰经济舱去曼谷，行李箱24kg，有充电宝26800mAh和防晒喷雾，能带吗？
```

```
带无人机DJI Mini 4 Pro和3块电池坐南航去新疆，行李28kg，怎么打包？
```

```
两瓶红酒能托运吗？春秋航空经济舱。
```

The skill outputs:
1. **Compliance verdict** — pass/fail for each item with reason
2. **Recommended plan** — cheapest compliant packing strategy (free options first)
3. **Special notes** — security tips, flight rules, airline screenshots

## File Structure

```
flight-baggage-check/
├── SKILL.md          # Skill definition (frontmatter + instructions)
└── README.md         # This file
```

## Related Skills

- **travel-outfit-planner**: Generates packing lists that can be checked by this skill
- **airport-transfer-guide**: Transit baggage re-check rules
- **family-travel-care**: Medication and baby food exemptions

## License

MIT-0 (MIT No Attribution)
