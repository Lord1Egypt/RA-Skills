---
name: chatmosp-kmc-simulator
description: |
  KMC (Kinetic Monte Carlo) simulation engine of the chatMOSP system. Invokes
  kmc_standalone.py via Wine to run the Windows main.exe engine, executes
  catalyst surface reaction kinetic simulations, and produces TOF / coverage
  results. Uses utils/plot_kmc_data.py to generate coverage.png, coverage_steps.png,
  tof.png, and tof_time.png (4 images total).
  Triggers: after parameter-builder has built KMC parameters and the user has
  confirmed via the 5-option prompt, this skill executes the KMC simulation.
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-kmc-simulator

## 1. Core Responsibilities

1. Check and manage Wine environment (KMC engine dependency)
2. Prepare KMC input files (copy template from MOSP_database + user-specified steps/T/pp)
3. Execute KMC simulation and monitor progress
4. Warn on large step counts (≥ 20M steps)
5. Generate TOF / coverage plots and CSV data
6. Auto-regenerate plots if missing or on user request

## 2. Prerequisites

- ✅ MSR task completed (if starting from MSR cluster)
- ✅ parameter-builder has built KMC parameters
- ✅ User has confirmed via the 5-option prompt (see parameter-builder)
- ✅ Wine environment installed (check on first run, prompt install if missing)
- ✅ MSR-generated `ini.xyz` copied to KMC task directory (if applicable)
- ✅ External `mosp-for-chatMOSP` installed, with `kmc_standalone.py`, `MOSP_database/`, and `engine/main.exe`
- ❌ DO NOT bypass parameter-builder and build KMC parameters manually
- ❌ DO NOT reuse MSR's `input.json` — KMC must independently prepare complete parameters

## 3. Wine Environment

The KMC engine is the Windows `main.exe`, requiring Wine to run.

### 3.1 Check Wine

```bash
which wine64 || which wine
```

### 3.2 Install Wine (Ubuntu/Debian)

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine64 wine32
```

### 3.3 Automatic environment check

- ✅ Wine installed → proceed normally
- ⚠️ Wine missing → prompt install instructions
- ❌ Version incompatible → prompt upgrade

## 4. Step-Count Warning

When KMC steps ≥ 20M, MUST warn user before execution:

```
⚠️ Calculation Time Warning:
Current KMC steps: {N}, estimated time: ~{estimated_hours} hours.
(Reference: 20M steps ≈ 12 hours, 40M steps ≈ 24+ hours)
Continue with KMC simulation?
```

| Steps | Estimated time |
|-------|----------------|
| 20M | ~12 hours |
| 40M | ~24 hours or longer |
| More | Linear growth |

> Note: Running multiple conditions (e.g., multiple temperatures) requires separate calculations; total time multiplies.

## 5. Input Contract (Required fields in input.json)

### Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| Element | string | Metal element (Pd, Pt, Au, etc.) |
| Lattice constant | string | Lattice constant (Å) |
| Crystal structure | string | Crystal structure (FCC, BCC, HCP) |
| Temperature | string | Temperature (K) |
| Pressure | string | Pressure (Pa) |
| flag_MSR | boolean | MUST be `false` |
| flag_KMC | boolean | MUST be `true` |
| KMC | object | KMC parameter object |

### KMC object required fields

| Field | Type | Description |
|-------|------|-------------|
| nLoop | string | Simulation steps |
| record_int | string | Recording interval |
| nspecies | number | Number of species |
| nproducts | number | Number of products |
| nevents | number | Number of reaction events |
| nevents_mob | number | Number of mobility events |
| s1 / s2 | string | Species 1/2 definitions (JSON string) |
| p1 | string | Product 1 definition (JSON string) |
| e1 ~ e7 | string | Reaction events 1~7 (JSON string) |
| li | array | Lattice interaction matrix |

> ⚠️ **CRITICAL**: Gas entropy `s1.S_gas` / `s2.S_gas` MUST match MSR's `Gas1_S` / `Gas2_S` (use the same calculation formula).

## 6. Directory Structure

KMC task directory must be under MSR directory:

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── KMC_{steps}steps/             ← KMC task directory
    ├── input.json                ← outside INPUT/
    ├── ini.xyz                   ← copied from MSR
    ├── coverage.png              ← generated after run
    ├── coverage_steps.png        ← generated after run
    ├── tof.png                   ← generated after run
    ├── tof_time.png              ← generated after run
    ├── INPUT/                    ← should be empty before run
    └── OUTPUT/                   ← populated after run
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

> ⚠️ **IMPORTANT**:
> - `ini.xyz` and `input.json` MUST be outside `INPUT/` (`kmc_standalone.py` clears `INPUT/OUTPUT`)
> - Ensure `INPUT/` and `OUTPUT/` are empty before running

## 7. Execution Steps

### Step 1: Create KMC task directory

```bash
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_{steps}steps/INPUT
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_{steps}steps/OUTPUT
```

### Step 2: Copy structure file

```bash
cp OUTPUT/{msr_task_name}/ini.xyz OUTPUT/{msr_task_name}/KMC_{steps}steps/ini.xyz
```

### Step 3: Prepare input.json

```bash
# Copy template from MOSP_database (do not create manually)
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}.json \
   OUTPUT/{msr_task_name}/KMC_{steps}steps/input.json

