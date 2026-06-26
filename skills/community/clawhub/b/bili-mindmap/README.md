# bili-mindmap

`bili-mindmap` is a publishable single-skill directory for turning a Bilibili video URL or `BV` id into `outline.md` and an `.xmind` file. It collects video metadata, subtitles, AI summary, comments, and ASR fallback material when subtitles are missing.

## Recommended Architecture

The preferred architecture is now host-model-driven:

- Python collects the raw materials.
- The host platform's injected model reads `context.md` and `host_outline_prompt.md`, then writes `outline.md`.
- Python renders `outline.md` into `.xmind`.

This means:

- You do not need to manually configure an OpenAI-compatible API inside the skill for the high-quality path.
- `scripts/generate_outline.py` still exists, but only as a local fallback.

## Package Contents

- `SKILL.md`: main skill entry
- `agents/openai.yaml`: UI metadata
- `references/mindmap-outline-template.md`: target outline structure template
- `references/host-llm-outline-spec.md`: host-model outline rules
- `scripts/prepare_bili_context.py`: collects context and writes `context.md` plus `host_outline_prompt.md`
- `scripts/generate_outline.py`: local fallback outline generator
- `scripts/render_xmind.py`: pure Python `.xmind` exporter
- `scripts/run_bili_mindmap.py`: one-command runner with `host` and `local` workflows
- `vendor/aliyun_asr/`: bundled Aliyun transcription implementation

## External Dependencies

- `bili` must be installed.
- If audio fallback is needed, `bilibili-cli[audio]` is recommended.
- Moonshine ASR requires the Python dependencies in `requirements.txt`.
- Aliyun ASR requires the Aliyun config file.
- Parakeet requires a local transcription endpoint compatible with the OpenAI Transcriptions API.

## ASR Strategy

- `--asr-provider auto`: try `moonshine -> parakeet -> aliyun`
- `--asr-provider moonshine`: Moonshine only
- `--asr-provider parakeet`: Parakeet only
- `--asr-provider aliyun`: Aliyun only

## Recommended Usage

The preferred flow inside the host platform is:

1. Run `python scripts/prepare_bili_context.py` to generate `context.md` and `host_outline_prompt.md`.
2. Let the host model generate `outline.md` from that prepared prompt package.
3. Run `python scripts/render_xmind.py` to export `.xmind`.

If you want a one-command entry point, use:

```bash
python scripts/run_bili_mindmap.py   --source "https://www.bilibili.com/video/BV1ABcsztEcY"   --output-dir output/BV1ABcsztEcY   --workflow host   --login-if-needed   --transcribe-if-needed
```

Behavior:

- On the first run, if `outline.md` does not exist yet, the script prepares the materials and prints the paths to `context.md`, `host_outline_prompt.md`, and the expected `outline.md`.
- After the host model writes `outline.md`, run the same command again and the script will automatically detect the existing outline, reuse its root title for naming when possible, and export the final `.xmind`.
- If you omit `--output-dir`, the script now falls back to the stable default directory `output/<BV-or-slug>`, so the second run can still find the same `outline.md`.

## Local Fallback Usage

If the host-model path is unavailable, keep using the local fallback flow.

### 1. Prepare Context

```bash
python scripts/prepare_bili_context.py   --source "BV1ABcsztEcY"   --output output/BV1ABcsztEcY   --login-if-needed   --transcribe-if-needed   --asr-provider auto
```

### 2. Generate Outline

```bash
python scripts/generate_outline.py   --context-dir output/BV1ABcsztEcY   --output output/BV1ABcsztEcY/outline.md
```

### 3. Export XMind

```bash
python scripts/render_xmind.py   --outline output/BV1ABcsztEcY/outline.md   --output output/BV1ABcsztEcY/result.xmind
```
