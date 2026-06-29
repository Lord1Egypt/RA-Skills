# Chrome Extension Maintenance And Evolution Playbook

Date: 2026-06-11

Use this playbook to maintain Chrome extensions in a portfolio without drifting away from Chrome Web Store policy, Chrome MV3 behavior, user trust, and measurable product value.

## Core Rule

Do not treat a Chrome extension as a one-time ZIP. Treat it as a small regulated product with a public promise, a privacy contract, a browser runtime, a support surface, a listing funnel, and a release history.

Every release must answer:

- What user job does this version improve?
- What permission, data-flow, or policy risk changed?
- What browser evidence proves the primary flow still works?
- What listing, landing, screenshot, privacy, and support copy need matching updates?
- What metric should move after release?

## Current Source Anchors

Verify these again when a release or public claim depends on current policy or platform behavior:

- Chrome Web Store Program Policies: https://developer.chrome.com/docs/webstore/program-policies
- Chrome Web Store privacy policy guidance: https://developer.chrome.com/docs/webstore/program-policies/privacy
- Limited Use policy: https://developer.chrome.com/docs/webstore/program-policies/limited-use
- User data FAQ: https://developer.chrome.com/docs/webstore/program-policies/user-data-faq
- Declare permissions: https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions
- MV3 service-worker lifecycle: https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle
- Migrate to extension service workers: https://developer.chrome.com/docs/extensions/develop/migrate/to-service-workers
- Extension security and remote-code rules: https://developer.chrome.com/docs/extensions/develop/migrate/improve-security
- Manifest CSP: https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy
- Extension E2E testing: https://developer.chrome.com/docs/extensions/how-to/test/end-to-end-testing
- Test service-worker termination: https://developer.chrome.com/docs/extensions/how-to/test/test-serviceworker-termination-with-puppeteer
- Extension updates: https://developer.chrome.com/docs/webstore/update
- CWS rollback: https://developer.chrome.com/docs/webstore/rollback
- Extension update lifecycle: https://developer.chrome.com/docs/extensions/develop/concepts/extensions-update-lifecycle
- Chrome i18n API: https://developer.chrome.com/docs/extensions/reference/api/i18n
- CWS discovery: https://developer.chrome.com/docs/webstore/discovery
- Chrome Extensions what's new: https://developer.chrome.com/docs/extensions/whats-new

## Portfolio Operating Loop

Weekly:

- Pull CWS installs, uninstalls, weekly users, impressions, page views, sources, regions, and languages.
- Pull Search Console clicks/impressions for root and product subdomains.
- Check GA only for acquisition events; do not use GA as retention truth unless extension-safe key events are configured.
- Review support messages, Chrome Web Store reviews, and crash/error artifacts.
- Triage each extension as `invest`, `maintain`, `pause promotion`, or `sunset candidate`.

Per release candidate:

- Identify one primary user flow and one metric this release should improve.
- Run manifest, permission, privacy, remote-code, locale, accessibility, and package checks.
- Run Playwright/Puppeteer E2E against the unpacked extension.
- Run service-worker restart/termination checks for any extension with a background worker.
- Capture desktop and mobile-width evidence for popup, side panel, options, and main page effects.
- Run ClawPatch or record why it cannot run.
- Update listing copy, privacy page, support page, landing page, `llms.txt`, screenshots, and CWS privacy declarations if product behavior or data flow changed.

Monthly:

- Revisit CWS policies, Chrome Extensions What's New, and MV3 API changes.
- Audit dependencies, remote-code risk, CSP, bundled libraries, and permission creep.
- Recheck localization coverage and RTL rendering.
- Review old screenshots and listing copy for promise drift.
- Review store category, homepage/support/privacy URLs, and sitemap/Search Console status.

Quarterly:

- Keep/invest if retained weekly users are growing or strategically valuable.
- Maintain if stable and low-risk.
- Pause promotion if P0/P1 product, privacy, or release issues are open.
- Sunset if install curiosity does not convert to durable use and the product does not feed a stronger product.

## Release Gate

Use this as a hard checklist before uploading a ZIP, submitting a CWS draft, or broadly promoting an extension.

