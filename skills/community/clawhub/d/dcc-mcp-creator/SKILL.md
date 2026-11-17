---
name: dcc-mcp-creator
description: >-
  Build or modernize DCC-MCP adapters and standalone studio MCP services. For individual tool skill packages, use dcc-mcp-skills-creator.
license: MIT-0
allowed-tools: Bash Read Write Edit
metadata:
  dcc-mcp:
    dcc: python
    layer: infrastructure
    compatibility: "dcc-mcp-core 0.17+, Python 3.7+"
    version: "0.19.117"
    search-hint: >-
      create DCC MCP adapter, Nuke MCP, DccServerBase, HostExecutionBridge,
      dispatcher, readiness, resources, gateway, Blender, 3ds Max, Unreal,
      ZBrush, Houdini, Maya, standalone internal MCP service, private intranet,
      non-DCC server, chunked main-thread jobs, cooperative cancellation
    tags: "adapter-development, internal-mcp-service, standalone, host-runtime, dispatcher, gateway, nuke, blender, 3dsmax, unreal, zbrush"
    skill-reference-docs:
      - "references/*.md"
  openclaw:
    homepage: https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp-creator/SKILL.md
---

# DCC-MCP Creator

Implement the requested adapter or service within its owner's project. A private
service needs no public repository, catalog entry, issue or release. For operating
an existing app use `dcc-mcp`; for individual tool packages use `dcc-mcp-skills-creator`.
An already-loaded skill needs no installation or new agent turn.

## Implementation boundaries

Use `DccServerBase` and `DccServerOptions.from_env(...)`, with host API calls
through `HostExecutionBridge`. Embedded, sidecar and standalone services have
different owner/host lifetimes; resolve that contract before wiring the runtime.
Reuse Core's public lifecycle, discovery and state owners rather than parallel
adapter implementations. Keep identity and host configuration data-driven.

For Python adapters, first verify the host's interpreter, ABI and dependencies.
When the host has no Python and Python is needed, prefer the existing shared
DCC-MCP Runtime; keep official JS/native bridges available without Python.
Follow [Python runtime selection](references/PYTHON_RUNTIME_SELECTION.md) before
choosing a payload or installer. Do not bundle or download Python per adapter.

Application UI uses project-owned `dcc-cua` / `ui-control`. Before observation
or input report `provider=dcc-cua runtime=<version> pid=<exact-pid> hwnd=<exact-native-hwnd>`.
Missing binding blocks actions. Read the bundled `dcc-cua` skill for UI work;
never fall back to generic Computer Use without the user's explicit change of provider.

## Choose relevant guidance

| Work | Read |
|---|---|
| New or modernized public adapter | [Adapter workflow](references/ADAPTER_WORKFLOW.md), [host patterns](references/HOST_PATTERN_MATRIX.md) |
| Private standalone service | [Internal service workflow](references/INTERNAL_SERVICE_WORKFLOW.md) |
| Server ownership, host dispatch, state digest, UI integration, gateway or sidecar wiring | [Runtime integration](references/RUNTIME_INTEGRATION.md); consult its relevant numbered contracts |
| Proposed adapter-local workaround for shared behavior | [Core escalation](references/CORE_ESCALATION_CHECKLIST.md) |
| Async/main-thread jobs, cancellation or reconnect | [Async recovery](references/ASYNC_RECOVERY.md) |
| Runtime failure or issue ownership | [Failure routing](references/FAILURE_ROUTING.md) |
| Nuke/standalone examples or cross-DCC file synchronization | [Integration examples](references/INTEGRATION_EXAMPLES.md) |
| Portable host setup or a typed native vector extension | [Native extension workflow](references/NATIVE_EXTENSION_WORKFLOW.md); distinguish software deployment, source-only standard adapters and released integration |
| Validation or release | [Testing and release](references/TESTING_AND_RELEASE.md) |

Use the `dcc-mcp` route only when live validation is needed; source-only edits
do not require starting a host, installing a CLI, or updating a server.
Run the relevant local checks, fix failures caused by the change, and verify the
requested behavior before reporting completion. Keep source/mock validation
separate from real-host acceptance. Publishing requires the requested scope
and the applicable release gates; native Python 3.7 remains an LTS profile,
and `py37-lite` does not satisfy its release gate.

## Non-Negotiables

- Do not touch a DCC API from a Tokio/HTTP worker thread.
- Do not parse or rewrite `SKILL.md`, `tools.yaml`, `groups.yaml`, or prompt/workflow files in adapter runtime code when core exposes a typed object or catalog API.
- Do not reach into `server._server` unless no public core API exists; if you must, file a core issue and keep the adapter shim small.
- Do not create Maya-only abstractions in shared core or adapter templates.
- Do not expose raw script execution as the primary user workflow when a typed skill can cover the task.
- Do not require GitHub, a public catalog entry, or public issue tracking for a private internal service.
- Do not publish local paths, private machine names, or source-attribution markers in public issues or PR text.
