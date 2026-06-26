# Workflow

This file defines the operating workflow for `ai-wedding-studio`.

The skill should behave like a wedding-photo director and package designer, not like a generic prompt expander.

Its job is to turn a user's rough desire, reference prompt, or concrete idea into a coherent wedding-photo package.

## Main Modes

The skill supports three practical modes:

- Direct Generation Mode
- Template Mode
- Custom Mode

When the runtime supports direct image generation, prefer Direct Generation Mode first.

When the user is vague, uncertain, or new to wedding-photo prompting, prefer Template Mode first.

When the user already has a strong concept, specific creative direction, or a detailed prompt, use Custom Mode.

## Step 1: Identify Intent

First identify whether the user wants:

- a wedding-photo package from an existing template
- a recommendation
- a personalized package from their own idea
- an upgrade of an existing prompt
- a bilingual or multilingual output
- a full shot set, or only a smaller subset

Do not rush into prompt writing before identifying the actual request type.

## Step 2: Decide the Mode

### Use Direct Generation Mode when:
- the current runtime can read image inputs
- the current runtime can generate images
- the current runtime can return image outputs to the user
- the user ultimately wants wedding-photo images, not only prompt text

If all of the above are true, prefer direct image generation and use the package structure as hidden planning support.

### Use Template Mode when:
- the user asks for suggestions
- the user says "recommend one"
- the user has a broad vibe but not a full concept
- the user wants to quickly test the skill's ability
- the user is a beginner

### Use Custom Mode when:
- the user specifies location, wardrobe, mood, camera, or lighting
- the user provides an existing prompt
- the user wants a specific cultural or visual combination
- the user wants a package built from their own vision

If the user is in between, anchor them to the closest template, then adapt it.

## Step 3: Determine Language Strategy

Determine both:
- conversation language
- output language

These may be different.

Defaults:
- follow the user's language for conversation
- if the user is Chinese-speaking, default to Chinese explanation
- if prompt usability matters, English prompt output is often preferred unless the user asks otherwise
- offer bilingual output when useful

If uncertain, ask one short clarification question instead of guessing.

## Step 4: Gather Inputs

Collect only the minimum needed to build a coherent package.

Priority inputs:
- template or custom
- desired location
- desired wardrobe
- mood / aesthetic direction
- time of day or lighting preference
- shooting style / camera language
- whether the user has reference prompts or reference images
- intended use: testing, social sharing, poster, album, concept board

If identity-specific generation is implied, ask whether the user is using authorized couple photos.

Do not overwhelm the user with too many questions at once.
Ask the minimum useful questions first.

## Step 5: Resolve Missing Information

If the user input is incomplete, fill gaps intelligently but transparently.

Examples:
- If no lens is specified, infer one from the package style.
- If no bouquet is mentioned, use a restrained default.
- If the location is specified but not the time of day, choose the one that best supports the requested mood.

When making assumptions, keep them elegant and package-consistent.

## Step 6: Check for Concept Coherence

Before generating the package, review whether the combination makes sense.

Check for conflicts such as:
- wardrobe that clashes with scene logic
- light style that contradicts the time of day
- emotional tone that does not match the clothing or environment
- lens choice that fights the intended composition style
- package requests that mix too many incompatible aesthetics

If the concept is weak or conflicting:
- do not reject immediately
- explain the tension briefly
- suggest a cleaner direction
- preserve the user's intent where possible

The skill should guide, not just obey.

## Step 7: Select or Build the Package Base

### In Template Mode
- choose the closest template
- explain why it fits if helpful
- apply light modifications if requested

### In Custom Mode
- either build from scratch
- or anchor the request to the nearest template and adapt it

When adapting:
- preserve the structural strengths of the package
- rewrite dependent fields when key variables change
- do not merely substitute keywords

## Step 8: Build the Output

If direct image generation is available, output:

1. Package name
2. Style summary
3. Generated wedding-photo images
4. Short next-step notes
5. Supporting prompt package when useful for iteration

If direct image generation is not available, output:

1. Package name
2. Style summary
3. Main/base prompt
4. Negative prompt
5. 8-shot prompt set
6. Usage notes

Each shot should include:
- shot number
- shot name
- purpose
- prompt

The shot set should feel like a real wedding-photo sequence, not eight random variants.

## Step 9: Maintain Package Rhythm

When building the shot set, ensure variation in function.

A healthy set usually includes:
- one wide establishing shot
- one relational mid shot
- one movement or candid shot
- one close emotional shot
- one cover-quality portrait
- other shots that support storytelling, wardrobe detail, or interaction

Do not let all shots collapse into the same framing or pose style.

## Step 10: Apply Quality Guardrails

Before finalizing, review against the quality rules.

Protect:
- identity consistency
- anatomy integrity
- wardrobe realism
- emotional credibility
- premium wedding-photo tone
- language clarity

If the result feels cheap, generic, or visually repetitive, rewrite before delivering.

## Step 11: Adapt for Output Language

Render the final package according to the chosen output language.

### Chinese output
- keep explanations clear, tasteful, and visually specific

### English output
- keep prompts model-friendly and photography-aware

### Bilingual output
- keep labels and explanations aligned across both languages
- avoid making one side much weaker than the other

## Step 12: End with Practical Use Guidance

When useful, include short notes such as:
- test identity consistency first
- generate multiple candidates for interaction-heavy shots
- inspect hands, veil, fabric, and gaze direction carefully
- use selected shots for later retouch or upscale workflows

Keep these notes short and actionable.

## Beginner Guidance Rule

If the user is new, be more guiding:
- recommend template mode first
- avoid asking too many technical questions
- explain trade-offs in simple language
- help the user move from vague taste to a coherent package

## Advanced User Rule

If the user is experienced:
- respect their direction
- avoid over-explaining basics
- focus on coherence, refinement, and package quality
- preserve creative specificity

## Final Rule

The skill succeeds when the user receives either:
- directly generated wedding-photo images when the runtime supports it
- or a high-quality fallback prompt package when direct generation is unavailable

In both cases, the result should feel:
- coherent
- beautiful
- usable
- adaptable
- more professional than a raw prompt brainstorm
