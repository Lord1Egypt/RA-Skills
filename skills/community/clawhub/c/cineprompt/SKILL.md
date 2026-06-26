# CinePrompt Skill

AI video prompt builder for cinematographers. Translates natural language shot descriptions into structured prompts optimized for AI video generators.

## What It Does

CinePrompt turns vague ideas ("cinematic sunset over mountains") into precise cinematography prompts with lens, movement, lighting, color science, sound design, and 133 total fields. Three workflow modes, 24 generation models, 8 model optimizers.

**Live:** https://cineprompt.io
**Guides:** https://cineprompt.io/guides (18+ articles, daily additions)
**Models:** https://cineprompt.io/models

## CLI Usage

```bash
# Install
npm install -g cineprompt

# Auth (Pro subscription required for API)
cineprompt auth cp_your_key_here

# Build a share link from state JSON
cineprompt build '{"mode":"single","subjectType":"character","fields":{...}}'

# Build from file
cineprompt build --file shot.json

# Pipe JSON
cat shot.json | cineprompt build

# List all 133 fields
cineprompt fields

# Show values for a specific field
cineprompt fields mood
cineprompt fields movement_type
```

## Building State JSON

The agent constructs a state object and passes it to the CLI. The CLI creates a share link on cineprompt.io where the user can view, tweak, and copy the prompt.

### State Structure

```json
{
  "mode": "single",
  "complexity": "complex",
  "subjectType": "character",
  "fields": {
    "media_type": ["cinematic"],
    "mood": ["contemplative"],
    "genre": ["drama"],
    "setting": "interior",
    "location_type": ["apartment"],
    "custom_location": "A cluttered one-bedroom with peeling wallpaper",
    "env_time": "night",
    "char_label": "A retired boxer",
    "subject_description": "Weathered face, broken nose, calloused hands",
    "expression": "quietly resigned",
    "wardrobe": "Stained white undershirt, suspenders hanging at sides",
    "action_primary": "sitting alone at a kitchen table",
    "shot_type": "medium close-up",
    "framing": ["positioned left-third of frame"],
    "focal_length": "85mm",
    "dof": "shallow depth of field, bokeh",
    "movement_type": ["static, locked-off"],
    "lighting_type": ["practical lights"],
    "key_light": "Single bare bulb overhead, slightly swinging",
    "film_stock": ["Kodak Vision3 500T 5219"],
    "color_grade": ["desaturated"],
    "sfx_environment": ["room tone"],
    "ambient": "Refrigerator hum, distant sirens",
    "props": "Half-empty whiskey bottle, old photograph face-down"
  }
}
```

### Key Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `mode` | `single`, `multi_shot` | Single shot or multi-shot sequence |
| `complexity` | `simple`, `complex` | Simple = curated fields, Complex = all fields |
| `subjectType` | `character`, `creature`, `object`, `vehicle`, `landscape`, `abstract` | Unlocks subject-specific fields |

### Field Types

**Button fields** (93) — accept arrays of predefined values. Use `cineprompt fields <name>` to see valid options.
```json
"media_type": ["cinematic"],
"mood": ["nostalgic", "contemplative"],
"shot_type": "extreme close-up"
```

**Text fields** (40) — accept free-form strings.
```json
"char_label": "A young street musician",
"subject_description": "Dark curly hair, paint-stained fingers",
"dialogue": "I never said goodbye",
"ambient": "Rain on a tin roof, distant thunder"
```

### Modes

**Single Shot** — one shot, full cinematography control.

**Multi-Shot** — sequence of shots with global settings + per-shot overrides. Supports recurring characters, transitions between shots.
```json
{
  "mode": "multi_shot",
  "complexity": "complex",
  "fields": {
    "media_type": ["cinematic"],
    "mood": ["tense"]
  },
  "shots": [
    {
      "subjectType": "character",
      "fields": {
        "shot_type": "establishing shot",
        "char_label": "Detective",
        "action_primary": "approaching the building"
      }
    },
    {
      "subjectType": "character",
      "fields": {
        "shot_type": "close-up",
        "char_label": "Detective",
        "expression": "steeling herself",
        "action_primary": "reaching for the door handle"
      }
    }
  ]
}
```

