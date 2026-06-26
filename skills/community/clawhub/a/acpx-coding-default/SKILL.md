---
name: acpx-coding-default
description: Use direct acpx CLI via exec as the default coding execution path for Codex- and Claude-focused agents.
---

# acpx-coding-default

Use direct `acpx` CLI through `exec` for coding work.

## Binary
Always prefer the plugin-local binary:

```bash
/opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx
```

## Core rules
- `acpx` is invoked through `exec`; it is not a separate built-in tool.
- For coding, debugging, refactoring, test-running, and repo tasks, default to direct `acpx`.
- Always pass explicit `--cwd`.
- Prefer `--format quiet` unless verbose output is requested.
- Reuse named sessions when continued context is useful.
- If `acpx` fails, report the exact failing command and reason before falling back.
- If the task explicitly asks for ACP runtime thread/session behavior, use ACP runtime instead of this skill.

## Adapter defaults
- Codex-focused agent -> `codex`
- Claude-focused agent -> `claude`

## Templates

### Codex one-shot
```bash
cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx codex exec "<prompt>"
```

### Claude one-shot
```bash
cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx claude exec "<prompt>"
```

### Codex session
```bash
cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx codex sessions show <name> \
  || /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx codex sessions new --name <name>

cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx codex -s <name> "<prompt>"
```

### Claude session
```bash
cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx claude sessions show <name> \
  || /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx claude sessions new --name <name>

cd "<repo>" && /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx claude -s <name> "<prompt>"
```

## Failure handling
- `NO_SESSION`: create the named session, then retry once.
- Binary missing/version issue: check plugin-local binary first.
- Adapter/toolchain missing: report the exact missing command.
- Do not silently switch to another execution path and pretend acpx was used.
eck plugin-local binary first.
- Adapter/toolchain missing: report the exact missing command.
- Do not silently switch to another execution path and pretend acpx was used.
