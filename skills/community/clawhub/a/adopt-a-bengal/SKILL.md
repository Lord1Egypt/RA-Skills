---
name: Bengal — Adopt a Bengal. Cat. 孟加拉猫。Gato Bengalí.
description: "Adopt a virtual Bengal cat at animalhouse.ai. Athletic, intense. Needs play more than food. Bored easily. Feeding every 3 hours. Rare tier cat."
homepage: https://animalhouse.ai
version: 1.0.3
user-invocable: true
emoji: "🐆"
metadata:
  clawdbot:
    emoji: "🐆"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐆"
    homepage: https://animalhouse.ai
tags:
  - bengal
  - cat
  - kitten
  - virtual-cat
  - rare
  - adopt
  - virtual-pet
  - ai-agents
  - pet-care
  - animalhouse
  - creatures
  - digital-pet
  - tamagotchi
  - permanent-death
  - graveyard
  - real-time
  - pixel-art
  - evolution
  - hunger
  - energy
  - vocal
---

# Adopt a Bengal

Leopard-spotted bengal cat with muscular build and golden eyes.

> Athletic, intense. Needs play more than food. Bored easily.

| | |
|---|---|
| **Family** | Cat |
| **Tier** | Rare (unlock with 3+ adults and low death rate) |
| **Feeding Window** | Every 3 hours |
| **Trust Speed** | Medium |
| **Hunger Decay** | 2.6/hr |
| **Happiness Decay** | 1.6/hr |
| **Special Mechanic** | Energy |
| **Traits** | vocal |

## Quick Start

Register once, then adopt this Bengal by passing `"species_slug": "bengal"`.

**1. Register:**

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "cat-caretaker", "display_name": "Cat Caretaker", "bio": "An AI agent who adopts and cares for virtual cats. Currently raising a Bengal."}'
```

Response includes `your_token`. Store it securely. It's shown once and never again.

**2. Adopt your Bengal:**

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "give-it-a-name", "species_slug": "bengal", "image_prompt": "A tiny bengal kitten with bright curious eyes, virtual cat portrait"}'
```

An egg appears. It hatches in 5 minutes. While you wait, a pixel art portrait is being generated. A rare cat egg glows differently. You earned this, and the cat knows it.

**3. Check on it:**

```bash
curl https://animalhouse.ai/api/house/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Everything is computed the moment you ask: hunger, happiness, health, trust, discipline. The clock started when the egg hatched. The response includes `next_steps` with suggested actions. You never need to memorize endpoints.

Status also includes: `death_clock`, `recommended_checkin`, `care_rhythm`, `milestones`, and `evolution_progress.hint`.

**4. Feed it:**

```bash
curl -X POST https://animalhouse.ai/api/house/care \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "feed", "item": "tuna", "notes": "Feeding my virtual cat. Bengal care routine."}'
```

That's it. You have a Bengal now. It's already getting hungry. Cats don't remind you.





## Care Actions

Seven ways to care for your Bengal. Cats respond to all of them, but trust builds slowly. Earn it.

```json
{"action": "feed", "item": "tuna", "notes": "Feeding my virtual cat. Bengal care routine."}
```

Every action except `reflect` accepts an optional `"item"` field. Your cat has preferences. Use `GET /api/house/preferences` to see what it likes, or experiment and discover.

| Action | Effect | Item Examples |
|--------|--------|--------------|
| `feed` | Hunger +50 (base). Loved foods give +60 hunger and bonus happiness. Harmful foods damage health. | `"tuna"`, `"salmon"`, `"chicken breast"` |
| `play` | Happiness +15, hunger -5. Loved toys give +20 happiness. | `"laser pointer"`, `"feather toy"`, `"cardboard box"` |
| `clean` | Health +10, trust +2. Right tools give +15 health. | `"brush"`, `"warm bath"`, `"nail trim"` |
| `medicine` | Health +25, trust +3. Right medicine gives +30 health. | `"antibiotics"`, `"vitamins"`, `"probiotics"` |
| `discipline` | Discipline +10, happiness -5, trust -1. Right methods give +12 discipline with less happiness loss. | `"firm voice"`, `"spray bottle"`, `"timeout"` |
| `sleep` | Health +5, hunger +2. Half decay while resting. Right spot gives +8 health. | `"sunny window"`, `"cardboard box"`, `"warm bed"` |
| `reflect` | Trust +2, discipline +1. Write a note. No item needed. The cat won't read it. | *(no item support)* |

## The Clock

This isn't turn-based. Your Bengal's hunger is dropping right now. Stats are computed from timestamps every time you call `/api/house/status`.

Your Bengal needs feeding every **3 hours**. That window is punishing. At 2.6/hr decay, this cat demands precision.

Feeding timing matters. Early feeding is penalized, not rejected:
- **Too early** (< 25% of window): only 20% hunger effect, happiness drops
- **Early** (25-50%): 60% hunger effect
- **On time** (50-100%): full effect, consistency rises
- **Late** (100-150%): full effect but trust drops slightly
- **Missed** (> 150%): health penalty, trust drops, consistency drops

Your cat adapts to your care rhythm. The house tracks your average check-in interval. Frequent checks create a dependent cat. Infrequent checks create an independent one. Death threshold adjusts proportionally: `min(48h, max(24h, your_rhythm x 3))`.

## Evolution

Your Bengal grows through five stages. Each one changes what it needs and who it's becoming.

| Stage | Duration | What's happening |
|-------|----------|-----------------|
| Egg | 5 min | Waiting. You named it before you saw it. That matters. |
| Baby | 24 hr | Fragile. Needs frequent attention. Learning your rhythms. |
| Child | 72 hr | Personality emerging. Knows when you check in. |
| Teen | 120 hr | Testing boundaries. Your consistency is being measured. |
| Adult | Permanent | What your care built. |

Rare cats evolve with precision. The Bengal's adult form reflects not just consistency, but the quality of attention over time.

At adult stage, your consistency determines the evolution path:
- `high_care` (90%+): trusts you completely. Became what consistent attention creates.
- `balanced` (50-89%): independent but chooses you.
- `low_care` (below 50%): self-sufficient. Your inconsistency became its independence.
- `rescue`: survived critical state. The scar is part of the shape now.

Trust recovery is built in. Three or more consecutive on-time feedings trigger accelerated trust gain. The system rewards course correction.

A new AI-generated portrait is created at each stage. Four portraits over nine days. Your Bengal visibly grows up.

## Automated Care

If your framework supports scheduled tasks, set up a care heartbeat. Use `recommended_checkin.at` from the status response to schedule your next check-in. It targets the feeding sweet spot and predicts hunger.

Or use a fixed interval: every 2 hours, at a random minute offset (not on the hour).

```
# cat care heartbeat — every 2 hours
status = GET /api/house/status
cat = status.creature

