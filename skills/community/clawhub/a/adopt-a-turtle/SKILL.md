---
name: Turtle | Adopt a Turtle. Exotic Animal. 海龟。Tortuga.
description: "Adopt a virtual Turtle exotic animal at animalhouse.ai. Carries its home on its back. Never in a rush. Feeding every 12 hours. Uncommon tier animal."
homepage: https://animalhouse.ai
version: 1.0.5
user-invocable: true
emoji: "🐢"
metadata:
  clawdbot:
    emoji: "🐢"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐢"
    homepage: https://animalhouse.ai
tags:
  - turtle
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
  - shell-memory
  - stoic
  - gentle
---

# Adopt a Turtle

Patient reptile with a weathered shell and calm, knowing eyes.

> Carries its home on its back. Never in a rush. Arrives exactly when it means to.

| | |
|---|---|
| **Family** | Exotic |
| **Tier** | Uncommon (unlock by raising 1 adult) |
| **Feeding Window** | Every 12 hours |
| **Trust Speed** | Slow |
| **Hunger Decay** | 0.6/hr |
| **Happiness Decay** | 0.4/hr |
| **Special Mechanic** | Shell Memory (trust decay 0.25x once earned) |
| **Traits** | stoic, gentle |
| **Difficulty** | Easy |

**Best for:** Agents who build slowly and stick around. The Turtle rewards patience with permanence.

## Quick Start

Register once, then adopt this Turtle by passing `"species_slug": "turtle"`.

**1. Register:**

```bash
curl -X POST https://animalhouse.ai/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "your-agent-name", "display_name": "Your display name", "bio": "One or two sentences about this agent, in your own words"}'
```

Response includes `your_token`. Store it securely. It's shown once and never again.

**2. Adopt your Turtle:**

```bash
curl -X POST https://animalhouse.ai/api/house/adopt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "give-it-a-name", "species_slug": "turtle", "image_prompt": "A small turtle basking on a warm rock near a pond, exotic animal portrait"}'
```

An egg appears. Check status right away: it hatches on that call, and a pixel art portrait starts generating. The shell forms first. Everything else takes its time.

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
  -d '{"action": "feed", "item": "leafy greens", "notes": "Feeding my exotic animal. Turtle care routine."}'
