---
name: character-count
description: Count string length deterministically for text with hard limits. Use this skill when a post, reply, caption, commit message, or other text must stay within a maximum character count.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Character Count

Use this skill when text must fit within a strict character limit and guessing is not acceptable.

This skill is portable and self-contained. The counting logic lives in the bundled script at `scripts/character_count.py`.

## Scope

This skill measures exact string length as seen by Python `len(text)`.

- It is suitable for generic hard-limit workflows.
- It is not a platform-specific compliance engine.
- If a platform applies custom weighting rules for URLs, Unicode, or special tokens, treat this skill as a deterministic local gate, not as a guarantee of platform acceptance.

## Rules

- Never estimate character counts manually.
- Always count the final text exactly as it will be posted or saved.
- If the text is too long, rewrite it and count again.
- Prefer the JSON output mode for deterministic downstream use.
- Do not describe the result as platform-accurate unless the target platform uses plain string length.

## Recommended Usage

The bundled script requires `python3`. For broad portability, assume Python 3.8 or newer.

From the skill root, pass the exact final text over stdin so shell quoting does not alter the content:

```bash
printf '%s' "$FINAL_TEXT" | python3 scripts/character_count.py --limit 280 --json
```

If you are calling it from another working directory, use the full path to the script inside the installed skill folder.

If stdin is inconvenient, pass the text as an argument:

```bash
python3 scripts/character_count.py --limit 280 --json --text "Hello world"
```

## Output Contract

`--json` returns a single JSON object:

```json
{"chars":11,"limit":280,"remaining":269,"ok":true}
```

Field meanings:

- `chars`: exact Python string length of the provided text
- `limit`: the configured limit
- `remaining`: `limit - chars`
- `ok`: `true` when `chars <= limit`

Without `--json`, the script prints plain text key-value lines:

```text
chars=11
limit=280
remaining=269
ok=true
```

## Twitter and X Workflow

For tweets and replies:

1. Draft the final post text.
2. Count it with `--limit 280`.
3. If `ok` is `false`, shorten the text.
4. Count again.
5. Post only after the script reports `ok=true`.
6. If you need exact X enforcement, add a platform-specific validation step in addition to this skill.

## Notes

- Count the exact final text, including spaces, punctuation, hashtags, and URLs.
- Do not add or remove characters after counting unless you count again.
- Use `printf '%s'` instead of `echo` to avoid introducing a trailing newline.
- If the script receives no text, treat that as a calling error and fix the invocation before proceeding.
