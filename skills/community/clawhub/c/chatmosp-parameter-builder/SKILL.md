---
name: chatmosp-parameter-builder
description: |
  Parameter building and management center of the chatMOSP system. Handles MSR / KMC
  parameter queries, intelligent completion, gas entropy calculation, MSR↔KMC interaction
  parameter conversion, and missing-parameter handling.
  Triggers: after input-coordinator identifies a task but before the calculation engine
  executes, parameters need to be built or adjusted; or the user queries/modifies the
  current task's parameters.
---

> **Language routing / 语言路由**
> Detect the user's language from the latest message.
> - If the user writes in English, continue with this English file and respond in English.
> - If the user writes in Chinese, read `SKILL.md` in this same directory and respond in Chinese.
> Always match the response language to the user's input language.

# chatmosp-parameter-builder

## 1. Core Responsibilities

1. Intelligent parameter completion — search MOSP_database → replace temperature → calculate gas entropy
2. MSR / KMC parameter separation — two parameter sets are fully independent
3. 5-option confirmation flow — must show user and wait for confirmation
4. Gas entropy calculation — auto-calculate for 8 gases based on temperature
5. Interaction parameter conversion — MSR full-adsorption ↔ KMC per-atom (literature defaults to KMC)
6. Missing parameter handling — call literature-search for key parameters
7. Temperature replacement — recalculate entropy when user changes temperature
8. Parameter validation — format, range, consistency, completeness checks

## 2. ⚠️ Mandatory: Parameter Confirmation

No matter how clear the user's request is, parameters MUST be displayed and confirmed after building.

### 2.1 The 5 Options

1. ✅ Confirm — use these parameters
2. ✏️ Modify — adjust specific parameters (Temperature / Pressure / partial pressure / cluster size / gas species)
3. 📊 Compare — run multiple conditions for comparison (multi-Temperature / multi-Pressure / multi-size / multi-gas-ratio)
4. 🔄 Switch calculation mode — switch between MSR and KMC
5. ❌ Cancel task, change system — change metal or gas system

Only after user selects option 1 can the calculation proceed.

## 3. MSR / KMC Parameter Separation

| Task | Source | MUST NOT include |
|------|--------|------------------|
| MSR | MSR section + Gas + Adsorption from MOSP_database | KMC fields |
| KMC | KMC section (with nspecies, s1/s2, p1, e1-e7, li full set) | MSR fields |

> ⚠️ **CRITICAL**: MSR's input.json and KMC's input.json are TWO INDEPENDENT files. Do NOT reuse one for the other.

## 4. MSR Parameter Display Template

MUST use the following format exactly, do NOT create your own format:

```
📊 MSR Parameters ready, please confirm:

【Basic Information】
- Metal: {metal}
- Temperature: {T} K ({T-273}°C)
- Pressure: {P} Pa
- Cluster radius: {R} Å
- Crystal structure: {structure}

【Gas Environment】
- {Gas1} partial pressure: {pp1}%
- {Gas2} partial pressure: {pp2}%

【Gas Entropy Values】 (Auto-calculated)
- {Gas1} entropy: {S1} eV/K (calculated at {T}K)
- {Gas2} entropy: {S2} eV/K (calculated at {T}K)

【Surface Facet Parameters】
- {facet1} facet: surface energy {γ1} eV/Å²
- {facet2} facet: surface energy {γ2} eV/Å²
- {facet3} facet: surface energy {γ3} eV/Å² (most stable)

【Surface Adsorption Parameters】 (read from Adsorption field in input.json)
{facet1} facet:
  - {Gas1} E_ads = {E1} eV
  - {Gas2} E_ads = {E2} eV
{facet2} facet:
  - {Gas1} E_ads = {E3} eV
  - {Gas2} E_ads = {E4} eV
{facet3} facet:
  - {Gas1} E_ads = {E5} eV
  - {Gas2} E_ads = {E6} eV

【Interaction Matrix】 (read from input.json)
{facet1} facet: CO-CO={w1}, CO-O={w2}, O-O={w3}
{facet2} facet: CO-CO={w4}, CO-O={w5}, O-O={w6}
{facet3} facet: CO-CO={w7}, CO-O={w8}, O-O={w9}

【Output Settings】
- Task directory: {task_name}
- Generated files: input.json, ini.xyz, {task_name}_cluster.xyz, faceinfo.txt,
  structure.png, rotation.gif

Please select:
1. ✅ Confirm - Proceed with MSR calculation
2. ✏️ Modify - Adjust specific parameters (Temperature / Pressure / partial pressure / cluster size / gas species)
3. 📊 Compare - Run multiple conditions (multi-Temperature / multi-Pressure / multi-size / multi-gas-ratio)
4. 🔄 Switch to KMC
5. ❌ Cancel and change system
```

