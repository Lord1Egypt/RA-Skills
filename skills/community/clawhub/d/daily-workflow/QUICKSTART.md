# Quickstart / 快速开始

## Install / 安装

```bash
openclaw skills install daily-workflow
```

or / 或

```bash
clawhub install daily-workflow
```

## Try it in 30 seconds / 30 秒验证

Say this to your agent at the end of a work session / 收工时对 agent 说：

```text
收工啦
```

You should get / 你应该得到：

- `Docs/STATUS.md` — current state, latest verification, next action;
- `Docs/NEXT_ACTIONS.md` — the immediate next step, then what follows,
  blockers and Owner decisions;
- a one-line summary of what was written.

Open those two files. That is the entire output — no dashboard, no database.

## Four phrases are enough / 四句话就够

| Say | What happens |
| --- | --- |
| `开工啦` | read existing state, orient for the session |
| `中段检查` | mid-session checkpoint |
| `收工啦` | wrap up, record exact next actions |
| `交接` | package a handoff for another person or another AI |

The point is resumability: tomorrow you, or a fresh AI session, can pick up
without re-reading the whole project.

## Minimum useful path / 最小可用路径

Just use `开工啦` and `收工啦`.

You do **not** need `Docs/PROJECT.md`, `TARGET.md`, `COMPLETED.md` or
`PENDING.md`. Those belong to the governance profile and only appear if your
project already runs one. The default lightweight profile writes two files.

## Privacy and safety / 隐私与安全

- Runs locally. Writes plain Markdown into your project's own `Docs/`.
- Stores no API keys, tokens, passwords or credentials.
- Never deletes history — superseded entries are archived, not removed.
- Read-only orientation first: nothing is written until intent is clear.
- Will not claim work is complete or QA-accepted without evidence.

## Next / 下一步

Full record structure and memory profiles: `SKILL.md`.
