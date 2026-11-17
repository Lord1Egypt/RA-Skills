# Privacy, cookies and consent by target country

Not legal advice and not an OpenAI rule — OpenAI only says advertisers must follow the laws
of the markets they target. Present this as general practice and let the client's legal team
decide. The pixel sets `__oppref` (30 d) and `__obref` (365 d) first-party cookies and, by
default, consent is on.

| Market | Law | Usual expectation | Page setting |
|---|---|---|---|
| UK | PECR + UK GDPR | prior opt-in for non-essential (ads/analytics) cookies; reject as easy as accept | `consent.countries` += `GB` |
| EU/EEA (FR, DE, ES, IT, NL, IE…) | ePrivacy + GDPR | same as UK | add each country — and its time zones to `geo.js` |
| Canada | PIPEDA; Québec Law 25 | notice; Québec wants tracking off by default | privacy link; consider `CA` if Québec matters |
| US | state laws (CCPA/CPRA…) | privacy notice, opt-out of "sharing", honour GPC | privacy link |
| Singapore | PDPA | notification + (deemed) consent | privacy link |
| Australia | Privacy Act | privacy policy; no cookie-banner mandate | privacy link |

In every market a footer privacy link to the client's own policy is cheap and expected —
reuse the client's existing per-country pages (the airline sites all had
`/<CC>/GB/privacy-policy/` and `/<CC>/GB/cookies/` in their footer).

## How the consent banner works (engine)
- `shared/geo.js` runs in `<head>` before the pixel: resolves country, reads
  localStorage `lp_measurement_consent` → `LP_GEO.consent` = `not_required` | `pending` |
  `granted` | `denied`.
- Pixel snippet: `pending`/`denied` → `oaiq("consent", false)` before init and no
  `page_viewed`; `granted` → `oaiq("consent", true)`.
- `lp.js` holds events while `pending`; Accept → `consent(true)`, sends `page_viewed`,
  flushes held events; Decline → drops them. Footer "Cookie settings" reopens the banner.
- Accept and Decline have identical styling on purpose.
- While the banner is up, `body` gets bottom padding equal to the banner height so the
  footer (with the policy links) can scroll above it.

## Known limits — tell the client
- The banner decision uses time zone/language, **not IP**: it must be made before pixel
  init and cannot wait for an async IP lookup. A UK-IP visitor whose computer is set to
  another zone (typical VPN tester) is routed to the UK site but sees no banner. Real UK
  residents have a UK time zone. To test: DevTools → ⋮ → 更多工具 → 传感器 (Sensors) →
  位置 London, keep DevTools open, reload. In Chinese DevTools the command menu needs
  `>传感器`, not "Show Sensors".
- Consent-country visitors who never accept produce no conversions → less attribution.
- With JS off the country is unknown and the `<noscript>` Image Tag still sends
  `page_viewed`.
