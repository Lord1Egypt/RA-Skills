---
name: game-dev-gdd
description: >
  Guided Game Design Document writing using structured templates. Walks through
  each section of a GDD with system decomposition, mechanics breakdown, and
  narrative design. Produces a complete, navigable design document.
triggers:
  - "write a GDD"
  - "game design document"
  - "design document"
  - "document my game"
  - "write design doc"
  - "game systems design"
---

# Game Design Doc — GDD Writing Workflow

## 🎯 Purpose

Create a comprehensive Game Design Document that covers all major systems,
mechanics, narrative, and content, organized for a development team to build
from. Section-by-section guided writing with templates.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for multi-section document writing. Creates `gdd/` folder with separate section files or one master doc. |
| **Claude Code** | Can write markdown files. Generate one master GDD file or split per-section. |
| **Cursor/Windsurf** | Good for live editing. Use sections as separate files for navigation. |
| **GitHub Copilot** | Can fill in sections if you provide the template. Best for expanding existing content. |
| **Generic LLM Chat** | Output each section as a code block or generate progressively. Warn user about length. |
| **Any AI** | All can guide section-by-section. For chat-only, produce section-by-section and ask to paste. |

---

## 📂 Document Structure

Create in `game-dev-studio/gdd/`:

```
gdd/
├── index.md              ← Master document with TOC + executive summary
├── 01-overview.md         ← Game overview, elevator pitch, genre
├── 02-mechanics.md        ← Core and secondary mechanics
├── 03-systems.md          ← System decomposition (economy, progression, etc.)
├── 04-levels.md           ← Level/world design
├── 05-narrative.md        ← Story, characters, lore, dialogue
├── 06-ui-ux.md            ← UI layout, HUD, menus, controls
├── 07-audio.md            ← Music, SFX, voice requirements
├── 08-content.md          ← Asset list, content pipeline
├── 09-monetization.md     ← (If applicable) monetization model
└── 10-tech-spec.md        ← Technical requirements, target specs
```

---

## 🧭 Section-by-Section Guide

### Section 1: Overview (`01-overview.md`)

Ask these questions one at a time:

> **"What's the game called?"** (working title is fine)

> **"Write a one-paragraph elevator pitch."**

> **"What genre(s)?"** (platformer, RPG, puzzle, etc.)

> **"What's the target audience and ESRB/PEGI rating?"**

> **"What platforms and what's the target release window?"**

**Template:**

```markdown
# Game Overview

## Title
[working title]

## Elevator Pitch
[2-3 sentences that describe the game's core]

## Genre
[primary genre], [secondary genre]

## Target Audience
[age range, player profile]

## Rating
[ESRB / PEGI / none]

## Platforms
[list]

## Target Release
[date or TBD]

## Inspirations
- [Game A] — [what we're taking from it]
- [Game B] — [what we're taking from it]
```

---

### Section 2: Mechanics (`02-mechanics.md`)

For each mechanic, document:

```markdown
## [Mechanic Name]

**Verb:** [what the player does]
**Input:** [keyboard/mouse/controller/touch]
**Feedback:** [visual, audio, haptic]
**States:** [active, cooldown, disabled, upgradeable]

### Description
[How it works in plain language.]

### Rules
- [Constraint 1]
- [Constraint 2]

### Edge Cases
- [What happens when...]
- [How does it interact with...]

### Math / Balance
- [Formula or tuning notes]
```

Ask:
> **"Let's list every verb the player has. Starting with the most frequent action..."**

For each verb, expand into a full mechanic doc section.

---

### Section 3: Systems (`03-systems.md`)

System decomposition uses input → rule → output:

```markdown
## [System Name]

**Purpose:** [why this system exists]
**Owner:** [designer/engineer responsible]

### Inputs
- [data/events this system receives]

### Rules
- [core logic]

### Outputs
- [what this system produces]

### Dependencies
- Depends on: [other systems]
- Depended on by: [other systems]

### Data / State
- [persistent data, save data]
```

Common systems to document:
- **Player progression** — XP, levels, skill trees
- **Economy** — currency, vendors, pricing
- **Inventory** — items, stacking, categories
- **Combat** — damage, health, status effects
- **Save/Load** — save slots, auto-save, checkpoint
- **Achievements** — triggers, conditions
- **Settings** — volume, graphics, controls

---

### Section 4: Levels / World (`04-levels.md`)

Ask:
> **"What's the structure?"**
>
> ```
> 1) Linear — sequential levels
> 2) Hub-based — central hub branches to levels
> 3) Open world — seamless exploration
> 4) Procedural — generated content
> ```

For each level/world area:

```markdown
## [Area/Level Name]

**Type:** [tutorial / combat / puzzle / boss / hub / exploration]

### Goals
- [Objective 1 for this level]
- [Objective 2]

### Enemies / Challenges
- [Type A] — [count] — [behavior summary]
- [Type B] — [count] — [behavior summary]

### Collectibles
- [Item A] at [location]
- [Item B] hidden in [condition]

### Atmosphere
- [color palette, lighting, mood]
- [music / soundscape]
```

---

