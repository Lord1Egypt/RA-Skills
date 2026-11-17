# Platform — Golden Paths, Toil, And Measuring The Delivery System

Scope: the organizational side — what to standardize, what to leave alone, how to measure whether delivery is improving, and when a platform team is justified.

**Before proposing an organizational change**, read `## Services` and `## Pipeline Health` in `~/Clawic/data/devops/memory.md` (how many services, how many distinct pipelines, measured durations) and `releases/<year>.md` plus `incidents/<year>.md` — the four delivery metrics come from those two files, not from a survey.

**Contents:** [Measure Before Changing](#measure-before-changing) · [The Golden Path](#the-golden-path) · [What To Standardize](#what-to-standardize) · [Self-Service Boundary](#self-service-boundary) · [Toil](#toil) · [When A Platform Team Is Justified](#when-a-platform-team-is-justified) · [Service Ownership](#service-ownership) · [Rolling Out A Practice](#rolling-out-a-practice)

## Measure Before Changing

The four metrics (SKILL.md, DORA Scoreboard) are computable from records you already keep:

| Metric | Computation | Common first finding |
|---|---|---|
| Deploy frequency | Rows in `releases/<year>.md` per service per week | One service deploys daily, the rest quarterly — the average hides everything |
| Change lead time | Median of (deploy time − merge time) | Most of it is waiting for a human gate, not pipeline runtime |
| Change failure rate | Releases followed by a rollback or hotfix within 24h ÷ total releases | Concentrated in one service or one type of change |
| Time to restore | Median of (resolved − started) from `incidents/<year>.md` | Detection dominates repair |

- Read them together. Deploy frequency alone rewards shipping breakage; change failure rate alone rewards shipping nothing.
- Per service, not per organization: the aggregate hides the one service that needs the work.
- Two weeks of baseline before any intervention. Without it, every change "worked".
- Never make them individual performance measures. The instant they are, the numbers get gamed and you lose the instrument.

## The Golden Path

One well-supported way to build, test, deploy, observe, and page for a new service — documented, templated, and actually used by the team that maintains it.

- The test is a stopwatch: **from `git init` to a running, monitored, deployable service in production**, how long? Teams with a real golden path measure this in hours; teams without measure it in weeks of copying an existing repo and inheriting its mistakes.
- A template is a starting point, not a cage. Every generated service must be editable by its owners without asking permission, or teams fork the template and the path dies.
- Templates rot. Whoever owns the path owns keeping it current with the practices in this skill, and a way to tell existing services what changed — a template with no update mechanism guarantees a fleet of divergent snowflakes.
- Adoption is voluntary but the path is subsidized: teams on the path get the pipeline, the dashboards, the alerts, and the runbook skeleton for free. Teams off it own all of it. Mandates produce compliance theater; a genuinely cheaper path produces adoption.

## What To Standardize

The defensible line: **standardize what breaks production, leave the rest.**

| Standardize | Leave to teams |
|---|---|
| Deploy mechanism and rollback | Language, framework, and libraries |
| Secret handling and pipeline permissions | Test style and coverage targets |
| Observability wiring: SLI, dashboard, alert routing | Dashboard layout and internal metric names |
| Incident process, severities, on-call tooling | Code review conventions |
| Artifact identity and promotion | Repository structure |
| Backup, restore, and drill cadence | Local development setup |

Every standard has a cost paid by every team forever. Standards that exist because "consistency is good", with no failure they prevent, are the ones engineers route around — and routing around one standard weakens the ones that matter.

## Self-Service Boundary

The platform's job is to make the safe thing the easy thing, without becoming a ticket queue.

- **Ticket queues become the bottleneck they were created to solve.** If provisioning a database requires a human, lead time includes that human's backlog.
- Self-service with guardrails: teams create what they need inside a policy envelope (allowed sizes, regions, tags, cost ceiling) enforced in code (`iac-workflow.md`), not in review.
- Escalate to a human only for what genuinely needs judgment: a new dependency on a regulated data store, a spend commitment, a change to the boundary itself.
- Measure requests that required a human. Each recurring one is either a missing self-service capability or a policy that should be automated.

## Toil

Toil is manual, repetitive, automatable work that scales with service count and produces no lasting value. It is not "work I dislike" — a hard debugging session is not toil.

- Cap it. The widely used SRE guidance is to keep toil under 50% of an operations-focused role's time; when it exceeds that, the surplus is a signal to stop taking on new services and automate instead.
- Count it crudely: interrupts per week per person, written into `## Pain Points` of `memory.md` when the number changes a decision. Precision is not the point, trend is.
- Automate in this order: (1) eliminate the need, (2) make it self-service, (3) script it, (4) document it. Documentation is the last resort, not the first response — a runbook for a task done weekly is a deferred automation with interest.
- Automation has its own cost: an automation nobody understands, that fails silently, is worse toil than the manual task. Automate what is stable and frequent; leave the rare and variable to a human with a runbook.

## When A Platform Team Is Justified

Signals, in order of reliability:

1. **Duplicated pipelines**: the same CI logic copied into more repositories than a person can update in a day.
2. **A rising share of engineering time on delivery plumbing** rather than product — measurable in the interrupt count above.
3. **Inconsistent incident readiness**: some services have alerts and runbooks, others have neither, and nobody can say which is which.
4. **Onboarding time for a new service measured in weeks.**

Headcount alone is not a signal. Below roughly a dozen engineers, one shared repository of conventions and one person who cares does more than a team.

Anti-patterns to name out loud: a platform team that becomes the ticket queue; a platform team with no users because it built what it found interesting; a platform team that owns production for services it did not write, which separates the people who cause incidents from the people woken by them.

## Service Ownership

- Every service has one owning team and one on-call rotation. Shared ownership means shared inattention; the service with no owner is the one still running an unpatched dependency.
- Record ownership where it is discoverable at 3am — in `## Services` with the owner's name, and the person in the shared `~/Clawic/data/contacts/contacts.md` (`memory-template.md`).
- A service with no owner has three honest outcomes: adopt it, decommission it, or freeze it with a written expiry date. Leaving it unowned is choosing the worst one.
- Decommissioning is a delivery task with its own checklist: traffic drained, dependents migrated, data exported or deleted per policy, DNS and certificates released, infrastructure destroyed, records updated. A half-decommissioned service is a security surface nobody watches.

## Rolling Out A Practice

Introducing anything from this skill — SLOs, canaries, postmortems, drills — follows the same shape:

1. **One service, one team, one quarter.** The pilot proves the practice in this organization's reality and produces the internal example that makes the case.
2. **Measure the metric it should move**, before and after. A practice that cannot name its metric is a preference.
3. **Write it down as an artifact** with the trade-offs and what was rejected — the decision will be re-litigated, and the write-up is what stops it being re-decided from scratch.
4. **Then expand**, with the pilot team as the reference rather than the platform team as the enforcer.
5. Retire practices that stopped paying. A ceremony nobody uses is a tax on every future change.

**Write in the same turn**: service ownership goes in `## Services` of `~/Clawic/data/devops/memory.md`, one pipeline per row in `## Pipeline Health` (the count is the number of rows, never a figure of its own), and the golden-path template with the date it was last refreshed in `## Delivery Setup`; a standardization or platform decision, with what it rejected, becomes `artifacts/<kebab-name>.md` with its `## Boxes` line; the metrics review cadence goes in `## Due` with its last run; people go in the shared `~/Clawic/data/contacts/contacts.md` and tracked initiatives in `~/Clawic/data/projects/<project>.md`, referenced here by name only (`memory-template.md`).
