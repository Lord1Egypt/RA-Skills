---
title: ComfyUI Skills for OpenClaw
---

# ComfyUI Skills for OpenClaw

Turn your ComfyUI workflows into callable skills for AI agents. Any agent that can run shell commands — Claude Code, Codex, OpenClaw — can discover, execute, and manage ComfyUI workflows through a single CLI.

## Core Capabilities

- **Agent-native CLI** — structured JSON output, pipe-friendly, designed for AI agents
- **Multi-server routing** — manage multiple ComfyUI instances under one namespace
- **Schema-based parameters** — expose a clean contract instead of raw graph nodes
- **Full lifecycle** — discover, import, execute, manage workflows and dependencies in one tool
- **Web UI included** — optional local dashboard for visual workflow management

## Quick Start

```bash
pip install comfyui-skill-cli
comfyui-skill server status
comfyui-skill list
comfyui-skill run local/txt2img --args '{"prompt": "a white cat"}'
```

## Project Links

- [GitHub Repository](https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw)
- [CLI Tool (PyPI)](https://pypi.org/project/comfyui-skill-cli/)
- [English README](https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw/blob/main/README.md)
- [Chinese README](https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw/blob/main/README.zh.md)
- [ComfyUI Native Routes Reference]({{ '/comfyui-native-routes/' | relative_url }})
