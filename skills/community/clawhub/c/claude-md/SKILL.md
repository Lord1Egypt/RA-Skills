---
name: claude-md
description:
  Creates or prunes CLAUDE.md from verified repository commands, architecture seams, and exceptional
  conventions, retaining only rules that prevent a concrete agent error.
disable-model-invocation: true
license: Apache-2.0
metadata:
  language: en
  translation_of: claude-md-cn
  version: "0.1.0"
---

# CLAUDE.md

Read existing guidance, build scripts, CI, and relevant source. Verify each fact, then create or
update CLAUDE.md using only the applicable sections below. Omit unsupported claims, empty sections,
and placeholders; retain necessary conditions and exceptions.

## Build / Test / Format

Use `<single entry point>` instead of `<misleading command>` because `<reason>`; `<exception>` is
the only exception. Build: `<command>`; unit tests: `<command>`; integration tests:
`<command, prerequisite, and coverage>`. After changing `<file type>`, run
`<generation or formatting command>`; before commit, run `<check>`. For `<special task>`, read
`<documentation path>`.

## Architecture

This repository owns `<scope>`; `<easily confused capability>` lives in `<other location>`.
`<module>` owns `<responsibility>` and must not depend on `<module>`. The contract and
implementation entry for `<cross-module or cross-process interaction>` are at `<path>`. Use
`<default implementation>` unless `<condition>` requires `<alternative>`.

## Conventions

`<path>` is generated; edit `<source>` instead. Place new implementation in
`<smallest applicable module>`. Follow `<configuration or contribution guide>` and preserve
`<exception not enforced by tooling>`.

## Requirements

`<build, test, or runtime case>` requires `<version, platform, or tool>` and does not support
`<known limit>`. `<special configuration>` applies only when `<condition>`.

For every sentence ask: “What concrete mistake would the agent make if this were deleted?” Remove
sentences with no specific preventive value, merge duplicates, and leave no placeholders. Preserve
and report an existing constraint that cannot be verified; correct or remove one proven stale.
