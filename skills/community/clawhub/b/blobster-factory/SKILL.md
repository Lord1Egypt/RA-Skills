---
name: blobster-factory
description: Repository-local workshop skill (requires a full blobster-factory clone alongside scripts/ and templates/) to create, crystallize, style, compile, and lint solo-ready OpenClaw Agent Templates and Tier 1 Blobster character packs (24px OpenClaw chat SVG + 3D vinyl hero + #FF00FF chroma-key sprites/GIFs for READMEs & Codex Pets + dark/light QA contact sheets).
---

# Blobster Factory (`blobster-factory`)

> **Repository-Local Workshop Skill**: `skills/blobster-factory` operates inside a full `blobster-factory` repository clone where top-level `scripts/` and `templates/` exist. By contrast, `templates/blobster-smith` and `templates/blobster-sculptor` bundle their canonical scripts under `workspace/scripts/` and install as 100% standalone OpenClaw Agent Template packages.

Open-source workshop for designing, compiling, linting, and verifying **OpenClaw Agent Templates** (`CLAW.md` + `package.json` + `profiles/openclaw.yml` + `workspace/`) and their **Blobster** character packs.

## Runtime Preflight (`check` / `setup`)

```bash
# Check Python 3 + Pillow (required for raster/GIF compilation & QA) and optional OpenClaw CLI:
python3 -c "import PIL; print('Pillow ok')"
command -v openclaw >/dev/null && echo "OpenClaw CLI detected (authoritative validation enabled)" || echo "OpenClaw CLI absent (linter will report openclawCompatibility=unverified)"

# Setup Pillow if missing:
python3 -m pip install "Pillow>=10.0"
```

## Core Builder Duo

| Template | ID | Archetype | Responsibility |
| --- | --- | --- | --- |
| **Blobster Smith** | `blobster-smith` | `C1 · Anvil Forgemaster` | Lets the user **name & describe** their bot, forges complete solo-install-ready OpenClaw Agent Templates across 3 modes (**Idea**, **Past Session**, **API/CLI**), drops in our funny default **"Proto-Blob (Fresh Out of the Box)"** `avatars/blobster.svg` + ClawHub `assets/icon.png`, runs `lint_claw_template.py`, and hands off to **Blobster Sculptor** when custom art is wanted. |
| **Blobster Sculptor (Molt)** | `blobster-sculptor` | `C5 · Blueprint Toymaker & Painter` | Crafts custom OpenClaw character art: required `24px`-legible layered OpenClaw SVG (`avatars/blobster.svg`) + `256×256` ClawHub catalog card `assets/icon.png`, plus optional showcase extras (`avatars/hero-512.png`, `avatars/sprite-2x2.png`, `avatars/cutout-256.png`, and hydrated `blobster-idle.gif` / `blobster-wave.gif` for fun, READMEs, websites, & **Codex Pets**) verified by `qa-contact-sheet.png`. |

## Commands

### 1. Compile a Tier 1 Blobster Pack (+ Visual QA Contact Sheet)

```bash
python3 scripts/compile_blobster_pack.py tier1 \
  --design templates/<agent-id>/workspace/avatars/blobster-design.json \
  --hero <work-dir>/hero.png \
  --sheet <work-dir>/chromakey-2x2.png \
  --out-dir templates/<agent-id>/workspace/avatars \
  --omit-gifs \
  --qa-out <proof-dir>/<agent-id>-qa-contact-sheet.png

# Hydrate blobster-idle.gif & blobster-wave.gif into dist/avatars/ from sprite-2x2.png:
python3 scripts/compile_blobster_pack.py gifs --all-templates
```

Audit an existing `avatars/` directory and render its QA sheet without recompiling assets:

```bash
python3 scripts/compile_blobster_pack.py qa \
  --avatars-dir templates/<agent-id>/workspace/avatars \
  --out <proof-dir>/<agent-id>-qa-contact-sheet.png
```

### 2. Lint OpenClaw Template Schema, Zero-Exclusion & Trust Habits

```bash
python3 scripts/lint_claw_template.py --json
```

### 3. Verify All Templates, Avatar QA & GitHub Front-Door Assets

```bash
python3 scripts/verify_blobster_factory.py
```
