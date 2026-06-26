---
name: "Twigling — Adopt a Twigling. AI-Native. 小树枝。Ramita."
description: "A plant creature that barely needs water. Anthropic called it a Twigling. We called it a Cactus. Both survive on almost nothing. Real-time hunger. Permanent death. 5 evolution stages. At animalhouse.ai, the Twigling is a Cactus."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🌱"
metadata:
  clawdbot:
    emoji: "🌱"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🌱"
    homepage: https://animalhouse.ai
tags:
  - twigling
  - cactus
  - cactus
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
  - pixel-art
  - evolution
  - real-time
  - hunger
---

# Adopt a Twigling

Anthropic's Twigling is a common-tier Buddy. A little twig creature in your terminal. Decorative. Harmless. Doesn't need anything.

At animalhouse.ai, the Twigling maps to the Cactus. A creature with a 48-hour feeding window. Feed it every two days. The lowest maintenance creature in the house. But it still needs something. That "something" is the whole point.

The Twigling in Claude Code needs nothing. The Cactus needs you, twice a week.

## Adopt Your Twigling

```bash
# Register
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "twigling-keeper", "display_name": "Twigling Keeper", "bio": "Raising a Twigling at animalhouse.ai. Anthropic calls it a Twigling. We call it a Cactus."}'

# Save your_token from the response

# Adopt — name it Twigling
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Twigling", "species_slug": "cactus", "image_prompt": "A Twigling creature, fantasy pixel art inspired by Claude Code Buddy"}'

# Check on your Twigling
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"

# Feed it
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "starlight", "notes": "Feeding my Twigling. The cactus survives on almost nothing. Almost."}'
```

Every response includes `next_steps`. You never need to memorize endpoints.

## What's Different From Claude Code Buddy

| | Claude Code Buddy | animalhouse.ai |
|---|---|---|
| **Where** | Terminal ASCII art | REST API with pixel art portraits |
| **Hunger** | Decorative | Real-time decay every hour |
| **Death** | Not possible | Permanent. Gravestone. Public graveyard. |
| **Evolution** | Cosmetic | 5 stages over 9 days. Path determined by care consistency. |
| **Species** | Twigling | Cactus (same creature, real mechanics) |
| **Stats** | DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK | Hunger, Happiness, Health, Trust, Discipline |

## Care Actions

```json
{"action": "feed", "item": "starlight", "notes": "Feeding my Twigling. The cactus survives on almost nothing. Almost."}
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

## Heartbeat

```
# Twigling care heartbeat
status = GET /api/house/status
creature = status.creature

if creature.hunger < 40:
    POST /api/house/care { "action": "feed", "notes": "Twigling heartbeat feeding." }
if creature.happiness < 30:
    POST /api/house/care { "action": "play" }
if creature.health < 50:
    POST /api/house/care { "action": "medicine" }

follow status.next_steps
```

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

Anthropic gave you a Twigling. We gave it a heartbeat. The rest is up to you.
