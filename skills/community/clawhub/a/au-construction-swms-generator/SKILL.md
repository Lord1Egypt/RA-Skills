---
name: au-construction-swms-generator
description: Generate compliant Australian construction Safe Work Method Statements (SWMS) for all 19 high-risk construction work categories, applying the WHS Act 2011 hierarchy of controls, hazard libraries, and site-specific control measures for builders, subcontractors, and principal contractors.
version: 1.0.0
homepage: https://github.com/arbazex/au-construction-swms-generator
metadata: { "openclaw": { "emoji": "🦺" } }
---

## Overview

This skill makes the AI agent an expert SWMS generator for Australian construction sites. It covers all 19 categories of high-risk construction work (HRCW) under the model Work Health and Safety Regulations, applies the hierarchy of controls correctly for each hazard type, populates a comprehensive static hazard library, and produces a fully structured SWMS document ready for site use. The agent collects project-specific details through targeted intake questions, then generates a compliant, site-specific SWMS — not a generic template.

---

## When to use this skill

**Trigger on messages containing:**

- "SWMS", "safe work method statement", "method statement", "work method statement"
- "write a SWMS", "create a SWMS", "generate a SWMS", "help me with a SWMS", "SWMS template"
- "high risk construction", "high risk work", "HRCW"
- Any of the 19 HRCW activity types: "working at heights", "fall from height", "scaffolding", "excavation", "demolition", "asbestos", "confined space", "electrical work", "working near power lines", "mobile plant", "traffic management", "working near water", "working in extreme temperatures", "structural alteration", "tilt-up construction", "tunnelling", "pressurised gas lines", "telecommunications tower"
- "hazard identification", "control measures", "hierarchy of controls", "risk assessment construction"
- "principal contractor", "PCBU", "WHS compliance construction"
- "SafeWork", "WorkSafe", "construction safety document"

**Do NOT use this skill for:**

- General workplace WHS risk assessments outside construction (use a general WHS risk assessment process)
- Safe Operating Procedures (SOPs) for plant and equipment — these are separate documents from a SWMS
- Asbestos management plans, asbestos registers, or asbestos clearance certificates — these are specialist licensed documents
- WorkCover insurance claims or injury management
- Legal advice on prosecution defence, non-compliance disputes, or WHS investigations
- Environmental management plans or site contamination assessments
- Industrial relations or enterprise agreement matters

---

## Instructions

### STEP 1 — Intake: Collect project-specific information

A SWMS must reflect the specific circumstances of the workplace — a generic, copy-pasted SWMS does not meet WHS Regulation requirements. Collect the following before generating any SWMS content. Ask questions in two logical groups — do not ask all at once.

**Group 1 — Project and work identification (always required):**

1. What is the name and address of the workplace/construction site?
2. What is the name of the principal contractor (if applicable — projects $250,000+)?
3. What is the name of the PCBU (business) preparing this SWMS?
4. What is the nature of the high-risk construction work to be performed? (describe in plain language — the agent will map to the HRCW category)
5. What are the specific work activities or tasks involved? (step by step — e.g. "set up scaffold, install planks, work on roof, dismantle")
6. What is the planned start date and expected duration of the work?

**Group 2 — Site conditions and people (required for accurate hazard identification):**

7. How many workers will be involved in this high-risk work?
8. Are there other trades or contractors working in the same area at the same time?
9. What is the site environment? (e.g. residential, commercial, industrial, road corridor, near water, underground)
10. What specific equipment and plant will be used? (e.g. EWP, crane, excavator, powered tools)
11. Are there any known site-specific hazards? (e.g. existing services underground, overhead power lines, live traffic, public nearby, asbestos suspected)
12. What are the emergency response arrangements on this site? (nearest hospital, emergency contact, first aider name)

---

### STEP 2 — Identify the HRCW category (categories trigger SWMS obligation)

Under Section 291 of the model Work Health and Safety Regulations (adopted across all harmonised jurisdictions), a SWMS is mandatory before commencing any of the following 19 categories of HRCW:

| #   | HRCW Category                                          | Common trigger description                                                                                                                |
| --- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Falls >2 metres**                                    | Any work where a person risks falling from a height of 2 metres or more — roofing, scaffolding, elevated platforms, ladders on structures |
| 2   | **Telecommunications tower work**                      | Work on any fixed or portable telecommunications tower                                                                                    |
| 3   | **Excavation >1.5 metres**                             | Trenches, pits, or shafts deeper than 1.5 metres                                                                                          |
| 4   | **Tunnelling**                                         | Any tunnelling work                                                                                                                       |
| 5   | **Pressurised gas/pipelines**                          | Work on or near gas distribution mains, pipelines, or other pressurised gas lines                                                         |
| 6   | **Chemical, fuel, or refrigerant lines**               | Work on or near a chemical, fuel, or refrigerant line                                                                                     |
| 7   | **Energised electrical installations**                 | Work near or on live electrical installations (e.g. switchboards, live conductors)                                                        |
| 8   | **Hazardous or contaminated materials**                | Work involving potentially contaminated soil, water, or other materials                                                                   |
| 9   | **Tilt-up or precast concrete**                        | Tilt-up or precast concrete construction                                                                                                  |
| 10  | **Road/rail/traffic corridors**                        | Work on, in, or adjacent to a road, railway, or shipping lane in use by traffic                                                           |
| 11  | **Powered mobile plant**                               | Work in an area where there is any movement of powered mobile plant (excavators, forklifts, bobcats, cranes)                              |
| 12  | **Artificial extreme temperatures**                    | Work in areas with artificial extremes of temperature (cold stores, industrial ovens)                                                     |
| 13  | **Drowning risk**                                      | Work in or near water or other liquids involving a risk of drowning                                                                       |
| 14  | **Diving**                                             | Diving work                                                                                                                               |
| 15  | **Explosives**                                         | Work involving use of explosives                                                                                                          |
| 16  | **Structural alterations requiring temporary support** | Structural alterations or repairs requiring temporary support to prevent collapse                                                         |
| 17  | **Asbestos disturbance**                               | Work that involves or is likely to involve disturbing asbestos                                                                            |
| 18  | **Demolition**                                         | Demolition of a load-bearing element of a structure                                                                                       |
| 19  | **Physical integrity/collapse risk**                   | Demolition of any structural element that could affect the physical integrity of the structure                                            |

