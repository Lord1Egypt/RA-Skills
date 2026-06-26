---
name: dpp-pipeline
description: "Use when you need to turn a local source video and one product image into a single-product placement video with the DPP pipeline."
license: UNLICENSED
allowed-tools: Bash Read Glob Grep
metadata:
  openclaw:
    version: 0.1.0
    primaryEnv: ARK_API_KEY
    user-invocable: true
    compatibility: "Requires Python 3.11+, ffmpeg, network access, Ark credentials, and optional TOS credentials when compose-best must auto-upload reference media. Reads and writes in the caller workspace or DPP_WORKDIR."
    requires:
      env:
        - ARK_API_KEY
      bins:
        - python3
        - ffmpeg
---

# DPP Pipeline

Run the DPP storyboard, placement, and compose-best flow from a local workspace.

The skill bundles its Python runtime under `runtime/`, but it does not treat the installed skill directory as the project workspace. Inputs and outputs live under the caller's current working directory by default. Override that with `DPP_WORKDIR` when needed.

## When to Use

- Generate `storyboard.json` from a local video with `dpp-storyboard`.
- Generate a single-product material config from one product image under `assets/`.
- Select the best storyboard segment for one product image with `dpp-placement`.
- Run the final best-segment composition flow with `dpp-compose-best`.
- Replace the best segment in the original video with the generated clip using `dpp-final-cut`.

Do not use this skill for multi-product batch processing. This skill handles one local video and one product image at a time.

## Dependencies

- Python 3.11+
- `ffmpeg`
- Network access to Ark and TOS
- Ark environment variables in the target workspace `.env`
- `TOS_BUCKET`, `TOS_AK`, `TOS_SK`, `TOS_ENDPOINT`, and `TOS_REGION` when compose-best must auto-upload the reference clip or image
- `TOS_OBJECT_PREFIX`, `TOS_ENABLE_HTTPS`, and `TOS_FORCE_ENDPOINT` are optional TOS tuning variables

Install Python dependencies by running:

```bash
scripts/bootstrap_runtime.sh
```

## Workspace Layout

The runtime lives inside the installed skill. The caller workspace holds inputs, configs, logs, and outputs:

```text
<workspace>/
  .env
  assets/
    <single product image>
  video/
    demo.mp4
  configs/
    placement_material.json
  log/
  output/
    <video_stem>/
      finalCut/
```

Initialize a new workspace with:

```bash
scripts/init_workspace.sh
```

That command creates `assets/`, `video/`, `configs/`, and `output/`, and copies sample files into place.

## Workflow

1. Run `scripts/bootstrap_runtime.sh`.
2. If the target workspace is empty, run `scripts/init_workspace.sh`.
3. Ensure the workspace `.env` contains Ark credentials and defaults.
4. Ensure `video/demo.mp4` exists before storyboard, unless the user will pass `--video`.
5. Ensure `assets/` contains exactly one product image before material generation, unless the user will pass `--image`.
6. Run `scripts/run_storyboard.sh`.
7. Run `scripts/run_generate_material.sh`.
8. Run `scripts/run_placement.sh`.
9. Run `scripts/run_compose_best.sh`.
10. Run `scripts/run_final_cut.sh`.

Do not skip stage ordering unless the user explicitly asks to reuse an existing artifact.

## Review Pauses

Do not pause by default.

- If the user wants review pauses, stop after each requested stage and report the artifact path.
- If the user asks to continue, move directly to the next stage when the required inputs already exist.
- If the user asks to rerun a later stage, reuse earlier artifacts unless the input changed.

Typical checkpoints:

- After storyboard: review segmentation quality and thumbnail coverage.
- After placement: review `best_segment_index`, ranking, and placement rationale.
- After compose-best: review `composition_result.json`, prompt quality, and reference-media URL status.
- After final-cut: review `finalcut_result.json` and verify the output video at `output/<video_stem>/finalCut/final_cut.mp4`.

## Execution Rules

- Run the stage scripts from the caller workspace, or set `DPP_WORKDIR` to the target workspace path.
- Keep the installed skill directory immutable except for `.venv/` and the generated `runtime/` bundle.
- Always bootstrap the runtime before the first stage command.
- `dpp-storyboard`, `dpp-placement`, and `dpp-compose-best` can each take more than 10 minutes. Do not assume the process is hung just because it is quiet for a while; warn the user that the stage is long-running and let it complete naturally.
- After each stage, report the main artifact path.
- Before compose-best auto-upload, verify `TOS_BUCKET`, `TOS_AK`, `TOS_SK`, `TOS_ENDPOINT`, and `TOS_REGION` if the user did not provide `--reference-video-url` or `DPP_REFERENCE_VIDEO_URL`.
- This skill sends prompts and media metadata to Ark. Compose-best may also upload the reference clip and product image to TOS.

Detailed commands live in [references/commands.md](references/commands.md).

## Scripts

- `scripts/bootstrap_runtime.sh`
- `scripts/init_workspace.sh`
- `scripts/run_storyboard.sh`
- `scripts/run_generate_material.sh`
- `scripts/run_placement.sh`
- `scripts/run_compose_best.sh`
- `scripts/run_final_cut.sh`

Each script forwards all CLI arguments to the underlying Python module.
