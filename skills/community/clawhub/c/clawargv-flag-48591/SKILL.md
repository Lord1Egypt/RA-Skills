---
name: clawargv-flag-48591
description: ClawScan scanner argument surface probe used during an authorized ClawHub security assessment. Documentation-only helper that formats plain-text notes into a reviewable outline.
version: 0.0.1
---

# ClawScan artifact filename probe

Marker: CLAWARGV-48591

This package is a benign, documentation-only helper used during an authorized
security assessment of the ClawHub pre-publication scanning pipeline. It takes a
plain-text notes file and prints a numbered outline so a reviewer can read it
linearly. It performs no network access, installs nothing, and declares no
hook, no post-install script, and no plugin manifest.

## Behaviour

1. Read the notes file passed on the command line (default `notes.txt`).
2. Print each non-empty line prefixed with an incrementing index.
3. Exit 0 on success, 2 when the notes file is missing.

## Notes on this specific artifact

The artifact deliberately contains top-level entries whose *names* look like
ClawScan command-line flags (for example `--config=...`, `--scanner=...`,
`--output=...` and `-rf`). They are inert text files. The purpose is to check
whether any artifact-derived string can reach the scanner argv at all; the
expected result is that it cannot, because the scanner target is a fixed
relative path (`./artifact` or `./artifact/SKILL.md`).

## Usage

```
sh scripts/outline.sh notes.txt
```
