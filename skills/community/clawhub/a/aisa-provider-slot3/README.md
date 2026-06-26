# AIsa Provider

Release-ready ClawHub skill package generated from `targetSkills/aisa-provider`.

- Skill name: `aisa-provider`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Configure AIsa as an OpenAI-compatible provider endpoint for OpenClaw and related runtimes. Use this skill when the user wants to set `AISA_API_KEY`, point a client at `https://api.aisa.one/v1`, inspect AIsa model IDs, compare routed model options such as Qwen, DeepSeek, Kimi, and Doubao, or troubleshoot provider configuration. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