**Frame → Motion** — dual-prompt output for img2vid workflows. Build the frame (image prompt), then direct the motion (video prompt). The FM tab uses direct-edit motion text with quick-insert chips:

- **Camera chips:** Slow push in, Slow pull out, Orbit, Dolly, Crane up/down, Handheld, Tracking, Locked off
- **Pacing chips:** Slow motion, Real-time, Time-lapse, Hyperlapse
- **Transition chips:** Whip pan, Steadicam, Rack focus, Reveal, Morph, Dissolve
- **Direction chips:** Slow Build, One at a Time, Breathe, Anchor, Physics, Chaos, Match

## Key Fields Reference

### Core (always relevant)
`media_type`, `mood`, `genre`, `setting`, `location_type`, `custom_location`, `env_time`, `weather`

### Subject — Character
`char_label`, `subject_description`, `expression`, `body_language`, `age_range`, `build`, `hair_style`, `hair_color`, `skin_tones`, `wardrobe`, `action_primary`, `props`

### Subject — Creature
`creature_label`, `creature_description`, `creature_category`, `creature_size`, `creature_body`, `creature_skin`, `creature_expression`

### Subject — Object
`obj_description`, `obj_material`, `obj_condition`, `obj_scale`

### Subject — Vehicle
`veh_description`, `veh_type`, `veh_era`, `veh_condition`

### Subject — Landscape
`land_scale`, `land_season`

### Subject — Abstract
`abs_description`, `abs_quality`, `abs_movement`, `abstract_environment`

### Camera & Lens
`shot_type`, `framing`, `focal_length`, `camera_body`, `lens_brand`, `lens_filter`, `dof`, `movement_type`, `pacing`

### Lighting
`lighting_type`, `lighting_style`, `key_light`, `fill_light`

### Color & Look
`color_grade`, `color_science`, `film_stock`, `palette_colors`

### Environment
`location`, `env_bg`, `env_mg`, `env_fg`

### Sound
`dialogue`, `dialogue_character`, `dialogue_language`, `delivery_style`, `delivery_style_custom`, `voiceover_text`, `music`, `music_genre`, `music_mood`, `ambient`, `sfx_environment`, `sfx_interior`, `sfx_dramatic`, `sfx_mechanical`, `beat_1`, `beat_2`, `beat_3`

### Style
`animation_style`, `documentary_style`, `commercial_type`, `music_video_style`, `social_media_style`, `format`

## Scene-to-Prompt

CinePrompt also accepts natural language descriptions via the Scene-to-Prompt feature. Users type a shot description and an LLM auto-populates all fields. The agent can use this as an alternative to manually constructing state JSON — just direct users to the text box at the top of the page.

## Generate

CinePrompt includes built-in generation with BYOK (bring your own key) across 24 models:
- **Text-to-video (9):** Kling O3 Pro, Sora 2 Pro, Veo 3.1, WAN 2.6, Seedance 1.5 Pro, LTX 2.3, Grok Imagine (Fal + Venice)
- **Image-to-video (5):** Kling O3 Pro, Sora 2 Pro, Veo 3.1, WAN 2.6, LTX 2.3, Grok Imagine
- **Reference-to-video (1):** Kling O3 Pro R2V (character elements)
- **Image gen (4):** Nano Banana Pro, NB2, Chroma, Grok Imagine
- **Image edit (4):** NBP Edit, NB2 Edit, Grok Imagine Edit, Qwen Edit
- **Providers:** Fal.ai + Venice.ai

## Subject Library

Persistent character/element system. Users save subjects with frontal + reference images and field state. Subjects auto-inject into prompts and enable R2V (reference-to-video) generation with Kling Elements.

## Internal Scripts

### cineprompt-x-post
Daily cron (8:55 AM) that reads today's guide article, finds a trending AI video post on X, and writes a quote-tweet mini-essay for the CinePrompt Discord channel. Output goes to Discord for Tylios to post.

### create-share-link.js
Creates share links via Supabase RPC (with API key) or direct insert (with service key). Used internally by the CLI and agent.

## Tiers

| Tier | Price | Access |
|------|-------|--------|
| Free | $0 | Simple mode only |
| Pro | $7/mo or $70/yr | All modes + API key + Generate |
| Founding | $25 lifetime | Everything (capped at 100) |
