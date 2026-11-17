---
name: commentmd
description: Open a browser tab so a human can highlight-and-comment on a Markdown file. Submits a structured JSON of comments the agent can read and respond to. Use whenever the agent has generated a Markdown document (design doc, tech spec, README, PR description) and needs human review before proceeding.
---

# commentmd

## When to invoke

- The user explicitly runs `/commentmd <md_path>`.
- The agent has generated a Markdown document (design, tech spec, README, PR description, etc.) and needs targeted human feedback before iterating.

## Usage

```
/commentmd <md_path>
```

`<md_path>` is a relative or absolute path to the Markdown file to review.

## Agent execution steps

1. Resolve `<md_path>` to an absolute path `$ABS`.
2. Run:
   ```bash
   python3 ~/.agents/skills/commentmd/scripts/serve.py "$ABS"
   ```
3. The command starts a local HTTP server (`127.0.0.1:3118`, or the next free port up to `3128`) and opens the browser. The user selects text, adds comments, then clicks **完成评论 (Finish)**. The command prints `wrote <out_path>` and exits.
4. Read `<out_path>` — by default `<md_name_without_ext>.comments.json` next to the source file.
5. Process each comment: `quote` is the original excerpt; `prefix` / `suffix` are 32-char anchor windows around it; `comment` is the human's note. If `md_changed_during_review` is `true`, warn the user that the source file was modified externally between server start and submit.
6. Revise the original document based on the comments and summarize in the reply how each was addressed.

## Headless / remote environments

Append `--static /tmp/review.html`:

```bash
python3 ~/.agents/skills/commentmd/scripts/serve.py "$ABS" --static /tmp/review.html
```

The user opens the HTML on their own machine; **Finish** downloads a JSON file. Ask the user for the downloaded file's path, then read it.

## Output JSON format

```json
{
  "schema_version": 1,
  "md_file": "/abs/path/plan.md",
  "md_sha256": "abc...",
  "md_changed_during_review": false,
  "created_at": "2026-07-01T10:00:00Z",
  "comment_count": 2,
  "comments": [
    {
      "id": "c1",
      "quote": "Store events in MySQL",
      "prefix": "In our storage layer, we ",
      "suffix": ", replicated across ...",
      "comment": "Why not PostgreSQL? JSONB support is better.",
      "created_at": "2026-07-01T10:00:12Z"
    }
  ]
}
```

`comment_count: 0` means the user has no objections.
