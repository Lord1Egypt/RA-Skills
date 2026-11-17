# Source Strategy

Use this file to decide what evidence is good enough for the current research object. Do not collect sources for their own sake; collect sources that can change the answer.

## Source Mix By Object Type

| Object type | Start with | Add for reality check | Common trap |
| --- | --- | --- | --- |
| Company | official site, filings, funding announcements, leadership pages | reputable reporting, customer reviews, employee signals, product changelog | treating PR, founder interviews, and copied funding databases as independent proof |
| Product | docs, release notes, pricing page, changelog, repository | user reviews, GitHub issues, app store reviews, benchmark comparisons, support forums | comparing feature lists without the user job |
| Open-source project | repository, releases, issues, maintainer docs, package stats | downstream adopters, forks, security advisories, community discussions | mistaking stars or hype for active production use |
| Person | primary writing, talks, interviews, official role pages | profiles, criticism, public records, timeline corroboration | flattening the person into one viral quote |
| Concept / technology | papers, standards, docs, early usage, naming history | adjacent concepts, debates, adoption examples, failed alternatives | writing a clean origin story where the record is messy |
| Market / category | official statistics, market reports with methodology, filings | buyer interviews, vendor pages, pricing, community complaints | accepting market-size numbers without checking definitions |
| Cultural phenomenon | primary artifacts, publication dates, creator statements | platform metrics, criticism, community reception, regional variants | treating one platform's discourse as the whole phenomenon |

## Minimum Evidence Sets

- `brief`: 3-5 strong sources, at least one primary source when available, plus clearly marked gaps.
- `deep report`: 8-15 sources across primary, current snapshot, user signal, and dissenting evidence.
- `decision brief`: enough evidence to support the verdict, the main risk, and one reversal condition. If the evidence is weak, recommend an experiment instead of a confident verdict.
- `research update`: old conclusion, changed facts, unchanged facts, and sources dated after the older report's evidence window.
- `asset pack`: evidence ledger plus reusable notes, source map, open questions, monitoring list, and search queries.

## Claim-Level Traceability

For load-bearing claims, follow [claim-citation-protocol.md](claim-citation-protocol.md).

For policy, standard, exam, certification, and official-program claims, also follow [formal-adoption-status-protocol.md](formal-adoption-status-protocol.md).

At minimum, preserve evidence IDs for:

- the one-line answer.
- each current official status or time-sensitive fact.
- each major recommendation, risk, reversal condition, or stakeholder impact.
- any claim where source type changes the meaning, such as official notice vs training-provider summary.

Do not rely on a final source dump. If a claim matters, the reader should be able to trace it back to the exact evidence entry that supports it.

## Recency Rules

Verify recently when claims involve:

- prices, plans, product availability, feature parity, model capabilities, leadership, funding, regulation, market share, benchmarks, security incidents, or platform policies.
- any topic where the user asks for latest, current, today, this year, recently, or update.

Always state the evidence window. For example: `Evidence checked through 2026-05-14` or `Source window: 2023-2026`.

## Conflict Handling

When sources disagree:

1. Identify whether they are actually independent.
2. Prefer primary records for hard facts, but keep user evidence for experience quality.
3. Record the conflict in the ledger with `conflicts_with`.
4. Explain how the disagreement changes confidence.
5. Name what would resolve it.

Do not average contradictory claims into a false middle. A weak but honest uncertainty is better than a smooth invented synthesis.

## Negative Evidence

Look for at least one of:

- a credible criticism or failed adoption case.
- user complaints that recur across channels.
- a competitor or substitute that wins on a different user job.
- a missing source that should exist if the optimistic story were true.

If negative evidence is unavailable, mark it as a gap instead of declaring none exists.