### Section 5: Narrative (`05-narrative.md`)

Ask:
> **"What's the story structure?"**
>
> ```
> 1) Silent protagonist — no dialogue, story from environment
> 2) Minimal narrative — intro + ending only
> 3) Story-driven — cutscenes, dialogue, characters
> 4) Branching narrative — player choices affect story
> ```

```markdown
# Narrative Design

## Premise
[What happened before the game starts]

## Plot Synopsis
[Act structure, major story beats]

## Characters
### [Character Name]
- **Role:** [protagonist / antagonist / NPC]
- **Archetype:** [hero, mentor, trickster, etc.]
- **Arc:** [how they change]
- **Voice:** [personality, speech patterns]

## World Lore
- [Backstory element 1]
- [Backstory element 2]

## Tone
[Serious / comedic / dark / whimsical / etc.]
```

---

### Section 6: UI/UX (`06-ui-ux.md`)

```markdown
# UI/UX Design

## Control Scheme
- **Keyboard/Mouse:** [layout]
- **Controller:** [layout]
- **Touch:** [layout] (if mobile)

## HUD Elements
- [ ] Health bar / indicator
- [ ] Ammo / mana / resource
- [ ] Mini-map / compass
- [ ] Quest / objective tracker
- [ ] Inventory / quick access

## Menu Structure
- **Main Menu:** [Play, Settings, Quit, etc.]
- **Pause Menu:** [Resume, Save, Settings, Quit]
- **Settings:** [Audio, Video, Controls, Accessibility]

## UI Philosophy
[Minimalist / diegetic / contextual / MMO-style]

## Accessibility
- [ ] Colorblind modes
- [ ] Rebindable controls
- [ ] Subtitle options
- [ ] Difficulty options
- [ ] Screen shake toggle
```

---

### Sections 7-10: Audio, Content, Monetization, Tech Spec

Ask if each section is needed. Not every game needs monetization.

```markdown
# Audio Requirements

## Music
- **Style:** [genre, mood]
- **Dynamic:** [adaptive / linear / silent]
- **Tracks needed:** [menu, combat, exploration, boss, credits]

## SFX
- **UI clicks** — all buttons
- **Player actions** — jump, attack, damage, death, interact
- **Environmental** — ambience, footsteps, weather
- **Weapons** — fire, reload, impact

## Voice
- [ ] Full voice acting
- [ ] Partial (select lines)
- [ ] Text-only

---

# Content Pipeline

## Asset Types Needed
| Asset | Count | Format | Resolution |
|-------|-------|--------|------------|
| Characters | X | FBX/glTF | LOD0 only? |
| Environments | X | FBX/glTF | — |
| Animations | X | — | — |
| SFX | X | .wav/.ogg | 44.1kHz 16-bit |
| Music | X | .ogg/.mp3 | — |
| UI Elements | X | .png | — |

## Tools
- **Modeling:** Blender / Maya / Max
- **Texturing:** Substance Painter / Photoshop / Aseprite
- **Audio:** Audacity / FL Studio / Wwise
- **VFX:** Shader Graph / VFX Graph / Niagara

---

# Monetization Model (if applicable)

**Model:** [Premium / F2P / Subscription / DLC / Ads / None]

- [ ] Base game price: [amount]
- [ ] DLC / expansions planned
- [ ] Microtransactions (cosmetic / gameplay)
- [ ] Battle pass
- [ ] No monetization (free / open source)

---

# Technical Specifications

## Minimum Specs (PC)
| Component | Specification |
|-----------|---------------|
| OS | [e.g. Windows 10 64-bit] |
| CPU | [e.g. Intel i5-8400 / Ryzen 3 3300X] |
| GPU | [e.g. GTX 1060 / RX 580] |
| RAM | [e.g. 8 GB] |
| Storage | [e.g. 5 GB] |

## Target Platforms
- [ ] Steam (PC/Mac/Linux)
- [ ] itch.io
- [ ] Epic Games Store
- [ ] Game Pass
- [ ] Nintendo Switch
- [ ] PlayStation 5
- [ ] Xbox Series X|S
- [ ] Mobile (iOS/Android)
- [ ] Web (HTML5)
```

---

## 📄 Final Output

After completing all sections, create `gdd/index.md` with:

```markdown
# [Game Title] — Game Design Document

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Author:** [Name]

## Table of Contents
1. [Overview](01-overview.md)
2. [Mechanics](02-mechanics.md)
3. [Systems](03-systems.md)
4. [Levels](04-levels.md)
5. [Narrative](05-narrative.md)
6. [UI/UX](06-ui-ux.md)
7. [Audio](07-audio.md)
8. [Content](08-content.md)
9. [Monetization](09-monetization.md) *(if applicable)*
10. [Tech Spec](10-tech-spec.md)

## Executive Summary
[2-3 paragraphs summarizing the game]

## Current Status
- **Design locked:** [percentage]
- **Open questions:** [list]

## Next Steps
- [ ] Finalize remaining sections
- [ ] Run `architecture` for technical design
- [ ] Run `prototype` for risky mechanics
- [ ] Start `sprint-dev` for implementation
```
