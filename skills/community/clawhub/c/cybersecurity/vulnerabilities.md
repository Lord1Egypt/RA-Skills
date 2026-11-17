# Vulnerabilities — Prioritization, SLAs, And The Backlog Nobody Triaged

Scanner output is a list of facts, not a plan. This file turns thousands of rows into an order of work that survives a challenge from engineering and from an auditor.

**Before triaging any backlog**, read `## Findings` in `~/Clawic/data/cybersecurity/memory.md` — or `findings.md` if `## Boxes` points there — so the same issue does not get a second id, and `## Environment` for which assets are crown jewels and which are internet-reachable. Exposure is half of every decision below. `severity_scale` and `remediation_sla_days` in `config.yaml` set the formula and the clock.

**Contents:** [The Gate, In Order](#the-gate-in-order) · [What Each Score Actually Means](#what-each-score-actually-means) · [Exposure Is The Multiplier](#exposure-is-the-multiplier) · [Triaging An Inherited Backlog Of Thousands](#triaging-an-inherited-backlog-of-thousands) · [SLAs That Survive An Auditor And Engineering](#slas-that-survive-an-auditor-and-engineering) · [When You Cannot Patch](#when-you-cannot-patch) · [Reading A Pentest Report](#reading-a-pentest-report) · [Scanner Reality](#scanner-reality) · [Metrics That Are Not Theatre](#metrics-that-are-not-theatre)

## The Gate, In Order

Run each vulnerability through these in sequence and stop at the first hit. This is SKILL.md Rule 4 as a procedure.

1. **In CISA's KEV catalog** → fix now, on the two-week clock BOD 22-01 sets for federal agencies (a defensible default for everyone else). KEV means confirmed exploitation in the wild — it is not a prediction, it is a report.
2. **EPSS ≥ 0.1 and the asset is reachable from the internet** → this cycle. EPSS is the probability of exploitation activity in the next 30 days; 0.1 sounds low and is roughly two orders of magnitude above the median CVE.
3. **The path ends at a crown-jewel asset**, even internally → this cycle, and the finding names the path (SKILL.md Rule 7).
4. **A working public exploit exists and the asset is reachable by anyone untrusted** — including any authenticated employee for an internal service → next cycle.
5. **Everything else** → the normal SLA by severity, batched into maintenance windows. This is the majority, and treating the majority as urgent is what destroys credibility for the first four rows.

**Worked example.** A CVSS 9.8 remote code execution on an internal build server with no public exploit and EPSS 0.002, versus a CVSS 6.5 authentication bypass on the internet-facing VPN appliance that is in KEV. The 6.5 wins outright, every time — rule 1 fires on it and nothing fires on the 9.8. The team that patches by score patches the 9.8 first and is breached through the 6.5.

## What Each Score Actually Means

| Score | Question it answers | Question it does not |
|---|---|---|
| CVSS base | How bad is the wound if exploited, in the abstract | Whether anyone will exploit it, or whether it is reachable here |
| EPSS | Probability of observed exploitation activity in the next 30 days | Impact, or whether *your* instance is exposed |
| KEV | Has it already been exploited in the wild, per confirmed reporting | How likely you specifically are to be hit |
| SSVC | A decision-tree alternative to a single number: exploitation state, exposure, mission impact → act / attend / track | Anything, unless somebody maintains the decision tree |
| Vendor severity | The vendor's own rating, often for their configuration | Your configuration, which may not be affected at all |

Cyentia and Kenna's exploit-prediction research has consistently put the share of published CVEs ever exploited in the wild at roughly 5%. That is the base rate that makes "patch everything by CVSS" the wrong strategy: you spend the same engineering hour on the 95% as on the 5%.

**CVSS is not a risk score, and its own specification says so.** It describes severity. Risk needs exploitability, exposure and asset value, which are the other three inputs of this file.

## Exposure Is The Multiplier

Same CVE, four completely different priorities:

| Where it sits | Multiplier |
|---|---|
| Internet-facing, unauthenticated, no compensating control | Highest — this is where mass exploitation lands |
| Internet-facing behind authentication or a WAF | High; the WAF is a delay, not a fix |
| Internal, reachable by any employee workstation | Medium-high — one phish and the attacker is on that network |
| Internal, reachable only from an administrative segment | Lower, and the finding is really about who can reach that segment |
| Not deployed, not running, or the vulnerable feature is disabled | Not a vulnerability here. Say so and close it |

**Know your edge before triaging.** An external attack-surface inventory — every hostname, IP, port and service you expose, including the appliances excluded from the scanner because "they are not servers" — is the prerequisite. The VPN concentrator, the file-transfer appliance, the load balancer and the network device are precisely the assets that dominate mass exploitation and precisely the ones missing from most scanner scopes (`network-security.md` covers discovering the surface).

## Triaging An Inherited Backlog Of Thousands

The backlog is not a queue to work through; it is a dataset to reduce. In this order:

1. **De-duplicate to the fix, not the finding.** One outdated base image produces hundreds of rows and one action. Group by remediation — "upgrade this package", "rebuild this image", "patch this appliance" — and the count usually falls by an order of magnitude before any prioritization happens.
2. **Remove the noise**: findings on decommissioned assets, informational rows, and anything the compensating control already handles. Do this before anyone sees the number.
3. **Apply the gate above** to what remains. Typically a handful of rows fire on rules 1-3, and that handful is this week's work.
4. **Bucket the rest by fix campaign** — "upgrade OpenSSL fleet-wide", "retire the three servers still on the old OS" — each with an owner and a date. A campaign is executable; a list of 4,000 CVEs is not.
5. **Publish the reduction openly**: "4,200 findings, 380 unique fixes, 9 urgent". The reduction is itself the deliverable, and it is what makes engineering trust the next list.
6. **Set the intake rule** so it never rebuilds: new findings enter the gate automatically, and anything not in rules 1-4 waits for the campaign that covers it.

## SLAs That Survive An Auditor And Engineering

Two audiences with opposite preferences, resolved the way SKILL.md's Where Experts Disagree describes: **keep the severity-to-days table as the contractual floor, and run the exploitation gate as the working order inside it.** The auditor gets a simple defensible table; engineering gets a queue that fixes the exposure that matters first.

Default clocks, from `remediation_sla_days`: critical 7 days, high 30, medium 90, low next maintenance cycle. KEV entries inherit the two-week clock regardless of their CVSS.

Rules that keep the table honest:

- The clock starts at **discovery**, not at ticket creation. Ticket-creation clocks measure your ticketing latency and hide the real exposure window.
- **An SLA nobody meets is worse than a longer SLA everybody meets.** If critical-in-7 is missed 80% of the time, the number is fiction and the metric is lying to the board. Either resource it or change it — and the change is a decision with a name on it.
- Emergency patching is a separate path with pre-approved change authority, not an SLA. Waiting for the weekly change advisory board with a KEV vulnerability on the edge is a process choice with a foreseeable outcome.
- Overdue means escalation to a named person on a schedule, not a red cell in a dashboard nobody opens.
- Every overdue finding is either being worked, formally accepted with an expiry, or the SLA is wrong. There is no fourth state.

## When You Cannot Patch

Legitimate and common: no vendor fix, a certified system, an appliance in a production line, a dependency that breaks. The finding does not disappear — it changes shape.

Compensating controls, ordered by how much of the path they actually remove:

1. **Remove reachability** — take it off the internet, put it behind the VPN, restrict source addresses to the handful that need it. This is the only option that genuinely removes the path rather than raising the cost.
2. **Disable the vulnerable feature or module** where the advisory names one.
3. **Segment it** so compromise stops at that host and cannot reach the identity plane or the crown jewels.
4. **Virtual patching** at a WAF or IPS with a rule specific to the exploit. Effective against commodity exploitation, bypassable by someone who cares, and it decays as variants appear.
5. **Detection with a response action** as the last resort — you are choosing to find out rather than to prevent, which is a valid choice only if somebody actually responds.
6. **Accept it formally**: a dated risk acceptance with an owner, an expiry, the compensating control and the condition that would reopen it. It goes in `## Risk Accepted` with a `## Due` row for the expiry, because an acceptance that lapses unnoticed is an unowned risk wearing a signature.

## Reading A Pentest Report

- **A pentest samples one path at one moment.** Absence of findings is evidence about the test's scope and duration, not about the system. Read the scope and the constraints section first — that is where "we could not test production" and "credentials were not provided" live.
- Re-rate every finding against your own exposure and asset value. Testers rate in the abstract and rarely know which internal host is the crown jewel.
- **The most valuable output is usually the attack narrative, not the finding list.** The chain — low-severity information disclosure plus a default credential plus a flat network equals domain admin — is what you fix; each link alone rates as medium and gets deferred.
- Retest is part of the engagement, not an optional extra. A closed finding that was never retested is a claim.
- Findings feed the backlog through the same gate as everything else. A pentest report is not a work plan and must never become the security programme (`program.md`).
- Feed each finding back into detection: could you have seen the tester do that? The answer is a `## Detections` gap and is worth more than the finding itself.

## Scanner Reality

- **Unauthenticated scans see the surface; authenticated scans see the truth.** Unauthenticated results are dominated by version-banner guesses and miss most of the real exposure. Authenticated scanning is the single biggest quality improvement available to a vulnerability programme.
- Coverage is the metric nobody reports: what fraction of known assets was actually scanned in the last cycle, and what is missing? An asset absent from the scan appears in the report as zero findings.
- Back-ported patches make version checks lie. Enterprise Linux distributions fix a CVE without changing the visible version, so a version-based scanner reports a vulnerability that the vendor already fixed — check the distribution's own advisory before raising it.
- False positives destroy the programme faster than missed findings, because the next real finding is discounted. Verify before assigning, and close false positives with the evidence.
- **Never aggressively scan OT, medical or legacy devices.** Some fail on a single unexpected packet, and the outage becomes your incident. Passive discovery and vendor guidance for those segments, always — and the exclusion is recorded in `## Scope & Authorization`, not remembered.
- Container images need scanning at build time, in the registry, and at runtime for what is actually deployed; the three answers differ, and only the third is what an attacker can reach (`supply-chain.md`).

## Metrics That Are Not Theatre

| Metric | Why it beats "number of vulnerabilities" |
|---|---|
| Mean time to remediate, split by KEV / internet-facing / everything else | The blended average hides the only number that matters |
| Percentage of KEV entries present in the estate, and their age | This is the board number: known-exploited, still open, how long |
| Scan coverage: assets scanned ÷ assets known | An unscanned asset reports zero findings |
| Recurrence rate: findings that come back after being closed | Measures whether the fix was a fix or a reboot |
| Open findings past SLA, by owner | Turns a security problem into an accountable one |
| Exposure reduction: internet-facing services removed or restricted | The only metric on this list an attacker would care about |

Raw open-finding count is not a metric: it moves with scanner coverage, so improving coverage looks like getting worse and turning off a scanner looks like winning.

Write what the triage produced (`memory-template.md`): every finding that will be tracked as a row in `## Findings` with its id, severity, the attack path it removes, owner and due date — never a duplicate id for an issue already there; each risk acceptance in `## Risk Accepted` with its expiry, plus a `## Due` row for that expiry; newly discovered internet-facing services, appliances and crown-jewel dependencies in `## Environment`, and any host in `~/Clawic/data/servers/servers.md`; the scan cadence, the KEV sweep and the pentest cycle as `## Due` rows; the triage ruleset once tuned to this org — the gate, the campaign list, the exclusions — as its own file in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn, because deriving it costs a week and nobody should pay that twice.
