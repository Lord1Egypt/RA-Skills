# Boot File Review Skill

## Why this exists

Boot files are easy to let drift.
They often become:
- repetitive
- too long
- unclear about what belongs where
- full of vague references to external notes
- partially stale after agent renames or workspace changes

This skill is meant to keep them lean and reliable.

## What it should do well

- review one agent at a time
- read only the context that is actually registered for that agent
- catch duplicate statements across boot files
- catch vague or broken references
- recommend the shortest stable version of each file
- create staged replacement drafts when asked

## What it should not become

- a giant general note summarizer
- a silent in-place rewriter
- a universal registry manager
- a substitute for real agent design decisions

## Best fit in this system

Use this skill as:
- a boot-file audit tool
- a refactor helper
- a confidence check before promoting bootstrap changes
- a future-proof way to support multiple agents with different supporting context