1. Purpose gate: one visible purpose, no surprise behavior, no broad feature stuffing.
2. Permission gate: no permission without an attached user action and listing/privacy justification.
3. Data-flow gate: document browser data, local storage, backend calls, third-party APIs, retention, and deletion path.
4. MV3 runtime gate: service worker has no durable global state assumptions; long work has recovery and timeout handling.
5. Security gate: no `eval`, `new Function`, remote scripts/styles, CDN execution, unsafe CSP, hidden telemetry, or dynamic hosted code.
6. UX gate: first action is obvious in under five seconds; empty/loading/error/success states are plain-language.
7. Accessibility/i18n gate: keyboard path, labels, focus, `default_locale`, complete locale keys, placeholder validation, RTL smoke.
8. Browser E2E gate: load unpacked extension, run real user flow, assert console/page errors are zero, capture screenshots.
9. Listing/landing gate: CWS title, summary, detailed description, screenshots, landing, support, privacy, and `llms.txt` match actual behavior.
10. Package gate: version increased, ZIP inspected, no stale dist, no missing assets, no unexpected host permissions.
11. Review gate: ClawPatch/gstack/persona review complete; all P0/P1 findings closed or promotion is blocked.
12. Publish gate: user approval required before upload, submit, unpublish, rollback, or public promotion.

## Issue Taxonomy

- `P0 product`: primary flow broken, data loss, unsafe behavior, severe expectation mismatch.
- `P0 privacy`: undisclosed collection/sharing, wrong privacy declaration, hidden telemetry, backend mismatch.
- `P1 release`: package cannot load, review-blocking manifest issue, open high review finding.
- `P1 permission`: unnecessary broad host/API permission or new warning not justified.
- `P1 listing`: CWS/landing promise does not match actual extension.
- `P1 retention`: high uninstall ratio, low weekly-user conversion, weak onboarding.
- `P2 search`: poor CWS/Search Console discoverability, weak screenshots, incomplete listing metadata.
- `P2 localization`: missing locale, placeholder mismatch, broken RTL, untranslated critical state.
- `P3 polish`: copy, spacing, screenshots, FAQ, support clarity.

## Metrics That Matter

Primary health:

- Weekly users.
- Uninstall/install ratio.
- CWS impressions to page views.
- Page views to installs.
- Reviews/support complaints by theme.

Secondary acquisition:

- Landing CTA clicks.
- Search Console queries/pages.
- CWS traffic source rows.
- Region/language usage.

Do not over-optimize for installs if weekly users stay flat or uninstall ratio rises.

## Evolution Patterns

Prefer these:

- Narrow one-click workflows over broad dashboards.
- `activeTab` and click-triggered scripting over persistent host permissions.
- Local-first output with optional remote improvement only after explicit user action.
- Clear state labels: ready, reading, improving, copied, exported, failed.
- Small versioned releases with one measurable behavior change.
- Locale expansion based on actual language/region usage and support burden.

Avoid these:

- Adding AI, background crawling, or host permissions to compensate for unclear product value.
- Shipping a landing promise before the extension flow proves it.
- Broad promotion while CWS review, privacy, or P0/P1 findings are unresolved.
- Treating screenshots as decoration; screenshots must prove the real first-use path.
- Keeping dead extensions in equal portfolio prominence.

## Reviewer Personas

- First-time user: Can they complete the primary task without reading docs?
- Privacy reviewer: What data leaves the browser, who receives it, and did the user explicitly trigger it?
- CWS reviewer: Does manifest/listing/privacy/permission behavior match policy?
- Power user: Is the output useful after the third use, not just novel once?
- Localization reviewer: Does the product still fit in German/Russian/Hindi, and does Arabic render coherently?
- Portfolio reviewer: Does this extension deserve shelf space versus the current winners?

## Default Ship Decision

Green:

- Primary browser flow works.
- Privacy and permission story is accurate.
- Listing and landing match.
- No untriaged P0/P1 findings.

Yellow:

- Usable for test/private/beta or quiet release.
- Do not broadly promote.

Red:

- Promise mismatch, privacy ambiguity, missing browser evidence, high uninstall risk, or open release blocker.

Default stance: yellow until evidence proves green.
