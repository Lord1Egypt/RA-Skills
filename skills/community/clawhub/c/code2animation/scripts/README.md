# Scripts

## generate-audio.ts

Generates TTS audio files for a video project using Microsoft Edge TTS.

Usage:
```bash
pnpm generate-audio <projectId>
```

Example:
```bash
pnpm generate-audio agentSaasPromoVideo
```

This will:
- Read the project JSON from `public/projects/<projectId>/<projectId>.json`
- Generate MP3 audio files for each speech clip
- Save audio files to `public/audio/<projectId>/`
- Create metadata JSON files with word boundary timing information

## render.js

Renders a video project to MP4 using Puppeteer and FFmpeg, with automatic compression.

Usage:
```bash
pnpm render <projectId> [--portrait] [--no-compress]
```

Examples:
```bash
# Render landscape video with compression
pnpm render agentSaasPromoVideo

# Render portrait video
pnpm render agentSaasPromoVideo --portrait

# Render without compression
pnpm render agentSaasPromoVideo --no-compress
```

This will:
1. Check if audio files exist (generate automatically if missing)
2. Start a Vite dev server
3. Launch headless browser with Puppeteer
4. Capture frames at 30 FPS
5. Assemble video with FFmpeg
6. Mix audio tracks with proper timing
7. Save final video to `public/video/render-<projectId>-<orientation>.mp4`
8. Compress video (unless --no-compress flag is set)
9. Save compressed video to `public/video/render-<projectId>-<orientation>-compressed.mp4`

### Options

- `--portrait` - Render in portrait mode (1080x1920) instead of landscape (1920x1080)
- `--no-compress` or `--skip-compress` - Skip automatic video compression after rendering

## compress.js

Compresses a video file using FFmpeg with H.264 codec.

Usage:
```bash
node scripts/compress.js <input-video-path> [--crf=23] [--preset=medium]
```

Examples:
```bash
# Compress with default settings (CRF=23, preset=medium)
node scripts/compress.js public/video/render-agentSaasPromoVideo-landscape.mp4

# High quality compression (larger file)
node scripts/compress.js public/video/render-agentSaasPromoVideo-landscape.mp4 --crf=18 --preset=slow

# Fast compression (lower quality)
node scripts/compress.js public/video/render-agentSaasPromoVideo-landscape.mp4 --crf=28 --preset=fast
```

### Compression Settings

**CRF (Constant Rate Factor)**: 18-28
- Lower = better quality, larger file size
- 18 = visually lossless
- 23 = default (good balance)
- 28 = lower quality, smaller file

**Preset**: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
- Faster presets = quicker encoding, larger files
- Slower presets = better compression, smaller files
- medium = default (good balance)

Output file will be saved as `<original-name>-compressed.mp4` in the same directory.

### Requirements

- Node.js 18+
- FFmpeg installed and available in PATH
- Puppeteer (automatically installed with dependencies)

### Install FFmpeg

macOS:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt-get install ffmpeg
```

Windows:
Download from https://ffmpeg.org/download.html

### Troubleshooting

If you get browser launch errors, set the browser path:
```bash
export PUPPETEER_EXECUTABLE_PATH=/path/to/chrome
```

Or install Chromium:
```bash
npx puppeteer browsers install chrome
```
