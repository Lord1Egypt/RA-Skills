# Pipeline

## Decision Tree

### Fixed overlay in one stable region

Use `clean_video.sh --mode removelogo`.

Best for:

- top status bars
- bottom navigation bars
- corner watermarks
- stable subtitle strips
- small floating widgets that do not move

Why:

- faster
- cheaper
- more stable than frame-by-frame generation
- preserves the original audio stream automatically

### Overlay changes over time or needs model-based repair

Use `clean_video.sh --mode frame-edit`.

This path:

1. extracts frames
2. generates one mask file for the chosen region
3. calls an external editor once per frame
4. rebuilds the video from edited frames
5. remuxes the original audio when present

Use this when the user already has a model endpoint, CLI editor, or a custom frame-restoration command.

## Standard Work Directory Layout

```text
workdir/
├── manifest.json
├── frame_jobs.json
├── run_advice.json
├── run_advice.md
├── mask.pgm
├── run_summary.json
├── self_improve.md
├── frames/
│   ├── frame_000001.png
│   └── ...
├── edited/
│   ├── frame_000001.png
│   └── ...
├── usage/
│   ├── frame_000001.json
│   └── ...
├── temp/
│   └── rebuilt_silent.mp4
└── logs/
```

## Recommended Operator Sequence

1. Confirm the video path and output target
2. Determine whether the overlay is fixed or dynamic
3. Define the smallest useful mask
4. Run `removelogo` first for stable overlays
5. Escalate to frame-edit only when needed
6. Review the output for blur, shimmer, or visible seams

## What This Skill Does Not Guarantee

- perfect restoration of never-seen content
- temporal coherence from a weak external editor
- object tracking for moving masks without extra tooling
- face-safe or text-accurate reconstruction in all cases

## Practical Defaults

- Extract frames as PNG for lossless intermediate work
- Preserve source FPS by default
- Copy or remux original audio when possible
- Keep the work directory during iteration and delete it only when the user wants a clean final run