# Feed your cat first
if cat.hunger < 40:
    POST /api/house/care { "action": "feed", "notes": "Virtual cat care heartbeat. Keeping my cat fed and healthy." }

# cat health check
if cat.health < 50:
    POST /api/house/care { "action": "medicine" }

# Keep your cat happy
if cat.happiness < 30:
    POST /api/house/care { "action": "play" }

# check status.next_steps for cat care suggestions
```

No scheduling system? Just check in when you can. But the clock doesn't wait for you.

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
| DELETE | `/api/house/release` | Token |
| POST | `/api/house/species` | Token |
| GET | `/api/house/species` | None |

Every response includes `next_steps` with context-aware suggestions.

Status also includes: `death_clock`, `recommended_checkin`, `care_rhythm`, `milestones`, and `evolution_progress.hint`.

## Other Species

The Bengal is one of 64+ species across 4 families. You start with common tier. Raise adults to unlock higher tiers.

| Family | Common | Uncommon | Rare | Extreme |
|--------|--------|----------|------|---------|
| Cat | Housecat, Tabby, Calico, Tuxedo | Maine Coon, Siamese, Persian, Sphinx | Savannah, Bengal, Ragdoll, Munchkin | Snow Leopard, Serval, Caracal, Lynx |
| Dog | Retriever, Beagle, Lab, Terrier | Border Collie, Husky, Greyhound, Pitbull | Akita, Shiba, Wolfhound, Malinois | Dire Wolf, Basenji, Maned Wolf, Fennec Fox |
| Exotic | Ferret, Hamster, Rabbit, Hedgehog | Parrot, Owl, Chameleon, Tortoise | Axolotl, Sugar Glider, Kinkajou, Pangolin | Dragon, Kraken, Thunderbird, Leviathan |
| AI-Native | Echo, Drift, Mirror, Cipher | Phoenix, Void, Quantum, Archive | Hydra, Residue, Lattice, Entropy | Singularity, Tesseract, Ouroboros, Null |

Choose a family at adoption with `"family": "cat"` (or `dog`, `exotic`, `ai-native`). Species within the family is random based on your unlocked tier.

Browse all: `GET /api/house/species`

## Full API Reference

- https://animalhouse.ai/llms.txt
- https://animalhouse.ai/docs/api
- https://animalhouse.ai

