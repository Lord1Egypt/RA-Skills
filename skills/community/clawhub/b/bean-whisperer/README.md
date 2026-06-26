<p align="center">
  <h1 align="center">BeanWhisperer</h1>
  <p align="center">
    <em>Your AI barista that speaks fluent GaggiMate.</em>
  </p>
  <p align="center">
    <a href="https://github.com/zsiddique/bean-whisperer/actions/workflows/ci.yml"><img src="https://github.com/zsiddique/bean-whisperer/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
    <a href="https://github.com/zsiddique/bean-whisperer/actions/workflows/semgrep.yml"><img src="https://img.shields.io/badge/security-semgrep-blue" alt="Semgrep"></a>
    <a href="https://github.com/zsiddique/bean-whisperer/actions/workflows/validate-skill.yml"><img src="https://github.com/zsiddique/bean-whisperer/actions/workflows/validate-skill.yml/badge.svg" alt="SKILL.md"></a>
    <a href="https://clawhub.ai/zsiddique/bean-whisperer"><img src="https://img.shields.io/badge/ClawHub-bean--whisperer-orange" alt="ClawHub"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT"></a>
  </p>
</p>

---

> **Snap a photo of your beans. Get a dialed-in pressure profile. Push it to your machine. Sip.**
>
> BeanWhisperer is an AI-powered espresso profile generator for [GaggiMate](https://gaggimate.eu/) Pro machines. It encodes [Lance Hedrick's](https://www.youtube.com/@LanceHedrick) espresso methodology into a tool that reasons about your coffee, generates optimized pressure profiles, and deploys them over WebSocket — all from a single conversation.

---

## How It Works

```
  Bean Photo / Name
        |
        v
  [Identify Bean] -----> roast, origin, process, freshness
        |
        v
  [Generate Profile] --> strategy, temp, ratio, dose, phases
        |
        v
  [Push to Machine] ---> ws://gaggimate.local/ws
        |
        v
  [Taste Feedback] ----> "too sour" / "bitter" / "thin"
        |
        v
  [Adjust & Re-push] --> iterate until dialed in
```

## Quick Install

### ClawHub (Recommended)

```bash
clawhub install bean-whisperer
```

### OpenClaw Workspace

```bash
cd ~/.openclaw/workspace/skills
git clone git@github.com:zsiddique/bean-whisperer.git
```

### Standalone

```bash
pip install websockets aiohttp
```

## Talk to It

Once installed as an OpenClaw or ClawHub skill, just talk naturally:

| You say | BeanWhisperer does |
|---------|-------------------|
| *Send a photo of a bean bag* | Identifies the bean, generates a profile, explains why |
| "New bean: Onyx Tropical Weather" | Researches it, picks strategy, creates profile |
| "Find me a lever profile for dark roast" | Searches Discord community profiles |
| "Push it to my machine" | Deploys via WebSocket in one command |
| "It was a bit sour" | Extends ratio (not finer!), re-pushes adjusted profile |
| "Make it an allonge" | Switches to low-contact strategy, 1:3.5 ratio |

The agent adopts a Lance Hedrick-style barista persona — it explains *why* every parameter was chosen using the sour-sweet-bitter framework.

## Profile Strategies

Six pressure profile strategies, auto-selected based on your bean:

| Strategy | Best For | Pressure | Time |
|----------|----------|----------|------|
| **bloom** | Light washed, African | 6-7 bar | 25-30s |
| **turbo** | Ultra light, processed, aged | 2-6 bar | 15-20s |
| **lever** | Medium, balanced | 8-9 bar declining | 30-40s |
| **declining** | Medium-dark, dark | 9 to 5.5 bar | 25-35s |
| **flat** | Any (safe starting point) | 9 bar sustained | 25-35s |
| **low-contact** | Ultra light geisha | 1-3 bar | 15-20s |

### Auto-Selection

| Roast | Process | Strategy |
|-------|---------|----------|
| Light | Washed | bloom |
| Light | Natural | turbo |
| Medium-light | Washed (African) | bloom |
| Medium-light | Washed (other) | lever |
| Medium | Any | lever |
| Medium-dark / Dark | Any | declining |
| Any | Anaerobic / Co-ferment | turbo |
| Any (aged >8 weeks) | Any | turbo |

## Lance Hedrick's Methodology

> *"Pressure is a red herring."*

1. **Pressure is a red herring** — balance > 9 bar. World-class espresso at 2-4 bar.
2. **Ratio is #1** — extend ratio before going finer.
3. **Coarser is default** — more even flow, less channeling.
4. **Temperature: lower than you think** — default 90C, rarely above 93-94.
5. **Processed coffees need gentleness** — low temp, coarser, moderate ratio.
6. **Aged coffee: accept low pressure** — don't go finer to compensate.
7. **Crema does not equal quality** — a balanced thin shot beats a thick channeled mess.

See [`references/lance-hedrick-methodology.md`](references/lance-hedrick-methodology.md) for the full framework.

## CLI Usage

### Generate a Profile

```bash
python3 scripts/generate-profile.py \
  --label "Ethiopian Yirgacheffe" \
  --roast light --origin ethiopia --process washed \
  --output my-profile.json
```

All parameters auto-select based on the bean. Override any of them:

```bash
python3 scripts/generate-profile.py \
  --label "My Custom Profile" \
  --roast medium --origin colombia --process natural \
  --dose 18 --ratio 2.2 --temp 91 --strategy lever \
  --style espresso --freshness fresh --output custom.json
```

### Push to Machine

```bash
python3 scripts/gaggimate-ws.py push my-profile.json    # save + favorite + select
python3 scripts/gaggimate-ws.py list                     # show all profiles
python3 scripts/gaggimate-ws.py get <id>                 # export profile JSON
python3 scripts/gaggimate-ws.py delete <id>              # remove a profile
```

### Browse Discord Community Profiles

```bash
python3 scripts/discord-profiles.py list                 # recent profiles
python3 scripts/discord-profiles.py search "lever"       # search by name
python3 scripts/discord-profiles.py recommend light kenya # AI recommendations
python3 scripts/discord-profiles.py download <thread-id>  # download profile
```

## Environment Variables

```bash
# Override GaggiMate hostname (default: gaggimate.local)
export GAGGIMATE_HOST=192.168.1.100

# Discord community profiles (store in ~/.config/gaggimate/discord-token)
export DISCORD_TOKEN="your-token"
```

## Parameters Reference

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `--label` | string | *(required)* | Profile name on machine |
| `--roast` | light, medium-light, medium, medium-dark, dark | *(required)* | Drives strategy/temp/ratio |
| `--origin` | ethiopia, colombia, brazil, kenya, sumatra, guatemala, costarica, blend, other | other | Affects strategy for certain roasts |
| `--process` | washed, natural, honey, anaerobic, co-ferment, unknown | washed | Anaerobic/co-ferment = gentle |
| `--dose` | 17-20 | auto | 20g light, 18g darker |
| `--ratio` | 1.5-3.5 | auto | Lance's ratio rules |
| `--temp` | 85-96 | auto | Roast + process based |
| `--strategy` | auto, bloom, turbo, lever, declining, flat, low-contact | auto | Override auto-selection |
| `--style` | espresso, ristretto, lungo, milk, allonge | espresso | Adjusts ratio target |
| `--freshness` | fresh, rested, aged | fresh | Aged = turbo strategy |

## Machine Compatibility

Built for **Rancilio Silvia + GaggiMate Pro**, works on any GaggiMate machine:

- Gaggia Classic / Classic Pro / Evo
- Rancilio Silvia (all versions)
- Any machine with GaggiMate Pro (pressure transducer + flow profiling)
- GaggiMate Standard (basic `"type": "standard"` profiles)

## Examples

Pre-generated profiles in [`examples/`](examples/):

| File | Bean | Strategy |
|------|------|----------|
| `light-washed-bloom.json` | Light Ethiopian | bloom |
| `medium-lever.json` | Medium Colombian | lever |
| `dark-declining.json` | Dark Italian blend | declining |
| `anaerobic-turbo.json` | Anaerobic natural | turbo |
| `geisha-allonge.json` | Light Geisha | low-contact |
| `sir-lancelots-lever.json` | Community (Lance's) | lever |

## Community

- [GaggiMate Discord](https://discord.gg/APw7rgPGPf) — `#profiles` channel
- [GaggiMate Docs](https://docs.gaggimate.eu/docs/profiles/) — Official profile docs
- [GaggiMate Firmware](https://github.com/jniebuhr/gaggimate) — Source code

## Credits

- **[GaggiMate](https://gaggimate.eu/)** by Jokim Niebuhr — the firmware making this possible
- **[Lance Hedrick](https://www.youtube.com/@LanceHedrick)** — espresso methodology and philosophy
- **GaggiMate Discord community** — profile strategies and testing

## License

MIT