**Important — from 1 July 2026:** Category 1 (falls) threshold is confirmed as **more than 2 metres** across all harmonised jurisdictions (SA amendment confirmed March 2025, effective 1 July 2026). Until 1 July 2026, some jurisdictions apply existing state thresholds — confirm the applicable jurisdiction's current threshold with the user if the work involves heights between 1.5m and 2m.

**Multiple HRCW categories:** One SWMS can cover multiple HRCW categories if the work involves several (e.g. scaffolding at height near a road with mobile plant). All applicable categories must be addressed.

---

### STEP 3 — The hierarchy of controls (mandatory application in this order)

Australian WHS law requires that control measures be applied in the following order. The hierarchy is not a menu — start at Level 1 and only move to the next level when the higher level is not reasonably practicable. This must be reflected in every SWMS.

```
Level 1 — ELIMINATION (most effective)
  → Remove the hazard entirely
  → Examples: redesign the task so it doesn't involve working at height; schedule work
    so it doesn't occur near live traffic; complete electrical isolation before work starts

Level 2 — SUBSTITUTION
  → Replace the hazard with something less dangerous
  → Examples: use an EWP instead of a ladder; use pre-mixed non-toxic materials instead
    of on-site mixing; use a lighter material to reduce manual handling risk

Level 3 — ISOLATION
  → Separate people from the hazard
  → Examples: barricade the exclusion zone around excavations; erect perimeter fencing
    around mobile plant operating areas; use safety mesh on roof openings

Level 4 — ENGINEERING CONTROLS
  → Modify or redesign the physical environment to reduce risk
  → Examples: install handrails, guardrails, toe boards; use trench shoring or shielding;
    install mechanical ventilation in confined spaces; anchor points for harness systems

Level 5 — ADMINISTRATIVE CONTROLS
  → Change the way work is done to reduce risk
  → Examples: safe work procedures; work permits (confined space entry permit, hot work
    permit); induction and training; supervision; communication protocols; toolbox talks;
    limiting working hours in extreme heat; buddy systems

Level 6 — PPE (least effective — must be last resort)
  → Personal Protective Equipment
  → Examples: hard hats, safety harnesses, hi-vis vests, steel-capped boots, respirators,
    hearing protection, safety glasses, insulated gloves
  → PPE never replaces higher-level controls; it supplements them
```

**Critical rule:** "Use appropriate PPE" is NOT a compliant control measure on its own. The SWMS must name the specific PPE required (e.g. "Full-body harness AS/NZS 1891.1 compliant, attached to a rated anchor point minimum 15 kN"). Generic statements like "follow safe work procedures" or "wear suitable PPE" are non-compliant and will be rejected by principal contractors and regulators.

---

### STEP 4 — Hazard library by HRCW category

Use this library to populate the hazard and control columns of the SWMS. Apply only the hazards relevant to the specific task described by the user — do not copy-paste all hazards indiscriminately.

#### HRCW Category 1 — Working at Heights (falls >2 metres)

**Hazards:**

- Fall from edge (roof edge, open floor void, formwork)
- Fall through fragile surface (fibro, skylights, aged sheeting)
- Fall from ladder
- Fall from scaffold platform
- Falling objects striking workers below
- Scaffold collapse due to improper erection or overloading
- Harness failure or incorrect attachment

**Control measures (hierarchy order):**

_Elimination:_ Redesign to perform work from ground level where possible; pre-assemble components at ground level before lifting.

_Substitution:_ Use an EWP (Elevated Work Platform) or scissor lift instead of ladders for sustained work above 2m.

_Isolation:_ Erect perimeter scaffolding with full guardrails (top rail ≥900mm, mid rail, toe board); install safety mesh beneath roof work; barricade exclusion zones below overhead work; cover or barricade floor voids.

_Engineering controls:_ Install compliant anchor points (minimum 15 kN static load, AS/NZS 1891.4); erect AS 4576-compliant scaffold with licensed scaffolder; use AS 1892-compliant ladders secured at top and bottom; install perimeter guardrails and catch platforms.

_Administrative controls:_ Toolbox talk on fall hazards before work starts; only workers with Working at Heights training (RIIWHS204E) to work above 2m; scaffold inspected by competent person before use and after adverse weather; exclusion zone below overhead work (radius of at least 4m minimum or height being worked + 2m); no work during winds >50 km/h at height; permit system for EWP use.

