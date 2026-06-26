# Integration Template

Use this template when wiring your own tools or skills into BookMorph Magic.

## 1. Book selector adapter

The selector phase must end with exactly one chosen source book.

Required fields:

- `book_title`
- `author`
- `book_path`
- `selection_round`

Optional fields:

- `selector_adapter`
- `selector_reference`
- `selector_checkpoint`
- `failures`

Recommended JSON shape:

```json
{
  "status": "success",
  "book_title": "Example Book",
  "author": "Example Author",
  "book_path": "/abs/path/to/book.epub",
  "selection_round": 1,
  "selector_adapter": "my-book-selector",
  "selector_reference": "round-1-first-candidate",
  "selector_checkpoint": "/abs/path/to/selector-result.json"
}
```

## 2. Longform content generator adapter

This phase generates the longform outputs from the selected book.

Required fields:

- `video_path`
- `audio_path`
- `attempt`

Optional fields:

- `longform_checkpoint`
- `failures`

Recommended JSON shape:

```json
{
  "status": "success",
  "video_path": "/abs/path/to/video.mp4",
  "audio_path": "/abs/path/to/audio.m4a",
  "attempt": 1,
  "longform_checkpoint": "/abs/path/to/longform-result.json"
}
```

## 3. Cover generator adapter

This phase generates the three required aspect ratios.

Required fields:

- `image_3x4`
- `image_4x3`
- `image_1x1`
- `attempt`

Optional fields:

- `prompt_archive`
- `cover_checkpoint`
- `failures`

Recommended JSON shape:

```json
{
  "status": "success",
  "image_3x4": "/abs/path/to/3x4.png",
  "image_4x3": "/abs/path/to/4x3.png",
  "image_1x1": "/abs/path/to/1x1.png",
  "attempt": 1,
  "prompt_archive": "/abs/path/to/prompts.md",
  "cover_checkpoint": "/abs/path/to/cover-result.json"
}
```

## 4. Final bundle call

Once the 3 adapters have succeeded, call `episode_bundle.py bundle` with the chosen book metadata and all output file paths.

If a phase fails, still call `bundle` with:

- `--status failed` or `--status partial`
- one or more `--failure stage=message`

This ensures `manifest.json` still exists for audit and resume workflows.
