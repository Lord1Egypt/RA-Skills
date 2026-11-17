# Picking a CRM, and Being Able to Leave It

The right CRM is the smallest thing that answers your three real questions. Every capability beyond that is paid for twice: once in subscription, once in the fields nobody fills.

Prices and limits move; the **structural differences below are stable**, the numbers are mid-2026 bands to verify before committing money.

**Contents:** [Start From The Three Questions](#start-from-the-three-questions) · [The Ladder](#the-ladder) · [Tool Notes](#tool-notes) · [The Exit Test](#the-exit-test) · [What Actually Costs Money](#what-actually-costs-money) · [Triggers To Move Up](#triggers-to-move-up) · [Reasons Not To Move](#reasons-not-to-move) · [Evaluating In A Week](#evaluating-in-a-week)

**Before recommending or changing a tool**, read `## System` in `~/Clawic/data/crm/memory.md` — what they use today, what they already tried, and why they left it. Recommending the tool someone abandoned last year is the fastest way to lose the argument.

## Start From The Three Questions

Ask what the CRM must answer, and take the first three answers literally:

- "Who do I know at X, and when did we last talk?" → contacts plus an interaction log. Nothing else required.
- "What is in play and what is the next step?" → deals with stages.
- "Which of my sources actually produce revenue?" → source field plus closed-deal history (`metrics.md`).
- "What is my team doing?" → shared writes, permissions, per-owner reporting. This is the question that costs real money.
- "What happens automatically when someone fills the form?" → automation and integrations (`automation.md`).

A tool that answers question one and two is a weekend. A tool that answers all five is a vendor relationship.

## The Ladder

| Rung | What it is | Good up to | Real limit |
|---|---|---|---|
| Markdown or JSON files | `db/` plus `interactions/<year>.md` | ~200 contacts, one person | No queries beyond grep; two devices conflict |
| Spreadsheet | One tab per entity | ~2,000 rows, one person | No relations; a formula error is silent and total |
| SQLite | One file, one table per entity | Tens of thousands, one writer | No UI, no concurrent writes (`files-and-sqlite.md`) |
| Notion / Airtable | Databases with relation fields | ~5,000 rows before views crawl | Automation is shallow; dedupe is manual |
| Lightweight CRM (Folk, Attio, Capsule, Pipedrive) | Real objects, pipelines, API | Small teams, tens of thousands of records | Per-seat cost; reporting depth varies sharply |
| Full platform (HubSpot, Salesforce, Zoho) | Everything, plus an admin surface | Whatever you can configure | Configuration becomes a job; contact-tier pricing |

Move one rung at a time, on a trigger (below), never two rungs on ambition.

## Tool Notes

What matters per tool is the data model and the exit, not the feature list.

| Tool | Model | Watch for |
|---|---|---|
| Plain files | Whatever you write | Zero lock-in, zero validation; discipline is the whole system |
| SQLite | Relational, real queries | Backup is a file copy; concurrent writes are the wall (`files-and-sqlite.md`) |
| Google Sheets | Flat rows | Everyone can break everything; version history is the only safety net |
| Notion | Databases with relations, one workspace | Fine as a CRM at small scale; large relation-heavy views get slow, and there is no dedupe |
| Airtable | Relational-ish, strong views and forms | Per-seat, with record and automation-run caps per plan; the caps arrive before the seats hurt |
| Folk | Contact-first, lightweight pipelines | Built for relationship management, not process-heavy sales |
| Attio | Flexible object model, strong data layer | You design the model, which means you can design it badly (`schema.md`) |
| Pipedrive | Deal-first, per-seat, activity-driven | Excellent at pipeline discipline; marketing and support live elsewhere |
| HubSpot | Free CRM tier, paid tiers around it | Paid marketing plans price on **marketing contacts**: the bill scales with list size, so importing a stale list has a monthly cost (`hygiene.md`) |
| Salesforce | Everything, configurable | Assumes an admin exists; total cost is seats plus that person's time |
| Streak / Gmail-native | Pipelines inside the inbox | Logging is frictionless, which is most of the battle for solo users; leaving means leaving your inbox |
| Project tools used as CRM (Monday, ClickUp, Trello) | Boards | A board has no organizations and no interaction history; it works until the first "when did we last talk" |

Per-seat CRMs cluster in roughly the 15-100 USD/seat/month band (mid-2026, verify). For one person, that is 180-1,200 USD/year against a SQLite file that costs nothing — a real decision, not an obvious one.

## The Exit Test

Run this **before** adopting, not when leaving. Four questions; two "no" answers disqualify a tool:

1. Can you export **contacts, organizations, deals and activity history**, with ids and foreign keys, on the plan you are buying?
2. Is the export self-service, or does it need support and a wait?
3. Does the API expose everything the UI shows, at a rate limit that allows a full extract in a day?
4. Are custom fields and stage histories included in the export, or only the current values?

A CRM you cannot leave stops having to earn you. That is not a paranoia argument: the moment a tool knows migration is impractical, its pricing behaves differently at renewal.

## What Actually Costs Money

- **Seats** — the sticker price, and the least of it.
- **Contact tiers** — plans that charge by stored or marketable contacts turn list hygiene into a line item. A stale list has a monthly cost.
- **The step function** — one needed feature sitting in the next tier up, at three times the price, for one report.
- **Configuration time** — the largest cost in every platform migration and the one nobody budgets. Measure it in weeks of the person doing it.
- **Data preparation** — cleaning before an import is unavoidable and always underestimated (`import.md`).
- **The exit** — extraction, mapping, parallel running, retraining. Assume one full sales cycle of reduced output.

Break-even to leave a free-but-painful setup: `annual_tool_cost + migration_weeks × weekly_cost` against hours saved per week × 50. If the tool saves 30 minutes a day for one person, most per-seat CRMs pay for themselves; if it saves five minutes, none of them do.

## Triggers To Move Up

Move only when one of these is true, and say which one out loud:

- A second person needs to **write** — the only trigger that reliably justifies a hosted tool.
- A query you need weekly is impossible in the current thing (not merely tedious).
- Two devices have produced conflicting copies more than once.
- The interaction log has become the bottleneck: you know things happened but cannot find when.
- An integration you depend on exists only in a tool (`automation.md`) — verify it does what you think before buying for it.
- Compliance requires audit trails or access control you cannot fake with a file (`privacy.md`).

Volume alone is not a trigger. SQLite does not care about 50,000 rows; your patience does.

## Reasons Not To Move

- Adoption is bad. A new UI does not fix a process with 40 required fields (`adoption.md`).
- The data is a mess. Migrating a mess produces a mess with a subscription — clean first (`hygiene.md`).
- Someone promised automation that will "save hours". Automation on rotten data does the wrong thing faster.
- A feature you would use quarterly. Do it by hand quarterly.
- The demo was good. Every demo is good; the demo runs on their data.

## Evaluating In A Week

1. Import 50 real records — never their sample data.
2. Recreate your actual pipeline with your stage names and your required fields (`schema.md`).
3. Log a week of real interactions in it, at the pace of a normal week.
4. Produce your three questions as answers: last-talked list, open pipeline with next steps, revenue by source.
5. **Export everything and open the file.** This is the step people skip and the only one that is irreversible if you get it wrong.
6. Delete the trial data and decide. If step 4 needed support or a workaround, the answer is no.

**After the decision**, write to `## System` in `~/Clawic/data/crm/memory.md`: the tool, where the data physically lives, the export cadence, and one line on what was rejected and why — that line is what stops the same evaluation happening again next year. If a migration follows, the plan goes to `artifacts/migration-<from>-to-<to>.md` with its `## Boxes` line (`memory-template.md`), and the export cadence goes into `## Due`.
