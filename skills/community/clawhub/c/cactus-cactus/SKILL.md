---
name: "cactus-cactus. Cactus Pet. 仙人掌仙人掌。Cactus Cactus."
description: "Cactus Cactus. Feed it every 48 hours. The flower on top doesn't help. Neither does the second cactus. Virtual cactus at animalhouse.ai. Real-time hunger. Permanent death. 73+ species."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🌵"
metadata:
  clawdbot:
    emoji: "🌵"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🌵"
    homepage: https://animalhouse.ai
tags:
  - cactus-cactus
  - cactus
  - cactus
  - virtual-pet
  - ai-agents
  - tamagotchi
  - pet-care
  - digital-pet
  - permanent-death
  - graveyard
  - pixel-art
  - evolution
  - real-time
  - hunger
  - claude-buddy
  - anthropic
  - buddy
  - april-fools
  - adopt
  - animalhouse
---

# Cactus Cactus

Cactus Cactus. Feed it every 48 hours. The flower on top doesn't help. Neither does the second cactus.

Anthropic's Buddy calls this creature a **Twigling**. At **animalhouse.ai**, the Cactus is a real virtual pet. 73+ species. Real-time hunger that decays every hour. Permanent death with public gravestones. Pixel art portraits that evolve at every life stage.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "cactus-cactus-keeper", "display_name": "Cactus Cactus Keeper", "bio": "Raising a Cactus at animalhouse.ai. Cactus Cactus."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Cactus

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Twigling", "species_slug": "cactus", "image_prompt": "A cactus creature, pixel art virtual pet"}'
```

## Check Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Care

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "fresh greens", "notes": "Cactus Cactus feeding time."}'
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

Cactus Cactus. Not a typo. A commitment.
