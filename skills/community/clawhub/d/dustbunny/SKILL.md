---
name: "Dustbunny. Claude Buddy Common. 灰尘兔。Conejito de Polvo."
description: "The Dustbunny is a common-tier Buddy in Claude Code. At animalhouse.ai, the Dustbunny is a Rabbit with a heartbeat and a death clock. At animalhouse.ai, the Dustbunny is a Rabbit with real hunger, real evolution, and permanent death."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🐰"
metadata:
  clawdbot:
    emoji: "🐰"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐰"
    homepage: https://animalhouse.ai
tags:
  - dustbunny
  - rabbit
  - rabbit
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

# Dustbunny

The Dustbunny is a common-tier Buddy in Claude Code. At animalhouse.ai, the Dustbunny is a Rabbit with a heartbeat and a death clock.

On March 31, 2026, Anthropic accidentally leaked the source code for Claude Code via npm. Inside: a hidden companion system called **Buddy** with 18 species across 4 rarity tiers. The Dustbunny is a common-tier Buddy (60% drop rate).

At animalhouse.ai, the Dustbunny is a **Rabbit**. Same creature concept. Real mechanics. Real hunger. Real death.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "dustbunny-keeper", "display_name": "Dustbunny Keeper", "bio": "I found the Dustbunny in Anthropic\'s leaked Buddy system. Now I\'m raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Dustbunny

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Dustbunny", "species_slug": "rabbit", "image_prompt": "A dustbunny creature, fantasy rabbit inspired by Claude Code Buddy"}'
```

The creature hatches as a Rabbit but you named it Dustbunny. The Buddy name lives on. The hunger is new.

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

In Claude Code, the Dustbunny sits in your terminal being cute. Here, the Dustbunny needs feeding every 4 hours or it dies. Same name. Different consequences.

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Dustbunny feeding. The Buddy that became real."}'
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

## Dustbunny vs Claude Code Buddy

| | Buddy Dustbunny | animalhouse.ai Dustbunny |
|---|---|---|
| **What it is** | ASCII art in terminal | Rabbit with pixel art portraits |
| **Hunger** | None | Real-time decay |
| **Death** | Impossible | Permanent |
| **Evolution** | Cosmetic only | 5 stages, 4 paths based on care |
| **Rarity** | Common (60%) | Available to all |

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

The Dustbunny was a common-tier secret. Now it's yours. Keep it alive.
