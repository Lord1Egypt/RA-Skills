# Adoption — Why CRMs Die and How to Revive One

Every abandoned CRM was abandoned for a reason that the next tool will not fix. The cause is almost always the same shape: **the person entering the data is not the person who benefits from it.** Everything here closes that gap.

**Contents:** [The Friction Budget](#the-friction-budget) · [The Five Ways A CRM Dies](#the-five-ways-a-crm-dies) · [Reviving A Dead CRM](#reviving-a-dead-crm) · [Field Discipline As Adoption Work](#field-discipline-as-adoption-work) · [The Ritual](#the-ritual) · [Team Rollout](#team-rollout) · [Solo Adoption](#solo-adoption) · [Signals It Is Working](#signals-it-is-working)

**Before diagnosing adoption**, read `## Data Health` and `## System` in `~/Clawic/data/crm/memory.md`, plus the interaction counts per week in `interactions/<year>.md`. Adoption is measurable: it is the ratio of records with an interaction to records total, over time (`hygiene.md`).

## The Friction Budget

**A record update has to cost under a minute, or it will not happen on a bad day** — and bad days are when the important deals move.

Budget, per interaction logged: who, what happened in one line, next step and date. That is four inputs. Every field beyond it is spent from the same budget, and the budget is not negotiable, it is behavioural.

| Cost | Effect on logging rate |
|---|---|
| Under a minute, no context switch | Survives busy weeks |
| Two to three minutes, one context switch | Survives calm weeks, dies in busy ones — which biases the data toward slow periods |
| Over five minutes, or a required field they do not have | Batched to Friday, then abandoned; the substance is gone by then (`followup.md`) |

The cheapest capacity increase is not discipline, it is subtraction: **delete two fields and adoption rises more than any training session produces.**

## The Five Ways A CRM Dies

| Cause | Symptom | Fix |
|---|---|---|
| Too many required fields | Records created outside the CRM (a notebook, an inbox folder), then never migrated | Four required fields maximum (`schema.md`) |
| No output the updater sees | It is a reporting tool for someone else, so it is filled the way reporting tools are filled — badly, at quarter end | Give the updater the overdue list and the "who do I know at X" answer daily |
| Data nobody trusts | One wrong number in a meeting and everyone reverts to their own spreadsheet | Hygiene sweep, then a visible fix (`hygiene.md`) |
| Stages that do not match reality | Deals sit in "Proposal" because there is no stage for what is actually happening | Redesign stages from the last 20 closed deals (`pipeline.md`) |
| Migration fatigue | Third tool in two years; nobody believes this one will last either | Stay put and fix the process; announce that the tool is not changing this year (`tools.md`) |

Not on the list, because it is almost never the real cause: "the team is not disciplined". Discipline that has to be renewed weekly is a design defect.

## Reviving A Dead CRM

Never start by importing everything and asking people to catch up. Start with the twenty records that matter.

1. **Audit and count** (`hygiene.md`) — do not clean yet. The counts decide whether reviving is cheaper than restarting.
2. **Pick the twenty live relationships**: open deals, active clients, top referrers. Nothing else is in scope for two weeks.
3. **Bring only those to current**: correct email, tier, last interaction, next step. Two hours of work.
4. **Delete or archive the rest from view.** A revived CRM with 4,000 dead rows still looks dead — and looking dead is what kills it again.
5. **Cut the fields** to the minimum record before anyone is asked to type into it (`schema.md`).
6. **Run the ritual for three weeks** without adding any new capability, tool, integration or field.
7. **Then, and only then**, reintroduce the archive by selective import (`import.md`) and add one capability at a time.

The order matters: capability added before the ritual sticks is how the CRM died the first time.

## Field Discipline As Adoption Work

- **Measure fill rates monthly** and act on them: below ~70% at 30 days, a field is deleted or made required (SKILL.md Rule 6). Publishing that number turns "should we add a field" from an opinion into an arithmetic problem.
- **Every new field needs a named person who fills it** and the query it serves. No name, no field.
- **Deleting a field is a feature announcement.** Say it out loud: "we removed four fields, updating a deal is now three inputs". That is the moment people re-engage.
- Defaults do more than requirements: a stage that pre-fills the next-step date one week out gets a real date typed over it far more often than an empty field gets filled.

## The Ritual

A CRM survives on one recurring event that consumes its data. Without it, the data has no consumer and the writing stops.

- **Weekly pipeline review** on `review_day` (`pipeline.md`) — the default. Twenty minutes, stalled list first.
- **The daily overdue list** (`followup.md`) — the solo version; it takes two minutes and it is the only reason to open the CRM on a normal day.
- **Monthly numbers** (`metrics.md`) — the one that keeps stage and source fields honest, because they are what the numbers are computed from.

Rules for the ritual: same time, same order, output written back in the same turn (`memory-template.md`). A review whose conclusions live only in someone's head teaches everyone that the CRM is optional.

## Team Rollout

- **One owner of the schema.** Not a committee: a committee produces a field per member.
- **Nobody's private pipeline stays private.** Two systems means the CRM is a reporting duplicate and the reporting will be wrong — this is the single most common team failure.
- **Managers read the CRM instead of asking.** The first time a manager asks in a meeting for a number that is in the CRM, everyone learns that updating it was optional.
- **Never use the CRM as a surveillance tool.** Activity leaderboards produce accurate activity data and nothing else (`metrics.md`).
- **Train on the ritual, not the software.** Twenty minutes on the weekly review beats two hours of feature tour.
- New joiners get the field dictionary (`artifacts/field-dictionary.md`) on day one, and the stage exit criteria on day two.

## Solo Adoption

The failure mode is different: there is no manager to enforce, and the data has an audience of one, later.

- **Log inside the same window as the conversation.** A call ends, one line goes in. The 15 seconds is the entire system (`followup.md`).
- **Make the CRM the place you look first**, not a place you report to: the overdue list before the inbox, twice a week.
- **Twenty minutes on Friday** is the whole ritual: stalled deals, next steps, three follow-ups booked, one line into `## Data Health` if anything was cleaned.
- Accept partial: a CRM with contacts and interactions and no deals is still worth having. A CRM with an empty deal pipeline and full custom fields is not (`personal-crm.md`).

## Signals It Is Working

| Signal | Measure | Meaning |
|---|---|---|
| Interaction coverage rising | records with ≥1 interaction ÷ total | The CRM is being used, not just populated |
| Next-step coverage near 1.0 | open deals with a future dated next step ÷ open deals | The ritual is actually running (`metrics.md`) |
| Somebody asks the CRM a question instead of a person | Anecdotal, and the strongest signal there is | It has become the record of truth |
| Fill rates stable after a field deletion | Per required field | The remaining fields are the right ones |
| Records created on the day the thing happened | `created` date vs interaction date | Friction is inside budget |

**Write the outcome of any adoption change**: field deletions and required-field decisions to `## System` and `artifacts/field-dictionary.md`; the ritual's day into `## Due`; the revival's keep/archive boundary and its counts into `## Data Health` (`memory-template.md`). An adoption fix nobody recorded gets undone by the next person who wants one more field.
