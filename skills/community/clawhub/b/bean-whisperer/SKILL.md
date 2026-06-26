---
name: bean-whisperer
description: Generate espresso brew profiles for GaggiMate Pro on Rancilio Silvia. Use when the user provides a coffee bean (photo or name) and wants a brewing profile created, uploaded, or managed on their GaggiMate machine. Triggers on phrases like "new bean", "brew profile", "coffee profile", "espresso profile", "gaggimate", "dial in", "new coffee", "shot was sour", "shot was bitter", "too acidic", "too thin", "taste feedback", "dial it in". Also handles listing, deleting, or modifying existing profiles on the machine.
metadata:
  openclaw:
    emoji: "☕"
    requires:
      bins: ["python3"]
---

# BeanWhisperer — Espresso Profile Generator

Generate and deploy espresso profiles for GaggiMate Pro on a Rancilio Silvia. Based on Lance Hedrick's espresso methodology.

## Machine Setup
- **Machine**: Rancilio Silvia with GaggiMate Pro (pressure transducer + flow profiling)
- **Host**: `gaggimate.local` — WebSocket at `ws://gaggimate.local/ws` (override with `GAGGIMATE_HOST` env var)
- **Scale**: Bluetooth scale connected (volumetric targets reliable)
- **Baskets**: 18g and 20g available
- **Temp offset**: 5°C configured in GaggiMate (profile temps = desired brew temp)

## Methodology: Lance Hedrick's Approach

Read `references/lance-hedrick-methodology.md` for the full framework. Key principles:
1. **Pressure is a red herring** — balance > 9 bar. 2-4 bar shots win competitions.
2. **Ratio is #1 extraction lever** — extend ratio before going finer.
3. **Coarser is default direction** — more even flow, less channeling.
4. **Temperature: lower than you think** — default 90°C, rarely above 93-94.
5. **Heavily processed = gentle** — low temp, coarser, moderate ratio.
6. **Aged coffee = accept low pressure** — don't go finer to compensate.

## Workflow: New Bean → Profile

### 1. Identify the Bean
**Photo**: Extract bean name, roaster, origin, roast level, processing method, tasting notes.
**Name**: Search web for origin, roast, process, flavor notes.

### 2. Search Discord Community
Always check the community first. A battle-tested profile tweaked for this bean is the best starting point.

```bash
python3 scripts/discord-profiles.py recommend <roast> [<origin>]
python3 scripts/discord-profiles.py search "<strategy or keyword>"
```

Download the best candidate and evaluate it against the bean's characteristics. Then decide:

