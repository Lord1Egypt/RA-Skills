# Gemini Provider

## Supported Provider

This skill currently supports one built-in generative editor path:

- Gemini Nano Banana 2, implemented through `scripts/gemini_nano_banana_edit.py`

The default model id in the script is:

- `gemini-3.1-flash-image-preview`

If you want to override it, set:

```bash
export GEMINI_MODEL='gemini-3.1-flash-image-preview'
export GEMINI_IMAGE_SIZE='1K'
```

## Required Setup

The user must configure an API key before running Gemini mode:

```bash
export GEMINI_API_KEY='your_api_key_here'
```

By default the wrapper reads `GEMINI_API_KEY`. You can change the env name only if you call the wrapper directly.

## Command Entry Points

Preferred high-level entry point:

```bash
bash scripts/clean_video.sh \
  --input /abs/path/input.mp4 \
  --output /abs/path/output.mp4 \
  --mode gemini-nano-banana \
  --region '0:0:100%:12%' \
  --image-size 1K
```

Low-level single-frame wrapper:

```bash
python3 scripts/gemini_nano_banana_edit.py \
  --input /abs/path/frame.png \
  --mask /abs/path/mask.pgm \
  --output /abs/path/frame_clean.png
```

## How The Wrapper Works

The wrapper sends Gemini:

1. the original frame
2. the binary mask
3. an instruction to preserve unmasked pixels and repair only the white masked region

If the mask is not already in a Gemini-friendly upload format, the wrapper converts it to PNG first.

## Budget And Progress

Before the Gemini pass starts, the skill now:

- counts how many frames will be processed
- prints a base cost estimate for the whole batch
- reminds the user that prompt and input tokens add a small extra amount

During processing, it prints:

- completed frame count
- elapsed time
- cumulative prompt tokens when usage metadata is available
- cumulative output tokens when usage metadata is available
- cumulative estimated spend in USD

The current base output-cost estimates used by the skill are:

- `0.5K`: about `$0.045` per generated image
- `1K`: about `$0.067` per generated image
- `2K`: about `$0.101` per generated image
- `4K`: about `$0.151` per generated image

These numbers are based on the official Gemini Developer API pricing page for `gemini-3.1-flash-image-preview`. Input tokens are billed separately at a much lower per-token rate, so the skill labels the pre-run number as a base estimate rather than an exact final bill.

## Important Limitations

- Gemini is being used as a frame editor, not a true video model
- Output can vary between adjacent frames
- Larger masks increase flicker risk
- The result is a plausible cleanup, not guaranteed factual recovery

## Best Practices

- Keep masks tight
- Prefer short videos for early iteration
- Start with fixed overlays before trying dynamic overlays
- Preserve the work directory with `--keep-workdir` when tuning mask size or prompt behavior
