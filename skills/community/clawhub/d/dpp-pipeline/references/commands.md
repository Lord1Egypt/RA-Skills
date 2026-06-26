# DPP Commands

These commands assume:

- `SKILL_ROOT` points at the installed `dpp-pipeline` skill directory.
- `WORKDIR` points at the caller workspace that contains `.env`, `video/`, `assets/`, `configs/`, and `output/`.

Example setup:

```bash
SKILL_ROOT=/absolute/path/to/installed-skill
WORKDIR=/absolute/path/to/project
cd "$WORKDIR"
```

The stage scripts default to `DPP_WORKDIR=$PWD`. If you do not want to `cd`, export `DPP_WORKDIR="$WORKDIR"` before running them.

## Bootstrap Runtime

Always run this before any stage command:

```bash
"$SKILL_ROOT"/scripts/bootstrap_runtime.sh
```

The bootstrap script:

- creates a dedicated `.venv` inside the skill directory if missing
- installs the bundled runtime in editable mode with dev dependencies
- verifies required Python imports
- verifies `ffmpeg`

## Initialize a Workspace

Run this once for a new workspace:

```bash
"$SKILL_ROOT"/scripts/init_workspace.sh "$WORKDIR"
```

It creates:

- `assets/`
- `video/`
- `configs/`
- `output/`

It also copies:

- `configs/placement_material.json`
- `env-example.txt` into `.env.example`

## Verify TOS Upload Environment

Run this before `dpp-compose-best` if the user expects automatic upload of the reference image or video:

```bash
env | rg '^(TOS_BUCKET|TOS_AK|TOS_SK|TOS_ENDPOINT|TOS_REGION|TOS_OBJECT_PREFIX|TOS_ENABLE_HTTPS|TOS_FORCE_ENDPOINT)='
```

Required in practice:

- `TOS_BUCKET`
- `TOS_AK`
- `TOS_SK`
- `TOS_ENDPOINT`
- `TOS_REGION`

Optional:

- `TOS_OBJECT_PREFIX`
- `TOS_ENABLE_HTTPS`
- `TOS_FORCE_ENDPOINT`

## Stage 1: Storyboard

Command:

```bash
"$SKILL_ROOT"/scripts/run_storyboard.sh --output output
```

Optional arguments:

- `--video /absolute/path/input.mp4`
- `--model <endpoint-or-model>`
- `--file-id <ark-file-id>`
- `--retry 1`

Primary output:

- `output/<video_stem>/storyboard.json`
- `output/<video_stem>/thumbnails/`

Use this stage when the user wants a storyboard breakdown from a local source video.

## Stage 2: Material Config

The material config is a single-product JSON file consumed by placement and compose-best.

Command:

```bash
"$SKILL_ROOT"/scripts/run_generate_material.sh
```

Primary output:

- `configs/placement_material.json`

Optional arguments:

- `--image /absolute/path/product.png`
- `--output /absolute/path/material.json`
- `--brand <brand>`
- `--product-name <name>`
- `--model <endpoint-or-model>`
- `--retry 1`

Required in practice:

- exactly one product image under `assets/`, unless `--image` is provided

## Stage 3: Placement

Command:

```bash
"$SKILL_ROOT"/scripts/run_placement.sh \
  --storyboard output/<video_stem>/storyboard.json \
  --material-config configs/placement_material.json
```

Optional arguments:

- `--output output/<video_stem>`
- `--model <endpoint-or-model>`
- `--retry 1`

Primary output:

- `output/<video_stem>/placement_analysis.json`

Use this stage when the user wants the best storyboard segment for one product image.

## Stage 4: Compose Best

Command:

```bash
"$SKILL_ROOT"/scripts/run_compose_best.sh \
  --storyboard output/<video_stem>/storyboard.json \
  --placement-analysis output/<video_stem>/placement_analysis.json \
  --material-config configs/placement_material.json
```

Optional arguments:

- `--output output/<video_stem>`
- `--prompt-model <doubao-seed-model>`
- `--generation-model <video-generation-model>`
- `--reference-video-url <https-or-asset-url>`
- `--duration 5`
- `--retry 1`
- `--generate-audio`

Primary output:

- `output/<video_stem>/composition_result.json`
- `output/<video_stem>/reference_clips/segment-XXXX.mp4`

Compose-best uses `best_segment_index` from `placement_analysis.json`. If Ark requires public reference URLs, the command will try TOS upload first. If upload is unavailable and the user does not provide `--reference-video-url`, the stage still writes a pending result that explains which URL is missing.

## Stage 5: Final Cut

Replace the best segment in the original source video with the generated video clip, producing a complete final video.

Command:

```bash
"$SKILL_ROOT"/scripts/run_final_cut.sh \
  --composition-result output/<video_stem>/composition_result.json
```

Optional arguments:

- `--output output/<video_stem>/finalCut`

Primary output:

- `output/<video_stem>/finalCut/final_cut.mp4`
- `output/<video_stem>/finalCut/finalcut_result.json`

This stage requires a succeeded `composition_result.json` with a valid `downloaded_video_path`. It uses FFmpeg concat filter to assemble three parts: original video before the best segment, the generated clip, and original video after the best segment.

## Human Review Pattern

If the user wants review pauses:

1. Run one stage.
2. Report the main artifact path.
3. Stop.
4. Resume only after the user says to continue or gives corrections.
