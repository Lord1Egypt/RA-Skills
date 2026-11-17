#!/usr/bin/env python3
"""Roll dice in standard notation, e.g. 2d6+3, 1d20, 4d6kh3."""
import argparse
import random
import re
import sys

PATTERN = re.compile(r"^(\d+)d(\d+)(?:([+-])(\d+))?(?:kh(\d+))?$", re.IGNORECASE)


def roll(spec: str, seed: int | None = None) -> dict:
    m = PATTERN.match(spec.strip())
    if not m:
        raise ValueError(f"Invalid dice notation: {spec!r}. Use e.g. 2d6+3, 1d20, 4d6kh3.")
    count, sides = int(m.group(1)), int(m.group(2))
    sign = m.group(3)
    mod = int(m.group(4)) if m.group(4) else 0
    if sign == "-":
        mod = -mod
    keep = int(m.group(5)) if m.group(5) else None

    if count < 1 or sides < 2:
        raise ValueError("Need at least 1 die and 2 sides.")
    if keep and keep > count:
        raise ValueError("Cannot keep more dice than rolled.")

    rng = random.Random(seed)
    rolls = [rng.randint(1, sides) for _ in range(count)]
    kept = sorted(rolls, reverse=True)[:keep] if keep else rolls
    total = sum(kept) + mod
    return {"spec": spec, "rolls": rolls, "kept": kept, "modifier": mod, "total": total}


def main():
    p = argparse.ArgumentParser(description="Roll dice (e.g. 2d6+3, 4d6kh3).")
    p.add_argument("spec", help="Dice notation")
    p.add_argument("--seed", type=int, help="Optional RNG seed for reproducibility")
    p.add_argument("--quiet", action="store_true", help="Print only the total")
    args = p.parse_args()
    try:
        r = roll(args.spec, args.seed)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    if args.quiet:
        print(r["total"])
    else:
        kept = r["kept"]
        dropped = [x for x in r["rolls"] if x not in kept] if len(kept) < len(r["rolls"]) else []
        parts = [f"Rolls: {r['rolls']}"]
        if dropped:
            parts.append(f"Kept: {kept}")
        if r["modifier"]:
            parts.append(f"Modifier: {r['modifier']:+d}")
        parts.append(f"Total: {r['total']}")
        print(" | ".join(parts))


if __name__ == "__main__":
    main()
