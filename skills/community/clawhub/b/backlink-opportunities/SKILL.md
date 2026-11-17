---
name: backlink-opportunities
description: Use when the user asks about backlinks, referring domains, link building, broken links pointing at them, or link gaps versus competitors. Analyzes a backlink profile and produces a human-reviewed link-opportunity plan — reclamation, competitor intersection, linkable assets, unlinked mentions. Import/direct-provider modes; never automates outreach or disavow.
---
# Backlink Opportunities

Earned links come from having something worth citing and telling the right people it exists. This skill finds the opportunities and drafts the plan; a human runs the outreach, and nothing here touches disavow.

Read `references/provider-selection.md` before choosing a source; DataForSEO calls go through the `references/dataforseo.md` cost gate (its backlinks endpoints are billable — same preflight/approval rules). All normalized factual inputs must satisfy the Groundcrew evidence contract (`evidence_type: backlink`). Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Evidence in (import / direct provider)

Category: `~~link database` (`references/connectors.md`) — GSC Links export at Tier 1, Open PageRank at Tier 2, Ahrefs MCP or TrustGrowth backlink snapshots at Tier 3. Backlink data is always a third-party index observation — no index sees every link. Every profile fact carries its provider name, retrieval date, and this limitation. Accept: provider exports (Ahrefs/Semrush/Moz/GSC links report), or cost-gated DataForSEO backlinks calls. Open mode without any link data does asset review only (step 3) and says the profile was not measured.

## The opportunity lanes

1. **Reclamation first — links you already earned.** Broken inbound links (target 404s → fix or redirect via `fix-my-site`), and redirect chains eating link equity. Cheapest wins, no outreach required.
2. **Competitor intersection.** Domains linking to N named competitors but not to this site — with the *reason* each linked (resource list, data citation, review). Requires competitor link data from the same provider/window; without it, the lane reports `not measured`.
3. **Linkable assets.** What on this site is citable (original data, tools, definitive references) — and what gap a new asset would fill. Feeds `content-strategy`.
4. **Unlinked mentions.** Imported mention data where the brand appears without a link — the warmest outreach there is.

## The plan out

Prospect table: domain · lane · evidence reference · why they would link · suggested asset · a draft angle (not a send-ready email). Ends with: **outreach is executed by a human**. This skill never sends, schedules, or automates contact, and never proposes paid links, link exchanges, or private blog networks — Google's link-spam policy makes those liabilities, and ETHICS makes them refusals.

## Toxicity and disavow — hard boundary

- No "toxic link" scores. Provider toxicity metrics, if imported, are reported as that provider's opinion with its name attached.
- **Never recommend, generate, or automate disavow.** Google states most sites should not use it and misuse harms. The most this skill says: "these links look manipulative; a human should review them against Google's link-spam documentation, and disavow is relevant mainly under a manual action."

## Connected mode

TrustGrowth's authority pillar summarizes link standing inside its own score (see `authority-review`). A detailed backlink read surface is documented in the live OpenAPI when available — check at execution time; until then connected mode adds nothing link-specific here.

## When not to use

- Overall authority standing (entity, references, credibility) → `authority-review`.
- Fixing broken targets/redirects in the repo → `fix-my-site`.
- Deciding what citable asset to build → `content-strategy`.
- Directory/listing hygiene as entity presence → `authority-review`, not mass submissions — quality directories only, by hand.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
