# OpenAI Ads — what is actually required

Source of truth, checked 2026-10-19. Re-check with `scripts/fetch-official.mjs` before
telling a client "OpenAI requires X" — policies change (ad policy is on v1.6).

| Source | URL |
|---|---|
| Ad policies (v1.6, 2026-09) | https://openai.com/policies/ad-policies/ |
| Crawler guidance (help center) | https://help.openai.com/en/articles/20001243-advertiser-guidance-for-allowing-openai-web-crawlers |
| Measurement Pixel | https://developers.openai.com/ads/measurement-pixel |
| Image Tag (no-JS) | https://developers.openai.com/ads/image-tag |
| Supported events | https://developers.openai.com/ads/supported-events |
| Ads docs index | https://developers.openai.com/ads/llms.txt |

## Contents
1. Hard requirements (an ad is rejected or cannot serve)
2. Content rules that apply to the landing page
3. Not required by OpenAI (our own standards — say so when you cite them)
4. Pixel facts that matter for page design

## 1. Hard requirements

- **OAI-AdsBot must be able to fetch the page.** "You must allow OAI-AdsBot. We recommend
  allowing both OAI-AdsBot and OAI-SearchBot." Blocks that count: robots.txt Disallow,
  WAF/CDN 403, CAPTCHA / JS challenge, login or password, geo rules, rate limiting (429).
  On a hosting platform with password protection this means **password protection off**.
- **The page must be reviewable.** "If an ad or landing page cannot be reviewed or
  evaluated by our systems, it is not eligible to serve." App-store links, deep links,
  documents, region-locked or redirecting destinations "may not provide enough crawlable
  content". → static HTML, no self-redirect (geo routing only rewrites link hrefs).
- **Destination integrity.** The landing page must be clearly related to the advertiser and
  the promoted offer, accurately represent them, and not mislead.
- **End-to-end consistency.** Creative, image and landing page are reviewed together; an
  approved creative may not link to a page with disallowed content.
- Support "can't manually bypass crawler validation" — fix access, then re-upload/resubmit.

JS is **not** forbidden. The rule is crawlability/reviewability, which is why we keep all
copy in static HTML and use JS only for routing, events and the consent banner.

## 2. Content rules that bite on landing pages

- Truthful, no unsupported claims about features, price, results, affiliations,
  comparisons. "Free X" claims need their eligibility conditions on the page.
- Allowed categories at launch: lifestyle & home, local services, **travel & experiences**,
  digital products & education. Finance / health / legal: US only, approved advertisers,
  case by case. Not allowed: dating/sexual, alcohol & tobacco (incidental mention OK when
  not the focus), gambling (casino *resort stays* OK), political, recreational drugs,
  counterfeit, weight-loss/detox style health claims, specific job/housing listings.
- No impersonation, no look-alike domains, no imitation of the ChatGPT UI.
- Advertiser may only use trademarks/logos they own or are licensed to use. → for agency-
  built pages use our own mark as favicon unless the client authorises their logo.
- Geographic compliance: the advertiser must follow the laws of the markets it targets
  (this is where privacy/cookie rules come in — see privacy-consent.md).

## 3. NOT OpenAI requirements (internal standards)

Say "our checklist recommends", never "OpenAI requires", for:
- contact phone / email on the page;
- privacy-policy link (legally advisable when a pixel runs — see privacy-consent.md);
- ≥ 300 words, single h1, FAQ + FAQPage JSON-LD, Offer schema, CTA above the fold;
- the six-dimension "audit" framework from third-party training material — it is a vendor
  framework, not an OpenAI requirement; one tool built on it misreported 3 of 5 failures on
  the first airline page because its regexes were tied to its own generator's class names.

## 4. Pixel facts that shape the page

- Install: official stub + `oaiq("init", {pixelId})`; consent must be set **before** init:
  `oaiq("consent", false)`. "When consent is false, the Pixel doesn't send measurement-event
  pings. … blocked events aren't replayed." → hold events yourself and replay on Accept.
- Consent defaults to true unless set false or the Pixel finds a stored denial.
  `oaiq("consent", false)` deletes both cookies.
- Cookies (first-party): `__oppref` 30 days (reset each time a non-empty `oppref` URL
  param is seen), `__obref` 365 days. Not set on `file://` pages (Chrome disables cookies).
- The Pixel captures `oppref` from the landing URL automatically and attaches it to events
  → forward `oppref` onto outbound CTA links too, so the brand site can attribute.
- Custom events: `oaiq("measure", "custom", {type: "custom"}, {custom_event_name})`;
  name 1–64 chars `[a-z0-9_-]`, must start/end alphanumeric, must not collide with a
  reserved (standard) event name.
- Standard events and their data type: `page_viewed`, `contents_viewed`, `items_added`,
  `checkout_started`, `order_created` → `contents`; `lead_created`, `registration_completed`,
  `appointment_scheduled` → `customer_action`; `subscription_created`, `trial_started` →
  `plan_enrollment`; `custom` → `custom`. `contents` array is optional.
- Endpoint: `POST https://bzr.openai.com/v1/sdk/events?pid=…` → **202** = accepted.
  Chrome also logs `ERR_ABORTED` for the same keep-alive request; that is not a failure.
  SDK `https://bzrcdn.openai.com/sdk/oaiq.min.js`, config `…/pixel-config/v1/<pixelId>.json`.
- CSP (if a site has one): script-src bzrcdn.openai.com; connect-src bzr.openai.com and
  bzrcdn.openai.com; img-src bzr.openai.com.
- 202 means received, not "matched to a conversion" — confirm in Ads Manager → the data
  source's event log.
