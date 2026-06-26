---
name: gcloud
description: Manage Google Cloud Platform resources using the official gcloud CLI, discovering command syntax dynamically with `gcloud <group> --help` before execution.
user-invocable: true
disable-model-invocation: true
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["gcloud"]},"install":[{"id":"gcloud-sdk","kind":"manual","url":"https://docs.cloud.google.com/sdk/docs/install-sdk","bins":["gcloud"],"label":"Install Google Cloud CLI (official)"}]}}
---

# Google Cloud CLI

gcloud - manage Google Cloud resources and developer workflows

This skill is built on top of the official [`gcloud` CLI](https://cloud.google.com/sdk/gcloud). It supports the full CLI surface while avoiding hardcoded syntax by always consulting `--help` output at runtime.

Related docs:
- Installation and setup: [installation.md](installation.md)
- Group reference: [groups.md](groups.md)
- Usage examples: [examples.md](examples.md)
- Troubleshooting: [troubleshooting.md](troubleshooting.md)

## Requirements

This skill requires `gcloud` CLI.

For setup instructions, see [installation.md](installation.md).

## Scope

Use this skill only for Google Cloud resource management via `gcloud` commands. Do not use unrelated endpoints, tools, or local file operations outside the requested task.

## Credentials and Environment

This skill uses the active Google Cloud CLI authentication context (`gcloud auth`) and configuration (`gcloud config`). It inherits the permissions of the active identity.

Before any operation:
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active account and project.
2. If the active account is not a dedicated service account, stop and ask the user to switch identities.
3. Confirm the target project and environment with the user before proceeding.

Credential safety rules:
- Use least-privilege service accounts.
- Do not use personal accounts or broad admin identities for automation.
- Be explicit when `--impersonate-service-account` is in use.
- Prefer sandbox projects for validation before production changes.

## Workflow

Before executing any `gcloud` command, follow this sequence:

1. Check active context:
   ```bash
   gcloud config list --format='text(core.account,core.project)'
   ```
2. Identify the right command group from [groups.md](groups.md).
3. Discover syntax using help commands:
   ```bash
   gcloud <GROUP> --help
   gcloud <GROUP> <SUBGROUP> --help
   ```
4. Build the exact command from discovered syntax.
5. Present the full command and wait for explicit user approval.
6. Execute only after approval.
7. Return output and summarize result.

## Approval Policy

All operations require explicit user confirmation before execution, including read operations.

This includes:
- Read/list/get operations
- Create/update/delete operations
- IAM and policy changes
- Configuration changes (`set`, `unset`, `reset`)
- Service enable/disable operations

For every operation, the agent must:
1. Show the full command.
2. Show active account/project context.
3. Wait for explicit user approval.

## Important Rules

- Never guess command syntax; always validate with `--help` first.
- Never execute commands autonomously.
- Use `--format=json` when output will be parsed programmatically.
- Use `--quiet` only after explicit user approval.
- Warn clearly when commands are high-impact (IAM, networking, deletion, org-level changes).

## What You Can Do

You can perform any operation available through `gcloud`, as long as it is within user-requested scope and approved before execution.

Examples and scenarios are documented in [examples.md](examples.md).

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for authentication, IAM, API enablement, and syntax troubleshooting steps.
