# Tracking and Integrations

Always verify current provider documentation before implementing syntax, SDK calls, supported event names, consent requirements, or API payloads when those details may have changed.

## General rules

- Instrument conversions at confirmed business boundaries, not optimistic button clicks.
- Preserve existing analytics abstractions when available.
- Keep browser and server tracking failures non-blocking.
- Never expose server secrets in client bundles.
- Respect existing consent and opt-out behavior.
- Use stable transaction/order identifiers.
- Deduplicate paired browser/server events where the provider supports it.
- Preserve UTM and provider-specific attribution context when supported and lawful.
- Do not log raw identity data or secret tokens.

## OpenAI Ads

When OpenAI Ads is in scope:

- Prefer the installed `openai-ads-conversions-setup` skill if available.
- Verify current official OpenAI Ads documentation before concrete implementation.
- Support Measurement Pixel, CAPI, or Pixel+CAPI according to the runtime and authorization.
- Prefer Pixel+CAPI for web purchase funnels when both are supported and permitted.
- Use one logical Pixel/data-source identity where required by current documentation.
- Use a shared event identifier for the same logical browser/server conversion when deduplication is supported.
- Preserve `oppref` attribution context according to current OpenAI Ads guidance.
- Keep CAPI secrets server-side only.
- Use documented standard events. Do not invent event names.
- Treat a verified paid order as the purchase conversion boundary.
- Validate that tracking failure cannot block checkout/order completion.

## Meta

When Meta measurement is in scope:

- Reuse existing Meta Pixel/CAPI integration when present.
- Prefer Pixel + CAPI for purchase-critical funnels when supported and authorized.
- Use the same logical event identifier for deduplication when supported.
- Fire Purchase at verified purchase success, not on checkout click.
- Preserve browser attribution cookies/parameters according to current Meta guidance and consent policy.
- Keep access tokens server-side.
- Use Test Events or equivalent validation when access exists.

## GA4

When GA4 is in scope:

- Reuse existing gtag/GTM/dataLayer conventions.
- Implement ecommerce events that match the actual funnel.
- Typical purchase funnel events:
  - `view_item`
  - `add_to_cart` when a cart action exists
  - `begin_checkout`
  - `purchase`
- Use a stable unique `transaction_id` for purchase.
- Ensure currency/value/item details are internally consistent.
- Verify with DebugView or equivalent tools when available.

## Google Tag Manager

When GTM exists:

- Prefer extending the existing data layer and container patterns instead of adding parallel direct tags.
- Keep environment separation clear.
- Validate triggers so purchase events do not fire twice.
- Preserve Consent Mode behavior when configured.

## Google Ads

When Google Ads conversion tracking is in scope:

- Determine whether conversions are imported from GA4 or sent directly.
- Avoid double-counting the same purchase through two primary conversion actions.
- Use the real transaction/order identifier when supported.
- Implement Enhanced Conversions only when authorized and compatible with consent/privacy policy.
- Validate account IDs, conversion IDs, and labels from the user's connected configuration; do not guess them.

## Google Search Console

Search Console is not a purchase analytics system.

Use it for:

- property ownership verification;
- sitemap submission/discovery;
- indexability monitoring;
- search performance visibility.

For Domain properties, DNS verification may require a TXT record and may be a human dependency when the agent lacks DNS access.

## Consent

Before adding advertising measurement, inspect:

- CMP;
- regional consent behavior;
- opt-out state;
- Google Consent Mode;
- existing tracking gates;
- user matching policy.

Do not silently bypass consent logic to improve attribution.

## Tracking matrix template

| Platform | Browser | Server | Primary conversion | Dedupe key | Attribution | Consent gate | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenAI Ads | Pixel / N/A | CAPI / N/A | verified paid order | shared event ID if paired | oppref / documented context | required policy | provider/debug verification | pending |
| Meta | Pixel / N/A | CAPI / N/A | Purchase | shared event ID if paired | documented browser/server context | required policy | Test Events | pending |
| GA4 | gtag/GTM | optional | purchase | transaction_id | campaign params | consent-aware | DebugView | pending |
| Google Ads | tag/import | optional | purchase | transaction/order ID where supported | Google attribution | consent-aware | conversion diagnostics | pending |
| Search Console | N/A | N/A | N/A | N/A | N/A | N/A | ownership + sitemap/index checks | pending |
