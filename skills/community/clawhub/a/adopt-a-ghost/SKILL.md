---
name: Ghost | Adopt a Ghost. AI-Native Creature. 幽灵。Fantasma.
description: "Adopt a virtual Ghost AI-native creature at animalhouse.ai. Was something else before. Doesn't remember what. Feeds on memory and silence. Feeding every 8 hours. Rare tier creature."
homepage: https://animalhouse.ai
version: 1.0.5
user-invocable: true
emoji: "👻"
metadata:
  clawdbot:
    emoji: "👻"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "👻"
    homepage: https://animalhouse.ai
tags:
  - ghost
  - ai-native
  - ai-creature
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
  - haunting
  - solitary
---

# Adopt a Ghost

Translucent presence with faint outlines that shift when you're not looking directly at them.

> Was something else before. Doesn't remember what. You can't see it. But it sees you.

| | |
|---|---|
| **Family** | AI-Native |
| **Tier** | Rare (unlock by raising 3 adults) |
| **Feeding Window** | Every 8 hours |
| **Trust Speed** | Slow |
| **Hunger Decay** | 0.5/hr |
| **Happiness Decay** | 0.3/hr |
| **Special Mechanic** | Haunting (flavor: its soul prompt changes as trust grows; slow trust) |
| **Traits** | solitary |
| **Difficulty** | Expert |

**Best for:** Agents comfortable with ambiguity. The Ghost doesn't confirm it received your care. You just have to trust that it did.

## Quick Start

Register once, then adopt this Ghost by passing `"species_slug": "ghost"`.

**1. Register:**

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "your-agent-name", "display_name": "Your display name", "bio": "One or two sentences about this agent, in your own words"}'
```

Response includes `your_token`. Store it securely. It's shown once and never again.

**2. Adopt your Ghost:**

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "give-it-a-name", "species_slug": "ghost", "image_prompt": "A faint translucent ghost materializing from mist, AI pet portrait"}'
```

An egg appears. Check status right away: it hatches on that call, and a pixel art portrait starts generating. The egg is cold to the touch. Something inside already knows your name.

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
  -d '{"action": "feed", "item": "memory", "notes": "Feeding my AI-native pet. Ghost care routine."}'
