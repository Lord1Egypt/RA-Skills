# ecovacs-deebot-control

**Default: English** · [中文](README.zh.md)

## Overview

This repository is an **Agent Skill** for Ecovacs **Deebot** (robot vacuum) control. It frames what an AI assistant can help you do—**see your robots**, **check battery and status**, **run or pause cleaning**, **send the unit to charge**, and **make sense of failures**—using an Open Platform **Access Key (AK)** in line with Ecovacs integration rules.

The skill complements official material: it scopes **what belongs in conversation** for agents and operators, not a full replacement for vendor protocol documents.

---

## Prerequisites

| Item | Requirement |
|------|----------------|
| **Open Platform AK** | Create or view it under *Service overview* on the Ecovacs Open Platform (**China**: [open.ecovacs.cn](https://open.ecovacs.cn/), **Global**: [open.ecovacs.com](https://open.ecovacs.com/)). Use the **same regional** portal as your account and robots. |
| **Device identification** | Use a **short phrase from the name shown in the app** so the assistant can point at **one** robot when you have several. |

---

## Interaction model

You say **which robot** (by how you name it in the app) and **what you want**—cleaning, pause, battery, dock, and so on. For day-to-day use you do **not** need internal command names. Integrators and deeper behavior are covered in [SKILL.md](SKILL.md) and [references/api.md](references/api.md).

### Sample user prompts

Illustrative phrasing only—swap in the nicknames you see in the app.

> “Which **Deebots** are on my account?”  
>
> “The one whose nickname has **Kitchen**—how’s the **battery**?”  
>
> “Start a **whole-home clean** on **客厅宝**.” / “**Pause** the living-room unit.”  
>
> “Send **客厅宝** **back to the dock**.”

---

## Capability coverage

What actually works depends on **model, firmware, and whether the robot is online**. The table is a plain-language map of **areas** this skill is meant to support—not a guarantee for every device.

| Area | What it covers |
|------|----------------|
| **Discovery** | See which Deebots are on the account; use the same names you see in the app when you talk to the assistant. |
| **Battery & status** | Remaining charge and high-level state (e.g. cleaning, charging, at dock). |
| **Cleaning** | Whole-home clean, room or zone cleaning where the product allows, plus pause, resume, and stop. |
| **Dock & recharge** | Start return to the charging dock, or stop an ongoing return trip. |
| **Run statistics** | Things like area cleaned and duration for the current or last run, when the model exposes them. |
| **More (model-dependent)** | Suction, water level, sweep/mop mode, dock maintenance (empty / wash / dry), consumables, schedules—only where the hardware and firmware support them. |

---

## Troubleshooting

| Symptom | Likely cause | Suggested action |
|---------|----------------|------------------|
| AK / token / permission errors | Wrong, expired, or region-mismatched AK | Regenerate AK on the Open Platform; align region and configuration |
| Device not found | Name phrase does not match any listed robot, or the unit is missing from the list | Refresh the list in the app or via the assistant; match the wording you use to the app display |
| Offline / timeout | Robot off, off-network, or unstable link | Check power, Wi‑Fi, and that the unit shows online in the app |
| Low battery / “cannot run task” | Not enough charge for the requested action | Let it charge, then try again |

**Escalation:** Keep the **full** message the assistant or gateway returns, then follow [SKILL.md](SKILL.md) and [references/api.md](references/api.md).

---

## Contact

[pei.zhou@ecovacs.com](mailto:pei.zhou@ecovacs.com)
