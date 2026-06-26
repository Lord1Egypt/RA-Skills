# Approval Model Reference

This file describes the approval model of the local full package of `cli-agent-bridge`.

It applies to the local runtime package, not to this public text-only release by itself.

## Intended approval rules in the local full package

No approval intended:

- AI-only execution
- `read`
- `list`
- `exists`

Explicit approval intended:

- `mkdir`
- `write`
- `append`

## Permanent restrictions

Even with approval, the local full package is intended to block:

- writes outside the configured workspace root
- delete operations
- move operations
- rename operations

## Important note

This published directory documents the model, but does not contain the executor that performs approval checks.
