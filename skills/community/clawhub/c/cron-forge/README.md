# CronForge — Visual Cron Job Builder for OpenClaw

Nobody remembers cron syntax. CronForge gives you copy-paste templates for every common schedule, plus a plain-English reference so you never have to google "cron every other Tuesday" again.

## The Problem

```
# What does this do?
0 */4 * * 1-5
# Nobody knows without looking it up
```

## The Solution

```
# CronForge template: every 4 hours on weekdays
Schedule: weekday-4h
Cron: 0 */4 * * 1-5
Plain English: "Every 4 hours, Monday through Friday"
```

## Templates

### Intervals
| File | Schedule | Use Case |
|------|----------|----------|
| `interval-5m.md` | Every 5 minutes | Critical monitoring |
| `interval-15m.md` | Every 15 minutes | Active monitoring |
| `interval-30m.md` | Every 30 minutes | Standard heartbeat |
| `interval-1h.md` | Every hour | Hourly checks |
| `interval-4h.md` | Every 4 hours | Periodic tasks |

### Daily
| File | Schedule | Use Case |
|------|----------|----------|
| `daily-morning.md` | 7 AM daily | Morning briefing |
| `daily-evening.md` | 6 PM daily | End-of-day summary |
| `daily-midnight.md` | Midnight | Cleanup, rotation |

### Weekly
| File | Schedule | Use Case |
|------|----------|----------|
| `weekly-monday.md` | Monday 9 AM | Week planning |
| `weekly-friday.md` | Friday 5 PM | Week review |
| `weekend-check.md` | Sat & Sun noon | Light weekend check |

### Monthly
| File | Schedule | Use Case |
|------|----------|----------|
| `monthly-first.md` | 1st at 9 AM | Monthly report |
| `monthly-last.md` | Last day at 5 PM | Month close |

## Cron Syntax Cheat Sheet

```
┌──────── minute (0-59)
│ ┌────── hour (0-23)
│ │ ┌──── day of month (1-31)
│ │ │ ┌── month (1-12)
│ │ │ │ ┌ day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

| Symbol | Meaning | Example |
|--------|---------|---------|
| `*` | Every | `* * * * *` = every minute |
| `*/N` | Every N | `*/15 * * * *` = every 15 min |
| `N` | Specific | `0 9 * * *` = at 9:00 |
| `N-M` | Range | `0 9 * * 1-5` = weekdays at 9 |
| `N,M` | List | `0 9,17 * * *` = 9 AM and 5 PM |

## OpenClaw Integration

```bash
# Create a cron job in OpenClaw
openclaw cron add --schedule "0 9 * * *" --prompt "Check email and summarize" --model haiku

# List active crons
openclaw cron list

# Remove a cron
openclaw cron remove <id>
```

## Pro Tips

- Use **Haiku** for routine crons (cheap). Save Opus for complex analysis.
- Stagger crons by a few minutes to avoid rate limits: 9:00, 9:05, 9:10 instead of all at 9:00.
- Add `--session` flag to run crons in their own session (isolated context).
- Test cron expressions at crontab.guru before deploying.
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
