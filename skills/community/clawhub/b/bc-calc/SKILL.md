---
name: bc-calc
description: |-
  This skill evaluates arithmetic expressions using the Unix `bc` calculator.
  It accepts full `bc` syntax (addition, subtraction, multiplication, division, modulus, scale, sqrt, and constants like `pi`).
  Use it when the user asks to "calculate", "compute", "do math", or simply poses a question such as "what is 1+1".
  The skill provides precise, arbitrary‑precision calculation.
version: 1.0.0
---

# bc-calc

Use the Unix `bc` calculator to evaluate arbitrary arithmetic expressions. The skill accepts the expression as a command‑line argument or via standard input.

## When This Skill Applies

This skill activates when the user's request involves:
- Basic or advanced arithmetic calculations (addition, subtraction, multiplication, division, modulus)
- Full `bc` expressions (including `scale`, `sqrt`, `pi`, etc.)
- Any math expression evaluation request

## How It Works

1. Parse the mathematical expression from the request or stdin.
2. Pass the expression to `bc` and capture the output.
3. Return the result, or the `bc` error message if the expression is invalid.

## Usage Examples

```
# As a CLI command with a single expression
bc-calc "12+34*5"

# With piped input and scale
printf "scale=2; 1/3" | bc-calc
```

## Installation

The skill can be installed with the ClawHub CLI:

```
openclaw install bc-calc
```

Or simply place the `bc-calc` directory under `~/.openclaw/workspace/skills`.

## Dependencies

* `node` (>=12)
* `bc` command‑line tool (usually pre‑installed on Linux/macOS)

## Optional Flags

```
# Show help
bc-calc --help
```

The help flag displays usage instructions.

NOTE: The math‑library flag `-l` is now enabled by default, giving access to trigonometric and other advanced functions.

Available functions:
- `s(x)` : sine, in radians.
- `c(x)` : cosine, in radians.
- `a(x)` : arctangent, in radians.
- `l(x)` : natural logarithm.
- `e(x)` : e^x.
- `j(n,x)` : Bessel function of integer order n for x.
