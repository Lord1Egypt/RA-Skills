# Strict receipt format for new scans

`scripts/validate_receipt.py ANSWER.txt RECEIPT.json` checks a local receipt. Python 3.10+ is required, with no third-party Python dependencies. It makes no network requests and is not a detector. The historical public dataset has a separate format and checker.

A 100% AI result is valid measurement data. To apply an already requested condition, use `--max-ai-exclusive 100`. Omitting that option checks evidence consistency only. Neither result grants publication permission or establishes quality or human authorship.

Save these artifacts in a private directory:

- The exact final answer bytes, submitted text, and effective editor text.
- A full accessibility snapshot of the completed result containing the Basic Scan heading, displayed model, AI/Mixed/Human buttons, freshness indicator, and any short-text warning.
- A JSON receipt with the following shape. Replace every placeholder with an observed value or a SHA-256 computed from exact file bytes.

```json
{
  "schema_version": 1,
  "service": "GPTZero",
  "mode": "Basic Scan",
  "model": "4.9b",
  "status": "complete",
  "text_up_to_date": true,
  "entry_mode": "verbatim",
  "observed_at": "2026-09-06T09:00:00Z",
  "ai_percent": 100,
  "mixed_percent": 0,
  "human_percent": 0,
  "short_text_warning": false,
  "answer": {"path": "answer.txt", "sha256": "REPLACE_WITH_HASH"},
  "submitted": {"path": "submitted.txt", "sha256": "REPLACE_WITH_HASH"},
  "editor": {"path": "editor.txt", "sha256": "REPLACE_WITH_HASH"},
  "visible_result": {"path": "result.txt", "sha256": "REPLACE_WITH_HASH"}
}
```

The timestamp and scores above illustrate the schema; they are not a real scan receipt. Model values must come from the current UI, not this example. The checker requires a timezone and verifies the saved UI's model and scores. It does not establish when the service was accessed.

Artifacts must remain inside the receipt directory; absolute paths, parent traversal, and escaping symlinks are rejected. File hashes are exact, including trailing newlines. Between answer/submitted/editor files only CRLF versus LF line endings may differ. Spaces, code indentation, punctuation, and line counts must remain intact. Rendered Markdown is deliberately unsupported. Keep final prose in a verbatim entry mode or report the representation limitation; do not loosen comparisons to hide input changes.

The visible-result parser supports the accessibility snapshot shape observed during development: `heading "Basic Scan" [level=1]`, `generic: Model ...`, `button "AI ...%"` (and Mixed/Human), and `generic: Text up-to-date`. A changed UI may need a reviewed parser update. Missing or ambiguous controls fail closed. A saved snapshot and its hashes can still be fabricated; this is a consistency check, not service authentication.

Never publish the raw account snapshot by default. A public study should export only needed fields and inputs with source attribution, as described in the measurement instructions.
