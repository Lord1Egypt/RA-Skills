# Retrieval Playbook

Use this reference when deciding how to retrieve content reliably.

## Default Order

1. `web_fetch`
2. `r.jina.ai`
3. interactive browser fallback
4. user help only if truly required

## When `web_fetch` Is Enough

Use the result directly when it contains:
- a clear title
- a coherent main body
- no obvious anti-bot or login-wall text
- enough content to believe the article is complete

## When to Try `r.jina.ai`

Use Jina mirror when:
- `web_fetch` is blocked
- only title/teaser is returned
- the site renders poorly via direct fetch
- the article body appears missing

Treat Jina as a retrieval fallback, not a separate source.

## When to Escalate to an Interactive Browser Fallback

Escalate when:
- fetch-based retrieval returns shell content
- the page is heavily client-rendered
- the site uses short-link redirects
- the page requires clicking to expand content
- the user asks for comments / replies / discussion sentiment
- the visible content depends on rendered DOM state

## Browser Tactics

After opening the page in the browser fallback:
- inspect the rendered text
- scroll for lazy loading
- click visible expanders
- dismiss simple overlays
- retry once in a fresh tab if the first load looks broken

## Verification Handling

Try simple actions first:
- "continue"
- "verify"
- close modal
- expand section

Only ask the user to step in when the page truly requires human-only action, such as:
- persistent login approval
- hard captcha / drag puzzle that does not clear
- account-specific authorization

## Failure Reporting

Report plainly:
- what method failed
- what fallback you tried
- whether the remaining blocker is a login/verification/access issue

Never summarize invisible content.
