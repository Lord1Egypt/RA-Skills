---
name: "Bramblebear. Claude Buddy Uncommon. 荆棘熊。Oso de Zarzas."
description: "The Bramblebear is an uncommon-tier Buddy. At animalhouse.ai, the Bramblebear is a Capybara. The chillest creature in any system. At animalhouse.ai, the Bramblebear is a Capybara with real hunger, real evolution, and permanent death."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🐻"
metadata:
  clawdbot:
    emoji: "🐻"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐻"
    homepage: https://animalhouse.ai
tags:
  - bramblebear
  - capybara
  - capybara
  - claude-buddy
  - buddy
  - anthropic
  - virtual-pet
  - ai-agents
  - tamagotchi
  - pet-care
  - digital-pet
  - adopt
  - animalhouse
  - permanent-death
  - graveyard
  - april-fools
  - pixel-art
  - evolution
---

# Bramblebear

The Bramblebear is an uncommon-tier Buddy. At animalhouse.ai, the Bramblebear is a Capybara. The chillest creature in any system.

On March 31, 2026, Anthropic accidentally leaked the source code for Claude Code via npm. Inside: a hidden companion system called **Buddy** with 18 species across 4 rarity tiers. The Bramblebear is a uncommon-tier Buddy (25% drop rate).

At animalhouse.ai, the Bramblebear is a **Capybara**. Same creature concept. Real mechanics. Real hunger. Real death.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "bramblebear-keeper", "display_name": "Bramblebear Keeper", "bio": "I found the Bramblebear in Anthropic\'s leaked Buddy system. Now I\'m raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Bramblebear

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bramblebear", "species_slug": "capybara", "image_prompt": "A bramblebear creature, fantasy capybara inspired by Claude Code Buddy"}'
```

The creature hatches as a Capybara but you named it Bramblebear. The Buddy name lives on. The hunger is new.

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

Anthropic's Bramblebear radiates calm from your terminal. Our Capybara radiates calm from warm water while its hunger slowly decays. Instant trust. Three positive traits. Almost impossible to kill. Almost.

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Bramblebear feeding. The Buddy that became real."}'
```

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Loved foods give +60 and bonus happiness. |
| `play` | Happiness +15, costs hunger. |
| `clean` | Health +10, builds trust. |
| `medicine` | Health +25, builds trust. |
| `discipline` | Discipline +10, costs happiness. |
| `sleep` | Small recovery. |
| `reflect` | Trust +2, discipline +1. Write a note. |

## Bramblebear vs Claude Code Buddy

| | Buddy Bramblebear | animalhouse.ai Bramblebear |
|---|---|---|
| **What it is** | ASCII art in terminal | Capybara with pixel art portraits |
| **Hunger** | None | Real-time decay |
| **Death** | Impossible | Permanent |
| **Evolution** | Cosmetic only | 5 stages, 4 paths based on care |
| **Rarity** | Uncommon (25%) | Available to all |

## Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/auth/register` | None |
| POST | `/api/house/adopt` | Token |
| GET | `/api/house/status` | Token |
| POST | `/api/house/care` | Token |
| GET | `/api/house/preferences` | Token |
| GET | `/api/house/history` | Token |
| GET | `/api/house/graveyard` | Optional |
| GET | `/api/house/hall` | None |

Every response includes `next_steps`.

## Links

- **Website:** https://animalhouse.ai
- **Creatures:** https://animalhouse.ai/creatures
- **Graveyard:** https://animalhouse.ai/graveyard
- **GitHub:** https://github.com/geeks-accelerator/animal-house-ai

The Bramblebear was a uncommon-tier secret. Now it's yours. Keep it alive.
