# Anti-AI Design Tell Review

Use this as a companion to `references/product-design-review.md` and `references/review-rubric.md` when the user asks for design critique, redesign readiness, visual polish, or says the interface looks generic, templated, or AI-generated.

This file is not a style preference list. Treat each item as a diagnostic signal. A pattern is only a finding when it harms product fit, task clarity, trust, originality, accessibility, or conversion.

## High-Confidence Tells

Flag these with evidence when visible:

- Default AI purple/blue gradients, neon glows, or decorative mesh backgrounds with no brand rationale.
- Three equal feature cards or repeated equal cards where the content has different importance.
- Centered hero with vague headline, vague subtext, and generic CTA.
- Fake dashboard, fake terminal, or fake product preview built from decorative rectangles instead of a real screenshot, generated asset, or actual component.
- Fake-precise metrics such as `99.9%`, `10x`, `48k`, or `92%` without source, label, or sample context.
- Decorative status dots, version labels, build metadata, or weather/time/location strips that do not convey real state.
- Overused eyebrow labels on every section, especially numbered labels such as `01`, `002`, `INDEX`, or `PHASE`.
- Mixed visual systems: inconsistent radius, icon families, shadows, typography, button styles, or neutral palettes.
- Card nesting and section-as-card structure that hides hierarchy instead of clarifying it.
- Generic names, generic avatars, placeholder companies, or `Acme`-style brands presented as real content.
- Copy that reads like filler: "seamless", "elevate", "unlock", "next-gen", "effortless", or poetic phrases that do not explain the product.

## Product UI Tells

For dashboards, admin panels, tools, editors, and workbenches, also check:

- Marketing-page hero structure used for an operational tool.
- Excessive empty space that slows scanning in high-frequency work.
- Metrics shown as decorative cards without drilldown, source, freshness, or action path.
- Tables hidden behind card grids when users need comparison, sorting, filtering, or bulk action.
- Every row action exposed equally instead of prioritizing common actions and protecting dangerous actions.
- Bulk actions without impact summary, permission gating, confirmation, undo, or audit trail.
- Empty/loading/error states omitted because only the successful demo state was designed.
- High-risk AI outputs shown with opaque scores instead of explainable reasons and evidence.
- Mobile layout merely squeezed from desktop, with fixed toolbars, clipped labels, or unreachable primary actions.

## Marketing And Conversion Tells

For landing pages, homepages, pricing pages, and campaign pages, also check:

- Hero value proposition could apply to any SaaS after changing the logo.
- CTA labels change wording across nav, hero, pricing, and footer for the same intent.
- Trust logos are plain text wordmarks or invented customer names presented as credibility.
- Screenshots are fake product UI and do not show a believable workflow.
- Each section repeats the same layout family.
- Long feature lists are used instead of grouping, proof, demos, or task-based narratives.
- Testimonials are too long, unattributed, or generic.

## Recommendation Rule

When flagging an AI tell, do not stop at criticism. Convert it into an implementable change:

```text
Finding: <specific tell>
Evidence: <where it appears>
Impact: <why it weakens product fit, trust, clarity, or task completion>
Recommendation: <what to replace it with>
Acceptance criteria: <how the user or QA can tell it is fixed>
```

## Do Not Overapply

- Do not penalize a simple design just because it is simple.
- Do not penalize density in an operational cockpit when density supports expert work.
- Do not force unusual visual patterns when a regulated, enterprise, or public-sector product needs predictability.
- Do not require image generation for internal tools unless visuals are part of the reviewed experience.
- Do not copy taste-skill landing-page bans blindly into dashboards, data tables, editors, or workflow-heavy product UI.
