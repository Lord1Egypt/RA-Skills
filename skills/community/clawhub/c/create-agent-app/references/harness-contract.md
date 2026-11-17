# Harness Contract

The generated app must be a base that can grow, not a toy interaction.

## Required Concepts

- **Provider adapter**: the only module that knows the model SDK details.
- **Agent harness**: owns prompt assembly, model calls, tool execution loop, state transitions, and trace capture.
- **Tool registry**: declares tool name, schema, handler, permission class, and dry-run support.
- **Approval gate**: blocks privileged actions until the user or host explicitly approves.
- **Memory store**: optional state layer; can be in-memory, file-backed, database-backed, or absent by design.
- **Artifact ledger**: records produced files, traces, reports, and validation outputs when the app produces artifacts.

## Tool Definition Requirements

Each tool must declare:

- stable name
- input schema
- output schema or documented result shape
- side-effect class: none, read, write, delete, network, external mutation
- approval requirement
- dry-run support
- audit fields to record in traces

## Trace Requirements

When tools are used, capture:

- run id
- user request
- selected provider and model
- tool call name and arguments after validation
- approval decisions
- tool result or error
- final status: success, failed, cancelled, or not-verified

## Honest Failure States

Use explicit errors for:

- provider not configured
- unsupported provider capability
- approval denied or missing
- validation command failed
- live smoke skipped because credentials are unavailable
- artifact validation failed

