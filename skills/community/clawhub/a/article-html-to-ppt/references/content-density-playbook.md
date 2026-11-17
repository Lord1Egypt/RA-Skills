# Content Density Playbook — Per-Route Guidelines

## Principle

**Information density is about using the available space fully, not about cramming more data points.**
A slide with 2 bars can be visually dense if the bars are annotated, compared, and contextualized.
A slide with 10 bars is sparse if they're tiny and unlabeled.

Each route has its own audience expectations, evidence types, and optimal density profile.

## Slide Canvas Budget

The usable area per slide (after margins) is approximately:
- **Width**: 12.2 inches (13.333 − 2 × 0.55 margin)
- **Height**: 6.8 inches (7.5 − 0.35 title − 0.35 footer)
- **Total canvas**: ~83 sq inches

## Per-Element Space Budget

| Element | Typical Height | Notes |
|---|---|---|
| Title (1 line) | 0.55–0.65" | 22–26pt, one line preferred |
| Title (2 lines) | 0.75–0.90" | 20–22pt, for compound titles |
| Subtitle/lead-in | 0.40–0.50" | 10–13pt, 1–2 sentences max |
| Chart area | 4.0–5.0" | Fills remaining vertical space |
| Table area | 3.5–5.0" | Depends on row count |
| Footer | 0.24" | Source + page number |

---

## Route: strategic_decision / investor_commercial (McKinsey-Class)

Audience: C-suite, board, investors. Expect crisp, data-dense, decision-oriented slides.

### Chart Rules
- **Minimum**: 3 categories with meaningful labels
- **Optimal**: 5–8 categories — this is the McKinsey sweet spot
- **Maximum**: 10 categories (more → consider horizontal bars or split)
- **Multi-series**: 2 series ideal for comparison (e.g. "Current" vs "Target")
- **Axis labels**: Keep category labels under 15 characters
- **Data labels**: Always show values on bars

### Table Rules
- **Minimum**: 3–4 data rows with meaningful comparisons
- **Optimal**: 4–8 rows, 2–4 columns
- **Column constraint**: Narrowest column ≥ 1.2" at minimum font
- **Cell text**: Keep under 30 characters per cell

### Cards / Metrics
- 3–4 cards per row, max 2 rows (6–8 total)
- 1 metric value (large) + 1 short label (≤10 chars) per card
- Never use cards when a bar chart would show the same data more clearly

---

## Route: project_governance (PMO / Steering Committee)

Audience: Project sponsor, program manager, steering committee. Expect status-driven,
accountability-focused slides with clear RAG indicators and decision logs.

### Narrative Flow
`outcomes_and_scope` → `plan_and_dependencies` → `risks_and_decisions_needed`

### Page Type Budget (8–12 slides)
| Page | Type | Density Rule |
|---|---|---|
| Cover | Title + date + project name + sponsor | Minimal, executive-friendly |
| Executive Status | RAG summary table (3–5 workstreams) | One row per workstream, one column per RAG dimension |
| Milestone Timeline | Horizontal phase roadmap (4–8 milestones) | Each milestone: date + status + owner |
| Key Achievements | 3–5 bullet cards | Quantified: "Reduced deployment time by 40%" |
| Risk & Issues | Heat matrix (likelihood × impact, 4–8 items) | Each item: description + mitigation + owner + RAG |
| Resource Burn | Bar/column chart (monthly or quarterly, 4–8 periods) | Actual vs Planned, cumulative |
| Dependency Map | Table or process flow (3–6 dependencies) | Each: from→to, what, status, risk |
| Budget vs Actual | Waterfall or stacked bar (3–6 categories) | Variance % per category |
| Decisions Needed | Structured table (1–3 decisions) | Each: decision, options, recommendation, deadline, approver |
| Next Steps / Actions | 3–5 action cards with owner + due date | Sorted by priority |
| Closing | Summary + next review date | Clean, forward-looking |

### PMO Density Anti-Patterns
| Pattern | Problem | Fix |
|---|---|---|
| Timeline with 2 milestones | Looks like project hasn't started | Add past milestones for context |
| Risk matrix with 1 item | Wasted space | Merge into executive status slide |
| Budget chart without variance | Just reporting numbers, not analyzing | Always show % variance vs plan |
| Decision slide with no recommendation | Leaves sponsor to decide without guidance | State recommendation + rationale |
| RAG without definitions | Ambiguous | Define Red/Amber/Green thresholds on-slide |

---

## Cross-Route Anti-Patterns

| Pattern | Problem | Fix |
|---|---|---|
| 2-bar chart | Wasted space | Add annotation box, or merge slides |
| Single-series with 3 categories | Underwhelming | Add comparison series |
| 2×2 table | Reads as list, not data | Convert to metric cards or structured text |
| Empty chart area >40% | Wasted canvas | Enlarge chart, add callout, or reduce slides |
| Same chart type 5 slides in a row | Monotonous | Alternate bar/column/stacked/waterfall |

## Source Extraction Check (All Routes)

Before writing the IR, verify:
1. **Are the 3–5 most important numbers from the source document present?**
2. **Does each chart answer one clear question?** (not "here's some data")
3. **Are comparisons explicit?** (not "X is 20%" but "X is 20% vs Y's 12%")
4. **Is every data point sourced?** (source_refs on every object)
