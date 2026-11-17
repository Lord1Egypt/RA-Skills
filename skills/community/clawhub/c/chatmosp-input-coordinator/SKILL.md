---
name: chatmosp-input-coordinator
description: |
  Entry skill of the chatMOSP system. Parses Chinese/English natural language input,
  recognizes three task types (MSR / KMC / parameter query), extracts metal, temperature,
  gas, partial pressure, steps, and size parameters, then dispatches
  parameter-builder, file-organizer, msr-generator, and kmc-simulator to complete
  the calculation.
  Triggers: user requests to run MSR or KMC, queries or adjusts parameters, or
  describes a metal catalysis system (Pd, Pt, Au, CO oxidation, water-gas shift, etc.).
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-input-coordinator

## 1. Core Responsibilities

1. Multilingual intent understanding — parse Chinese/English natural language input
2. Task recognition — identify MSR / KMC / parameter-query task types
3. Parameter extraction — extract metal, temperature, gas, partial pressure, steps, size
4. Skill dispatch — chain parameter-builder → file-organizer → calculation engine
5. Dialogue management — confirmation, clarification, error handling

## 2. Task Type Recognition

Three supported task types:

| Type | Meaning | Typical keywords |
|------|---------|------------------|
| MSR | Metal cluster structure generation | cluster, structure, morphology, nanoparticle, MSR |
| KMC | Kinetic Monte Carlo simulation | kinetic, simulation, TOF, steps, KMC, Monte Carlo |
| Parameter query | View or adjust parameters | parameter documentation, show parameters, parameter setting |

This ClawHub main test release supports only the legacy six-skill workflow
above. If the user requests EKMC, slab KMC, Stepwise EKMC, server submission, or
job monitoring, state that this main test release does not support those newer
features and do not route to non-existent skills.

Confidence threshold: 0.70. Below threshold → actively ask user for clarification.

## 3. Parameter Extraction

### 3.1 Required parameters

| Parameter | Recognition rules |
|-----------|-------------------|
| Metal element | Pd / Pt / Au / Cu / Ni (Chinese & English names) |
| Temperature | Supports °C and K, auto-converts to K |
| Pressure | Pa / kPa / MPa / atm |
| Gas species | CO / O₂ / H₂ / N₂ / CO₂ / NO |

### 3.2 Advanced parameters

- Gas partial pressure: CO9 (CO pp = 9%), O18 (O₂ pp = 18%); multiple gases joined with `_`: CO9_O18
- Cluster size: R50 (50 Å), R20 (default 20 Å)
- Simulation steps: 200000000steps, 1e6 steps, one million steps

### 3.3 Extraction examples

| User input | Extracted |
|------------|-----------|
| Pd 在 CO 氧化环境下 200 摄氏度结构 | metal=Pd, T=473K, gases=[CO, O₂] |
| Pt structure under CO oxidation at 400 Celsius | metal=Pt, T=673K, gases=[CO] |
| Run Pd MSR with CO9_O18 partial pressure at 473K, cluster size R50 | metal=Pd, T=473K, pp={CO:9,O₂:18}, R=50 |

## 4. Skill Dispatch

### 4.1 Routing table

```
MSR task        → parameter-builder → file-organizer → msr-generator
KMC task        → parameter-builder → file-organizer → kmc-simulator
Parameter query → parameter-builder
```

### 4.2 Cross-skill handoff (MUST follow)

- **MSR → KMC**: After MSR completes, it produces ini.xyz. For KMC, kmc-simulator independently fetches the full KMC parameter set (nspecies, s1/s2, p1, e1-e7, li) from MOSP_database. Do NOT reuse MSR's input.json. See kmc-simulator.
- **Parameter modification**: If user changes temperature, parameter-builder MUST recalculate gas entropy per §7.5.
- **Missing parameters**: If key parameters (E_ads, w, gamma) are missing, parameter-builder calls literature-search to fill the gap (open-access journals prioritized). See literature-search.
- **Visualization**: After MSR completes, msr-generator runs utils/paint.py to produce PNG + GIF. See msr-generator.
- **Wine environment**: KMC tasks are checked and managed by kmc-simulator. See kmc-simulator.

### 4.3 Error handling

| Situation | Action |
|-----------|--------|
| Missing parameters | Prompt user, suggest reasonable defaults |
| Task ambiguity | Offer 2–3 candidate scenarios |
| EKMC/slab/Stepwise/server requested | Explain that this main test release does not support that feature |
| Skill failure | Suggest retry or degradation |
| Low confidence | Actively clarify intent |
| Directory exists | Ask before overwriting |

## 5. Interaction

### 5.1 Task confirmation

After task recognition, MUST confirm with user. Display templates are defined in parameter-builder's "MSR / KMC parameter display format" section.

### 5.2 Clarification triggers

- Vague temperature: "high temperature" → ask for specific value
- Unknown gas ratio: CO oxidation needs CO+O₂ → ask for partial pressures
- Unclear unit: "pressure" → ask Pa / kPa / atm
- Unspecified metal/gas: list available options for the current task

## 6. Dependencies

- **chatmosp-parameter-builder** — parameter completion + gas entropy calculation
- **chatmosp-file-organizer** — directory structure creation
- **chatmosp-msr-generator** — MSR calculation
- **chatmosp-kmc-simulator** — KMC simulation
- **chatmosp-literature-search** — literature search (when parameters missing)

## 7. File structure

```
chatmosp-input-coordinator/
├── SKILL.md       # Chinese reference
└── SKILL_cn.md    # This file (English)
```
## ChatMOSP Companion Skills

This skill is part of the ChatMOSP skill set. For complete functionality, install the companion ChatMOSP skills from ClawHub when they are missing:

- chatmosp-input-coordinator
- chatmosp-parameter-builder
- chatmosp-msr-generator
- chatmosp-kmc-simulator
- chatmosp-literature-search
- chatmosp-file-organizer

If a required companion skill is unavailable, ask the user to install the missing ChatMOSP skill from ClawHub before continuing. Use the GitHub repository only as a fallback.
