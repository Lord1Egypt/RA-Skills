# Illustration Grammar

## Purpose

This module captures the borrowed strength of reference illustration systems: stable scene grammar, repeatable visual beats, and high consistency across a set.

It is a method layer, not a style copy layer.

## Core Principles

1. One image, one primary message.
2. Scene continuity matters more than decorative variety.
3. Consistency comes from a fixed visual grammar, not from repeating the same layout blindly.
4. The illustration should support the content, not compete with it.
5. Do not copy reference composition, character identity, prop arrangement, or signature brushwork.

## Grammar Dimensions

When generating illustration-style pages or illustration-first inline images, declare:

- scene_role: opening / transition / emphasis / closure / atmosphere
- subject_focus: who or what carries the frame
- camera_distance: close / medium / wide
- composition_axis: centered / left-weighted / right-weighted / diagonal / layered
- motion_state: still / walking / turning / reaching / observing
- environment_density: sparse / medium / dense
- palette_temperature: warm / neutral / cool
- line_character: thin / medium / bold / hand-drawn / clean
- texture_level: flat / paper-grain / watercolor / ink / mixed
- text_load: none / very_low / low

## Scene Constraints

- Prefer repeated subjects or recurring scene logic across a set.
- Keep object count limited when the page already contains textual burden.
- Use background variation only when it serves rhythm or narrative.
- Keep small Chinese text out of the image model by default.
- Keep visible objects semantically linked to the source.

## Anti-Patterns

- Random decorative clutter.
- Unstable character proportions.
- Mixing unrelated illustration styles in one set.
- Overly busy backgrounds that fight the copy.
- Generic AI gloss without scene logic.

## Output Fields

When illustration grammar is enabled, each page should expose:

- illustration_grammar_id
- scene_role
- subject_focus
- composition_axis
- camera_distance
- palette_temperature
- texture_level
- text_load
- blocked_mimicry
- prompt_style_phrase
