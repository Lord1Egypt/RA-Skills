# Incident Response — The Lifecycle After The First Hour

Picks up at rung 8 of SKILL.md's First Hour ladder and does not repeat it. Scope here: eradication, recovery gates, the decisions that get made badly under pressure, and the review that turns one incident into a control.

**Before touching an incident**, read `incidents/<year>.md` if the `## Boxes` index in `~/Clawic/data/cybersecurity/memory.md` names it — the awareness timestamp, the previous scope and "we have seen this actor before" all live there — plus `## Scope & Authorization` (what containment is pre-approved) and `## Environment` (log sources and their retention, which decides what questions are answerable at all). `containment_bias` and `edr_platform` in `config.yaml` decide the levers below.

**Contents:** [The Five Phases And What Ends Each One](#the-five-phases-and-what-ends-each-one) · [Roles When There Are Three People](#roles-when-there-are-three-people) · [Scoping: The Question That Actually Matters](#scoping-the-question-that-actually-matters) · [Containment Levers By Layer](#containment-levers-by-layer) · [Eradication Gate](#eradication-gate) · [Recovery Gate](#recovery-gate) · [Communications During](#communications-during) · [Third Parties And Who To Call In What Order](#third-parties-and-who-to-call-in-what-order) · [The Post-Incident Review That Changes Something](#the-post-incident-review-that-changes-something) · [Failure Modes Of The Process Itself](#failure-modes-of-the-process-itself)

## The Five Phases And What Ends Each One

NIST SP 800-61's lifecycle, with the exit condition that stops teams from declaring a phase over because they are tired of it:

| Phase | Ends when |
|---|---|
| Preparation | Not an incident phase — it is the state you are in right now, and it decides everything below. Its measure is retention and reachability, not documents. |
| Detection and analysis | The fact pattern is written: what, when first observed, awareness timestamp, affected identities and hosts, initial access hypothesis with a confidence word |
| Containment | The attacker cannot re-enter with what they already hold — every credential, token, key and grant they touched is dead — and the spread has a boundary you can name |
| Eradication | Every persistence mechanism found is removed **and** the initial access vector is closed; both, or you are containing the same incident twice |
| Recovery | Systems are back with monitoring proving the actor did not come back, on a stated watch period |
| Post-incident | Two dated actions with owners exist, and one detection or control changed |

**The two clocks running in parallel.** Technical scope and legal notification are on different tracks with different owners: analysis paced by evidence, notification paced by statute from the awareness timestamp. Never let one wait for the other — "we will notify when we understand it fully" is how a 72-hour clock is missed, and every regime accepts a phased notification with what is known so far.

## Roles When There Are Three People

Every role below exists in every incident; in a small org one person holds several, and the failure is holding all of them silently.

- **Incident lead** — owns decisions and the timeline, does no hands-on analysis. The moment the lead starts typing in a console, the incident loses its coordinator, and this is the single most common structural failure in small teams.
- **Investigator** — evidence, timeline, scope. Says *confirmed / likely / possible / unknown* with SKILL.md Rule 3's definitions and nothing softer.
- **Scribe** — timestamps, decisions and their reasons, in the incident row as they happen. Reconstructed timelines are wrong and everybody discovers this during the audit, not during the incident.
- **Communicator** — the single voice to staff, customers, counsel, insurer. Multiple voices produce contradictory statements that outlive the incident.
- **Decider outside the incident** — the person who can authorize taking production down. Name them before you need them; their absence is what turns a 20-minute containment into a 6-hour one.

Rotate at 12 hours. Beyond that, judgement degrades measurably and the mistakes are the irreversible kind — an incident on hour 16 of a single lead is how the wrong host gets wiped.

## Scoping: The Question That Actually Matters

Not "which machines have malware" but **"what did the credential reach"**. Modern intrusions are credential-shaped: one foothold, then legitimate authentication everywhere else, which leaves no malware and no alert.

The scope loop, run until it stops producing new entities:

1. From the compromised identity, list every authentication it performed in the window — start 30 days before the earliest confirmed activity, because the discovered start is almost never the real one.
2. From each host reached, list the credentials that were resident on it — cached domain credentials, service account tokens, cloud instance metadata roles, browser session cookies, SSH keys, CI runner tokens.
3. Each of those credentials becomes a new identity in step 1.
4. Stop when a full pass adds nothing new. That closure — not a clean scan — is what "scope confirmed" means.

**Dwell time is why the window is wide.** Mandiant's M-Trends reports have tracked global median dwell time down into the sub-two-week range, but that median is dominated by ransomware, which announces itself; quiet intrusions found by an internal hunt or a third-party notification run much longer. If your log retention is 30 days and the intrusion is older, the honest answer is *unknown* — write it as unknown, do not soften it into "no evidence of".

Cheapest scope checks that repeatedly change the answer: sign-in logs filtered to the attacker's device id and ASN rather than to the user; every account that authenticated from any IP the attacker used; process-creation events on any host the identity touched; new or modified scheduled tasks, services, SSH keys, API keys, OAuth grants and mail rules across the whole tenant in the window.

## Containment Levers By Layer

Pick the lever that stops the path while keeping RAM alive (SKILL.md Rule 2). Each has a tell that reveals it to the attacker.

| Layer | Lever | Reversible | Attacker-visible |
|---|---|---|---|
| Endpoint | EDR network isolation (host stays running, only the EDR channel survives) | Yes, one click | Yes — the operator sees the session drop |
| Identity | Revoke sessions and refresh tokens, disable the account, block sign-in | Yes | Yes, immediately |
| Identity, quieter | Conditional access policy scoping the account to one compliant device or one named location | Yes | Sometimes reads as a network glitch |
| Network | VLAN quarantine, ACL, or DNS sinkhole for the C2 domain | Yes | Sinkhole is quiet; a hard block is loud |
| Cloud | Deny-all SCP or policy on the compromised principal, key deactivation (not deletion) | Yes | Yes |
| Application | Rotate the signing secret, revoke the OAuth grant, disable the integration | Yes | Yes |
| Physical | Pull the network cable, keep power on | Yes | Yes, and it stops your own telemetry too |

Never as containment: power off (destroys memory and often the encryption keys still resident during a ransomware run), reimage before capture, restore from backup before root cause, or "run the AV scan and see".

**Sequence the loud actions.** If containment will be visible anyway, do everything at once in a single planned window — all sessions, all keys, all grants, all hosts — rather than one lever a day. A partial eviction teaches the attacker exactly which door you found and gives them time to use the ones you missed; that pattern is the usual explanation for the actor who returns a week later with no new phishing email.

## Eradication Gate

Do not declare eradication until every line is answered with evidence, not with belief:

- Initial access vector identified and closed. If it is still *unknown*, say so explicitly and treat recovery as provisional — reinfection through the same door is the default outcome otherwise.
- Persistence swept on every affected host and in every affected tenant: scheduled tasks and cron, services and systemd units, run keys and launch agents/daemons, WMI subscriptions, startup folders, SSH `authorized_keys`, new local and directory accounts, group memberships, OAuth grants and service principals, mail rules and forwarding, API keys, device registrations, CI/CD secrets and webhooks.
- Every credential exposed on every touched host rotated — including service accounts, the directory-sync account, and any secret that sat in an environment variable, a config file or a CI log on those machines.
- Golden-ticket class exposure handled: if a domain controller or the directory sync account was compromised, the krbtgt password is rotated twice with the replication interval between the resets, or the attacker keeps minting tickets through every other fix you make.
- Backdoored artifacts checked, not just hosts: images, AMIs, templates, IaC modules, and any build produced during the intrusion window.
- Detections exist for what you just found, so the same technique fires next time (`detection.md`).

## Recovery Gate

Recovery is a decision with conditions, not a moment of relief:

1. Rebuild rather than clean. A cleaned host is a bet against an operator who chose their persistence deliberately.
2. Restore from a backup **predating the confirmed initial access**, not the detection date — the gap between the two is where the backdoored backup lives.
3. Bring systems back in dependency order — identity, then core infrastructure, then the business systems — and put the highest-value system back last, when monitoring has already proved itself on something cheaper.
4. Instrument before restoring: extra logging, the new detections, and a named person watching them.
5. Declare a watch period proportional to the intrusion — commonly two to four weeks of elevated monitoring — with an explicit end date so it actually ends.
6. Reset user-facing credentials on a schedule the help desk can survive, and use a verification path the attacker cannot satisfy — if they own the mailbox, email verification is the attacker's verification.

## Communications During

- Move incident coordination off the potentially compromised channel. If the mail tenant or the chat workspace is in scope, the attacker is reading the incident bridge; use phone or a separate tenant, and say why in one line so nobody re-invites the problem.
- Internal message shape: what is known, what is being done, what staff must do differently today, when the next update comes. Give the next-update time and keep it even when there is no news — silence generates rumours that cost more than the incident.
- Never speculate on attribution or scope outside the incident room. "We are investigating unauthorized access to one mailbox" survives being quoted; "it looks like a nation state" does not survive anything.
- Every external statement goes through counsel once the incident could be notifiable. The first public statement is the one quoted forever, including in the regulator's file.

## Third Parties And Who To Call In What Order

1. **Insurer first, before engaging anyone.** Most cyber policies mandate panel counsel and panel IR vendors; engaging your own firm first is a common way to void the coverage you are paying for. The claims line and the notice clause are in `~/Clawic/data/finances/subscriptions.md`.
2. **Counsel second**, ideally as the engaging party for the IR firm, so the investigation has the best available privilege posture. Counsel owns notification wording and the materiality call, not the technical team.
3. **IR retainer / forensics firm** for anything beyond your team's evidence handling, or when the report has to survive a regulator or a lawsuit.
4. **Law enforcement** where required or where the actor may be sanctioned. They rarely recover anything, they occasionally have decryption keys, and their report can matter for the insurance claim.
5. **The provider whose platform is involved** — cloud, SaaS, registrar, ISP. They hold logs you cannot get retroactively, and their retention is shorter than your investigation; ask on day one, in writing.

Every one of these people is a row in `~/Clawic/data/contacts/contacts.md`, added the first time you need them, because at 3am the search for a phone number costs the first twenty minutes.

## The Post-Incident Review That Changes Something

Run it within two weeks, while the detail is recoverable and the discomfort is still useful. Blameless in tone and specific in output — a review that produces "improve security awareness" produced nothing.

Six questions, in order:

1. When did the attacker start, and when did we know? The gap is the number that matters, and it decomposes into detection gap plus escalation gap — usually the second is larger and nobody measures it.
2. Which control was supposed to stop this, and what actually happened to it? (Absent, disabled, misconfigured, bypassed, or present-and-ignored — the last one is the most common and the most uncomfortable.)
3. Which question could we not answer, and what would have made it answerable? That is a log-source and retention finding, and it goes in the `Gap` column of `## Environment`.
4. What did we do that we would not do again? Name it plainly; this is where the real learning is.
5. What did we get right that was luck rather than design? Luck does not repeat.
6. Two actions, each with an owner and a date. Two, not twelve — a twelve-action list is a list nobody executes.

## Failure Modes Of The Process Itself

| Failure | What it looks like | Fix |
|---|---|---|
| Investigation by committee | Fifteen people on the bridge, nobody assigned to the timeline | Named lead, named investigator, everyone else on request |
| Declaring victory at containment | Ticket closed, no eradication sweep, same actor back in a week | Eradication and recovery gates above, both written |
| Timeline reconstructed afterwards | Timestamps disagree with logs; the regulator notices | Scribe writes it live into `incidents/<year>.md` |
| Tool-driven scoping | "EDR shows nothing on the other hosts" treated as clean | EDR sees execution, not authentication — scope by credential (above) |
| The 3am irreversible action | Wrong host wiped, evidence gone | Any irreversible step requires a second person to confirm the target |
| No end to the incident | Weeks of half-attention, no closure, no review | A written recovery declaration with a watch-period end date |
| Reinfection blamed on the malware | Same intrusion, never closed vector | Reinfection with the same tooling is one incident, not two — reopen the original |

Before the session ends, write it (`memory-template.md`): the incident row and its timeline in `incidents/<year>.md` starting with the awareness timestamp; every remediation action as a row in `## Findings` with owner, due date and the attack path it removes; new log-source gaps in `## Environment`; new detections in `## Detections`; the post-incident review as its own file in `~/Clawic/data/cybersecurity/artifacts/`, with its `## Boxes` line and its read-when condition in the same turn; the watch-period end date and any new drill cadence as `## Due` rows; counsel, insurer and IR contacts in `~/Clawic/data/contacts/contacts.md`; hosts rebuilt or retired in `~/Clawic/data/servers/servers.md`; indicators that will be blocked or hunted beyond this incident in `indicators.md`. Evidence stays in the case store — the file records its name, hash and location only.