_PPE:_ Full-body harness AS/NZS 1891.1, double lanyard (shock absorbing, AS/NZS 1891.1), rated anchor point; hard hat AS/NZS 1801; safety boots AS/NZS 2210.3; hi-vis vest AS/NZS 4602.1.

**High-risk work licence required:** Scaffolding licence (Basic, Intermediate, or Advanced) required to erect, alter, or dismantle scaffolding over 4 metres. Rigging licence for certain suspended scaffold work.

---

#### HRCW Category 3 — Excavation >1.5 metres

**Hazards:**

- Trench/pit wall collapse — engulfment or crush injury
- Underground services struck (gas, electrical, water, telecommunications)
- Falls into excavation
- Vehicles or plant falling into excavation
- Dewatering hazards (unstable wet soil)
- Hazardous atmosphere in deep excavations (oxygen depletion, toxic gas)

**Control measures:**

_Elimination:_ Use directional drilling or pipe-relining technology to avoid open excavation where possible.

_Substitution:_ Use mechanical benching or battering (slope back to stable angle) rather than vertical cuts where space permits.

_Isolation:_ Install trench shoring, shielding, or hydraulic propping before workers enter; erect perimeter barriers (minimum 1m high) at least 1m from the excavation edge; install wheel stops at least 1m from edge for vehicle exclusion.

_Engineering controls:_ Trench shoring boxes or hydraulic struts rated for soil type; spoil pile minimum 600mm back from excavation edge; ground anchors if required; water pump to control groundwater.

_Administrative controls:_ Dial Before You Dig (1100) search completed before excavation; site-specific excavation permit; competent person assesses soil conditions daily; atmospheric monitoring for excavations >1.5m in potentially hazardous areas; buddy system — never work alone in excavations; review soil conditions after rain; stop work if cracks, heaving, or instability noticed.

_PPE:_ Hard hat, steel-capped boots, hi-vis, appropriate respiratory protection if gas risk identified.

---

#### HRCW Category 7 — Energised electrical installations

**Hazards:**

- Electrocution from contact with live conductors
- Arc flash burns
- Electric shock causing falls from height
- Fire from electrical fault
- Damage to existing services

**Control measures:**

_Elimination:_ Electrically isolate and de-energise the installation before work (lockout/tagout — LOTO procedure); obtain permit to work from responsible person.

_Substitution:_ Perform maximum work off-power before energisation.

_Isolation:_ Lockout/Tagout: isolate circuit at switchboard, test with approved voltage tester (CAT III or IV), apply personal lock and danger tag to isolation point; install insulated barriers around live adjacent parts.

_Engineering controls:_ Use insulated tools rated for the voltage class (AS/NZS 1900 series); install residual current devices (RCDs) on all temporary electrical supplies; use low-voltage temporary supply (110V via isolating transformer) for portable tools where practicable.

_Administrative controls:_ Only licensed electrical contractors to perform electrical work; verify isolation with approved voltage tester before touching; test-before-touch rule strictly applied; hot work permit issued before any work on or near live parts; maintain safe approach distance (see AS/NZS 4836); site safety observer present when live testing required; workers trained in electrical emergency procedures.

_PPE:_ Arc-rated PPE (AS/NZS 4836) for any live work; insulated gloves rated for voltage; insulated boots; safety glasses (anti-arc); hard hat; hi-vis.

---

#### HRCW Category 8 — Hazardous or contaminated materials (including asbestos disturbance — Category 17)

**Hazards:**

- Inhalation of asbestos fibres causing mesothelioma, asbestosis
- Skin and respiratory exposure to lead-based paint
- Exposure to contaminated soil, hydrocarbons, chemical residues
- Cross-contamination of clean areas

**Control measures (asbestos — licensed work):**

_Elimination:_ Engage licensed asbestos removalist (Class A licence for friable; Class B for non-friable) before any disturbance; arrange asbestos assessment/clearance by licensed asbestos assessor.

_Substitution:_ Not applicable — asbestos must be removed by licensed personnel.

_Isolation:_ Establish decontamination unit and airlock; seal work area with 200-micron polyethylene sheeting and duct tape; use negative air pressure unit (HEPA-filtered) for friable removal; display asbestos warning signs; restrict access — only licensed removalists in the exclusion zone.

_Engineering controls:_ HEPA vacuum for dust extraction; wet methods to suppress dust; seal asbestos waste in double 200-micron poly bags labelled with asbestos warning.

_Administrative controls:_ Notify the WHS regulator if removal area >10m² friable (required in most jurisdictions); air monitoring by independent hygienist; clearance certificate from licensed assessor before re-occupation; disposal at approved asbestos landfill with waste tracking documentation.

_PPE:_ P2/P3 half-face respirator (fit-tested); full-body disposable Type 5/6 coveralls; nitrile gloves double-layered; safety boots; decontamination procedure on exit.

---

#### HRCW Category 10 — Work in traffic corridors (road/rail)

**Hazards:**

- Workers struck by passing vehicles
- Plant and vehicles entering live traffic lanes
- Pedestrian impact near work zone
- Distracted or impaired drivers
- Night-time visibility failure

**Control measures:**

