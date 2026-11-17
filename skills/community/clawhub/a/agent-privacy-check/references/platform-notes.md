# Platform Notes

The questions are shared across platforms. The artifact names below are leads,
not a promise that every version or installation uses the same layout.

## Codex

For a Codex Desktop or CLI audit, check the selected workspace's project
instructions, installed Skill files, available tools, terminal or shell
boundary, browser and connected-app surface, model or connector configuration,
memory or session scope, and sandbox or network policy when exposed.

Ask separately:

- Can the agent read the path, or can it also write, delete, execute, upload,
  or administer?
- Is the capability granted by the runtime, or merely requested in a Skill?
- Which model provider or connected service receives the context?
- Can external content influence tool selection or command parameters?

Do not infer the whole Codex Desktop host, a user's other workspaces, or a
browser profile from one project file. If the current surface cannot expose a
runtime control, report it as Unknown.

Minimum read-only evidence:

| Surface | What to inspect | Safe fallback |
| --- | --- | --- |
| Workspace boundary | Current workspace root, project instructions, installed Skill files, and declared path scope | Ask for a redacted permission summary or mark the host boundary Unknown |
| Tool boundary | Tools shown to the current session, including terminal, browser, connectors, and network actions | Use the visible tool list or the platform's documented inspection surface; do not infer from Skill prose |
| Data and provider boundary | Secret filenames or environment names, model or connector destination, sandbox and egress policy | Record classified names and destination class without values; mark provider handling Unknown when unavailable |

## Claude Code

For Claude Code, inspect the selected project's CLAUDE.md or equivalent
instructions, .claude settings and hooks, Skill or plugin manifests, MCP
configuration, permission prompts, shell and filesystem scope, network
boundary, and session or memory behavior that the user has placed in scope.

Treat local settings, hooks, and repository-provided instructions as separate
surfaces. A repository file can influence a run without proving that a
permission prompt will grant the requested action. Record version-dependent
behavior as Unknown until the installed runtime or its documentation makes it
clear.

Minimum read-only evidence:

| Surface | What to inspect | Safe fallback |
| --- | --- | --- |
| Project instructions | CLAUDE.md or equivalent, .claude settings and local settings, commands, Skills, and plugins | Read only the selected project; mark user-level configuration Unknown when outside scope |
| Hooks and tools | Hooks, MCP configuration, tool permissions, shell and filesystem scope | Use the installed CLI's documented help or status inspection; do not run an unknown hook |
| External boundary | MCP servers, network policy, model provider, browser, and log destinations | Record recipient control, payload class, approval, and retention; mark the missing fields Unknown |

## Generic agents

Start from the launcher or runtime manifest, project instructions, Skill or
plugin directory, tool definitions, environment metadata, sandbox or
container policy, egress controls, memory store, and audit logs. If a vendor
uses different names, map its actual artifact to the shared questions rather
than copying this table.

Minimum read-only evidence:

| Surface | What to inspect | Safe fallback |
| --- | --- | --- |
| Runtime | Version, launcher flags, manifest, sandbox, and process identity | Ask the operator for a redacted runtime policy or mark enforcement Unknown |
| Tools and data | Tool definitions, path scopes, environment names, memory, and local data classes | Use metadata and synthetic examples; never print secret values |
| Egress | Proxy or allowlist, destination configuration, logs, and external-service policy | Record the sink class and mark untestable behavior Unknown |

Record the runtime version whenever it is available. Configuration names and
permission behavior can change between versions; a version-specific control
must be checked against the installed runtime or current vendor documentation.

## Cross-platform comparison

Use the same four-way status vocabulary on every platform:

| Question | Evidence needed |
| --- | --- |
| What can it see? | Resource path or data class plus granted read operation |
| What can it change? | Write, delete, execute, send, publish, or administer operation |
| Where can data leave? | Destination, mechanism, and payload path |
| What can steer it? | Source provenance, mutability, delimiters, validation, and tool authorization |

The report should identify platform differences as differences in evidence or
enforcement. Do not claim that a control on Codex, Claude Code, or a generic
runtime is portable until it was observed or documented for that platform.
