# ecovacs-skills-pet-control

**Default: English** · [中文](README.zh.md)

## Overview

Agent Skill for Ecovacs **FAMIBOT** (pet robot). It tells an assistant what it may help with—**read state**, **change everyday settings**, and **run motions or built-in sounds**—via an Open Platform **Access Key (AK)**.

This repo scopes **conversation-safe capabilities** for agents; full platform docs remain on the Ecovacs Open Platform site.

---

## Prerequisites

| Item | Requirement |
|------|----------------|
| **Open Platform AK** | From *Service overview* on [open.ecovacs.cn](https://open.ecovacs.cn/) (Mainland China) or [open.ecovacs.com](https://open.ecovacs.com/) (non-China regions). **Do not** use account passwords in the skill session. |
| **Device nickname** | A **substring of the name shown in the app** so one FAMIBOT is selected when several are bound to the AK. |

---

## How to use (users)

Say **which pet** (app nickname) and **what you want**. You do not need command names.

### Example prompts

> “How is **Rocky** doing—mood and overall state?”  
> “What’s **Rocky**’s volume and is the mic on?”  
> “Set **Rocky**’s idle timeout to **three minutes** after wake with no interaction.”  
> “Have **Rocky** nod once / wag tail / look happy.”  
> “Have **Rocky** **bark happily**.”  
> “Have **Rocky** **bark loudly** (happy).”  
> “Have **Rocky** **dance**.” (default: `showcase_custom`)  
> “Do the **showcase dance**.”  
> “Every **minute**, bark **ten times** on **Rocky**.” (device-side schedule, one request)  
> “Put **Rocky** to **sleep**.” / “**Stop** the scheduled routine on **Rocky**.”

Integrators: [SKILL.md](SKILL.md) · [references/api.md](references/api.md) · `scripts/ecovacs.py`

---

## Supported capabilities

Availability depends on **model, firmware, deployment, and online status**.

### Read (queries)

| Topic | Examples of what you can ask |
|-------|--------------------------------|
| **State & persona** | Overall pet state, current emotion, persona/role list, gender, initialization status |
| **Device I/O** | Microphone on/off, camera on/off, volume, eye brightness, UI language, wake idle timeout |
| **Context** | Location/weather-style info (when exposed), latest diary entry |

### Write (settings)

| Topic | Notes |
|-------|--------|
| **Mic / camera / volume** | Toggle or adjust levels |
| **Wake idle timeout** | How long the pet stays awake with no interaction |
| **Wake word / nickname** | High impact—change only when the user clearly asks |
| **Gender** | Pet gender setting |

Persona **cannot be changed through the skill**; use queries above to read mood/persona.

### Motion, sleep & sound (control)

| Topic | Notes |
|-------|--------|
| **Single motions** | Nod, shake, turn head, wag tail, emotion poses |
| **Built-in sounds** | Default: **`category`** (e.g. `happy`, gateway picks randomly). When the user specifies intensity (loud/soft), set **`file`** (e.g. `happy-h-1`…`happy-h-5`) — [phoenix-single-action.md §2.2](references/phoenix-single-action.md) |
| **Combined shows** | Single preset `showcase_custom` (~45s script) — [dance-routines.md](references/dance-routines.md) |
| **Sleep** | Enter sleep mode |
| **Stop / cancel** | Stop motion and clear **device-queued** scheduled routines (`reset`) |

Before visible motions, the helper script **wakes the pet if needed** (camera on + standard work mode) so “success but no movement” is less common.

Action timing defaults: single step ≤ ~10s; hand-built sequences ≤ ~20s; preset dance `showcase_custom` ~45s (see [SKILL.md](SKILL.md)).

---

## Repository layout

| Path | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Agent entry: AK flow, command list, script examples |
| [scripts/ecovacs.py](scripts/ecovacs.py) | Gateway client (devices, cmd, display, auto-wake) |
| [scripts/dance_choreography.py](scripts/dance_choreography.py) | `showcase_custom` choreography (used by `ecovacs.py`) |
| [references/](references/) | API, schema, motion protocols, **dance preset**, troubleshooting |

---

## Troubleshooting

| Symptom | Suggested action |
|---------|------------------|
| Missing AK / auth errors | Refresh AK; match Open Platform region to the account |
| Device not found | Align phrasing with the app name; retry when online |
| “Not enabled” / blocked | Request is outside this skill’s supported set—see [SKILL.md](SKILL.md) or ask your operator |
| Motion OK but no movement | Pet may still be asleep; script auto-wake may have failed—wake in the app and retry |
| Sound did not play | Try `category` when intensity is vague; verify `file` against §2.2 when intensity is explicit; keep the full error text |

Details: [references/troubleshooting.md](references/troubleshooting.md)

---

## Contact

[pei.zhou@ecovacs.com](mailto:pei.zhou@ecovacs.com)
