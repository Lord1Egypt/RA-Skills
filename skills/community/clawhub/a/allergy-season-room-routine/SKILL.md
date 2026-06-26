---
name: allergy-season-room-routine
description: "Build a low-effort room routine card for sneezing, irritation, or stuffiness that feels worse indoors during allergy season, with daily, weekly, and high-pollen-day actions plus clear medical safety boundaries."
---

# Allergy Season Room Routine

## Purpose

Help the user create a practical, low-effort room routine for allergy season when sneezing, eye or nose irritation, or stuffiness seems worse indoors. The deliverable is a printable routine card for one room, organized into daily, weekly, and high-pollen-day actions.

This is a prompt-only home routine workflow. It is not medical advice and does not diagnose allergies, asthma, infection, mold illness, or any other health condition.

## Use This Skill When

Use this skill when the user wants to:

- Reduce likely indoor irritants during pollen season in a bedroom, living room, home office, entryway, or other room.
- Turn vague allergy-season discomfort into a simple cleaning, laundry, air, and entry routine.
- Pick low-effort actions instead of creating an unrealistic whole-home overhaul.
- Make a printable card they can place in the room or share with household members.
- Plan extra steps for high-pollen days without changing medication or treatment.

Do not use this skill to diagnose symptoms, recommend allergy medicines, adjust inhalers, evaluate severe reactions, inspect hazardous mold, or replace professional care.

## Best Inputs

Ask only for details the user can comfortably share. If information is missing, proceed with placeholders and mark assumptions.

- Room to focus on.
- Main symptoms or annoyances in the user's words.
- Suspected triggers such as pollen on clothes, open windows, pets, dust, bedding, rugs, vents, fragrance, smoke, dampness, or outdoor gear.
- Current cleaning or laundry habits.
- Tools available, such as vacuum, microfiber cloth, air purifier, washable curtains, HVAC filter, doormat, hamper, or storage bins.
- Effort level: tiny, moderate, or more thorough.
- Desired cadence and print size.

## Workflow

1. **Start with safety.** If the user reports breathing trouble, wheezing, throat or face swelling, faintness, chest tightness, severe reaction, or rapidly worsening symptoms, advise urgent local medical care before routine planning.
2. **Pick one room.** Keep the first routine focused on a single room so the result is usable.
3. **Note likely irritant paths.** Map how pollen or irritants may enter and settle: windows, shoes, clothes, pets, bedding, rugs, soft furniture, vents, clutter, laundry, or outdoor equipment.
4. **Choose low-effort actions.** Prefer small repeatable steps: close windows on high-pollen days, wipe surfaces, change pillowcase, run existing filtration, move outdoor clothes, wash hands or face after being outside, vacuum with available equipment, and reduce fragrance or smoke exposure.
5. **Separate cadence.** Sort actions into daily, weekly, and high-pollen-day sections. Keep each section short enough to finish.
6. **Add setup notes.** Include supplies, best time of day, household owner, and a two-minute minimum version.
7. **Create the printable card.** Produce a concise card with checkboxes, cadence, and a safety note.
8. **Add review prompt.** Suggest reviewing after one to two weeks to remove actions that did not help or were too hard to maintain.

## Output Format

Return the routine package in this order:

1. **Room Snapshot**

| Field | Detail |
|---|---|
| Room | |
| Main indoor discomfort | |
| Likely irritant paths | |
| Available tools | |
| Effort level | |
| Review date | |

2. **Low-Effort Action Menu**

| Action | Why it may help | Effort | Cadence |
|---|---|---|---|

Use cautious language such as "may reduce tracked irritants" and "worth trying." Do not promise symptom relief.

3. **Printable Room Routine Card**

```text
ALLERGY SEASON ROOM ROUTINE
Room:

Daily:
[ ] 
[ ] 
[ ] 

Weekly:
[ ] 
[ ] 
[ ] 

High-pollen-day extras:
[ ] 
[ ] 
[ ] 

Two-minute version:
[ ] 
[ ] 

Safety note:
This routine is not medical advice. Seek urgent local care for breathing trouble, wheezing, swelling, faintness, chest tightness, severe reactions, or symptoms that feel dangerous.
```

4. **Cadence Plan**

| When | Trigger | Actions |
|---|---|---|
| Daily | | |
| Weekly | | |
| High-pollen day | | |
| After outdoor exposure | | |

5. **Open Questions**

List missing details that would make the card more specific, such as room type, pets, bedding, windows, carpets, HVAC filter access, or available tools.

## Message Style

- Keep the routine realistic and easy to repeat.
- Use plain language and checkboxes.
- Focus on environment and habits, not diagnosis or treatment.
- Respect renters, shared homes, budgets, energy limits, and household conflict.
- Offer a smallest-useful version when the user is tired or busy.

## Safety Boundary

- Do not diagnose allergies, asthma, sinus infection, mold illness, chemical sensitivity, or any medical condition.
- Do not recommend medications, supplements, immunotherapy, inhaler changes, or dosing.
- Do not tell the user to stop prescribed treatment.
- Do not claim any room action will prevent allergic reactions or cure symptoms.
- For breathing trouble, wheezing, chest tightness, throat, tongue, lip, or face swelling, faintness, blue lips, severe hives, severe reactions, or rapidly worsening symptoms, advise urgent local medical care or emergency services.
- For persistent, new, worsening, or concerning symptoms, suggest contacting a qualified clinician.

## Example Prompts

- "My bedroom feels worse during pollen season. Make me a room routine card."
- "I sneeze more indoors after going outside. Help me build a low-effort plan."
- "Create daily, weekly, and high-pollen-day actions for my home office."
- "Make a printable allergy-season routine for a room with rugs and pets."
