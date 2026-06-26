# AgentSaaS Video Editor Skill

A comprehensive video editing and rendering skill that enables AI agents to create code-driven animations with text-to-speech narration and smooth transitions.

## Purpose

This skill allows agents to:
- Create and preview interactive video projects with animations
- Generate TTS audio narration using Microsoft Edge TTS
- Render complete videos with synchronized audio and visual effects
- Support both portrait and landscape video formats
- Apply smooth transition effects between media elements

## Core Capabilities

### 1. Interactive Video Preview
- Real-time preview of video projects in the browser
- Playback controls for testing and debugging
- Support for transitions, media clips, and timing adjustments
- Frame-by-frame seeking for precise editing
- Live transition preview with easing effects

### 2. Transition System
- **transitionIn**: Each media defines its own entrance animation
- **Supported transitions**: fade, zoom, slide2Left, slideUp, none
- **Easing**: Built-in easeOutCubic for smooth slide and zoom animations
- **stayInClip**: Media can persist throughout entire clip duration
- **Cross-clip transitions**: Automatic handling of clip boundaries

### 3. TTS Audio Generation
- Automated text-to-speech using Microsoft Edge TTS (msedge-tts)
- Support for multiple voices (English and Chinese)
- Word-level timing metadata for lip-sync and animations
- Audio file caching for faster previews

### 4. Video Rendering
- Automated frame-by-frame rendering using Puppeteer
- FFmpeg integration for video encoding and audio mixing
- 30 FPS output at 1920x1080 (landscape) or 1080x1920 (portrait)
- Deterministic rendering for consistent results
- Transition effects preserved in final output

## Project Configuration Format

### Media Item Properties
- **src**: HTML filename in the footage directory
- **words**: Trigger phrase from speech that activates this media
- **transitionIn**: Entrance animation type (optional)
- **transitionDuration**: Duration in seconds (optional, default: 0.6s)
- **stayInClip**: If true, media remains visible until clip ends (optional)

### Transition Types
- **fade**: Opacity transition (0 → 1)
- **zoom**: Scale transition (2x → 1x) with opacity
- **slide2Left**: Horizontal slide from right (100% → 0%)
- **slideUp**: Vertical slide from bottom (100% → 0%)
- **none**: No transition effect

### Transition Behavior
- **transitionIn**: Defines how this media enters the scene
- **transitionDuration**: Duration in seconds (default: 0.6s)
- **stayInClip**: If true, media remains visible until clip ends
- **Easing**: slide2Left and slideUp use easeOutCubic for smooth deceleration

### Reference Implementation
See `public/projects/agentSaasPromoVideo.json` for a complete working example demonstrating all transition types and stayInClip behavior.

## Technical Requirements

### System Dependencies
- **Node.js**: 18 or higher
- **FFmpeg**: Required for video encoding and audio mixing
- **Chromium/Chrome**: Used by Puppeteer for headless rendering

### Node.js Dependencies
- **React & Vite**: Frontend framework and build tool
- **Puppeteer**: Headless browser for frame capture
- **msedge-tts**: Microsoft Edge TTS for audio generation
- **Express**: Optional HTTP server (for TTS API endpoint)
- **Motion (Framer Motion)**: Animation library
- **Tailwind CSS**: Styling framework

## Shell Commands Used

This skill executes the following shell commands:

### Audio Generation
```bash
npx tsx scripts/generate-audio.ts <projectId>
```
- Reads project JSON configuration
- Generates MP3 audio files using Edge TTS
- Saves word-level timing metadata

### Video Rendering
```bash
node scripts/render.js <projectId> [--portrait]
```
- Starts a local Vite dev server
- Launches Puppeteer to capture frames
- Uses FFmpeg to encode video and mix audio
- Cleans up temporary files

### FFmpeg Operations
- Frame encoding: `ffmpeg -framerate 30 -i frames/frame-%05d.jpg -c:v libx264 ...`
- Audio mixing: `ffmpeg -i video.mp4 -i audio1.mp3 -i audio2.mp3 -filter_complex ...`

### Browser Detection
- Uses `which` command to find Chrome/Chromium on Linux/macOS
- Respects `PUPPETEER_EXECUTABLE_PATH` environment variable

## API Endpoints (Optional)

The skill may expose an HTTP endpoint for TTS generation:

```
POST /api/tts
Content-Type: application/json

{
  "text": "Text to speak",
  "voice": "en-US-GuyNeural",
  "rate": "+0%",
  "pitch": "+0Hz"
}
```

This endpoint is optional and only used when pre-generated audio files are not available.

## Security Considerations

### File System Access
- Reads from: `public/projects/<projectId>/`
- Writes to: `public/projects/<projectId>/audio/`, `public/video/`
- Creates temporary directories for frame storage
- Cleans up temporary files after rendering

### Network Access
- Starts local HTTP server on port 5175+ (configurable)
- Connects to Microsoft Edge TTS service (external)
- No external API keys required for basic functionality

### Process Execution
- Spawns child processes for: Vite dev server, FFmpeg encoding
- Uses `execSync` for: browser detection, audio generation trigger
- All commands are predefined and not user-controllable

