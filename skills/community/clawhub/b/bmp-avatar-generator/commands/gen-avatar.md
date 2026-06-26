---
description: Generate a deterministic pixel-art avatar SVG from a seed string using the bmp-avatar-generator skill.
argument-hint: <seed> [output-path]
---

Use the `bmp-avatar-generator` skill to generate an avatar.

- **seed**: `$1`
- **output path**: `$2` — if empty, default to `./$1.svg` in the current working directory and tell the user the exact path you used.

If `$1` is empty, stop and ask the user for a seed instead of generating a random one.

Do **not** change the pinned package version (`@0.0.5`).

Follow the skill's own steps for generation, terminal preview, and final confirmation — don't hardcode paths to skill-bundled scripts from this command, since commands install globally and the skill resolves its own base directory.