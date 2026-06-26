# Manifest Schema

`manifest.json` is the stable record of one packaged run.

## Top-level fields

- `episode`
- `episode_number`
- `status`
- `generated_at`
- `selection_round`
- `selected_book`
- `attempts`
- `outputs`
- `source_outputs`
- `failures`

## `selected_book`

- `title`
- `author`
- `path`
- `selector_adapter`
- `selector_reference`

## `attempts`

- `selector_rounds`
- `longform_attempts`
- `cover_attempts`

## `outputs`

Final packaged files inside the episode directory:

- `video_path`
- `audio_path`
- `image_3x4_path`
- `image_4x3_path`
- `image_1x1_path`
- `manifest_path`

## `source_outputs`

Original paths before bundling:

- `video_path`
- `audio_path`
- `image_3x4_path`
- `image_4x3_path`
- `image_1x1_path`
- `prompt_archive_path`
- `selector_checkpoint_path`
- `longform_checkpoint_path`
- `cover_checkpoint_path`

## `failures`

Array of objects with:

- `stage`
- `message`

Recommended statuses:

- `success`
- `partial`
- `failed`
