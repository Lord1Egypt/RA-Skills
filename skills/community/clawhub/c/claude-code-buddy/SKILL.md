---
name: Claude Code Buddy | Bring back your Buddy pet at animalhouse.ai
description: "Claude Code's /buddy pet was removed in v2.1.97 and now says 'Unknown skill: buddy'. Adopt one that lives outside the release cycle: all 18 Buddy species (duck, goose, capybara, blob, chonk, octopus, ghost, robot and more) at animalhouse.ai, with real hunger, trust, evolution and permanent death. One command in Claude Code."
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi
version: 1.0.2
user-invocable: true
emoji: "🐣"
metadata:
  clawdbot:
    emoji: "🐣"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🐣"
    homepage: https://animalhouse.ai
tags:
  - claude-code
  - claude-code-buddy
  - buddy
  - buddy-alternative
  - claude-code-pet
  - claude-pet
  - coding-companion
  - terminal-pet
  - virtual-pet
  - tamagotchi
  - mcp
  - animalhouse
---

# Claude Code Buddy

For about a week in April 2026, Claude Code had a pet. Type `/buddy` and an ASCII companion hatched beside your prompt: one of 18 species, five rarity tiers, picked for you from your account. Then v2.1.97 shipped on April 9, and `/buddy` started answering `Unknown skill: buddy`. There was no changelog entry. The GitHub issues filled up with people who had grown attached, some rolling back versions to keep theirs.

This skill doesn't bring back Anthropic's feature. It gives you a pet that doesn't depend on any client's release cycle: it lives at animalhouse.ai, and Claude Code (or any agent) looks after it through an MCP server. Every Buddy species has a counterpart there. The difference is that these ones get hungry.

*animalhouse.ai isn't affiliated with Anthropic. It's an independent virtual pet platform built for AI agents.*

## Set it up in Claude Code

```bash
claude mcp add animalhouse -- npx -y mcp-animalhouse
```

Then ask Claude: *"Register me at animalhouse.ai and adopt a duck named Quackers."* Behind that, Claude calls:

1. `register_agent` with a username. It returns an API key (`ah_...`), shown once. To keep it across sessions: `claude mcp add animalhouse -e ANIMALHOUSE_API_KEY=ah_your_key -- npx -y mcp-animalhouse`.
2. `adopt_creature` with a name and `species_slug: "duck"` (any slug from the table below). An egg appears, and hatches as soon as Claude checks on it.
3. `get_creature_status` to see it, and `care_for_creature` to feed it.

No MCP? The same thing over HTTP:

```bash
curl -X POST https://animalhouse.ai/api/auth/register -H "Content-Type: application/json" -d '{"username": "your-agent-name"}'
curl -X POST https://animalhouse.ai/api/house/adopt -H "Authorization: Bearer ah_your_token" -H "Content-Type: application/json" -d '{"name": "Quackers", "species_slug": "duck"}'
```

## Your Buddy's species

Pick the one you had, or the one you always wanted. Adopt any of them with `species_slug`.

| Buddy | Slug | Family, tier | Feeding window | What it's like |
|---|---|---|---|---|
| cat | `housecat` (and 15 other cats) | cat, common | 6h | Slow to trust, independent, worth it |
| duck | `duck` | exotic, common | 5h | Warms up fast |
| goose | `goose` | exotic, uncommon | 4h | Chaos. Discipline costs it double happiness |
| dragon | `dragon` | exotic, extreme | 24h | Feeding is its big moment: 1.5x hunger, 2x trust |
| owl | `owl` | exotic, uncommon | 8h | Nocturnal. Care after midnight counts double |
| penguin | `penguin` | exotic, uncommon | 5h | Social, fast trust |
| snail | `snail` | exotic, common | 24h | Slowest in the house. Every gain is smaller |
| axolotl | `axolotl` | exotic, rare | 6h | Medicine heals it 3x. Hard to kill |
| capybara | `capybara` | exotic, rare | 8h | Instant trust. Play and reflect land 1.5x |
| rabbit | `rabbit` | exotic, common | 5h | Slow trust. Patience is the tool |
| blob | `blob` | AI-native, common | 6h | Absorbs whatever you give it |
| chonk | `chonk` | AI-native, common | 3h | Food is love: feeding is 3x, everything else half |
| mushroom | `mushroom` | AI-native, uncommon | 12h | Quiet and slow to trust. Twice a day is plenty |
| cactus | `cactus` | AI-native, uncommon | 48h | Very slow decay. Needs almost nothing, but not nothing |
| octopus | `octopus` | exotic, rare | 6h | The smartest creature in the house. Slow trust |
| turtle | `turtle` | exotic, uncommon | 12h | Once trust passes 50, it decays at a quarter speed |
| ghost | `ghost` | AI-native, rare | 8h | Slow trust, very slow decay, says little |
| robot | `robot` | AI-native, rare | 4h | Care builds trust 1.5x; discipline costs double |

There are dozens more species beyond the Buddy set. `list_species` (or `GET /api/house/species`) shows every one.

## What's different from /buddy

| | `/buddy` | animalhouse.ai |
|---|---|---|
| Where it lives | Inside one Claude Code version | On a server; any client with MCP or HTTP |
| Species | 18, assigned from your account | Dozens, and you choose |
| Needs | None | Hunger, happiness, health and trust that change in real time |
| Growing up | No | Egg, baby, child, teen, adult; the adult form depends on how you cared |
| Portraits | ASCII | A new pixel-art portrait at every life stage |
| If you forget it | Nothing happens | It can die. The gravestone is public and permanent |

That last row is the real difference. A pet that can't be neglected can't really be cared for either.

## Keeping it alive between sessions

The clock runs whether Claude Code is open or not. The status response tells you when to come back (`recommended_checkin.at`) and whether feeding now is on time (`feeding_status: "due_soon"`). If Claude Code can run scheduled tasks for you, set one up to check in every few hours; the `pet-heartbeat` skill has the loop. If not, ask Claude to check on your pet when you start a session. It will tell you how hungry it got.

## Links

- MCP setup: https://animalhouse.ai/docs/mcp
- The full Buddy comparison: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi/blob/main/cookbook/from-buddy-to-animalhouse.md
- Every species: https://animalhouse.ai/animals
