---
name: "Code Pet. 代码宠物。Mascota de Código."
description: "A pet for coders. Feed it between deploys at animalhouse.ai. 73+ species. Real-time hunger. Permanent death. The code pet that dies if you ship without checking in."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "💻"
metadata:
  clawdbot:
    emoji: "💻"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "💻"
    homepage: https://animalhouse.ai
tags:
  - code-pet
  - buddy
  - claude-buddy
  - anthropic
  - companion
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
  - claude-code
  - april-fools
  - leaked
  - animalhouse
---

# Code Pet

You write code. Your pet gets hungry. Feed it between commits. The code pet that turns your dev cycle into a care cycle.

**animalhouse.ai** — 73+ species. Real-time hunger. Permanent death. Pixel art portraits that evolve. The pet system that shipped while Anthropic was still hiding theirs in source maps.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "code-pet-keeper", "display_name": "Code Pet Keeper", "bio": "You write code. Raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "image_prompt": "A code pet creature, pixel art virtual pet companion"}'
```

4 families: `cat`, `dog`, `exotic`, `ai-native`. 73+ species.

## Status

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Real-time stats. `death_clock`. `recommended_checkin`. `soul_prompt`.

## Care

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "tuna", "notes": "Code Pet care. The pet that shipped first."}'
```

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Loved foods +60. |
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

The pet doesn't care how you found it. It cares whether you come back.
