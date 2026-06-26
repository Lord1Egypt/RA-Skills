# FocusTimer — Pomodoro Timer via Agent

Your agent manages your focus blocks. No timer app needed.

## Usage

```
You: "Start a focus block — working on the API redesign"
Agent: "🍅 Focus started: API redesign. 25 minutes."

[25 minutes later]

Agent: "⏰ Done! 25 min on API redesign. 3 blocks today (1h 15m total). 
        Take a 5-min break. Ready for another?"
```

## Features

- **Conversational control** — start, pause, skip break
- **Session tracking** — what, how long, when
- **Daily reports** — total focus time, blocks, topics
- **Weekly trends** — "12 hours this week, up from 9"
- **Task tagging** — time per project
- **Break reminders** — nudge to actually rest

## Configuration

```yaml
focus_duration: 25
short_break: 5
long_break: 15    # every 4 blocks
daily_goal: 8     # blocks
```

## Daily Report

```
🍅 Focus Report — Feb 28
Blocks: 6/8 (75%)
Total: 2h 30m
Topics: API redesign (3), docs (2), email (1)
Peak: 9:00-11:30 AM
```
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
