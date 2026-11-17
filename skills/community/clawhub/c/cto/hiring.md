# Team Building and Hiring

## Hiring Heuristics

- **Slope over intercept — but only where mentors exist.** Growth rate beats current skill for juniors, and a junior with no senior nearby stalls. Under ~10 engineers hire senior-heavy; add juniors once each has a senior with real mentoring time.
- **Weight work samples and structured interviews.** Meta-analytic evidence (Schmidt & Hunter) puts work samples and structured interviews at the top of predictors; unstructured "chat" interviews are barely better than chance. Same questions to every candidate, written scorecards, calibrated rubric.
- **Scorecards before debrief.** Collect written scores before anyone speaks — the first voice in an open debrief anchors everyone else, and it's usually the most senior person, not the most accurate.
- **References for collaboration, interviews for skill.** Skill is visible in a loop; how someone behaves across 18 months isn't. Ask references: "would you hire them again? for what role?" — the hesitation is the data.
- **Start senior searches ~2 quarters early.** Search 6-12 weeks + notice period 4-12 weeks + ramp ~1 quarter. A staff-level "we need them now" is already 6 months late.

## Engineering Ladder

| Level | Scope | Expectation |
|-------|-------|-------------|
| Junior | Tasks | Ships with guidance |
| Mid | Features | Ships independently |
| Senior | Projects | Leads technical work, unblocks others |
| Staff | Domain | Shapes technical direction across teams |
| Principal | Organization | Influences company strategy |

Promotion test: the person is **already operating** at the next level — promotion confirms, never anticipates. Anticipatory promotions create title inflation you can't walk back.

## Interview Loop

1. Recruiter screen — logistics, compensation range stated early (mismatches discovered at offer waste the whole loop)
2. Technical screen — 1 hour, real problem from your domain, not puzzles
3. Panel — coding + system design + behavioral, 4-5 hours total; each interviewer owns one signal
4. References — before offer for senior roles
5. Debrief — written scores first, then discussion

**Red flags:** can't explain a failure or what changed after it · blames others for every project problem · zero questions about the business · dismissive of approaches they didn't choose · "I" for every success, "we" for every failure.

## Org Scaling

| Team size | Structure | The move |
|-----------|-----------|----------|
| 1-5 | Flat, all report to CTO | Hire the senior who raises everyone's bar |
| 5-15 | Tech-lead model | First EM at ~8-10 engineers — past that, 1:1s alone eat a workweek |
| 15-30 | Squads of 5-8, clear ownership | Second EM + first staff engineer |
| 30-50 | Directors | Director of Engineering |
| 50+ | VP Engineering | Split the job: CTO (technology, outward) vs VPE (org, delivery, inward) — one person doing both past ~50 does both badly |

- Manager span: 5-8 directs. Below 4, the layer isn't paying for itself; above 8, 1:1s and growth conversations decay first.
- Squads: 5-8 engineers, ownership of a service or feature area, embedded PM/design when possible, cross-team dependencies minimized by design.
- **Conway's law is a tool, not a warning**: teams ship their communication structure, so draw the org chart you want your architecture to become (the inverse Conway maneuver) — reorg first, extract services second (→ `architecture.md`).

## Retention

- Re-level compensation against market annually, unprompted. The raise that retains costs less than the search that replaces: contingency recruiters alone run 20-25% of first-year salary, before the empty-seat months and ramp.
- Track **regretted** attrition separately from total — total attrition including managed-out low performers is noise; one regretted staff-level loss is a fire alarm.
- The exit-interview answer is rarely the real reason. Watch upstream signals: stopped volunteering in design reviews, calendar suddenly private, "how's the roadmap looking" questions.
- Sustainable on-call (→ `operations.md`), visible career growth, and voice in decisions retain more than perks — perks are matched by any competitor in a week; the other three aren't.
