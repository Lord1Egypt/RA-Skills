---
name: bili-mindmap
description: Turn a Bilibili video URL or BV number into a human-like XMind mind map. Use when the user wants to collect subtitles, comments, AI summary, and transcript fallback, then generate structured notes or mind maps for a Bilibili video.
version: 0.2.1
metadata:
  clawdbot:
    emoji: ":brain:"
---

# Bili Mindmap

Turn a Bilibili video into a mind map that feels closer to something a human actually organized.

## Recommended Flow

- Python scripts collect video details, subtitles, AI summary, comments, and ASR fallback when needed.
- The host platform's injected model reads the prepared context and writes a high-quality `outline.md`.
- Python renders `outline.md` into an `.xmind` file.

## Preconditions

- `bili` must be installed and available.
- If audio fallback is needed, `bilibili-cli[audio]` should be installed.
- If cloud ASR is used on Windows, the Aliyun config file should already exist.
- If local ASR is preferred on Linux or macOS, make sure the Parakeet endpoint is running.

## Core Constraints

- Prefer subtitles first. Only fall back to ASR when subtitles are unavailable.
- Login check is mandatory: run `bili status` before `bili login`.
- The main way to produce `outline.md` should be the host model, not the local rule-based script.
- The main structure should come from subtitles or ASR. Comments and the site AI summary are supplemental only.
- Do not mechanically copy spoken transcript text. Merge themes, compress phrasing, and organize by logic.
- If information is weak or incomplete, mark it explicitly instead of inventing facts.

## Main Workflow

1. Accept either a full video URL or a `BV` id.
2. Run `bili status` to check login.
3. If needed, run `bili login` and wait for the user to scan.
4. Run `python scripts/prepare_bili_context.py --source <video-url-or-bv> --login-if-needed --transcribe-if-needed`.
5. Read the generated files: `context.md`, `host_outline_prompt.md`, `manifest.json`, `video_details.json`, `subtitles.txt`, `ai_summary.txt`, and `comments.txt`.
6. Feed `host_outline_prompt.md` to the host platform model and let it write `outline.md`. Only use `scripts/generate_outline.py` when the host model path is unavailable.
7. Run `python scripts/render_xmind.py --outline <output-dir/outline.md> --output <output-dir/result.xmind>`.
8. Tell the user where the `.xmind` file was written and which sources were most important.

## One-Command Workflow

`run_bili_mindmap.py` now supports two workflows:

- `--workflow host`: recommended quality path. Collects context first, then waits for a host-generated `outline.md`.
- `--workflow local`: fallback path. Uses `scripts/generate_outline.py` locally.

Recommended command:

```bash
python scripts/run_bili_mindmap.py   --source "BV1ABcsztEcY"   --output-dir output/BV1ABcsztEcY   --workflow host   --login-if-needed   --transcribe-if-needed
```

On the first run, if `outline.md` does not exist yet, the script will stop after context preparation and print:

- the `context.md` path
- the `host_outline_prompt.md` path
- the expected `outline.md` path

After the host model writes `outline.md`, run the same command again and it will render the `.xmind` file.

## Fallback Workflow

When the host model cannot be used, fall back to the local outline generator:

```bash
python scripts/generate_outline.py   --context-dir <output-dir>   --output <output-dir/outline.md>
```

This is only a fallback. It is usually lower quality than the host-model result.

## Collection Strategy

Collect information in this order:

1. `bili video <source>` for video details
2. `bili video <source> --subtitle` for subtitles
3. `bili video <source> --ai` for the site AI summary
4. `bili video <source> --comments` for hot comments
5. If subtitles are unavailable:
   - `bili audio <source> -o <output-dir/audio>` to extract audio
   - `auto` mode falls back in `moonshine -> parakeet -> aliyun` order

## Output Requirements

- Use the video title as the root topic.
- Keep subtitles or ASR as the main evidence.
- Prefer abstraction and synthesis over transcript copying.
- Mark uncertainty explicitly.
- The final artifacts should include both `outline.md` and `.xmind`.

## Important Files

- `scripts/prepare_bili_context.py`: login checks, content collection, ASR fallback, and generation of `context.md` plus `host_outline_prompt.md`
- `scripts/generate_outline.py`: local fallback outline generator
- `scripts/render_xmind.py`: pure Python XMind renderer
- `scripts/run_bili_mindmap.py`: one-command entry point with `host` and `local` workflows
- `references/mindmap-outline-template.md`: structure template for the final outline
- `references/host-llm-outline-spec.md`: quality and behavior rules for the host model path
- `vendor/aliyun_asr/`: bundled Aliyun file transcription implementation
