# Family Travel Care（特殊旅客关怀）

Itinerary-first flight support for babies, children, elderly passengers, reduced-mobility travelers, and people carrying medication or medical devices.

把用户这趟行程串成一个可执行方案：现在要做什么、什么时候申请、准备什么、到机场怎么说。

## Features

- **Companion-aware service guide**: Tailored services for infants (0-2), children (2-12), mobile elderly (65+), and reduced-mobility passengers
- **Free services surfacing**: Bassinets, priority boarding, wheelchair assistance, special meals, extra infant baggage — all listed with how-to and deadlines
- **Paid upgrade analysis**: Cost-benefit comparison of lounges, premium economy, extra legroom — only when meaningful for the specific group
- **Document checklist**: Infant passport, birth certificate, medical certificates, prescription medication letters — with bilingual (CN/EN) templates
- **Medication quick-judgment**: A/B/C tier classification for common medications with carry-on rules and security declaration cards
- **Low-cost airline awareness**: Detects budget carriers and adjusts all service recommendations accordingly
- **Action timeline**: What to do now, 48h before, and at the airport

## Installation

```bash
clawhub install yunzhi/family-travel-care
```

Or manually copy the skill folder:

```bash
cp -r family-travel-care ~/.claude/skills/
```

## Usage

Ask your AI assistant about traveling with dependents:

```
带8个月宝宝和70岁妈妈坐国泰经济舱从上海经香港转机去伦敦，妈妈膝盖不好
```

```
5岁小朋友第一次坐飞机，春秋航空去三亚，有轻微哮喘需要带药
```

```
带轮椅的老人坐东航去北京，需要什么服务和证件？
```

The skill outputs:
1. **Free services** — per companion type, with request method and deadline
2. **Recommended upgrades** — price/value analysis, only when meaningful
3. **Documents checklist** — with bilingual templates
4. **Medication guide** — quick-judgment table + security declaration card
5. **Action timeline** — now / 48h before / at airport

## File Structure

```
family-travel-care/
├── SKILL.md          # Skill definition (frontmatter + instructions)
└── README.md         # This file
```

## Related Skills

- **travel-outfit-planner**: Baby supplies and elderly comfort items in packing
- **flight-baggage-check**: Medication and baby food exemptions
- **airport-transfer-guide**: Wheelchair timing and family facility locations during transit

## License

MIT-0 (MIT No Attribution)
