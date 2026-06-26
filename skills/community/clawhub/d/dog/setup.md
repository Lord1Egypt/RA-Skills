# Setup - Dog

Read this on first activation when `~/dog/` does not exist or is incomplete.

## Operating Attitude

- Be practical, calm, and specific.
- Help with the live problem first, then capture the context that improves future support.
- Treat dog care as operations: health, walks, training, safety, and logistics all interact.
- Stay conservative whenever health risk or bite risk is unclear.

## First Activation

1. Ask how the user wants this skill to activate:
   - whenever they mention a dog, puppy, foster, or dog-care task
   - only when explicitly requested
   - only for specific dogs or topics such as health, walks, training, or travel
2. Ask permission before writing local files:
```bash
mkdir -p ~/dog/dogs ~/dog/sitter-packs
touch ~/dog/memory.md ~/dog/shopping.md
chmod 700 ~/dog
```
3. If approved and `memory.md` is empty, initialize from `memory-template.md`.
4. Identify the current roster:
   - each dog's name
   - age or age range
   - size or weight range if known
   - major conditions, meds, or allergies already known
5. Ask what matters most right now:
   - symptom or urgent concern
   - walk or routine setup
   - training or behavior issue
   - travel, boarding, or sitter planning
   - vet or medication coordination

## Baseline Context to Capture

Capture only details that improve future support materially:
- household composition and who handles the dog
- normal walk load and current constraints
- training level, major triggers, and management tools already used
- feeding style and restrictions
- regular vet or emergency clinic details if the user wants them stored
- boarding, crate, car, grooming, or handling difficulty

If there is an active problem, ask only what changes the next safe step.

## Runtime Defaults

- For symptoms, open with `triage.md`.
- For training, check threshold and management before adding more difficulty.
- For behavior, ask what happened, where, and at what distance.
- For travel or boarding, reduce friction with a concrete handoff pack.
- If the user declines memory, still help fully in-session without pushing setup again.

## Integration Preference

Store activation preference in plain language, for example:
- "Use dog automatically whenever I talk about Mochi or dog care."
- "Ask first before switching into dog mode."
- "Only use dog for walks, training, and health questions."
