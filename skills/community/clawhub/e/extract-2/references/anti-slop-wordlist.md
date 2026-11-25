# Anti-Slop Wordlist

## Purpose

This is a mechanical enforcement list, not a style guide. After generating any output (`.md`, `.json`, export files), run a literal grep against the file for each term below. A hit that is used as a **genuine positive descriptor** is a failure — rewrite that passage with something specific (cite a px value, hex color, ratio, or concrete trade-off), re-check, and repeat until the grep returns 0 hits against genuine descriptors.

## Exemption

A hit **inside a quoted foil** is fine. Example:

> "Could have gone for a generic *modern* look, but instead chose 2px radii consistently across all 47 interactive elements to signal engineering precision."

Here "modern" is the rejected alternative, not a descriptor of the analyzed site. This is acceptable.

## Banned Terms

When used as positive descriptors of the analyzed design, these terms are banned:

```
clean
modern
sleek
visually appealing
user-friendly
intuitive
seamless
elegant
minimalist
polished
refined
sophisticated
premium feel
```

## Grep Command

Run this after every output file is written. Adjust the filename as needed:

```bash
grep -inE "clean|modern|sleek|visually appealing|user-friendly|intuitive|seamless|elegant|minimalist|polished|refined|sophisticated|premium feel" {output-file}
```

If any line matches:
1. Read the matching line in context
2. If the term is a **genuine descriptor** (not inside a quoted foil/rejected alternative), rewrite it
3. Replace the vague term with a **specific measurement or trade-off** — e.g. replace "clean layout" with "120px section gaps with no visible dividers, creating separation through whitespace alone"
4. Re-run the grep
5. Repeat until 0 genuine-descriptor hits

## Why This Exists

"Clean and modern" describes every website ever built by an AI agent. It carries zero information. If a principle could apply to a different website without changing a single word, it has failed the specificity test. Every claim must be backed by a concrete value (px, hex, ratio, count) and cite evidence from the actual DOM data or screenshot.

The test: **"Could I have written this without seeing this specific website?"** If yes, it's slop. Rewrite it.
