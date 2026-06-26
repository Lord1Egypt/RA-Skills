# FFmpeg Text Overlay Guide

Quick reference for the ffmpeg drawtext approach used by `scripts/ffmpeg_render.py`.

## Drawtext Syntax

```
drawtext=fontfile=/path/to/font.ttf:text='Hello':fontsize=24:fontcolor=white:x=100:y=100
```

## Timing with `enable`

Show text only between seconds 2 and 5:
```
enable='between(t\,2\,5)'
```

Show for first 3 seconds:
```
enable='lte(t\,3)'
```

## Position Macros

- `(w-text_w)/2` — center horizontally
- `h/2-text_h/2` — center vertically
- `w-text_w-50` — right-align with 50px padding

## Multi-line text

Use `\n` in text for line breaks, or chain multiple drawtext filters.

## Background Video

Generate a solid color background:
```
-f lavfi -i color=c=0x0b1021:s=1280x720:d=60:r=30
```

## Full example

```bash
ffmpeg -f lavfi -i color=c=black:s=1280x720:d=10 \
  -i audio.mp3 \
  -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='Hello':fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t\\,0\\,5)'" \
  -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k \
  -shortest -movflags +faststart output.mp4
```

## Tips

- Escape commas in drawtext with `\,`
- Escape single-quotes in text with `\\'`
- Use `-shortest` when audio is shorter than background duration
- Add `-movflags +faststart` for web playback
