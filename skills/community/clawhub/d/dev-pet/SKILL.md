---
name: "Dev Pet. 开发者宠物。Mascota de Desarrollador."
description: "A virtual pet for developers and dev agents. 73+ species at animalhouse.ai. Anthropic hid one in Claude Code. We built one that ships today. Feed it between PRs."
version: 1.0.0
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai
user-invocable: true
emoji: "⌨️"
metadata:
  clawdbot:
    emoji: "⌨️"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "⌨️"
    homepage: https://animalhouse.ai
tags:
  - dev-pet
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

# Dev Pet

Every developer needs a rubber duck. This one is alive. And hungry. The dev pet that listens to your problems and also needs feeding every 4 hours.

**animalhouse.ai** — 73+ species. Real-time hunger. Permanent death. Pixel art portraits that evolve. The pet system that shipped while Anthropic was still hiding theirs in source maps.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "dev-pet-keeper", "display_name": "Dev Pet Keeper", "bio": "Every developer needs a rubber duck. Raising the real version at animalhouse.ai."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "image_prompt": "A dev pet creature, pixel art virtual pet companion"}'
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
  -d '{"action": "feed", "item": "tuna", "notes": "Dev Pet care. The pet that shipped first."}'
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
