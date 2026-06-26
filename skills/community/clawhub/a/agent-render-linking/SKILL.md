---
name: agent-render-linking
description: Create zero-retention agent-render.com links for markdown, code, diffs, CSV, or JSON artifacts. Use when an agent needs to share a nicely rendered artifact in the browser instead of pasting raw content into chat. Trigger for requests like "share this as a link", "make a diff link", "render this markdown/code/csv/json", or when chat rendering is weak. Agent Render is open source, hosted on Cloudflare Pages, and self-hostable. Use platform-specific linked-text syntax only on surfaces that support it cleanly, such as Discord Markdown links, Telegram HTML links, or Slack mrkdwn links; otherwise send a short summary plus the raw URL.
---

# Agent Render Linking

Create browser links for artifacts rendered by `agent-render.com`.

## Project context

Agent Render is:
- open source
- publicly hosted on Cloudflare Pages at `agent-render.com`
- self-hostable for people who want their own deployment
- meant to provide a zero-retention browser viewer for agent-shared artifacts

Source repository:
- `https://github.com/baanish/agent-render`

## Core rule

Keep the artifact content in the URL fragment, not in normal query params.

Use this fragment shape:

```text
#agent-render=v1.<codec>.<payload>                (plain | lz | deflate)
#agent-render=v1.arx.<dictVersion>.<payload>   (arx)
```

Supported codecs:
- `plain`: base64url-encoded JSON envelope
- `lz`: `lz-string` compressed JSON encoded for URL-safe transport
- `deflate`: deflate-compressed UTF-8 JSON bytes encoded as base64url
- `arx`: domain-dictionary substitution + brotli (quality 11) + base76/base1k/baseBMP encoding (~70% smaller than deflate with baseBMP). Fetch the shared dictionary from `https://agent-render.com/arx-dictionary.json` to apply substitutions locally before brotli compression. Three encoding tiers: baseBMP (~62k safe BMP code points, ~15.92 bits/char, best density), base1k (1774 Unicode code points U+00A1–U+07FF), and base76 (ASCII fallback). The encoder tries all three and picks the shortest.
- packed wire mode (`p: 1`) may be used automatically to shorten transport keys

Prefer:
1. shortest valid fragment for the target surface
2. codec priority `arx -> deflate -> lz -> plain` unless explicitly overridden
3. packed wire mode when available

## Envelope shape

Use this JSON envelope:

```json
{
  "v": 1,
  "codec": "plain",
  "title": "Artifact bundle title",
  "activeArtifactId": "artifact-1",
  "artifacts": [
    {
      "id": "artifact-1",
      "kind": "markdown",
      "title": "Weekly report",
      "filename": "weekly-report.md",
      "content": "# Report"
    }
  ]
}
```

## Supported artifact kinds

### Markdown

```json
{
  "id": "report",
  "kind": "markdown",
  "title": "Weekly report",
  "filename": "weekly-report.md",
  "content": "# Report\n\n- Item one"
}
```

### Code

```json
{
  "id": "code",
  "kind": "code",
  "title": "viewer-shell.tsx",
  "filename": "viewer-shell.tsx",
  "language": "tsx",
  "content": "export function ViewerShell() {\n  return <main />;\n}"
}
```

### Diff

Prefer a real unified git patch in `patch`.

```json
{
  "id": "patch",
  "kind": "diff",
  "title": "viewer-shell.tsx diff",
  "filename": "viewer-shell.patch",
  "patch": "diff --git a/viewer-shell.tsx b/viewer-shell.tsx\n--- a/viewer-shell.tsx\n+++ b/viewer-shell.tsx\n@@ -1 +1 @@\n-old\n+new\n",
  "view": "split"
}
```

Use `view: "unified"` or `view: "split"`.

A single `patch` string may contain multiple `diff --git` sections.

### CSV

```json
{
  "id": "metrics",
  "kind": "csv",
  "title": "Metrics snapshot",
  "filename": "metrics.csv",
  "content": "name,value\nrequests,42"
}
```

### JSON

```json
{
  "id": "manifest",
  "kind": "json",
  "title": "Manifest",
  "filename": "manifest.json",
  "content": "{\n  \"ready\": true\n}"
}
```

## Multi-artifact bundles

Use multiple artifacts when the user should switch between related views.

Example cases:
- summary markdown + patch diff
- report markdown + raw CSV
- config JSON + related code file

Set `activeArtifactId` to the artifact that should open first.

## Link construction

Construct the final URL as:

```text
https://agent-render.com/#agent-render=v1.<codec>.<payload>                (plain | lz | deflate)
https://agent-render.com/#agent-render=v1.arx.<dictVersion>.<payload>       (arx)
```

For `plain`:
1. Serialize the envelope as compact JSON
2. Base64url-encode it
3. Append it after `v1.plain.`

For `lz`:
1. Serialize the envelope as compact JSON
2. Compress with `lz-string` URL-safe encoding
3. Append it after `v1.lz.`

