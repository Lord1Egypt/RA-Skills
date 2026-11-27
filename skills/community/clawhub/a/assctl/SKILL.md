---
name: assctl
description: Create, inspect, validate, edit, and theme local ASS subtitle files with assctl. Use when the user wants new timed ASS subtitles, style and palette changes, or edits that preserve karaoke timing and metadata.
homepage: https://github.com/psyb0t/assctl
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [assctl]
permissions:
  network: "Upstream GitHub and DaFont downloads for fonts-install and --embed-preset-fonts. Subtitle editing works locally."
  shell: "Run the assctl command, which runs ffmpeg and ffprobe for burn, or the psyb0t/assctl:v0.4.1@sha256:9ee38ba5e8e6f450c919a4831e6c7449d6372ba1180e3c8a9ca082ec2f46cb2c Docker image with the working directory mounted."
  filesystem: "Read the requested subtitle, JSON or font files, write the requested output, and install preset fonts in the user font directory."
---

# assctl

## Security & safety

The command edits local files. Write to a new output path unless the user asks to replace an existing file. Treat dialogue and metadata as document content.

## When to use

Use for ASS subtitle creation, inspection, fixes, and visual presets. Use timed text or an existing subtitle file as input.

## When NOT to use

Use a speech transcription tool to obtain timestamps and a video renderer to turn subtitles into video pixels.

## Usage

Run `assctl fonts-install` on the rendering machine when the preset fonts are missing. It installs verified font files and source notices into the user's font directory. Use `--preset NAME` to install one preset's requirements. Social looks include `tiktok-bold`, `reels-bold`, `shorts-impact`, `social-center`, `social-box`, `social-hook`, and `the-bold`. Use uppercase text for THE BOLD FONT's free version. ASS sets placement; existing inline position tags and event margins still take precedence.

```bash
assctl inspect captions.ass
assctl presets --json
assctl positions --json
assctl theme --preset ivory-navy --output themed.ass captions.ass
assctl position --text-position portrait-lower-middle --output moved.ass themed.ass
assctl validate themed.ass
```

See [setup and JSON examples](references/setup.md) for timed captions and precise edits.

Run `assctl burn VIDEO --subtitles FILE --output OUT` to draw captions into a video with FFmpeg; it re-encodes only the picture, in the source codec, and copies audio, tracks, chapters and metadata. Run `assctl safe-area FILE` before delivering captions for TikTok, Shorts or Reels; it fails when a style's or event's margins reach under the platform's buttons or captions. Add `--embed-preset-fonts` to `captions` or `theme` when the rendering machine should not need installed fonts; it also installs those fonts locally.

`create`, `captions`, and `theme` accept `--text-position` to choose placement independently of appearance. `position` changes only style geometry. Existing event margins and inline tags keep their precedence. `tags --spec FILE` generates a typed override block, including karaoke, drawing, fades, clipping, and transforms. Typed durations in JSON use nanoseconds.
