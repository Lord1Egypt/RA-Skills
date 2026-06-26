# CLI And MCP - Cursor

Use this file when the user wants repeatable terminal execution, unattended runs, or tool access through MCP.

## `cursor-agent` Posture

Treat `cursor-agent` as a real execution surface, not a thin wrapper around editor chat.
Good fits:
- bounded repo tasks
- reproducible automation
- explicit terminal-first workflows
- session resume and checkpointed work

## Non-Interactive Risk

- Non-interactive usage should be treated as high trust.
- Do not assume interactive approval behavior will save you in unattended runs.
- Before launching, lock the repo, objective, allowed files, and verification path.

## MCP Boundaries

Cursor supports MCP, but the question is not "can it connect?"
The question is:
- which host is involved
- what data it can read
- what side effects it can trigger
- whether local-only assumptions still hold once MCP is enabled

## Default Policy

- prefer no MCP unless the workflow materially benefits
- prefer local or tightly scoped servers over broad remote ones
- require explicit approval before remote MCP
- document what each approved server is allowed to touch

## Failure Signs

- the run uses the wrong repo because CLI context was never pinned
- the task widens after launch because the prompt stayed vague
- MCP was enabled to "help" before its scope was reviewed
- the user expected local-only work but the workflow now depends on remote tools
