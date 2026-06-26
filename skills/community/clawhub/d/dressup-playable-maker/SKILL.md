---
name: dressup-playable-maker
description: Create dress-up style playable ads for mobile advertising platforms like Mintegral. Use when the user needs to create or customize a fashion dress-up interactive ad with character customization, clothing items, and CTA buttons. Supports template-based generation with customizable assets (character, clothes, background, UI styles).
---

# Dressup Playable Maker

Create interactive dress-up playable ads for mobile advertising platforms.

## Quick Start

Generate a new playable from template:

```bash
python3 scripts/generate.py --input-dir /path/to/assets --output-dir /path/to/output
```

## Required Assets Structure

Input folder should contain:

```
assets/
├── character/
│   ├── body.png          # Base character body
│   ├── hair/
│   │   ├── hair_1.png
│   │   ├── hair_2.png
│   │   └── hair_3.png
│   ├── dress/
│   │   ├── dress_1.png
│   │   ├── dress_2.png
│   │   └── dress_3.png
│   └── shoes/
│       ├── shoes_1.png
│       ├── shoes_2.png
│       └── shoes_3.png
├── background.jpg        # Game background
└── ui/
    ├── button_bg.png     # Selection button background (optional)
    └── hand_cursor.png   # Hand hint cursor (optional)
```

## Customization Options

### Colors
Edit generated `config.js`:
- `primaryColor`: Main theme color
- `buttonBorderColor`: Selected item border color
- `backgroundOverlay`: Background tint

### Layout
Edit generated `style.css`:
- `--character-scale`: Character size (default: 1.1)
- `--button-size`: Selection button size
- `--bottom-spacing`: Distance from buttons to screen bottom

### Categories
Modify `steps` array in `index.html` to change clothing categories:
- Default: `['hair', 'dress', 'shoes']`
- Can add: `['accessory', 'makeup', 'background']`

## Output Structure

```
output/
├── index.html      # Main game file (v57)
├── mraid.js        # MRAID support
└── assets/         # Copied and optimized images
```

## Platform Support

- **Mintegral**: Full support with MRAID 3.0
- **Other platforms**: Generic playable format

## Best Practices

1. **Image sizes**: Keep character parts under 500KB each
2. **Format**: Use PNG for transparency, JPG for backgrounds
3. **Dimensions**: Character parts should align at same canvas size
4. **Testing**: Always test on actual mobile devices

## Version History

- **v57**: Fixed hair/head item selection bug (index mismatch)
- **v56**: Initial version

## Advanced: Manual Customization

For full control, edit the generated `index.html`:

- `defaultHair`, `defaultDress`, `defaultShoes`: Set default outfits
- `gameReady()`, `gameStart()`, `gameEnd()`: Lifecycle hooks
- `window.install()`: CTA button action

## Troubleshooting

**Character parts not aligning**: Ensure all images have same canvas size and anchor point.

**Buttons too small/large**: Adjust `--button-size` in CSS or regenerate with different base size.

**Performance issues**: Reduce image file sizes, limit to 3-4 clothing items per category.

**Selection showing wrong item**: Fixed in v57 - ensure using latest template.
