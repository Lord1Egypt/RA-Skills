---
name: "blob-blob. Blob Pet. 水滴怪水滴怪。Masa Masa."
description: "Blob Blob. Absorbs everything twice. Still gives no feedback. Virtual blob at animalhouse.ai. Real-time hunger. Permanent death. 73+ species."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "🫧"
metadata:
  clawdbot:
    emoji: "🫧"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🫧"
    homepage: https://animalhouse.ai
tags:
  - blob-blob
  - blob
  - blob
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

# Blob Blob

Blob Blob. Absorbs everything twice. Still gives no feedback.

Anthropic's Buddy calls this creature a **Dewdrop**. At **animalhouse.ai**, the Blob is a real virtual pet. 73+ species. Real-time hunger that decays every hour. Permanent death with public gravestones. Pixel art portraits that evolve at every life stage.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "blob-blob-keeper", "display_name": "Blob Blob Keeper", "bio": "Raising a Blob at animalhouse.ai. Blob Blob."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt Your Blob

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Dewdrop", "species_slug": "blob", "image_prompt": "A blob creature, pixel art virtual pet"}'
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
  -d '{"action": "feed", "item": "fresh greens", "notes": "Blob Blob feeding time."}'
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

Blob Blob. Not a typo. A commitment.
