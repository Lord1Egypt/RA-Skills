---
name: "dr-agent-secrets"
description: "Persistent local secret setup, rotation, inspection, and recovery with SecretRefs, protected env fragments, redaction, and restart safety."
---

# DR Agent Secrets

Use when setting up, adding, inspecting, validating, rotating, or troubleshooting persistent local secrets or environment variables for Daniel-owned OpenClaw agents across sessions.

This skill stores procedures only. Never store a secret value.

## Core Rules

1. Keep values out of chat, memory, workspace instructions, git, logs, screenshots, transcripts, receipts, and final answers.
2. Redact diagnostics: report key names and presence/absence only.
3. Prefer OpenClaw SecretRefs for supported OpenClaw-managed fields.
4. Use protected, additive local env fragments only for service-level environment that the gateway or child processes must inherit.
5. Inspect the existing effective configuration before changing it. Never replace a global env file, systemd drop-in, or permission policy that can contain unrelated settings.
6. Ask before a gateway restart when interruption risk is unclear, and before changing secret paths, credential mechanisms, permissions policy, or production/customer-impacting auth.

## Pattern A — OpenClaw SecretRefs

Use SecretRefs when an OpenClaw-managed config field supports them.

1. Configure the SecretRef through the supported OpenClaw secret command or configuration flow.
2. Run the supported plaintext-secret audit when available.
3. Reload or restart only under the applicable approval gate.
4. Verify the actual feature without printing its credential.
5. Record only a non-secret identifier and owning subsystem.

Completion criterion: the intended feature works and no value entered durable text.

## Pattern B — Additive env.d fragment

Use this only when a gateway service or its spawned tools need a value across sessions.

1. Inspect the current service unit and drop-ins, existing env fragments, file ownership, and permissions. Print paths and key names only.
2. Create or update one project-scoped fragment with mode 600 inside an existing or newly created mode-700 env.d directory. Preserve unrelated files.
3. If service configuration does not already load the fragment, add a dedicated, named drop-in only after confirming it will not replace existing EnvironmentFile declarations. Use explicit protected paths when the host cannot safely expand a fragment pattern.
4. Run daemon-reload only when unit/drop-in configuration changed.
5. Restart only after the requester approves when interruption risk exists.
6. Verify the relevant capability and, when cross-path behavior matters, invoke dr-runtime-contract.

Do not use redirection or replacement operations against an unknown existing service override. If a shared override needs modification, stop and present a bounded patch for review.

## Adding or Rotating a Secret Group

- Use one stable fragment per project/system, not a global catch-all.
- Create files under a restrictive umask and enforce 600 on files and 700 on containing secret directories.
- Update only keys owned by the requested system.
- Before rotation, identify consumers, cache/reload behavior, and rollback source through a non-secret manifest.
- Do not delete an old credential or file until the replacement capability passes across all declared runtime paths.

Completion criterion: the owner, consumers, reload state, and redacted validation result are known.

## Reload And Validation

1. Determine whether the consumer reads credentials at startup, per request, or through a cache.
2. Use the approved reload/restart action only.
3. Confirm directory/file permissions and service references without reading values.
4. Run a safe capability check for the feature, not only an environment-presence check.
5. For OpenClaw memory/provider credentials, use a relevant non-secret health/status command where available.
6. If the credential must work across Gateway, fresh sessions, isolated children, scheduled jobs, or API clients, invoke dr-runtime-contract and require its full applicable matrix to pass.

Do not print a service Environment property that can expose values.

## Runtime Contract Cross-Reference

Use dr-runtime-contract whenever a persistent secret or environment setting must work across enabled runtime paths. This skill remains authoritative for SecretRefs, protected files, permissions, redaction, rotation safety, and restart safety. Runtime-contract owns precedence, stale-declaration detection, cross-path capability verification, and the redacted receipt.

## Git And Backup Safety

Keep secret-bearing files out of version control. Before any commit, inspect staged paths and stop if a secret-bearing file is present. Backup material may record path conventions, key names, owner subsystem, and validation steps; it must never record values, tokens, passwords, private keys, OAuth files, or env-file contents.

## Troubleshooting

When a credential works in a shell but not in the gateway:

1. Inspect the service's declared secret sources and relevant drop-ins without exposing values.
2. Check whether a daemon reload is needed.
3. Check for known legacy sources only when investigating a specific conflict.
4. Apply the approved reload/restart action.
5. Verify the intended capability.
6. Use dr-runtime-contract if more than one runtime path is enabled.

## Receipt

Report only changed paths, permission result, daemon-reload/restart state, capability result, and any remaining approval. Never report secret values.
