# Daily Reflect — Daily Journal Prompts Skill

> Morning writing prompts and evening reflections to build a daily journaling habit.

[![clawhub](https://img.shields.io/badge/clawhub-daily--reflect-blue)](https://clawhub.ai/skills/daily-reflect)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

An [OpenClaw](https://openclaw.ai) skill that guides you through daily journaling — a morning writing prompt to set intentions, and an evening reflection to review your day. Designed to build a sustainable journaling habit with the highest user retention of any daily skill type.

---

## Features

- **Morning Prompts** — Theme-based writing guide (7 weekly themes: intention / gratitude / challenge / connection / weekly review / dreams / inner voice)
- **Evening Reflection** — 3-question daily review, emotion check-in, next-day intention
- **Streak Tracking** — Daily check-in motivation
- **Non-judgmental Tone** — Warm, open, inclusive writing guidance
- **Bilingual** — Chinese and English

---

## Daily Push Schedule

| Push | Time | Content |
|------|------|---------|
| Morning | 09:00 | Today's journal theme + 3 guiding questions + writing starter |
| Evening | 21:00 | Day review + emotion score + tomorrow's intention |

```bash
node scripts/push-toggle.js on <userId>
node scripts/push-toggle.js on <userId> --morning 09:00 --evening 21:00 --channel telegram
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

Supported channels: `telegram` / `feishu` / `slack` / `discord`

---

## Trigger Words

日记、写日记、今天写什么、每日日记、日记打卡、自我反思、情绪日记、每日复盘、journal、journaling、writing prompt、morning journal、evening reflection、gratitude journal、self-reflection

---

*MIT License · OpenClaw Skill*

## Keywords

daily journal · journaling · journal prompts · writing prompts · daily reflection · self-awareness · gratitude · 日记 · 写日记 · 每日日记 · 自我反思 · 日记打卡

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/daily-reflect)
