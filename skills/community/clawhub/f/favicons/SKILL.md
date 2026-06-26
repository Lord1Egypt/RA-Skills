---
name: favicons
description: Use the favicons Node.js library to generate multi-platform website icons (Favicons).
---

# Favicons

Generate cross-platform website icons using the Node.js `favicons` library.

## Use Cases

Use this skill when the user needs to generate website icons, create a PWA icon set for a website, generate app icons for different platforms (iOS, Android, Windows), or produce a complete icon package including HTML tags and manifest files.

## Installing Dependencies

Ensure `favicons` is installed in the project before execution:

```bash
npm install favicons
```

## Quick Start

```javascript
import { favicons } from "favicons";

const response = await favicons(source, configuration);
```

## Workflow

1. **Confirm Source Image**: Requires a clear app icon source image (recommended 512x512 or larger, supports PNG/SVG)
2. **Configure Options**: Set app name, icon path, platform toggles, etc., as needed
3. **Execute Generation**: Run the script to generate icon files
4. **Output Files**: Obtain image files, configuration files, and HTML tags

## Executing Icon Generation

Use the bundled script to generate icons:

```bash
node <skill-path>/scripts/generate_favicons.js <source-image> <output-directory> <config-JSON>
```

### Example

```bash
# Basic usage
node scripts/generate_favicons.js ./logo.png ./dist

# Full configuration
node scripts/generate_favicons.js ./logo.png ./dist '{
  "appName": "My App",
  "appShortName": "App",
  "background": "#2196F3",
  "icons": {"android": true, "appleIcon": true, "windows": true}
}'
```

## Configuration Reference

For detailed configuration options, refer to [config_reference.md](references/config_reference.md).

### Common Configuration

| Option | Description |
| :--- | :--- |
| `appName` | Application name |
| `appShortName` | Application short name (displayed on desktop) |
| `path` | Icon deployment path prefix |
| `background` | Icon background color |
| `icons.android` | Generate Android icons |
| `icons.appleIcon` | Generate Apple Touch icons |
| `icons.favicons` | Generate generic favicons |

### Disabling Specific Platforms

```javascript
{
  icons: {
    android: false,      // Skip Android icons
    appleStartup: false, // Skip Apple startup images
    yandex: false        // Skip Yandex icons
  }
}
```

## Output Files

The generated directory contains:

- **Image Files**: PNG icons of various sizes
- **Configuration Files**: `manifest.json`, `browserconfig.xml`
- **HTML Tag File**: `favicon-tags.html` (can be directly copied into `<head>`)

## FAQ

**Why are some icons missing?**
Some icons (such as macOS SVG, Windows tile silhouette effects) require additional module support; the project will follow up continuously.

**Generation failed?**
- Ensure the source image exists and is in the correct format
- Check that Node.js version >= 14
- Ensure the `favicons` package is installed correctly