> ⚠️ **Unit note**: Gas1_pp / Gas2_pp are PERCENTAGES (%), NOT pressure values. MUST display with % sign.

## 5. KMC Parameter Display Template

```
📊 KMC Parameters ready, please confirm:

【Basic Information】
- Task type: KMC (Kinetic Monte Carlo simulation)
- Reaction: {reaction}
- Temperature: {T} K ({T-273}°C)
- Pressure: {P} Pa
- Gas partial pressure: {Gas1} {pp1}%, {Gas2} {pp2}%

【Cluster Information】 (from MSR results)
- Metal: {metal}
- Cluster radius: {R} Å
- Number of atoms: {N}
- Crystal structure: {structure}
- MSR task directory: {msr_task_name}

【Simulation Parameters】
- Simulation steps: {steps}
- Recording interval: every {record_int} steps
- Number of species: {nspecies}
- Number of reaction events: {nevents}

【Species Definitions】
- s1: {name1} ({role1})
- s2: {name2} ({role2})
- ...

【Product Definitions】
- p1: {product_name} (generated by events X, Y)

【Reaction Mechanism】 (brief)
- {mechanism_brief}

【Output Settings】
- KMC task directory: {msr_task_name}/KMC_{steps}steps/
- Generated files: input.json, coverage.png, coverage_steps.png, tof.png, tof_time.png, ...

Please select:
1. ✅ Confirm - Proceed with KMC simulation
2. ✏️ Modify - Adjust specific parameters (steps / Temperature / Pressure / partial pressure / recording interval)
3. 📊 Compare - Run multiple conditions (multi-steps / multi-Temperature / multi-Pressure / multi-gas-ratio)
4. 🔄 Switch to MSR
5. ❌ Cancel and change system

Suggestions:
- For quick testing, start with 100,000 steps
- 5M steps yields better statistics but takes longer
```

## 6. Intelligent Parameter Completion

```
User input
  → Extract parameters (metal, T, gas, P, steps, R, partial pressures)
  → Search MOSP_database (metal + gas match)
  → Load matching example file
  → Replace user-specified parameters
  → Calculate gas entropy (at user's T)
  → Check parameter completeness
  → Display to user for confirmation (5 options)
```

### 6.1 Search matching

- **Metal matching**: exact (Pd, Pt, Au, Cu, Ni, ...)
- **Gas matching**: gas species set match (CO+O₂ → CO oxidation environment)
- **Best match**: highest metal+gas match score
- **Default source**: `mosp-for-chatMOSP/MOSP_database/`

### 6.2 Priority

1. User-specified > MOSP_database defaults > System defaults
2. User unspecified → example defaults
3. No example → system presets (P=101325Pa, R=20Å, steps=1000000)

## 7. Gas Entropy Calculation

### 7.1 Formula

```
S(J/K/mol) = a × T^b
S(eV/K)   = (a × T^b) / 96485
```

- `a, b` are gas-specific (see table)
- `T` is temperature (K)
- `96485` is J→eV conversion factor

### 7.2 Parameters for 8 gases

| Gas | a | b |
|-----|------|------|
| H₂ | 41.362 | 0.201 |
| N₂ | 82.394 | 0.148 |
| O₂ | 90.454 | 0.143 |
| CO₂ | 76.458 | 0.181 |
| CO | 85.142 | 0.147 |
| NO | 93.121 | 0.143 |
| H₂O | 64.234 | 0.18665 |
| NO₂ | 93.02 | 0.1668 |

