[English](README.md) · [中文](README-zh.md)

# Avatar Generator Skill

A skill that generates deterministic pixel-art avatars as SVG from any seed string. Powered by [`@bitmappunks/avatar-generator`](https://www.npmjs.com/package/@bitmappunks/avatar-generator), pinned to version `0.0.5` and invoked via `npx` — no global install required.

> Same seed → same avatar, every time.

## Overview

This skill is applicable to Claude Code, OpenClaw, Hermes Agent, and other LLM-based agent systems that load `SKILL.md`-style skills. It is a plain-file skill with no platform-specific code.

## Installation

**The installation example below uses Claude Code for demonstration. In practice, you can simply hand the repository URL to your agent and let it handle the installation — it's that easy.**

### Option 1: Direct Download

Clone into your agent's skills directory:

```bash
cd ~/.claude/skills
git clone https://github.com/bitmappunks-com/avatar-generator-skill.git bmp-avatar-generator
```

For other agents, substitute the appropriate skills directory (e.g. `~/.openclaw/workspace/skills` for OpenClaw).

### Option 2: ClawHub (when available)

```bash
clawhub install bmp-avatar-generator
```

### Optional: enable the `/gen-avatar` slash command

The repo also ships a slash command at `commands/gen-avatar.md`. Symlink (or copy) it into your agent's commands directory to enable `/gen-avatar <seed> [output-path]`:

```bash
# Claude Code
ln -s ~/.claude/skills/avatar-generator/commands/gen-avatar.md ~/.claude/commands/gen-avatar.md
```

For other agents, substitute the appropriate commands directory. After this, `/gen-avatar alice ./alice.svg` generates the avatar directly — no prose needed.

The skill runs `@bitmappunks/avatar-generator@0.0.5` on demand via `npx`; the first call downloads it into the npx cache, later calls reuse the cache.

## Usage

Once installed, the agent activates this skill when you ask it to generate an avatar from a seed:

- "make an avatar for `user-42` at `/tmp/u42.svg`"
- "generate an avatar for `alice` and save it to `./alice.svg`"
- "create an avatar with seed `hello`"

The agent will call:

```bash
npx -y @bitmappunks/avatar-generator@0.0.5 --out "<path>" --seed "<seed>"
```

If you do not provide a seed, the agent should use the current Unix timestamp (seconds) as the default seed so each run produces a different avatar.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| `seed` | Optional | Any string. Same seed → same avatar. If omitted, default to the current Unix timestamp in seconds so each run differs while still recording the exact seed used. |
| `output path` | Required | Absolute or relative `.svg` path. If you pass a directory, the skill appends `<seed>.svg`. |

## Output

- 24x24 pixel-art SVG.
- For PNG or resized output, convert separately (`rsvg-convert`, `sharp`, ImageMagick, etc.) — this skill does not transcode.

## Version Pinning

The skill locks `@bitmappunks/avatar-generator` to `0.0.5`. This is intentional: avatar output must be reproducible across time and across machines. Upgrading the underlying package can change the visual algorithm, breaking determinism for any previously generated avatar.

Do not change the pin without coordinating with consumers.

## Requirements

- Node.js (any recent LTS)
- `npx` (bundled with npm)

Terminal preview uses the bundled `svg-tui.js` — no extra dependency. Any terminal with 24-bit color support will render it.

## License

MIT — see [LICENSE](LICENSE).

## Author

BitmapPunks · [bitmappunks-com/avatar-generator-skill](https://github.com/bitmappunks-com/avatar-generator-skill)
