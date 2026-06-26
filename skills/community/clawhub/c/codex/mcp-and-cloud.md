# MCP and Cloud

## MCP Basics

Inspect current MCP state before enabling anything:

```bash
codex mcp list
codex mcp get SERVER_NAME
```

Manage servers deliberately:

```bash
codex mcp add ...
codex mcp remove SERVER_NAME
codex mcp login SERVER_NAME
codex mcp logout SERVER_NAME
```

Treat each server as a separate trust decision with its own data reach and side effects.

## Cloud Task Flow

Codex Cloud is useful when you want remote task execution plus local review and apply:

```bash
codex cloud exec ...
codex cloud status TASK_ID
codex cloud list
codex cloud diff TASK_ID
codex cloud apply TASK_ID
```

Never jump from cloud execution to local apply without reviewing the diff first.

## App-Server and Advanced Integrations

`codex app-server` is an advanced integration surface and remains experimental:

```bash
codex app-server --listen stdio://
codex app-server --listen ws://127.0.0.1:PORT
```

Use it only when the integration path and analytics posture are understood.

## Local OSS Provider

When local inference is the goal, Codex can route to an OSS provider:

```bash
codex exec --oss --local-provider ollama ...
codex exec --oss --local-provider lmstudio ...
```

Do not treat local-provider mode as equivalent to hosted Codex behavior; capability and reliability can differ significantly.
