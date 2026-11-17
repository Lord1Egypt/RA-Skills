# On Call: Incidents and What Comes After

During an incident, the goal is not to understand — it is to stop the bleeding. Understanding is tomorrow's work, and it is worth more if the system is up while you do it. Incident command structure and comms roles are `incident-response`; this is the developer's route with the pager in hand.

**First, before diagnosing**, read `releases/<year>.md` for what shipped in the last hours and any `artifacts/runbook-*.md` the `## Boxes` index names for this symptom. Most incidents are a recent change, and the second most common is a repeat.

## The First Ten Minutes

1. **Confirm it is real and scope it**: who is affected, what percentage, since when. A dashboard alone is not confirmation — reproduce the user-visible failure once.
2. **Check what changed.** Deploys, flags, config, migrations, dependency updates, upstream provider status — in that order. The change that shipped closest before the start time is the first hypothesis.
3. **Mitigate.** Roll back, flip the flag, scale out, disable the feature, fail over, shed load. Mitigation is not a fix and does not need to be understood to be correct.
4. **Say something.** Even "investigating, checkout failing for some users, next update in 15 minutes" — silence costs more than an imperfect update, and it stops five people from asking you individually.
5. **Only now, diagnose** — on a copy, on logs, on a replica. Never by pushing experimental changes to production (`bugs.md`).

If mitigation is not obvious within about 15 minutes, escalate. Escalating early is cheap; escalating at hour two is a second incident.

## Triage Table

| Signal | Most likely | First move |
|---|---|---|
| Started exactly at a deploy time | The deploy | Roll back; confirm after |
| Started at a round clock time | Cron, token expiry, certificate, scheduled job overlap | Check what runs at that time |
| Gradual degradation over hours | Leak, queue backlog, disk, connection pool | Look at the rising resource, not the errors |
| Errors only on one instance | Bad node, partial deploy, local state | Remove it from the pool first, inspect after |
| Errors on writes, reads fine | Database, locks, replication, disk full | Check the primary's locks and disk |
| Everything slow, no errors | Saturation somewhere shared | Queue depth and pool utilization before CPU |
| Upstream 5xx | Dependency, or your retry storm making theirs worse | Check their status, then check your retry policy |
| Only new users affected | Onboarding path, defaults, a migration that skipped existing rows | The new-record path (`migrations.md`) |
| Recovered by itself | Load spike, transient dependency, or a retry that eventually worked | Do not close it — it will be back, and the record is the value |
| Anything else | Unknown | Bisect the surface: disable the newest subsystem, halve the traffic path |

## Mitigations Ranked by Time to Effect

Rollback (minutes, if the artifact exists) → flag off (seconds) → scale out (minutes, works only for saturation) → shed or rate-limit load (immediate, degrades deliberately) → disable the feature at the edge (immediate) → restart (seconds, buys time on a leak, hides evidence) → forward fix (never the first choice; it is a full pipeline plus an untested change under pressure).

Restarting destroys the state that explains the incident. Capture what you can first — heap dump, thread dump, the current log tail, the metric screenshot — because after the restart, the evidence is gone and the incident will return.

## While It Burns

- **One person decides.** Two people rolling back different things is a longer outage than either alone.
- **Announce every action before taking it**, in the channel: "reverting to v2.13.3 now". This is how the timeline gets written for free.
- **Timestamp everything.** Copy log lines and metric screenshots as you go; the dashboards you are reading get rolled up and re-scaled within days.
- **Do not fix unrelated things you notice.** Park them in `## Open Threads` of `memory.md`; they are tomorrow's tickets.
- **Hand over deliberately** if it runs long: what is known, what was tried, what is running now, what the current hypothesis is.

## Postmortem

Write it within a few days, while the detail is recoverable. What makes it worth writing:

- **Timeline with timestamps**: first impact, detection, mitigation, resolution. Detection minus first impact is the number worth attacking — an incident found by a customer means the monitoring is the finding.
- **Impact in user terms**: duration, how many, what they experienced. Not "the service degraded".
- **The chain, not the culprit.** "Deployed a bad query" stops one instance; "a query pattern change was invisible in review and no test asserts query count" stops the class. Blameless is not politeness — a blaming postmortem produces careful reporting, not careful systems.
- **What made it hard**: the missing dashboard, the runbook that was wrong, the alert nobody owned. Usually worth more than the root cause.
- **Action items with owners and dates**, ranked. Three that get done beat twelve that do not, and the top one is usually detection.

## Reducing the Next Page

- Every alert has an owner, a runbook, and a human action. An alert with no action is noise that trains people to ignore the page.
- Alert on symptoms users feel (error rate, latency, queue age), not on causes (CPU). Cause alerts fire when nothing is wrong and stay silent when something is.
- Threshold check after every incident: if the alert fired late or not at all, that is an action item (this is the most commonly skipped one).
- Anything paged twice gets either a fix or a runbook. Twice is the definition of recurring.
- A page that arrives with no context costs 10 minutes of orientation; put the dashboard link and the runbook link in the alert itself.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Diagnosing before mitigating | Every minute of understanding is a minute of outage | Mitigate, then diagnose |
| Pushing a fix straight to production | Untested change under pressure, often a second incident | Roll back to something known good |
| Restarting immediately | Buys minutes and destroys the evidence | Capture state first, then restart |
| Changing several things at once | Recovery is unattributable and the cause survives | One action, observe, next |
| No communication because there is nothing new | People escalate to fill the silence | Update on a clock, even to say "still investigating" |
| Closing an incident that recovered on its own | It returns, with no record and no head start | Log it with `Root cause: unknown` and a date |
| Postmortem naming a person | Produces defensive reporting, and the system stays fragile | Name the chain and the missing guardrail |
| Action items with no owner | Nothing happens; the same incident recurs | Owner and date, tracked, reviewed on `## Due` |

## Write It Down, Same Week

- **The incident** → a row in `~/Clawic/data/developer/incidents/<year>.md` the day it happens: date, symptom, duration, mitigation, root cause (`unknown` is a valid value with a date), and a pointer to the write-up (`memory-template.md`).
- **The write-up** → `artifacts/postmortem-<name>.md`, read whole when that symptom returns; add its `## Boxes` line in the same turn.
- **A repeat symptom** → `artifacts/runbook-<symptom>.md` with the ordered checks and the mitigation, so the next page is a lookup instead of a diagnosis.
- **Action items** → the tracker if there is one, plus a `## Due` row for the monthly check that they are actually closing.
- **A cross-repo cause** → `## Pain Points` in `memory.md`; a repo-specific one → `## Gotchas` in that repo's profile.