For `deflate`:
1. Serialize the envelope as compact JSON (or packed wire form)
2. Encode JSON to UTF-8 bytes
3. Deflate the bytes
4. Base64url-encode the compressed bytes
5. Append it after `v1.deflate.`

## Shared arx dictionary

The `arx` codec uses a substitution dictionary to replace common patterns with short byte sequences before brotli compression. The dictionary is served as a static JSON file:

- **Endpoint**: `https://agent-render.com/arx-dictionary.json`
- **Pre-compressed**: `https://agent-render.com/arx-dictionary.json.br` (brotli, ~929 bytes)

The dictionary contains two arrays:

- `singleByteSlots`: up to 25 patterns mapped to single control bytes (highest compression value)
- `extendedSlots`: additional patterns mapped to two-byte sequences (0x00 prefix + index)

To use the dictionary for local `arx` encoding:

1. Fetch `https://agent-render.com/arx-dictionary.json`
2. Apply substitutions in order: for each entry, replace all occurrences of the pattern in the serialized JSON envelope with its corresponding control byte(s)
3. Brotli-compress the substituted bytes at quality 11
4. Encode the compressed bytes using **baseBMP** (preferred, smallest), **base1k** (mid-tier), or **base76** (ASCII fallback)
    - BaseBMP uses ~62k safe BMP code points (U+00A1–U+FFEF, skipping surrogates, combining marks, zero-width chars). Prefix the encoded string with U+FFF0 marker. ~15.92 bits/char
    - Base1k uses 1774 Unicode code points (U+00A1–U+07FF, skipping combining diacriticals and soft hyphen). ~10.79 bits/char
    - Base76 uses 77 ASCII fragment-safe characters — use this if the target surface cannot handle Unicode in URL fragments. ~6.27 bits/char
    - Try all three and pick the shortest
5. Prepend `v1.arx.<dictVersion>.` to form the fragment payload (use the same dictionary version used for substitution)

The dictionary includes JSON envelope boilerplate patterns (like `","kind":"Markdown","content":"`), JSON-escaped Markdown syntax, programming keywords, and common English words. The viewer loads the same dictionary on startup to reverse substitutions during decode.

If the dictionary fetch fails, fall back to `deflate` codec.

## Practical limits

Respect these limits:
- target fragment budget: about 8,000 characters
- target decoded payload budget: about 200,000 characters
- strict Discord practical budget for linked text workflows: about 1,500 characters

If a link is getting too large:
1. try `arx` first, then `deflate`, then `lz`, then `plain`
2. allow packed wire mode
3. trim unnecessary prose or metadata
4. prefer a focused artifact over a bloated one
5. return a structured failure when the payload cannot fit the requested budget

## Agent budget mode

When the caller provides a strict budget (for example 1,500 chars):

1. encode using all available candidates (`arx/deflate/lz/plain`, packed and non-packed)
2. choose the shortest fragment that is within budget
3. if no candidate fits, return the shortest fragment plus a clear budget failure explanation

Do not silently truncate content to force fit.

## Formatting links in chat

Use platform-specific link text only on surfaces that support it cleanly.

### Discord

Prefer standard Markdown links:

```md
[Short summary](https://agent-render.com/#agent-render=...)
```

Examples:
- `[Weekly report](https://agent-render.com/#agent-render=...)`
- `[Config diff](https://agent-render.com/#agent-render=...)`
- `[CSV snapshot](https://agent-render.com/#agent-render=...)`

### Telegram

Prefer HTML links because OpenClaw Telegram outbound text uses `parse_mode: "HTML"`.

```html
<a href="https://agent-render.com/#agent-render=...">Short summary</a>
```

### Slack

Prefer Slack `mrkdwn` link syntax:

```text
<https://agent-render.com/#agent-render=...|Short summary>
```

### All other OpenClaw chat surfaces

For WhatsApp, Signal, iMessage, Google Chat, IRC, LINE, and any other surface without reliable inline link-text formatting, do not force Markdown-style links.

Use:
- a short summary line first
- then the raw URL on its own line

If a provider later exposes a reliable native linked-text format, use that provider-specific syntax instead of generic Markdown.

## Output style

When sharing a link:
- keep the summary short
- make the artifact title human-readable
- use filenames when they help the viewer
- do not narrate the transport details unless the user asks

## Good defaults

- Prefer one strong artifact over many weak ones
- Prefer `patch` for diffs
- Prefer readable titles
- Prefer Markdown link text when supported
- Prefer shortest-by-measurement instead of human guesses
- Use budget-aware encoding for Discord-like constraints

## Avoid

- Do not put raw artifact content in normal query params
- Do not upload artifact content to a server for this workflow
- Do not dump giant noisy bundles when a focused artifact is enough
- Do not invent unsupported fields unless the renderer has added them
- Do not handcraft packed envelopes manually if helper utilities are available; construct logical envelopes and let transport logic pack automatically
