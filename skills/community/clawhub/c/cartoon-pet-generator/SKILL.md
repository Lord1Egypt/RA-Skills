---
name: cartoon-pet-generator
description: Generate cute cartoon-style pet images (dogs, cats, etc.) using code. Use when user asks for cartoon pet drawings, cute animal illustrations, or simple pet avatars. No AI image API required - generates SVG and converts to PNG using Node.js and rsvg-convert.
---

# Cartoon Pet Generator

Generate adorable cartoon-style pet images programmatically without any AI image generation API.

## What This Skill Does

Creates SVG-based cartoon pets (dogs, cats, rabbits, etc.) and converts them to PNG format. Works entirely with code - no external APIs or image generation services needed.

## Quick Start

### Generate a Cartoon Dog

```bash
node /path/to/scripts/generate_pet.js dog /tmp/dog.png
```

### Generate a Cartoon Cat

```bash
node /path/to/scripts/generate_pet.js cat /tmp/cat.png
```

### Custom Colors

```bash
node /path/to/scripts/generate_pet.js dog /tmp/dog.png --body-color "#FFB347" --ear-color "#FF8C00"
```

## Supported Pets

- `dog` - Cute cartoon dog
- `cat` - Adorable cartoon cat
- `rabbit` - Fluffy cartoon rabbit
- `bear` - Cuddly cartoon bear

## Customization Options

| Option | Description | Example |
|--------|-------------|---------|
| `--body-color` | Main body color | `#D2691E` |
| `--ear-color` | Ear color | `#8B4513` |
| `--bg-color` | Background color | `#87CEEB` |
| `--size` | Image size (width) | `400` |

## How It Works

1. **Generate SVG** - Node.js creates an SVG with the pet design
2. **Convert to PNG** - Uses `rsvg-convert` (or `convert`) to convert SVG → PNG
3. **Output** - Returns the path to the PNG file

## Requirements

- Node.js (for SVG generation)
- `rsvg-convert` or ImageMagick `convert` (for SVG to PNG conversion)

## Example Usage in Conversation

User: "给我画一只小狗"

Response: Run the script and send the image:
```bash
node scripts/generate_pet.js dog /tmp/cute_dog.png
```

Then send with: `<qqimg>/tmp/cute_dog.png</qqimg>`
