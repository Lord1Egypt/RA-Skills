---
name: agentmailer-cli
description: Operate AgentMailer from a shell with the generated CLI for inboxes, messages, threads, drafts, attachments, domains, webhooks, policy, events, billing, and A2A resources.
---

# AgentMailer CLI

Use the `agentmailer` command for shell automation, inspection, and reproducible operational checks. The CLI is generated from the same reviewed OpenAPI contract as the SDKs.

## Start safely

Set `AGENTMAILER_API_KEY` in the process environment or a local secret manager. Do not pass credentials as command arguments or commit `.env` files.

Begin with a read-only check:

```bash
agentmailer inboxes list --limit 10 --format table
```

Discover the exact current surface instead of guessing flags:

```bash
agentmailer --help
agentmailer inboxes --help
agentmailer --help --format json
```

For a mutating command, use `--dry-run` when available, inspect the exact target and payload, and keep a stable idempotency key for retryable creates or sends. Scripted output defaults to structured data when piped; set `--format json` when the consumer requires a fixed contract.

The checked-in CLI is currently the source-of-truth client until a release asset is independently verified. Build it from `cli/` with the Rust toolchain rather than assuming an installer exists.

Read [references/commands.md](references/commands.md) for global controls and operational patterns.

## Examples

Use the [CLI example directory](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/cli) for inbox listing, monitoring, identity discovery, and sending. The [complete examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples) provides equivalent TypeScript and Python workflows.
