# Output Format Guide

Use this reference when the user wants a structured result instead of a freeform
summary.

## Default format

```md
## Stable Preferences
- ...

## Working Rules
- ...

## Anti-Patterns
- ...

## Reusable Context Block
...
```

## Condensed profile format

Use this when the user wants something compact and easy to maintain.

```md
## Memory Profile
- Preference: ...
- Default: ...
- Constraint: ...
- Avoid: ...
```

## Prompt-ready context block

Use this when the user wants a block that can be reused in later prompts.

Keep it short, specific, and future-facing.

```text
The user prefers concise technical explanations, structured outputs when useful,
and stable defaults over exploratory prompt variation. Avoid verbose summaries
unless explicitly requested.
```

## Review mode

Use this when the user already has memory notes and wants cleanup.

```md
## Keep
- ...

## Rewrite
- ...

## Remove
- ...

## Why
- ...
```