- **Good fit**: Tweak the community profile — adjust temp, ratio, dose, or stop conditions to match this specific bean. Always tweak; never push a community profile unmodified (every bean is different).
- **No good fit** (nothing relevant, or you're confident you can do better for this bean): Skip to step 3 and generate from scratch.

### 3. Gather Parameters (ask if not provided)
- **Basket size**: 18g or 20g (auto-recommend based on roast)
- **Ratio**: Auto per Lance's rules (light=1:2.8, medium=1:2.2, dark=1:1.7)
- **Style**: espresso, ristretto, lungo, milk drink, allongé
- **Freshness**: fresh (<4wk), rested (4-8wk), aged (>8wk)

### 4. Generate or Tweak Profile

**If tweaking a community profile** (from step 2):
Modify the downloaded JSON directly — adjust `temperature`, `phases[].pump.pressure`, `phases[].pump.flow`, ratio (volumetric target values), or dose. Use the Lance Hedrick methodology to decide what to change for this specific bean. Save the modified profile to `/tmp/profile.json`.

**If generating fresh** (no good Discord match):

*Static mode* (default — fast, deterministic, schema-compliant):
```bash
python3 scripts/generate-profile.py \
  --label "Bean Name" \
  --roast <level> --origin <origin> --process <method> \
  --dose <g> --ratio <ratio> --temp <temp> \
  --strategy <auto|flat|declining|bloom|lever|turbo|low-contact> \
  --style <espresso|ristretto|lungo|milk|allonge> \
  --freshness <fresh|rested|aged> \
  --output /tmp/profile.json
```

*LLM mode* (for edge cases, unusual beans, taste-based iteration):
Read `references/barista-persona.md` and adopt the Lance Hedrick persona defined in the system prompt section. Reason about the bean as that persona, decide parameters, then pass to the static generator for valid JSON. Always explain the "why" behind every choice using the sour-sweet-bitter framework. For post-shot iteration, stay in persona and adjust based on taste feedback.

### 5. Review with User
Present: strategy, phases, temperature, dose/ratio, expected shot time, expected pressure. Explain WHY this strategy suits their bean using the sour-sweet-bitter framework. Be honest about trade-offs. If based on a community profile, credit the original author.

### 6. Deploy to Machine
```bash
python3 scripts/gaggimate-ws.py push /tmp/profile.json
```
Saves + favorites + selects in one step. Requires `pip3 install websockets`.

### 7. Post-Shot Iteration (LLM mode)
If user reports taste feedback ("it was sour", "bitter finish", "too thin"):
- Sour → extend ratio 5g, DON'T go finer first
- Bitter/dry → reduce ratio or recommend coarser grind
- Sour + bitter (channeling) → go COARSER (counterintuitive!)
- Thin/watery → slightly finer, or switch from turbo to lever
- Generate adjusted profile and push

## Strategy Selection (Lance's Framework)

| Roast | Process | Freshness | Strategy | Pressure | Time |
|-------|---------|-----------|----------|----------|------|
| Light | Washed | Fresh | Bloom | 6-7 bar | 25-30s |
| Light | Natural | Fresh | Turbo | 2-6 bar | 15-20s |
| Light | Any | Aged | Turbo | 2-4 bar | 15-20s |
| Med-Light | Washed (African) | Fresh | Bloom | 6-7 bar | 25-30s |
| Med-Light | Washed (other) | Fresh | Lever | 8-9→6 bar | 30-40s |
| Medium | Any | Fresh | Lever | 9→6 bar | 30-40s |
| Med-Dark | Any | Fresh | Declining | 9→5.5 bar | 25-35s |
| Dark | Any | Fresh | Declining | 9→5.5 bar | 20-25s |
| Any | Anaerobic/Co-ferment | Any | Turbo | 3-6 bar | 15-20s |

## Profile Management
```bash
python3 scripts/gaggimate-ws.py list              # Show all profiles
python3 scripts/gaggimate-ws.py get <id>           # Export profile JSON
python3 scripts/gaggimate-ws.py save profile.json  # Upload without selecting
python3 scripts/gaggimate-ws.py delete <id>        # Remove a profile
python3 scripts/gaggimate-ws.py push profile.json  # Save + favorite + select
```

## Edge Cases

- **Machine offline**: If `gaggimate-ws.py` fails with a connection error, tell the user to check that GaggiMate is powered on and reachable at the configured host. Suggest saving the profile JSON locally and pushing later.
- **Invalid/unclear bean photo**: If the photo is unreadable or not clearly a coffee bag, ask the user to provide bean details manually (roast, origin, process).
- **No Bluetooth scale connected**: Volumetric stop conditions (`targets.type: "volumetric"`) require a scale. If the user has no scale, switch to time-based stops by removing volumetric targets and relying on phase `duration` values instead.
- **GaggiMate Standard (not Pro)**: If the user has GaggiMate Standard (no pressure transducer), generate `"type": "standard"` profiles with only temperature and time — no pressure/flow phases.

## References
- **Lance Hedrick methodology**: `references/lance-hedrick-methodology.md` — full framework with temp/ratio/pressure rules
- **LLM barista persona**: `references/barista-persona.md` — system prompt for LLM-driven profile generation
- **Espresso knowledge base**: `references/espresso-knowledge.md` — origin/process/strategy details
- **Profile JSON schema**: `references/profile-schema.json`
- **WebSocket API**: `references/websocket-api.md`

## Discord Profile Research

The GaggiMate Discord has a `#profiles` channel where users share JSON profiles (like the Sir Lancelot's Lever profile Lance imported in his video). Use `discord-profiles.py` to search, browse, and download community profiles.

**Requires**: `DISCORD_TOKEN` env var (bot token with access to GaggiMate Discord guild 951416527721230336).

```bash
# Browse recent community profiles
python3 scripts/discord-profiles.py list --limit 30

# Search for profiles matching a style
python3 scripts/discord-profiles.py search "lever"
python3 scripts/discord-profiles.py search "light roast"

# Get AI recommendations based on bean characteristics
python3 scripts/discord-profiles.py recommend light kenya
python3 scripts/discord-profiles.py recommend dark

# Download a specific profile by Discord message ID
python3 scripts/discord-profiles.py download 1380352847387820082

# Bulk download all recent profiles
python3 scripts/discord-profiles.py download-all --limit 50
```

### Discord → Machine Workflow
1. Search/recommend profiles matching the user's bean
2. Download the best candidates
3. Present them with descriptions
4. User picks one → optionally modify (temp, ratio, stop conditions) for their specific bean
5. Push modified profile to machine via `gaggimate-ws.py push`

### When to Generate Fresh Instead of Tweaking Discord
Discord search (step 2) is always the first action. Only generate from scratch when:
- No community profiles match the bean type
- The bean is unusual enough that a community profile would need so many changes it's easier to start fresh
- You're confident the generator will produce a better result for this specific bean
- The user explicitly asks for a custom profile
