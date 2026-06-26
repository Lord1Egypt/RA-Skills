# Daily Movie — Movie & TV Recommendation Skill

> One curated film or series pick every day — synopsis, Douban + IMDb ratings, where to stream. Bilingual EN/CN.

[![clawhub](https://img.shields.io/badge/clawhub-daily--movie-blue)](https://clawhub.ai/skills/daily-movie)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

An [OpenClaw](https://openclaw.ai) skill that recommends one movie and one TV series every day — with synopsis, Douban/IMDb ratings, platform availability, and a spoiler-free reason to watch. High open rate by design: everyone wants to know what to watch tonight.

---

## Features

- **Daily Pick** — 1 movie + 1 series per day, genre rotates by weekday
- **Ratings** — Douban + IMDb scores
- **Spoiler-Free** — Synopsis without plot reveals
- **Platform Guide** — Where to watch (Netflix, iQiyi, Youku, etc.)
- **Evening Pick** — Lighter recommendation for tonight + weekend preview
- **Bilingual** — Chinese and English

---

## Daily Push Schedule

| Push | Time | Content |
|------|------|---------|
| Morning | 10:00 | Today's movie + series recommendation |
| Evening | 19:00 | Tonight's watch + weekend new releases preview |

```bash
node scripts/push-toggle.js on <userId>
node scripts/push-toggle.js on <userId> --morning 10:00 --evening 19:00 --channel feishu
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

Supported channels: `telegram` / `feishu` / `slack` / `discord`

---

## Weekly Genre Rotation

| Day | Genre |
|-----|-------|
| Mon | 励志 Inspiring |
| Tue | 悬疑惊悚 Thriller |
| Wed | 爱情 Romance |
| Thu | 喜剧 Comedy |
| Fri | 动作科幻 Action/Sci-Fi |
| Sat | 经典名作 Classics |
| Sun | 家庭纪录片 Family/Documentary |

---

*MIT License · OpenClaw Skill*

## Keywords

movie recommendation · what to watch · film recommendation · daily movie · Netflix · Korean drama · 电影推荐 · 今天看什么 · 今晚看什么 · 豆瓣高分 · 剧推荐 · 看什么电影

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/daily-movie)
