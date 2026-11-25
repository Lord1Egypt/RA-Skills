# Execution Workflow

Use this workflow after the one-time intake is complete.

## 1. Normalize intake

Create an internal structured Intake Manifest containing:

- known facts;
- user constraints;
- JEV-authorized decisions;
- technical permissions;
- production permissions;
- account/connector availability;
- secret references;
- human-only dependencies;
- unresolved assumptions.

Do not expose raw secrets.

## 2. Create Human Dependency Manifest

For each potential dependency record:

- system/provider;
- capability affected;
- whether agent access exists;
- whether permission exists;
- whether a secret reference exists;
- whether a human-only action is expected;
- whether work can continue around it;
- final manual action if still unresolved.

Continue execution after creating this manifest.

## 3. Inspect existing implementation

When a repository exists:

- detect framework, router, runtime, package manager, database, ecommerce platform, payment provider, analytics, deployment, secrets pattern, tests, and CI/CD;
- search for existing product, cart, checkout, order, payment, analytics, email, SEO, consent, and deployment code;
- identify existing domain docs;
- preserve working patterns unless there is a verified reason to change them.

## 4. Product and market research

Verify current product information and gather market evidence.

Produce an internal research summary:

- verified facts;
- unverified claims;
- likely buyers;
- buying occasions;
- competitor offer patterns;
- price range;
- strengths;
- weaknesses;
- objections;
- trust requirements;
- real urgency drivers.

Do not publish unverified claims.

## 5. JEV selects the commercial strategy

Choose:

- primary buyer;
- primary use case;
- positioning;
- promise/value proposition;
- price within authority and constraints;
- quantity tiers/bundles;
- free-shipping threshold if authorized;
- upsell/order-bump logic if justified;
- primary CTA;
- trust strategy.

Record meaningful decisions in `JEV_DECISIONS.md` when a repository is available.

## 6. Funnel architecture

Prefer the shortest credible path.

Typical purchase funnel:

- landing/product page;
- offer selection;
- checkout;
- payment;
- verified order;
- confirmation;
- recovery path for failed/cancelled payment.

Add cart, upsell, email capture, or account creation only when there is a business or platform reason.

## 7. Copy and content

Write complete production copy in the configured storefront language(s).

Cover:

- hero;
- value proposition;
- product in action;
- included items;
- use cases;
- offer selector;
- product details;
- objection handling;
- shipping/returns summary;
- final CTA;
- transactional confirmation content;
- SEO metadata.

Keep claims evidence-based. Shipping copy in particular: state a dispatch window, delivery estimate, or carrier only when it is confirmed. For dropshipping, pre-order, or test-the-demand launches there is usually no fixed ETA — keep the shipping summary generic (returns window, who the seller is) and promise no delivery time rather than inventing one.

## 8. Visual system and assets

Audit available assets and choose a coherent system for:

- typography;
- spacing;
- buttons;
- cards;
- offer selector;
- trust components;
- responsive behavior;
- product imagery;
- social share imagery.

Do not materially alter product appearance in generated visuals.

## 9. Implement commerce

Implement or integrate:

- offer/variant state;
- price calculation;
- cart state if needed;
- shipping/tax display;
- checkout creation;
- payment provider flow;
- payment verification;
- webhook handling;
- idempotent order creation;
- failed/cancelled recovery;
- order confirmation;
- fulfillment trigger when available.

## 10. Implement measurement

Use `tracking-and-integrations.md`.

Create a tracking matrix with:

- platform;
- browser event;
- server event;
- conversion boundary;
- event ID/dedupe strategy;
- attribution data;
- consent gate;
- validation method;
- status.

## 11. SEO and search readiness

Implement as applicable:

- title/meta description;
- canonical URL;
- Open Graph;
- product structured data;
- sitemap;
- robots;
- hreflang;
- Search Console verification support;
- indexability checks.

## 12. Consent/privacy integration

Preserve existing consent architecture.

Do not fire advertising/user-matching events in a way that conflicts with the configured consent policy.

Keep tracking failure non-blocking for the core purchase flow.

Generate the required legal pages and consent flow with `web-compliance-builder` when the site lacks them.

## 13. Deploy

Within granted authority:

- configure environment variables using references, never raw secrets in source;
- deploy staging/preview;
- test;
- deploy production;
- configure domain/DNS/SSL where authorized;
- preserve email DNS records;
- verify canonical domain and redirects.

Use `dokploy-deploy` when the target is a Dokploy instance.

If a human-only action blocks production, leave the deployment fully prepared and document the exact final action.

## 14. QA

Test the real customer journey.

At minimum verify:

- landing loads;
- product assets load;
- offer selection works;
- price/discount calculations are correct;
- checkout receives correct product and quantity;
- final amount is visible before payment;
- test payment succeeds when credentials allow;
- success redirect alone is not treated as authoritative paid state;
- webhook/provider verification updates one order exactly once;
- payment retry does not duplicate a paid order;
- failed/cancelled payment recovers cleanly;
- transactional email behavior is correct when available;
- OpenAI/Meta/Google events fire at correct boundaries;
- purchase event is not fired on mere button click;
- consent behavior is respected;
- mobile layout works;
- desktop layout works;
- keyboard/focus behavior works;
- no broken links;
- no placeholder copy remains;
- no secrets are exposed;
- no obvious console/runtime errors remain;
- performance is acceptable for the implementation context.

Run `landing-launch-check` before production go-live (SEO, AEO/GEO, EU compliance).

### Visual QA method (avoid false reads)

When judging the rendered page from screenshots:

- Verify the viewport a real user actually sees: scroll the target section into view (`el.scrollIntoView({block:'center'})`), let lazy assets settle, then screenshot that viewport. A full-page screenshot renders below-the-fold `loading="lazy"` images as blank white boxes even though they load on real scroll — a blank in a full-page capture is not proof of a broken image. Confirm with the element's `naturalWidth`/`complete` before concluding an image failed.
- Check that no overlay covers product imagery or the primary CTA — the consent banner, sticky bars, and modals are the usual offenders. Reproduce with the consent banner actually showing (clear the consent cookie / load fresh), because a dismissed banner hides the defect.
- Confirm an image you suspect is "broken" actually loads at its URL (`curl -o /dev/null -w "%{http_code} %{size_download}"`) before editing layout. A 200 with real bytes means the problem is layout/overlay, not the asset.
- When the user reports a visual defect (especially via a screenshot), treat their screenshot as primary evidence and reproduce it in their viewing terms; do not dismiss it because your own render looked fine.

Fix issues found when possible instead of only listing them.

## 15. Conversion review

Review as a first-time buyer.

Within seconds the page should answer:

- what is this;
- who is it for;
- what do I get;
- what does it cost;
- why buy now;
- how do I buy;
- when will it arrive;
- what happens if something goes wrong.

Remove unnecessary decisions and friction.

## 16. Final handoff

Use `delivery-report.md`.

Do not claim a system is live, verified, indexed, or tracking correctly unless it was actually verified.
