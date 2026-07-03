# HyperFrames Composition Rules — Full Reference

## Root Composition Structure (index.html)

```html
<!doctype html>
<html>
<body>
  <div data-composition-id="main" data-start="0"
       data-width="1920" data-height="1080">
    <!-- clips here -->
  </div>
</body>
</html>
```

**IMPORTANT**: Standalone compositions (index.html) put `data-composition-id` div directly in `<body>`. Do NOT use `<template>` on standalone files — it hides content and breaks rendering.

## Data Attributes — Complete Reference

### All Clips

| Attribute | Required | Values |
|-----------|----------|--------|
| `id` | Yes | Unique identifier |
| `data-start` | Yes | Seconds or clip ID reference (`"el-1"`, `"intro + 2"`) |
| `data-duration` | Required for img/div/compositions | Seconds. Video/audio auto-detects from media. |
| `data-track-index` | Yes | Integer. Same-track clips CANNOT overlap. |
| `data-media-start` | No | Trim offset into source (seconds) |
| `data-volume` | No | 0-1 (default 1) |

`data-track-index` does NOT affect visual layering — use CSS `z-index` for stacking.

### Composition Clips

| Attribute | Required | Values |
|-----------|----------|--------|
| `data-composition-id` | Yes | Unique composition ID |
| `data-start` | Yes | Start time (root: use `"0"`) |
| `data-duration` | Yes | Takes precedence over GSAP timeline duration |
| `data-width` / `data-height` | Yes | Pixel dimensions |
| `data-composition-src` | No | Path to external HTML file |
| `data-variable-values` | No | JSON object of per-instance variable overrides |

### On Root `<html>` Element

| Attribute | Required | Values |
|-----------|----------|--------|
| `data-composition-variables` | No | JSON array of declared variables |

## Track Rules

- Same-track clips CANNOT overlap in time
- `data-track-index` is for the framework's time sequencing, NOT visual z-order
- Visual layering → use CSS `z-index`
- Track indices are integers starting from 0

## Video and Audio — Hard Rules

1. Video elements MUST have `muted playsinline`
2. Audio is ALWAYS a separate `<audio>` element
3. Never nest video inside a timed div — use a non-timed wrapper
4. Never call `play()`/`pause()`/`seek()` on media — framework owns playback
5. Never animate video element dimensions — animate a wrapper div

```html
<!-- CORRECT -->
<video id="v1" data-start="0" data-duration="10" data-track-index="0"
       src="clip.mp4" muted playsinline></video>
<audio id="a1" data-start="0" data-duration="10" data-track-index="2"
       data-volume="0.8" src="clip.mp4"></audio>

<!-- WRONG — never combine video and audio -->
<video src="clip.mp4" data-start="0" data-duration="10" data-track-index="0"></video>
```

## Sub-Composition Format

Sub-compositions use `<template>` wrapper:

```html
<template id="scene-intro-template">
  <div data-composition-id="scene-intro" data-width="1920" data-height="1080">
    <!-- content -->
    <style>
      [data-composition-id="scene-intro"] { /* scoped styles */ }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // tweens...
      window.__timelines["scene-intro"] = tl;
    </script>
  </div>
</template>
```

Load in root composition:
```html
<div id="el-intro" data-composition-id="scene-intro"
     data-composition-src="compositions/intro.html"
     data-start="0" data-duration="5" data-track-index="1"></div>
```

Framework auto-nests sub-timelines — do NOT manually add them.

## Variables — Parametrized Compositions

### Declare (on `<html>` root)

```html
<html data-composition-variables='[
  {"id":"title","type":"string","label":"Title","default":"Hello World"},
  {"id":"accent","type":"color","label":"Accent","default":"#ff6b35"},
  {"id":"speed","type":"number","label":"Speed","default":1.0},
  {"id":"show_logo","type":"boolean","label":"Show Logo","default":true},
  {"id":"theme","type":"enum","label":"Theme","default":"dark","options":[
    {"value":"dark","label":"Dark"},
    {"value":"light","label":"Light"}
  ]}
]'>
```

### Read (in composition script)

```javascript
const { title, accent, speed, show_logo, theme } = window.__hyperframes.getVariables();
```

### Override at render time

```bash
npx hyperframes render --variables '{"title":"New Title","theme":"light"}'
npx hyperframes render --variables-file ./vars.json
npx hyperframes render --strict-variables  # Fail on undeclared keys
```

### Per-instance overrides (sub-compositions)

```html
<div data-composition-id="card-1" data-composition-src="compositions/card.html"
     data-variable-values='{"title":"Pro","price":"$29"}'></div>
<div data-composition-id="card-2" data-composition-src="compositions/card.html"
     data-variable-values='{"title":"Enterprise","price":"Custom"}'></div>
```

## Common Dimensions

| Use Case | Width | Height |
|----------|-------|--------|
| Standard landscape (YouTube, product) | 1920 | 1080 |
| Vertical (TikTok, Reels, Stories) | 1080 | 1920 |
| Square (Instagram feed) | 1080 | 1080 |

## File Organization

All files live at the project root alongside `index.html`:
```
my-video/
├── index.html              # Root composition
├── compositions/           # Sub-compositions
│   ├── intro.html
│   └── outro.html
├── fonts/                  # Custom .woff2 fonts
├── renders/                # Output MP4s (auto-created)
├── transcript.json         # From transcribe command
├── narration.wav           # From TTS
├── background.mp4          # Media assets
└── music.wav
```

Sub-compositions use `../` to reference root-level assets.
