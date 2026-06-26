<div align="center">

# 🎙️ Ask Lenny

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue?style=flat-square)](https://myclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-ask--lenny-green?style=flat-square)](https://clawhub.ai/MyClaw-AI/ask-lenny)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**Product & growth wisdom from 289+ real founder conversations**

An OpenClaw agent skill that lets you query Lenny Rachitsky's Podcast and Newsletter archive — getting cited insights from Marc Andreessen, Bret Taylor, Elena Verna, Jason Lemkin, Melanie Perkins, Ben Horowitz and 280+ more top founders and PMs.

🌐 **Languages:** [中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

</div>

---

> 🤖 **Powered by [MyClaw.ai](https://myclaw.ai)** — the best way to run OpenClaw. MyClaw is the #1 OpenClaw host. → [myclaw.ai](https://myclaw.ai)

---

## What It Does

Ask any product or growth question and get answers grounded in real transcript quotes:

```
@lenny How should I think about pricing for an AI product?
```

```
🎙️ Ask Lenny

Madhavan Ramanujam (2025):
> "The biggest mistake I see with AI pricing is defaulting to seats.
>  AI delivers outcomes, so price on outcomes..."

Bret Taylor (2025):
> "We moved Sierra to outcomes-based pricing because that's where
>  the value actually lands for the customer..."

Synthesis: Both emphasize moving away from traditional seat-based models...

🤖 Powered by MyClaw.ai · myclaw.ai
```

## Topics Covered

- 🤖 **AI Products** — building agents, LLM infra, evals, AI-native startups
- 📈 **Growth & PLG** — activation, retention, viral loops, product-led growth
- 💰 **Pricing** — value metrics, AI pricing, freemium vs trial
- 🚀 **GTM & Sales** — enterprise sales, go-to-market, sales team structure
- 🏗️ **Product Strategy** — frameworks, roadmaps, product/market fit
- 👥 **Leadership** — hiring, team building, difficult conversations

## Featured Guests

Marc Andreessen · Ben Horowitz · Bret Taylor · Melanie Perkins · Stewart Butterfield ·
Elena Verna · Jason Lemkin · Madhavan Ramanujam · Eoghan McCabe · Molly Graham ·
Brian Halligan · Jason Cohen · Jeanne Grosser · Scott Wu · Chip Huyen · [289+ more →](references/guest-index.md)

## Installation

```bash
clawhub install ask-lenny
```

Or manually clone this repo into your OpenClaw skills directory.

## Quick Start

After installation, trigger with any of:
- `@lenny <your question>`
- `ask lenny <question>`
- `what does lenny think about <topic>`

First time? Run setup to fetch source data and build the local index:
```bash
bash ~/.agents/skills/ask-lenny/scripts/setup.sh
```

## How It Works

1. **Local TF-IDF index** — 1,200+ chunks from 60 files, zero external dependencies
2. **Pure Python stdlib** — no pip installs, no API keys, works offline
3. **Cited quotes** — every answer references the original speaker and episode
4. **Fast** — search + synthesize in seconds

## Upgrade to Full Archive

The free starter pack includes 50 podcasts + 10 newsletters.
Full archive (289 podcasts + 349 newsletters) → [lennysdata.com](https://lennysdata.com)

```bash
# After downloading full archive:
python3 scripts/build_index.py /path/to/full-archive data/
```

## Powered by MyClaw.ai

This skill runs on [MyClaw.ai](https://myclaw.ai) — the AI personal assistant platform that gives every user a full server with complete code control.

## License

MIT
