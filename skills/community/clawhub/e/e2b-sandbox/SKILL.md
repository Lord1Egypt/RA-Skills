---
name: e2b-sandbox
description: >-
  Spin up and manage E2B cloud sandboxes for agent work. Use when an OpenClaw
  agent needs an isolated remote Linux sandbox instead of the local workspace:
  creating disposable coding labs, running internet-facing services, booting a
  clean VM for risky commands, snapshotting a prepared environment, or
  reconnecting to an existing E2B sandbox by id or label.
---

# E2B Sandbox

Use this skill when the task should run in an E2B sandbox rather than directly on the OpenClaw host.

## Credentials

This skill requires `E2B_API_KEY` in the environment.
Configure it in Vault / env before use.

## MCPorter-native setup

Register the local MCP server once:

```bash
node /home/charl/.openclaw/workspace/skills/e2b-sandbox/scripts/register-mcporter.mjs
```

This writes an `e2b-sandbox` entry into:

```text
~/.openclaw/workspace/config/mcporter.json
```

Then verify it:

```bash
mcporter list e2b-sandbox --schema
```

## Primary usage

After registration, prefer MCP tools instead of shell wrappers.

Expected tool names:
- `e2b-sandbox.create_sandbox`
- `e2b-sandbox.list_sandboxes`
- `e2b-sandbox.get_info`
- `e2b-sandbox.exec`
- `e2b-sandbox.host`
- `e2b-sandbox.set_timeout`
- `e2b-sandbox.snapshot`
- `e2b-sandbox.kill`

Example low-level calls:

```bash
mcporter call e2b-sandbox.create_sandbox --args '{"label":"codex-lab","template":"base","timeoutMs":3600000}'
mcporter call e2b-sandbox.exec --args '{"sandbox":"codex-lab","cmd":"python3 --version"}'
mcporter call e2b-sandbox.host --args '{"sandbox":"codex-lab","port":3000}'
```

## Shell helper fallback

A wrapper still exists for debugging or environments where you want direct script access:

```bash
/home/charl/.openclaw/workspace/skills/e2b-sandbox/scripts/run-e2b.sh help
```

## Notes

- Sandbox ids and labels are tracked in `~/.openclaw/workspace/.state/e2b-sandboxes.json`.
- Prefer labels for longer tasks so later steps can refer to the same sandbox cleanly.
- The MCP server is local and uses the E2B Node SDK under the hood.
- Use this helper for one-shot command execution. If a task needs a long interactive PTY session or a specialized template flow, read `references/e2b-notes.md` first.
- If a task needs a custom image or preinstalled stack, create the sandbox/template first, then snapshot it for reuse.

## Read next when needed

Read `references/e2b-notes.md` when you need:
- state-file behavior
- timeout / snapshot guidance
- port exposure reminders
- when to use MCP tools vs the shell helper