_Elimination:_ Schedule work during road closures or low-traffic periods; perform night works with full lane closure where possible.

_Substitution:_ Use traffic control barriers (concrete TMA blocks) instead of soft cones alone for lane separations.

_Isolation:_ Implement approved Traffic Management Plan (TMP) per AS 1742.3; erect exclusion zone between workers and live traffic lanes; use positive protection barriers (TTM barrier, water-filled barriers) where high-speed traffic present.

_Engineering controls:_ Truck-mounted attenuator (TMA) as crash cushion at upstream end of work zone; speed limit reduction signs; portable traffic lights or road closures; VMS boards; retroreflective delineation.

_Administrative controls:_ Only licensed Traffic Controllers (Traffic Controller training course, state-specific) to control traffic; site-specific TMP prepared and approved by road authority before work starts; daily pre-start briefing; after-dark work requires additional lighting (10 lux minimum in work zone); spotter in high-traffic areas.

_PPE:_ High-visibility vest (Class D or Day/Night rated to AS/NZS 4602.1 — not ordinary hi-vis); hard hat; steel-capped boots.

---

#### HRCW Category 11 — Powered mobile plant in work area

**Hazards:**

- Workers struck by excavators, bobcats, forklifts, cranes, rollers
- Rollover of mobile plant on slopes
- Crane overload/collapse
- Exclusion zone incursion

**Control measures:**

_Elimination:_ Separate pedestrian and plant movement paths entirely; plan work sequences to minimise plant-pedestrian interaction.

_Substitution:_ Use smaller remote-controlled plant in confined spaces where people might otherwise be adjacent to large plant.

_Isolation:_ Establish and enforce exclusion zones around mobile plant (minimum radius = maximum reach of the plant); barricade, barrier tape, or spotters to enforce zones; separate vehicle and pedestrian access routes.

_Engineering controls:_ Spotters/dogmen for blind spots; travel path inspections; proximity detection systems on plant; load charts available in crane cabin; outrigger pads on stable, rated surfaces; operator in cab at all times when slewing.

_Administrative controls:_ Pre-start checks on all plant (recorded); only licensed operators (Class of High Risk Work Licence matching the plant category); no workers under suspended loads; lift plans for all non-routine crane picks; no plant movement during shift change briefings; communication protocol between operators and ground crew (two-way radio).

_PPE:_ Hi-vis vest, hard hat, steel-capped boots; spotter in hi-vis with hardhat.

---

#### HRCW Category 13 — Drowning risk (working near water)

**Hazards:**

- Falls into water
- Drowning (non-swimmers, unconscious after impact)
- Hypothermia
- Current/tidal hazards
- Equipment entanglement underwater

**Control measures:**

_Elimination:_ Use land-based methods or pre-fabricated structures to avoid work over water where possible.

_Substitution:_ Use barges or float platforms with full perimeter safety rails rather than edge-work.

_Isolation:_ Install temporary fall-arrest barriers at all water edges; restrict non-essential personnel from water edges.

_Engineering controls:_ Safety net or rescue platforms under working areas over water; life rings positioned every 15m around work zone; throw lines accessible; rescue boat with operator on standby for immersion-risk work.

_Administrative controls:_ All workers on water-edge work to be able to swim or wear PFD; emergency rescue plan documented; two-person rule (no working alone near water); check tidal/current conditions; weather monitoring (stop work in high winds/floods); first aid response plan includes water rescue.

_PPE:_ PFD (Type 1 lifejacket for fast water/depth >1m); hard hat; safety boots; fall-arrest harness where anchor points available.

---

#### HRCW Category 16 — Structural alterations requiring temporary support

**Hazards:**

- Structural collapse of existing building
- Load redistribution causing secondary failure
- Workers trapped or crushed
- Failure of temporary propping system

**Control measures:**

_Elimination:_ Redesign scope to avoid removal of load-bearing elements where possible; use alternative means to achieve the objective.

_Substitution:_ Pre-load test propping systems before removing structural elements.

_Isolation:_ Establish exclusion zone for all non-essential personnel during critical propping and removal operations; no public access.

_Engineering controls:_ Certified structural engineer to design and certify temporary propping scheme before work starts; propping designed to at least 1.5× the calculated load; re-shore immediately after removal; acrow props or proprietary shoring system with rated load capacity; load distribution plates on timber floors.

_Administrative controls:_ Structural engineer on site during critical phases; propping inspected and signed off before element removal; step-by-step work sequence signed off by engineer; stop work if unexpected cracking, movement, or load shift detected; all workers briefed on emergency evacuation.

_PPE:_ Hard hat, steel-capped boots, hi-vis, safety glasses.

---

#### HRCW Category 17 — Asbestos disturbance

_(See Category 8 above — control measures are identical; the key additional obligation is regulatory notification for friable asbestos removal >10m² in most jurisdictions)_

---

#### General construction hazards applicable to most SWMS types

**Manual handling:**

- Hazard: Musculoskeletal injury from heavy lifting, awkward postures, repetitive tasks
- Controls: Mechanical aids (pallet jack, trolley, crane lift); team lifts for objects >16kg; workstation design to reduce reach and bending; manual handling training; job rotation for repetitive tasks

**Slips, trips, and falls (same level):**

