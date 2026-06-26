---
name: bmp-avatar-generator
version: 0.1.2
description: Generate a deterministic pixel-art avatar SVG from a seed string using the @bitmappunks/avatar-generator npm package (version 0.0.5, run via npx), and save it to a specified file path. Use this whenever the user asks to create, generate, make, or produce an avatar from a seed, name, or ID, including requests like "avatar for user X", "generate an avatar", "make me an avatar", "bitmappunks", or any mention of avatar generation tied to a deterministic input string.
author: BitmapPunks
license: MIT
homepage: https://github.com/bitmappunks-com/avatar-generator-skill
---

# Avatar Generator

> [English](SKILL.md) · [中文](SKILL-zh.md)

Generate a deterministic SVG avatar by running `@bitmappunks/avatar-generator@0.0.5` via `npx`. Same seed → same avatar.

**Version is locked to `0.0.5`.** Do not upgrade or drop the version pin without explicit user instruction.

## Inputs required

1. **seed** — the string that deterministically produces the avatar. Optional: if omitted, default to the current Unix timestamp in seconds so the result changes each time, and report the exact seed used back to the user.
2. **output path** — where the `.svg` file is saved. If the user gave a directory, join it with `<seed>.svg`. If no path was given, default to `./<seed>.svg` in the current working directory and tell the user what path you used.

Ask only if the output path is ambiguous.

## Run

```bash
npx -y @bitmappunks/avatar-generator@0.0.5 --out "<output-path>" --seed "<seed>"
```

- `-y` auto-accepts the npx install prompt.
- The `@0.0.5` pin is required — never run it unpinned (`@latest` or bare).
- Resolve `<seed>` to the user-provided seed, otherwise use the current Unix timestamp in seconds.

## Preview

Render the generated SVG inline in the terminal using the bundled `scripts/svg-tui.js` (resolve its path from this skill's base directory, shown in the skill-load message):

```bash
node "<skill-base-dir>/scripts/svg-tui.js" "<output-path>"
```

It parses the avatar's pixel stripes and prints them as ANSI truecolor blocks — works in any terminal transcript that supports 24-bit color, with no external dependency beyond `node` (already required by `npx`).

## Confirm

Tell the user the absolute output path and the seed. One sentence.

## Notes

- Output is SVG only. For PNG or resizing, convert separately (e.g. `rsvg-convert`, `sharp`) — don't silently change format.
- One seed per invocation. For multiple seeds, loop the command.
- If `npx` errors (network, registry, install), surface the error — don't retry silently or fall back to a different version.
