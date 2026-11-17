# Recovery — Backups That Restore, Failovers That Work, Drills That Prove It

Scope: everything you rely on when the normal path is gone. The rule that organizes it: a backup is a hypothesis until a timed restore has confirmed it.

**Before answering anything about backups, failover, or DR**, read `## Services` in `~/Clawic/data/devops/memory.md` (RTO/RPO per service, backup method, last restore test) and `## Due` for the drill cadence — state any overdue drill in one line, as a statement rather than a question.

**Contents:** [RTO And RPO First](#rto-and-rpo-first) · [What Actually Needs Backing Up](#what-actually-needs-backing-up) · [Backup Design](#backup-design) · [The Restore Drill](#the-restore-drill) · [Failover](#failover) · [Game Days](#game-days) · [The Disaster Nobody Plans For](#the-disaster-nobody-plans-for)

## RTO And RPO First

Two numbers per service, agreed with whoever owns the business consequence, before choosing any technology.

- **RTO** — how long the service may be down. Determines the recovery *mechanism*: restore from backup (hours), warm standby (minutes), active-active (seconds).
- **RPO** — how much data may be lost. Determines *backup frequency*: `RPO ≈ backup interval + replication lag + detection delay`. Nightly snapshots mean an RPO of up to 24 hours, whatever the intention was.

| RTO / RPO | Mechanism | Rough cost |
|---|---|---|
| Hours / hours | Snapshots plus a documented restore | Storage only |
| < 1 hour / minutes | Point-in-time recovery, continuous log shipping | Storage plus log retention |
| Minutes / seconds | Warm standby, replicated, promotable | Roughly a second environment |
| Seconds / near zero | Active-active across zones or regions | 2× infrastructure plus the complexity of consistency |

Write both numbers down per service. Undeclared, they default to whatever the last person configured, and the difference is discovered at the worst possible time.

## What Actually Needs Backing Up

Databases are the obvious half. The list that makes a restore *complete*:

| Item | Why it is missed |
|---|---|
| Database data | Never missed — but see PITR vs snapshot below |
| Object storage / uploads | Assumed durable; durability is not versioning, and a delete is replicated instantly |
| Encryption keys and their grants | The restore succeeds and the data is unreadable |
| Secrets and their bindings | The service starts and cannot authenticate to anything |
| Database configuration (parameter groups, extensions, roles) | The restored instance behaves subtly differently under load |
| DNS records and certificates | Traffic cannot reach the recovered system (`~/Clawic/data/domains/domains.md`) |
| Infrastructure definitions | Reproducing the environment by hand is where hours go (`iac-workflow.md`) |
| CI/CD configuration and runners | You can recover the service but not deploy the fix |
| Queue and stream contents in flight | Accepted losses, but only if someone decided that |

Version control is not a backup of the platform: the repository host, the registry, and the secret store each need their own answer.

## Backup Design

- **3-2-1 as the baseline**: three copies, two media or storage classes, one off-site — and for ransomware, one immutable or otherwise not deletable by the credentials your systems hold.
- The backup credential must not be able to delete backups. An attacker (or a script) with production access deleting the backups is the single most common way "we had backups" becomes "we had backups".
- **Snapshots and replicas are not backups.** A replica faithfully replicates a `DELETE`; a snapshot chained to the source instance dies with it. Cross-account or cross-project copies survive both accidents and compromise.
- Retention is a decision with a schedule: daily for a fortnight, weekly for a quarter, monthly for a year is a common shape — set it against `compliance_regime` and the cost, and enforce it with a lifecycle rule instead of a human.
- Point-in-time recovery beats nightly snapshots for anything transactional, because the recovery target is usually "just before that migration ran at 14:07", not "midnight".
- Monitor backup *success*, and alert on the absence of a successful backup — a job that silently stopped running six weeks ago is the classic finding of a first restore drill.

## The Restore Drill

The only evidence that any of this works. Quarterly by default, as a row in `## Due`, with a measured duration.

1. **Restore into a scratch environment**, never over the live one. Restoring over production during a drill is a self-inflicted incident.
2. **Time it end to end**: request to usable service, including the parts nobody counts — locating the right backup, permissions, key access, DNS, and the smoke test.
3. **Verify data, not just startup**: row counts, a checksum on a known table, the newest record's timestamp (that timestamp is your real RPO).
4. **Record what was missing** in that drill's `artifacts/<kebab-name>.md`, with its `## Boxes` line. The first drill always finds something: a key grant, a parameter group, an extension, an environment variable, a certificate. That list is the deliverable.
5. **Compare measured RTO against declared RTO.** If measured exceeds declared, either the mechanism changes or the promise changes — both are legitimate, silence is not.
6. Rotate who runs it. A drill only the person who built it can perform has not tested the runbook.

## Failover

- Automatic failover trades a class of outage for a class of split-brain. Managed databases with quorum-based promotion make this safe; hand-rolled promotion scripts frequently do not.
- Know what does *not* fail over automatically: connection strings cached in application pools, DNS with a long TTL (`migrations.md`), certificates bound to a hostname, and cron jobs pinned to one node.
- Failback is the forgotten half. Plan the return trip, including how the data written during the failover reconciles.
- Multi-region is a big step: cross-region latency changes application behavior, and the consistency model becomes an application concern, not an infrastructure setting. Do not adopt it because it sounds resilient; adopt it because an RTO/RPO pair requires it.
- Test failover in the same drill cadence. A standby that has never been promoted is a standby of unknown state.

## Game Days

Rehearsed failure in a controlled window — the cheapest way to find the gap between the diagram and reality.

- Start in a non-production environment with an announced window, a hypothesis ("if we kill the primary, traffic recovers in under 2 minutes"), and an abort condition.
- Good first experiments: kill an instance; fill a disk; add latency to a dependency; expire a credential; block egress to a third party; take the metrics stack away and see if anyone can still diagnose anything.
- Measure detection time separately from recovery time. Most game days find that detection was the slow part.
- The output is action items with owners and dates, tracked in `## Due` like postmortem items (`incidents.md`).
- Production chaos experiments come later, with a small blast radius, an automatic stop, and someone watching. They are the last step of a mature practice, not the first purchase.

## The Disaster Nobody Plans For

- **Loss of the account, not the machine.** Provider account suspension, a billing failure, or a compromised administrator locks you out of everything at once, including the backups stored in the same account. One off-provider copy of the critical data plus the infrastructure code answers this.
- **The person who knew.** Single-owner knowledge is a recovery risk: if only one engineer can perform a restore, the recovery plan has an availability of one human. Runbooks and rotation are the mitigation.
- **The recovery path that depends on the failed system.** Runbooks on the wiki hosted on the cluster; the deploy pipeline that needs the registry that is down; the paging tool authenticating through the identity provider that is the outage. Enumerate these dependencies once into the DR plan at `artifacts/dr-plan.md`; each needs an offline or independent path (`incidents.md`).

**Write in the same turn**: RTO, RPO, backup method, and the date and measured duration of the last restore per service go in `## Services` of `~/Clawic/data/devops/memory.md` — with `never` written explicitly where no restore has been tested, because that word is what makes the gap visible. Drill cadences and their last run go in `## Due`; the DR plan, the restore runbook, and each drill's findings become `artifacts/<kebab-name>.md` with their `## Boxes` line; a drill that turned into a real incident gets its row in `incidents/<year>.md` (`memory-template.md`).
