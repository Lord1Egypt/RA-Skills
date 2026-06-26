---
name: Browser Fu
description: "Fixes browser automation failures. Snapshot-first workflow + API discovery behind any website UI. Use when: 'browser not working', 'can't click', 'flaky UI', 'DOM not exposed', 'scrape website', 'browser keeps failing', 'automate this website', 'web scraping', 'element not found'."
---

# Browser Fu 🥊

Stop fighting the DOM. Read it first, find the API behind it, skip the UI entirely when possible.

## The Rule

**Never blind-click. Always snapshot first.**

```
1. browser snapshot  →  read the page, get element refs
2. browser act       →  use refs from snapshot (e.g. ref="e12")
3. browser snapshot  →  verify what changed
```

If the snapshot doesn't show what you need, the element isn't in the DOM. Don't guess. Don't retry the same approach.

## Decision Tree

On any browser task, follow this order:

1. **Can I skip the browser entirely?** Check if a CLI tool, API, or `web_fetch` handles it. If yes, don't open the browser.
2. **Can I find the underlying API?** See `references/api-discovery.md`. Most SPAs make fetch/XHR calls you can replicate directly. This is 10x faster and more reliable than UI automation.
3. **Can I do it with snapshot + act?** Snapshot, find the ref, act on it. One action per snapshot cycle.
4. **Does the page need time to load?** Use `loadState: "networkidle"` or a brief wait before snapshotting. SPAs often render asynchronously.
5. **Still not working?** The site likely has anti-bot protection. Report it, don't retry blindly.

## Common Failures and Fixes

| Symptom | Wrong approach | Right approach |
|---|---|---|
| "Element not found" | Click by text/selector guess | Snapshot first, use exact ref |
| "DOM not exposed" | Give up | Snapshot with `refs="aria"`, or check network tab for API |
| Blank/empty page | Retry same URL | `loadState: "networkidle"`, then snapshot. If still blank, JS-heavy SPA, try `web_fetch` or find API |
| Clicking does nothing | Click again harder | Snapshot after click to check state. Maybe it DID work but page re-rendered |
| Login wall | Try to automate login | Use `profile="user"` for existing session cookies |
| Infinite scroll | Scroll and pray | Find the pagination API endpoint instead |

## API Discovery (the power move)

Most modern websites are SPAs with REST/GraphQL APIs behind the UI. See `references/api-discovery.md` for the full procedure:

1. Open the page in browser
2. Check network requests (console tool or snapshot the page and look for fetch patterns)
3. Find the data endpoint
4. Call it directly with `web_fetch` or `exec curl`

This turns a 2-hour flaky scrape into a 2-minute clean data pull.

## Snapshot Best Practices

- Use `refs="aria"` for stable cross-call references
- Keep the same `targetId` across snapshot/act pairs (don't switch tabs accidentally)
- For complex pages, use `depth` to limit how deep the DOM tree goes
- `compact: true` reduces token usage on large pages
- For token-heavy pages where snapshots are too large, pair with predicate-snapshot for ML-ranked element pruning (~95% fewer tokens)

## When to NOT Use Browser

- Reading public web pages → `web_fetch` (faster, no browser overhead)
- Search queries → `web_search` (Brave API)
- Known APIs (GitHub, Stripe, etc.) → use their CLI/API directly
- Pages that return empty via `web_fetch` → then use browser

## Safeguards

- Never store or output passwords, session tokens, or cookies found in browser state
- Never automate purchases, payments, or irreversible actions without explicit user approval
- If a site blocks automation, respect it. Don't circumvent CAPTCHAs or bot detection
