# Package Schema

This file defines the standard structure for a wedding-photo package used by `ai-wedding-studio`.

A package is not just a prompt. It is a reusable wedding-photo blueprint that describes:
- who the couple is
- what they wear
- where the scene happens
- how the scene should feel
- how the camera should see it
- which shots belong to the set
- what quality and consistency rules must be preserved

Use this schema when creating a new package or adapting an existing one.

## Design Principle

Every package should be:
- cohesive
- editable
- reusable
- easy to adapt
- strong enough to generate a full multi-shot set

A package should describe a complete wedding-photo concept, not a single isolated image.

## Required Top-Level Fields

Each package should include these top-level fields:

- `id`
- `name_zh`
- `name_en`
- `category`
- `summary`
- `subject_profile`
- `wardrobe`
- `location`
- `time_and_light`
- `camera_language`
- `mood_keywords`
- `global_constraints`
- `base_prompt`
- `negative_prompt`
- `frames`

## Field Reference

### `id`

A stable machine-friendly package identifier.

Example:
- `dali_sunrise_wedding`
- `beach_sunset_wedding`
- `han_style_studio_white`

Use lowercase snake_case.

### `name_zh`

Chinese display name for the package.

### `name_en`

English display name for the package.

### `category`

Broad package type.

Suggested values:
- `outdoor_wedding`
- `studio_wedding`
- `chinese_traditional_wedding`
- `editorial_wedding`
- `casual_couple_portrait`

### `summary`

A short description of the package concept, visual identity, and typical use cases.

Keep it concise but specific.

### `subject_profile`

Describe the intended couple profile and identity-preservation rules.

Recommended subfields:
- `ethnicity`
- `age_range`
- `identity_rules`

Use `identity_rules` to preserve realism and prevent prompt drift.

Example concerns:
- preserve facial identity
- preserve age feeling
- avoid over-stylized beauty changes
- keep cross-shot consistency

### `wardrobe`

Describe wardrobe and styling.

Recommended subfields:
- `bride`
- `groom`

Each side may include:
- dress / suit
- veil / accessories
- styling notes

Wardrobe should be concrete enough to keep the series visually coherent.

### `location`

Describe the setting.

Recommended subfields:
- `country`
- `province` or `region`
- `city`
- `spot`
- `foreground`
- `midground`
- `background`

This should support both realism and image composition.

### `time_and_light`

Describe time of day, key lighting effect, tone, and color temperature.

Recommended subfields:
- `time`
- `effect`
- `lighting`
- `color_temperature`
- `tone`

This field is one of the strongest drivers of visual consistency.

### `camera_language`

Describe how the scene should be photographed.

Recommended subfields:
- `camera_body`
- `lens`
- `composition`
- `image_style`

This should capture the intended photographic logic, not just random camera jargon.

### `mood_keywords`

A short keyword list that defines the emotional and aesthetic direction.

Examples:
- romantic
- airy
- elegant
- cinematic
- documentary
- intimate
- ceremonial

Keep the list focused.

### `global_constraints`

Non-negotiable quality rules for the whole package.

These should protect:
- identity consistency
- wardrobe integrity
- realistic anatomy
- emotional tone
- wedding-photo quality level

Use this field for package-wide guardrails, not shot-specific details.

### `base_prompt`

The main prompt that establishes the unified world of the package.

This prompt should define:
- subjects
- styling
- scene
- mood
- light
- camera style
- realism expectations

Each shot prompt should build on this base rather than replace it.

### `negative_prompt`

The package-wide negative prompt.

Include recurring failure modes such as:
- bad hands
- face asymmetry
- dress distortion
- pose stiffness
- cheap-looking output
- over-smoothed skin
- anatomy errors

### `frames`

A list of shot definitions for the package.

Each frame should include:
- `id`
- `name`
- `purpose`
- `prompt`

This is the heart of the package.

## Frame Design Rules

A strong package should include a mix of shot functions, not repeated variants of the same image.

A typical 8-shot set may include:
- wide master shot
- mid interaction shot
- bride-led shot
- groom-led or bouquet interaction shot
- emotional close-up
- motion/candid shot
- back-view narrative shot
- cover portrait shot

Each frame should do a different job.

Avoid:
- eight nearly identical poses
- only face-close shots
- only wide scenic shots
- conflicting emotional tones within one package

## Editable Fields

Packages should support adaptation, but not every field should be equally flexible.

Commonly editable fields:
- location
- wardrobe
- bouquet or props
- time of day
- lens style
- mood direction

When these change, dependent fields should also be reviewed.

## Adaptation Principle

Do not swap variables blindly.

When a key field changes, rewrite dependent parts such as:
- foreground/background description
- pose language
- emotional tone
- framing strategy
- light description
- texture emphasis

Example:
Changing from mountain sunrise to beach sunset should affect more than the location line.

## Language Principle

Packages should be usable in:
- Chinese workflows
- English workflows
- bilingual workflows

Package metadata may be bilingual, but prompt text should be optimized for the intended output language.

## Recommended Optional Fields

You may also include these when useful:
- `status`
- `use_cases`
- `props`
- `internal_group`
- `output_notes`
- `retouch_notes`
- `adaptation_rules`

Use optional fields only when they improve reuse or clarity.

## Minimal Example

```yaml
id: beach_sunset_wedding
name_zh: 海边黄昏婚纱照
name_en: Beach Sunset Wedding
category: outdoor_wedding
summary: Sunset beach wedding package with soft wind, warm glow, and natural romantic movement.
subject_profile:
  ethnicity: Chinese couple
  age_range: 25-30
  identity_rules:
    - preserve facial identity
    - keep cross-shot consistency
wardrobe:
  bride:
    dress: white satin mermaid wedding dress
  groom:
    suit: ivory suit
location:
  country: China
  city: Sanya
  foreground: wet sand
  background: sea and sunset sky
time_and_light:
  time: sunset
  lighting:
    - warm side backlight
camera_language:
  lens: 50mm
mood_keywords:
  - romantic
  - free
  - luminous
global_constraints:
  - avoid stiff posing
  - preserve fabric detail
base_prompt: >
  A Chinese couple in wedding attire at sunset on the beach...
negative_prompt: >
  extra fingers, blurry face, warped dress...
frames:
  - id: wide_master
    name: Wide master shot
    purpose: Establish the environment
    prompt: >
      Full-body wide shot on the beach at sunset...
```

## Final Rule

If a package feels like a single long prompt, it is too weak.

A real package should feel like a reusable wedding-photo system.
