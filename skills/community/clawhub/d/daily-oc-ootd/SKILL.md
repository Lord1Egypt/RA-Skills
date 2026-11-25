---
name: daily-oc-ootd
description: Generate an original-character outfit-of-the-day phone wallpaper from character and background images supplied for the current invocation. Use for random or specified OC/background selection, autonomous styling, and a short generation log.
metadata: {"version":"0.1.1"}
---

# Daily OC OOTD v0.1

Create one new portrait phone wallpaper using only the character and background references supplied for this invocation. OOTD means outfit of the day; OC means original character. The release version is 0.1.1 (display version v0.1).

## Per-invocation assets

- Do not maintain a persistent character pool or background pool. Do not copy references into this skill, a reusable library, or long-term memory.
- Require the user to supply at least one character image and at least one background image for every invocation. If either category is missing, request the missing images before generating; do not substitute historical assets or invent a missing reference.
- Use only the current invocation's supplied assets. References explicitly attached or linked by the user for this invocation count as current inputs; do not silently retrieve earlier uploads.
- If image roles are ambiguous and cannot be inferred reliably, ask which images are characters and which are backgrounds.
- Temporary processing copies may be used when tools require them, but do not retain them as a reusable asset pool. This policy governs the agent's behavior and does not promise deletion from chat history or provider storage.

## Selection

- Honor specified characters, background, character count, and selection constraints.
- Otherwise, randomly select one character and one background from the eligible current inputs. Use a random-choice facility when available; do not present an aesthetic preference as a random draw.
- For multiple requested characters, select distinct characters without replacement unless the user requests duplicates. Multiple reference images of the same character are one candidate when identifiable.
- If the requested number exceeds the available distinct characters, ask the user to reduce the count or provide additional characters.
- Assign short invocation-local labels, such as Character 1 and Background 2, so the selection can be reported without preserving a library.

## Creative direction

Inspect the selected references. Preserve the character's recognizable facial features, hair or fur, markings, silhouette, species, and essential design traits. Preserve the background's main atmosphere and identifying visual elements while harmonizing perspective, lighting, and style.

Autonomously choose a coherent theme, outfit, accessories, pose, camera angle, composition, and mood. Default to allowing outfit changes while retaining character identity. Honor constraints such as original costume, no anthropomorphizing, cute styling, street photography, or nighttime atmosphere. Adapt styling to nonhuman anatomy rather than changing species by default.

Default to one 9:16 portrait phone wallpaper, or the closest supported portrait ratio. Keep the subject readable, anatomy coherent, and the character integrated with the scene. Leave useful breathing room for a phone clock or interface without obscuring important features. Do not add text or a watermark unless requested.

## Image generation

Use an available image-generation or image-editing tool that accepts reference images. Supply both the selected character and background references, along with the creative direction and user constraints. Follow the tool's supported input and output formats; do not invent a tool name, installation command, API credential, or successful result.

If reference-based image generation is unavailable, explain the missing capability and return a ready-to-use prompt plus the selected reference labels as an explicitly ungenerated fallback. Do not claim that a prompt is a finished wallpaper. If a generation fails, report the failure honestly and respect the tool's retry guidance.

Inspect the result when possible for character identity, background atmosphere, requested count, outfit constraints, and portrait composition. Correct a material mismatch using the same current references when the tool supports it. Disclose any unresolved mismatch.

## Delivery

Return the generated image or a usable image link, followed by a short generation log containing:

- Selected character and background labels, and whether selection was random or specified.
- Theme, outfit, pose, and composition in a few concise phrases.
- Actual aspect ratio or dimensions when known, and any material limitation.

Keep the log separate from the image. Save no reusable character/background catalog. This skill runs on demand; its name does not schedule daily generation or create animation.
