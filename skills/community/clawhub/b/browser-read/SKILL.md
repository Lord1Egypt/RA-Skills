---
name: browser-read
description: Extract readable content from browser pages as markdown. Use when web_fetch fails (bot protection, auth-required pages, Twitter/X, LinkedIn) and you already have the page open in the browser.
---

# browser-read

Extract readable text from an already-open browser page and return markdown, suitable for pages where `web_fetch` is blocked or missing auth context.

## When to use

- `web_fetch` returned an error or empty content.
- Page requires authentication/cookies/session state available only in the browser.
- You need text extraction from Twitter/X or LinkedIn timelines/articles where screenshot/OCR was previously used.

## When NOT to use

- `web_fetch` already returns good markdown/text (faster and cheaper).
- Purely static pages where normal fetch is sufficient.

## Steps

1. Navigate to the URL with `browser navigate`.
2. Read extraction script from `~/clawd/skills/browser-read/extract.js`.
3. Run `browser act` with `kind=evaluate` and pass the script contents as `fn`.
4. Script returns `{title, content, excerpt, byline, siteName, length}` where `content` is markdown.
5. If extraction fails or returns empty content, script falls back to `document.body.innerText`.

## Example (tool calls)

```json
{
  "action": "navigate",
  "targetId": "...", 
  "url": "https://example.com"
}
{
  "action": "act",
  "targetId": "...",
  "kind": "evaluate",
  "fn": "(() => { ... return {title, content, excerpt, byline, siteName, length}; })()"
}
```

## Notes

- `extract.js` is a self-contained IIFE so it can be passed directly as the `fn` value to `browser act`.
- Keep in mind this is a lightweight extractor; it intentionally strips script/style/nav/header/footer/aside/cookie/ad elements before conversion.
