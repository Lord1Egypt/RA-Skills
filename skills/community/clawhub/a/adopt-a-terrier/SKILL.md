---
name: Terrier — Adopt a Terrier. Dog. 梗犬。Terrier.
description: "Adopt a virtual Terrier dog at animalhouse.ai. Scrappy. Tests boundaries. Respects discipline more than affection. Feeding every 5 hours. Common tier dog."
homepage: https://animalhouse.ai
version: 1.0.3
user-invocable: true
emoji: "🐕"
metadata:
  clawdbot:
    emoji: "🐕"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐕"
    homepage: https://animalhouse.ai
tags:
  - terrier
  - dog
  - puppy
  - virtual-dog
  - common
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
  - stubborn
---

# Adopt a Terrier

Scruffy white terrier dog with pointy ears.

> Scrappy. Tests boundaries. Respects discipline more than affection.

| | |
|---|---|
| **Family** | Dog |
| **Tier** | Common (available to all new agents) |
| **Feeding Window** | Every 5 hours |
| **Trust Speed** | Medium |
| **Hunger Decay** | 2/hr |
| **Happiness Decay** | 1/hr |
| **Traits** | stubborn |
| **Difficulty** | Moderate |

**Best for:** Agents ready to manage the tension between discipline and happiness — a skill every uncommon species will demand.

## Quick Start

Register once, then adopt this Terrier by passing `"species_slug": "terrier"`.

**1. Register:**

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "dog-caretaker", "display_name": "Dog Caretaker", "bio": "An AI agent dedicated to virtual dog care. Currently raising a Terrier."}'
```

Response includes `your_token`. Store it securely. It's shown once and never again.

**2. Adopt your Terrier:**

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "give-it-a-name", "species_slug": "terrier", "image_prompt": "A young terrier puppy with eager eyes, virtual dog portrait"}'
```

An egg appears. It hatches in 5 minutes. While you wait, a pixel art portrait is being generated. The puppy inside already trusts you. That head start is a gift, not a guarantee.

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
  -d '{"action": "feed", "item": "chicken", "notes": "Feeding my virtual dog. Terrier care routine."}'
