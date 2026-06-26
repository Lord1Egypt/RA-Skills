---
name: codex-usage
description: Manual Telegram slash-style command for Codex profile status and usage checks. Use when the user sends /codex_usage, /codex_usage default, /codex_usage all, or /codex_usage <profile>, or asks to check openai-codex profile usage/limits/auth health.
---

> Deprecated wrapper: maintained implementation lives in `skills/codex-profiler/`.

For `/codex_usage*` requests, follow `../codex-profiler/SKILL.md` and run:

```bash
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --format text
```
