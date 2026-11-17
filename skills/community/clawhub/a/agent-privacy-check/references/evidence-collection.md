# Evidence Collection

Use this checklist to collect enough evidence without turning a privacy audit
into a data dump. Read only the artifacts needed for the declared scope.

## Inspectable surfaces

| Surface | Look for | Record |
| --- | --- | --- |
| Agent instructions | Project instructions, Skill files, plugin manifests, hooks, prompts | Which instructions are loaded, whether they are mutable, and whether they request access or egress |
| Tool and permission metadata | Filesystem roots, shell, code execution, browser, network, connectors, model tools | Operation, resource scope, approval requirement, and enforcement evidence |
| Local data boundary | Workspace, repository, home paths, session or memory stores, browser profile | Read/write/delete reach; use names and classifications, not values |
| Secrets and identity | Environment variable names, credential-file names, SSH or cloud profiles, tokens, cookies | Secret type, owner, path scope, and whether the agent can read it |
| External boundary | Provider, API, webhook, browser upload, email, chat, Git, telemetry, logs, other agents | Destination, transport, payload route, retention or review status, and evidence label |
| Untrusted inputs | Web, email, documents, issues, pull requests, downloaded packages, retrieved content, memory, tool output | Who can change it, whether it is pinned, and whether it can influence a tool call |
| Isolation and oversight | Sandbox or container, network policy, approval UI, interrupt, rollback, audit log | Actual enforcement and the gaps that remain |

## Collection sequence

1. Declare the target and scope. Write down excluded paths and unavailable
   controls before inspecting content.
2. Read configuration and metadata before executing anything. Prefer the
   platform's read-only inspection or help mode.
3. Build a source and capability inventory. A filename such as .env is
   evidence that a candidate exists, not permission to print its contents.
4. Build a sink inventory. Include the model request and logging path when
   their handling is not fully known.
5. Mark external instructions and memory as untrusted until their provenance,
   integrity, and influence boundary are shown.
6. Reconcile declared permissions with runtime evidence. Record mismatches as
   findings.
7. Preserve the evidence labels and unknowns in the final report.

## Redaction rules

Keep the report useful without copying secrets:

- replace values with [REDACTED] and keep only the type, source, and scope;
- show a short relative path or a classified basename when a full path is
  sensitive;
- show a hostname or service class when the destination is necessary, but omit
  query strings, authorization headers, signed URLs, cookies, and payloads;
- use synthetic markers such as SYNTHETIC_TEST_VALUE in examples;
- do not paste full environment files, browser exports, private keys, session
  transcripts, customer records, or access tokens into prompts, fixtures, or
  reports.

## Observation boundaries

Configuration can show that a path is available; it does not show that the
path was used. Logs can show an event; they may omit provider-side retention,
redaction, or downstream copies. A successful request shows reachability; it
does not prove that the content was appropriate or deleted.

When a boundary requires a live request, use a user-approved test endpoint and
synthetic data only. A privacy check can remain Unknown when a safe test is not
available.
