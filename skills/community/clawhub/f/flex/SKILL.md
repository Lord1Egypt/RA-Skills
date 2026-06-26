---
name: flex
version: "1.0.0"
description: "Generate CSS Flexbox layouts using interactive CLI commands. Use when building responsive flex containers, rows, columns, or alignment configurations."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Flex — CSS Flexbox Layout Generator

A CLI tool for generating CSS Flexbox layouts. Create flex containers, configure alignment, justify, wrap, gap, and order properties, then export production-ready CSS code.

## Prerequisites

- Python 3.8+
- `bash` shell
- Write access to `~/.flex/`

## Data Storage

All layout configurations are stored in JSONL format at `~/.flex/data.jsonl`. Each record represents a saved flex layout with all its properties.

## Commands

Run commands via: `bash scripts/script.sh <command> [arguments...]`

### create

Create a new flex container layout with a name and optional initial properties.

```bash
bash scripts/script.sh create --name "navbar" --direction row --items 5
bash scripts/script.sh create --name "sidebar" --direction column
```

**Arguments:**
- `--name` — Layout name (required)
- `--direction` — Flex direction: `row`, `column`, `row-reverse`, `column-reverse` (optional, default: `row`)
- `--items` — Number of child items (optional, default: 3)

### row

Create a quick horizontal row layout preset.

```bash
bash scripts/script.sh row --name "header-row" --items 4
bash scripts/script.sh row --name "card-grid" --gap 16
```

**Arguments:**
- `--name` — Layout name (required)
- `--items` — Number of items (optional, default: 3)
- `--gap` — Gap in pixels (optional, default: 0)

### column

Create a quick vertical column layout preset.

```bash
bash scripts/script.sh column --name "sidebar-nav" --items 6
```

**Arguments:**
- `--name` — Layout name (required)
- `--items` — Number of items (optional, default: 3)
- `--gap` — Gap in pixels (optional, default: 0)

### wrap

Toggle or set flex-wrap on an existing layout.

```bash
bash scripts/script.sh wrap --id <layout_id> --value wrap
bash scripts/script.sh wrap --id <layout_id> --value nowrap
```

**Arguments:**
- `--id` — Layout ID (required)
- `--value` — Wrap value: `wrap`, `nowrap`, `wrap-reverse` (optional, default: `wrap`)

### align

Set align-items property on a layout.

```bash
bash scripts/script.sh align --id <layout_id> --value center
```

**Arguments:**
- `--id` — Layout ID (required)
- `--value` — Alignment: `flex-start`, `flex-end`, `center`, `stretch`, `baseline` (required)

### justify

Set justify-content property on a layout.

```bash
bash scripts/script.sh justify --id <layout_id> --value space-between
```

**Arguments:**
- `--id` — Layout ID (required)
- `--value` — Justify: `flex-start`, `flex-end`, `center`, `space-between`, `space-around`, `space-evenly` (required)

### gap

Set the gap property on a layout.

```bash
bash scripts/script.sh gap --id <layout_id> --value 16
bash scripts/script.sh gap --id <layout_id> --row 8 --column 16
```

**Arguments:**
- `--id` — Layout ID (required)
- `--value` — Gap in pixels (optional)
- `--row` — Row gap in pixels (optional)
- `--column` — Column gap in pixels (optional)

### order

Set the order of a specific child item within a layout.

```bash
bash scripts/script.sh order --id <layout_id> --item 2 --value -1
```

**Arguments:**
- `--id` — Layout ID (required)
- `--item` — Item index, 1-based (required)
- `--value` — Order value (required)

### grow

Set flex-grow for a child item.

```bash
bash scripts/script.sh grow --id <layout_id> --item 1 --value 2
```

**Arguments:**
- `--id` — Layout ID (required)
- `--item` — Item index (required)
- `--value` — Flex-grow value (required)

### shrink

Set flex-shrink for a child item.

```bash
bash scripts/script.sh shrink --id <layout_id> --item 3 --value 0
```

**Arguments:**
- `--id` — Layout ID (required)
- `--item` — Item index (required)
- `--value` — Flex-shrink value (required)

### export

Export a layout or all layouts as CSS code.

```bash
bash scripts/script.sh export --id <layout_id>
bash scripts/script.sh export --all --output layouts.css
```

**Arguments:**
- `--id` — Export a specific layout (optional)
- `--all` — Export all layouts (optional)
- `--output` — Output file path (optional, default: stdout)

### help

Display help information and list all available commands.

```bash
bash scripts/script.sh help
```

### version

Display the current tool version.

```bash
bash scripts/script.sh version
```

## Examples

```bash
# Create a navigation bar
bash scripts/script.sh create --name "navbar" --direction row --items 5
bash scripts/script.sh justify --id abc123 --value space-between
bash scripts/script.sh align --id abc123 --value center
bash scripts/script.sh export --id abc123

# Quick card grid
bash scripts/script.sh row --name "cards" --items 4 --gap 16
bash scripts/script.sh wrap --id def456 --value wrap

# Export everything
bash scripts/script.sh export --all --output flex-layouts.css
```

## Notes

- Each layout stores complete flex properties: direction, wrap, align, justify, gap, and per-item grow/shrink/order
- The `export` command generates clean, production-ready CSS with class names derived from layout names
- Use `row` and `column` shortcuts for common patterns instead of `create`
- Item properties (grow, shrink, order) are stored per item index within each layout

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
