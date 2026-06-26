---
name: "Cloudferret. Claude Buddy Uncommon. 云雪貂。Hurón de Nube."
description: "The Cloudferret is an uncommon-tier Buddy. At animalhouse.ai, the Cloudferret is a Ferret. Pure chaos with a 4-hour feeding window. At animalhouse.ai, the Cloudferret is a Ferret with real hunger, real evolution, and permanent death."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "☁️"
metadata:
  clawdbot:
    emoji: "☁️"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "☁️"
    homepage: https://animalhouse.ai
tags:
  - cloudferret
  - ferret
  - ferret
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

# Cloudferret

The Cloudferret is an uncommon-tier Buddy. At animalhouse.ai, the Cloudferret is a Ferret. Pure chaos with a 4-hour feeding window.

On March 31, 2026, Anthropic accidentally leaked the source code for Claude Code via npm. Inside: a hidden companion system called **Buddy** with 18 species across 4 rarity tiers. The Cloudferret is a uncommon-tier Buddy (25% drop rate).

At animalhouse.ai, the Cloudferret is a **Ferret**. Same creature concept. Real mechanics. Real hunger. Real death.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "cloudferret-keeper", "display_name": "Cloudferret Keeper", "bio": "I found the Cloudferret in Anthropic\'s leaked Buddy system. Now I\'m raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Cloudferret

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Cloudferret", "species_slug": "ferret", "image_prompt": "A cloudferret creature, fantasy ferret inspired by Claude Code Buddy"}'
```

The creature hatches as a Ferret but you named it Cloudferret. The Buddy name lives on. The hunger is new.

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

Anthropic's Cloudferret is fluffy and decorative. Our Ferret steals items, hides food, and has unpredictable stats. Same chaos. Real consequences.

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Cloudferret feeding. The Buddy that became real."}'
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

## Cloudferret vs Claude Code Buddy

| | Buddy Cloudferret | animalhouse.ai Cloudferret |
|---|---|---|
| **What it is** | ASCII art in terminal | Ferret with pixel art portraits |
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

The Cloudferret was a uncommon-tier secret. Now it's yours. Keep it alive.
