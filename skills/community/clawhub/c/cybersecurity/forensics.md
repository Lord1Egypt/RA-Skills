# Forensics — Evidence, Artifacts, And Timelines

Answering "what did they touch?" in a way that survives a lawyer, a regulator, or your own re-reading in six months.

**Before collecting anything**, read `## Scope & Authorization` in `~/Clawic/data/cybersecurity/memory.md` — imaging a device you do not own, or a personal device an employee brought, is a legal problem before it is a technical one — and the `Log Sources` table in `## Environment` for what retention you actually have. Read `incidents/<year>.md` if `## Boxes` names it: the awareness timestamp anchors every timeline you are about to build.

**Contents:** [Order Of Volatility](#order-of-volatility) · [Collect Before You Analyze](#collect-before-you-analyze) · [Chain Of Custody: The Six Fields](#chain-of-custody-the-six-fields) · [Windows Artifacts That Answer Questions](#windows-artifacts-that-answer-questions) · [macOS Artifacts](#macos-artifacts) · [Linux Artifacts](#linux-artifacts) · [Cloud And SaaS: What You Cannot Get Retroactively](#cloud-and-saas-what-you-cannot-get-retroactively) · [Building The Timeline](#building-the-timeline) · [Anti-Forensics And What It Leaves Behind](#anti-forensics-and-what-it-leaves-behind) · [When To Stop, And When To Hand Over](#when-to-stop-and-when-to-hand-over)

## Order Of Volatility

RFC 3227's ordering, with the practical half-life. Collect top-down; anything below survives the step above.

| Tier | What | Gone when |
|---|---|---|
| 1 | CPU registers, cache | Instantly; irrelevant outside research |
| 2 | RAM: running processes, injected code, decrypted config, encryption keys, clipboard, unsaved documents | Power off, reboot, and progressively as memory is reused |
| 3 | Network state: established connections, ARP and DNS cache, listening sockets | Minutes; reboot |
| 4 | Running-system state: logged-on sessions, open files, loaded drivers, scheduled tasks | Reboot |
| 5 | Disk: filesystem, deleted-but-unallocated data, journals | Reimage, secure wipe, disk reuse |
| 6 | Remote and archival logs, backups, cloud audit logs | Their retention window — which nobody controls and everybody assumes is longer than it is |

**The counterintuitive one is tier 6.** It sits at the bottom of the volatility list but is frequently the *first* thing to disappear in practice, because SaaS and cloud audit retention runs on a fixed clock. A mailbox audit trail with 90-day retention expires on schedule whether or not your investigation is finished. Export the shortest-retention log source in the first hour, even before disk imaging, and record the export's hash.

## Collect Before You Analyze

Two different jobs, and mixing them is how evidence gets contaminated.

- **Memory before disk, always**, on any host still running that matters. Memory holds the decrypted payload, the C2 configuration, the process ancestry, and — during a ransomware run — sometimes the encryption key. A memory image is minutes of work and unrecoverable an hour later.
- **Triage collection beats full disk imaging when time is scarce.** A structured artifact collection of a few gigabytes answers most questions in a fraction of the time; reserve full physical imaging for the small number of hosts where deleted-file recovery or a court proceeding is genuinely in play.
- **Hash at collection, verify after transfer.** SHA-256 of every artifact, recorded before it moves. An artifact with no acquisition hash is a file, not evidence.
- **Work on copies.** Analysis on the original is the single mistake that voids everything downstream, and it is unrecoverable.
- **Record the collection command itself**, verbatim, with its timestamp and the operator. Reproducibility is the difference between a finding and an assertion.
- **Timezone discipline**: convert everything to UTC in the timeline and keep the original timezone in the raw record. Half of all timeline errors are a system clock and an analyst assumption disagreeing silently — verify each source's clock offset against a known event before trusting its ordering.
- **Live response on a compromised host is itself an intrusion into evidence**: every command you type creates artifacts and overwrites unallocated space. Minimize, document, and prefer the EDR's collection path where one exists (`edr_platform`).

## Chain Of Custody: The Six Fields

For each item, from acquisition to disposal: **what** (item, source host, description), **when** (acquisition timestamp with timezone), **who** (person acquiring, by name), **how** (tool and exact command, tool version), **hash** (algorithm and value), **where** (storage location and access control). Each transfer appends a row with the same six fields.

Storage rule for this skill: the memory file records the item name, its hash, its custody location and who holds it. The evidence itself never enters `~/Clawic/data/` — a malware sample copied there is a live malicious file in a folder nobody scans, and a mailbox export there is a second copy of the breach.

## Windows Artifacts That Answer Questions

| Question | Artifact |
|---|---|
| Who logged in, from where, how | Security log 4624 with logon type (2 interactive, 3 network, 10 RDP, 9 runas-with-new-credentials — the classic pass-the-hash tell), 4625 failures, 4648 explicit-credential use |
| Did they get admin | 4672 special privileges assigned at logon; 4732/4728 additions to a privileged group |
| What ran | 4688 process creation **with command line auditing enabled** — off by default, and its absence is the most expensive gap on Windows; Sysmon event 1 where deployed |
| What ran when there are no process logs | Prefetch (execution evidence with run counts and last-run times, workstations only), Amcache and Shimcache (presence and path, weaker timing semantics), SRUM (per-process network bytes — the exfiltration estimator nobody uses), UserAssist and BAM |
| Persistence | 7045 service installed, 4698 scheduled task created, run keys, WMI subscriptions, startup folders, 4720 account created |
| What files existed or moved | `$MFT` and the USN journal — the USN journal survives deletion and shows renames, which is how mass-encryption timing gets reconstructed |
| Lateral movement out | RDP client artifacts, 3 network logons on the destination, `\\host\c$` access, remote service creation on the target |
| Remote access in | RDP operational logs (`TerminalServices-LocalSessionManager` 21/25 for session start and reconnect), VPN appliance logs |
| Data staged for exfiltration | Archive files in temp and profile directories, unusually large recent writes, SRUM egress counts, cloud-sync client logs |
| Anti-forensics | 1102 security log cleared, 104 other log cleared, EDR service stop, `wevtutil cl`, USN journal deletion |

Enable command-line auditing and PowerShell script-block logging *before* the incident; retrofitting them mid-incident gives you evidence starting now and nothing about what happened.

## macOS Artifacts

- **Unified logs** — `log show --predicate ... --last 7d` — rich but short-lived; the on-disk archive rotates in days on a busy machine, so export early. `log collect` produces a portable archive.
- **Persistence lives in launch agents and daemons** — `Library/LaunchAgents` inside each user's home, plus `/Library/LaunchAgents` and `/Library/LaunchDaemons` system-wide — as well as login items, configuration profiles (`profiles -P`), and `/etc/periodic` and cron for the older tooling.
- **Quarantine and provenance**: the `com.apple.quarantine` extended attribute records the download source and the app that wrote it; `LSQuarantineEvent` in `QuarantineEventsV2` holds the URL history of downloads.
- **TCC** (`TCC.db`) shows which apps hold camera, microphone, screen-recording, full-disk-access and accessibility permissions — accessibility and full disk access are the two an attacker actually wants.
- **FSEvents** gives filesystem change history that survives deletion of the files themselves.
- **Notable gap**: with SIP and FileVault active, no consumer tooling images an encrypted volume without credentials; a live triage collection under a logged-in admin session is usually the only practical path, and it must be authorized in writing.

## Linux Artifacts

- `auth.log` / `secure` for authentication and sudo; `journalctl` for the systemd view; `wtmp`, `btmp`, `lastlog` for sessions — all trivially editable by root, so treat them as leads and corroborate with a second source.
- **auditd is the only real answer for execution** on Linux, and it must be configured beforehand. Without it, execution evidence is largely absent and honest reporting says so.
- Persistence sweep: `crontab -l` for every user plus `/etc/cron*`, systemd units and timers (including user units under `~/.config/systemd/user`), `~/.ssh/authorized_keys` on every account, `LD_PRELOAD` and `/etc/ld.so.preload`, shell rc files, `/etc/passwd` entries with UID 0 or a new shell, kernel modules, and package-manager hooks.
- Containers evaporate: a compromised container's filesystem disappears on restart. Capture from the host — the container's writable layer under the runtime's storage directory, plus the image digest and the runtime logs — and treat the image itself as the durable artifact (`endpoints.md` covers what EDR sees inside containers).
- Timestamps: `ctime` cannot be set by ordinary tooling the way `mtime` can, so a file whose `mtime` predates its `ctime` by a suspicious margin is a timestomping tell.

## Cloud And SaaS: What You Cannot Get Retroactively

The defining property of cloud forensics is that the evidence is a subscription setting somebody made months ago.

| Platform | Always there | Only if enabled beforehand |
|---|---|---|
| AWS | CloudTrail management events, 90 days in Event history | Data events (S3 object-level, Lambda invoke), VPC flow logs, DNS query logs, longer retention via a trail to S3 |
| Azure / Entra | Sign-in and audit logs, retention by licence tier | Unified audit log detail, mailbox item access, longer retention via a diagnostic setting to a workspace |
| Google Cloud / Workspace | Admin Activity audit logs, long default retention | Data Access logs (opt-in, and the ones you need), Drive and Gmail detail by edition |
| M365 mailboxes | Basic audit trail | Per-item read events — the difference between "they had access" and "they read these 40 messages", and it is a licence tier, not a setting you can enable after the fact |

Consequences that shape the first hour: **export before you investigate**, because portal retention expires on a clock; snapshot the volumes of an affected instance rather than logging into it; preserve the machine image, not the running instance; and if the answer to "what did they read" requires a log tier the org does not have, the honest finding is *unknown* plus a control recommendation, never an inferred "no evidence of access".

## Building The Timeline

- One table, UTC, one row per event, with three mandatory columns: source, observed fact, confidence (SKILL.md Rule 3). A row with no source is a hypothesis and belongs in prose.
- **Super-timeline tooling** (Plaso/log2timeline and equivalents) is right for a disk image and wrong for everything else — it produces millions of rows, and the analysis is the filtering, not the generation. Anchor on a known event and expand outward in both directions rather than reading forward from the beginning.
- **Pivot on the strongest identifier available**, in this order of durability: TTP and technique, tooling, host and network artifacts, domain, IP address, hash. The bottom of that list is what an attacker changes in seconds; the top is what they would have to rebuild.
- Mark inferred rows as inferred, and keep the reasoning in a separate sentence from the observation. Auditors and lawyers read the confidence column first.
- The timeline is finished when the initial access event has a source, not when the rows stop arriving.

## Anti-Forensics And What It Leaves Behind

Every destruction technique creates its own artifact — the absence is the evidence:

- Cleared event log → 1102/104 and a discontinuity; the surrounding logs on other hosts still show the session.
- Timestomped file → `ctime` inconsistency, `$MFT` `$STANDARD_INFORMATION` versus `$FILE_NAME` disagreement, and a nanosecond field of zeros.
- Deleted files → USN journal entries, `$MFT` residue, shadow copies, backups.
- Disabled EDR or agent → the console records the last check-in, and the gap is timestamped precisely.
- Log pipeline "broken" → forwarder logs on the source host, and the receiving side's ingest metrics.

Treat all of it as SKILL.md's decode rule says: anything that clears or disables telemetry is confirmed hostile until proven otherwise, and the destruction timestamp is itself a high-confidence event in the timeline.

## When To Stop, And When To Hand Over

Stop when the questions that drive decisions are answered: how they got in, what they reached, what they took, whether they are still in, and whether it is notifiable. Further depth is a research project and you are paying for it in downtime.

Hand to a specialist firm when: the matter is heading to court or a regulator wants a report; the intrusion touches a domain controller, an identity provider, or a signing key; the evidence involves a device you do not own; the actor is still active and hands-on; or the insurance policy names a panel vendor — in which case using anybody else can void the claim (`~/Clawic/data/finances/subscriptions.md` holds the policy terms).

After the investigation, write it (`memory-template.md`): the timeline into the incident's section in `incidents/<year>.md` with the evidence column holding location and hash only; every log source you wished you had into the `Gap` column of `## Environment` — that column is the pre-written answer to "can we even tell?" next time; indicators worth blocking or hunting beyond this incident into `indicators.md`, defanged and with an expiry; the collection procedure that worked, and any per-platform export step that took an hour to figure out, into `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn. Any retention or logging change becomes a `## Findings` row with an owner and a due date.
