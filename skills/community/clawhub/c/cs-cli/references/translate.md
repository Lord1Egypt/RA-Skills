# Multilingual Translation Workflow

> **Preread**: `references/image-processing.md` for translate parameters and language codes.

## Scenario

The user has an image containing text, such as a menu, road sign, or document screenshot, and needs it translated into a target language while preserving the original layout.

## Decision Flow

### 1. Confirm Target Language

Infer the `--lang` parameter from the user's request. See `references/image-processing.md` for language codes.

### 2. Single Language vs Multiple Languages

- **Single language**: run `image translate <image-path> --lang xx` with final save options from `SKILL.md`; without a preference add `-o translated_xx.jpg -s`.
- **Multiple language versions**: use different `--lang` values, distinct local paths and `--save-title` values, and verify each result.

### 3. Multilingual Chaining Logic

```text
same input file -> run translate N times, each with a different --lang and --save-title
```

## Notes

- Processing can take longer, usually 10-60 seconds. Handle timeouts with the retry strategy.
- Text in the image must be clear enough for accurate recognition and translation.
