# Daily Idiom — Chinese Idiom Learning Skill

> One Chinese idiom (成语) every day — story, usage, examples, quiz. Perfect for Chinese learners.

[![clawhub](https://img.shields.io/badge/clawhub-daily--idiom-blue)](https://clawhub.ai/skills/daily-idiom)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

An [OpenClaw](https://openclaw.ai) skill for learning one Chinese idiom (成语) or proverb every day — with origin story, modern usage, example sentences, and an evening quiz. Perfect for Chinese learners, culture enthusiasts, and anyone who wants to level up their Mandarin.

---

## Features

- **Daily Idiom** — One 成语/俗语/谚语 per day, theme-based by weekday
- **Origin Story** — Historical/literary background (50–80 words)
- **Bilingual** — Chinese original + English translation (meaning, not literal)
- **Usage Guide** — When and how to use it in modern context
- **Example Sentences** — 2 sentences with translations
- **Memory Tip** — Mnemonic or word-root breakdown
- **Evening Quiz** — 3-question review with answers and explanations

---

## Daily Push Schedule

| Push | Time | Content |
|------|------|---------|
| Morning | 08:00 | Today's idiom + story + usage + quiz teaser |
| Evening | 21:00 | Quiz on today's idiom + tomorrow's preview hint |

```bash
node scripts/push-toggle.js on <userId>
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 21:00 --channel feishu
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

Supported channels: `telegram` / `feishu` / `slack` / `discord`

---

## Weekly Themes

| Day | Theme |
|-----|-------|
| Mon | 励志 Motivation |
| Tue | 智慧 Wisdom |
| Wed | 友情 Friendship |
| Thu | 财富 Wealth |
| Fri | 趣味 Fun |
| Sat | 历史 History |
| Sun | 生活 Daily Life |

---

*MIT License · OpenClaw Skill*

## Keywords

Chinese idiom · chengyu · 成语 · daily idiom · Chinese learning · learn Chinese · Chinese proverb · 每日成语 · 成语故事 · 俗语 · 中文学习 · idiom of the day

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/daily-idiom)
