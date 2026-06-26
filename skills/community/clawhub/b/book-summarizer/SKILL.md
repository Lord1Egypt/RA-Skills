---
name: book-summarizer
description: Use this skill when the user wants a long-form book summarized in the user's preferred language at an explicitly verified 20 percent compression ratio, with the result rejected if it falls outside the allowed range. Warning: this skill may consume many tokens because it can run multiple times until it reaches the requested compression rate.
---

# Book Summarizer

Use this skill for requests like:

- "Summarize this book at a 20% compression ratio"
- "Generate a substantial summary and verify the ratio"
- "Produce the summary in batches and validate the final total"

## Rules

- Default target ratio: `0.20`
- Default tolerance: `0.02`
- Accept only summaries between `18%` and `22%` of the original word count
- Output must be in user's language of choice (e.g., pt-BR)
- If the ratio is outside the allowed range, do not import the summary
- In chat-only mode, if the source is very large, generate the summary in multiple batches and merge them before validation
- All packaged helper scripts live in `scripts/` inside this skill folder

## Workflow

1. Start from a local plain-text book file or a downloaded Project Gutenberg text.
2. Count the source words with `python scripts/book_tools.py count <original_file>`.
3. Compute the target summary length with `python scripts/book_tools.py target <original_file> --ratio 0.20`.
4. If the source is too large for one reply, split it with `python scripts/split_book.py <original_file> 3000`.
5. Draft summary batches in order, preserving chronology and section fidelity.
6. Merge the batches with `python scripts/book_tools.py aggregate <summary_file> <batch_files...>`.
7. Validate the final ratio with `python scripts/verify_summary_ratio.py <original_file> <summary_file>`.

## Key Files

- `scripts/book_tools.py`
- `scripts/split_book.py`
- `scripts/verify_summary_ratio.py`
- `SKILL.md`

## Notes

- The packaged scripts use only the Python standard library.
- Run the commands from the skill folder, or use explicit paths if you call them from elsewhere.
- For very large books, prefer the automated pipeline over single-turn chat drafting.
- In chat-only mode, books above roughly 80k words should be summarized over multiple turns; do not pretend a single short draft satisfies the 20% rule.


