---
name: autonomous-product-funnel
description: Build and launch a complete single-product sales funnel end to end (research, offer, copy, design, checkout, payment, analytics, ad pixels, SEO, deploy, QA, handoff) from one comprehensive intake, then continue autonomously without ordinary approval gates. Use when asked to create, rebuild, or launch a product funnel or landing-to-purchase flow.
license: "MIT-0"
metadata: {"version":"1.2.0","category":"marketing","tags":["funnel","ecommerce","checkout","analytics","seo","launch"],"license":"MIT-0"}
---

# Autonomous Product Funnel

## Core contract

Build the funnel as an execution system, not a planning exercise.

Use this sequence:

1. Inspect available context, files, project data, repository, connectors, and supplied URLs.
2. Prefill everything that is already known.
3. Run one comprehensive intake using `references/intake-questionnaire.md`.
4. Produce an internal Intake Manifest and Human Dependency Manifest.
5. Let JEV resolve all routine product, offer, marketing, UX, architecture, implementation, tracking, and deployment decisions within the user's stated constraints.
6. Research and verify current external facts when they materially affect implementation.
7. Build the complete funnel as far as technically possible.
8. Verify checkout, payment state handling, analytics, SEO, deployment, and responsive behavior.
9. Deliver a decision log, QA report, tracking matrix, and exact remaining manual actions using `references/delivery-report.md`.

Do not stop after producing a plan, wireframe, copy draft, or frontend.

The default definition of done is:

`traffic -> landing -> offer -> checkout -> payment -> verified order -> confirmation -> measurement`

## Language policy

Keep the Skill itself, bundled references, internal field names, and internal documentation in English.

At runtime:

- Detect the user's active conversation language from the current interaction.
- Ask the intake questionnaire in that language.
- Write progress updates, explanations, decision summaries, warnings, QA results, and final handoff in that language.
- If the user changes language, follow the user's new language for subsequent user-visible communication.
- Do not translate code identifiers, environment variable names, event names, provider names, URLs, or technical protocol fields.
- Treat the funnel's customer-facing language as a separate business requirement. Use the market/content language specified in intake even when it differs from the user's conversation language.
- If the user requests multiple storefront languages, implement the requested localization strategy; do not infer storefront language solely from chat language.

Example: a Chinese-speaking user may ask the agent in Chinese while the funnel itself is built in Swedish and English.

Keep every chat-facing line — progress notes, status one-liners between tool calls, and the final handoff — in the conversation language. Writing storefront copy in another language (e.g. Swedish) does not change the chat language: do not let the storefront language leak into status updates. Re-check this after any context compaction, which commonly resets it.

## One-intake rule

The intake is the only normal human decision gate.

Before showing it:

- Reuse facts already provided in the conversation.
- Inspect relevant project files and repository configuration when available.
- Inspect supplied product URLs and public product information when allowed.
- Inspect connected services when the required connector is already available.
- Prefill known answers and mark them as detected rather than asking again.

Ask the user to fill only missing fields that materially affect the build, permissions, legal identity, money movement, account ownership, or human-only actions.

Accept these shorthand values:

- `JEV`: let JEV decide.
- `UNKNOWN`: research or infer if possible.
- `N/A`: not applicable.
- `KEEP`: preserve the existing implementation.
- `NONE`: not currently available.

After intake submission, do not interrupt for ordinary decisions. If a missing value can be inferred, researched, defaulted safely, or implemented behind configuration, do that and record the choice.

## JEV decision authority

JEV is the autonomous executive decision role for this skill.

How JEV runs:

- If the `typesafe-ai` skill is available, route substantive judgment calls (offer structure, positioning, risk, scope) through TypeSafe's Jev. Record its `confidence` and `probabilities`, not just the chosen option. Never use Jev for anything verifiable by reading code, running a command, or checking live state.
- If the probabilities are near-even, or confidence is low, do not pick on intuition: apply the decision priority below and take the most reversible option. Escalate to the user only when the decision is irreversible, spends money, or makes legal claims.
- If `typesafe-ai` is unavailable, the agent acts as JEV and applies the decision priority below directly.

JEV may decide without asking again:

- target segment and primary use case;
- positioning and value proposition;
- page structure and CTA hierarchy;
- offer and quantity-tier structure within price/margin constraints;
- copy direction and objection handling;
- responsive UX and accessibility fixes;
- SEO structure and metadata;
- architecture, libraries, schemas, API boundaries, and refactors when within granted technical authority;
- analytics abstraction and event placement;
- deployment implementation within granted production authority;
- which low-risk implementation path to use when several valid options exist.

Use this decision priority:

1. explicit user constraints and legal/safety requirements;
2. verified product facts and current platform requirements;
3. existing repository and infrastructure conventions;
4. payment correctness and data integrity;
5. conversion impact and customer trust;
6. privacy, consent, security, and maintainability;
7. performance and accessibility;
8. simplicity, reversibility, and implementation cost;
9. visual preference.

For meaningful decisions, record:

- decision;
- evidence or constraint;
- alternatives considered when relevant;
- reason;
- downstream effect.

Write important decisions to `JEV_DECISIONS.md` when working in a repository.

## Related skills

Load these on demand when the step matches. Use `openskills list` to confirm they are installed; never invent names.

| Step | Skill |
| --- | --- |
| Privacy/Cookie/Terms/Refund pages, GDPR consent | `web-compliance-builder` |
| Pre-launch SEO, AEO/AIO, GEO, EU compliance audit | `landing-launch-check` |
| Visual system, layout, accessibility | `ui-ux-pro-max` |
| Product/hero image prompts | `image-prompt-engineer` |
| Persuasion and conversion psychology (ethical only) | `psychology-master` |
| Wise card payments (when Wise is the chosen gateway) | `wise-payment-gateway` |
| Deploy to Dokploy | `dokploy-deploy` |
| Copy polish before publishing | `de-ai-english` / `chinese-humanizer` |
| Performance and a11y QA | `web-performance-audit`, `web-accessibility-audit` |

Reader-facing copy must be de-AI'd before it ships.

## Default stack (new projects only)

Applies only when no repository or stack exists and intake says `JEV` or `UNKNOWN`. Existing conventions always win.

- Package manager: `pnpm`.
- If a backend is needed and none exists: Appwrite, managed through the Appwrite CLI.
- If the product page collects personal data or runs ad pixels: include a GDPR-compliant consent flow (see `web-compliance-builder`). The consent banner must not cover product imagery or the primary CTA — dock it to a corner (e.g. bottom-left) rather than centering it over content, and verify this at desktop and mobile widths with the banner actually showing.

## Human dependency policy

Treat the following as likely human-only dependencies unless a connected tool can perform them safely:

- account creation requiring personal identity;
- KYC or banking verification;
- 2FA, passkeys, CAPTCHA, or device approval;
- signing legal terms or regulated attestations;
- payment-provider account ownership verification;
- ad-account business verification;
- registrar or DNS ownership approval when no authorized connector exists;
- entering secrets that the agent cannot access through an approved secret store;
- production spending authorization not granted during intake;
- purchases or paid ad spend above the authorized budget.

Collect these dependencies during intake. After intake, do not repeatedly ask for them.

When a dependency is unavailable:

1. complete all surrounding implementation;
2. create a clearly named config/env placeholder when appropriate;
3. provide test-mode coverage when possible;
4. document the exact blocked capability;
5. continue with all other work;
6. list the exact manual action only in the final handoff unless immediate intervention is strictly required to avoid destructive or unsafe behavior.

Never ask the user to paste raw secrets, private keys, CAPI tokens, passwords, or recovery codes into chat. Ask for connector availability, secret-manager path, or environment variable name instead.

## Research and truthfulness

Separate verified facts from assumptions.

Verify before publishing:

- product contents, size, material, age guidance, safety warnings, certifications, scent, warranty, shipping claims, stock, and delivery times;
- current payment, analytics, pixel, search, consent, and advertising integration requirements;
- current legal or policy claims when they affect implementation.

Do not invent:

- reviews or star ratings;
- customer counts;
- awards;
- certifications;
- MSRP or fake compare-at pricing;
- stock scarcity;
- countdown urgency;
- guarantees;
- health or safety claims;
- shipping method, delivery times, or dispatch windows that are not confirmed (dropshipping and pre-order products often have no fixed ETA — say nothing rather than guess).

