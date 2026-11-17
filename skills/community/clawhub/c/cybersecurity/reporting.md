# Reporting — Findings, Executive Summaries, Board Slides

A security report exists to cause a decision. If the reader finishes it without knowing what they must decide, it failed regardless of how correct it was.

**Before writing**, read `## Findings` in `~/Clawic/data/cybersecurity/memory.md` — or `findings.md` if `## Boxes` points there — so ids are not reused and a previously accepted risk is not re-reported as new, plus `## How They Work` for how this reader consumes findings. `report_audience` and `conventions.finding_id` in `config.yaml` set the register and the numbering.

**Contents:** [Write For The Decision](#write-for-the-decision) · [The Finding](#the-finding) · [Severity That Survives Challenge](#severity-that-survives-challenge) · [Confidence Language](#confidence-language) · [The Executive Summary](#the-executive-summary) · [The Board Slide](#the-board-slide) · [Metrics For An Audience That Cannot Verify Them](#metrics-for-an-audience-that-cannot-verify-them) · [Delivering Bad News](#delivering-bad-news) · [The Incident Update](#the-incident-update) · [Language Traps](#language-traps)

## Write For The Decision

Before the first sentence, answer three questions:

1. **Who decides, and what are they deciding?** Fund it, accept it, prioritize it, disclose it, or act now. A report with no decision is a newsletter.
2. **What do they need in order to decide?** Usually impact, likelihood, cost and the alternative — not the technique.
3. **What happens if they do nothing?** Say it plainly, with the timeframe. This is the sentence most reports omit and the one that moves budgets.

Structure follows from that: **the decision first, the evidence second, the detail in an appendix.** Executives read the first paragraph and the last; engineers read the reproduction steps; nobody reads the middle. Put the ask where it will be read.

## The Finding

Nine fields. Anything missing makes it unactionable, and the two that get dropped are the two that matter most.

| Field | Content |
|---|---|
| Id | Stable, never reused, from the org's scheme |
| Title | The problem in one line, in the reader's language — not the vulnerability class |
| Severity | With the reasoning, not just the label |
| **Attack path removed** | What an attacker can no longer do once it is fixed. A finding that cannot fill this field is a preference, not a finding |
| Evidence | What was observed, with the confidence word and its source |
| Impact | The business consequence, in plain language, at the scale it would actually occur |
| Reproduction | Enough for the owner to see it themselves — the fastest route to agreement |
| Remediation | The specific fix, and the cheapest option that closes the path |
| **Owner and due date** | A named person and a date. No owner and no date is a complaint (SKILL.md Rule 6) |

Write the title for the person who has to act. "Any logged-in customer can read another customer's invoices by changing the id in the URL" is understood and prioritized immediately; "IDOR in the invoice endpoint" is triaged next sprint by someone who has to decode it first.

## Severity That Survives Challenge

Severity is an argument with three inputs, and every serious challenge attacks one of them:

- **Impact**: what the attacker gains. Irreversible (funds moved, data published) outranks recoverable (a service restarts).
- **Exploitability**: what they need. Unauthenticated and remote outranks authenticated-plus-a-race-window by a wide margin.
- **Exposure**: who can reach it. Internet outranks internal outranks administrative segment.

Rules that keep the scale credible:

- **State the reasoning, always.** "High: unauthenticated, internet-facing, leads to customer data" is defensible. "High" alone is an opinion, and the first pushback wins.
- **Let a medium be a medium.** Severity inflated to force attention works twice; after that every finding is discounted, including the real one. This is the single fastest way to lose a security team's credibility with engineering.
- **Say when a compensating control genuinely reduces practical risk.** Acknowledging it is what makes your severity trustworthy the next time you refuse to lower one.
- Chains get rated as chains: three mediums that combine into domain admin is a critical, and the finding is the chain, with the individual links as its steps.
- Disagreement about severity is a decision the owner can escalate. Document their rating alongside yours rather than quietly conceding — the record matters if it is exploited.

## Confidence Language

Use SKILL.md Rule 3's four words with their definitions, and keep observed, inferred and recommended in separate sentences:

- **Confirmed** — two independent sources agree.
- **Likely** — one reliable source, consistent with the rest of the timeline.
- **Possible** — a single weak indicator.
- **Unknown** — say so, and name the evidence that would settle it.

Two failures to avoid, in opposite directions. **False certainty**: "the attacker accessed 40,000 records" when the logging cannot show reads — the honest version is "40,000 records were reachable by the compromised account; per-item access logging does not exist, so what was read is unknown." **Uniform hedging**: qualifying everything equally, so the reader cannot tell the confirmed from the speculative and discounts all of it. Precision about your own uncertainty is what makes the confirmed statements land.

"No evidence of X" and "X did not happen" are different claims. Only make the second when the logging would have shown it, and say why it would have.

## The Executive Summary

Five sentences, in this order, and it must stand alone if nothing else is read:

1. What happened, or what the assessment found — one sentence, no jargon.
2. What it means for the business — money, customers, regulatory exposure, operations.
3. What is already done or contained.
4. What decision is needed, from whom, by when.
5. What happens if that decision is not made.

Never open with methodology. Never open with a compliment. Never bury the decision in paragraph four. If a number is in the summary, it must be one you can defend for ten minutes — the summary number is the one that gets quoted back.

## The Board Slide

Boards decide about money, risk and accountability. They do not decide about controls.

- Three to five items, each in the form: **risk in business terms · what we are doing · what we need**.
- Trend beats snapshot: "critical findings past SLA fell from 14 to 3 in six months" says more than any current count.
- Frame in the language of business risk — revenue at risk, customer commitments, regulatory exposure, operational downtime — never in techniques or tool names.
- Ask for one thing per session. A slide with six asks receives zero.
- Answer the four questions boards actually ask, before they ask them: are we compliant with what we have committed to, could what happened to that company happen to us, what would it cost, and are we spending the right amount relative to peers.
- Never present a maturity score without saying what changed and what it cost. A number that only goes up is not believed, correctly.

## Metrics For An Audience That Cannot Verify Them

| Report | Not |
|---|---|
| Mean time to remediate KEV and internet-facing findings | Total vulnerability count (moves with scanner coverage, so improving coverage looks like failure) |
| Percentage of assets covered by EDR, MDM and logging | Number of alerts generated |
| Findings past SLA, by owner | Number of rules enabled |
| Time from awareness to containment in the last incident | Blocked attacks per month (unfalsifiable and meaningless) |
| Phishing report rate and time-to-first-report | Click rate alone, which drives programmes toward punishing users |
| Restore drill result: time and completeness, dated | "Backups are configured" |
| Exposure reduction: internet-facing services removed | Maturity score with no delta |

Every metric shown must have a stated collection method and a date. A metric an executive cannot verify is a trust transaction — spend it on the few that matter, and make each one falsifiable.

## Delivering Bad News

- **Early and plainly.** The cost of a late disclosure is always higher than the cost of the news, and the delay itself becomes the story.
- Lead with the fact, then the context. Burying it in paragraph three reads as concealment when it is discovered.
- Bring the options with it: what can be done now, what it costs, what happens if nothing is done. Bad news with options is a decision; bad news alone is a problem you handed over.
- Never blame a person in a written report. Name the control that failed and the process that allowed it. Named individuals in writing destroy the reporting culture that finds the next one.
- Own your own errors first and in the same document. Credibility is what makes every future finding believed.

## The Incident Update

A fixed shape, sent on a stated cadence, keeps everyone out of the incident channel:

1. **Status**: investigating / contained / recovering / closed.
2. **What we know**, with confidence words.
3. **What we are doing right now**, and who is doing it.
4. **What we need from you**, or "nothing".
5. **Next update at** — a specific time, kept even when there is no news.

Do not speculate on attribution or final scope in an update. Do not promise a resolution time you cannot control. Do not let the technical detail expand as the audience widens — the executive update and the engineering update are two documents, and merging them serves neither.

## Language Traps

| Trap | Why it fails | Instead |
|---|---|---|
| "Critical vulnerability" with no exposure or exploitability | The first informed challenge collapses the whole report | State impact, exploitability and exposure separately |
| "Hackers could access everything" | Unfalsifiable, and reads as scaremongering | Name the data, the account and the path |
| "Best practice requires…" | An appeal to authority, and engineers push back correctly | Name the attack path it removes |
| "We were targeted by a sophisticated actor" | Usually untrue, and it reads as an excuse | Describe what happened; sophistication is a claim requiring evidence |
| "The system is secure" | Cannot be true of any system, and it will be quoted after the next incident | "These paths are closed; these remain open; this is what we cannot see" |
| "100% compliant" | Compliance is scoped and time-bound | "Compliant with X, in scope Y, as of Z, with N exceptions" |
| Passive voice for failures ("credentials were exposed") | Hides the owner and the decision | Say what happened and who owns the fix |
| Technique names as the finding title | The reader must decode before prioritizing | Plain-language consequence in the title |

Write it (`memory-template.md`): every finding as a row in `## Findings` with its id, severity, attack path removed, owner and due date — ids never reused, and a resolved finding leaves `### Open` with its resolution recorded where it belongs; anything the owner declines in `## Risk Accepted` with the acceptance date, the expiry and the compensating control, plus a `## Due` row for the expiry, because a verbal acceptance reappears in the next audit with nobody's name on it; the reader's preferences — audience, severity wording, format, delivery channel — in `config.yaml` under `conventions` and `report_audience`, never in memory, since a stated preference is a declaration; the report, the board summary and any reusable template as their own files in `~/Clawic/data/cybersecurity/artifacts/`, each opening with when to re-read it and getting its `## Boxes` line in the same turn. Reports name hosts, accounts and identifiers freely; they never carry credentials, and personal data appears as counts and categories.
