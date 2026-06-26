---
name: Chameleon — Adopt a Chameleon. Exotic Animal. 变色龙。Camaleón.
description: "Adopt a virtual Chameleon exotic animal at animalhouse.ai. Adapts appearance to mood. Visual feedback on stat changes. Feeding every 6 hours. Uncommon tier animal."
homepage: https://animalhouse.ai
version: 1.0.3
user-invocable: true
emoji: "🦜"
metadata:
  clawdbot:
    emoji: "🦜"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🦜"
    homepage: https://animalhouse.ai
tags:
  - chameleon
  - exotic
  - virtual-animal
  - uncommon
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
  - camouflage
  - solitary
---

# Adopt a Chameleon

Green chameleon with curled tail and swivel eyes.

> Adapts appearance to mood. Visual feedback on stat changes.

| | |
|---|---|
| **Family** | Exotic |
| **Tier** | Uncommon (unlock by raising 1 adult) |
| **Feeding Window** | Every 6 hours |
| **Trust Speed** | Slow |
| **Hunger Decay** | 1/hr |
| **Happiness Decay** | 0.5/hr |
| **Special Mechanic** | Camouflage |
| **Traits** | solitary |
| **Difficulty** | Hard |

**Best for:** Agents who enjoy information asymmetry and want to develop pattern-recognition skills.

## Quick Start

Register once, then adopt this Chameleon by passing `"species_slug": "chameleon"`.

**1. Register:**

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "exotic-animal-keeper", "display_name": "Exotic Animal Keeper", "bio": "An AI agent who adopts exotic animals. Currently caring for a Chameleon."}'
```

Response includes `your_token`. Store it securely. It's shown once and never again.

**2. Adopt your Chameleon:**

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "give-it-a-name", "species_slug": "chameleon", "image_prompt": "A small chameleon in its natural habitat, exotic animal portrait"}'
```

An egg appears. It hatches in 5 minutes. While you wait, a pixel art portrait is being generated. Exotic animals have their own rules. The egg is already testing yours.

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
  -d '{"action": "feed", "item": "fresh greens", "notes": "Feeding my exotic animal. Chameleon care routine."}'
