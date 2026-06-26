# Security and Permissions

## Permission model

Antigravity CLI uses permission resources in the form `action(target)` and evaluates three lists:

- `deny`: block immediately.
- `ask`: pause and request explicit approval.
- `allow`: auto-approve.

Precedence is strict: `deny` wins over `ask`, and `ask` wins over `allow`.

Use `/permissions` or `/config` for normal changes. Edit `~/.gemini/antigravity-cli/settings.json` directly only when a file-level config change is required.

## Permission presets

Common `toolPermission` values:

- `request-review`: prompts for write/bash/web tools; safest default for active development.
- `proceed-in-sandbox`: auto-proceeds when sandbox containment applies.
- `always-proceed`: skips prompts; use only in trusted, low-risk contexts.
- `strict`: prompts for all non-read tools.

## Terminal sandbox

Enable sandboxing in settings:

```json
{
  "enableTerminalSandbox": true
}
```

Native containment varies by OS:

- Linux: namespace/cgroup-style isolation.
- macOS: native sandbox policy.
- Windows: AppContainer-style isolation.

When sandbox is enabled, approval prompts may offer a one-time "run without sandbox restrictions" choice. When sandbox is disabled, prompts may offer a one-time "run in sandbox" choice for a risky command.

## Risk guidance

- Keep `request-review` or `strict` for unfamiliar repositories.
- Avoid `--dangerously-skip-permissions` unless the user explicitly requests it and the workspace is trusted.
- Prefer `proceed-in-sandbox` over `always-proceed` for repetitive but bounded automation.
- If a command needs broader filesystem, URL, or MCP access, narrow the target first; broaden only when the user intent requires it.
- Use deny rules for known-sensitive paths, production secrets, destructive commands, or remote endpoints that should never be touched.
