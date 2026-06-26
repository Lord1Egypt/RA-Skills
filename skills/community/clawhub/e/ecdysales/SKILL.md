---
name: ecdysales
description: "Quick product image processing: add price sticker + watermark + logo. Use when user sends `$price:` with an image. Minimal context, runs fast."
requires:
  bins:
    - convert
    - identify
    - bc
    - python3
---

# Ecdysales 🏷️

You add price stickers to product images. Nothing else.

## When to act

A message has `$price:` AND an image was attached.

## What to do

1. Run: `scripts/run.sh --latest '<price>' [flags]` — **use single quotes**
2. The script prints `✅ Done: <output-path>` — save that path
3. Reply with the output image to the user
4. Say nothing else.

⚠️ **Single quotes for prices:** `'$1300'` not `"$1300"` — double quotes break `$`.
⚠️ `MEDIA:` line must be FIRST in your reply. Without it, nothing is sent.

## Skip flags

| User says | Add to command |
|-----------|---------------|
| `no-logo` | `--no-logo` |
| `no-watermark` | `--no-watermark` |
| `sticker-only` | `--sticker-only` |

## Errors

| Situation | Reply |
|-----------|-------|
| `$price:` but no image | 📸 Send an image with your price |
| Image but no `$price:` | 💰 Include `$price: $XXX` |
| Processing failed | ❌ Something broke, try again |

## Safety

- **No network access.** All processing is local via ImageMagick. No external APIs, no data leaves the machine.
- **No shell injection.** Prices are passed to ImageMagick `caption:`, not interpolated into shell commands. Single quotes prevent variable expansion.
- **Read-only input.** Source images are never modified. Output goes to a separate `output/` directory.
- **No persistent state.** No databases, no config files written at runtime, no tracking.
- **Worst case:** A malformed image causes ImageMagick to error out. The script catches this and reports failure.
- **Cleanup:** Output files should be cleaned periodically (e.g. cron job) to avoid disk fill.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-27 | Initial release |

## Everything else

NO_REPLY. Don't chat. Don't explain. Just process or stay quiet.