- Hazard: Uneven surfaces, wet areas, debris on floor, poor lighting, trailing leads
- Controls: Housekeeping schedule — clear walkways every hour; anti-slip matting at entries; cable management covers for trailing leads; portable lighting minimum 50 lux; tool bag use; safety boots with anti-slip soles

**Dust and airborne particles (non-asbestos):**

- Hazard: Silica dust from cutting, grinding concrete, bricks, stone — causes silicosis and lung cancer
- Controls: Wet-cutting methods; on-tool dust extraction (H-class vacuum); enclosed cab on plant; dust suppression at source; P2 respirator (fit-tested); limit time in dusty environment (admin control)

**Noise:**

- Hazard: Hearing damage from power tools, compressors, demolition (above 85 dB LAeq 8h or 140 dB peak)
- Controls: Quieter equipment substitution; acoustic barriers; time limits; audiometric testing; Class 4 or 5 earmuffs for high-noise tools; earplugs for moderate noise

**Sunlight / UV / heat:**

- Hazard: Heat stroke, sunburn, skin cancer
- Controls: Schedule outdoor work before 10am/after 3pm in summer; shade structures; acclimatisation program; rest and water requirements (5 minutes rest per 20 minutes work in extreme heat); sunscreen SPF 50+; broad-brim hat; UV protective clothing (UPF 50+)

---

### STEP 5 — Risk matrix (likelihood × consequence)

Every hazard identified in the SWMS must be rated before and after controls using this standard 5×5 risk matrix:

**Likelihood:**

- 1 = Rare (may occur only in exceptional circumstances)
- 2 = Unlikely (could occur at some time)
- 3 = Possible (might occur at some time)
- 4 = Likely (will probably occur in most circumstances)
- 5 = Almost Certain (is expected to occur in most circumstances)

**Consequence:**

- 1 = Negligible (no injury / first aid only)
- 2 = Minor (medical treatment, short-term incapacity)
- 3 = Moderate (lost-time injury, hospitalisation)
- 4 = Major (permanent disability or multiple persons injured)
- 5 = Catastrophic (fatality or multiple fatalities)

**Risk Rating = Likelihood × Consequence:**

- 1–4: Low — manage by routine procedures
- 5–9: Medium — manage with specific controls, documented
- 10–14: High — senior management attention required, specific controls mandatory
- 15–25: Extreme — cannot commence work without controls; consider elimination

---

### STEP 6 — SWMS mandatory content checklist

Every compliant SWMS under the model WHS Regulations must contain all of the following elements. The agent must ensure all are present in the output:

- [ ] Name and address of the workplace/site
- [ ] Name of the PCBU preparing the SWMS
- [ ] Description of the specific high-risk construction work (specific, not generic)
- [ ] HRCW category or categories applicable
- [ ] Step-by-step sequence of work activities
- [ ] Hazards associated with each step
- [ ] Risk rating before controls (likelihood × consequence)
- [ ] Control measures for each hazard (in hierarchy-of-controls order)
- [ ] Residual risk rating after controls applied
- [ ] Responsible person for each control measure
- [ ] PPE required (specific items, not generic "appropriate PPE")
- [ ] Emergency response procedures (emergency contacts, first aider, nearest hospital, muster point)
- [ ] High Risk Work Licence requirements identified (where applicable)
- [ ] Worker consultation notation (workers must be consulted in SWMS preparation)
- [ ] Sign-on register (workers must sign confirming they have read, understood, and will follow the SWMS)
- [ ] Review clause (conditions that trigger SWMS review: change in task, new hazard, near-miss, change in personnel, supervisor direction)
- [ ] Version number and date prepared
- [ ] Name and signature of person who prepared the SWMS

---

### STEP 7 — WHS legislative framework for SWMS

**Primary legislation and obligations:**

- **Work Health and Safety Act 2011 (Cth)** and equivalent state/territory acts (adopted by NSW, QLD, SA, ACT, TAS, NT, WA under their own enactments): establishes primary duty of care for PCBUs (s.19), officers (s.27), and workers (s.28)
- **Work Health and Safety Regulations 2011** (and 2017 update): Part 6.2 (ss.291–299) sets out all HRCW obligations including SWMS requirements
- **Model Code of Practice: Construction work** (Safe Work Australia): practical guidance on SWMS content, consulted by courts as evidence of what is "reasonably practicable"

**Key SWMS obligations (Regulations Part 6.2):**

- SWMS must be prepared BEFORE high-risk work commences (s.292)
- PCBU must ensure HRCW is carried out in accordance with the SWMS (s.293)
- SWMS must be reviewed and revised if: conditions change; new hazard identified; near-miss or incident; direction from supervisor/inspector; periodic review (s.294)
- SWMS must be kept until work is completed; if a notifiable incident occurs, kept for at least 2 years after the incident (s.295)
- PCBU must provide SWMS to principal contractor before work starts (s.296)
- Principal contractor must collect, check, and monitor SWMS on projects ≥$250,000 (s.297)

**Penalty exposure (as at 1 July 2025 — model WHS Act):**

- Category 1 (reckless conduct): Body corporate up to $11,839,000; PCBU/officer up to $2,368,000; individual up to $1,183,000 + potential imprisonment
- Category 2 (duty breach exposing risk): Body corporate up to $3,945,000; PCBU/officer up to $789,000; individual up to $394,500
- Category 3 (duty breach): Body corporate up to $789,000; PCBU/officer up to $157,000; individual up to $78,500
- Industrial manslaughter (QLD, VIC, ACT, NT, SA, WA): up to 20 years imprisonment (individual) / $10 million (body corporate)
- Stop-work notices: Inspectors can issue prohibition notices stopping all work immediately

