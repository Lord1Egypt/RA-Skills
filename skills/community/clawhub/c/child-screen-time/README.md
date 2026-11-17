# Child Screen Time Negotiator 📱👶

Stop fighting over screen time. This tool turns it into a fair, transparent
system where kids **earn** entertainment time through good behavior, chores,
and learning — while educational screen time stays generous.

## The Problem

Every parent struggles with screen time:
- **"Just five more minutes!"** — turning into an hour
- **Arbitrary limits** — kids feel punished, parents feel like wardens
- **No distinction** — Minecraft and Khan Academy count the same
- **Power struggles** — every transition is a battle
- **No accountability** — kids don't see the big picture

## The Solution

A two-category budget system with an earned-time economy:

1. **Educational time** (Khan Academy, coding, languages) — generous limits
2. **Entertainment time** (games, YouTube) — earned through good behavior

Kids negotiate for more time through a fair, rules-based system instead of
whining. Parents get data-driven report cards and automatic tracking.

## Features

- 👶 **Per-child profiles** — age-appropriate limits based on AAP guidelines
- 📚 **Two-category tracking** — educational vs. entertainment
- ⭐ **Earned-time economy** — bonus minutes for chores, homework, reading
- 🤝 **Negotiation system** — kids request more time, system evaluates fairly
- 📊 **Report cards** — weekly compliance scores with praise and improvement areas
- 📅 **Usage history** — track patterns over time
- 🏆 **Compliance scoring** — rewards smooth transitions and rule-following
- 👨‍👩‍👧‍👦 **Multi-child** — compare siblings fairly

## Quick Start

```bash
# Set up your family
python3 scripts/screen_time.py add-child Alice 10
python3 scripts/screen_time.py set-limit Alice 120  # 2h entertainment

# Daily usage
python3 scripts/screen_time.py log Alice 45 "Minecraft" fun
python3 scripts/screen_time.py log Alice 30 "Khan Academy" edu
python3 scripts/screen_time.py award Alice 15 "finished homework early"
python3 scripts/screen_time.py status Alice

# Alice negotiates for more time
python3 scripts/screen_time.py negotiate Alice 30 "want to play with friend online"

# Weekly report card
python3 scripts/screen_time.py report-card Alice 7
```

## AAP Guidelines Used

| Age | Max Entertainment Screen Time |
|-----|-------------------------------|
| Under 2 | None (video chatting OK) |
| 2–5 | 60 min/day (co-viewing recommended) |
| 6–9 | 90 min/day |
| 10–13 | 120 min/day |
| 14–17 | 150 min/day |

See [`references/aap-guidelines.md`](references/aap-guidelines.md) for details.

## Requirements

- Python 3.6+ (stdlib only, no pip packages)

## License

MIT © Denis Voronin
