# Provider Integration

## Purpose

`restore_frames.py` is intentionally provider-agnostic.
It lets the skill hand each frame and a mask to any external image-editing command that can write a cleaned output frame.

## Required Command Contract

Your editor command must accept placeholders:

- `{input}`
- `{mask}`
- `{output}`
- `{index}`

Example template:

```bash
my-editor --input {input} --mask {mask} --output {output}
```

The script replaces placeholders with absolute paths and executes the command once per frame.

## Expected Behavior

The external command should:

1. read the input frame
2. respect the mask as the edit region
3. write an output frame with the same dimensions
4. leave unmasked regions visually stable

## Strong Recommendations

- Edit only the masked region
- Keep output format PNG during intermediate work
- Avoid changing colors or exposure outside the mask
- Avoid random generation settings when temporal consistency matters

## If No External Editor Exists Yet

The skill is still useful for:

- extracting frames
- generating masks
- testing fixed-region cleanup with `removelogo`
- preparing deterministic work folders and manifests

Once a provider CLI or API wrapper exists, wire it into `--editor-cmd` without changing the skill contract.
