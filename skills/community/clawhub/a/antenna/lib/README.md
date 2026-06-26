# `lib/` — Sourced Bash Helpers

Files in this directory are **sourced**, never executed. Each one is a small,
focused library of shell functions extracted from the `scripts/` dir to
eliminate duplicated logic.

## Sourcing convention

Every helper script in `scripts/` computes `SKILL_DIR` the same way:

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
```

To source a library:

```bash
# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"
```

## Rules for library files

1. **Read-only by default.** If a library mutates state, call that out in
   its header comment and keep mutation helpers separate from readers.
2. **No top-level side effects.** A library must be safe to source twice.
   Use a guard variable (`_ANTENNA_LIB_X_LOADED`) at the top.
3. **Callers set inputs.** Libraries should not redeclare `PEERS_FILE`,
   `CONFIG_FILE`, etc. They assume the caller has set them, the same way
   the inline code did.
4. **Return values via stdout.** Empty string means "not found" unless the
   helper name ends in `_require`, in which case missing data is fatal.
5. **Error handling stays conservative.** Mirror the tolerance of the code
   you are replacing unless you are deliberately tightening it.

## Current libraries

- `peers.sh` — read helpers for `antenna-peers.json`. Addresses REF-1303,
  REF-1405, REF-1513.
