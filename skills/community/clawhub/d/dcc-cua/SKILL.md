---
name: dcc-cua
description: >-
  Control application UI through project-owned DCC-CUA. Use for explicit DCC-CUA requests, including browsers and non-DCC apps, or DCC-MCP UI fallback.
license: MIT-0
allowed-tools: Bash Read
metadata:
  dcc-mcp:
    dcc: python
    layer: infrastructure
    compatibility: Cross-platform routing contract. The current DCC-CUA host is installed and verified through the official dcc-mcp-cli component manifest; exact platform capabilities remain runtime-discovered.
    version: "0.19.117"
    search-hint: "dcc-cua DCC CUA dcc cua our dcc-cua our dcc cua 我们的 dcc-cua 我们的 dcc cua project-owned UI control browser DOM exact PID HWND computer use automation"
    tags: "dcc-cua, dcc-ui-control, ui-control, browser-dom, exact-window, computer-use, infrastructure"
  openclaw:
    emoji: "🖱️"
    homepage: https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-cua/SKILL.md
---

# DCC-CUA — Project UI Control Router

Use this Skill as the canonical route whenever the user explicitly names
`dcc-cua`, `DCC CUA`, `our dcc-cua`, or `我们的 dcc-cua`.

## Non-substitution contract

An explicit DCC-CUA request is a hard routing boundary, regardless of whether
the target is Maya, Chrome, a browser, or another desktop application.

- Use the project-owned `dcc-cua` runtime and DCC-MCP `ui-control` surface.
- Never load or call generic Codex/OpenAI Computer Use, the `computer-use`
  Skill, `@oai/sky`, or Browser/Chrome automation plugins for that request.
- Never treat a DCC-CUA runtime, binding, readiness, or permission failure as
  permission to change providers.
- Repair the project route when safely possible. Otherwise report the exact
  blocker and stop.
- Use a generic provider only after the user explicitly retracts the DCC-CUA
  requirement or explicitly requests that provider by name.

This boundary is provider selection, not an authorization bypass. DCC-CUA task
grants, target binding, interruption, and confirmation policy still apply.

## Route attestation

Before the first application observation or input, report all four fields:

```text
provider=dcc-cua runtime=<version> pid=<exact-pid> hwnd=<exact-native-hwnd>
```

Do not perform the operation if the provider is different or the target is not
exactly bound.

## Runtime preflight

Use the official component contract; do not download an arbitrary executable:

```bash
dcc-mcp-cli components status dcc-cua
dcc-mcp-cli components ensure dcc-cua --yes
dcc-cua manifest
dcc-cua ping
```

Run `components ensure` only when installation or repair is authorized. It
consumes the official versionless manifest, verifies the declared SHA-256, and
reconciles the independently released companion executable.

For semantic application profiles:

```bash
dcc-cua profiles
dcc-cua profile --id <profile-id>
```

Do not invent a profile ID. Runtime-advertised capabilities are authoritative.

## Execution order

1. Prefer a typed DCC-MCP host tool when it directly expresses the operation.
2. Use DCC-CUA only for the UI behavior that typed host tools cannot expose.
3. Bind one exact target with process ID and native window handle. Missing
   either identifier blocks observation and input.
4. Open one scoped session with the minimum task grant required for the work.
5. Take a fresh observation before each action that depends on UI state.
6. Act using stable semantic control or DOM references when available.
7. Wait for a typed state transition and verify the real final state.
8. Stop the session on success, failure, interruption, or abandonment.

Continue within the existing task grant until the requested destination state
is verified, or a concrete blocker requires user action. Do not ask again for
authorized steps. An `input sent` acknowledgement is not completion evidence.

For native application menu bars, prefer the negotiated `native_menu_path`
route through `ui_control__act(action="invoke_menu", menu_path=[...])` when a
semantic menu click or Alt mnemonic cannot prove that a popup opened. A menu
invocation invalidates the current observation; honor `verification_required`
and verify the popup or resulting application state with a fresh snapshot.

## Long-running tasks and batching

For long-running visual tasks or batching, read
[continuity and evidence epochs](references/CONTINUITY.md). Use Host-held state
only when the running version advertises it; otherwise keep sequential verified
steps. Discovery must not invalidate an active action chain.

## DCC-host route

For UI in a registered DCC instance, read [DCC host commands](references/DCC_HOST.md).

## Browser and non-DCC route

For browser or non-DCC application UI, read [browser and desktop binding](references/BROWSER_AND_DESKTOP.md).

## Target and evidence invariants

- Preserve PID and native window handle in observations and audit records.
- Treat a changed PID, window handle, tab target, or session owner as a fresh
  binding that requires a fresh observation.
- Keep `full` readiness strict. If only an exact-window or typed-browser route
  is independently ready, report that route-specific degraded readiness.
- Honor Escape/user interruption immediately and do not resume without fresh
  authorization and observation.
- Do not expose local usernames, internal package paths, browser profile data,
  credentials, tokens, or unrelated window titles in public evidence.
- Verify success by reading the destination state after the mutation.

## Failure behavior

When DCC-CUA cannot complete the request, report:

1. the exact component/runtime version,
2. the exact target identity that was bound,
3. the failing readiness, capability, permission, or action stage,
4. the last safe observation or typed error, and
5. the safe next repair step.

Do not mention a generic Computer Use fallback unless the user asks for one.
