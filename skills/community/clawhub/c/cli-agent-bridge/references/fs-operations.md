# Filesystem Operations Reference

This file describes the guarded filesystem model used by the local full package of `cli-agent-bridge`.

It is not a promise that the public ClawHub upload directory can read or write files by itself.

## Intended local behavior

In the local full package, filesystem actions are intended to stay within a configured workspace root.

Expected action surface:

- `read`
- `list`
- `exists`
- `mkdir`
- `write`
- `append`

Blocked actions in the local full package:

- `delete`
- `move`
- `rename`
- writes outside the configured workspace root

## Approval boundary

In the local full package:

- `read`, `list`, and `exists` are intended to run without approval
- `mkdir`, `write`, and `append` are intended to require explicit approval

## Important note

The public ClawHub release documents this model, but does not ship the runtime layer that enforces it.
