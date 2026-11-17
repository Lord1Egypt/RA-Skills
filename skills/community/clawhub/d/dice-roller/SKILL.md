---
name: dice-roller
description: Roll dice using standard tabletop notation (e.g. 2d6+3, 1d20, 4d6kh3). Use when the user asks to roll dice, generate random numbers within a dice-shaped distribution, resolve RPG-style checks, or needs reproducible random rolls via a seed. Supports modifiers and "keep highest" (kh) notation.
---

# Dice Roller

Roll dice in standard notation via `scripts/roll.py`.

## Usage

```bash
python3 scripts/roll.py <spec> [--seed N] [--quiet]
```

- `spec`: dice notation — `<count>d<sides>[+/-<mod>][kh<keep>]`
  - Examples: `2d6`, `1d20+5`, `3d8-1`, `4d6kh3` (roll 4d6, keep highest 3)
- `--seed N`: optional integer seed for reproducible rolls
- `--quiet`: print only the total

## Output

Default prints rolls, kept dice (if applicable), modifier, and total:

```
Rolls: [6, 2] | Modifier: +3 | Total: 11
```

`--quiet` prints only the integer total.

## Notes

- At least 1 die and 2 sides required.
- `kh` keep count cannot exceed dice rolled.
- Invalid notation exits with code 2 and an error message.
