---
version: "1.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
description: "Generate CSS and SVG animation code snippets using bash and Python. Use when building UI animations, keyframes, or transition effects."
---

# Animation — CSS/SVG Animation Code Generator

Generate production-ready CSS keyframe animations, SVG motion paths, transitions, and easing functions from the command line. Animations are stored locally in JSONL format for reuse, chaining, and export.

## Prerequisites

- Python 3.6+
- Bash 4+

## Data Storage

All animation records are persisted to `~/.animation/data.jsonl`. Each record is a JSON object with fields like `id`, `name`, `type`, `code`, `created_at`, etc.

## Commands

Run via: `bash scripts/script.sh <command> [options]`

| Command | Description |
|---|---|
| `create` | Create a new CSS or SVG animation definition |
| `keyframe` | Generate a `@keyframes` block with named steps |
| `transition` | Generate a CSS transition shorthand snippet |
| `timing` | Show or set timing-function values for an animation |
| `easing` | List built-in easing curves or define a custom cubic-bezier |
| `sequence` | Build a multi-step animation sequence from existing entries |
| `loop` | Set loop/iteration count for an animation |
| `chain` | Chain two or more animations with configurable delays |
| `export` | Export one or all animations as a `.css` / `.svg` file |
| `preview` | Generate an HTML preview page for a given animation |
| `list` | List all stored animations |
| `help` | Show usage information |
| `version` | Print the tool version |

## Usage Examples

```bash
# Create a fade-in animation
bash scripts/script.sh create --name fadeIn --type css --property opacity --from 0 --to 1 --duration 0.5s

# Generate keyframes
bash scripts/script.sh keyframe --name bounce --steps '0%:translateY(0);50%:translateY(-20px);100%:translateY(0)'

# Create a transition
bash scripts/script.sh transition --property transform --duration 0.3s --easing ease-in-out

# List all saved animations
bash scripts/script.sh list

# Preview an animation in HTML
bash scripts/script.sh preview --name fadeIn

# Export animations to a CSS file
bash scripts/script.sh export --name fadeIn --format css --output animations.css

# Chain two animations
bash scripts/script.sh chain --names fadeIn,bounce --delay 0.2s

# Show available easing functions
bash scripts/script.sh easing --list

# Set loop count
bash scripts/script.sh loop --name bounce --count infinite

# Build a multi-step sequence
bash scripts/script.sh sequence --names fadeIn,bounce --mode sequential
```

## Output Format

All commands output to stdout. Structured data is returned as JSON. Generated code is printed as raw CSS or SVG text suitable for copy-paste or piping.

## Notes

- Animation IDs are auto-generated UUIDs.
- The `preview` command creates a self-contained HTML file that can be opened in any browser.
- `chain` and `sequence` reference animations by name; they must exist in the data store.
- `export --format svg` wraps animations in an `<svg>` + `<animate>` / `<animateTransform>` structure.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
