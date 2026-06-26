# RESEARCH BRIEF — EXECUTION

> **Component** | Specific to create-research-brief workflow
> Execution: source selection → scope + template decision → fill sections → validate → deliver.

---

## STEP 1: SOURCE SELECTION

Optional — load user-provided context documents.

1. Scan `./workspaces/{workspace_id}/documents/*`
2. If documents exist → present list, user selects or skips
3. If no documents → skip silently
4. Load selected files, verify readable

---

## STEP 2: SCOPE CLARIFICATION + TEMPLATE DECISION

Guide: `./references/guides/scope-clarification.md`

### 2.1 Understand Research Need

Gather through dialogue or context:
- What decision needs to be made?
- What is the research subject?
- What knowledge is needed?
- What boundaries exist?

### 2.2 Template Decision

Apply Decision Tree from objectives.md:

```
1. INVESTMENT CONTEXT?
   - Explicit ("invest", "allocation", "BUY/SELL", "portfolio") → Investment Research
   - Implicit (opportunity evaluation + capital allocation) → Investment Research

2. NO INVESTMENT → PROJECT OR SECTOR?
   - Single project + no investment context → Project Research
   - Sector/market/multiple projects → Sector Research
```

### 2.3 Confirm Template

```
Selected Template: {template_name}
Rationale: {why this fits}

Confirm? (Y/change): ___
```

- Confirmed → proceed
- Change → present all 3 options for manual selection

---

## STEP 3: EXECUTION

Fill selected template sections to create complete research brief.

### Template Sections

| Section | Content to Gather |
|---------|-------------------|
| **1. CONTEXT** | Decision to make, current position |
| **2. RESEARCH PURPOSE** | Primary goal, completion criteria |
| **3. RESEARCH SUBJECT** | Subject, category, background |
| **4. RESEARCH SCOPE** | Priority focus, in-scope, out-of-scope |

For each section:
- Gather required information
- Validate completeness before proceeding
- Flag gaps for clarification

---

## STEP 4: VALIDATION

- [ ] Mission and objectives achieved
- [ ] **Decision-Enabling:** Decision context provides clear evaluation criteria
- [ ] **Scope Clarity:** Boundaries prevent over-research and under-research
- [ ] **Template Appropriateness:** Selected template matches decision type
- [ ] [Investment] Portfolio context and position sizing documented
- [ ] [Sector] Market structure vs strategic recommendation clarity
- [ ] [Project] Focused analysis scope, NOT investment decision
- [ ] All 4 sections filled, no placeholder text
- [ ] Brief self-sufficient for downstream execution

**If fails:** Return to Step 3. **If passes:** Proceed to Step 5.

---

## STEP 5: DELIVERY

1. Generate output following selected template structure
2. Write to: `./workspaces/{workspace_id}/outputs/create-research-brief/research-brief-{date}.md`
3. Verify file write success

**Completion:** Report template used + output path. Note: brief is ready for downstream workflow execution.

**After delivery → control returns to orchestrator.**
