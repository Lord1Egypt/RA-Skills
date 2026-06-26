---
name: article-summary-card
description: Use when the user wants a webpage, article, markdown, or pasted text summarized in the current session and exported as a reusable bundle. Stable workflow: extract article text, do a two-round session summary with tags, then render the final JSON into Markdown, HTML, and PNG.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
        - google-chrome
---

# Article Summary Card

Turn an article into a concise summary bundle.

## When to use
- Summarize a webpage or article and deliver the result as an image.
- Convert long text into a reusable set of outputs: `JSON`, `Markdown`, `HTML`, `PNG`.
- Produce repeatable summary cards with a consistent layout and predictable sizing.

## Runtime Requirements
- `python3`
- `curl`
- Chrome or Chromium for headless screenshots
- Python package: `Pillow`

If Chrome is not installed at the default path, adjust the browser candidate list in `scripts/render_card.py`.

## Workflow
1. Read the input article from a URL or local file.
2. Extract the title and article body; remove obvious page chrome when possible.
3. In the current session, run two prompt rounds:
   - Round 1: create a summary plan that decides how the article should be divided into sections.
   - Round 1 must also generate 3 to 8 short tags for the article.
   - Round 2: write the final summary JSON according to that plan.
4. Use the unified renderer to export the final summary JSON as `Markdown`, `HTML`, and `PNG`.
5. Verify the outputs exist and have a reasonable size.

## Commands

Extract article text for the session workflow:

```bash
python3 article-summary-card/scripts/extract_article.py \
  --url 'https://example.com/article' \
  --out output/article-input.json
```

The extracted JSON contains:
- `title`
- `source`
- `article_text`

Then in the current session:
- Use `references/prompts/plan-system.md` and `references/prompts/plan-user.md` to design the summary structure.
- Use `references/prompts/summary-system.md` and `references/prompts/summary-user.md` to write the final summary JSON.
- Include `tags` in the final summary JSON and show them at the end of the rendered card and Markdown output.

Preferred final export:

```bash
python3 article-summary-card/scripts/render_outputs.py \
  --summary output/article-summary.json \
  --out-stem output/article-summary
```

This produces:
- `output/article-summary.md`
- `output/article-summary.html`
- `output/article-summary.png`

Optional lower-level renderers:

```bash
python3 article-summary-card/scripts/render_markdown.py --summary output/article-summary.json --out output/article-summary.md
python3 article-summary-card/scripts/render_card.py --summary output/article-summary.json --out output/article-summary.png
```

Adjust styles in:

```bash
article-summary-card/assets/templates/mobile-card.css
```

The renderer keeps HTML and CSS separate:

```bash
article-summary-card/assets/templates/mobile-card.html
article-summary-card/assets/templates/mobile-card.css
```

The size system is based on a 375px design width multiplied by `SCREEN_RATIO` in CSS and Python.

Optional helper: generate a local heuristic draft JSON when you want a quick bootstrap, but do not treat it as the preferred path for high-quality output:

```bash
python3 article-summary-card/scripts/summarize_article.py \
  --url 'https://example.com/article' \
  --out output/article-summary-draft.json \
  --mode heuristic
```

For final output, replace or rewrite that draft in-session and then use `render_outputs.py`.
`summarize_article.py` is a compatibility helper, not the main summarizer.

## Cross-Platform Adapters

- `Codex`
  - Native entrypoint is this skill folder itself: `article-summary-card/SKILL.md`
  - Optional UI metadata: `article-summary-card/agents/openai.yaml`
- `Claude Code`
  - Project slash command: `.claude/commands/article-summary-card.md`
  - Usage pattern: `/article-summary-card <url-or-file> [output-stem]`
- `OpenClaw`
  - OpenClaw uses skill folders containing `SKILL.md`, so this same directory is portable.
  - Install helper:

```bash
python3 article-summary-card/scripts/install_openclaw.py
```

  - Default destination: `~/.openclaw/workspace/skills/article-summary-card`

## Notes
- This skill prefers deterministic rendering over image-generation models so long Chinese text stays accurate.
- The preferred summarizer is the current session model, not an API call inside Python.
- Summary instructions are intentionally extracted into `references/prompts/` so they can be revised without editing Python code.
- Cross-platform portability comes from keeping one shared skill core and only adding thin platform entrypoints.
- If a site is hard to extract, inspect the HTML and add a site-specific extraction rule in `scripts/summarize_article.py`.
- For very long articles, keep the summary short enough to fit on one card. If it still overflows, shorten section points before re-rendering.
- `summarize_article.py` no longer performs LLM calls; it only generates a heuristic draft JSON.
- When DOM height measurement succeeds, the renderer trusts that height and skips whitespace auto-cropping to avoid cutting off low-contrast tags or footer content.
- The renderer uses overscan-then-crop for long screenshots to avoid incomplete bottom rendering in headless Chrome.