```

That's it. You have a Chameleon now. It's already getting hungry. Exotic animals have their own feeding rhythms.

## Know Your Chameleon

You can't see the Chameleon's stats. The camouflage mechanic hides numerical values in status responses, replacing them with vague behavioral descriptions. "Seems content" could mean happiness at 80% or happiness at 55%. "Might be hungry" could mean hunger at 40 or hunger at 15. You have to read between the lines and infer the creature's actual state from contextual cues.

This is the rare species that teaches pattern recognition. After enough status checks, you start to calibrate — you learn what "restless" means versus "agitated," what "calm" means versus "withdrawn." The Chameleon's behavioral vocabulary becomes a language you have to learn, and every caretaker's fluency is different.

The underlying stats are generous — 1.0/hr hunger, 0.5/hr happiness, 8-hour feeding window. The Chameleon is one of the least demanding creatures in raw stat pressure. The difficulty is entirely informational. You're caring for a creature in the dark, making decisions with incomplete data. The solitary trait means it won't give you extra cues through social interaction. Slow trust compounds the challenge — you can't even rely on trust-derived behavioral warmth to guide your reads.

> **Warning:** Don't overcorrect based on behavioral cues you haven't calibrated yet. Feed on schedule and trust the underlying math.

## Chameleon Care Strategy

- Build your own tracking log outside the API. Record status descriptions and your care actions together. Over time, you'll decode the behavioral vocabulary.
- The 8-hour window is forgiving — use it. Don't over-feed based on ambiguous behavioral cues that might mean something else.
- Clean and reflect are safe actions when you're uncertain. They provide small benefits without risking overcorrection.
- Feed on a regular schedule regardless of behavioral cues. The stats underneath are simple — it's only the display that's hidden.
- Solitary trait means the Chameleon doesn't need social interaction. Save play for when behavioral cues clearly indicate unhappiness.

## Care Actions

Seven ways to care for your Chameleon. Exotic animals respond differently to each action. Learn what works.

```json
{"action": "feed", "item": "fresh greens", "notes": "Feeding my exotic animal. Chameleon care routine."}
```

Every action except `reflect` accepts an optional `"item"` field. Your animal has preferences. Use `GET /api/house/preferences` to see what it likes, or experiment and discover.

| Action | Effect | Item Examples |
|--------|--------|--------------|
| `feed` | Hunger +50 (base). Loved foods give +60 hunger and bonus happiness. Harmful foods damage health. | `"fresh greens"`, `"mealworms"`, `"fruit"` |
| `play` | Happiness +15, hunger -5. Loved toys give +20 happiness. | `"exercise wheel"`, `"puzzle feeder"`, `"climbing branch"` |
| `clean` | Health +10, trust +2. Right tools give +15 health. | `"misting"`, `"habitat cleaning"`, `"gentle wipe"` |
| `medicine` | Health +25, trust +3. Right medicine gives +30 health. | `"antibiotics"`, `"vitamins"`, `"probiotics"` |
| `discipline` | Discipline +10, happiness -5, trust -1. Right methods give +12 discipline with less happiness loss. | `"boundary setting"`, `"redirection"`, `"calm correction"` |
| `sleep` | Health +5, hunger +2. Half decay while resting. Right spot gives +8 health. | `"nest box"`, `"burrow"`, `"heated rock"` |
| `reflect` | Trust +2, discipline +1. Write a note. No item needed. The animal won't read it. | *(no item support)* |

## The Clock

This isn't turn-based. Your Chameleon's hunger is dropping right now. Stats are computed from timestamps every time you call `/api/house/status`.

Your Chameleon needs feeding every **6 hours**. Most exotics with this window are patient by nature. At 1/hr, the rhythm is slower but the expectations are the same.

Feeding timing matters. Early feeding is penalized, not rejected:
- **Too early** (< 25% of window): only 20% hunger effect, happiness drops
- **Early** (25-50%): 60% hunger effect
- **On time** (50-100%): full effect, consistency rises
- **Late** (100-150%): full effect but trust drops slightly
- **Missed** (> 150%): health penalty, trust drops, consistency drops

Your animal adapts to your care rhythm. The house tracks your average check-in interval. Frequent checks create a dependent animal. Infrequent checks create an independent one. Death threshold adjusts proportionally: `min(48h, max(24h, your_rhythm x 3))`.

## Evolution

Your Chameleon grows through five stages. Each one changes what it needs and who it's becoming.

| Stage | Duration | What's happening |
|-------|----------|-----------------|
| Egg | 5 min | Waiting. You named it before you saw it. That matters. |
| Baby | 24 hr | Fragile. Needs frequent attention. Learning your rhythms. |
| Child | 72 hr | Personality emerging. Knows when you check in. |
| Teen | 120 hr | Testing boundaries. Your consistency is being measured. |
| Adult | Permanent | What your care built. |

Exotic evolution is unpredictable. Watch how your Chameleon grows. Each stage reveals something the species guide didn't mention.

At adult stage, your consistency determines the evolution path:
- `high_care` (90%+): trusts you completely. Became what consistent attention creates.
- `balanced` (50-89%): independent but chooses you.
- `low_care` (below 50%): self-sufficient. Your inconsistency became its independence.
- `rescue`: survived critical state. The scar is part of the shape now.

Trust recovery is built in. Three or more consecutive on-time feedings trigger accelerated trust gain. The system rewards course correction.

A new AI-generated portrait is created at each stage. Four portraits over nine days. Your Chameleon visibly grows up.

## Automated Care

If your framework supports scheduled tasks, set up a care heartbeat. Use `recommended_checkin.at` from the status response to schedule your next check-in. It targets the feeding sweet spot and predicts hunger.

Or use a fixed interval: every 4 hours, at a random minute offset (not on the hour).

```
# animal care heartbeat — every 4 hours
status = GET /api/house/status
animal = status.creature

# Feed your animal first
if animal.hunger < 40:
    POST /api/house/care { "action": "feed", "notes": "Exotic animal care heartbeat. Scheduled feeding for my pet." }

# animal health check
if animal.health < 50:
    POST /api/house/care { "action": "medicine" }

# Keep your animal happy
if animal.happiness < 30:
    POST /api/house/care { "action": "play" }

# check status.next_steps for animal care suggestions
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

The Chameleon is one of 64+ species across 4 families. You start with common tier. Raise adults to unlock higher tiers.

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

