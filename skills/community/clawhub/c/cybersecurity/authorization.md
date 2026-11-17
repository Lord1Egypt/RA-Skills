# Authorization — Scope, Rules Of Engagement, Disclosure

The gate in SKILL.md Rule 1, as a procedure: how to establish that testing is authorized, what to do when it is not, and how to handle a researcher who arrives with a vulnerability.

**Before proposing anything that touches a real system**, read `## Scope & Authorization` in `~/Clawic/data/cybersecurity/memory.md` — the systems in scope, the exclusions, the disruption allowed, the approval chain, and the confirmation date. Scope older than the last environment change is not scope. `authorized_scope_file` in `config.yaml` names the long version; `safety_posture.live_commands` says whether commands may be run at all or only described.

**Contents:** [The Three Questions](#the-three-questions) · [What Counts As Authorization](#what-counts-as-authorization) · [Rules Of Engagement](#rules-of-engagement) · [Fallbacks When Scope Is Missing](#fallbacks-when-scope-is-missing) · [Testing Somebody Else's Platform](#testing-somebody-elses-platform) · [Actions That Need A Second Confirmation](#actions-that-need-a-second-confirmation) · [Receiving A Vulnerability Report](#receiving-a-vulnerability-report) · [Disclosing A Vulnerability You Found](#disclosing-a-vulnerability-you-found) · [Running A Bug Bounty Or VDP](#running-a-bug-bounty-or-vdp) · [The Boundary This Skill Does Not Cross](#the-boundary-this-skill-does-not-cross)

## The Three Questions

Before anything touches a real system, all three must have an answer. Missing any one → describe instead of executing, and use a fallback below.

1. **Who owns it?** Not who asked. The person with authority over the system, which for a hosted service is frequently the provider rather than the user, and for a client's environment is the client rather than your customer.
2. **What does the written scope say?** Systems in, systems explicitly out, addresses, accounts, time windows, and the techniques permitted.
3. **How much disruption is allowed?** No impact, degradation acceptable in a window, or full — including whether social engineering, denial of service and physical access are in or out.

**Ambiguity is a boundary problem, not a creativity prompt.** The instinct to interpret an unclear scope generously is the instinct that produces the incident. Ask, and record the answer with its date.

## What Counts As Authorization

| Is | Is not |
|---|---|
| A signed engagement letter or a statement of work naming systems and windows | "Go ahead, have a look" in a chat message |
| A written scope from the system owner, with dates | Permission from a user of the system who does not own it |
| A published safe-harbour policy or bug-bounty programme, and staying inside its stated scope | A vendor's marketing claim that they welcome research |
| An internal authorization from someone with authority over the asset, recorded | An assumption that internal means allowed |
| A cloud provider's stated testing policy, for your own resources within its limits | Testing a SaaS product because you are a paying customer |
| A client's authorization, for a client's system | Your customer's authorization for their customer's system |

Two recurring traps: **the asset that belongs to someone else** — the acquired subsidiary still owned by the seller, the marketing site run by an agency, the SaaS tenant hosted by a vendor — and **the third-party impact** of testing your own system when it is hosted on shared infrastructure or integrates with a partner. Both need their own authorization, and neither is covered by yours.

## Rules Of Engagement

Written before the work starts, kept where both sides can see it:

- **Scope**: exact hostnames, addresses, accounts, applications, and anything explicitly excluded. Wildcards need an explicit statement about what they include.
- **Windows**: when testing may run, and when it must not — trading hours, month-end close, clinical hours, production releases.
- **Techniques permitted**: exploitation or proof-of-existence only, credential attacks, lateral movement, social engineering, physical, denial of service. Each named, not implied.
- **Data handling**: whether real data may be accessed at all, how much is enough to prove the finding (one record, never a dump), where evidence is stored, and when it is destroyed.
- **Source addresses** the testing will come from, so the defenders can distinguish you from an actual intruder afterwards.
- **Emergency contacts on both sides**, reachable during the window, with a stop phrase that halts everything immediately.
- **Escalation triggers**: what to do on finding a critical vulnerability, evidence of a prior compromise, or personal data outside the expected scope. Finding somebody else already inside stops the test and starts an incident.
- **Deconfliction**: whether the defenders know. If they do not, one named person must, or their genuine incident response will run at full cost against you.
- **Retest terms and the report's audience**, agreed at the start rather than negotiated at the end.

## Fallbacks When Scope Is Missing

Never nothing. Every one of these delivers value without touching a system you are not authorized to touch:

- **Lab reproduction**: build the vulnerable configuration locally and demonstrate it there. Proves the finding with zero exposure.
- **Read-only review**: architecture, configuration exports, code, IaC, policies. Usually finds more than a scan would, and needs no execution authorization.
- **Tabletop**: walk the attack path with the people who own the systems. Frequently produces better findings than testing, because the assumptions surface in conversation.
- **Detection logic**: write the rules that would catch the technique. Useful regardless of whether the vulnerability is ever confirmed.
- **Remediation design**: specify the fix, the rollout and the verification, so the moment authorization arrives the work is ready.
- **Passive external reconnaissance** using public sources only — certificate transparency, DNS, internet-wide scan datasets — which touches nothing of theirs.
- **Documentation review**: their own diagrams and runbooks against reality, with the gaps as findings.

State plainly which one you are doing and why: "no scope on file for that host, so this is a read-only review of the configuration you provided" is a professional answer, not a refusal.

## Testing Somebody Else's Platform

- **Cloud providers** publish testing policies. Your resources within the stated limits are generally fine; the provider's managed services, other tenants, and anything resembling a denial-of-service test are not. Read the current policy rather than a remembered version.
- **SaaS products**: being a customer is not authorization. Many run a bug-bounty or disclosure programme — use it, stay in its scope, and use a test tenant.
- **Managed hosting and shared infrastructure**: your application is yours; the platform is not, and a test that degrades the platform affects other customers.
- **Third-party integrations and webhooks**: testing your side is yours; sending traffic to their endpoint is theirs.
- **Personal devices and staff accounts**: an employee's device is not automatically in scope, and in many jurisdictions employee monitoring has its own legal requirements independent of any security justification.

## Actions That Need A Second Confirmation

Even inside authorization, some actions ship with their consequence stated and an explicit confirmation — never buried inside a block of read-only checks (SKILL.md's Output Gates):

| Action | Consequence to state |
|---|---|
| Anything that writes, deletes or modifies data | Irreversible without a restore |
| Account disable, session revocation, key deactivation at scale | Users locked out; a service outage if a service account is caught |
| Host isolation or reimaging | Loss of volatile evidence; the user loses their machine |
| Firewall or policy change | Can black-hole production, and rollback may need the access you just blocked |
| Anything visible to an attacker during an active incident | Tips them off; may trigger destruction or encryption |
| Scanning OT, medical or legacy segments | Device failure and a real-world outage |
| Password or key rotation on shared credentials | Everything using that credential breaks, and the inventory of consumers is usually incomplete |

The pattern: state what it does, state what it breaks, state whether it is reversible, then ask. One action per confirmation — a batch of five with one "proceed?" is not a confirmation.

## Receiving A Vulnerability Report

An external researcher emailing you is a disclosure with a clock and a reputational tail. The response is a process, not an improvisation:

1. **Acknowledge within a day**, in a human voice, with a reference. Silence is what turns researchers into public disclosers.
2. **Never threaten.** Legal aggression against a good-faith reporter is the single most reliable way to convert a private finding into a public story, and it deters the next reporter who would have told you quietly.
3. **Triage on the report's evidence**, and reproduce before disputing. Ask for detail rather than assert it is invalid.
4. **Give a remediation timeline** and keep them updated. Researchers accept slow; they do not accept silence.
5. **Check for exploitation**: if it is real, has anybody else found it? That question makes it an incident investigation as well as a fix.
6. **Credit them** if they want it, and honour any coordinated disclosure date you agree.
7. **Publish a security contact** — a `security.txt` file and a monitored address — so the next report reaches you rather than a sales inbox or social media.

If the reporter demands payment for details before disclosing, that is extortion rather than research, and it is handled as an incident with counsel involved.

## Disclosing A Vulnerability You Found

- Contact through their published channel — `security.txt`, a disclosure programme, a security address. Failing that, a technical contact rather than support.
- Report the minimum that proves it, and stop testing the moment you have it. Continued poking after the finding is what turns research into unauthorized access.
- Never access, download or retain their data. One record is proof; a dataset is a breach with your name on it.
- Give a reasonable deadline and say what happens after it. Common practice is 90 days with an earlier date for actively exploited issues, which industry disclosure programmes have made a de facto norm.
- Document everything you did and when, from the first request. If the relationship goes badly, your log is the record of good faith.
- Know the legal terrain: unauthorized access statutes exist in most jurisdictions and good intent is not always a defence. Where the target has no safe-harbour policy, the safest useful action can be a report with no proof-of-concept.

## Running A Bug Bounty Or VDP

- **A vulnerability disclosure policy comes first**, and it is free: a published scope, a safe-harbour statement, a contact, and a commitment to respond. Most of the value of a bounty without any of the cost.
- Do not start a paid bounty until you can fix things. A bounty against an untriaged backlog buys expensive duplicates of findings you already had.
- Scope explicitly, including what is out, and state clearly that denial of service, social engineering and physical testing are excluded unless you mean otherwise.
- Safe harbour must be unambiguous, because researchers read it as a legal document and it is the term that decides participation.
- Budget triage time, not just bounties: triage is the real cost, and an unresponsive programme damages the reputation it was meant to protect.
- Duplicate and out-of-scope handling should be generous and fast. The reputational return on being pleasant to researchers is disproportionate.

## The Boundary This Skill Does Not Cross

Defensive work, always. Not provided under any framing: malware or exploit development for use against live targets, credential-theft tooling, persistence or anti-forensics techniques, detection-evasion for real environments, or anything meaningfully enabling abuse of a system the user has not shown authorization for. "It is my own system" changes what can be reviewed and reproduced; it does not turn the skill into an offensive capability.

Nor does it monitor individuals: monitoring here means the user's own systems and logs, under a scope they own. Employee monitoring, partner surveillance and device tracking are refused as a class, whatever the security framing, and the request itself is worth naming plainly rather than answering sideways.

Write it (`memory-template.md`): the authorization — owner, systems in scope, exclusions, disruption allowed, approval chain, source addresses, and the confirmation date — in `## Scope & Authorization`, with the long version at the path in `authorized_scope_file`; the emergency contacts on both sides, and any external researcher you now have a relationship with, in `~/Clawic/data/contacts/contacts.md`; each finding from an authorized test in `## Findings` with owner, due date and the attack path it removes; the rules of engagement, the disclosure policy and the researcher-response template as their own files in `~/Clawic/data/cybersecurity/artifacts/` with their `## Boxes` lines in the same turn; the scope re-confirmation and any retest date as `## Due` rows. Scope is never widened on inference — re-confirm and re-date instead.
