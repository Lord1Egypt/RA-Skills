# Output Templates

Structured output templates for Conversion Rate Doctor deliverables. Use Mode A for full funnel audits and Mode B for targeted page diagnoses.

---

## Mode A — Full Funnel Audit Template

### 1. Executive Summary

Provide a 3-5 sentence summary covering:
- The overall conversion rate and how it compares to category benchmark
- The primary bottleneck stage(s) identified
- The total estimated revenue recovery opportunity
- The number of findings and recommended priority sequence

**Format:**

> **Overall Conversion Rate:** [X.X%] vs. category benchmark [X.X-X.X%]
> **Primary Bottleneck:** [Stage name] — [brief description of the core issue]
> **Revenue Recovery Opportunity:** $[range] per month across [N] findings
> **Recommended First Action:** [One-sentence description of the highest-priority fix]

### 2. Current Metrics Snapshot

Present the complete funnel in a standardized table:

| Funnel Stage | Current Rate | Category Benchmark | Status | Absolute Monthly Drop-off |
|---|---|---|---|---|
| Landing to PDP | X% | X-X% | Healthy / Warning / Critical | N visitors |
| PDP to Add-to-Cart | X% | X-X% | Healthy / Warning / Critical | N visitors |
| ATC to Cart View | X% | X-X% | Healthy / Warning / Critical | N visitors |
| Cart to Checkout Start | X% | X-X% | Healthy / Warning / Critical | N visitors |
| Checkout to Payment | X% | X-X% | Healthy / Warning / Critical | N visitors |
| Payment to Confirmation | X% | X-X% | Healthy / Warning / Critical | N visitors |

**Status definitions:**
- **Healthy** — At or above category benchmark median
- **Warning** — 0.5 to 1.0 standard deviations below median
- **Critical** — More than 1.0 standard deviation below median

Include supplementary context:
- **Traffic volume:** [sessions/month]
- **Device split:** [X% mobile / X% desktop]
- **AOV:** [$X]
- **Data period:** [date range]
- **Traffic source mix:** [organic X%, paid X%, direct X%, etc.]

### 3. Funnel Stage Analysis

For each stage flagged as Warning or Critical, provide a dedicated analysis section:

#### [Stage Name] — [Status]

**Current performance:** [Rate] vs. benchmark [Range]
**Gap magnitude:** [X percentage points below benchmark floor]
**Absolute impact:** [N visitors lost per month at this stage]

**Elements examined:**
- [Element 1]: [Assessment]
- [Element 2]: [Assessment]
- [Element 3]: [Assessment]

**Root cause summary:** [2-3 sentences describing the primary cause(s) of underperformance at this stage]

### 4. Finding Details

Number each finding sequentially. Use this format for every finding:

#### Finding [N]: [Descriptive Title]

| Attribute | Detail |
|---|---|
| **Funnel Stage** | [Stage name] |
| **Page Element** | [Specific element affected] |
| **Evidence Tier** | T1 (A/B test) / T2 (Analytics correlation) / T3 (Heuristic) |
| **Evidence Summary** | [What data supports this finding] |
| **Psychology Principle** | [Principle name] |
| **Principle Mechanism** | [How the principle applies to this specific issue] |
| **Estimated Impact** | [X-X% lift in stage conversion rate] |
| **Monthly Revenue Impact** | [$X-$X range] |
| **Implementation Effort** | Low / Medium / High |

**Diagnosis:** [Detailed description of the problem observed, why it causes friction, and what behavioral evidence supports the diagnosis.]

**Prescribed Fix:** [Specific, actionable description of what to change. Include enough detail that a designer or developer could implement without further clarification.]

**Measurement Plan:** [How to validate the fix — metric to track, expected lift, recommended test duration, minimum sample size for significance.]

### 5. Prioritized Fix List

Rank all findings in a single summary table:

| Rank | Finding | Stage | Expected Revenue Impact | Effort | Priority Score |
|---|---|---|---|---|---|
| 1 | [Title] | [Stage] | $X-$X/mo | Low/Med/High | [Score] |
| 2 | [Title] | [Stage] | $X-$X/mo | Low/Med/High | [Score] |

**Priority Score formula:** (Monthly Traffic at Stage) x (Expected Lift %) x (AOV) / (Effort Score)

### 6. Implementation Roadmap

Group fixes into execution phases:

#### Phase 1: Quick Wins (Week 1-2)
- [ ] [Fix description] — [Expected impact]
- [ ] [Fix description] — [Expected impact]

#### Phase 2: Strategic Improvements (Week 3-6)
- [ ] [Fix description] — [Expected impact]
- [ ] [Fix description] — [Expected impact]

#### Phase 3: Incremental Gains (Ongoing sprint cycles)
- [ ] [Fix description] — [Expected impact]

#### Phase 4: Long-term Investments (Next quarter)
- [ ] [Fix description] — [Expected impact]

**Testing sequence note:** [Guidance on which fixes to A/B test independently vs. which can be bundled, and recommended test duration for each phase.]

---

## Mode B — Targeted Page Diagnosis Template

### 1. Diagnosis Summary

> **Page/Stage Analyzed:** [URL or stage name]
> **Target Metric:** [metric name] — Current: [X%], Benchmark: [X-X%]
> **Gap:** [X percentage points below benchmark floor]
> **Findings:** [N issues identified], [N fixes prescribed]
> **Estimated Recovery:** [X-X% lift in target metric], [$X-$X/mo revenue impact]

### 2. Page Element Assessment

Evaluate every relevant element on the target page. Use a standardized assessment grid:

| Element | Current State | Assessment | Issue Found |
|---|---|---|---|
| [Element 1] | [Brief description] | Pass / Fail / Needs Improvement | Yes / No |
| [Element 2] | [Brief description] | Pass / Fail / Needs Improvement | Yes / No |

### 3. Findings

Use the same Finding Detail format as Mode A (Section 4 above) for each issue discovered.

### 4. Competitive Comparison (if applicable)

| Element | Your Page | Competitor A | Competitor B | Best Practice |
|---|---|---|---|---|
| [Element] | [State] | [State] | [State] | [Recommended pattern] |

### 5. Prioritized Fix List

Same format as Mode A (Section 5 above).

### 6. A/B Test Recommendations

For each prescribed fix, provide a test design:

| Fix | Control | Variant | Primary Metric | Secondary Metrics | Min Sample Size | Est. Duration |
|---|---|---|---|---|---|---|
| [Fix title] | [Current state] | [Proposed change] | [Metric] | [Metrics] | [N visitors] | [N days] |
