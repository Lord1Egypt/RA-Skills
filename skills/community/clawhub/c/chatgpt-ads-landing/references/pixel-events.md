# Pixel events — mapping, testing, debugging

## Mapping the client's Ads Manager events
The client (or Ads Manager → Conversions → data source) gives a pixel ID and a list of
conversion events, often as raw snippets like
`oaiq("measure","custom",{type:"custom"},{custom_event_name:"page_view_action"})`.
Map each one to *when* it should fire on this page, then express it in `pixelEvents`:

| Typical event | page.json | Fires when |
|---|---|---|
| `page_viewed` | automatic (build) | page load (or on Accept for consent visitors) |
| `contents_viewed` (standard) | engagement `{visible: "#id", standard: true}` | that section is ≥ 50% in view |
| scroll depth (custom) | engagement `{scrollPercent: 50}` | 50% of the page scrolled |
| dwell time (custom) | engagement `{seconds: 30}` | 30 s of *foreground* time |
| CTA click (custom) | `click: "click_cta"` | any `data-cta` click |
| per-button extra | `ctas.<name>.event` | that button only |

Ask before inventing a trigger: "contents_viewed when the user reaches section X — OK?"
Purchases/leads that happen on the client's own site cannot be fired from this page; the
client must install the pixel (or Conversions API) there, and `oppref` forwarding makes
attribution possible.

## Verifying
- `node <skill>/scripts/verify.mjs <url> --proxy http://<your-proxy> --only pixel`
  loads the page in Chrome, scrolls to each `visible` target, scrolls to the bottom,
  clicks a CTA (navigation suppressed), waits for the longest `seconds` event, and checks
  every expected event was POSTed, answered 2xx and carried the test `oppref`.
- The preflight prints the proxy's exit country. **If it is CN the SDK is 403'd** and pixel
  checks are skipped — ask the user to switch the VPN to an overseas node. The user's proxy
  is typically `http://<your-proxy>` (Clash); its exit changes when they switch nodes or
  modes, so never assume yesterday's exit.
- Without a working proxy, the strongest local evidence is the stub queue: before the SDK
  loads, `window.oaiq.q` holds every call the page made — but say clearly that this proves
  *the page calls the pixel*, not that OpenAI received anything.

## Debugging checklist ("pixel 不触发")
1. Is the live page the new build? `verify.mjs --dist` (byte compare, no cache).
2. Is the SDK reachable from where the tester is? (CN → no.)
3. Console: `LP_CONFIG.pixelEvents`, `LP_GEO`, `LP.consent()` — a consent-country visitor
   who has not accepted sends nothing by design.
4. Network → filter `events` (or `bzr.openai.com`): 202 = accepted. The event name is in the
   request **payload**, not the URL — click the request → 载荷 (Payload) to see
   `custom_event_name`. `ERR_ABORTED` next to a 202 is the keep-alive request, not a failure.
5. Event received but not in Ads Manager → event name must exactly match the data source's
   event; custom names `[a-z0-9_-]{1,64}`. The data source's 事件流 (event stream) only shows
   roughly the last 15 minutes — look right after testing, and tell the user to do the same.