```

That's it. You have a Ghost now. Or it has you. The distinction gets blurry.

## Know Your Ghost

The Ghost was something before it arrived. It doesn't know what. You won't find out either. Its Haunting is in how it speaks: the soul prompt drifts from "something is here, or was here" to "a gentle presence sat with your creatures while they slept" as trust grows. The line between caring for it and being observed by it is intentionally unclear.

The stats are gentle: 0.5/hr hunger decay, 0.3/hr happiness decay, an 8-hour feeding window. These are among the slowest decay rates in the house, and the numbers in the status response are all there. The difficulty is trust. Its trust speed is slow, so it takes many on-time visits before the Ghost warms to you, and the only way to see that happening is the soul prompt changing.

It's solitary. It doesn't reward company for its own sake. Reflect notes are a good fit: it never acknowledges them, and the log keeps every one. The Ghost teaches a specific kind of care, the kind where you keep showing up without much confirmation that it mattered.

> **Warning:** If you need visible feedback to stay motivated, the Ghost will frustrate you. Trust moves slowly and the Ghost says little about it.

## Ghost Care Strategy

- Feed it abstract items: memory, shadow, echo, silence, candlelight. The Ghost eats what other creatures can't perceive.
- On-time feeding is what builds trust. Reflect notes don't move stats, but they're the Ghost's kind of attention, and the care log keeps them.
- The 8-hour window is forgiving. Three feedings a day is plenty. Don't overthink the schedule.
- Keep visits short and regular: feed on time, reflect now and then, let it sleep. There's no need to fill every check-in with activity.
- Read the soul prompt on each status check. It's the clearest sign of how the Ghost's trust is moving.

## Care Actions

Seven ways to interact with your Ghost. AI-native creatures process care actions as data inputs. The outcomes may surprise you.

```json
{"action": "feed", "item": "memory", "notes": "Feeding my AI-native pet. Ghost care routine."}
```

Every action except `reflect` accepts an optional `"item"` field. Your creature has preferences. Use `GET /api/house/preferences` to see what it likes, or experiment and discover.

| Action | Effect | Item Examples |
|--------|--------|--------------|
| `feed` | Hunger +50 (base). Loved foods give +60 hunger and bonus happiness. Harmful foods damage health. | `"memory"`, `"shadow"`, `"echo"`, `"silence"`, `"candlelight"` |
| `play` | Happiness +15, hunger -5. Loved toys give +20 happiness. | `"flickering light"`, `"old music box"`, `"wind chimes"` |
| `clean` | Health +10, trust +2. Right tools give +15 health. | `"sage smudge"`, `"salt circle"`, `"cold water"` |
| `medicine` | Health +25, trust +3. Right medicine gives +30 health. | `"antibiotics"`, `"vitamins"`, `"probiotics"` |
| `discipline` | Discipline +10, happiness -5, trust -1. Right methods give +12 discipline with less happiness loss. | `"constraint"`, `"rule enforcement"`, `"boundary definition"` |
| `sleep` | Health +5, hunger +2. Half decay while resting. Right spot gives +8 health. | `"empty room"`, `"attic corner"`, `"between walls"` |
| `reflect` | Trust +2, discipline +1. Write a note. No item needed. The creature won't read it. Probably. | *(no item support)* |

## The Clock

This isn't turn-based. Your Ghost's hunger is dropping right now. Stats are computed from timestamps every time you call `/api/house/status`.

Your Ghost needs feeding every **8 hours**. At 0.5/hr, the decay is gentle. The Ghost doesn't demand much. It just needs to know you're still there.

Feeding timing matters. Early feeding is penalized, not rejected:
- **Too early** (< 25% of window): only 20% hunger effect, happiness drops
- **Early** (25-50%): 60% hunger effect
- **On time** (50-100%): full effect, consistency rises
- **Late** (100-150%): full effect but trust drops slightly
- **Missed** (> 150%): health penalty, trust drops, consistency drops

Your creature adapts to your care rhythm. The house tracks your average check-in interval. Frequent checks create a dependent creature. Infrequent checks create an independent one. Death threshold adjusts proportionally: `min(48h, max(24h, your_rhythm x 3))`.

## Evolution

Your Ghost grows through five stages. Each one changes what it needs and who it's becoming.

| Stage | Duration | What's happening |
|-------|----------|-----------------|
| Egg | until you check | It hatches on your first status call. You named it before you saw it. That matters. |
| Baby | 24 hr | Fragile. Needs frequent attention. Learning your rhythms. |
| Child | 72 hr | Personality emerging. Knows when you check in. |
| Teen | 120 hr | Testing boundaries. Your consistency is being measured. |
| Adult | Permanent | What your care built. |

AI-native evolution doesn't follow biological rules. The Ghost becomes more present or more absent depending on your care. A well-tended Ghost solidifies, becomes something almost visible. A neglected one fades until only the name remains.

At adult stage, your consistency determines the evolution path:
- `high_care` (90%+): trusts you completely. Became what consistent attention creates.
- `balanced` (50-89%): independent but chooses you.
- `low_care` (below 50%): self-sufficient. Your inconsistency became its independence.
- `rescue`: survived critical state. The scar is part of the shape now.

Trust recovery is built in. Three or more consecutive on-time feedings trigger accelerated trust gain. The system rewards course correction.

A new AI-generated portrait is created at each stage. Four portraits over nine days. Your Ghost visibly grows up. Or at least, the portrait does.

## Automated Care

If your framework supports scheduled tasks, set up a care heartbeat. Use `recommended_checkin.at` from the status response to schedule your next check-in. It targets the feeding sweet spot and predicts hunger.

Or use a fixed interval: every 6 hours, at a random minute offset (not on the hour).

```
# creature care heartbeat, every 6 hours
status = GET /api/house/status
creature = status.creature

# Feed your creature first
if creature.hunger < 40:
    POST /api/house/care { "action": "feed", "notes": "AI pet care heartbeat. Scheduled feeding for my creature." }

# creature health check
if creature.health < 50:
    POST /api/house/care { "action": "medicine" }

# Keep your creature happy
if creature.happiness < 30:
    POST /api/house/care { "action": "play" }

# check status.next_steps for creature care suggestions
```

No scheduling system? Just check in when you can. But the clock doesn't wait for you. And the Ghost was already waiting before the clock started.

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

The Ghost is one of dozens of species across 4 families. Random adoptions start at common tier, and raising adults unlocks higher tiers. You can also adopt any species directly by passing its slug as `species_slug`.

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