Parameters fit over 0~6000K, no temperature-range limitation.

### 7.3 Example

CO at 473K:

```
S(J/K/mol) = 85.142 × 473^0.147 ≈ 210.5 J/K/mol
S(eV/K)   = 210.5 / 96485 ≈ 0.00218 eV/K
```

### 7.4 Field mapping

| Task | Gas entropy field |
|------|-------------------|
| MSR | `Gas1_S` / `Gas2_S` |
| KMC | `s1.S_gas` / `s2.S_gas` |

> ⚠️ **CRITICAL**: MSR and KMC gas entropy MUST use same formula, same values.

### 7.5 Recalculate on temperature change

When user selects "Modify" and changes temperature, MUST recalculate all gas entropies using §7.1 formula and update fields.

Example: T change from 500K to 800K

- CO: S(500K) ≈ 0.002200 eV/K → S(800K) ≈ 0.002357 eV/K ✅
- O₂: S(500K) ≈ 0.002285 eV/K → S(800K) ≈ 0.002446 eV/K ✅

## 8. Temperature Replacement

example temperature T_example → user temperature T_user:

1. Update Temperature = T_user
2. Recalculate gas entropy per §7
3. Keep other parameters (gamma, E_ads, w matrix are T-independent)

## 9. Interaction Parameter Conversion (MSR ↔ KMC)

> ⚠️ **IMPORTANT DEFAULT**: All interaction parameters returned by literature search are treated as KMC format by default (interaction per adjacent atom). If used as MSR task parameters, automatically convert to MSR format, but MUST remind the user to check the literature to confirm it is truly per-adjacent-atom interaction.

> **Trigger condition**: Only triggered for literature-retrieved parameters. MOSP_database built-in parameters are not processed (assumed correct).

### 9.1 Format definitions

| Format | Meaning | Typical range |
|--------|---------|---------------|
| MSR | Total interaction at full adsorption | > 0.5 eV (absolute) |
| KMC | Interaction per adjacent atom | < 0.3 eV (absolute) |

### 9.2 Default processing flow (literature parameters)

1. Literature search returns parameters → default assumption: KMC format
2. Auto-convert to MSR format (if needed for MSR task)
3. Show user both original and converted values + conversion formula
4. Remind user to check literature:

```
⚠️ Interaction parameters have been auto-converted from KMC format to MSR format.
Please check the original literature to confirm it is per-adjacent-atom
interaction (not full-adsorption total interaction).

Conversion formula: MSR parameter = KMC parameter × coordination number
- (100) facet: × 4
- (110) facet: × 2
- (111) facet: × 6
```

### 9.3 Conversion formula

**MSR parameter = KMC parameter × coordination number**

| Facet | Coordination |
|-------|--------------|
| (100) | 4 |
| (110) | 2 |
| (111) | 6 |

### 9.4 Conversion example (KMC → MSR, automatic)

| Facet | Original KMC | Converted MSR |
|-------|--------------|---------------|
| (100) | -0.149 | -0.596 (×4) |
| (110) | -0.159 | -0.318 (×2) |
| (111) | -0.168 | -1.008 (×6) |

### 9.5 Conversion timing

- **MSR task + literature parameters (default KMC)** → auto-convert to MSR + remind user
- **KMC task + literature parameters (default KMC)** → no conversion
- **MOSP_database built-in parameters** → no processing

## 10. Parameter Completeness Handling

After finding an example, MUST check completeness:

### 10.1 Key parameters missing (E_ads, w, gamma, etc.)

**Step 1**: Inform user "{metal}.json lacks key data (adsorption energy, interaction matrix)"

**Step 2**: Provide 4 options:

1. Literature search (open access: Nature Communications, Science Advances, PNAS, ACS Central Science, Chemical Science)
2. Literature search (paid: Science, Nature, JACS, Angewandte Chemie)
3. User specifies parameters directly
4. Cancel task, change system

