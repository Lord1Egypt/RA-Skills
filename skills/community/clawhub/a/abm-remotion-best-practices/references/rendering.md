# Remotion Rendering Reference

Detailed rendering options, output formats, quality settings, and common render scenarios.

## Local Render

The basic render command:

```bash
npx remotion render src/index.ts CompositionId out/video.mp4
```

- `src/index.ts` -- the Remotion entry file
- `CompositionId` -- the `id` from your `<Composition>` registration (PascalCase)
- `out/video.mp4` -- output file path

## Preview Mode

Open an interactive preview in the browser:

```bash
npx remotion preview src/index.ts
```

Opens at `http://localhost:3000` with:
- Frame-by-frame scrubbing
- Real-time prop editing
- Composition selection (if multiple registered)
- Playback controls

## Output Formats

### Video Formats

| Format | Extension | Flag | Notes |
|--------|-----------|------|-------|
| H.264 (MP4) | `.mp4` | `--codec h264` | Default. Best compatibility. |
| H.265 (MP4) | `.mp4` | `--codec h265` | Smaller files, less compatible. |
| VP8 (WebM) | `.webm` | `--codec vp8` | Web-friendly, good quality. |
| VP9 (WebM) | `.webm` | `--codec vp9` | Better compression than VP8. |
| ProRes | `.mov` | `--codec prores` | Professional editing workflows. |

### Image Formats

| Format | Extension | Flag | Notes |
|--------|-----------|------|-------|
| PNG Sequence | `.png` | `--image-format png` | Lossless frames for post-processing |
| JPEG Sequence | `.jpg` | `--image-format jpeg` | Smaller frames, lossy |
| GIF | `.gif` | `--codec gif` | Animated GIF output |

## Quality Settings

### CRF (Constant Rate Factor)

Controls video quality for H.264 and H.265:

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --crf 18
```

| CRF | Quality | File Size | Use Case |
|-----|---------|-----------|----------|
| 0 | Lossless | Very large | Archival |
| 15 | Excellent | Large | Production master |
| 18 | Very good | Medium | **Recommended default** |
| 23 | Good | Smaller | Web delivery |
| 28 | Acceptable | Small | Fast previews |
| 51 | Worst | Tiny | Testing only |

Lower CRF = higher quality, larger files.

### JPEG Quality

Controls quality when using JPEG frame encoding:

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --jpeg-quality 90
```

Range: 0-100 (default: 80). Only affects JPEG-based encoding pipelines.

## Resolution Override

Override the composition dimensions at render time:

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --width 1280 --height 720
```

Useful for rendering lower-resolution previews quickly.

## Custom Props

Pass runtime props to the composition:

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --props='{"title":"Launch Day","color":"#ff0000"}'
```

Props must be valid JSON. They override the `defaultProps` in the `<Composition>` registration.

## Still Image Render

Render a single frame as an image:

```bash
npx remotion still src/index.ts CompositionId out/frame.png --frame=60
```

- `--frame=60` renders frame 60 (1 second into a 60fps video)
- Output format determined by file extension (`.png` or `.jpg`)
- Useful for thumbnails, social preview images, and debugging

## Codec Selection Guide

| Scenario | Codec | CRF | Command |
|----------|-------|-----|---------|
| Production delivery | H.264 | 18 | `--codec h264 --crf 18` |
| Fast preview | H.264 | 28 | `--codec h264 --crf 28` |
| Web embedding | VP9 | 23 | `--codec vp9 --crf 23` |
| Professional editing | ProRes | - | `--codec prores` |
| Social media upload | H.264 | 18 | `--codec h264 --crf 18` |
| Animated thumbnail | GIF | - | `--codec gif` |

## Common Render Scenarios

### Production Video (High Quality)

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --codec h264 --crf 18
```

### Fast Preview (Lower Quality)

```bash
npx remotion render src/index.ts MyVideo out/preview.mp4 --codec h264 --crf 28 --width 960 --height 540
```

### Social Media Upload

```bash
npx remotion render src/index.ts MyVideo out/social.mp4 --codec h264 --crf 18
```

H.264 is universally accepted by all social platforms (YouTube, TikTok, Instagram, LinkedIn).

### PNG Sequence for Post-Processing

```bash
npx remotion render src/index.ts MyVideo out/frames/ --image-format png
```

Renders each frame as a separate PNG file for use in external video editors.

### WebM for Web Embedding

```bash
npx remotion render src/index.ts MyVideo out/video.webm --codec vp9 --crf 23
```

Smaller files than H.264 with comparable quality, good for web delivery.

## Render Performance Tips

- **Reduce resolution** for previews (`--width 960 --height 540`)
- **Increase CRF** for faster renders during development (`--crf 28`)
- **Use `--frames=0-60`** to render only a portion for testing
- For parallel rendering at scale, see `references/lambda.md`
