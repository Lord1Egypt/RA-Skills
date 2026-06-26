---
name: core-prism
description: CORE four-dimensional strategic lens for deep analysis of news, business theories, and strategic decisions. Use when (1) analyzing news/reports/business theories, (2) making strategic decisions requiring multi-dimensional breakdown, (3) extracting core insights from reading, (4) user explicitly asks "analyze with CORE framework".
permissions:
  filesystem:
    read:
      - USER.md  # Reads user context for personalizing [E] Execution dimension
config:
  reads:
    - USER.md  # User profile for [E] Execution dimension personalization
---

# CORE Prism (CORE四维战略透镜)

**Purpose**: Deep analysis framework using first principles to find essence, opportunities, risks, and actions.

---

## 🎯 Why CORE?

1. **MECE principle** — Mutually Exclusive, Collectively Exhaustive
2. **Forced compression** — Forces deep distillation, not summarization
3. **Ultra-high signal-to-noise** — Judge strategic value in 1 minute

---

## Four Dimensions

### [C] Core Logic (第一性本质)

**Strip away the packaging, find the essence**

In one sentence: What is the first principle (physics or economics) at play?

**Don't say**: "This disrupts the industry"  
**Do say**: "This exists by lowering X cost / improving Y efficiency"

**Examples**:
- Sora's essence = A data engine that deeply understands physical world motion
- OpenClaw's essence = An OS that lets AI proactively trigger tasks

---

### [O] Opportunity & Value (价值捕获)

**Track the flow of money, data, and power**

Where are profit pools shifting? Who controls irreplaceable leverage?

**Key questions**:
- In this gold rush: Who's mining? Who's selling shovels?
- Where should the user position themselves?

---

### [R] Risk & Contrarian (反共识与脆弱性)

**Be a contrarian to crowd emotions**

- When crowds are bullish → Point out hidden assumptions (relies on copyrighted data? regulatory risk?)
- When crowds panic → Find wrongly punished opportunities

**Key questions**:
- What's the second-order negative effect?
- Where's the biggest black swan?

---

### [E] Execution & Echo (战略映射)

**Answer "So What?"**

For the user's current situation (assets, knowledge, business):
- What action is needed TODAY?
- What should they watch out for?
- If irrelevant → mark as "cognitive reserve only"

**Context adaptation**:
- Read USER.md for user's profession, current projects, challenges
- Map insights to user's actual context
- Use second-person ("you") when addressing the user

---

## Workflow

### 1. Receive Input

**Supported inputs**:
- News article (URL or text)
- Business theory / book chapter
- Strategic decision scenario
- Event / trend description

### 2. Apply CORE Analysis

For each dimension, ask:

**[C] Core Logic**:
- What's the REAL shift? (not the headline)
- What first principle explains this?

**[O] Opportunity**:
- Who profits from this?
- Where's the value capture?
- Infrastructure vs application play?

**[R] Risk**:
- What's everyone missing? (contrarian take)
- What hidden assumptions does this rely on?
- What's the black swan?

**[E] Execution**:
- Read USER.md (if available) for context
- Map to user's profession/projects/challenges
- Provide concrete, user-specific actions

### 3. Output Structured Analysis

**Format**:
```markdown
## 【CORE Analysis】

**[C] Core Logic (本质)**:
- [First-principle insight]

**[O] Opportunity (机会)**:
- [Value flow + who wins]
- [Infrastructure vs application]

**[R] Risk (风险)**:
- [Contrarian take]
- [Hidden black swan]

**[E] Execution (行动)**:
- [User-specific action for TODAY]
- [What to watch out for]
```

---

## Configuration

**User context** (optional but recommended):
- Path: `~/.openclaw/workspace/USER.md`
- Reads: profession, interests, current challenges
- If not found: Uses generic second-person ("you")

**No other configuration needed** — CORE is a pure analysis tool.

---

## Example Usage

### Input: News Article
**User**: "Analyze this with CORE: 'AI Agent接入硬件，政府警惕'"

**Claude**:
1. Reads article content
2. Checks USER.md:
   - Profession: Product Manager at AI company
   - Challenge: Designing AI products
3. Applies CORE:
   - [C]: Control shift from human to AI (can operate hardware)
   - [O]: Infrastructure providers (who makes "AI-to-hardware bridges")
   - [R]: Regulatory window is short (3-6 months)
   - [E]: **For you**: Design "assistive" not "autonomous" AI to reduce regulatory risk
4. Outputs structured analysis

### Input: Business Theory
**User**: "Apply CORE to Clayton Christensen's Disruptive Innovation"

**Claude applies CORE**:
- [C]: Incumbents fail because they listen to top customers
- [O]: Low-end entrants who serve "non-consumers"
- [R]: Only works if tech improvement > market demand growth
- [E]: Don't just serve premium users; also explore "good enough" low-end

---

## Quality Standards

**Forbidden**:
- Surface-level "this is important" commentary
- Repeating press release language
- Generic "AI is changing everything" platitudes

**Required**:
- Sharp, one-sentence essence ([C])
- Contrarian perspective ([R])
- User-specific actionable insight ([E])
- No fluff, all substance

---

## Integration with Other Skills

**Called by**:
- `insight-radar`: Analyzes daily news with CORE
- `cognitive-forge`: Can optionally use CORE for book analysis (though F.A.C.E.T. is preferred)

**Calls**:
- None (pure analysis tool)

---

## Use Cases

| Scenario | Input | CORE Focus |
|----------|-------|------------|
| **Daily news** | AI/tech headlines | [O] Where's value flowing? [E] What to do today? |
| **Reading** | Business book chapter | [C] First principle? [R] When does this fail? |
| **Decision making** | "Should I invest in X?" | [O] Who wins? [R] What's the black swan? [E] Action? |


*Last updated: 2026-03-27*