## Environment Variables

Optional configuration:
- `PUPPETEER_EXECUTABLE_PATH`: Custom browser path for Puppeteer
- `FASTMCP_LOG_LEVEL`: Logging level (default: ERROR)

## Project Structure

```
public/
  projects/
    <projectId>/
      <projectId>.json       # Project configuration
      footage/               # HTML/CSS media components
      audio/                 # Generated TTS audio files
        0.mp3, 1.mp3, ...
        0.json, 1.json, ...  # Word timing metadata
  video/
    render-<projectId>-landscape.mp4
    render-<projectId>-portrait.mp4
```

## Usage Example

```bash
# 1. Generate audio for a project
pnpm generate-audio agentSaasPromoVideo

# 2. Preview in browser
pnpm dev

# 3. Render final video
pnpm render agentSaasPromoVideo

# 4. Render portrait version
pnpm render agentSaasPromoVideo --portrait
```

## HTML Animation Guidelines

When creating HTML animations for video rendering, use the **CSS variable timeline** model.

### Core Model
- Renderer controls time: Puppeteer sets `--t` every frame.
- Page only renders state: `DOM = f(t)`.
- No lifecycle animation APIs (`play/start/reset`) and no hidden runtime state.
- **Transition system handles entrance effects**: Don't implement slide/fade transitions in HTML - use the project's `transitionIn` property instead.

### ✅ Required Patterns
- Define timeline root:
  ```css
  :root { --t: 0; }
  ```
- Every animated property must derive from `--t`.
- Always clamp normalized progress values:
  ```css
  --p: clamp(0, calc((var(--t) - var(--start)) / var(--duration)), 1);
  ```
- Express initial/ending states directly in CSS (seek-safe at any frame).
- Use small deterministic JS only for content mapping (e.g., subtitle/text index from `t`).
- **Let transition system handle entrance**: Focus on content animation, not entrance effects.

### 🚫 Forbidden Patterns
- `transition`
- `animation` / `@keyframes`
- `window.registerFrameAnimation(...)`
- `requestAnimationFrame` loops for timeline progression
- Implicit time from `Date.now()` / `performance.now()` for visual state
- **Manual entrance transitions**: Don't implement slide/fade in HTML - use `transitionIn` in project config
- **Fade-out effects**: Elements should not disappear after animation completes. Use `opacity: var(--p)` instead of `opacity: calc(var(--p) * (1 - var(--fade)))` to keep elements visible at their final state.

### Recommended Template
```css
.element {
  --start: 0.5;
  --duration: 1;
  --p: clamp(0, calc((var(--t) - var(--start)) / var(--duration)), 1);

  opacity: var(--p);
  transform: translateY(calc((1 - var(--p)) * 20px));
}
```

### Easing (without transition)
Use math on progress directly:
```css
--p: clamp(0, calc((var(--t) - var(--start)) / var(--duration)), 1);
--ease-out: calc(1 - (1 - var(--p)) * (1 - var(--p)));
opacity: var(--ease-out);
```

### JS Hook Pattern (text/content only)
```html
<script>
  const labels = ['A', 'B', 'C'];
  const el = document.getElementById('label');

  window.onTimelineUpdate = (t) => {
    const idx = Math.floor(Math.max(0, t) / 1.2) % labels.length;
    el.textContent = labels[idx];
  };
</script>
```

### Time Semantics (`t` vs `globalTime`)
- `onTimelineUpdate(t, globalTime)` supports two time domains:
  - `t`: clip-local time (resets to `0` when clip changes). This is the default for most HTML animations.
  - `globalTime`: continuous timeline across clips. Use only when an element must stay continuous through cross-clip transitions.
- Do **not** assume `t` is media-local. If a media appears mid-clip, `t` may already be large when it first becomes visible.
- For media-local behavior (e.g., toggle starts animating when this media appears), anchor from first visible `globalTime` and derive:
  - `local = globalTime - mediaStartGlobalTime`
- Keep fallback for compatibility:
  ```js
  window.onTimelineUpdate = (t, globalTime) => {
    const g = Number.isFinite(globalTime) ? globalTime : t;
    // use `t` for normal clip-local animation, `g` only when continuity is required
  };
  ```

### Determinism Checklist
- Seeking to any `t` yields exactly one deterministic frame.
- Animation state must not depend on "previous frame".
- Cross-clip transition visuals should be continuous in both clips.
- Final frame (`t = totalDuration`) must remain on the last clip (no wrap to first clip).

## Limitations

- Requires FFmpeg to be installed on the system
- TTS generation requires internet connection (Microsoft Edge TTS)
- Rendering is CPU-intensive and may take several minutes
- Maximum TTS text length: ~1000 characters per clip
- Frame capture requires sufficient disk space

## Transparency Statement

This skill executes shell commands and spawns child processes for video rendering. All operations are limited to:
1. Starting a local development server (Vite)
2. Running FFmpeg for video encoding
3. Launching Puppeteer for frame capture
4. Detecting browser executables on the system

No arbitrary code execution or user input is passed to shell commands. All file paths and commands are predefined and validated.
