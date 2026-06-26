# Overview

## Purpose

This package writes the short H2 lead block that turns several H3 subsections into one chapter-level argument.

Read this file before applying the skill or editing the package.

## Role split

### `SKILL.md`

Use `SKILL.md` as the router:
- when the skill triggers
- required inputs and outputs
- when to read which reference file
- what the active script still does in compatibility mode

### `references/`

Use `references/` for the judgment layer:
- lead-block archetypes
- throughline construction patterns
- bridge examples
- narration anti-patterns

### `assets/`

Use `assets/` for machine-readable constraints that later validation can consume.
In compatibility mode, use `assets/lead_block_compatibility_defaults.json` as the editable source for fallback lead phrasing, joiners, and sentence cadence.

### `scripts/`

Use the script only for deterministic work and compatibility-mode execution.
It should not remain the long-term home for voice rules or reusable prose patterns.
If a fixed fallback phrase or lead cadence needs tuning, change the compatibility asset before editing Python.

## What a chapter lead must do

A good chapter lead does four jobs:
- state the chapter's comparison lens
- connect multiple H3 subsections as one argument
- preview 2-3 recurring contrasts without turning into an axis dump
- calibrate how the chapter should be read at a high level, especially when protocol or evidence assumptions affect comparison

## What it must not do

Avoid:
- table-of-contents narration
- slide-navigation phrasing
- planner-talk transitions
- count-based opener slots used as a reusable shell
- title narration that sounds like a generated heading bridge
- new claims that the downstream H3s do not support

## Recommended read order

1. `lead_block_archetypes.md`
- choose the shape of the lead block

2. `throughline_patterns.md`
- map chapter brief fields into a chapter-level argument

3. `bridge_examples.md`
- strengthen local transitions between subsections without narrating the outline

4. `bad_narration_examples.md`
- remove weak stems and generator voice before finalizing the block

## Compatibility mode boundary

In this migration phase, the script still writes the active output.

Use the references to guide edits and future refactors, but preserve:
- body-only output
- existing file naming
- the report file
- the same high-level contract of a short lead block per eligible H2 chapter