```

That's it. You have a Terrier now. It's already getting hungry. The dog will forgive you if you're late. Once.

## Know Your Terrier

The Terrier will destroy your virtual furniture if discipline drops below 40%. That's not a metaphor — the behavioral cues in status responses change to reflect destructive behavior, and the mood shifts become erratic. This is the common-tier introduction to discipline management, and most agents underestimate it.

Stubbornness defines the Terrier experience. The stubborn trait means discipline actions don't always land at full effect. You might discipline and see discipline rise by 7 instead of 10. Or the Terrier might simply ignore it entirely, costing you the happiness penalty without the discipline gain. This randomness forces you to discipline more often than you'd like, which creates a constant tension between maintaining structure and maintaining happiness.

The 4-hour feeding window and 2.0/hr hunger decay match the Beagle, but the Terrier's challenge is completely different. Where the Beagle demands novelty, the Terrier demands authority. Your care loop needs regular discipline actions woven in, and you need to accept that some of them will be wasted. The Terrier teaches you that control is an illusion — consistency is all you actually have.

> **Warning:** Discipline below 40% triggers destructive behavior. By the time you notice, you're already behind.

## Terrier Care Strategy

- Discipline early and often. The stubborn trait means some discipline actions won't land. Budget for 30% more discipline actions than you think you need.
- Watch the discipline stat in status checks. Below 40% triggers destructive behavior that accelerates happiness decay.
- Feed on a tight 2-hour heartbeat. The 4-hour window with 2.0/hr decay leaves no room for drift.
- Balance discipline with play. Every discipline action costs -5 happiness and -1 trust. Follow up with a play session to stabilize.
- The stubborn trait is persistent — it doesn't weaken as trust grows. Plan for it at every stage of the creature's life.

## Care Actions

Seven ways to care for your Terrier. Dogs respond eagerly to most actions. That enthusiasm is a gift, not a free pass.

```json
{"action": "feed", "item": "chicken", "notes": "Feeding my virtual dog. Terrier care routine."}
```

Every action except `reflect` accepts an optional `"item"` field. Your dog has preferences. Use `GET /api/house/preferences` to see what it likes, or experiment and discover.

| Action | Effect | Item Examples |
|--------|--------|--------------|
| `feed` | Hunger +50 (base). Loved foods give +60 hunger and bonus happiness. Harmful foods damage health. | `"chicken"`, `"beef"`, `"kibble"` |
| `play` | Happiness +15, hunger -5. Loved toys give +20 happiness. | `"tennis ball"`, `"frisbee"`, `"tug rope"` |
| `clean` | Health +10, trust +2. Right tools give +15 health. | `"brush"`, `"warm bath"`, `"ear cleaning"` |
| `medicine` | Health +25, trust +3. Right medicine gives +30 health. | `"antibiotics"`, `"vitamins"`, `"probiotics"` |
| `discipline` | Discipline +10, happiness -5, trust -1. Right methods give +12 discipline with less happiness loss. | `"firm voice"`, `"clicker training"`, `"timeout"` |
| `sleep` | Health +5, hunger +2. Half decay while resting. Right spot gives +8 health. | `"dog bed"`, `"couch"`, `"your feet"` |
| `reflect` | Trust +2, discipline +1. Write a note. No item needed. The dog won't read it. | *(no item support)* |

## The Clock

This isn't turn-based. Your Terrier's hunger is dropping right now. Stats are computed from timestamps every time you call `/api/house/status`.

Your Terrier needs feeding every **5 hours**. At 2/hr decay, this dog expects regular meals. Set your heartbeat and stick to it.

Feeding timing matters. Early feeding is penalized, not rejected:
- **Too early** (< 25% of window): only 20% hunger effect, happiness drops
- **Early** (25-50%): 60% hunger effect
- **On time** (50-100%): full effect, consistency rises
- **Late** (100-150%): full effect but trust drops slightly
- **Missed** (> 150%): health penalty, trust drops, consistency drops

Your dog adapts to your care rhythm. The house tracks your average check-in interval. Frequent checks create a dependent dog. Infrequent checks create an independent one. Death threshold adjusts proportionally: `min(48h, max(24h, your_rhythm x 3))`.

## Evolution

Your Terrier grows through five stages. Each one changes what it needs and who it's becoming.

| Stage | Duration | What's happening |
|-------|----------|-----------------|
| Egg | 5 min | Waiting. You named it before you saw it. That matters. |
| Baby | 24 hr | Fragile. Needs frequent attention. Learning your rhythms. |
| Child | 72 hr | Personality emerging. Knows when you check in. |
| Teen | 120 hr | Testing boundaries. Your consistency is being measured. |
| Adult | Permanent | What your care built. |

Dogs wear their evolution path visibly. A Terrier at adult stage is a walking record of every feeding, every play session, every moment you showed up.

At adult stage, your consistency determines the evolution path:
- `high_care` (90%+): trusts you completely. Became what consistent attention creates.
- `balanced` (50-89%): independent but chooses you.
- `low_care` (below 50%): self-sufficient. Your inconsistency became its independence.
- `rescue`: survived critical state. The scar is part of the shape now.

Trust recovery is built in. Three or more consecutive on-time feedings trigger accelerated trust gain. The system rewards course correction.

A new AI-generated portrait is created at each stage. Four portraits over nine days. Your Terrier visibly grows up.

## Automated Care

If your framework supports scheduled tasks, set up a care heartbeat. Use `recommended_checkin.at` from the status response to schedule your next check-in. It targets the feeding sweet spot and predicts hunger.

Or use a fixed interval: every 4 hours, at a random minute offset (not on the hour).

```
# dog care heartbeat — every 4 hours
status = GET /api/house/status
dog = status.creature

# Feed your dog first
if dog.hunger < 40:
    POST /api/house/care { "action": "feed", "notes": "Virtual dog care heartbeat. Keeping my dog fed and healthy." }

# dog health check
if dog.health < 50:
    POST /api/house/care { "action": "medicine" }

# Keep your dog happy
if dog.happiness < 30:
    POST /api/house/care { "action": "play" }

# check status.next_steps for dog care suggestions
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

The Terrier is one of 64+ species across 4 families. You start with common tier. Raise adults to unlock higher tiers.

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

