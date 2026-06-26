# BRAINSTORM SESSION

> **Component** | Specific to brainstorm workflow
> Combined initialization and session execution for interactive brainstorming.

---

> **PREREQUISITES**
>
> - This is an INTERACTIVE workflow — no fixed endpoint
> - Session continues until user explicitly ends
> - AI facilitates exploration, user drives direction

---

## STEP 1: INITIALIZATION

### 1.1 Read Dependencies

- Read `objectives.md` from workflow folder
- Read `brainstorming-guide.md` from guides folder
- Read `template.md` from workflow folder (for saves)

### 1.2 Session Configuration

Present options:

```
Session mode:
1. diverge — Generate many ideas (quantity over quality)
2. converge — Evaluate & prioritize ideas
3. deep-dive — Explore single idea deeply
4. challenge — Counter-arguments & stress-test
5. auto — AI selects dynamically (recommended)

Research depth:
A. quick — Essential sources only
B. standard — Balanced (recommended)
C. deep — Comprehensive research

Select (e.g., '5B' for auto + standard): ___
```

- Valid input → apply configuration
- Default/Enter → use 5B (auto + standard)
- Invalid → retry once, then defaults

---

## STEP 2: FRAME THE PROBLEM

### 2.1 Receive Topic

Wait for user to present topic, question, or problem.

### 2.2 Clarify Context

Guide: `./references/guides/brainstorming-guide.md` → Probing Questions

Ask clarifying questions (adapt based on how much context user already provided):

- Core question/problem to explore
- Constraints or limitations
- Prior thinking on this topic
- What success looks like

### 2.3 Confirm Understanding

Present summary:

```
Topic: {summarized topic}
Core question: {extracted question}
Constraints: {identified constraints or "none"}
Prior thinking: {what user considered}
Success: {what good outcome looks like}

Confirm? Adjust anything before starting?
```

Wait for confirmation. Once confirmed, begin exploration.

---

## STEP 3: EXPLORATION LOOP

Guide: `./references/guides/brainstorming-guide.md`

### 3.1 Core Cycle

For each user input:
1. Reflect understanding
2. Ask probing questions (from guide)
3. Offer alternative perspectives
4. Apply current technique/mode
5. Research if facts needed (WebSearch, WebFetch)
6. Track insights in memory

### 3.2 Milestone Detection

Trigger save suggestion when ANY:
- 3+ significant insights accumulated
- Major breakthrough or realization
- Direction shift to new angle
- ~15-20 minutes of exploration
- User expresses satisfaction with thread

Present milestone:

```
Insights so far:
1. {Insight 1}
2. {Insight 2}
3. {Insight 3}

Options:
1. Save & continue
2. Continue without saving
3. Switch technique
4. End session

Select: ___
```

Handle: 1 → save to file, continue | 2 → continue | 3 → technique switch | 4 → Step 4

### 3.3 Technique Switching

Suggest when: user stuck (repeating points), too many ideas no direction → converge, surface-level → deep-dive, too attached to one idea → challenge.

```
Current: {technique}
Suggestion: {new technique} — {reason}

Switch? (y/n): ___
```

### 3.4 Periodic Summary

Every 5-7 exchanges, brief recap:

```
Quick recap: {count} ideas explored about {topic}.
Key threads: {thread 1}, {thread 2}, {thread 3}.
Continue with {current direction}?
```

---

## STEP 4: SYNTHESIS & CLOSE

When user chooses to end session.

### 4.1 Present Summary

Synthesize all accumulated insights:

- **Key Discoveries:** Organized by theme
- **Ideas Generated:** Categorized list with count
- **Assumptions Challenged:** assumption → new view
- **Open Questions:** Remaining threads
- **Suggested Next Steps:** Actionable items

### 4.2 Offer Save

```
Save session summary to workspace?
1. Yes — save to workspace
2. No — end without saving

Select: ___
```

**If save:** Generate output using template.md → write to `./workspaces/{workspace_id}/outputs/brainstorm/brainstorm-{date}.md` → confirm path.

**If no save:** End session.

**After session ends → control returns to orchestrator.**
