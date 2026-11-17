# Investor and Donor Pipelines

Fundraising is the same machine as sales with three differences: the stages are named for someone else's internal process, the timeline is set by a calendar you do not control, and the relationship continues after the close — the close is the beginning of the reporting obligation, not the end of the work.

Everything is stored in the same boxes: deals in `## Pipeline`, people in the shared contacts box, meetings in `interactions/<year>.md`, cadences in `## Due` (`memory-template.md`).

**Contents:** [Raising From Investors](#raising-from-investors) · [Investor Stages](#investor-stages) · [Running The Raise In Parallel](#running-the-raise-in-parallel) · [Reading A Soft No](#reading-a-soft-no) · [Between Raises](#between-raises) · [Major-Gift Fundraising](#major-gift-fundraising) · [Moves Management Stages](#moves-management-stages) · [Portfolio And Cadence](#portfolio-and-cadence) · [Lapsed Donors](#lapsed-donors) · [Grants](#grants) · [Data Care In Both](#data-care-in-both)

**Before any fundraising session**, read `## Pipeline` for the live process, `closed-deals.md` for who passed and why (that list is next round's target list), and `## Due` for update cadences and grant deadlines.

## Raising From Investors

The record structure: the **firm** is the organization, the **partner** is the person and the deal's primary contact, the **introducer** is a contact linked by `referred_by` (`schema.md`). The deal's value is the check size you are asking that firm for — not the round total, which would make the pipeline sum meaningless.

Three fields that do not exist in a sales CRM and matter more than most that do:

- **Intro path**: who introduced you and how warm. It is the single strongest predictor of whether a first meeting happens at all.
- **Check size and ownership target**: what they need to own to be interested. A fund with a 200,000 EUR check and a 10% target is not a fit for your round shape, whatever the meeting felt like.
- **Decision process**: how many partners, which day the partnership meets, and whether your contact can sponsor a deal. Fundraising slips are almost always a partnership calendar, not a lack of interest.

## Investor Stages

Named for their process, exiting on their action (SKILL.md Rule 4):

| Stage | Exits when | Not an exit |
|---|---|---|
| Researched | You have a name, a thesis fit, and an intro path | Adding a fund to a spreadsheet |
| Intro requested | The introducer agreed to send it | You asked for the intro |
| Intro made | The email went out, both sides copied | The introducer said they would "get to it" |
| First meeting | The meeting happened | It was booked |
| Second meeting / deep dive | They asked for materials or data | They said "keep us posted" |
| Partner meeting | You presented to the partnership | An associate said it is scheduled |
| Diligence | References, data room access, customer calls | A list of questions by email |
| Term sheet | A document exists | Verbal terms discussed |
| Closed | Documents signed and money wired | A signed term sheet — deals die between term sheet and wire |

Passes are closed-lost with a reason code from a closed list: thesis fit, stage, traction, market size, team, timing, no lead. That list is what makes the next round's target list, and the "timing" and "traction" passes are the warmest leads you will have in twelve months.

## Running The Raise In Parallel

- **A raise is time-boxed** — pick the window and run it. An open-ended raise reads as an open-ended raise, and investors price momentum.
- **Batch, do not sequence.** Group targets into tiers and open a tier at a time, roughly 10-15 firms per batch: enough for parallel processes and few enough to prepare for properly. Sequential outreach means the process takes as long as the sum of everyone's calendars.
- **Practice tier first**, real targets second, top choices third — once the pitch has survived a few meetings. The reverse order burns the meetings that mattered.
- **Weekly review during the raise**, not the default `review_day` cadence: stalled means one week here, not `stall_days` (`pipeline.md`). Update `## Due` with the raise cadence and set it back afterwards.
- **Every meeting produces one line in `interactions/<year>.md`**: who was in the room, what they pushed on, what they asked for, what happens next. Objections repeat across firms, and the pattern in that column is your pitch's actual weakness.

## Reading A Soft No

Investors rarely say no clearly; the signals are behavioural, and reading them wrong costs weeks.

| Signal | What it means |
|---|---|
| Associate-only meetings, repeatedly | No partner sponsor. Ask directly who the sponsor would be |
| Reply latency growing meeting over meeting | Interest cooling; the pace of *their* replies is the honest metric |
| "Keep us posted on progress" with no next step | A pass phrased politely. Close it lost with reason `timing`, keep them on the update list |
| Diligence questions with no partner meeting scheduled | Information gathering about the market, not about you |
| They ask who else is in | Real interest, and a signal to accelerate the rest of the batch |
| Fast, specific no with a reason | The most valuable answer you get. Write the reason down verbatim |

The rule that keeps the pipeline honest: **if there is no next step with a date agreed by them, it is not an active conversation** — same as any other pipeline.

## Between Raises

- **The monthly investor update is the pipeline.** Send it to everyone who passed, everyone who is in, and everyone who asked to be kept posted. It converts "timing" passes into next round's term sheets, and it is a `## Due` row that must never slip.
- Track it as a cadence, not a task: who receives it, when the last one went, what was promised in it.
- **Asks belong in the update**: one specific request per issue (an intro, a hire, a customer). A monthly update with no ask trains people to skim it.
- Existing investors' reporting obligations, board materials and cap-table documents live outside the CRM; keep the *cadence* here and the documents where the company's records live.

## Major-Gift Fundraising

Nonprofit development runs on **moves management**: a planned sequence of contacts that moves a donor from awareness to gift, with each move recorded. It is a CRM discipline before it is a fundraising one, which is why it works in the same structure.

The record: the **donor** is a person (the household or the foundation is the organization), the **deal** is the ask — one ask, with its target amount, ask date and purpose. Giving history is an interaction history with amounts.

## Moves Management Stages

| Stage | Exits when | The move |
|---|---|---|
| Identification | Capacity and affinity evidence exists | Research, screening, a board member's recognition |
| Qualification | They agreed to a conversation | The visit that establishes real interest, not just capacity |
| Cultivation | They have engaged with the work — a visit, a volunteer role, a question about impact | Sequenced, personal contacts with no ask |
| Solicitation | The ask has been made, with a number and a purpose | The ask meeting, planned with a date in `## Due` |
| Stewardship | The gift is received and acknowledged | Reporting on what the gift did; this is where the next gift comes from |

Two rules that separate practitioners from amateurs: **the ask amount is set before the meeting**, from capacity plus inclination plus relationship depth — never invented in the room; and **cultivation with no planned ask date is not cultivation**, it is friendship on the organization's budget. Every donor in cultivation has a target ask date in `## Due`.

## Portfolio And Cadence

- A full-time major-gift officer's portfolio is commonly held at roughly **100-150 households** — the number exists because more than that makes the planned-move cadence impossible, which is the whole method. A part-time or volunteer fundraiser should scale it down proportionally, not aspire to the same list.
- Every donor in the portfolio has a **next move with a date**, exactly like a deal (SKILL.md Rule 3). A portfolio with no dated moves is a mailing list.
- **Acknowledge fast.** A gift acknowledged within a couple of days materially outperforms one acknowledged in three weeks, and the acknowledgment is the first move of the next cycle.
- **The second gift is the hard one.** Retention of first-time donors is the weakest point in most programs; a dated stewardship move within 90 days of a first gift is the highest-leverage row in `## Due`.
- Recurring/monthly donors are a different pipeline with a different rhythm: retention work, not solicitation work. Keep them out of the major-gift portfolio so the counts stay meaningful.

## Lapsed Donors

The two acronyms worth knowing, because they define the two easiest lists to build and the two most neglected:

- **LYBUNT** — gave *last year but unfortunately not this*. The highest-yield reactivation list in the database; they are still donors, they simply have not been asked this cycle.
- **SYBUNT** — gave *some year but unfortunately not this*. Colder, worth an annual campaign, not a personal move.

Build both from the interaction history at the start of every fiscal year, put the pass into `## Due`, and record the counts in `## Data Health`. A reactivation ask names the last gift and what it did — that specificity is the entire difference in response rate.

## Grants

- **The deadline is the close date and it does not move.** Grants are calendar-driven, which makes them the one pipeline where `## Due` matters more than the stage.
- Stages: eligible → LOI submitted → invited to apply → submitted → decision → reporting. Reporting is a stage, not an afterthought: missed reports disqualify the renewal.
- Track the **reporting obligations of won grants** in `## Due` the day the grant is awarded. This is the most commonly dropped commitment in small organizations.
- A declined grant carries a reason and a re-apply date; most funders have an annual cycle, so the loss has a dated next step.

## Data Care In Both

- **Giving history and wealth-screening data are sensitive**, and screening data is inferred rather than stated. Store what supports the relationship; do not store speculation about someone's finances you would not repeat to them (`privacy.md`).
- **Anonymity requests are suppression entries** with a scope, honored everywhere including donor walls and annual reports — the scope column exists for exactly this (`memory-template.md`).
- Investor and donor conversations both contain confidential third-party information. The note-writing test applies unchanged: would you send this line to the person it is about?
- After a raise or a campaign closes, write the teardown to `artifacts/win-loss-<name>.md` — pass reasons, what changed the outcome, who introduced whom — and index it. The next raise or campaign starts from that file, and it is the single most valuable document either process produces.

**Write in the same turn**: firms and funders as organizations, partners and donors in the shared contacts box, asks and rounds as deals in `## Pipeline`, every meeting in `interactions/<year>.md`, passes and gifts in `closed-deals.md` with their reason, and every update cadence, ask date, grant deadline and reporting obligation in `## Due` (`memory-template.md`).
