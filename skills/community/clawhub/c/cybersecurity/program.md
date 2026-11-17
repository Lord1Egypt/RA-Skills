# Program — Building The Security Function From Nothing

For the org with no security programme, or the person who just became its owner. Sequenced by attack path removed per unit of effort — never by framework chapter order, which is written for auditing a mature programme and not for building one.

**Before planning**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` (what exists, what the crown jewels are, what logging exists) and `## Findings` for what is already known and unfixed — a new owner rediscovering old findings burns the credibility they need in month one. `org_profile` in `config.yaml` scales everything below: a five-person startup and a 500-person company get the same order and a different depth.

**Contents:** [Week One](#week-one) · [The First Ninety Days](#the-first-ninety-days) · [The Order That Removes The Most Path](#the-order-that-removes-the-most-path) · [Scaling By Organization Size](#scaling-by-organization-size) · [Budget: What To Buy And When](#budget-what-to-buy-and-when) · [Build Or Buy The Watching](#build-or-buy-the-watching) · [Hiring The First Security People](#hiring-the-first-security-people) · [Working With Engineering Without Being The Department Of No](#working-with-engineering-without-being-the-department-of-no) · [Awareness That Is Not A Video](#awareness-that-is-not-a-video) · [Measuring A Programme](#measuring-a-programme) · [The Traps Of A New Programme](#the-traps-of-a-new-programme)

## Week One

Do not write a strategy. Answer six questions, because everything else depends on them:

1. **What would hurt most if it leaked, stopped, or was changed?** Three to five crown jewels, named concretely.
2. **Who has administrative access to each**, including former staff, contractors and service accounts?
3. **What is exposed to the internet**, and who owns each thing?
4. **What logging exists, and for how long?** This decides what any future incident can conclude.
5. **What is the backup, and when was it last restored?** Not "do we have backups" — when was the last restore.
6. **Who would we call at 3am** — counsel, insurer, an IR firm, the cloud provider?

Every answer goes into `## Environment` and `~/Clawic/data/contacts/contacts.md`. The unanswerable ones are your first findings, and they are usually more valuable than anything a scanner will produce.

## The First Ninety Days

| Period | Focus | Deliverable |
|---|---|---|
| Days 1-14 | Discovery: the six questions, the asset picture, the existing pain | A written current-state with the gaps named, no recommendations yet |
| Days 15-30 | The cheap wins: MFA on the critical accounts, remove the internet exposure nobody needed, audit logging on and exported | Two or three visible fixes that cost nothing and prove the function works |
| Days 31-60 | The identity and backup foundations: privileged access cleanup, a timed restore test, the leaver process | A restore test result and a privileged-access inventory, both dated |
| Days 61-90 | Visibility and the plan: EDR coverage, the first detections, the incident contact list, and a one-page roadmap with costs | A roadmap the business signs off, in business language |

**Ship something visible in the first month.** A new security function that spends 90 days assessing and then presents a strategy has spent its credibility before it starts. Fix something real and tell people you fixed it.

## The Order That Removes The Most Path

The sequence, for an organization starting from nothing. Each step removes a path an actual attacker uses, and each is cheap relative to the one after it.

1. **MFA on email, the identity provider, VPN, remote access and administrative accounts** — phishing-resistant on admin accounts. Credentials and phishing dominate initial access; Verizon's DBIR has repeatedly put the human element at roughly two-thirds of breaches.
2. **Backups: offline or immutable, with a timed full restore test.** This is the only control that caps the worst-case consequence rather than reducing its probability.
3. **Patch and inventory the internet-facing edge**: VPN concentrators, gateways, file-transfer appliances, anything with a public login. The other half of initial access.
4. **Remove the internet exposure you do not need at all.** The cheapest control there is: services deleted cannot be exploited.
5. **Separate admin identities, no standing domain admin, unique local admin passwords.** Removes the escalation from one host to the estate.
6. **EDR with block mode and somebody who responds**, on every endpoint that can be enrolled.
7. **Audit logging on, exported off the platform, retained past your realistic dwell time.** Everything after this depends on being able to see.
8. **The leaver process, verified.** Sample it; the number of survivors is never zero the first time.
9. **The five detections that matter** (`detection.md`), with a response action each.
10. **Vulnerability management with the exploitation gate**, not a scanner dumping thousands of rows.
11. **The incident basics**: contact list, the insurer's terms read *before* the incident, a one-page playbook, and one tabletop.
12. **Everything else** — awareness, policies, frameworks, maturity models.

Framework order inverts this: policies and governance first, technical controls later. That order is correct for demonstrating a programme and wrong for building one, because it spends the first six months producing documents while every path stays open.

## Scaling By Organization Size

| `org_profile` | Reality | What the programme is |
|---|---|---|
| solo | No IT, everything is SaaS, the founder is the admin | Steps 1-4 plus a password manager and device encryption. An afternoon of work removes most of the realistic risk |
| startup | Cloud-native, no security staff, a growing engineering team | Steps 1-9 owned by an engineer with a fraction of their time; buy managed detection rather than building it; secure the pipeline early because it is small enough to change |
| smb | Mixed on-prem and cloud, an IT team, no security team | The full list, with a part-time or fractional security owner and an MSP for the watching. The gap here is nearly always identity and backups, not tooling |
| enterprise | Multiple teams, existing tooling, real budget | The list is done unevenly; the work is coverage, consistency and evidence, and the hard problem is organizational rather than technical |
| msp | You hold the keys to many customers | Your own tenant is the crown jewel, because your compromise is all of theirs at once: separate customer credentials, per-customer isolation, MFA on every management tool, and the assumption that you are a high-value target |

## Budget: What To Buy And When

Order of purchase, when each dollar has to justify itself:

1. **Free or included first.** MFA, cloud-provider security defaults, OS hardening, logging, the identity provider features you already pay for. Most organizations own more capability than they have enabled — this is the highest-return week of work available.
2. **Password manager and MDM** — cheap, high leverage, and they make everything else enforceable.
3. **EDR**, which is the first substantial line item and the one worth paying for.
4. **Backup with immutability**, if what exists is not immutable.
5. **Managed detection and response**, when nobody can watch at 3am (below).
6. **Vulnerability management** and external attack-surface monitoring.
7. **Cyber insurance** — read the notice clause, the panel requirements and the exclusions before buying, because they constrain your incident response.
8. **Everything else**, only against a named path it removes.

Two rules that survive a budget challenge: **do not buy a tool you have nobody to run**, since an unwatched tool is a licence with a false sense of coverage; and **estimate the operating cost** — tuning, triage, integration — which frequently exceeds the licence.

## Build Or Buy The Watching

Below roughly the size where you can staff a 24/7 rota — which needs several analysts, not one — coverage is the argument and managed detection wins. Above it, context is the argument and in-house wins. The hybrid that works in practice: MDR for triage, in-house owning detection engineering and response decisions.

What to demand from a provider, because the market's default contract is weak on all four: their detection content and how it is tuned to you; their response authority — can they isolate a host, or only email you; the escalation path and the actual time to a human; and access to your own raw logs, so leaving them does not mean losing your history.

**MDR does not remove the need for an owner on your side.** Someone must receive escalations, make containment decisions, and act at 3am. A managed service with nobody answering the phone is a very expensive log archive.

## Hiring The First Security People

- **The first hire is a generalist engineer with security judgement**, not a specialist and not a manager. The work in year one is building and fixing, not governing.
- Second hire depends on where the pain is: detection and response if the estate is noisy and unwatched, application security if the product is the risk, compliance if revenue is blocked by audits.
- **A GRC-first hire in a company with no technical controls produces documentation of an insecure environment.** It is the most common early mis-hire and it is expensive in credibility as well as salary.
- Fractional and virtual CISOs are a genuine fit for smb and below: strategy, board communication and vendor selection a few days a month, with the execution done by engineering.
- Judge candidates on how they reason about a path and a trade-off, never on certification count or tool familiarity.

## Working With Engineering Without Being The Department Of No

- **Bring the fix, not just the finding.** A pull request beats a ticket; a working example beats a policy.
- Meet them in their tooling: findings in the issue tracker with the right labels, checks in CI, guardrails in the platform. Security in a separate spreadsheet is security nobody sees.
- **Build the paved path.** A secure default that is easier than the insecure one wins every time, and it scales without you. The template, the module, the library, the pipeline check.
- Say yes with conditions rather than no. "Yes, behind the proxy, with these two logs enabled" is a partnership; "no" routes around you next time and you stop hearing about changes.
- Prioritize their time as carefully as your budget: a list of three things engineering will actually do beats thirty they will not.
- Publish the reasoning. Engineers comply with what they understand and route around what they do not.

## Awareness That Is Not A Video

- The annual compliance video changes nothing except the training-completion metric. Its value is evidence for an auditor, and it should be treated as exactly that.
- What works: role-specific and short. Finance gets payment-verification, developers get the classes in their own code, executives get targeted-attack briefings.
- **Make reporting easy and rewarded.** The report button and the culture around it produce more security than any curriculum — report rate and time-to-first-report are the metrics (`phishing.md`).
- Just-in-time beats scheduled: the warning at the moment of the risky action is remembered; the module from March is not.
- Never punish. Punishment collapses reporting, which hides the incidents you need to see.
- Onboarding is the highest-attention moment there is: five minutes on the three things that matter here beats an hour in month nine.

## Measuring A Programme

| Measure | Why |
|---|---|
| Coverage: percentage of assets with MFA, EDR, logging, backup, patching in SLA | Coverage gaps are where incidents happen, and the denominator forces asset honesty |
| Time: awareness to containment, discovery to remediation for exploited classes | The numbers that decide incident cost |
| The restore test: date, duration, completeness | The only meaningful measure of the control that caps the worst case |
| Findings past SLA, by owner | Turns security debt into accountable work |
| Exposure: internet-facing services, and the trend | The number an attacker would care about |
| Incident count and cost, with the near misses | Honest, and the trend is the story |

Not measures: number of tools, number of policies, training completion, blocked attacks, maturity score with no delta. All of them can improve while the organization gets less secure.

## The Traps Of A New Programme

| Trap | Why it fails |
|---|---|
| Framework-first: writing an ISMS before turning on MFA | Six months of documents with every path still open |
| The pentest as the programme | It samples one path at one moment; findings feed the backlog, they are not the plan |
| Buying tooling to substitute for an owner | An unwatched tool is a licence and a false sense of coverage |
| Announcing a three-year strategy in month one | Spends credibility before delivering anything; ship a visible fix first |
| Copying a large enterprise's programme | Their controls assume staff you do not have; the result is shelfware |
| Optimizing for the audit | Produces evidence of controls rather than controls |
| Treating awareness as the primary control | Places the whole burden on the person with the least information at the worst moment |
| Never saying what you are *not* doing | An unwritten scope means every gap is a surprise; write the accepted risks down with expiries |

Write it (`memory-template.md`): the current-state picture — crown jewels, systems, trust boundaries, log sources with their retention and gaps — in `## Environment`; every gap as a `## Findings` row with an owner, a due date and the path it removes, so the roadmap and the finding register are the same artifact rather than two that diverge; each consciously deferred item in `## Risk Accepted` with an expiry and a `## Due` row, because "we are not doing that yet" is a decision that needs a review date; every recurring control — access review, restore drill, tabletop, pentest, phishing simulation, vendor reassessment, KEV sweep — as a `## Due` row with its cadence; the 3am contacts, the insurer, counsel and the MDR escalation path in `~/Clawic/data/contacts/contacts.md`; tooling subscriptions and the cyber policy in `~/Clawic/data/finances/subscriptions.md`; the roadmap itself, the security policy set and the board narrative in `~/Clawic/data/cybersecurity/artifacts/` with their `## Boxes` lines in the same turn; and if the remediation is tracked as work with a deadline, its summary and owner in `~/Clawic/data/projects/<project>.md`, with the security detail staying here and referenced by name.
