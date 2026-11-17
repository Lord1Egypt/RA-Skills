# The Personal CRM — Solo, Freelance, and Non-Sales Pipelines

The version that survives a busy month. One person, no team, no admin, and a total time budget of twenty minutes a week. Everything in this file is the same machine as the rest of the skill with most of it switched off.

**Contents:** [The Twenty-Minute System](#the-twenty-minute-system) · [What To Switch Off](#what-to-switch-off) · [Freelance And Consulting](#freelance-and-consulting) · [Job Search](#job-search) · [Networking Without A Pipeline](#networking-without-a-pipeline) · [Creators, Communities, Collaborators](#creators-communities-collaborators) · [Advisors, Mentors, And Board Relationships](#advisors-mentors-and-board-relationships) · [Long-Dormancy Businesses](#long-dormancy-businesses) · [Failure Modes Specific To Solo](#failure-modes-specific-to-solo)

**Before building any of these**, read `## System` and `## Boxes` in `~/Clawic/data/crm/memory.md`. The most common solo mistake is building a second system next to one that already half-exists.

## The Twenty-Minute System

Three files, four fields, one ritual.

- **People** → the shared box `~/Clawic/data/contacts/contacts.md`: name, role, channel, one line of context. Their tier and how you met them go in `## People` in `memory.md`, keyed by the same email (`memory-template.md`).
- **Interactions** → `interactions/<year>.md`: date, who, one line of substance, next step.
- **Open things** → `## Pipeline` in `memory.md`: whatever is in play, with a next step and a date.

The ritual, once a week, twenty minutes: overdue next steps first, then anyone past `stale_days` you actually want to keep, then three follow-ups booked. That is the whole system, and it outperforms every abandoned SaaS CRM on the only metric that matters — being used in month four (`adoption.md`).

## What To Switch Off

| Feature | Why it is wrong at this scale |
|---|---|
| Lead scoring | Scores a customer model you do not have; you can hold your whole list in your head (`schema.md`) |
| Multiple pipelines | Halves an already tiny sample; one pipeline, a `type` tag if needed (`pipeline.md`) |
| Weighted forecasting | Under ~20 closed deals it is arithmetic on noise — call the deals (`metrics.md`) |
| Automated sequences | The relationships here are ones where a template is a downgrade (`followup.md`) |
| Custom fields beyond the minimum record | Every one is a tax on the four fields that matter (`adoption.md`) |
| A web UI or mobile app for your own data | The most common way a personal CRM dies before it is useful (`files-and-sqlite.md`) |
| Six stages | Three is usually right: talking / proposed / decided |

Keep, always: the identity key, the interaction log, the next step with a date, the suppression list once anyone has asked you to stop (`privacy.md`).

## Freelance And Consulting

The pipeline has four sources and they are unequal: past clients, referrals, inbound, and outbound. The first two convert several times better than the last two in almost every freelance practice — and they are the two that go quiet without any visible signal (`metrics.md`).

- **Past clients are the pipeline.** A quarterly reconnect pass over everyone you have invoiced is the single highest-return recurring row in `## Due`. Not a newsletter: one line, personal, referencing the work.
- **Track capacity as a stage input.** A deal you cannot start for two months has a close date two months out; quoting as if you were free is how a freelance pipeline produces feast and famine.
- **Proposals are deals, and proposals expire.** Put the expiry in the next-step date; an unanswered proposal after two weeks goes to the breakup message (`pipeline.md`).
- **Referrers get tier A** even without a live deal, and the `Referred by` cell in `## People` gets filled every time (`schema.md`). Five people generate most freelance work; without the field you cannot name them.
- **The retainer renewal is a deal** with a known value and a fixed date, opened one cycle before the end (`pipeline.md`).
- Delivery of the work — scope, milestones, documents — is a project in `~/Clawic/data/projects/<project>.md`, not a CRM record (`clients` skill). The closed-deal row keeps only the project name (`memory-template.md`).

## Job Search

An application pipeline behaves exactly like a sales pipeline in which you are the product, and the two things that make it work are the same: a next step on everything, and a record of every conversation.

| Stage | Exits when | Next step, typically |
|---|---|---|
| Researching | The role and a person inside are identified | Find the warm path before applying cold |
| Warm path | Someone agreed to refer or introduce | Send them the one-paragraph version to forward |
| Applied | Application submitted, date recorded | Follow up in 7-10 days if silent |
| Screen | Recruiter call happened | Ask their process and timeline — that is your close date |
| Interviews | Each round completed | Confirm the next round's date before leaving the call |
| Offer / rejection | Written outcome | Rejections get a thank-you and a re-open date; people move companies |

- **A referral is worth more than any number of applications.** Model the introducer as the primary contact of the deal, not the recruiter.
- **Log every conversation the same day** — the interviewer's name, what they cared about, what you promised. Round three should reference round one, and nothing else makes that possible.
- **Every rejection carries a re-open date** (six months) and a warm contact. This is the highest-value list a job seeker builds and the one that gets deleted in frustration.
- Recruiters are contacts with a `type` tag, not companies; they move firms and they take their roles with them.
- Track the search's own numbers: applications → screens → interviews → offers. If screens are rare, the problem is the top of the funnel; if interviews rarely convert, it is not (`metrics.md`).

## Networking Without A Pipeline

For relationships that will never have a deal — peers, former colleagues, people whose work you follow.

- **No stages, no deals.** Tiers and recency only: the tier in `## People`, the recency from `interactions/<year>.md` (`followup.md`). With no pipeline, `## People` is the whole database and it is the section that will cross the split threshold first.
- Cap tier A at about twenty people. Beyond that the cadence is theatre.
- **The context line is the whole value**: what they are working on, what they care about, what you last discussed. Two years later, that line is the difference between a warm message and an awkward one.
- Trigger events beat cadence: a job change, a launch, a talk. A yearly "how are you" is worth less than one message the week their thing shipped (`followup.md`).
- Birthdays, family details, gift ideas and the personal side of staying in touch: `people`.

## Creators, Communities, Collaborators

- **Podcast and newsletter guests** are a pipeline with three stages — asked, booked, published — and a stewardship step afterwards that most people skip. A guest who was well handled introduces the next two.
- **Sponsors and partners** are deals with renewal dates: track the cycle, not the conversation, and open the renewal one cycle early (`pipeline.md`).
- **Collaborators and contributors** are tier B with trigger-based contact; the trigger is usually their own launch.
- **Superfans and repeat buyers** deserve a tag and nothing more elaborate — an audience is not a CRM, and importing a mailing list into one destroys both (`import.md`).
- Consent and suppression apply exactly as they do in sales; an audience relationship is not a lawful basis for a sales email (`privacy.md`).

## Advisors, Mentors, And Board Relationships

- Cadence over pipeline: monthly or quarterly, in `## Due`, with the date set by you because they will not chase you.
- **Bring the same three things every time**: what changed, what you decided, what you need. The record of the previous three answers is what makes the relationship compound.
- Log what they advised *and what you did about it*. An advisor who sees their advice acted on stays engaged; one who repeats themselves stops.
- Asks are specific and rationed. Two per quarter, named in advance in the next-step field.

## Long-Dormancy Businesses

Real estate, insurance, weddings, home renovation, tax and legal work: the customer buys once every several years, so recency rules that assume a quarterly rhythm are wrong.

- **The cadence is annual, and the trigger is an anniversary** — purchase date, policy renewal, move-in date. All of them are `## Due` rows set on the day the deal closes.
- **Referral is the business.** A past customer who is contacted twice a year refers; one contacted never does not remember your name in five years.
- **The pipeline is small and slow**: stage dwell times of months are normal, so `stall_days` gets overridden in `config.yaml` rather than fought with.
- Track the *life event* that will trigger the next purchase, not the purchase itself. That field is what makes a dormant list into a pipeline.

## Failure Modes Specific To Solo

| Failure | Fix |
|---|---|
| Building the system instead of using it | Two weeks of the minimum record before any tooling decision (`tools.md`) |
| Logging only when things are going well | The interaction log's value is entirely in the quiet periods; one line, always |
| Every contact in tier A | Twenty is the ceiling; the rest is a wish list (`followup.md`) |
| A pipeline of things you hope for | A deal needs a next step *they* agreed to (`pipeline.md`) |
| Abandoning after a busy month | Do not catch up. Bring the twenty live relationships current and move on (`adoption.md`) |
| Keeping everyone forever | An annual purge of people you will never contact again makes the rest usable (`privacy.md`) |

**Write in the same turn as the conversation**: the person into the shared `~/Clawic/data/contacts/contacts.md`, their tier and source into `## People`, the line into `interactions/<year>.md` with its next step, anything in play into `## Pipeline`, and every anniversary, reconnect pass or recurring check-in into `## Due` (`memory-template.md`). For a solo operator this is the entire system — if it is not written, it did not happen, because there is nobody else who remembers.
