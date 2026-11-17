# Design Review — Attack Paths Before Controls

For "is this secure?", a new architecture, or a change to an existing one. The deliverable is a small set of ranked attack paths with the controls that break them — not a control checklist, and not STRIDE notation for its own sake (the notation depth lives in the sibling `threat-modeling` skill).

**Before reviewing a design**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` for the trust boundaries and crown jewels already mapped, and open any `artifacts/threat-model-*.md` the `## Boxes` index names for this system — re-deriving a model somebody already built produces a different answer and destroys trust in both.

**Contents:** [The Four Questions](#the-four-questions) · [Draw The Boundaries, Not The Boxes](#draw-the-boundaries-not-the-boxes) · [Enumerating Paths Without A Framework](#enumerating-paths-without-a-framework) · [Ranking Paths](#ranking-paths) · [The Path Table](#the-path-table) · [Controls: Break The Path, Name The Link](#controls-break-the-path-name-the-link) · [Assumptions Are The Real Findings](#assumptions-are-the-real-findings) · [Reviewing A Change Rather Than A System](#reviewing-a-change-rather-than-a-system) · [Timeboxes And Depth](#timeboxes-and-depth) · [Traps Of Design Review](#traps-of-design-review)

## The Four Questions

The whole method, in the order that produces answers:

1. **What is worth stealing, breaking or abusing here?** Data, money, availability, trust, compute. Name the concrete asset — "the payout bank details", not "customer data".
2. **Where does something untrusted meet something trusted?** Every entry point: public API, webhook, upload, admin panel, support tool, CI/CD, the third-party integration, the queue another team writes to.
3. **What does the attacker have to chain to get from an entry point to an asset?** That chain is the path, and it is the unit of the whole review.
4. **Which single link is cheapest to break, and how would we know if somebody tried?** Control plus detection, per path.

If a review produces a list of controls without a list of paths, it produced a checklist. The test: for every recommended control, you can state the path it removes in one sentence (SKILL.md Rule 7).

## Draw The Boundaries, Not The Boxes

A data-flow diagram is useful only for its boundaries — every other line on it is documentation.

- Mark each boundary where **the authority changes**: internet → edge, user → admin, application → database, tenant → tenant, CI → production, employee → contractor, first party → vendor.
- On each boundary, write three things: **who authenticates whom** (often only one direction, and the missing direction is a finding), **what is validated crossing it**, and **what is logged crossing it**.
- The boundary nobody draws is the one that gets crossed: the queue, the shared cache, the internal service that trusts any caller inside the VPC, the support tool that can impersonate users, the build system that can deploy.
- **Multi-tenancy adds one boundary per tenant pair**, and the enforcement point is what matters: a `tenant_id` in a `WHERE` clause enforced by developer discipline is not a boundary, it is a convention. Where is it impossible to write the query wrong?
- Data classification is a boundary property: what crosses in, what crosses out, whether it may be logged, and where it may be stored.

## Enumerating Paths Without A Framework

Walk each entry point and ask the same five questions. This produces the paths that actually occur, which is a shorter and more useful list than a full mnemonic sweep.

| Question | Path class it finds |
|---|---|
| Can I reach it without authenticating? | Exposed admin interface, unauthenticated internal service, forgotten staging environment |
| Can I be a different user or a different tenant? | Broken object-level authorization — the most common serious web finding by a wide margin |
| Can I make the system act on my behalf toward something it trusts? | SSRF into the metadata service, forged webhook, confused deputy, request smuggling |
| Can I influence what runs? | Injection, deserialization, template injection, a dependency or build step I control |
| Can I stay, or come back? | Long-lived token, a key I can register, an account I can create, a persistence surface with no expiry |

Then two more that catch what the technical sweep misses:

- **The human path**: who can be convinced to do this by phone, and is there an out-of-band verification step? The support tool that can reset MFA is an attack path with a help-desk shape.
- **The abuse path**: the feature working exactly as designed, at scale, by someone hostile — free-tier compute for mining, password reset as an enumeration oracle, the referral bonus, the API that sends email to arbitrary addresses. Abuse is not a bug, so no scanner will ever report it, and it is the class that costs product companies real money.

## Ranking Paths

Rank on three factors, plus one that decides the tie:

- **Attacker cost**: what do they need — an account, a phishing success, an insider, a specific race window? Anything requiring no authentication ranks above everything requiring some.
- **Impact at the end of the path**: irreversible (funds moved, data published) beats recoverable (a service restarts).
- **Detection**: would we see it? A path that is invisible ranks above an equivalent path that is loud, because the invisible one runs to completion.
- **Tiebreak on reversibility.** Between two equal-impact paths, fix the one whose damage cannot be undone.

Deliberately not a numeric score. A three-factor qualitative ranking with reasons written down survives a challenge; a computed 7.4 invites an argument about the arithmetic instead of the path.

## The Path Table

The deliverable, and it fits on one page:

| # | Path | Attacker needs | Impact | Would we see it | Cheapest break |
|---|---|---|---|---|---|
| 1 | Phished admin session → support tool → impersonate any user → change payout details | One admin phish | Funds diverted, irreversible | Only in support-tool logs nobody reads | Phishing-resistant MFA on admin, plus an alert on payout changes made through impersonation |
| 2 | Forged webhook → false payment credit | Knowledge of the endpoint | Financial, reversible with reconciliation | No | Verify the provider's signature; reject unsigned |
| 3 | SSRF in the image fetcher → instance metadata → role credentials | Any authenticated user | Cloud account access | Only with data-event logging | Enforce IMDSv2/hop limit, and an egress allowlist for the fetcher |

Three to seven rows. A twenty-row table is a scanner report wearing a design review's clothes, and nobody acts on it.

## Controls: Break The Path, Name The Link

- **Break the cheapest link, not every link.** A path is a chain: removing any one link removes the path. The instinct to control every step produces a design nobody ships.
- Prefer controls that make the vulnerability class **unrepresentable** over controls that catch instances: a query layer that cannot omit the tenant filter beats a code review that looks for the omission; parameterized queries by construction beat input sanitization; a type that cannot hold an unvalidated URL beats remembering to validate.
- **Where is it impossible to get wrong?** Push enforcement down to the layer where the mistake cannot be made — the gateway, the framework, the database policy — rather than up to the layer where the developer must remember.
- Every recommendation states where it leaks. Phishing-resistant MFA leaks through the help-desk reset path; a WAF leaks to anyone who cares; network segmentation leaks through the management plane.
- Pair each control with the detection for when it fails, because every control fails eventually and the detection is what makes that recoverable (`detection.md`).
- Say what you are **not** recommending and why. "We are not encrypting this at the application layer because the threat we care about is a live application compromise, which application-layer encryption does not address" prevents the same suggestion arriving quarterly.

## Assumptions Are The Real Findings

Every design rests on assumptions, and the exploitable ones are the unwritten ones. Extract them explicitly:

- "The internal network is trusted" — by which host, and what happens when one laptop is compromised?
- "Only our services call this API" — enforced how, and what happens when it is discovered?
- "The library validates that" — verified, or believed?
- "Nobody knows this endpoint exists" — that is not a control, and certificate transparency logs, DNS history and JavaScript bundles all disagree.
- "The vendor handles security" — read what their contract and their SOC 2 report actually cover (`supply-chain.md`).
- "This is temporary" — it is not, and the review must treat it as permanent.

Each assumption becomes either a verified fact (with how it was verified) or an open question that gates the conclusion. SKILL.md Rule 3 applies to design work exactly as it does to incidents: state what is observed, what is inferred, and what would settle it.

## Reviewing A Change Rather Than A System

Most reviews are of a diff, not a greenfield. Ask only what the change can move:

- Does it add an entry point, or make an existing one reachable by a wider audience?
- Does it move data across a boundary that it did not cross before — including into a log, a queue, an analytics pipeline or a third party?
- Does it add a new trust relationship: a dependency, a vendor, a webhook, a service account, a permission?
- Does it weaken an existing enforcement point — a new code path around the authorization middleware, a new admin capability, a bypass "for testing"?
- Does it change who can deploy or who can access production?

Nothing moved on any of those axes, and the review is one line: "no boundary change, no new trust relationship, no new entry point". That answer, given quickly and consistently, is what buys the credibility to slow down the change that does move something.

## Timeboxes And Depth

- **30 minutes**: assets, entry points, boundaries, top three paths. Right for a normal feature, and it catches the majority of serious findings.
- **Half a day**: full path table, per-path controls, assumptions, abuse cases. Right for a new service, a new integration, or anything touching money, authentication or personal data.
- **Multi-day, with the team in the room**: a new architecture, a tenancy model, or a payments path. The value is the shared model as much as the document.

Trigger the deeper tier on: money movement, authentication or authorization changes, personal or regulated data, a new external integration, multi-tenancy, or anything that can deploy to production. Everything else gets the 30 minutes.

## Traps Of Design Review

| Trap | Why it fails | Do instead |
|---|---|---|
| Enumerating threats against a diagram instead of paths against an asset | Produces 60 findings of equal weight and no order of work | Rank paths; three to seven, with reasons |
| Reviewing after the design is built | The review becomes a list of things nobody will change | Review at the decision, when the cost of a change is a conversation |
| A control per threat | Unshippable, and the team routes around security next time | Break the cheapest link per path |
| Treating a framework's mnemonic as the goal | Notation completeness is not coverage | The four questions, then notation only if the audience needs it |
| Ignoring the abuse path | The feature working as designed, at scale, hostile — no scanner ever reports it | One abuse question per entry point |
| Model written once and never re-read | The system changes weekly; a stale model is worse than none because it is believed | The model is an artifact with a read-when condition, updated on boundary changes |

Write it (`memory-template.md`): the threat model as its own file in `~/Clawic/data/cybersecurity/artifacts/`, opening with when to re-read it — "before any change to the payment path or its dependencies" — and getting its `## Boxes` line in the same turn; new trust boundaries, entry points and crown jewels in `## Environment`, keyed by the same names the model uses; each accepted path-closing action as a `## Findings` row with an owner, a due date and the path it removes; each path the team consciously accepts in `## Risk Accepted` with its expiry and a `## Due` row; the detections the model implies in `## Detections`; any new third party the design introduces in `## Vendors`, and the entity itself in `~/Clawic/data/contacts/contacts.md` or `~/Clawic/data/domains/domains.md` rather than duplicated here. A model with no re-read condition is a document; one with a condition is a control.
