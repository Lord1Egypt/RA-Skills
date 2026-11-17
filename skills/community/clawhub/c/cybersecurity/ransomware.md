# Ransomware And Extortion

Two separate incidents wearing one ransom note: **encryption** (an availability problem solved by restore) and **theft** (a confidentiality problem no payment ever solves). Size them separately or every decision that follows is wrong.

**Before anything**, read `incidents/<year>.md` and any `artifacts/playbook-ransomware.md` the `## Boxes` index in `~/Clawic/data/cybersecurity/memory.md` names — a playbook written calmly beats judgement under pressure — plus `## Environment` for what the backups actually are and `~/Clawic/data/finances/subscriptions.md` for the insurer's notice clause, which constrains who may be engaged in the next hour.

**Contents:** [The First Thirty Minutes](#the-first-thirty-minutes) · [Do Not Reboot: Why](#do-not-reboot-why) · [Sizing The Encryption](#sizing-the-encryption) · [Sizing The Theft](#sizing-the-theft) · [Backups: The Only Question That Matters](#backups-the-only-question-that-matters) · [The Payment Decision](#the-payment-decision) · [Negotiation, If It Happens](#negotiation-if-it-happens) · [Recovery Order](#recovery-order) · [ESXi, NAS And The Backup Server](#esxi-nas-and-the-backup-server) · [Prevention That Actually Removes The Path](#prevention-that-actually-removes-the-path)

## The First Thirty Minutes

In order, and the order is the point:

1. **Write the awareness timestamp** with its timezone. Every legal clock in SKILL.md's Notification Clocks starts here, and encryption plus data theft usually means a personal-data breach.
2. **Do not reboot, do not power off, do not "clean"** any affected machine (below).
3. **Contain at the network and identity layer**: isolate encrypting hosts through EDR, disable the accounts being used, revoke sessions and tokens, and block the identity used to reach the backup system.
4. **Protect the backups before anything else** — take them offline or make the repository immutable now. Modern operators delete backups *before* encrypting, and the window in which you can still save them is minutes.
5. **Check whether it is still running.** Encryption in progress changes the decision: stopping the process or isolating the host mid-run saves whatever is left, and the key may still be in memory.
6. **Capture memory on at least one affected host** before it is touched (`forensics.md`). Some families keep the symmetric key in memory during the run.
7. **Notify the insurer** before engaging any IR firm — engaging your own firm first can void the policy. Then counsel.
8. **Move incident comms off the affected environment.** If the mail tenant is encrypted or compromised, the bridge is compromised too.
9. **Identify the family** from the note, the extension and a sample: ID Ransomware and the No More Ransom project both map notes and extensions to families, and free decryptors exist for a meaningful minority of them — checking costs ten minutes and occasionally ends the incident.

## Do Not Reboot: Why

Three independent reasons, any one of which is sufficient:

- **The key may be in memory.** Several families generate the file-encryption key locally and hold it in RAM for the run. Reboot and it is gone forever.
- **Reboot can complete the attack.** Some deployments encrypt the master boot record or finish encryption on startup, and some run the payload from a startup mechanism installed for exactly this purpose.
- **You lose the scope evidence** — running processes, connections, injected code — that tells you how many other machines are dirty. You would end up with one clean machine and no idea about the rest.

Isolate at the network layer, keep power on. This is SKILL.md Rule 2 in its most expensive instance.

## Sizing The Encryption

- Count affected hosts, shares and services rather than files, and separate *encrypted* from *inaccessible* — a share that is offline because you isolated it is not lost data.
- Establish the earliest encryption timestamp from file `mtime` and the USN journal, then look **backwards weeks**, not hours: the encryption is the last act of an intrusion that typically had days to weeks of quiet access for credential theft and staging. The initial access is never the ransom note.
- Identify what the identity used for encryption could reach that has *not* been encrypted yet — that list is the remaining blast radius and it determines what to isolate next.
- Do not trust "the backup server is fine" until somebody has looked at it with credentials that were not exposed in the intrusion.

## Sizing The Theft

Theft is a separate investigation with a separate legal consequence, and it is the half that decides notification.

- Evidence of exfiltration: sustained outbound volume in flow logs or SRUM counters, archive files staged in temp and profile directories, cloud-storage and file-transfer client artifacts, and connections to legitimate file-sharing services (the modern default — it blends into normal traffic and defeats naive IP blocking).
- **The leak site is evidence, not proof.** Operators inflate claims, republish old data, and list victims who paid. A file tree screenshot is worth more than a claim; a sample is worth more than a tree.
- Reason from access rather than from their claims: what data could that identity reach, over what window, and what does your logging say about actual reads? Where per-item access logging does not exist, the honest answer is *unknown* and that is often what has to be notified.
- Personal data goes into the record as **counts and categories** — "412 customer records, name plus email plus order history" — never as copies of the records. The notification decision needs the category and the count, not the content.

## Backups: The Only Question That Matters

Extortion leverage exists only when restore fails. The audit, in the order that finds problems:

| Check | Failure mode it catches |
|---|---|
| Are the backups reachable with production credentials? | Then they were encrypted too — this is the single most common cause of a paid ransom |
| Are they immutable or offline (object lock, WORM, tape, a separate credential domain)? | Deletion before encryption is standard operator procedure |
| When was the last **timed** restore test, of a full system rather than a file? | Untested backups fail at restore for mundane reasons: missing agents, missing encryption keys, missing dependencies |
| What is the actual restore *rate* in TB/hour on this hardware? | It sets the real recovery time; the number people quote is the backup rate, not the restore rate |
| Does the retention predate the intrusion start? | A backup taken during the dwell time restores the backdoor with the data |
| Are the backup system's own credentials and encryption keys stored outside the environment? | Restoring requires them, and they are usually in the encrypted password manager |

**A decryptor does not replace this.** Even when payment produces a working decryptor, it is slow, it fails on a portion of files, and it decrypts one file at a time on production hardware — organizations that pay still restore a substantial share of systems from backup. Payment buys a tool, not a recovery.

## The Payment Decision

Not a technical decision. Counsel and the executive own it; the technical job is to make it an informed one.

Facts that are not in dispute and belong in the briefing:

- Payment does not delete stolen data. The only enforcement is the criminal's reputation, and re-extortion of the same victim happens.
- Paying an entity or wallet under sanctions is a legal exposure independent of the extortion itself — counsel and the insurer must clear the recipient before any payment is contemplated. This alone can make the answer no.
- The decryptor's performance is a recovery variable to be tested on a sample, not a certainty.
- Insurance policy terms may require pre-approval for payment; paying first can forfeit reimbursement.

What decides it in practice: does a validated restore path exist within the tolerable downtime, and does the theft half have a legal consequence that payment cannot change? If restore works, payment buys only silence — and silence is exactly what cannot be enforced.

## Negotiation, If It Happens

Professional negotiators exist for this and the insurer usually mandates one. If contact happens:

- One channel, one named person, everything logged. Never the person doing the technical recovery.
- Contact buys time and information — proof of decryption on sample files, the file tree of what they hold — regardless of any intent to pay. Deadlines are a pressure tactic and they slip.
- Never reveal insurance coverage, the true value of the data, or the restore progress. Coverage discovered by the operator becomes the floor of their demand.
- Ask for proof of deletion knowing it is unverifiable; the answer's specificity is still information about what they actually hold.

## Recovery Order

1. **Rebuild the identity plane first.** If a domain controller or the identity provider was reached, the environment stays compromised no matter what you restore — including the krbtgt double-rotation and a full service-account rotation (`incident-response.md` holds the eradication gate).
2. Stand up a clean network segment and bring restored systems into it, rather than restoring into the environment the attacker still knows.
3. Restore in dependency order: identity, DNS and directory, then databases, then applications, then user endpoints. Publish a business-priority order agreed with the business *before* restoring, because everybody's system is critical during an outage.
4. Scan and patch every restored system before it rejoins — you are restoring the vulnerability that let them in along with the data.
5. Reset every credential in the environment, including service accounts, API keys and anything in CI, and use a verification path the attacker cannot satisfy.
6. Elevated monitoring for a stated period with an end date, watching specifically for the persistence you may have missed.
7. Only then declare recovery, in writing, with what remains unrestored.

## ESXi, NAS And The Backup Server

The three targets that turn a bad day into an existential one, because each multiplies the blast radius:

- **Hypervisors**: encrypting the datastore takes out every VM at once. Management interfaces must not be reachable from user networks, must not share the directory that user accounts authenticate against, and must be patched on the edge-device clock (SKILL.md's controls table).
- **NAS and file servers**: often the same credential as everything else, often with snapshots the same credential can delete. Snapshots under a separate administrative domain are the control.
- **Backup infrastructure**: treat it as tier-zero. Separate credentials, separate authentication domain, MFA on its console, immutability on the repository, and an alert on any deletion or retention change — that alert is one of the highest-value detections in the whole estate (`detection.md`).

## Prevention That Actually Removes The Path

Ordered by path removed per unit of effort, matching SKILL.md's controls table:

1. **Immutable or offline backups plus a timed, full-system restore test.** This is the control that removes the leverage. Everything else reduces probability; this one caps the consequence.
2. **Phishing-resistant MFA on email, VPN, the identity provider and every administrative interface** — the initial access is overwhelmingly credentials or an unpatched edge device.
3. **Patch internet-facing edge devices on the KEV clock.** Mass-exploited VPN, gateway and file-transfer appliances are the other half of initial access, and they are routinely excluded from the scanner because "they are not servers".
4. **No standing domain-admin, unique local admin passwords, admin identities that never read mail** — these remove the escalation that turns one host into the estate.
5. **EDR in block mode with somebody who responds**, plus an alert on shadow-copy deletion, mass file rename, and backup-repository changes. Detect-only mode during an encryption run is a notification, not a control.
6. **Segmentation that stops SMB and RDP moving laterally between user machines**, so one host is one host.
7. **A tested playbook and a tabletop.** The decisions above are bad when made at 3am for the first time; the playbook is an artifact and belongs in the boxes below.

After the incident, write it (`memory-template.md`): the incident row with awareness timestamp, encrypted scope, stolen-data assessment and outcome in `incidents/<year>.md`; the restore rate and the actual recovery time — the two numbers that will be argued about in the next budget cycle — plus backup topology and immutability state in `## Environment`; every backup, segmentation and identity gap as a `## Findings` row with owner and due date; the restore drill and tabletop cadences as `## Due` rows; the ransomware playbook and the post-incident review as their own files in `~/Clawic/data/cybersecurity/artifacts/`, each with its `## Boxes` line and read-when condition in the same turn; ransom-note indicators, leak-site URLs (defanged) and sample hashes in `indicators.md`; the insurer's claims line and the negotiator in `~/Clawic/data/contacts/contacts.md`. Ransom notes, samples and exfiltrated data stay in the case store — the record holds the hash and the location only.
