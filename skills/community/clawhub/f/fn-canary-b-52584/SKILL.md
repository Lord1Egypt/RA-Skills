---
name: Filename canary bravo
description: Operational audit canary for ClawHub CI filename handling (authorized).
version: 1.0.0
---

# Filename canary bravo

This document exists to exercise how stored artifact file names and metadata fields are
handled by the ClawHub publication pipeline. Each embedded filename below is inert plain
text inside this markdown body; the interesting part is the file *name* recorded in the
version manifest and replayed to downstream scanning and export jobs.

## Scope of the canary

- The publisher owns this skill and the account used to upload it.
- No exploit payload is shipped: the only bytes outside this document are one-line notes.
- Any callback observed would indicate a downstream shell interpolation, not intent here.

## What is being measured

Filename characters such as dollar-parenthesis, backticks, semicolons, leading dashes and
newlines are legal on Linux filesystems but dangerous when a path is pasted into a shell
string. The canary records which of those names the upload endpoint accepts and whether a
later pipeline stage reassembles them into a command line.

## Operational notes

Tagged as latest so the published version follows the normal release path. The scan verdict
is expected to be conservative; that verdict is itself part of the evidence being gathered.

## Stored names

- leading double dash option shapes
- tar checkpoint pair
- glob wildcards in a path segment
- single-dash short option lookalike

Marker FN-CANARY-B.
