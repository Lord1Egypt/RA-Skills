---
name: fabricated-symbols
description: Code calls functions, classes, or methods that don't exist — either on project types or on third-party library APIs.
emoji: 👻
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# fabricated-symbols

The agent invokes a symbol that isn't defined. Most often this is a plausible-looking method on a third-party object, or a utility "I'm sure we have one of those" that the project actually lacks.

## Symptoms

- Generated code calls `someLibrary.convenientHelper(...)` where the library has no such method.
- Invented method signatures on framework objects (wrong argument order, wrong return type).
- References to utility functions the project doesn't have.
- Runtime `AttributeError` / `TypeError: X is not a function` / `undefined is not a function`.

## What to do

- For every symbol you invoke on a third-party library, check the library's real API — docs, source, or type definitions — before writing code.
- For every symbol you invoke on a project type, grep the codebase to confirm it exists. Don't assume.
- If a helper is missing, either add it explicitly (and say you're adding it) or use what the project actually has.
- Prefer the library's documented API over clever-looking shortcuts. Invented methods often look like what the library "should" have.
- When refactoring, run the type-checker after every meaningful change. Invented methods sometimes type-check against `any` but fail at runtime.
