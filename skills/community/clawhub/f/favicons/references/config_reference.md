# Favicons Configuration Reference

## Complete Configuration Options

| Option | Type/Default | Description |
| :--- | :--- | :--- |
| `path` | `string` | Path where icons will be stored on the server |
| `appName` | `string`| null` | Application name |
| `appShortName` | `string`| null` | Application short name; falls back to `appName` if not set |
| `appDescription` | `string`| null` | Application description |
| `developerName` | `string`| null` | Developer name |
| `developerURL` | `string`| null` | Developer URL |
| `dir` | `"auto"` | Text direction (`auto`, `ltr`, `rtl`) |
| `lang` | `"en-US"` | Language setting |
| `background` | `"#fff"` | Background color for flattened icons |
| `theme_color` | `"#fff"` | Theme color |
| `appleStatusBarStyle` | `"black-translucent"` | iOS status bar style |
| `display` | `"standalone"` | Preferred display mode |
| `orientation` | `"any"` | Default screen orientation |
| `scope` | `"/"` | Navigation scope of the application |
| `start_url` | `"/?homescreen=1"` | Start URL when launched from device |
| `version` | `"1.0"` | Application version number |
| `pixel_art` | `false` | Whether to preserve sharp edges for pixel art |
| `manifestMaskable` | `false` | Whether to generate maskable icons |
| `loadManifestWithCredentials` | `false` | Whether to request manifest file with credentials |

## Icon Platform Toggles

| Option | Type | Description |
| :--- | :--- | :--- |
| `android` | `boolean` or object | Android home screen icons |
| `appleIcon` | `boolean` or object | Apple Touch icons |
| `appleStartup` | `boolean` or object | Apple startup images |
| `favicons` | `boolean` or object | Generic favicons |
| `windows` | `boolean` or object | Windows 8 tile icons |
| `yandex` | `boolean` or object | Yandex browser icons |

Options supported by platform objects:
- `offset`: Percentage offset
- `background`: Background handling method

## Shortcuts Configuration

```javascript
shortcuts: [
  {
    name: "View Inbox",
    short_name: "Inbox",
    description: "View inbox messages",
    url: "/inbox",
    icon: "test/inbox_shortcut.png"
  }
]
```

## Output File Manifest

### response.images
Array of image file buffers to be written:
- **Android**: 9 sizes ranging from `android-chrome-36x36.png` to `android-chrome-512x512.png`
- **Apple Icon**: 13 files ranging from `apple-touch-icon-57x57.png` to `apple-touch-icon-1024x1024.png`
- **Apple Startup Images**: 30 sizes covering resolutions for various iPhone/iPad generations
- **Favicons**: `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `favicon.ico`
- **Windows**: 5 sizes ranging from `mstile-70x70.png` to `mstile-310x310.png`
- **Yandex**: `yandex-browser-50x50.png`

### response.files
Configuration files to be written:
- `manifest.json` - Web App Manifest
- `browserconfig.xml` - Windows tile configuration

### response.html
Array of tag strings to be inserted into the HTML `<head>`

## Accessing Default Configuration Programmatically

```javascript
import { config } from 'favicons';

// Access default configuration
console.log(config);
```