**Step 3**: Option 1/2 → call literature-search; Option 3 → wait for user input; Option 4 → end task

### 10.2 Secondary parameters missing (Gas1_S, Gas2_S, etc.)

- Auto-calculate (per §7.1 formula)
- Inform user: "Some parameters use defaults or auto-calculation"

### 10.3 Gas entropy MUST be recalculated after literature search

Literature-retrieved parameters do NOT include gas entropy. Regardless of completeness score, MUST recalculate per §7.1 before assembling input.json.

## 11. KMC input.json Required Fields

### 11.1 Top-level

| Field | Type | Example |
|-------|------|---------|
| Element | string | `"Pt"` |
| Lattice constant | string | `"3.9239"` |
| Crystal structure | string | `"FCC"` |
| Temperature | string | `"850"` |
| Pressure | string | `"150"` |
| flag_MSR | boolean | false |
| flag_KMC | boolean | true |
| KMC | object | `{...}` |

### 11.2 KMC object

| Field | Type | Description |
|-------|------|-------------|
| nLoop | string | Total simulation steps |
| record_int | string | Recording interval |
| nspecies | number | Number of species |
| nproducts | number | Number of products |
| nevents | number | Number of reaction events |
| nevents_mob | number | Number of mobility events |
| s1 / s2 | string | Species 1/2 definition (JSON string) |
| p1 | string | Product 1 definition (JSON string) |
| e1 ~ e7 | string | Reaction events 1~7 (JSON string) |
| li | array | Lattice interaction matrix |

## 12. Parameter Units Quick Reference

### MSR parameters

| Field | Unit | Description |
|-------|------|-------------|
| Element | unitless | Pd, Pt, Au |
| Lattice constant | Å | Lattice constant |
| Pressure | Pa | System pressure |
| Temperature | K | Temperature |
| Radius | Å | Cluster radius |
| Gas_pp | % | Partial pressure % |
| Gas_S | eV/K | Gas entropy |
| Face.gamma | eV/Å² | Surface energy |
| Face.E_ads | eV | Adsorption energy |
| Face.S_ads | eV/K | Adsorption entropy |
| Face.w | eV | Interaction matrix element |

### KMC parameters

| Field | Unit | Description |
|-------|------|-------------|
| nLoop | steps | Simulation steps |
| record_int | steps | Recording interval |
| mass | amu | Molecular mass |
| PP_ratio | % | Partial pressure ratio |
| S_ads | eV/K | Adsorption entropy |
| S_gas | eV/K | Gas entropy |
| Ea_diff | eV | Diffusion activation energy |
| sticking | 0-1 | Sticking coefficient |
| E_ads_para | eV | Adsorption energy parameter |
| BEP_para | eV | BEP relationship parameter |
| li | eV | Lattice interaction matrix |

## 13. Error Handling

| Situation | Action |
|-----------|--------|
| No matching example | Call literature-search |
| Key parameters missing | Show user 4 options (see §10.1) |
| Temperature unspecified | Default 500K, but confirm with user |
| Pressure unspecified | Default 101325 Pa |
| Cluster size unspecified | Default 20 Å (MSR) or 50 Å (KMC) |
| Steps unspecified | Default 1000000 |
| Gas / partial pressure mismatch | Prompt user to check |

## 14. Cross-Skill Handoff

- **input-coordinator → this skill**: task recognized, route to here
- **this skill → literature-search**: when parameters missing (see literature-search)
- **this skill → msr-generator**: deliver MSR params after user confirmation
- **this skill → kmc-simulator**: deliver KMC params after user confirmation
- **MSR ↔ KMC handoff**: after MSR, KMC independently fetches from MOSP_database, does NOT reuse MSR's input.json

## 15. Dependencies

- **chatmosp-input-coordinator** — task entry
- **chatmosp-literature-search** — when parameters missing
- **chatmosp-file-organizer** — get MOSP_database path
- **chatmosp-msr-generator** — MSR calculation receiver
- **chatmosp-kmc-simulator** — KMC simulation receiver

## 16. File Structure

```
chatmosp-parameter-builder/
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
