---
name: chatmosp-file-organizer
description: |
  File system manager of the chatMOSP system. Handles MSR / KMC task directory
  creation, intelligent naming (in `metal_gas-pp_T_K_P_Pa_R_size` format), and
  secure file operations (path-traversal protection, whitelist restriction).
  Triggers: after parameter-builder confirms parameters and before calculation
  engine runs, this skill creates the task directory; or when a KMC task needs
  to create a subdirectory under an existing MSR task.
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-file-organizer

## 1. Core Responsibilities

1. **Intelligent task naming** — generate task names per MSR / KMC format
2. **Standard directory creation** — MSR and KMC standard structures
3. **Path logic management** — direct KMC vs sequential KMC
4. **Secure file operations** — path-traversal protection + whitelist

## 2. Security-First Principles

- ✅ Path-traversal protection: auto-clean `../`, `//`, `~` and other dangerous chars
- ✅ Whitelist paths: all operations restricted to `mosp-for-chatMOSP/OUTPUT/`
- ✅ TaskNameValidator: validates task name legality, supports new naming format
- ✅ Permission check: ensure appropriate read/write permissions

**Forbidden patterns**: `..`, `//`, `~`, `/root`, `/etc`, `*.exe`, `*.sh`

**Allowed characters**: `a-zA-Z0-9_-.Å`

**Max path length**: 512

## 3. Task Naming Rules

### 3.1 MSR tasks

**Format**: `{metal}_{gas-pp}_{T}K_{P}Pa_R{size}`

**Example**: `Pd_CO9_O18_473K_101325Pa_R50`

| Field | Rule | Default |
|-------|------|---------|
| Metal | Element symbol (Pd, Pt, Au, ...) | required |
| Gas pp | Multi-gas joined with `_`, pp follows gas (CO9 = CO 9%) | required |
| Temperature | Number + K | 500 |
| Pressure | Number + Pa | 101325 |
| Size | R + number (Å) | 20 |

### 3.2 KMC tasks

**⚠️ IMPORTANT**: KMC task directory MUST be created as a subdirectory under the corresponding MSR task directory.

**Recommended format**: `KMC_{steps}steps` (concise; T/P already encoded in MSR dir name)

**Alternative format**: `KMC_{T}K_{P}Pa_{steps}steps`

**Examples**:
- Concise: `KMC_5000000steps`
- Verbose: `KMC_473K_101325Pa_5000000steps`

## 4. Directory Structures

### 4.1 MSR task directory

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
├── faceinfo.txt            # Facet information
├── ini.xyz                 # Real cluster (KMC input)
├── {task_name}_cluster.xyz # Structure for plotting
├── rotation.gif            # Rotation animation
├── structure.png           # Structure image
├── parameter_analysis.md   # Parameter analysis
├── paint.py                # Plotting script
├── input.json              # MSR parameter file
└── metadata.json           # Task metadata
```

### 4.2 KMC task directory (under MSR directory)

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── KMC_{steps}steps/
    ├── input.json          # KMC params (required)
    ├── ini.xyz             # Copied from MSR
    ├── coverage.csv        # Coverage data
    ├── coverage.png        # Coverage vs Time
    ├── coverage_steps.png  # Coverage vs Steps
    ├── run.log             # Run log
    ├── site_tof.csv        # Site TOF
    ├── tof.csv             # TOF data
    ├── tof.png             # TOF vs Time
    ├── tof_time.png        # TOF vs Steps
    ├── INPUT/              # KMC auto-fills
    │   ├── events.txt
    │   ├── input.txt
    │   ├── LI.txt
    │   ├── products.txt
    │   └── species.txt
    └── OUTPUT/             # KMC auto-output
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

## 5. Path Logic

### 5.1 MSR task path

- Location: `mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- MSR generates `ini.xyz` and `{task_name}_cluster.xyz`
- **DO NOT** prepare `ini.xyz` for MSR (MSR generates it)

### 5.2 KMC task path (two modes)

**Mode 1: Direct KMC** (no corresponding MSR, copy from MOSP_database)

- Location: `mosp-for-chatMOSP/OUTPUT/{kmc_task_name}/`
- Use when: no MSR result available

**Mode 2: Sequential KMC** (use MSR-generated ini.xyz, **recommended**)

- Location: `mosp-for-chatMOSP/OUTPUT/{msr_task_name}/{kmc_task_name}/`
- Use when: MSR result available

**Prefer Mode 2** for cluster consistency.

## 6. Visualization Commands (for MSR)

```bash
# Static structure image
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

# Rotation animation
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

See msr-generator §5.3 for details.

## 7. API Examples

### Create MSR directory

**Input**:

```json
{
  "action": "create_msr_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "radius": "50"
  }
}
```

**Output**:

```json
{
  "success": true,
  "task_type": "MSR",
  "task_name": "Pd_CO9_O18_473K_101325Pa_R50",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50",
  "standard_files": [
    "faceinfo.txt", "ini.xyz", "{task_name}_cluster.xyz",
    "rotation.gif", "structure.png", "parameter_analysis.md",
    "paint.py", "input.json", "metadata.json"
  ]
}
```

### Create KMC directory

**Input**:

```json
{
  "action": "create_kmc_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "steps": "200000000",
    "parent_msr_task": null
  }
}
```

**Output**:

```json
{
  "success": true,
  "task_type": "KMC",
  "task_name": "Pd_CO9_O18_473K_101325Pa_200000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_200000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["INPUT", "OUTPUT"],
  "output_files": ["coverage.csv", "coverage.png", "coverage_steps.png", "run.log", "site_tof.csv", "tof.csv", "tof.png", "tof_time.png"]
}
```

## 8. Error Handling

| Error | Action |
|-------|--------|
| Path traversal (`../`) | Reject operation, return error |
| Illegal characters in name | TaskNameValidator rejects |
| Directory exists | Ask before overwriting |
| Insufficient permissions | Prompt user to check |
| Path outside whitelist | Reject operation |

## 9. Cross-Skill Handoff

- **parameter-builder → this skill**: called after parameter confirmation
- **this skill → msr-generator**: after MSR directory creation
- **this skill → kmc-simulator**: after KMC directory creation
- **msr-generator → this skill**: for KMC subdirectory creation after MSR

## 10. Dependencies

- **chatmosp-parameter-builder** — get task parameters
- **chatmosp-input-coordinator** — get task type
- **chatmosp-msr-generator** — MSR calculation receiver
- **chatmosp-kmc-simulator** — KMC simulation receiver

## 11. File Structure

```
chatmosp-file-organizer/
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