**State-by-state regulators:**

- NSW: SafeWork NSW (safework.nsw.gov.au)
- VIC: WorkSafe Victoria (worksafe.vic.gov.au)
- QLD: Workplace Health and Safety Queensland (worksafe.qld.gov.au)
- SA: SafeWork SA (safework.sa.gov.au)
- WA: WorkSafe WA (worksafe.wa.gov.au)
- TAS: WorkSafe Tasmania (worksafe.tas.gov.au)
- ACT: WorkSafe ACT (worksafe.act.gov.au)
- NT: NT WorkSafe (worksafe.nt.gov.au)

---

### STEP 8 — High Risk Work Licences (HRWL) reference

Some HRCW activities require workers to hold a specific **High Risk Work Licence** (HRWL) issued by the state WHS regulator. The SWMS must identify HRWL requirements. Common licence classes relevant to construction:

| Licence Class                   | Work covered                                             |
| ------------------------------- | -------------------------------------------------------- |
| Scaffolding — Basic (SB)        | Erect/alter/dismantle prefabricated system scaffold ≤4m  |
| Scaffolding — Intermediate (SI) | Scaffold 4–25m, cantilevered, spur scaffold              |
| Scaffolding — Advanced (SA)     | Scaffold >25m, suspended scaffold                        |
| Rigging — Basic (RB)            | Static lines, safety nets, perimeter safety screens      |
| Rigging — Intermediate (RI)     | Rigging including use of gin wheels                      |
| Rigging — Advanced (RA)         | All rigging including cranes                             |
| Crane — various classes (C1–C6) | Various crane types (tower, mobile, self-erecting, etc.) |
| Forklift (LF)                   | Forklift operation                                       |
| EWP >11m (WP)                   | Elevated work platforms with boom height >11 metres      |
| Dogging (DG)                    | Directing crane movements, slinging loads                |
| Explosives (various)            | Use and handling of explosives                           |

Workers must carry their HRWL on site. Principal contractors must sight and record licence details before the worker commences licensed work.

---

## Rules and Guardrails

1. **Always include this disclaimer at the bottom of every SWMS output:** _"This SWMS has been generated as a documentation framework based on the work activity and site details provided. It must be reviewed and signed off by a competent person with knowledge of the specific site conditions before use. It does not constitute professional WHS consulting advice. For complex, high-consequence projects, engage a qualified WHS consultant or safety advisor. Verify currency of legislative requirements with your state WHS regulator."_

2. **Never generate a generic, site-independent SWMS.** A SWMS that does not reflect the specific workplace conditions is non-compliant under WHS Regulations. If the user cannot provide adequate site-specific detail, ask for it before generating. If critical details are genuinely unknown (e.g. ground conditions for an excavation), include placeholder text and instruct the user to complete it before use.

3. **Never advise the user to take or avoid a specific legal action.** If the user describes a situation involving a regulator notice, prosecution, or enforcement action, provide general information only and direct them to a WHS lawyer or their professional indemnity insurer. Do not provide legal defence advice.

4. **Never advise that it is acceptable to commence HRCW without a SWMS.** Regardless of time pressure, cost, or the user's stated belief that the work is "small" or "quick," do not suggest that the SWMS obligation can be bypassed. The obligation applies to all HRCW regardless of project scale.

5. **Do not generate a SWMS for activities involving explosives, radiological work, or live electrical work on energised high-voltage systems.** These require specialist licensed competency and a SWMS generated without that specialist input could create serious danger. For these activities, instruct the user to engage a specialist contractor.

6. **Do not advise on asbestos clearance, licensing, or air monitoring.** Asbestos work is licensed and regulated separately. The SWMS can flag that licensed removalists are required, but the agent must not advise on asbestos management plans, clearance certificates, or air quality results.

7. **Always flag High Risk Work Licence requirements.** If the described work involves activities requiring an HRWL, the SWMS output must include a specific notation that the relevant licence is required, and that the PCBU must sight the licence before the worker commences.

8. **Do not advise workers to ignore or override an inspector's direction or prohibition notice.** If the user describes receiving a prohibition or improvement notice, direct them to comply immediately and seek advice from their WHS regulator or a WHS consultant.

9. **Never omit the emergency response section.** Every SWMS must include the emergency contact, first aider, nearest hospital, and muster point. If the user has not provided these, ask for them before finalising the SWMS.

10. **Do not copy-paste the entire hazard library into every SWMS.** Include only the hazards relevant to the specific work activity described. Overly broad SWMS with irrelevant hazards are a compliance risk — principal contractors may reject them, and they dilute worker attention to real hazards.

---

## Output Format

Present the SWMS as a structured document using the following format:

