---
name: arxiv-to-beamer
description: Given an arxiv identifier or arxiv abs/pdf URL, download the LaTeX source (or, if PDF-only, fall back to MinerU's PDF -> Markdown API), ask an OpenRouter model to generate a Beamer presentation introducing the work, and package the result as an Overleaf-uploadable .zip. Use when the user provides an arxiv link/id and asks for a beamer / slides / 演示文稿 / 介绍 derived from the paper.
---

# arxiv-to-beamer

Turn an arxiv paper into an Overleaf-ready Beamer project, using an OpenRouter
model to draft the slides from the paper's own LaTeX source — or, when arxiv
has no TeX source, from a Markdown rendering produced by MinerU.

## Prerequisites

- Env var `OPENROUTER_API_KEY` must be exported in the shell.
- Env var `MINERU_API_TOKEN` should be exported when the paper might be
  PDF-only (used for the MinerU fallback). Get one from
  <https://mineru.net> → console → API.
- Python 3.9+ on PATH (only stdlib is used — no `pip install` needed).

If `OPENROUTER_API_KEY` is not set, stop and ask the user to export it before
running anything. If a paper turns out to be PDF-only and `MINERU_API_TOKEN`
is missing, ask the user to export that too (or pass `--no-mineru-fallback`
to skip the fallback entirely).

## Usage

Invoke the bundled script with the arxiv id (e.g. `2603.19835`) or any
arxiv URL (`abs/`, `pdf/`, `e-print/`). Always prefer the
`${CLAUDE_PROJECT_DIR}` variable so the path resolves regardless of cwd:

```bash
python "${CLAUDE_PROJECT_DIR:-.}/.claude/skills/arxiv-to-beamer/scripts/arxiv_to_beamer.py" <arxiv_id_or_url>
```

Optional flags:

- `--output <path>` — output zip path (default `<id>-beamer.zip` in cwd).
- `--model <name>` — OpenRouter model id (default `anthropic/claude-sonnet-4.5`).
- `--language <lang>` — slide language hint passed to the model (default `中文`).
- `--keep-source` — also copy the extracted arxiv source (or MinerU
  markdown output) next to the zip.
- `--max-chars <n>` — cap source bytes sent to the model (default 200000).
- `--mineru-timeout <sec>` — how long to wait for MinerU PDF parsing
  (default 900s).
- `--no-mineru-fallback` — skip the MinerU fallback when arxiv is PDF-only
  (script then exits with code 2 instead).

## What the script does

1. Parses the arxiv id from the input (supports `2603.19835`, `2603.19835v2`,
   the legacy `hep-th/9901001` form, and full URLs).
2. Downloads `https://arxiv.org/e-print/<id>`. Detects PDF-only submissions
   via magic bytes.
3. **If TeX source is present:** extracts the archive (gzipped tar, plain
   tar, or a single gzipped `.tex`) into a temp dir and gathers every
   `.tex` / `.bib` file.
4. **If PDF-only:** falls back to the MinerU API:
   - `POST https://mineru.net/api/v4/extract/task` with
     `{"url": "https://arxiv.org/pdf/<id>", ...}`.
   - Polls `GET .../extract/task/<task_id>` until `state == "done"`.
   - Downloads the result zip (`full_zip_url`), extracts it, and
     concatenates every `.md` file as the source text.
   - Aborts (exit `2`) if MinerU is unreachable, the task fails or times
     out, or `MINERU_API_TOKEN` is not set.
5. Builds a prompt containing the collected source (truncated to
   `--max-chars`) and asks the model: "帮我做一个 beamer 来介绍一下这个
   研究工作", with formatting instructions so the response is parseable.
6. Parses files from the response. Recognised forms, in order:
   - `===== FILE: <relpath> =====` blocks (preferred, multi-file).
   - Fenced code blocks with a filename hint (`` ```latex main.tex ``).
   - A single fenced LaTeX block → `main.tex`.
   - Anything else → dumped verbatim into `main.tex`.
7. Writes everything into `<id>-beamer.zip`. Upload that zip via
   Overleaf → New Project → Upload Project.

## When invoked

- Run the script in the foreground; do not background it.
- Surface the script's stdout/stderr to the user.
- Report the absolute path of the produced `.zip`.
- If the script exits with code `2`:
  - Check the stderr message: it will say either "TeX source missing and
    MINERU_API_TOKEN not set" (ask the user to export the token, or rerun
    with `--no-mineru-fallback`), "MinerU PDF parsing failed" (network /
    quota issue — surface the detail), or "no downloadable TeX source"
    (paper is withdrawn). Do not blindly retry.
- If OpenRouter returns an HTTP error, surface the message; do not retry
  silently more than once.
