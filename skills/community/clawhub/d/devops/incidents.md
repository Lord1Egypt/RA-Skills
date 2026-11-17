# Incidents — On-Call, Response, And The Learning Loop

Scope: the human system around failure. `oncall_model` in `config.yaml` decides how much of this applies — a solo operator needs severities and postmortems, not a follow-the-sun rotation.

**At the start of anything incident-shaped**, read `incidents/<year>.md` if `## Boxes` points there (has this happened before, and what fixed it), `## Services` in `~/Clawic/data/devops/memory.md` for the owner and the runbook pointer, and any `artifacts/runbook-*.md` the index names for this symptom. **Check `## Due`** for overdue postmortem action items — an unfinished action is often the cause in front of you.

**Contents:** [Severity](#severity) · [Rotation Design](#rotation-design) · [The First Ten Minutes](#the-first-ten-minutes) · [Roles](#roles) · [Communication](#communication) · [Runbooks](#runbooks) · [Postmortems](#postmortems) · [Action Items](#action-items)

## Severity

Define severities by impact, never by which component broke. Three levels are enough for most teams; five is a taxonomy nobody remembers at 3am.

| Level | Impact | Response | Comms |
|---|---|---|---|
| Sev1 | Core journey broken or data at risk, for most users | Page immediately, all hands allowed, rollback authority without approval | Status page and stakeholder update on a fixed cadence |
| Sev2 | Degraded or partial: one journey, one region, one large customer | Page during hours the rotation covers; escalate if unresolved within a stated time | Internal channel plus affected-customer notice |
| Sev3 | Contained: workaround exists, no budget burn of consequence | Ticket, next business day | Ticket only |

- Anyone can declare; nobody needs permission to raise the level. Over-declaring is cheap, under-declaring costs the first thirty minutes.
- Declaring is not the same as escalating. Say what you need — a decision, a specialist, a customer comms owner — rather than adding people and hoping.
- Data loss and security exposure are Sev1 regardless of user count, and security exposure adds a preservation duty: capture logs and state before restarting anything.

## Rotation Design

- A 24×7 single-site rotation needs roughly eight engineers to keep shift frequency humane; splitting across two sites lets each site run with about six. Below that, do not pretend to run 24×7 — run business-hours with a documented degradation, which is honest and sustainable.
- Cap page load at about two incidents per 12-hour shift. Above that, the rotation is doing operations work that should be fixed or automated (`platform.md`), and the fix belongs in this quarter's plan.
- Compensate on-call explicitly (time off or pay). Unpaid on-call is a retention problem disguised as a schedule.
- Primary and secondary, with automatic escalation on no-ack — a common shape is escalate after 5 minutes unacknowledged. A rotation with no escalation path fails the first time someone's phone is silent.
- Handover is a contract: what is broken now, what is fragile, what is deferred, what is deployed and still baking, what is overdue in `## Due`. Handover by silence is how a slow burn survives three shifts.
- Onboarding to the rotation: shadow first, then paired shifts, then solo. First page alone with no rehearsal is how good engineers learn to hate on-call.

## The First Ten Minutes

Order matters; diagnosis is not step one.

1. **Acknowledge and declare.** Severity, channel, and who is coordinating — even if that is you alone.
2. **Stabilize.** Roll back, flip the flag, shift traffic, scale out (`deploys.md`). Restoring service first is not giving up on the root cause; it is buying the time to find it calmly.
3. **What changed?** Deploys, config, flags, infrastructure applies, third-party status, certificate expiry, and scheduled jobs — in that order. The change immediately preceding the symptom is the suspect until eliminated.
4. **Establish the blast radius.** Which users, which journeys, which regions, and is data affected. This determines comms and severity, and it is the question stakeholders ask first.
5. **Preserve evidence** before restarting: logs, a copy of the failing state, the metrics window. A restart that fixes it and destroys the evidence guarantees a recurrence.
6. **Write the timeline as you go**, in the incident channel with timestamps. Reconstructing it afterwards from memory produces a postmortem that is wrong in the details that matter.

## Roles

Even a two-person incident benefits from naming these; one person can hold two, never all three.

| Role | Owns | Explicitly does not |
|---|---|---|
| Incident commander | Decisions, severity, who does what, when to roll back | Debug hands-on — a commander in a terminal stops commanding |
| Operations lead | The hands: commands, queries, changes, one at a time and announced | Communicate externally |
| Communications | Status page, stakeholders, customer-facing updates on cadence | Make technical decisions |

One change at a time, announced before it is made. Parallel undocumented changes are why nobody can say afterwards what fixed it — and "what fixed it" is the entire value of the incident.

## Communication

- Fixed cadence beats accuracy: an update every 30 minutes for Sev1 even when the update is "still investigating, next update at HH:MM". Silence is read as absence.
- Say impact in user terms ("checkout is failing for about 30% of customers"), never in component terms ("the queue consumer is backing up").
- Never promise a resolution time you do not have. Promise the next update time instead — that one you control.
- Publish the postmortem to the same audience that received the incident updates, at the depth that audience needs.

## Runbooks

- A runbook exists for every alert that pages and for every failure that has happened twice. Under `artifacts/runbook-<symptom>.md`, indexed in `## Boxes` with the symptom as its read condition, so a responder finds it by what they see rather than by what it is called.
- Structure: symptom → verify it is really this → immediate mitigation → diagnosis steps → escalation criteria → rollback command with the recorded artifact identity.
- Written for a tired stranger: exact commands, exact expected output, no "obviously". Every secret in it is a pointer (`secrets.md`).
- **Store it where it survives the outage.** A runbook only readable on the infrastructure that is down is not a runbook.
- Update it during or immediately after the incident that used it. The moment you discover the step is wrong is the only moment you will remember to fix it.

## Postmortems

Blameless, written within a few days while memory is fresh, for every Sev1 and every recurrence. Sections:

| Section | Content |
|---|---|
| Impact | Duration, users affected, budget consumed, money or data if quantifiable |
| Timeline | Detection, escalation, key decisions, mitigation, resolution — with timestamps and evidence |
| Detection | How you found out. "A customer told us" is itself a finding |
| Contributing factors | Plural, always: the trigger, the reason it was possible, the reason it took that long to notice, and the reason it took that long to fix |
| What went well | Genuinely — the parts that worked are the parts to protect during the next reorganization |
| Action items | Owned, dated, tracked (below) |

- **Blameless means the system is the subject.** "Engineer ran the wrong command" is not a finding; "the command that drops the table is one character from the one that describes it, with no confirmation" is.
- Counterfactuals are not findings. "If we had noticed sooner" describes a wish; "the alert evaluates a 15-minute window, so detection could not have been faster than 15 minutes" describes a system.
- Time-to-detect, time-to-mitigate, and time-to-resolve are three separate numbers. Recording them separately is what tells you whether to invest in alerting, in runbooks, or in architecture.
- Small incidents deserve short postmortems. A four-page template for a 10-minute blip guarantees nobody writes them at all.

## Action Items

The step that decides whether the incident taught anything.

- Each item: one owner (a person), one date, and a classification — prevent, detect faster, mitigate faster. A list that is all "prevent" means detection and recovery never improve.
- Track them in `## Due` until closed. Review on a cadence, and report the completion rate; below about half, the postmortem process has become theater.
- A repeat incident whose action items from last time were never completed is not a new incident — say so explicitly in the write-up, because that fact is the finding.
- One or two items that actually ship beat twelve that are aspirational. Prefer the item that removes the class of failure over the one that removes this instance.

**Write in the same turn**: every incident gets a row in `~/Clawic/data/devops/incidents/<year>.md` (date, severity, service, detection method, the three durations, impact, cause class, postmortem pointer). The postmortem and any runbook go in `artifacts/<kebab-name>.md` with their `## Boxes` line and the symptom as the read condition. Action items with owners and dates go in `## Due`; people who own services or carry the pager go in the shared `~/Clawic/data/contacts/contacts.md` and are referenced here by name only; a recurring cause goes in `## Pain Points` of `memory.md` (`memory-template.md`).