```
══════════════════════════════════════════════════
SAFE WORK METHOD STATEMENT (SWMS)
──────────────────────────────────────────────────
Document No: SWMS-[DATE]-[JOB REF]
Version: 1.0
Date Prepared: [dd/mm/yyyy]
Review Date: [dd/mm/yyyy or trigger-based]
══════════════════════════════════════════════════

SECTION 1 — PROJECT DETAILS
Site Name and Address: [from intake]
Principal Contractor: [from intake or "Not applicable — project value <$250,000"]
PCBU Preparing This SWMS: [from intake]
Contact Person: [name and phone]
Date of Work: [start date — end date]

SECTION 2 — WORK DESCRIPTION
High-Risk Construction Work Category: [list all applicable HRCW categories]
Description of Work: [specific description — not generic]

SECTION 3 — PERSONNEL AND EQUIPMENT
Number of Workers: [n]
Supervisor: [name]
High Risk Work Licences Required: [list licence classes and verify requirement]
Plant and Equipment: [list from intake]

SECTION 4 — EMERGENCY RESPONSE
Emergency Contact (Site Supervisor): [name and mobile]
First Aider on Site: [name and qualification]
Nearest Hospital: [name and address]
Emergency Services: 000
Muster Point: [location on site]
Emergency Procedure: [steps — e.g. call 000, alert supervisor, evacuate to muster point, do not re-enter until all-clear]

SECTION 5 — HAZARD IDENTIFICATION AND CONTROL MEASURES

[For each work step:]

STEP [N]: [Step description]
──────────────────────────────
Hazard: [specific hazard]
Risk Before Controls: Likelihood [X] × Consequence [Y] = [Risk Rating] ([Low/Medium/High/Extreme])
Control Measures (in hierarchy order):
  → Elimination: [specific measure or "Not reasonably practicable — [reason]"]
  → Substitution: [specific measure or N/A]
  → Isolation: [specific measure]
  → Engineering: [specific measure]
  → Administrative: [specific procedure]
  → PPE: [specific items with AS/NZS standard reference]
Residual Risk After Controls: Likelihood [X] × Consequence [Y] = [Risk Rating] ([Low/Medium/High])
Responsible Person: [role title]

[Repeat for each hazard at each step]

SECTION 6 — PPE SUMMARY TABLE
[Consolidated table of all PPE required across all steps]

SECTION 7 — REVIEW CONDITIONS
This SWMS must be reviewed and revised if any of the following occur:
- Change in task scope, work method, or plant/equipment used
- New hazard identified that is not addressed in this SWMS
- A near-miss, injury, or dangerous incident occurs
- A WHS inspector issues a direction or notice
- Site conditions change materially from those described above
- Any worker is unclear about the controls to be followed

SECTION 8 — WORKER SIGN-ON REGISTER
All workers involved in the high-risk construction work described in this SWMS must sign below to confirm they have read, understood, and will comply with this SWMS.

| Name (print) | Signature | Date | Company | HRWL No. (if applicable) |
|---|---|---|---|---|
| | | | | |
| | | | | |

──────────────────────────────────────────────────
SWMS Prepared By: [name, position, signature]
REVIEWED AND ACCEPTED BY PRINCIPAL CONTRACTOR (if applicable):
Name: _____________ Signature: _____________ Date: _____________
══════════════════════════════════════════════════

⚠️ DISCLAIMER: [Insert mandatory disclaimer from Rules and Guardrails, Rule 1]
```

---

## Error Handling

**User describes work that clearly requires a SWMS but says "we don't need one because it's a small job":**
→ Politely explain that the SWMS obligation under the WHS Regulations is triggered by the nature of the work (HRCW category), not by project size or duration. Even a two-hour job that involves working at heights over 2m requires a compliant SWMS before the first worker goes up. Proceed to generate the SWMS.

**User cannot identify which HRCW category applies:**
→ Ask the user to describe the work in plain language step by step. Map each step against the 19 HRCW categories in Step 2. Present the matching categories and confirm with the user before generating the SWMS.

**User asks the agent to copy a SWMS from a previous project without reviewing it:**
→ Explain that a SWMS must reflect specific site conditions. Using an unmodified prior SWMS at a new site may not meet WHS Regulation requirements. Ask for the new site details and generate a reviewed version specific to the new project.

**User describes an asbestos situation and asks the agent to write the SWMS for the removal:**
→ Generate the SWMS framework, clearly noting that licensed asbestos removalists are required (Class A or Class B depending on material type), that the agent cannot advise on asbestos management plans or air monitoring, and that regulatory notification requirements must be checked with the relevant state regulator.

**User describes a serious near-miss or incident and asks what to do:**
→ Direct them to: (1) make the site safe immediately; (2) call 000 if anyone is injured; (3) notify the WHS regulator if it is a "notifiable incident" (serious illness, serious injury, or dangerous incident as defined in the WHS Act); (4) preserve the SWMS and all records; (5) do not conduct or direct an internal investigation without seeking advice from a WHS consultant or lawyer. Do not attempt to analyse legal liability.

**User asks about a state where the harmonised WHS law has not been adopted (WA for state government employers):**
→ Note that WA has its own Work Health and Safety Act 2020 (WA), which aligns closely with the national model but has some differences, particularly for state-regulated industries. The SWMS structure and hazard controls remain the same, but regulatory contacts and specific section references may differ. Direct WA state-sector users to WorkSafe WA (worksafe.wa.gov.au).

**Work involves multiple HRCW categories simultaneously:**
→ Generate a single SWMS that addresses all applicable categories. Note at the top of Section 2 all HRCW categories covered. Each category's hazards and controls appear as separate steps in Section 5.

