---
name: gemini
description: Gemini CLI for one-shot Q&A, summaries, and generation.
homepage: https://ai.google.dev/
metadata: {"clawdbot":{"emoji":"♊️","requires":{"bins":["gemini"]},"install":[{"id":"brew","kind":"brew","formula":"gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (brew)"}]}}
---

# Gemini CLI

Use Gemini in one-shot mode with a positional prompt (avoid interactive mode).

Quick start
- `gemini "Answer this question..."`
- `gemini --model <name> "Prompt..."`
- `gemini --output-format json "Return JSON"`

File-output mode (for large token or explicit file return)
- When content is large (e.g. long article/story/report) **or** user explicitly asks for file output, use:
- `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --prompt "<prompt>"`
- Default model: `gemini-3-flash-preview`
- For video parsing with large content (long video, dense transcripts, many segments), prefer `gemini-3-flash-preview` first.
- Script behavior:
  - Always saves Gemini output to a file under `outputs/` in this skill directory.
  - Always returns `file_path` (absolute path) in JSON.
  - Optionally returns `content` when `--include-content` is provided.
- Optional args:
  - `--model <model_name>`
  - `--output-format text|json`
  - `--output-file <filename>`
  - `--output-dir <dir>`
  - `--include-content`

Required response contract for this mode
- Must include absolute file path from script JSON: `file_path`
- Content in response is optional and controlled by `--include-content`

Example
- User request: `使用 gemini 模型写 1000 字小说并输出文件给我`
- Command:
  - `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --prompt "写一篇约 1000 字中文小说，主题是..." --output-file novel-1000-words.txt`
- Expected JSON stdout:
  - `{"ok":true,"file_path":"/Users/shichen/skills/gemini/outputs/novel-1000-words.txt"}`

Video parsing example (large content)
- User request: `请解析这个长视频并输出文件`
- Command:
  - `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --model gemini-3-flash-preview --prompt "解析视频内容并输出结构化总结..." --output-file video-analysis.txt`

Extensions
- List: `gemini --list-extensions`
- Manage: `gemini extensions <command>`

Notes
- If auth is required, run `gemini` once interactively and follow the login flow.
- Avoid `--yolo` for safety.
