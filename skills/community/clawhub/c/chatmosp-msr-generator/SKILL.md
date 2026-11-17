---
name: chatmosp-msr-generator
description: |
  MSR (Multiscale Structure Reconstruction) calculation engine of the chatMOSP system.
  Invokes mosp-for-chatMOSP/utils/msr.py to generate metal cluster structures
  (Wulff construction), producing ini.xyz and {task_name}_cluster.xyz, then
  automatically generates PNG structure images and GIF rotation animations,
  and finally sends them to the user via Feishu.
  Triggers: after parameter-builder has built parameters and the user has confirmed
  via the 5-option prompt, this skill executes the MSR calculation.
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-msr-generator

## 1. Core Responsibilities

1. Execute metal cluster structure generation (Wulff construction)
2. Validate input parameter completeness
3. Warn on large clusters (R ≥ 50Å)
4. Generate structure files + visualization images
5. Send results to user via Feishu

## 2. Prerequisites

- ✅ parameter-builder has built the parameters
- ✅ User has confirmed via the 5-option prompt (see parameter-builder)
- ✅ `input.json` exists at `OUTPUT/{task_name}/input.json`
- ✅ Target directory has been created by file-organizer
- ✅ External `mosp-for-chatMOSP` installed, with `utils/msr.py` and `utils/paint.py`
- ❌ DO NOT bypass parameter-builder and build parameters manually
- ❌ DO NOT skip user confirmation and execute calculation directly

## 3. Input Contract (Required fields in input.json)

| Field | Description |
|-------|-------------|
| Element | Metal element (Pd, Pt, Au, etc.) |
| Temperature / Pressure | Temperature / Pressure |
| Gas1_name / Gas1_pp / Gas1_S | Gas 1 name / partial pressure / gas entropy |
| Gas2_name / Gas2_pp / Gas2_S | Gas 2 name / partial pressure / gas entropy |
| Radius | Cluster radius (Å) |
| nFaces / Face1 / Face2 / Face3 | Surface facet parameters |

Gas entropy (`Gas1_S` / `Gas2_S`) is calculated by parameter-builder using the formula in §7.1. **DO NOT manually fill or reuse values from example files.**

## 4. Large-Cluster Warning

MUST check cluster radius before execution. Warn user when R ≥ 50Å:

```
⚠️ Calculation Time Warning:
Current cluster radius is {R}Å, estimated calculation time is approximately
{estimated_minutes} minutes.
(R=50Å ~20 min, R=65Å ~40 min)
Continue with MSR calculation?
```

| Radius | Atoms (approx) | Time (approx) |
|--------|----------------|---------------|
| 50 Å | 11,000 | 20 min |
| 65 Å | 35,000 | 40 min |
| Larger | Cubic growth | Significantly longer |

## 5. Execution Steps

### Step 1: Run MSR calculation

```bash
cd mosp-for-chatMOSP
python3 utils/msr.py --json OUTPUT/{task_name}/input.json --output OUTPUT/{task_name}/
cd -
```

### Step 2: Validate output

```bash
ls -lh OUTPUT/{task_name}/ini.xyz
ls -lh OUTPUT/{task_name}/{task_name}_cluster.xyz
```

- ✅ `ini.xyz` MUST exist and be > 0KB, otherwise MSR failed
- ✅ `{task_name}_cluster.xyz` MUST exist (for visualization)

### Step 3: Generate visualization (two separate steps)

```bash
# Static structure image
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

# Rotation animation
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

> `paint.py` can only generate ONE type per call (PNG OR GIF); two separate steps are required. For atom counts > 20,000, recommend generating only the static image.

### Step 4: Send to user via Feishu

```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "{workspace}/mosp-for-chatMOSP/OUTPUT/{task_name}/structure.png",
  "caption": "{Metal}-{T}K-{P}Pa-CO{pp1}%-O2{pp2}%-R{R}Å"
}
```

Requirements:

1. Send `structure.png` to user
2. Send `rotation.gif` to user
3. Briefly describe structural features (e.g., "Pd nanoparticle shows truncated octahedron, mainly exposing (111) facets")

## 6. Output Files

| File | Description |
|------|-------------|
| ini.xyz | Real cluster structure (all atoms), input for KMC |
| {task_name}_cluster.xyz | Surface-atom-classified structure for plotting |
| faceinfo.txt | Facet information statistics |
| input.json | MSR parameter file |
| structure.png | Static structure image |
| rotation.gif | Rotation animation |

## 7. Key Principles

- MSR `input.json` MUST NOT contain KMC parameters — KMC parameters are prepared independently by kmc-simulator
- `ini.xyz` is the **OUTPUT** of MSR, NOT the input — do not prepare `ini.xyz` for MSR tasks
- DO NOT directly copy example files from `MOSP_database` — use parameter-builder to recalculate gas entropy

## 8. Error Handling

| Error | Action |
|-------|--------|
| ini.xyz missing or 0KB | MSR failed; suggest adjusting parameters and retrying |
| {task_name}_cluster.xyz missing | Check MSR log; may be convergence failure |
| MSR timeout | Reduce cluster radius or check parameter validity |
| User cancellation | Terminate, preserve generated files |

## 9. Cross-Skill Handoff

- **MSR → KMC**: After MSR completes, `ini.xyz` is produced. KMC tasks independently fetch complete KMC parameters from `MOSP_database` via kmc-simulator. Do NOT reuse this skill's `input.json`. See kmc-simulator.
- **MSR failure → parameter-builder**: Parameter issues go back to parameter-builder for adjustment.
- **Re-running MSR**: If directory already exists, ask user before overwriting.

## 10. Dependencies

- **mosp-for-chatMOSP** — MSR calculation engine (cloned)
- **chatmosp-parameter-builder** — parameter building and gas entropy calculation
- **chatmosp-file-organizer** — directory structure
- **chatmosp-input-coordinator** — task entry point

## 11. File Structure

```
chatmosp-msr-generator/
├── SKILL.md       # Chinese reference
└── SKILL_cn.md    # This file (English)
```

## 12. Example

```
User: Calculate Pt nanoparticle cluster structure at 500K

System: [Recognize as MSR task → parameter-builder searches params →
        Show 5-option confirmation → User confirms → R=20Å, no warning →
        Invoke msr.py → Validate output → Generate PNG+GIF → Send via Feishu]
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
