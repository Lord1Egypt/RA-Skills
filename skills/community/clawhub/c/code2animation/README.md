# AgentSaaS Video Editor

Code-driven video creation with TTS narration and automated rendering.

## Features

- Interactive video preview with real-time playback controls
- TTS audio generation using Microsoft Edge TTS
- Automated frame-by-frame rendering (30 FPS, 1920x1080/1080x1920)
- HTML/CSS animation support with deterministic timing
- Portrait and landscape video formats

## Quick Start

**Prerequisites:** Node.js 18+, FFmpeg

```bash
# Install dependencies
pnpm install

# Generate TTS audio
pnpm generate-audio agentSaasPromoVideo

# Preview in browser
pnpm dev

# Render final video
pnpm render agentSaasPromoVideo [--portrait]
```

## Commands

```bash
pnpm dev                          # Start development server
pnpm generate-audio <projectId>   # Generate TTS audio files
pnpm render <projectId>           # Render landscape video (1920x1080)
pnpm render <projectId> --portrait # Render portrait video (1080x1920)
```

## Project Structure

```
public/projects/<projectId>/
├── <projectId>.json      # Project configuration
├── footage/              # HTML/CSS media components
└── audio/                # Generated TTS files (MP3 + timing JSON)

public/video/             # Rendered output videos
```

## Animation Guidelines

**Supported patterns:**
- setTimeout-based style changes
- CSS transitions (auto-converted to frame-based)
- Typewriter effects with character timing
- Fade in/out and slide animations

**Best practices:**
```html
<!-- Auto-detected fade in -->
<div style="opacity: 0;">Content</div>
<script>
setTimeout(() => element.style.opacity = '1', 100);
</script>
```

## System Requirements

- **FFmpeg**: Video encoding and audio mixing
- **Chromium/Chrome**: Headless rendering via Puppeteer
- **Internet**: Microsoft Edge TTS service

## Installation

### FFmpeg
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Chromium (if needed)
```bash
npx puppeteer browsers install chrome
# or set custom path
export PUPPETEER_EXECUTABLE_PATH=/path/to/chrome
```
