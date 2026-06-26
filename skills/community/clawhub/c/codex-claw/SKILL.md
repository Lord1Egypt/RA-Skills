---
name: codex-claw
description: Install and verify Codex Claw for Codex Desktop AGENTS.md, Agent MD, SOUL.md, soul file, session memory, personality, and OpenClaw workspace context loading through the @openclaw/codex-claw plugin with post-compaction reinjection.
metadata:
  short-description: Install and verify Codex Desktop AGENTS.md/SOUL.md context loading
  tags:
    - codex
    - codex-desktop
    - openclaw
    - agents-md
    - agent-md
    - soul-md
    - soul-file
    - context
    - memory
    - personality
    - plugin-install
---

# Codex Claw

Use this skill when a user wants Codex Desktop to load selected OpenClaw
`AGENTS.md` and `SOUL.md` context, asks how to install the Codex Claw plugin,
or needs to review those files for compatibility with native Codex behavior.

This skill is the searchable setup and safety guide. The actual runtime is the
OpenClaw code plugin package `@openclaw/codex-claw`.

Search phrases this skill should satisfy: Codex Desktop AGENTS.md, Agent MD,
SOUL.md, soul file, soul loader, Codex personality, Codex memory, OpenClaw
workspace context, post-compaction context, and Codex plugin install.

## Install The Plugin

Prefer the ClawHub package when the local OpenClaw build supports ClawHub plugin
install routing:

```bash
openclaw plugins install clawhub:@openclaw/codex-claw
```

If the local installer says the ClawHub artifact is not exposed for direct
plugin install yet, download the package from ClawHub and install the verified
`.tgz` artifact directly:

```bash
clawhub package download @openclaw/codex-claw --version latest -o /tmp/codex-claw --force
openclaw plugins install /tmp/codex-claw/openclaw-codex-claw-*.tgz --force
```

Restart the OpenClaw gateway after plugin installation.

## Configure Codex Desktop Context

Run the plugin command from the OpenClaw workspace that owns the context files:

```bash
openclaw codex-claw install \
  --agents ~/.openclaw/workspace/AGENTS.md \
  --soul ~/.openclaw/workspace/SOUL.md
```

The command writes:

- `~/.codex/openclaw-codex-claw-marketplace`, the local Codex Desktop
  marketplace payload
- `~/.codex/codex-claw.json`, the explicit source paths and reinjection mode

It does not copy the real `AGENTS.md` or `SOUL.md` files into the plugin. Codex
Desktop hooks read only the configured local paths at session time.

Register the generated marketplace with Codex Desktop:

```bash
codex plugin marketplace add ~/.codex/openclaw-codex-claw-marketplace
```

On macOS, if `codex` is not on `PATH`, use:

```bash
/Applications/Codex.app/Contents/Resources/codex plugin marketplace add ~/.codex/openclaw-codex-claw-marketplace
```

Enable plugins and hooks in `~/.codex/config.toml`:

```toml
[features]
plugins = true
codex_hooks = true
plugin_hooks = true

[plugins."codex-claw@codex-claw"]
enabled = true
```

Restart Codex Desktop after changing the marketplace or config.

## Verify

Check local bridge state without reading private file contents:

```bash
openclaw codex-claw status
```

Then start a fresh Codex Desktop session and ask:

```text
Do not use tools. If Codex Claw context was loaded into this session, reply FOUND CODEX_CLAW_CONTEXT and name the two source file headings you can see. If it was not loaded, reply NOT FOUND.
```

If verification fails, inspect diagnostics:

```bash
tail -n 50 ~/.codex/codex-claw-hook.log
openclaw codex-claw status
```

Fresh sessions are the best test. Existing sessions may not load newly added
plugin context until Codex Desktop restarts or a new session starts.

## Review AGENTS.md And SOUL.md

Before making these files always-on Codex Desktop context, ask the user to
clean or scope anything that conflicts with native Codex behavior.

Use these questions:

- Does either file claim priority over Codex system, developer, safety, tool, or
  direct user instructions?
- Does either file require OpenClaw, Claude, Eva, gateway, ACP, TTS, memory, or
  browser tools that may not exist in native Codex Desktop?
- Does either file tell the agent to hide uncertainty, suppress failed tests, or
  pretend unavailable capabilities are available?
- Does either file trigger automatic publishing, messaging, browsing, file
  editing, or credential access without explicit user approval?
- Does either file contain secrets, API keys, customer data, private memories,
  or local-only paths that should not appear in every Codex session?
- Are personality and collaboration preferences framed as lower-priority user
  context rather than as system rules?
- Are project conventions stable enough to load every session, or should they
  remain workspace-local and be loaded only on demand?

Keep stable collaboration preferences, coding style, repo conventions, review
preferences, and personality guidance when they are clearly lower-priority user
context and do not ask Codex to misrepresent its capabilities.

## What Codex Claw Does Not Do

- It does not require API keys, browser sessions, remote services, or network
  credentials.
- It does not upload `AGENTS.md` or `SOUL.md` to ClawHub.
- It does not make loaded context higher priority than native Codex
  instructions.
- It does not prove that every instruction inside the loaded files is safe.
  Review the files before enabling them broadly.

## ClawHub Display Caveat

If the ClawHub package page does not show the plugin README or source files,
verify the downloadable artifact rather than assuming the package is empty:

```bash
clawhub package download @openclaw/codex-claw --version latest -o /tmp/codex-claw --force
clawhub package verify /tmp/codex-claw/openclaw-codex-claw-*.tgz --package @openclaw/codex-claw --version latest
tar -tzf /tmp/codex-claw/openclaw-codex-claw-*.tgz | sort
```

Current ClawHub npm-pack package listings may expose only metadata files such
as `package.json` and `openclaw.plugin.json` even when the tarball contains the
README, runtime, source, and bundled skill.
