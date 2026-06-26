---
name: browser-read-x
description: Extract the main X/Twitter post or article content from a page that is already open in the browser (using browser act evaluate).
---

# browser-read-x

Site-specific extractor for **X/Twitter**.
It is tuned to return the central post/article content while filtering
UI chrome such as sidebars, trends, login/signup prompts, reaction metrics,
and article footer/promotional blocks.

## Use case

- `web_fetch` is noisy or blocked (auth-required/public X/X-protected pages).
- You need tweet/article text from an already-open X page in browser.
- You specifically want the main status/article body, not sidebar or CTAs.

## How to use

1. Navigate to the URL with `browser navigate` (or ensure the page is already open).
2. Run `browser act` with `kind="evaluate"` and pass the contents of
   `skills/browser-read-x/extract.js` as `fn`.
3. The script returns:
   - `title`
   - `content` (plain markdown-ish text with reduced X UI noise)
   - `excerpt`
   - `byline`
   - `siteName`
   - `length`
   - `url`

## Example

```json
{
  "action": "act",
  "kind": "evaluate",
  "targetId": "...",
  "fn": "(() => { ... })()"
}
```

## Notes

- Self-contained and safe to pass directly as JS to `browser act`.
- The script prefers the specific status/article node on X and falls back
  to generic article/main selection if that fails.
- For non-X pages it still behaves similarly to the generic extractor
  (best-effort cleanup + markdownish text conversion).