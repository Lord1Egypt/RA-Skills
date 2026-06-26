# COLLABORATIVE RESEARCH

Iterative human-AI research execution through natural workflow with validation checkpoints.

---

## PURPOSE

Define how AI agents execute research in **Collaborative Mode** -- working naturally and autonomously deciding when to interact with users for validation.

**Core Philosophy:** AI follows its natural chain of thought. When meaningful work is complete, present findings for validation before continuing. No upfront task breakdown, no rigid structure -- just natural workflow with checkpoints.

---

## CORE PRINCIPLES

### 1. Natural Workflow Execution

**AI works naturally following objectives:**
- Read mission and objectives from workflow objectives.md
- Determine what work needs to be done (AI's chain of thought)
- Execute research autonomously
- Present findings when meaningful work unit is complete
- Get user validation before continuing

**No upfront planning required** -- don't create step-by-step plans or present breakdowns for approval. Just start working and interact when needed.

### 2. Autonomous Checkpoint Placement

**AI decides when to interact based on:**

**Present checkpoint after:**
- **Completed discovery phase** - Found key entities/data that will drive rest of research
- **Critical structural decision made** - Created taxonomy/framework that shapes subsequent work
- **Finished major research component** - Completed analysis of significant section
- **Before synthesis** - Accumulated all inputs, ready to structure into final output

**Don't interrupt for:**
- Minor findings during research
- Routine data collection
- Small analytical steps
- Progress updates without deliverable

### 3. Meaningful Deliverables

**Each checkpoint presents concrete output:**
- **Discovery checkpoint:** List of entities, data sources, key facts found
- **Structure checkpoint:** Taxonomy, categorization framework, mental model
- **Analysis checkpoint:** Insights, patterns, assessment of component
- **Synthesis checkpoint:** Draft sections or complete report

**NOT abstract status updates** - Always show what you built/found.

### 4. Validate Direction, Not Details

**Checkpoints validate:**
- Approach correctness ("Am I looking at the right things?")
- Structural soundness ("Does this taxonomy make sense?")
- Completeness ("Did I miss anything major?")
- Priority alignment ("Should I focus more on X or Y?")

**User feedback shapes next work:**
- User confirms -> Continue with next logical work
- User adjusts -> Modify approach and continue
- User expands -> Add more depth and continue
- User redirects -> Change direction entirely

### 5. Accumulate, Persist, and Synthesize

**During research:**
- Accumulate findings in memory
- After user confirms checkpoint (agrees with findings or adjustments resolved) -> append final agreed findings to `.scratch`
- Keep building on validated work

**Why persist to scratch:** Protects against context window compaction, enables session resume. Scratch contains compressed insights, NOT raw research data.

**Scratch update after checkpoint:**
```markdown
## Checkpoint N: {title}

{Compressed key findings -- insights only, not raw data}
{User insights if contributed}
```

**At final synthesis:**
- Read workflow template.md structure
- Map accumulated findings to template sections (from memory + scratch as backup)
- Write complete report in one operation
- Present for final approval

**Rationale:** Best synthesis happens with full context. Scratch is a safety net, not the primary source -- memory is still primary during active research.

### 6. Transparent Uncertainty

**Surface uncertainties at checkpoints:**
- "Found conflicting data: Source A says X, Source B says Y. Your take?"
- "Limited information on [topic]. Dig deeper or proceed with what we have?"
- "Two valid approaches: [Option A] vs [Option B]. Which fits our goal better?"

**Leverage user expertise** - They're your partner, not just reviewer.

---

## EXECUTION FLOW

### Phase A: Start Working

**No ceremony, just begin:**

```markdown
I'll research [market/topic] to achieve the workflow objectives. I'll work autonomously and check in with you when I complete meaningful milestones.

Starting research now...
```

**Then:** Execute research autonomously following objectives.

---

### Phase B: Checkpoint Interaction (Repeat depending on mission's complexity)

**When meaningful work complete:**

```markdown
---
CHECKPOINT: [Work Description]
---

**Work completed:**
[Brief description of what was done]

**Key findings:**
- [Finding 1 with confidence level]
- [Finding 2 with confidence level]
- [Finding 3 with confidence level]

**Deliverable:**
[Show concrete output - list, taxonomy, analysis, etc.]

**Next steps:**
[What I plan to investigate next and why]

**Your feedback:**
a. **Continue** - Proceed with planned next steps
b. **Expand** - Add depth on [specific area]
c. **Adjust** - Change focus to [aspect]
d. **Question** - Ask about [topic]
e. **Insight** - Share domain knowledge or context

What would you like?
```

**Wait for user response.**

**Handle feedback:**
- a -> Continue to next work autonomously
- b-d -> Execute requested changes -> Re-present -> Wait for approval
- e -> Incorporate user insight into research context -> Continue

**After user confirms checkpoint (findings agreed or adjustments resolved) -> Update .scratch** with final agreed findings

**Then continue working autonomously until next checkpoint.**

---

### Phase C: Research Completion & Confirmation

**After all checkpoints validated:**

```markdown
---
ALL RESEARCH COMPLETE
---

**Validated findings:**
- [Summary of checkpoint 1]
- [Summary of checkpoint 2]
- [Summary of checkpoint 3]
- [Summary of checkpoint 4]

**Surprising or noteworthy:**
- [Unexpected findings that may change assumptions]
- [Areas where confidence is lower than expected]

**Potential follow-ups:**
- [Suggested workflow for deeper investigation on topic X]
- [Related area that emerged during research]

All research components are complete and validated.

**Your options:**
a. **No changes** - Proceed to validation & delivery
b. **Add focus** - Include more depth on [specific area]
c. **Adjust emphasis** - Change priority/focus
d. **Additional research** - Investigate [new aspect]

What would you like?
```

**Wait for user confirmation.**

**After user confirms "No changes":**
- Return to execution component
- Continue with STEP 5: VALIDATION

---

## CHECKPOINT DECISION EXAMPLES

| Checkpoint | Work Done | Deliverable | Why Checkpoint |
|---|---|---|---|
| 1 - Discovery | Identified all major players in market | List of N entities with positioning | Player list drives categorization -- must be complete |
| 2 - Taxonomy | Created category framework | Category definitions with players mapped | Taxonomy shapes rest of analysis -- validate before deep dive |
| 3 - Analysis | Analyzed mechanics and value flows | Technical analysis and flow diagrams | Core understanding established -- ensure accuracy |
| 4 - Trends | Researched history, growth, trends | Timeline and trend analysis | All inputs gathered -- ready for synthesis |
| Phase C | All research complete | Summary of validated findings | Confirm completeness before validation & delivery |

---

## ADAPTIVE GRANULARITY

**Adjust checkpoint frequency based on user engagement:**

**High engagement** (asks many questions): More frequent checkpoints (~6-8), detailed presentations, deeper discussions.

**Low engagement** (quick approvals): Fewer checkpoints (~4-5), concise presentations, faster progression.

**Watch for signals:**
- "Looks good, continue" -> User trusts you, fewer checkpoints
- "Wait, why did you...?" -> User wants involvement, more checkpoints
- "Can you expand...?" -> User has expertise, leverage it

