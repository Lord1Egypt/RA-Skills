# page.json and index.html contract

## Contents
1. page.json fields
2. index.html tokens and data attributes
3. Content rules (what makes a page pass review and convert)

## 1. page.json

```jsonc
{
  "_comment": "…",                       // any "_comment" key is free text — never put {{…}} in it (check flags it as a placeholder)
  "url": "https://your-site.example.com/", // site root; REPLACE_WITH_SUBDOMAIN until the first deploy
  "title": "Brand · Campaign",           // page_viewed contents.name
  "pixelId": "…",                        // empty = no pixel installed (check fails)
  "contentId": "brand_campaign",         // page_viewed contents.id
  "deploy": { "siteId": "123" },         // written by publish.mjs after the first deploy; not shipped to the page
  "routing": {
    "sites": { "US": "https://…?utm_…", "GB": "…" },  // ISO-2 → client's tracked landing URL, exactly as the client sent it
    "fallback": "https://…",             // visitor in no listed country; also the no-JS href of geo CTAs
    "forwardKeys": ["oppref", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"],
    "version": "v1",                     // appended as v= on CTA links
    "ipLookup": true                     // IP country overrides time zone when it is a listed country
  },
  "ctas": {
    "hero":    { "dest": "geo" },        // routed per visitor
    "book_us": { "dest": "US", "event": "optional_extra_custom_event" }   // fixed country
  },
  "links": {                             // footer compliance links, routed like CTAs but no params/events
    "privacy": { "US": "…", "GB": "…", "fallback": "…" },
    "cookies": { "GB": "…", "fallback": "…" }
  },
  "consent": {                           // omit when no target country needs prior consent
    "countries": ["GB"],
    "text": "We use cookies to measure how our ads on ChatGPT perform. They are only set if you accept.",
    "policyLink": "cookies", "policyText": "Cookie Policy",
    "accept": "Accept", "decline": "Decline", "label": "Cookie consent"
  },
  "pixelEvents": {
    "click": "click_cta",                // custom event on every CTA click
    "engagement": [                      // each fires at most once per page load
      { "event": "contents_viewed", "standard": true, "visible": "#section-id" },
      { "event": "page_view_action", "scrollPercent": 50 },
      { "event": "time_spent_on_page", "seconds": 30 }   // foreground time only
    ]
  }
}
```

Routing order per visitor: IP country (if `ipLookup` and it is in `sites`) → time zone →
browser language region → `fallback`. Destination params win over forwarded ones: a
client's `utm_campaign` is never overwritten by the ad URL's. `lp_cta=<cta>` and `v` are
always appended so clicks are attributable per button.

Time-zone → country table lives in `shared/geo.js` (`TZ_COUNTRY`, `TZ_PREFIX`). When a new
target country is added to `sites`, make sure its zones are in that table, and add a test
zone to `COUNTRY_TZ` in the skill's `scripts/verify.mjs`.

## 2. index.html

| Write | Build turns it into |
|---|---|
| `{{PAGE_URL}}` | page.json `url` (canonical, og:image) |
| `<a data-cta="hero" href="{{cta:hero}}">` | no-JS href = fixed country site, or `fallback` for geo; lp.js rewrites per visitor |
| `<a data-link="privacy" href="{{link:privacy}}">` | `links.privacy.fallback`; lp.js rewrites per visitor |
| `<button data-consent-settings hidden>` | shown only to consent-country visitors; reopens the banner |

Build injects: `window.LP_CONFIG`, inline `shared/geo.js`, the official pixel snippet (with
consent-before-init), `<noscript>` Image Tag, `assets/lp.js`, robots.txt, sitemap.xml.
Never hand-write any of those into the page.

Asset paths are **relative** (`assets/hero.jpg`, in CSS `url("hero.jpg")`). An absolute
`/slug/assets/…` path works locally under a sub-folder but 404s on the platform — that is
how a hero background once disappeared. check.js now verifies CSS `url()`s.

## 3. Content rules

- Everything a reviewer or ChatGPT needs is in static HTML: offer, eligibility, prices with
  validity, FAQ. JS only enhances.
- One h1 that matches the ad headline; the primary CTA before the first h2.
- JSON-LD (`Service`/`Product` + `Offer`s + `FAQPage`) uses the **same words** as the
  visible copy; check.js compares FAQPage questions with the visible FAQ.
- Use only facts from the client's material. Do not invent headings, coupon amounts or
  claims to fill a layout; mark gaps as `填【…】` and ask.
- Images < 800KB each (check warns); the hero image doubles as og:image.
- Favicon: our own simple mark unless the client authorises their logo.
- Body text ≥ 300 words of real content (check enforces).
