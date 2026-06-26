---
name: convert_document_to_markdown
description: Convert supported local files into Markdown by running this repository's Dockerized file-only CLI. This skill must run through Docker with a prebuilt Aliyun CR image selected by host architecture and fixed version, not through a local Python runtime.
metadata: {"openclaw":{"homepage":"https://clawhub.ai","skillKey":"convert_document_to_markdown","primaryEnv":"VL_API_KEY","requires":{"bins":["docker"]}}}
---

# Convert Document To Markdown

Use this skill when a user wants a supported local file converted into Markdown for later processing.

## What this skill does

- Converts supported local files into Markdown:
  `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.txt`, `.json`, `.xml`, `.md`
- Image handling modes are file-type dependent:
  `ocr` / `vl` / `none` for `.docx`, `.pptx`, `.xlsx`, and image files;
  `ocr` / `vl` / `vl-page` / `none` for `.pdf`
- Only runs through Docker. Do not use local Python execution as an operational path.
- Uses a prebuilt Aliyun CR image with fixed version `0.0.1`:
  `convert-document-to-markdown-arm64:0.0.1` on ARM64 hosts,
  `convert-document-to-markdown-x64:0.0.1` on x64 hosts
- Returns structured JSON by default so later tool calls can consume `markdown`, `logs`, and `meta`.
- Reads one-time VL configuration from OpenClaw skill config or the repository `.env` file, then forwards it into the container automatically.
- Only exposes the `file` command. URL, health, and version commands are intentionally removed to keep startup lean.
- Do not use `latest`, do not build a fallback image at runtime, and do not treat `.doc`, `.ppt`, `.xls`, audio files, or unlisted image formats as supported inputs.

## Required workflow

1. By default the scripts use `crpi-4auaoyyj6r36p6lb.cn-hangzhou.personal.cr.aliyuncs.com/huozige_lab`.
2. Let the wrapper script resolve the host architecture and choose `convert-document-to-markdown-arm64:0.0.1` or `convert-document-to-markdown-x64:0.0.1`.
3. If needed, override with `IMAGE_REGISTRY` or `IMAGE_NAME`.
4. For a local file, run:
   `scripts/run_docker_cli.sh file <absolute-or-relative-path> --format json`
5. Parse the JSON result.
6. If `success` is `false`, surface `error.message` and relevant `logs`.
7. If `success` is `true`, use `markdown` as the canonical output for downstream work.

## One-time VL configuration

This skill is designed so the user does not need to re-enter Vision API settings on each run.

Preferred OpenClaw configuration in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "convert_document_to_markdown": {
        "enabled": true,
        "apiKey": "sk-xxx",
        "env": {
          "VL_BASE_URL": "https://api.openai.com/v1",
          "VL_MODEL": "gpt-4.1-mini"
        }
      }
    }
  }
}
```

This works because:

- `skillKey` is `convert_document_to_markdown`
- `primaryEnv` is `VL_API_KEY`, so `apiKey` maps to `VL_API_KEY`
- `env` can hold `VL_BASE_URL` and `VL_MODEL`

Repository-local runtime configuration:

- copy `.env.example` to `.env`
- fill `VL_BASE_URL`, `VL_API_KEY`, and `VL_MODEL`
- by default the scripts use `crpi-4auaoyyj6r36p6lb.cn-hangzhou.personal.cr.aliyuncs.com/huozige_lab`
- optionally override with `IMAGE_REGISTRY` or `IMAGE_NAME`
- use `scripts/run_docker_cli.sh`, which loads `.env`, forwards any host `VL_*` variables into `docker run`, and pulls the correct fixed-version image if missing

## Command patterns

Local file:

```bash
scripts/run_docker_cli.sh file ./notes.pdf --image-process-model ocr --format json
```

## Parameters

- `--image-process-model ocr`
  Default mode. Use Tesseract OCR for images.
- `--image-process-model vl`
  Use a Vision API. Only choose this when the environment provides `VL_API_KEY` and related variables.
- `--image-process-model none`
  Skip image recognition for speed.
- `--image-process-model vl-page`
  PDF only. Do not use this mode for Office documents or image files.
- `--format json|markdown`
  Use `json` unless the user explicitly wants raw Markdown on stdout.
- `--output <path>`
  Save the Markdown to a file. Prefer this only when you invoke `docker run` directly with a writable host mount.
- `--log-file <path>`
  Save detailed logs to a file. Prefer this only when you invoke `docker run` directly with a writable host mount.

## Operational notes

- For very large local files, stay with the Docker CLI path; do not wrap the file content into base64 or a temporary HTTP service.
- The skill is Docker-only. Do not instruct users to run `uv`, `python`, or any other local runtime path for production use.
- The wrapper scripts choose the image by host architecture. Override with `IMAGE_ARCH` only when you have a concrete reason.
- Prefer `IMAGE_REGISTRY` plus the fixed version `0.0.1`; only use `IMAGE_NAME` when you need to pass the full image reference explicitly.
- When the user asks for VL or VL-page, first check whether `VL_BASE_URL`, `VL_API_KEY`, and `VL_MODEL` are already configured via OpenClaw skill config or `.env`.
- If the user only needs extracted Markdown and not the raw JSON wrapper, read the JSON and return the `markdown` field.
- If the user provides an unsupported extension such as `.doc`, `.ppt`, `.xls`, `.wav`, `.mp3`, `.m4a`, or `.mp4`, say the current skill does not reliably support it.

## Safety notes

- Treat file paths as untrusted input. Quote shell arguments correctly.
- Do not claim success unless the command returns `success: true`.