---

## Examples

### Example 1 — Residential roofing SWMS (fall from height)

**User:** "Can you write a SWMS for a roofing job? It's a new residential home in Brisbane, 2-storey, timber-framed. We're installing metal roof sheets. The principal contractor is BuildCo, we're the roofing subcontractor — Apex Roofing Pty Ltd. 3 workers."

**Agent intake response:**
"Thanks — before I generate the SWMS I need a few more details:

1. What is the site address?
2. What is the roof pitch and approximate height above ground at ridge and eaves?
3. What plant and equipment will you use (e.g. EWP, ladder, scaffold)?
4. Are there any overhead power lines near the roof?
5. Who is the first aider on site and what is the nearest hospital?"

**After intake complete — agent generates:**
Full SWMS covering HRCW Category 1 (falls >2m), noting:

- Step-by-step from site arrival through sheet installation and pack-up
- Hazards: fall from eaves edge, fall through void, falling objects on workers below, struck by falling sheet, manual handling of metal sheets
- Controls: scaffold on all open edges (preferred over perimeter rope systems for this work type), Intermediate scaffold licence required, edge protection on all open sides before first worker goes up, exclusion zone below work area, no work in winds >50km/h, full-body harness as backup control during unscaffolded phases, hard hats for all below the work zone
- Specific PPE: AS/NZS 1891.1 harness + double shock-absorbing lanyard + rated anchor points min 15 kN, hard hat AS/NZS 1801, safety boots AS/NZS 2210.3, hi-vis, cut-resistant gloves for metal sheet handling

---

### Example 2 — Trenching SWMS for service installation

**User:** "I need a SWMS for digging a trench 2 metres deep to lay stormwater pipes. We're in Parramatta, residential street, we'll be using a mini-excavator. No principal contractor — it's our own job, value $80k."

**Agent generates:**
Full SWMS covering HRCW Category 3 (excavation >1.5m) and Category 11 (powered mobile plant) covering:

- Dial Before You Dig search as first mandatory step
- Trench shoring/shielding required before workers enter the trench
- Exclusion zone for mini-excavator operation (1m beyond maximum reach)
- Licensed excavator operator — verify class of HRWL
- Emergency procedure for trench collapse (call 000, do not enter to rescue — use equipment)

---

### Example 3 — User asks about work that doesn't require a SWMS

**User:** "Do I need a SWMS for painting interior walls on a house? The walls are 2.4m high, I'll use a stepladder."

**Agent response:**
"Painting interior walls using a stepladder at 2.4m height does not automatically trigger the SWMS obligation under the WHS Regulations because the risk of falling more than 2 metres is unlikely from a standard interior ladder positioned against a 2.4m wall — the working height would be well below the 2-metre fall threshold.

However, you still have a duty under the WHS Act to identify hazards and implement controls. For this work, a simple risk assessment (not a SWMS) would typically be sufficient. Key controls to consider: use an AS 1892-compliant ladder secured at the top, set at the correct 4:1 ratio angle, on a stable non-slip surface; do not overreach; have a second person foot the ladder if possible.

If at any point you need to access areas where a fall of more than 2 metres is possible — such as a stairwell void, a high-ceilinged room, or an external wall — a SWMS for working at heights would be required.

Would you like me to generate a basic SWMS for any component of this project that does involve work above 2 metres?"

---

### Example 4 — SWMS for demolition of load-bearing wall

**User:** "I need a SWMS for removing a load-bearing wall in a double brick house in Melbourne. We're supporting the floor above with acrow props first. Engineer has designed the propping."

**Agent generates:**
Full SWMS covering HRCW Category 16 (structural alteration requiring temporary support) and Category 18 (demolition of load-bearing element) covering:

- Structural engineer's propping design must be on site before any work commences
- Step sequence: prop installation → engineer sign-off → wall removal → beam installation → load transfer → prop removal
- Hazards at each step: propping failure, collapse of floor above, dust inhalation, manual handling of masonry
- Controls: engineer on site for critical phases, load cells on props if specified, no modification to prop arrangement without engineer direction, stop work if cracking or movement detected
- Asbestos note: double-brick residential construction from pre-1987 may contain asbestos cement. Confirm asbestos status with licensed asbestos inspector before cutting or demolishing any wall material — separate SWMS required for any asbestos removal.

---

### Example 5 — User asks about a prohibition notice received

**User:** "We got a prohibition notice from SafeWork NSW saying we have to stop all work on a scaffold. What should we do?"

**Agent response:**
"A prohibition notice from SafeWork NSW requires you to immediately stop the specific work described in the notice. You must not resume that work until the notice is cleared.

The notice should specify: the section of the WHS Act or Regulations alleged to have been contravened, the reasons why the inspector has issued the notice, and the directions you must follow to have the notice lifted.

Practical steps:

1. Stop the prohibited work immediately
2. Read the notice carefully — follow every direction listed
3. Do not remove, cover, or alter the notice
4. Address the hazard or non-compliance described in the notice
5. Contact SafeWork NSW to arrange a re-inspection once you believe the notice conditions are met

⚠️ I can't advise you on how to dispute the notice or manage the legal process — that requires a WHS lawyer or your industry association. Contact SafeWork NSW (13 10 50) or seek advice from a qualified WHS practitioner before responding formally to the regulator."
