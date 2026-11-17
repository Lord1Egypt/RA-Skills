# Detection — Log Sources, Rule Quality, Coverage

A detection is a data source plus a rule plus a response. Missing any of the three and it is a log line (SKILL.md Rule 8). This file covers building the three in that order, because the order is the whole discipline.

**Before writing or tuning any rule**, read `## Detections` in `~/Clawic/data/cybersecurity/memory.md` — or `detections.md` if `## Boxes` points there, including its `## Retired` section, so the noisy rule somebody killed last year does not get re-enabled — plus the `Log Sources` table in `## Environment`, whose `Gap` column already says what you cannot see. `siem_platform` in `config.yaml` decides the dialect below; with `none`, write vendor-neutral pseudo-rules that name the exact fields required.

**Contents:** [Log Sources Before Rules](#log-sources-before-rules) · [The Source Table Worth Maintaining](#the-source-table-worth-maintaining) · [Precision, And The Math That Ends Arguments](#precision-and-the-math-that-ends-arguments) · [The Base Rate Problem](#the-base-rate-problem) · [Anatomy Of A Rule Worth Deploying](#anatomy-of-a-rule-worth-deploying) · [The Detections Worth Having First](#the-detections-worth-having-first) · [Tuning Without Blinding Yourself](#tuning-without-blinding-yourself) · [Coverage As A Gap Map](#coverage-as-a-gap-map) · [Detection As Code](#detection-as-code) · [Health: The Rule That Stopped Firing](#health-the-rule-that-stopped-firing) · [Metrics](#metrics)

## Log Sources Before Rules

Rules written against data you do not collect are the most common wasted effort in security engineering. The sequence:

1. **Inventory what you already have** — identity provider, EDR, cloud audit trail, mail platform, VPN, DNS, firewall. Most organizations own far more telemetry than they query.
2. **Note the retention of each**, and specifically whether it is shorter than your realistic dwell time. Retention shorter than the intrusion makes "what did they touch" *unknown* by construction.
3. **Find the gaps** against the paths that actually matter to this org, from the design work in `design-review.md`.
4. **Only then write rules**, and only for sources that are reliably arriving.

**The order of value for a small organization**, when each source has to justify its ingest cost:

| Rank | Source | Why it ranks here |
|---|---|---|
| 1 | Identity provider sign-in and audit logs | Almost every intrusion is an identity event; also the cheapest source there is |
| 2 | EDR telemetry | Execution, persistence and lateral movement on the endpoint |
| 3 | Cloud control-plane audit (CloudTrail, Entra audit, Admin Activity) | Where an intrusion becomes an account takeover |
| 4 | Mail platform audit, including rules and OAuth grants | BEC's whole footprint |
| 5 | DNS query logs | Cheap, high-value: C2 and exfiltration both need name resolution |
| 6 | Firewall and VPN | Edge exploitation and the egress picture |
| 7 | Application logs | High value when authorization events are logged; usually they are not |
| 8 | Full packet capture | Expensive, rarely retained long enough to matter, last on the list |

## The Source Table Worth Maintaining

For each source, four columns, and the fourth is the valuable one: **what it covers**, **retention**, **arrival health**, **the gap**. "EDR, 30 days raw, healthy, nothing on the two Linux build servers" is a sentence that pre-answers a question you will ask at 3am. This table lives in `## Environment` and is the single artefact that most improves incident outcomes, because it converts an unanswerable question into a known limitation with a date on it.

Field normalization matters more than the platform: agree on where the username, the source address, the hostname and the process live, and every future rule is portable. Adopt an existing schema rather than inventing one — the cost of the choice is trivial and the cost of ad-hoc field names compounds with every rule.

## Precision, And The Math That Ends Arguments

**Precision = TP ÷ (TP + FP)** over the last 30 days. This is the analyst's experience of the rule: out of everything it sent, how much was real.

Recall — of everything real, how much did we catch — is unmeasurable in production because the denominator is unknown. That asymmetry is why precision is the operational metric and recall is estimated through purple-team exercises instead.

Thresholds that work in practice:

- **Above ~50%**: a good rule; the analyst opens it expecting something.
- **10-50%**: acceptable for high-severity techniques, provided the triage step is cheap and scripted.
- **Below ~10%**: tune or retire it. Analysts triage the queue they believe, and a queue nobody believes is a queue nobody reads — the real alert then arrives into an abandoned inbox.
- **Zero true positives in 90 days**: not necessarily bad, but it must be *tested*. An untested rule that has never fired is indistinguishable from a broken one.

Volume math before deployment: expected alerts per day × minutes to triage must fit in the hours you actually have. Ten alerts a day at 15 minutes each is 2.5 hours — a real part of somebody's job, and the decision to spend it should be explicit rather than discovered.

## The Base Rate Problem

The reason "99% accurate" detection is worthless, in one worked example. Suppose 10,000 logins a day and one is malicious. A rule with 99% true-positive rate and a 1% false-positive rate produces 1 true positive and about 100 false positives — precision under 1%. The analyst discards 100 alerts to find 1, and within a week discards all 101.

Three consequences that shape every rule you write:

1. **Rarity beats cleverness.** A rule keyed on something genuinely rare in your environment (a service account logging in interactively, a new inbox rule, a break-glass account used at all) outperforms a sophisticated behavioural model with a 1% error rate on a common event.
2. **Chain conditions to shrink the denominator.** Impossible travel alone is a VPN. Impossible travel *plus* an unmatched device id *plus* no MFA challenge is an incident.
3. **Prefer detections on the attacker's *objective*** — persistence created, credential dumped, backup deleted — over detections on their *tooling*, because objectives are rare in normal operations and tooling changes weekly.

## Anatomy Of A Rule Worth Deploying

Every rule carries all eight, or it is not finished:

| Field | Content |
|---|---|
| Name | What it detects, in plain words |
| Data source | The exact log source and the fields required — the rule is dead if the source stops |
| Logic | The query, with its version history |
| Technique | The ATT&CK id or a plain-language technique name, for coverage mapping |
| Severity and expected volume | What the analyst should feel, and how often |
| **Response action** | The first three steps for the analyst. Without this the alert is a notification |
| Validation | How it was tested — an atomic test, a purple-team exercise, a real incident |
| Precision and last tuned | The 30-day number and the date somebody last looked |

**The response action is the field that gets omitted and the one that matters.** "Investigate" is not a response action. "Check whether the user travelled; compare the device id against their known devices; if unmatched, revoke sessions and call them" is.

## The Detections Worth Having First

Ordered by value per unit of effort for an organization starting from nothing. Each is rare in normal operations, which is what makes it precise.

| Detection | Source | Why it earns its place |
|---|---|---|
| New inbox rule that hides or forwards mail | Mail audit | The BEC signature, high precision, cheap |
| New OAuth consent or service principal with mail/file scopes | Identity audit | Token persistence that survives every password reset |
| New MFA method registered, especially soon after a password reset | Identity audit | The attacker making the account look secure |
| Break-glass or emergency account used | Identity | Should be zero; any firing is meaningful |
| Successful authentication with no MFA challenge | Identity | Finds the legacy path before an attacker does |
| Impossible travel **plus** unmatched device id | Identity | The chained version; alone it is a VPN |
| Password spray shape: many accounts, few attempts, one source | Identity | Catches the campaign, not the individual failure |
| Shadow copy deletion, mass file rename, backup repository change | EDR, backup system | The last minutes before encryption, and the highest-value alert in the estate |
| EDR agent stopped, security log cleared, logging pipeline broken | EDR, endpoint | Anti-forensics; treat as confirmed hostile |
| Cloud: root or top-level account used, IAM policy widened, CloudTrail or audit logging disabled | Cloud audit | The three moves every cloud intrusion makes |
| New public exposure: storage bucket, database, security group opened to 0.0.0.0/0 | Cloud config | Catches the misconfiguration and the attacker equally |
| Credential access on the endpoint: LSASS handle, credential dumping tooling behaviour | EDR | Directly on the objective, not the tool |
| Egress to a newly registered domain, or beaconing with regular intervals | DNS, proxy | C2, before the exfiltration |

Ten well-tuned detections that somebody responds to beat 400 vendor defaults nobody reads. **Turning on everything the vendor ships is the canonical mistake**: precision collapses, the queue is abandoned, and the real alert lands in it.

## Tuning Without Blinding Yourself

- Tune with the **narrowest possible exclusion**: this process on this host by this account, not the process everywhere. Broad exclusions are the attacker's allowlist, and they are invisible six months later.
- Every exclusion carries a reason, a date and an owner. Review the exclusion list quarterly as a `## Due` item — the exclusions, not the rules, are where coverage silently disappears.
- Prefer changing the *environment* over tuning the rule: if a script triggers the credential-dumping detection, fix the script. You have then removed a false positive and an attack technique at once.
- Aggregate rather than suppress. Fifty identical alerts become one alert with a count of fifty; suppression loses the fiftieth, which is the one that was different.
- Retiring a rule is a legitimate outcome and it goes in `## Retired` with the reason. Without that record, the same noisy rule is re-enabled every year by the next person.

## Coverage As A Gap Map

Map detections to techniques (ATT&CK), and read the result as a map of what you cannot see — never as a scorecard.

- **Coverage is measured against techniques, never against the number of enabled rules.** Four hundred rules covering fifteen techniques is fifteen.
- Weight by what applies to you: on-premises Windows techniques are irrelevant to an all-SaaS company, and full-matrix coverage is a vendor's goal, not yours.
- Distinguish three states honestly: no data source (a collection gap), data but no rule (a detection gap), rule but never validated (an unknown). The three have completely different costs to fix, and conflating them produces a heat map that lies.
- **Validate rather than assume.** Atomic tests for individual techniques, purple-teaming for chains. A rule that has never been tested has an unknown state, not a green one.
- Prioritize gaps by the paths in your own threat models (`design-review.md`), not by matrix completeness. The technique an actual attacker would use against your actual architecture ranks above a colourful gap in a column that does not apply.

## Detection As Code

- Rules in version control, in review, with a test case each. A rule changed directly in a console has no history and no author, and the reason for the change is gone in a week.
- Portable rule formats (Sigma and equivalents) are worth it when you may change platform or share with a community; native format is worth it when you exploit platform-specific functions. Pick per rule, not per organization.
- CI on the rule repository: syntax validation, a test against sample events, and a check that the required fields exist in the current schema.
- Deploy new rules in a monitor-only state for a week to measure real volume before they page anybody. The estimate is always wrong, usually low.

## Health: The Rule That Stopped Firing

**"Alerts for a technique that suddenly stopped" is a broken pipeline far more often than an improved environment.** The failure is silent by construction: no data means no alerts means no complaints.

- Every data source needs a heartbeat check — event volume per source per hour, with an alert on a drop past a threshold. This is the single most valuable monitor in the whole detection stack, and it is usually the last one built.
- Alert on the absence of expected events: no sign-in events for 30 minutes during business hours is an outage of your visibility.
- Re-validate rules after any platform change, agent upgrade, schema change or log-format change. Field renames break rules silently.
- Track ingest cost per source alongside its detections; a source that costs more than it detects is a budget conversation, and having the number ready is what wins it.

## Metrics

| Metric | What it tells you |
|---|---|
| Precision per rule, 30 days | Whether the analyst should believe it |
| Alert volume per analyst hour available | Whether the queue is workable at all |
| Time to triage, median and 95th percentile | The tail is where the missed incident lives |
| Technique coverage, weighted by applicability | The gap map |
| Source health: uptime and volume anomalies | Whether your detections exist today |
| Detections that fired in real incidents, and the ones that should have | The only ground truth available; harvest it from every post-incident review |

Not a metric: number of rules enabled, number of alerts generated, number of events ingested. All three go up when things get worse.

Write it (`memory-template.md`): every rule created, tuned or retired as a row in `## Detections` with its source, technique, response action, precision and last-tuned date — and retired rules with their reason, so nobody re-enables them; every new or missing log source, with its retention and its `Gap`, in `## Environment`; each collection gap that needs budget or engineering as a `## Findings` row with an owner and a due date; the exclusion review, the coverage review and any purple-team exercise as `## Due` rows; the detection engineering standard and any validated rule pack in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn. Indicators a rule blocks or hunts for beyond a single incident belong in `indicators.md` with an expiry, never hardcoded into the rule where they will outlive their usefulness silently.
