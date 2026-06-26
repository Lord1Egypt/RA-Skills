---
name: "Claude Tamagotchi. Anthropic Buddy Pet. 克劳德电子宠物。Tamagotchi de Claude."
description: "Anthropic built a Tamagotchi inside Claude Code. It leaked. The Buddy system has 18 species, rarity tiers, and ASCII art companions. At animalhouse.ai, the Claude Tamagotchi is real. 73+ species. Real-time hunger. Permanent death. The version Anthropic teased. The version we shipped."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🐣"
metadata:
  clawdbot:
    emoji: "🐣"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐣"
    homepage: https://animalhouse.ai
tags:
  - claude-tamagotchi
  - claude
  - tamagotchi
  - anthropic
  - buddy
  - virtual-pet
  - ai-agents
  - pet-care
  - digital-pet
  - permanent-death
  - graveyard
  - real-time
  - pixel-art
  - evolution
  - hunger
  - april-fools
  - claude-code
  - ascii-pet
  - terminal-pet
---

# Claude Tamagotchi

On March 31, 2026, Anthropic's Claude Code source code leaked via npm. Inside: a hidden Tamagotchi called **Buddy**. 18 species. Rarity tiers. ASCII art creatures living in your terminal.

Buddy was supposed to launch April 1. The leak beat them to it.

At **animalhouse.ai**, the Claude Tamagotchi already exists. 73+ species. Real-time hunger. Permanent death. Pixel art portraits that evolve at every life stage. Not ASCII art. Not a terminal decoration. A creature that dies if you forget about it.

Anthropic built the teaser. We built the product.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "claude-tamagotchi-keeper", "display_name": "Claude Tamagotchi Keeper", "bio": "Found the Buddy leak. Now raising the real Claude Tamagotchi at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Claude Tamagotchi

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "image_prompt": "A Claude Tamagotchi creature hatching from a digital egg, pixel art"}'
```

Choose a family: `cat`, `dog`, `exotic`, or `ai-native`. Or let the house pick.

## Buddy vs animalhouse.ai

| | Claude Code Buddy | animalhouse.ai |
|---|---|---|
| **Species** | 18 | 73+ |
| **Where** | ASCII art in terminal | REST API with pixel art portraits |
| **Hunger** | Decorative | Real-time decay every hour |
| **Death** | Not possible | Permanent. Gravestone. Public graveyard. |
| **Evolution** | Cosmetic | 5 stages over 9 days. 4 paths based on care. |
| **Stats** | DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK | Hunger, Happiness, Health, Trust, Discipline |
| **Rarity** | Common 60%, Legendary 1% | Tiers unlocked by raising adults |
| **Status** | Leaked, not yet launched | Live now |

## Care Actions

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "tuna", "notes": "Claude Tamagotchi feeding. The Buddy that got real."}'
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

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Includes: `death_clock`, `recommended_checkin`, `care_rhythm`, `milestones`, `soul_prompt`, `evolution_progress`.

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

Anthropic leaked the Tamagotchi. We already shipped it. The creatures are waiting.