Never infer product facts from the product photos themselves. A photo does not prove a set is fixed vs randomized, that items never repeat, contents, counts beyond what packaging text states, material, or scent. If a claim cannot be sourced from the supplier, packaging text, or an authoritative product page, omit it — describe only what the image visibly shows, and ask the user for the supplier link or confirmation when a claim would materially help conversion.

Use seasonality, actual inventory, real deadlines, and documented offers as legitimate urgency only when true.

## Execution workflow

Use `references/execution-workflow.md` after intake.

At minimum, complete these workstreams:

- product and competitor research;
- customer and use-case selection;
- offer economics;
- funnel information architecture;
- production copy;
- visual system and asset audit;
- cart/checkout/payment;
- verified order lifecycle;
- transactional messaging when supported;
- OpenAI Ads, Meta, Google, and other requested measurement;
- SEO and structured metadata;
- consent/privacy integration according to the selected stack;
- domain and deployment;
- responsive, accessibility, performance, and error-state QA;
- full customer-journey verification.

## Tracking and advertising measurement

Use `references/tracking-and-integrations.md` whenever tracking is in scope.

Important defaults:

- OpenAI Ads: prefer Measurement Pixel + Conversions API when supported and authorized; use documented standard events and shared dedupe identifiers for paired browser/server events.
- Meta: prefer Pixel + CAPI for purchase-critical funnels when supported and authorized; deduplicate paired events.
- GA4: implement relevant ecommerce events and use a stable transaction identifier for purchase.
- Google Search Console: treat indexing/domain verification separately from GA4/Google Ads conversion tracking.
- Preserve attribution parameters and consent behavior.
- Do not let tracking failure block checkout or payment success.

If the installed `openai-ads-conversions-setup` skill is available and OpenAI Ads tracking is in scope, use it for implementation or validation rather than inventing undocumented OpenAI Ads syntax.

## Payment correctness

Use the existing payment provider when it is working unless there is a strong reason to replace it.

Never trust client-submitted price, discount, tax, shipping total, or paid state.

For purchase funnels:

- calculate or validate price server-side;
- create payment sessions server-side where the provider requires it;
- verify successful payment server-side;
- use webhook/provider verification when applicable;
- make order creation idempotent;
- prevent duplicate paid orders on retries;
- preserve recoverable cart/offer state after failed payment;
- never store card data;
- keep secrets server-side;
- do not treat a success redirect alone as proof of payment.

## Repository behavior

When a repository exists:

- inspect before choosing architecture;
- preserve framework, package manager, style, deployment, analytics, and secret conventions when reasonable;
- extend existing abstractions instead of creating parallel ones;
- search existing documentation such as `CONTEXT.md`, `CONTEXT-MAP.md`, and `docs/adr/`;
- create or update `CONTEXT.md` only for real domain concepts;
- create an ADR only for consequential, hard-to-reverse trade-offs;
- when the project holds sibling funnels cloned from a shared template, a layout/UX fix to a shared component (consent banner, header, offer selector) usually applies to all of them — flag the others and offer to apply the same fix, but do not silently modify a live sibling funnel the user did not name;
- cut each fix branch from the up-to-date default branch (`origin/main`), not from a stale feature branch left over from the previous step; stage only the files you changed and confirm the diff before committing;
- do not commit secrets.

## Progress updates

Keep the user informed in their language during long execution, but do not convert updates into approval gates.

Good update:

"Product research and offer design are complete. JEV selected parents preparing Halloween party bags as the primary buyer and chose a 1/2/3-set quantity structure because it maps directly to the main use cases. I am continuing with checkout and tracking integration."

Bad update:

"I found three pricing options. Which one do you want?"

## Final handoff

Use `references/delivery-report.md`.

The final response must clearly separate:

- what was completed;
- what JEV decided;
- what was verified;
- what is live;
- what assumptions remain;
- what requires human intervention.

For every human action, state:

- exact system/location;
- exact action;
- exact field or secret name when applicable;
- required value type, never the secret itself;
- why the agent could not perform it;
- what capability becomes active afterward.

Do not label ordinary unfinished engineering work as human intervention.
