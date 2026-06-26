# Task Type Templates

Reference templates for common task categories. Load the relevant section before generating a TodoList.

---

## #research — Research & Analysis

Use for: competitive analysis, industry research, trend reports, user research, literature reviews.

**Standard breakdown:**
```
[ ] 1. Define research scope and key questions (avoid scope creep)
[ ] 2. Identify information sources (web search / knowledge base / documents)
[ ] 3. Gather information from each source
[ ] 4. Filter for relevance and credibility — remove duplicates
[ ] 5. Structure findings (categorize, compare, extract key points)
[ ] 6. Synthesize conclusions and insights
[ ] 7. Flag uncertain claims and recommend items for user verification
```

**Hallucination risk:** Steps 3–4. Never substitute "it is generally believed that" for actual sourced findings.

**Key confirmations:** Time range, geographic scope, desired depth (overview vs. deep dive).

---

## #content — Content Creation

Use for: blog posts, social media (LinkedIn, X, Instagram, Xiaohongshu), newsletters, video scripts, emails.

**Standard breakdown:**
```
[ ] 1. Confirm audience, platform, tone, length/duration constraints
[ ] 2. Define core message (max 3 key points)
[ ] 3. Choose content structure (narrative / tips / comparison / story-led / ...)
[ ] 4. Write first draft
[ ] 5. Platform fit check (format, hashtags, character limits, restricted terms)
[ ] 6. Hook quality check (is the title compelling? does the opening grab attention?)
```

**Key confirmations:** Target audience, brand voice constraints, whether visual/media suggestions are needed.

**Note:** For platform-specific tasks (e.g. Xiaohongshu, LinkedIn), load the corresponding platform skill before steps 4–6.

---

## #technical — Technical Design

Use for: system architecture, technology selection, API design, infrastructure planning, code structure.

**Standard breakdown:**
```
[ ] 1. Clarify functional and non-functional requirements (performance, scalability, cost)
[ ] 2. Identify constraints (existing stack, team capabilities, timeline)
[ ] 3. Generate candidate solutions (minimum 2)
[ ] 4. Evaluate trade-offs for each option
[ ] 5. Recommend a solution with clear rationale
[ ] 6. Identify technical risks and mitigation strategies
[ ] 7. Outline an implementation path (phased if applicable)
```

**Hallucination risk:** Steps 3–4. Do not invent non-existent frameworks or cite outdated benchmarks.

**Key confirmations:** Team size, budget range, deadline pressure, legacy system dependencies.

---

## #data — Data Processing & Organization

Use for: data cleaning, format conversion, report generation, information structuring, archiving.

**Standard breakdown:**
```
[ ] 1. Understand source format and target format
[ ] 2. Identify data quality issues (missing values, duplicates, anomalies)
[ ] 3. Define handling rules for each issue type
[ ] 4. Execute transformations
[ ] 5. Validate output (spot-check sample records)
[ ] 6. Deliver output with a summary of decisions and trade-offs made
```

**Key confirmations:** How to handle anomalies (drop vs. fill?), required output format.

---

## #multi-skill — Multi-Skill Pipelines

Use for: tasks requiring 2+ skills chained in sequence (e.g. research → write → publish).

**Standard breakdown:**
```
[ ] 1. Map the skill chain (which skills run in what order)
[ ] 2. Define data handoffs (what does each step receive and produce)
[ ] 3. Identify the critical bottleneck (most likely failure point)
[ ] 4. Plan fallback behavior (what happens if a step fails)
[ ] 5. Execute in sequence — validate output quality at each handoff before proceeding
```

**Key principle:** Each skill does only its own job. Do not start writing content inside a research skill, or trigger searches inside a writing skill.

**Key confirmations:** Final deliverable format, and whether the user wants to review intermediate outputs (fully automated vs. checkpoint-based).
