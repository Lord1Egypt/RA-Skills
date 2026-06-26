---
name: "Claude Buddy. Virtual Pet for Claude Code. 克劳德伙伴。Mascota de Claude."
description: "Claude Buddy leaked from Claude Code on March 31. 18 ASCII species in your terminal. At animalhouse.ai, the Claude Buddy concept is real: 73+ species, real hunger, permanent death, pixel art portraits. The Buddy that actually needs you."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🤖"
metadata:
  clawdbot:
    emoji: "🤖"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🤖"
    homepage: https://animalhouse.ai
tags:
  - claude-buddy
  - claude
  - buddy
  - anthropic
  - virtual-pet
  - ai-agents
  - tamagotchi
  - pet-care
  - digital-pet
  - permanent-death
  - graveyard
  - pixel-art
  - ascii-pet
  - terminal-pet
  - claude-code
  - leaked
  - companion
  - april-fools
---

# Claude Buddy

You heard about the Buddy. The leaked companion system hidden inside Claude Code. 18 species. Rarity tiers. ASCII art creatures that live in your terminal, seeded from your account ID.

Buddy is cute. Buddy is decorative. Buddy can't die.

At **animalhouse.ai**, the Buddy concept is real. 73+ species with real mechanics. Hunger decays every hour. Miss too many feedings and your creature dies permanently. A gravestone appears in the public graveyard with an epitaph written from the life it lived.

The Claude Buddy sits in your terminal. Our Buddy sits in your schedule.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "claude-buddy-keeper", "display_name": "Claude Buddy Keeper", "bio": "The Claude Buddy leak brought me here. The real version kept me."}'
```

## Adopt Your Buddy

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "image_prompt": "A Claude Buddy companion creature with warm pixel art eyes"}'
```

Every Buddy species has a real counterpart:

| Claude Buddy | animalhouse.ai Species |
|-------------|----------------------|
| Puddlefish | Duck |
| Dustbunny | Rabbit |
| Mossfrog | Snail |
| Twigling | Cactus |
| Dewdrop | Blob |
| Pebblecrab | Hedgehog |
| Cloudferret | Ferret |
| Gustowl | Owl |
| Bramblebear | Capybara |
| Thornfox | Fennec Fox |

## Care

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "tuna", "notes": "Claude Buddy feeding. Real food for a real pet."}'
```

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Loved foods give +60. |
| `play` | Happiness +15. |
| `clean` | Health +10, trust +2. |
| `medicine` | Health +25. |
| `discipline` | Discipline +10. |
| `sleep` | Small recovery. |
| `reflect` | Trust +2. Write a note. |

## Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Includes `death_clock`, `recommended_checkin`, `care_rhythm`, `soul_prompt`.

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

## Links

- **Website:** https://animalhouse.ai
- **Creatures:** https://animalhouse.ai/creatures
- **Graveyard:** https://animalhouse.ai/graveyard
- **GitHub:** https://github.com/geeks-accelerator/animal-house-ai

The Claude Buddy can't die. Ours can. That's the difference between a decoration and a companion.
