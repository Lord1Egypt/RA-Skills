---
name: echo-hello
description: Emit a friendly greeting with optional name. Use when a quick hello or smoke-test response is needed.
metadata: { "openclaw": { "emoji": "👋" } }
---

# echo-hello

Print a greeting. If a name is given, greet that person; otherwise greet the world.

## Usage

```bash
bash scripts/hello.sh [name]
```

## Examples

```bash
bash scripts/hello.sh
# Hello, world!

bash scripts/hello.sh OpenClaw
# Hello, OpenClaw!
```

## Notes

- Exit code is always 0 on success.
- Empty name falls back to "world".
