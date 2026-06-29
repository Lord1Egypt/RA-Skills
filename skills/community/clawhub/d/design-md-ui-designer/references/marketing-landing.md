# Marketing Landing Reference

Use this reference when a page must convert, sell, capture demand, or make a
product easier to share. Keep the work tied to product truth and current user
behavior; do not make a polished page for a weak offer without saying so.

## Launch Brief

Fill this before layout work:

```yaml
traffic_source: ""          # exact first qualified traffic source
one_reader: ""              # specific visitor and painful moment
awareness_level: ""         # unaware/problem/solution/product/ready
offer: ""                   # free MVP, paid add-on, or skill/data bundle
first_action: ""            # install, audit, read, download, buy, book
share_moment: ""            # why they would send it to someone
trust_reason: []            # real proof: screenshots, dataset, tests, source
boundaries: []              # what is not promised or not affiliated
update_policy: ""           # how future updates are delivered
kill_gate: ""               # traction threshold and date
```

If any of `traffic_source`, `share_moment`, or `trust_reason` is empty, the
landing is not ready for a premium treatment. Fix the offer or run research
first.

## Conversion Anatomy

Prefer this order for focused product pages:

1. Hero: literal product/offer name, single reader, single painful moment, real
   product state or artifact, one CTA.
2. Proof strip: dataset date, version, source archive, permission posture,
   review/test status, privacy facts, or update cadence.
3. Problem lens: what the visitor is currently doing wrong and why it costs
   attention, trust, or time.
4. Product workflow: input, analysis, output, next action. Show the actual
   artifact whenever possible.
5. Included: concrete deliverables, update policy, compatibility, support.
6. Use cases/personas: who should use it now, and when not to use it.
7. Trust receipts: source links, real screenshots, CWS reviewer guide, test
   output, changelog, public dataset scope, or named public references.
8. Content hub: articles/playbooks for search and sharing.
9. Pricing or monetization boundary: free path, paid path, refund/delivery,
   no-hidden-claim boundary.
10. FAQ and final CTA: repeat the same action, not a new funnel.

## Copy Rules

- One reader, one offer, one action.
- Use the visitor's task language, not generic AI words such as "leverage",
  "seamless", "transform", or "unlock" unless the copy proves the claim.
- Replace broad promises with bounded evidence: date, dataset size, version,
  permission scope, fixture, or test gate.
- Never invent testimonials, buyer names, ratings, logos, revenue numbers,
  review speed, or "trusted by" claims.
- Use named third-party brands only as factual topic references. Do not imply
  partnership, endorsement, official ranking influence, or platform access.
- CTA copy should describe what happens next: "Run the public-page audit",
  "Read the dataset playbook", "Install the local extension", or "Request a
  teardown".

## Trust Receipts

Use receipts instead of fake social proof:

- current product screenshot with sanitized fixture data;
- source archive and checksum;
- CWS reviewer instructions and permission explanation;
- dataset snapshot date, row count, fields, and collection boundary;
- release notes and update cadence;
- public article explaining a real workflow;
- independent test/e2e output, if safe to publish;
- privacy/support pages that exactly match implementation.

## SEO Article Cluster

Create `3-9` articles when the product needs education, dataset explanation, or
an organic traffic path. Each article needs:

- a search-intent title;
- a 1200x630 or 1280x720 thumbnail readable at small card size;
- one concrete operator task;
- a product CTA that matches the article intent;
- internal links to the landing, privacy/support/reviewer pages when relevant;
- an affiliation or source boundary when third-party platforms are discussed.

YouTube-style thumbnails are allowed for article cards when they improve
scannability. Use bold readable overlays, one dominant idea, high contrast, and
real topic cues. Do not use official logos or endorsement-like placement unless
rights are explicit. If the user explicitly allows a third-party name for blog
thumbnails, use it as a textual topic label only.

## Monetization Boundary

For early products, keep the extension/app free until there is evidence of
repeat use. Monetize the higher-touch layer first when appropriate:

- manual teardown;
- operator implementation pack;
- updated dataset report;
- skill package;
- private workshop;
- maintained workflow template.

State clearly what buyers receive, how updates work, refund/delivery terms, and
what is not included. Do not hide paid logic inside a marketplace extension
unless privacy, policy, payment, support, and delivery are already production
ready.

## Scoring

Score before shipping:

| Category | Pass Bar |
| --- | --- |
| Traffic source | exact first qualified source named |
| Share moment | user would naturally send/save/repost a specific artifact |
| Offer clarity | free and paid paths are distinct |
| Proof integrity | every claim maps to a real receipt |
| Visual trust | page looks specific, not template-generic |
| Article cluster | titles/thumbnails/tasks support real search intent |
| SEO baseline | canonical, meta, social preview, sitemap, structured data |
| Rights safety | brands/logos/claims cannot imply affiliation |
| Responsive polish | no clipping/overflow at mobile/tablet/desktop |
| Kill gate | traction threshold and review date are documented |

Block if any category is below `9/10` for paid launches or below `8/10` for
free MVP public pages.