# Adjust fields:
# - nLoop: user-specified steps
# - T: user-specified temperature
# - gas_pp: user-specified partial pressures
# - record_int: recording interval
# - s1.S_gas / s2.S_gas: recalculated using parameter-builder §7.1 formula
```

### Step 4: Show parameters for user confirmation

Use parameter-builder §KMC parameter display format (5 options).

### Step 5: Check Wine + step warning

- Check Wine environment
- Warn when steps ≥ 20M

### Step 6: Execute KMC

```bash
python3 {mosp_root}/kmc_standalone.py \
  --xyz OUTPUT/{task_dir}/ini.xyz \
  --json OUTPUT/{task_dir}/input.json \
  --out-dir {task_dir}
```

`{mosp_root}` is normally `$HOME/.openclaw/workspace/mosp-for-chatMOSP` or
`$OPENCLAW_WORKSPACE/mosp-for-chatMOSP`. Confirm that this directory exists
before running.

> Note: pass just the task directory name to `--out-dir` (e.g.
> `{msr_task_name}/KMC_{steps}steps`). The script automatically places it under
> `OUTPUT/`; even if an `OUTPUT/` prefix is accidentally included it is
> de-duplicated, so no `OUTPUT/OUTPUT/` nesting is produced.

## 8. Output Files

| File | Location | Description |
|------|----------|-------------|
| coverage.png | KMC task dir | Coverage vs Time |
| coverage_steps.png | KMC task dir | Coverage vs Steps |
| tof.png | KMC task dir | TOF vs Time |
| tof_time.png | KMC task dir | TOF vs Steps |
| coverage.csv | OUTPUT/ | Coverage data |
| tof.csv | OUTPUT/ | TOF data |
| site_tof.csv | OUTPUT/ | Site TOF data |
| rec_cov.data | OUTPUT/ | Coverage records (KMC engine raw output) |
| rec_event.data | OUTPUT/ | Event records |
| rec_site_spc.data | OUTPUT/ | Site-species records |

### 8.1 Sending Images to User (Feishu)

> ⚠️ **One image per call**: Feishu message tool only supports 1 image per attachment.
> Sending more than one will silently drop the extras. After KMC completes, you MUST
> send the 4 images one at a time with numbered labels.

Send order and labels:

1. Image 1/4: Coverage vs Time — `coverage.png`
2. Image 2/4: Coverage vs Steps — `coverage_steps.png`
3. Image 3/4: TOF vs Time — `tof.png`
4. Image 4/4: TOF vs Steps — `tof_time.png`

Example per message:
```
message(action=send, message="Image 1/4: Coverage vs Time",
         attachments=[{filePath:"...coverage.png", type:"image"}])
```

## 9. Output Check & Auto-Regenerate

After KMC completes (especially when user asks "is the task done?"), MUST check and regenerate plots if needed:

```bash
KMC_TASK_DIR="KMC task directory"
KMC_OUTPUT="$KMC_TASK_DIR/OUTPUT"

# 1. Check data files
if [ ! -f "$KMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$KMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$KMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ Data files missing, KMC may not have completed"
  exit 1
fi

# 2. Check step-count consistency
EXPECTED=$(grep -E "^[0-9]+\s+! Num of steps" "$KMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL=$(tail -n 1 "$KMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "❌ Expected $EXPECTED steps, got $ACTUAL, KMC did not complete"
  exit 1
fi

# 3. Check plots (4 images), regenerate if missing
if [ -f "$KMC_TASK_DIR/coverage.png" ] && \
   [ -f "$KMC_TASK_DIR/coverage_steps.png" ] && \
   [ -f "$KMC_TASK_DIR/tof.png" ] && \
   [ -f "$KMC_TASK_DIR/tof_time.png" ]; then
  echo "✅ Plots already exist"
else
  python3 ../../utils/plot_kmc_data.py "$KMC_OUTPUT"
  echo "✅ Plots regenerated"
fi
```

> Plotting script: `mosp-for-chatMOSP/utils/plot_kmc_data.py`

## 10. Error Handling

| Error | Action |
|-------|--------|
| Step-count mismatch | Check KMC log; may not have finished |
| Data files missing | KMC did not complete; check `run.log` |
| Lattice constant missing | Copy complete template from MOSP_database; do not create manually |
| INPUT/OUTPUT dir missing | Create them in Step 1 |
| ini.xyz missing | Copy from MSR task directory |
| Wine missing | Prompt install instructions |
| KMC segfault | Wine version incompatible; prompt upgrade |

## 11. Cross-Skill Handoff

- **MSR → KMC**: After MSR completes, `ini.xyz` is produced. This skill independently fetches complete KMC parameters from MOSP_database. Do NOT reuse MSR's `input.json`.
- **Parameter modification**: If user changes temperature, parameter-builder MUST recalculate gas entropy per §7.5.
- **Long-task query**: When user asks "is the task done?", run §9 check script, regenerate plots if needed.

## 12. Dependencies

- **mosp-for-chatMOSP** — KMC engine (cloned, includes main.exe)
- **chatmosp-parameter-builder** — parameter building and gas entropy
- **chatmosp-file-organizer** — directory creation
- **chatmosp-input-coordinator** — task entry point
- **Wine** — required for Windows main.exe

## 13. File Structure

```
chatmosp-kmc-simulator/
├── SKILL.md       # Chinese reference
└── SKILL_cn.md    # This file (English)
```

## 14. Example

```
User: Run KMC simulation for Pt CO oxidation at 850K, 150Pa, 20M steps

System: [Recognize as KMC → parameter-builder searches params →
        Show 5-option confirmation → User confirms → Check Wine installed →
        ⚠️ 20M steps ≈ 12 hours, warn user → User confirms again →
        Prepare input.json → Invoke kmc_standalone.py → Monitor progress →
        Check output → Generate 4 images → Send one-by-one → Display results]
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
