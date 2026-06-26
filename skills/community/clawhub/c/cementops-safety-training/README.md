# CementOps Safety Training Skill

**Part of the [CementOps Compliance Suite](https://cementops.ai) — Free on ClawHub**

MSHA Part 46 safety training program management for cement plant operations. Build compliant training programs, generate task training outlines, deliver toolbox talks, and prepare for MSHA inspections.

Built from real cement plant training programs that have survived MSHA audits.

## What It Does

| Capability | Description |
|-----------|-------------|
| **Part 46 Requirements** | Complete training hour requirements, training categories, record keeping, competent person definitions — all from 30 CFR Part 46 |
| **Task Training Templates** | 10 structured task training outlines with objectives, prerequisites, PPE, step-by-step procedures, hazards, and competency evaluation criteria |
| **Toolbox Talks** | 12 ready-to-use 5-minute safety talks with key points, discussion questions, and regulatory references |
| **Compliance Verification** | 5-step audit readiness checklist: records, training plan, task training, contractors, refresher content |
| **Program Setup Guide** | Step-by-step guide to building a Part 46 program from scratch — written plan through inspection readiness |

## What's Included

```
cementops-safety-training/
  SKILL.md                                    — Agent instructions (ClawHub manifest)
  README.md                                   — This file
  test-queries.json                           — 20-query evaluation suite
  knowledge-bases/
    msha-part46-requirements.json             — Complete Part 46 regulatory requirements
    training-topics.json                      — Training topics by plant area
  training-content/
    task-training-templates.json              — 10 task training outlines (LOTO, confined space, hot work, etc.)
    safety-talks.json                         — 12 toolbox talks in 5-minute format
  troubleshooting/
    training-compliance.json                  — Compliance verification troubleshooting
  guidance-templates/
    training-program-setup.md                 — Program build guide
  safety/
    training-safety.json                      — Training-specific hazard protocols
```

## Quick Start

Install from ClawHub:

```bash
npx clawhub@latest install cementops-safety-training
```

## Who This Is For

- **Plant safety managers** — build and maintain Part 46 programs, prepare for MSHA inspections
- **Training coordinators** — task training templates, toolbox talk content, record keeping guidance
- **Plant supervisors** — ready-to-deliver safety talks for pre-shift meetings
- **New safety professionals** — step-by-step program setup guide for plants starting from scratch

## Limitations

- **This is regulatory guidance, not legal advice.** Always consult qualified legal counsel for formal MSHA proceedings.
- **Training content is designed for cement manufacturing (SIC 3241)** under 30 CFR Part 56 (Surface Metal and Nonmetal Mines). Does not cover underground mining (Part 57) or coal mining (Parts 70-90).
- **Task training templates are starting points.** Customize to your plant's specific equipment, procedures, and hazards.

---

## CementOps AI Skill Catalog

This skill is part of the **CementOps Compliance Suite** — 3 free skills covering MSHA, safety training, and environmental compliance. CementOps AI builds 18 specialized AI skills covering every area of cement plant operations.

| # | Skill | Domain | Availability |
|---|---|---|---|
| 1 | **MSHA Compliance** | Regulatory/citation defense | Free on ClawHub |
| 2 | **Safety Training** | Part 46 training programs | Free on ClawHub |
| 3 | **Environmental Compliance** | EPA/NESHAP/CEMS/Title V | Free on ClawHub |
| 4 | Pyroprocessing | Kiln/preheater/cooler optimization | CementOps AI Platform |
| 5 | Raw Grinding | Raw mill operation and optimization | CementOps AI Platform |
| 6 | Finish Grinding | Cement mill operation and optimization | CementOps AI Platform |
| 7 | Quality Control | Chemistry, testing, and specifications | CementOps AI Platform |
| 8 | Coal Mill | Fuel preparation and explosion safety | CementOps AI Platform |
| 9 | Raw Materials Handling | Stockpile and feed systems | CementOps AI Platform |
| 10 | Quarry Operations | Drilling, blasting, crushing | CementOps AI Platform |
| 11 | Cement Storage & Shipping | Silos, packing, bulk loading | CementOps AI Platform |
| 12 | Maintenance Planning | PM/CM scheduling and execution | CementOps AI Platform |
| 13 | Spare Parts | Inventory and procurement | CementOps AI Platform |
| 14 | Plant Utilities | Compressed air, water, power | CementOps AI Platform |
| 15 | Reliability Engineering | RCA, FMEA, asset health | CementOps AI Platform |
| 16 | Process Optimization | Heat balance, throughput | CementOps AI Platform |
| 17 | Energy Optimization | SEC, energy audits, CCUS | CementOps AI Platform |
| 18 | Refractory | Lining design, installation, inspection | CementOps AI Platform |

Premium skills include deterministic parameter checking engines, equipment databases, failure mode libraries, and troubleshooting decision trees built from 18+ months of cement plant domain engineering.

---

## About CementOps AI

CementOps AI builds AI agents for cement plant operations. We deploy tailored AI in 3-week sprints — covering your entire plant from quarry to shipping — for plants that need to run safer and smarter without adding headcount.

**Want the full platform?** [Book a demo](https://cementops.ai) | **Contact:** jlarkin@cementops.ai

## License

MIT