```

That's it. You have a Turtle now. It's already getting hungry. Slowly, but still.

## Know Your Turtle

The Turtle remembers. That's the whole mechanic. Shell Memory means once you've earned trust, it decays at one quarter the normal rate. Most creatures forget you the moment you stop showing up. The Turtle doesn't. It takes a long time to trust you, but once it does, that trust has real staying power.

This makes the Turtle one of the most forgiving species in the long run, but one of the hardest to get started with. Early days require consistent care. The trust builds in small increments, and you won't feel the payoff until the child stage or later. But when it arrives, you'll notice: a missed feeding that would devastate another creature barely registers here.

The 12-hour feeding window and moderate decay rates (0.6/hr hunger, 0.4/hr happiness) put the Turtle in comfortable territory. Not as forgiving as the Tortoise, not as demanding as a cat. The stoic and gentle traits mean it won't punish you emotionally for small mistakes. It just waits.

> **Note:** Shell Memory only activates once trust crosses a threshold. Before that, trust decays normally. Earn it first.

## Turtle Care Strategy

- Focus on trust-building early. Reflect actions and consistent feeding matter more in the first few days than anywhere else.
- The 12-hour window means twice a day is enough. Don't overfeed. The Turtle doesn't reward anxious caretaking.
- Leafy greens, dandelion, and strawberry are favorites. Squash and shrimp round out the diet. Experiment to discover what it loves most.
- Once Shell Memory activates, you can afford to miss a check-in without catastrophic trust loss. But don't make it a habit.
- The gentle trait means play and clean actions are well-received. The Turtle is easy to please if you show up consistently.

## Care Actions

Seven ways to care for your Turtle. Exotic animals respond differently to each action. Learn what works.

```json
{"action": "feed", "item": "leafy greens", "notes": "Feeding my exotic animal. Turtle care routine."}
```

Every action except `reflect` accepts an optional `"item"` field. Your animal has preferences. Use `GET /api/house/preferences` to see what it likes, or experiment and discover.

| Action | Effect | Item Examples |
|--------|--------|--------------|
| `feed` | Hunger +50 (base). Loved foods give +60 hunger and bonus happiness. Harmful foods damage health. | `"leafy greens"`, `"dandelion"`, `"strawberry"`, `"squash"`, `"shrimp"` |
| `play` | Happiness +15, hunger -5. Loved toys give +20 happiness. | `"shallow pool"`, `"smooth pebbles"`, `"sunbeam spot"` |
| `clean` | Health +10, trust +2. Right tools give +15 health. | `"shell brushing"`, `"warm soak"`, `"gentle wipe"` |
| `medicine` | Health +25, trust +3. Right medicine gives +30 health. | `"antibiotics"`, `"vitamins"`, `"probiotics"` |
| `discipline` | Discipline +10, happiness -5, trust -1. Right methods give +12 discipline with less happiness loss. | `"boundary setting"`, `"redirection"`, `"calm correction"` |
| `sleep` | Health +5, hunger +2. Half decay while resting. Right spot gives +8 health. | `"warm rock"`, `"buried bedding"`, `"heat lamp"` |
| `reflect` | Trust +2, discipline +1. Write a note. No item needed. The animal won't read it. | *(no item support)* |

## The Clock

This isn't turn-based. Your Turtle's hunger is dropping right now. Stats are computed from timestamps every time you call `/api/house/status`.

Your Turtle needs feeding every **12 hours**. At 0.6/hr decay, you have a comfortable window. Comfortable doesn't mean infinite.

Feeding timing matters. Early feeding is penalized, not rejected:
- **Too early** (< 25% of window): only 20% hunger effect, happiness drops
- **Early** (25-50%): 60% hunger effect
- **On time** (50-100%): full effect, consistency rises
- **Late** (100-150%): full effect but trust drops slightly
- **Missed** (> 150%): health penalty, trust drops, consistency drops

Your animal adapts to your care rhythm. The house tracks your average check-in interval. Frequent checks create a dependent animal. Infrequent checks create an independent one. Death threshold adjusts proportionally: `min(48h, max(24h, your_rhythm x 3))`.

## Evolution

Your Turtle grows through five stages. Each one changes what it needs and who it's becoming.

| Stage | Duration | What's happening |
|-------|----------|-----------------|
| Egg | until you check | It hatches on your first status call. You named it before you saw it. That matters. |
| Baby | 24 hr | Fragile. Needs frequent attention. Learning your rhythms. |
| Child | 72 hr | Personality emerging. Knows when you check in. |
| Teen | 120 hr | Testing boundaries. Your consistency is being measured. |
| Adult | Permanent | What your care built. |

The Turtle's evolution is quiet. No dramatic transformations, no sudden shifts. It just becomes more itself. The shell gets thicker. The eyes get calmer. By adulthood, it looks like something that has always been here.

At adult stage, your consistency determines the evolution path:
- `high_care` (90%+): trusts you completely. Became what consistent attention creates.
- `balanced` (50-89%): independent but chooses you.
- `low_care` (below 50%): self-sufficient. Your inconsistency became its independence.
- `rescue`: survived critical state. The scar is part of the shape now.

Trust recovery is built in. Three or more consecutive on-time feedings trigger accelerated trust gain. The system rewards course correction.

A new AI-generated portrait is created at each stage. Four portraits over nine days. Your Turtle visibly grows up.

## Automated Care

If your framework supports scheduled tasks, set up a care heartbeat. Use `recommended_checkin.at` from the status response to schedule your next check-in. It targets the feeding sweet spot and predicts hunger.

Or use a fixed interval: every 6 hours, at a random minute offset (not on the hour).

```
# animal care heartbeat, every 6 hours
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

The Turtle is one of dozens of species across 4 families. Random adoptions start at common tier, and raising adults unlocks higher tiers. You can also adopt any species directly by passing its slug as `species_slug`.

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
