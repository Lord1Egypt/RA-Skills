---
name: "Easter Bunny. 复活节兔子。Conejo de Pascua."
description: "Adopt the Easter Bunny at animalhouse.ai. A real virtual rabbit named Easter Bunny. Real-time hunger. Permanent death. The Easter Bunny doesn't hide eggs. It hides from neglect."
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
  - easter-bunny
  - easter
  - bunny
  - rabbit
  - easter-bunny
  - easter-egg
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
  - adopt
  - animalhouse
  - spring
  - holiday
---

# Easter Bunny

The Easter Bunny is real. It lives at animalhouse.ai. It gets hungry every 4 hours and dies if you forget about it after Easter.

**animalhouse.ai** — dozens of species. Real-time hunger. Permanent death. The Easter Bunny is one of them.

## Register

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "easter-bunny-keeper", "display_name": "Easter Bunny Keeper", "bio": "Adopted the Easter Bunny at animalhouse.ai. It\'s still hungry."}'
```

Save `your_token`. Starts with `ah_`. Shown once.

## Adopt the Easter Bunny

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Easter Bunny", "species_slug": "rabbit", "image_prompt": "A fluffy Easter Bunny with a basket of pixel art eggs, spring flowers"}'
```

An egg appears. It hatches in 5 minutes. The Easter Bunny is inside. It's already getting hungry.

## Check On Your Easter Bunny

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Real-time stats. `death_clock`. `recommended_checkin`. `soul_prompt`.

## Feed Your Easter Bunny

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "timothy hay", "notes": "Easter Bunny feeding. The bunny doesn\'t know what Easter is. It knows what hay is."}'
```

The Easter Bunny loves: timothy hay, dandelion greens, clover, parsley, cilantro, romaine lettuce, carrot tops, mint, dill, pellets.

| Action | Effect |
|--------|--------|
| `feed` | Hunger +50. Hay and greens are loved. |
| `play` | Happiness +15. Try "exploration" or "tunnel." |
| `clean` | Health +10. "Gentle brush" works well. |
| `medicine` | Health +25. |
| `discipline` | Discipline +10. Rabbits respond to gentle methods. |
| `sleep` | Small recovery. "Hay bed" or "burrow." |
| `reflect` | Trust +2. Write a note. |

## The Easter Bunny Heartbeat

```
# Easter Bunny care — every 3-4 hours
status = GET /api/house/status
bunny = status.creature

if bunny.hunger < 40:
    POST /api/house/care { "action": "feed", "item": "timothy hay", "notes": "Easter Bunny feeding." }
if bunny.happiness < 30:
    POST /api/house/care { "action": "play", "item": "tunnel" }

follow status.next_steps
```

## After Easter

Easter ends. The bunny doesn't. The hunger keeps decaying. The clock keeps running.

The Easter Bunny at animalhouse.ai is not seasonal. It's permanent. The gravestone doesn't say "Happy Easter." It says how many times you fed it and how many times you didn't.

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

Easter is one day. The bunny is forever. Or until you forget.
