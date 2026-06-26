# Effects Reference

## Gradient Backgrounds

Applied around the browser recording with configurable padding and corner radius.

| Gradient | Character |
|----------|-----------|
| `midnight` | Dark, deep blue/purple tones |
| `ember` | Hot, glowing warmth |
| `forest` | Natural greens, earthy depth |
| `nebula` | Cosmic purples and pinks |
| `slate` | Cool, neutral grays |
| `copper` | Warm metallic amber tones |

A gradient is automatically selected if `--background` is not specified.

## Customization Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--background <name>` | auto | Override gradient preset, or `none` to disable |
| `--no-background` | — | Disable background entirely |
| `--padding <percent>` | `8` | Space between video and background edge (0-50%) |
| `--corner-radius <px>` | `12` | Rounded corners on the video frame |
| `--no-shadow` | — | Remove the drop shadow behind the video |

## Automatic Effects

These effects are applied during video composition:

| Effect | Description | Disable with |
|--------|-------------|--------------|
| **Auto-trim** | Removes idle time between agent actions for a tighter video | — |
| **Auto-zoom** | Zooms into the active area during interactions | `--no-zoom` |
| **Click highlights** | Visual pulse overlay on each mouse click | `--no-highlight` |
| **Cursor trail** | Smooth cursor movement path overlay | `--no-cursor` |

## Composition Pipeline

The effects are applied in this order during video composition:

1. **Trim** — idle frames removed based on event timestamps
2. **Zoom** — camera follows the active element with smooth transitions
3. **Click highlights** — pulse overlays composited at click coordinates
4. **Cursor trail** — cursor path rendered from event log
5. **Background** — gradient applied with padding, corner radius, and shadow
6. **Encode** — final output at 30 FPS (mp4) or 15 FPS (gif)

## Output Formats

| Format | FPS | Codec | Use case |
|--------|-----|-------|----------|
| mp4 | 30 | libx264 | Default, all platform presets except github-gif |
| gif | 15 | gif | `github-gif` preset (max 8 MB) |
