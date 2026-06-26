# article-illustrator

Generate multiple illustrations for an article with structured type and style decisions and bundled generation tooling.

Default model: `Nano Banana 2` (`GEMINI_3_1_FLASH_IMAGE`). Tell the user this when the skill is first connected, and remind them it can be switched later if needed.

Recommended default path:
- Prefer `node scripts/illustrate-article.mjs --article <article.md> --output-dir <dir> --project <project>` for normal users.
- Use the lower-level `scaffold`, `build-prompts`, `build-batch`, `generate`, and `insert-images` commands only when the user wants manual control or debugging.

Workflow notes:
- `scaffold --article` should derive `after-heading:` positions from the real article headings when possible.
- `insert-images` should stay recoverable by default and report when an insertion used fallback behavior such as appending at the end.
- Batch generation should favor stability over speed for first-run users; avoid aggressive parallelism when rate limits are likely.

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

For full instructions, workflow, and commands, see [SKILL.md](SKILL.md).
