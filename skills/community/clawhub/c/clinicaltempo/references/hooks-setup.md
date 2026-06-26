# Hook setup — Clinical Tempo ClawHub skill

Configure **optional** reminders for **Claude Code**, **Codex CLI**, or similar agents that support shell hooks. Mirrors the pattern from [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent); paths are adjusted for this monorepo.

## Overview

| Script | Purpose | Typical hook |
| --- | --- | --- |
| **`scripts/activator.sh`** | Reminds: `build:llm`, `CLAWHUB.md`, `GET /api/dance-extras/live` | `UserPromptSubmit` |
| **`scripts/error-detector.sh`** | Hints after failed shell steps (optional) | `PostToolUse` (Bash) |

Keep output **small** (~50–150 tokens) to limit overhead.

---

## Path from repo root

When the skill lives at **`.cursor/skills/clawhub/`**:

```text
.cursor/skills/clawhub/scripts/activator.sh
.cursor/skills/clawhub/scripts/error-detector.sh
```

---

## Claude Code — project-level

Create **`.claude/settings.json`** in the **clinicaltempo** repo root:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".cursor/skills/clawhub/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".cursor/skills/clawhub/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

### Activator only (lower overhead)

Omit the `PostToolUse` block.

---

## Codex CLI

Same JSON shape under **`.codex/settings.json`** (if your Codex build supports hooks).

---

## Cursor

Cursor does not use this `settings.json` hook system by default. **Rely on** the **Cursor Rules** / **@** mention of **`public/llm-full.txt`** and **`CLAWHUB.md`**, or install the **OpenClaw** hook for gateway sessions.

---

## OpenClaw

Use **`hooks/openclaw/`** in this skill (`clinicaltempo-clawhub` bootstrap) — see **`references/openclaw-integration.md`**.

---

## Troubleshooting

| Issue | Check |
| --- | --- |
| Hook not firing | Paths relative to **repo root**; scripts executable (`chmod +x`)
| Too noisy | Use **activator only**; remove PostToolUse
| Wrong project | Hooks are **per workspace**; copy settings to each clone
