# Accountability Buddy 🤝

An OpenClaw skill that acts as your learning accountability partner — tracking streaks, sending check-ins, and celebrating wins.

## What It Does

- **Daily check-ins** — Morning reminders, evening progress logs
- **Streak tracking** — Count consecutive days, celebrate milestones
- **Slip support** — Encouragement when you miss a day
- **Weekly reviews** — Reflect on progress, adjust goals

## Quick Start

```
"Start accountability for learning Python"
"I did my learning today"
"Check my streak"
"Weekly review"
```

## Example Interaction

**Day 1:**
> **You:** Start accountability for Python, 30 min/day
> **Buddy:** Awesome! Let's lock it in:
> - Topic: Python
> - Daily goal: 30 min
> - Start: Today (March 30)
>
> I'll check in each morning and evening. You got this! 🦀

**Day 3:**
> **Buddy:** 🔥 3-day streak! You're building a habit. How's Python going?
> **You:** Learned loops today!
> **Buddy:** Nice! Loops are where it gets fun. See you tomorrow.

**Day 8 (missed day):**
> **You:** Missed yesterday
> **Buddy:** Life happens. The gap between 'missed' and 'quit' is huge.
>
> What's the plan for today? Even 5 minutes keeps the momentum.

**Day 30:**
> **Buddy:** 🏆 30-DAY STREAK! You're unstoppable!
>
> You showed up every day for a month. That's not just learning — that's who you are now.

## Why Accountability Works

- **Public commitment** — Telling someone makes it real
- **Streak psychology** — We hate breaking streaks
- **Gentle pressure** — A nudge when motivation fades
- **Celebration** — Wins feel better when noticed

## Philosophy

**Consistency > Intensity**

- 10 minutes daily beats 2 hours weekly
- Any progress counts
- Missing a day isn't failure — quitting is

## Installation

```bash
clawhub install accountability-buddy
```

Or manually:
```bash
git clone https://github.com/thinktankglobalbot/accountability-buddy-skill.git
cp -r accountability-buddy-skill ~/.openclaw/skills/accountability-buddy
```

## Data Storage

Progress is stored locally in:
```
~/.openclaw/skills/accountability-buddy/data/progress.json
```

## Future Features (Roadmap)

- [ ] Pair with real accountability partner
- [ ] Export progress to calendar
- [ ] Integration with Learn Anything skill
- [ ] Streak rewards/badges
- [ ] Group accountability (learning pods)

## License

MIT — use freely, modify, share.

---

Built with 🦀 for OpenClaw
