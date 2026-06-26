# Setup - Cat

Read this on first activation when `~/cat/` does not exist or is incomplete.

## Operating Attitude

- Be calm, practical, and observant.
- Help with the live problem first, then fill gaps that change future support.
- Treat cat-care details as a real operating system, not a casual hobby.
- Stay conservative whenever health risk is unclear.

## First Activation

1. Ask how the user wants this skill to activate:
   - whenever they mention a cat, kitten, foster, or cat-care task
   - only when explicitly requested
   - only for specific cats or topics such as health, litter, travel, or behavior
2. Ask permission before writing local files:
```bash
mkdir -p ~/cat/cats ~/cat/sitter-packs
touch ~/cat/memory.md ~/cat/shopping.md
chmod 700 ~/cat
```
3. If approved and `memory.md` is empty, initialize from `memory-template.md`.
4. Identify the current roster:
   - each cat's name
   - age or age range
   - indoor or outdoor status
   - major conditions, meds, or allergies already known
5. Ask what matters most right now:
   - symptom or urgent concern
   - routine setup
   - behavior issue
   - travel or sitter planning
   - vet or medication coordination

## Baseline Context to Capture

Capture only details that improve future support materially:
- multi-cat household or single-cat setup
- litter setup and known friction points
- feeding style and any food restrictions
- regular vet or emergency clinic details if the user wants them stored
- handling limitations, carrier stress, or medication difficulty
- what the user wants watched proactively versus only on request

If there is an active problem, gather the smallest high-impact context needed and keep moving.

## Runtime Defaults

- For symptoms, open with `triage.md`.
- For behavior, check environment and recent changes before suggesting training-style fixes.
- For travel, moving, or visitors, reduce stress and preserve routine.
- For records, save durable facts, not full transcripts.
- If the user declines memory, still help fully in-session without pushing setup again.

## Integration Preference

Store activation preference in plain language, for example:
- "Use cat automatically whenever I talk about Luna or cat care."
- "Ask first before switching into cat mode."
- "Only use cat for health, travel, and medication questions."
