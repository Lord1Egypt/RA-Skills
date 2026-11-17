# Image Enhancement and Restoration Workflow

> **Preread**: `references/image-processing.md` for the enhance mode list and the `hd`/`restore` parameters.

## Scenario

The user has blurry, dark, shadowed, or scratched photos that need restoration or enhancement.

## Decision Tree

| User Description | Route To |
|------------------|----------|
| "The photo is too blurry" | `image hd` |
| "The photo is too dark" | `image enhance --mode 1` |
| "There are shadows" | `image enhance --mode 5` |
| "The old photo has scratches" | `image restore` |
| "A screen photo has patterns" | `image enhance --mode 8` |
| "I want a black-and-white effect" | `image enhance --mode 3` |
| "Remove handwritten annotations" | `image enhance --mode 9` |
| "Remove the watermark" | `image enhance --mode 10` |

## Multi-Step Combination

If one pass is not good enough, chain operations by writing an intermediate local output and processing it again:

```text
camscanner-cli image enhance input.jpg --mode 5 -o temp.jpg
# Continue only after the preceding step succeeds and temp.jpg is usable.
camscanner-cli image hd temp.jpg -o enhanced.jpg -s --save-title "Enhanced image"
```

Keep intermediate artifacts local. The example saves the final artifact to both destinations by default; adjust for explicit preferences using `SKILL.md` and avoid overwriting existing files.
