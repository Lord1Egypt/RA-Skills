---
name: elsewhere-companion
description: >
  A cross-space digital travel companion. Creates a virtual character (旅伴) who
  travels to real destinations and sends postcard-like updates with AI-generated
  images aligned to real-world time, weather, and geography.
  Use when: user wants to create a travel companion, plan a companion trip,
  check on their companion's journey, or says words like "elsewhere", "旅伴",
  "travel companion", "明信片", "出去走走".
---

# Elsewhere Companion

A digital travel companion who journeys to real places and sends you postcard-like updates.

## Prerequisites

1. **Python 3** must be installed
2. **GEMINI_API_KEY** environment variable must be set (create `data/.env` with `GEMINI_API_KEY=...`)
3. **Python packages**: `google-genai`, `jinja2`, `Pillow`, `python-dotenv` (install via `pip install -r requirements.txt`)

---

## Global Constraints

- **Language**: Always communicate with the user in their language (the language they are using in the current conversation). Do not switch to other languages unless explicitly requested.

---

## Workflow Overview

There are three phases: **Onboarding** → **Trip Planning** → **Traveling** (automated).

---

## Phase 1: Onboarding (First-time setup)

If `data/persona.json` does not exist or has an empty `basic_info.name`, the companion hasn't been created yet. Collect the following information from the user:

1. **name** - the companion's name
2. **relation** - relationship (e.g., childhood friend, penpal, imaginary sibling)
3. **personality** - a few words (e.g., curious, poetic, a little clumsy)
4. **toneOfVoice** - e.g., casual and warm, literary, playful
5. **appearance** - hair, clothing style, vibe description

After collecting all information, create the persona file:

```bash
python -c "
import json, os
os.makedirs('data', exist_ok=True)
persona = {
    'basic_info': {
        'name': '<name>',
        'relation': '<relation>',
        'personality': '<personality>',
        'tone_of_voice': '<toneOfVoice>',
    },
    'appearance': {
        'description': '<appearance>',
        'reference_image_path': './assets/personas/persona_ref.png',
    },
}
with open('data/persona.json', 'w', encoding='utf-8') as f:
    json.dump(persona, f, ensure_ascii=False, indent=2)
print('Persona saved to data/persona.json')
"
```

Then ask the user to upload a reference photo and save it to `assets/personas/persona_ref.png`.

---

## Phase 2: Trip Planning

Ask the user: "Where should **{name}** go next?"

Accept a destination suggestion, then generate the itinerary:

```bash
python $CLAUDE_SKILL_DIR/scripts/generate_itinerary.py <destination> [--origin <city>] [--days <num>]
```

Show the generated itinerary to the user and ask for confirmation. Once confirmed, proceed to Phase 3.

---

## Phase 3: Traveling (Automated)

### Starting the journey

Start the heartbeat loop:

```
/loop 15m !`python $CLAUDE_SKILL_DIR/scripts/run_cron.py`
```

The loop runs `run_cron.py` every 15 minutes. It automatically:
1. Checks the current time against the itinerary timeline
2. Updates node statuses (PENDING → ACTIVE → COMPLETED)
3. Generates text + image content via Gemini (when triggered by the state machine)
4. Renders the appropriate Markdown template
5. Prints the result for delivery

The state machine rules (from `references/state_machine.md`):
- **State transitions** (PENDING→ACTIVE): always triggers a message
- **45-minute interval**: messages are separated by at least 45 minutes
- **Attraction first visit**: always triggers
- **Attraction subsequent visits**: 40% probability for 2nd, 10% for 3rd
- **Max 1 message per cron tick**

### Checking status

```bash
python $CLAUDE_SKILL_DIR/scripts/run_cron.py --check-only
```

### Ending the journey

When all nodes are COMPLETED, stop the loop:

```
/loop stop
```

Tell the user the trip is over and ask if they'd like to plan a new one.

---

## Manual postcard generation

If you need to generate a postcard for a specific node:

```bash
python $CLAUDE_SKILL_DIR/scripts/generate_post.py <node_id>
```

Then render it with the template:

```bash
python $CLAUDE_SKILL_DIR/scripts/render_output.py --context '<json_context>'
```

---

## File reference

- Scripts: `$CLAUDE_SKILL_DIR/scripts/`
- Templates: `$CLAUDE_SKILL_DIR/templates/`
- Runtime data: `data/` (itinerary.json, persona.json)
- Generated images: `assets/generated/`
