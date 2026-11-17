# Research Methodology Atlas

Use this atlas before choosing a template. Methods define the thinking path; templates only carry the final shape.

Do not try to use every method. Pick a small method stack that changes the answer.

## Core Method Families

| Method | Use when | Core question | Typical evidence | Output blocks |
| --- | --- | --- | --- | --- |
| `evidence-triangulation` | facts may be stale, copied, disputed, or source-sensitive | What is true enough to rely on? | primary sources, public records, independent reporting | `evidence-ledger`, `source-map`, `conflict-table` |
| `claim-citation-audit` | the answer contains official, time-sensitive, decision-critical, or easily challenged claims | Can every load-bearing claim be traced to evidence? | evidence ledger entries with titles, URLs, dates, source type, reliability, and corroboration groups | `claim-citation-map` |
| `historical-lineage` | user asks how something developed | How did it become this? | dates, papers, releases, institutional records, histories | `deep-timeline`, `mechanism-shifts` |
| `paradigm-analysis` | concepts, theories, schools, technical paradigms, cultural discourse | Which frames compete? | papers, essays, debates, definitions, critiques | `schools-disputes`, `concept-current-snapshot` |
| `competitive-analysis` | user compares products, companies, alternatives, or categories | What competes with what? | product docs, pricing, reviews, market maps | `competitive-matrix`, `user-choice-logic` |
| `jtbd-user-choice` | adoption, switching, user preference, product-market fit | What job does the user hire this for? | reviews, interviews, issues, forums, usage examples | `jtbd-analysis`, `user-signal-summary` |
| `ecosystem-mapping` | platforms, markets, open-source, supply chains, standards | Who depends on whom? | partner pages, repositories, standards, distribution channels | `ecosystem-map`, `power-dependency-map` |
| `literature-review` | papers, technical lineage, scientific claims | What does the research record say? | papers, benchmarks, citations, methods sections | `literature-thread`, `benchmark-caveats` |
| `osint-due-diligence` | company, person, funding, team, public footprint | What can public information verify? | filings, websites, GitHub, hiring, patents, public records | `entity-dossier`, `risk-register` |
| `user-signal-analysis` | reputation, product friction, community reception | What do users repeatedly praise or complain about? | reviews, issues, Reddit, Zhihu, X, app stores | `user-signal-summary`, `channel-bias-note` |
| `causal-mechanism-analysis` | user asks why something rose, failed, shifted, or persisted | What mechanism explains the outcome? | timelines, decisions, constraints, counterexamples | `mechanism-shifts`, `causal-chain` |
| `red-team-dissent` | stakes are high or conclusion may be too smooth | What would make this wrong? | failed cases, criticism, contradictory evidence | `dissent-review`, `reversal-conditions` |
| `scenario-planning` | future uncertainty matters | What futures are plausible and what triggers each? | trend signals, constraints, adoption data, regulation | `future-scenarios`, `monitoring-list` |
| `decision-analysis` | user needs go / hold / no-go, buy, adopt, invest, learn | What should we do now? | evidence stack, alternatives, risks, constraints | `decision-matrix`, `next-actions` |
| `monitoring-design` | report needs updating over time | What should we watch? | volatile facts, leading indicators, policy / release cycles | `monitoring-list`, `recheck-plan` |
| `benchmark-analysis` | performance, model, tool, repository maturity, leaderboard claims | What does the benchmark prove and not prove? | benchmark docs, methodology, replications, caveats | `benchmark-caveats`, `comparison-table` |
| `policy-and-standard-tracking` | laws, policies, standards, certification rules, exam reforms, versioned official requirements | What is official, what is draft / trial, and what is currently enforceable? | official notices, regulatory pages, standards bodies, exam calendars, implementation timelines | `official-source-priority`, `policy-timeline`, `stakeholder-impact`, `monitoring-list` |
| `formal-status-analysis` | official force, implementation stage, or adoption status may be confused | What has legal / institutional force, what is draft, and what still needs formal adoption? | official journal, regulator notice, standards body page, consultation, political agreement, institution policy | `formal-adoption-status`, `claim-citation-map` |
| `exam-standard-analysis` | language exams, professional certifications, school admissions tests, scoring changes | How do standard, syllabus, test format, score use, and transition period differ? | official syllabus, sample questions, test calendar, score-use policy, institution requirements | `official-source-priority`, `policy-timeline`, `stakeholder-impact`, `comparison-table`, `recheck-plan` |
| `research-quality-audit` | user asks whether a completed research output was good, shallow, reliable, or worth improving | What worked, what failed, and what should change next? | original request, prior output, method stack, evidence list, user feedback | `research-retrospective` |
| `report-quality-scoring` | a completed report needs a ship / revise / rerun decision | Is this report good enough to rely on? | report output, evidence ledger, claim map, quality rubric | `report-quality-scorecard` |

## Methods To Treat As Plans, Not Claims

These can be proposed or designed, but the skill must not pretend they already happened:

- `survey-research`: can design survey or analyze existing survey data.
- `expert-interview`: can draft interview guide or synthesize provided interviews.
- `field-research`: can plan field observation, not fabricate it.
- `statistical-causal-inference`: can outline needed data and identification strategy, not infer causality without data.
- `financial-modeling`: can frame assumptions, not provide investment advice as certainty.

## Method Stack Rules

- Start with `evidence-triangulation` whenever facts are time-sensitive, disputed, or decision-relevant.
- Add `claim-citation-audit` when the output includes official status, time-sensitive facts, decision verdicts, stakeholder impact, or claims the user may need to defend.
- Add `historical-lineage` when the user asks for development history, origin, evolution, or "how it got here".
- Add `paradigm-analysis` when terms, schools, definitions, or theories are contested.
- Add `jtbd-user-choice` to competitive research when user adoption matters.
- Add `red-team-dissent` to any confident strategic or decision claim.
- Add `monitoring-design` when conclusions are volatile or updateable.
- Add `policy-and-standard-tracking` when the object has official status, transition dates, implementation stages, trial periods, or legal / institutional force.
- Add `formal-status-analysis` when official source type is not enough and procedural status changes the conclusion.
- Add `exam-standard-analysis` when the object is an exam, certification, curriculum standard, or admissions requirement.
- Use `research-quality-audit` and `report-quality-scoring` for post-run evaluation; do not rewrite the report unless the user asks.
- Prefer 2-4 methods for normal answers; 5-7 only for full deep research or parallel sprints.

## Method Stack Output

Before writing the answer, internally choose:

```text
Primary method:
Supporting methods:
Methods explicitly not used:
Why this stack fits:
Output blocks to compose:
```

When useful, show the method stack briefly in the final answer. Do not expose it if it would distract from a simple response.
