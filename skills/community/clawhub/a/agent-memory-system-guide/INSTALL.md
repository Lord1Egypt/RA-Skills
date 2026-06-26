# Install Skill for Agent

## Native OpenClaw install

Use the current OpenClaw-native install flow first:

```bash
openclaw skills install agent-memory-system-guide
```

This installs the skill into the active workspace `skills/` directory. That is the preferred path for current OpenClaw versions when you want the skill available in one workspace immediately.

## Post-install self-check

After install, use this lightweight self-check:

1. Confirm the skill is visible in your current OpenClaw workspace skill list.
2. Run `python3 scripts/memory_capture.py bootstrap --workspace /path/to/workspace`.
3. Confirm the workspace now has `SESSION-STATE.md`, `working-buffer.md`, and `memory-capture.md`.
4. Optionally run `python3 scripts/memory_capture.py report --workspace /path/to/workspace` to verify the workspace surface and warnings.

## Manual / agent-assisted install

```text
Please install agent-memory-system-guide as a usable skill. Keep SKILL.md, README files, templates (including `templates/OBSIDIAN-NOTE.md`), and any docs intact; preserve the repository identity, but use the canonical OpenClaw skill id `memory-system`; confirm it is usable in OpenClaw and Codex; treat OpenViking as an optional enhancement rather than a hard dependency and as one possible recall backend instead of the core workflow; and follow the repository instructions for paths or environment variables.
```

```text
请把 agent-memory-system-guide 安装成可用 skill。保留 SKILL.md、README、templates（包括 `templates/OBSIDIAN-NOTE.md`）和相关文档；保留仓库身份，但在 OpenClaw 中使用 canonical skill id `memory-system`；确认它可在 OpenClaw 和 Codex 中使用；把 OpenViking 视为可选增强而不是硬依赖，并把它理解成可选召回后端之一而不是核心流程本身；路径或环境变量优先遵循仓库说明。
```

Historical GitHub release archive: [v0.1.0](https://github.com/cjke84/agent-memory-system-guide/releases/tag/v0.1.0)

Registry / published skill version: `1.1.7`
