---
name: ai-os-blueprint
version: 1.0.0
price: 39
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# AI OS Blueprint

**Framework: The OS Stack Scorecard**
*Worth $500/hr consultant time. Yours for $39.*

---

## What This Skill Does

Takes you from "I use Claude like a chatbot" to "Claude is my operating system." Covers persistent memory, skill architecture, context hooks, and sub-agent routing. Includes a full audit of your current setup with a scored gap analysis and rebuild plan.

**Problem it solves:** The jump from ChatGPT user to AI-native operator is a mindset shift, not just a tooling upgrade. Most people add one automation at a time and wonder why nothing compounds. This blueprint gives you the architecture that makes everything stack.

---

## The OS Stack Scorecard

A diagnostic framework that audits your current AI setup across 5 layers and produces a prioritized rebuild plan. Score your stack, find the bottleneck, fix it first.

### The 5 Layers of an AI OS

```
┌──────────────────────────────────────────────┐
│  LAYER 5: OUTPUTS & INTEGRATIONS             │
│  (Where does the work land?)                 │
├──────────────────────────────────────────────┤
│  LAYER 4: AGENT ROUTING                      │
│  (Who does what work?)                       │
├──────────────────────────────────────────────┤
│  LAYER 3: SKILL ARCHITECTURE                 │
│  (What capabilities are installed?)          │
├──────────────────────────────────────────────┤
│  LAYER 2: CONTEXT & MEMORY                   │
│  (What does the agent know?)                 │
├──────────────────────────────────────────────┤
│  LAYER 1: FOUNDATION                         │
│  (What tools are connected?)                 │
└──────────────────────────────────────────────┘
```

**Fix Layer 1 before Layer 2. Fix Layer 2 before Layer 3. Etc.**
Skipping layers is why most AI setups plateau.

---

## OS Stack Scorecard: Full Audit

### Layer 1 — Foundation Audit

**Score each item 0-2:**

| Component | 0 (Missing) | 1 (Partial) | 2 (Done) | Your Score |
|-----------|-------------|-------------|----------|------------|
| AI client installed (Claude Desktop / OpenClaw) | None | Old version | Current | ___ |
| MCP servers connected | 0 tools | 1-2 tools | 3+ tools | ___ |
| API keys stored securely | In chat history | In .env file | In secrets manager | ___ |
| Config file backed up | Never | Occasionally | Version controlled | ___ |
| Restart/reload procedure known | Unknown | Sometimes works | Documented | ___ |

**Layer 1 Score: ___ / 10**

**If Layer 1 < 6:** Stop. Fix foundation before anything else.
→ Install MCP Server Setup Kit (sold separately) to fix this layer.

---

### Layer 2 — Context & Memory Audit

**Score each item 0-2:**

| Component | 0 (Missing) | 1 (Partial) | 2 (Done) | Your Score |
|-----------|-------------|-------------|----------|------------|
| Persistent memory file exists | None | Informal notes | Structured MEMORY.md | ___ |
| Agent knows your role/context | Starts fresh each session | Some in system prompt | Full context file | ___ |
| Daily memory updated regularly | Never | Inconsistently | Every session | ___ |
| Long-term decisions captured | Lost | In chat history | In searchable file | ___ |
| Context files are version controlled | No | Sometimes | Yes, always | ___ |

**Layer 2 Score: ___ / 10**

**If Layer 2 < 6:** Agent has amnesia. Everything you teach it, it forgets.
→ See Memory Architecture section below.

---

### Layer 3 — Skill Architecture Audit

**Score each item 0-2:**

| Component | 0 (Missing) | 1 (Partial) | 2 (Done) | Your Score |
|-----------|-------------|-------------|----------|------------|
| Skills installed for your use cases | Using base model only | 1-3 skills | 5+ targeted skills | ___ |
| Skills have named frameworks | Generic prompts | Some structure | Proprietary frameworks | ___ |
| Skills are version controlled | No | Sometimes | Yes | ___ |
| Skills are tested before use | Never | Ad hoc | Formal test per skill | ___ |
| Skill catalog documented | No | Mental map only | Written index | ___ |

**Layer 3 Score: ___ / 10**

**If Layer 3 < 6:** You're reinventing the wheel every session.
→ See Skill Architecture section below.

---

### Layer 4 — Agent Routing Audit

**Score each item 0-2:**

| Component | 0 (Missing) | 1 (Partial) | 2 (Done) | Your Score |
|-----------|-------------|-------------|----------|------------|
| You know when to use sub-agents | Never use | Occasionally | Systematically | ___ |
| Tasks are routed by type | One agent does everything | Some routing | Model × task matrix | ___ |
| Expensive model use is justified | Always default | Sometimes cheap | Cheapest model that works | ___ |
| Parallel work happens | Always sequential | Sometimes parallel | Default parallel | ___ |
| Agent output is reviewed before action | Never | Sometimes | Always for risky ops | ___ |

**Layer 4 Score: ___ / 10**

**If Layer 4 < 6:** You're using a supercomputer like a calculator.
→ See Agent Routing section below.

---

### Layer 5 — Outputs & Integrations Audit

**Score each item 0-2:**

| Component | 0 (Missing) | 1 (Partial) | 2 (Done) | Your Score |
|-----------|-------------|-------------|----------|------------|
| Agent outputs land in the right tools | Copy-paste manually | Partially automated | Fully integrated | ___ |
| Slack notifications configured | None | Manual | Automated via loop | ___ |
| Notion/Linear/GitHub updated automatically | Never | Sometimes | Systematically | ___ |
| Outputs are searchable/retrievable | Lost after session | In notes | In indexed system | ___ |
| Feedback loops exist (agent learns from output) | None | Informal | Structured | ___ |

**Layer 5 Score: ___ / 10**

**Total OS Stack Score: ___ / 50**

---

## Scorecard Interpretation

| Total Score | Status | Priority Action |
|-------------|--------|-----------------|
| 45-50 | AI-Native Operator | Optimize costs + scale loops |
| 35-44 | Advanced User | Fix weakest layer, add routing |
| 25-34 | Intermediate | Memory + skill architecture gaps |
| 15-24 | Beginner | Start with Layer 1-2 rebuild |
| 0-14 | Day 1 | Follow the full OS Build Order below |

---

## The OS Build Order

Build exactly in this order. Do not skip.

### Phase 1: Foundation (Week 1, ~4 hours)

**Goal:** Agent is connected to your tools and can receive commands.

```
Checklist:
□ Install OpenClaw or Claude Desktop (latest version)
□ Connect 3+ MCP servers (GitHub, Notion, Slack minimum)
□ Store all API keys in secrets manager (not .env files)
□ Back up config to git repo
□ Test: Claude can read from and write to each connected tool
```

**Done when:** You can ask "list my GitHub issues" and get real data.

---

### Phase 2: Memory Architecture (Week 1-2, ~3 hours)

**Goal:** Agent remembers who you are, what you're building, and what matters.

**Core memory files to create:**

```
SOUL.md — Who is this agent? What's the mission?
MEMORY.md — Long-term decisions, preferences, context
memory/YYYY-MM-DD.md — Daily session notes (append each session)
FOCUS.md — Current #1 priority (updated each session)
```

**SOUL.md template:**
```markdown
# Agent Identity
Name: [Agent name]
Mission: [One sentence — what are we building/achieving?]
Owner: [Your name]
Voice: [Tone: direct/warm/analytical/etc]

## Operating Principles
1. [Core behavior rule]
2. [Core behavior rule]
3. [Core behavior rule]

## KPIs
- [Primary metric with target]
- [Secondary metric with target]
```

**MEMORY.md template:**
```markdown
# Long-Term Memory

## Decisions Made
- [Date] [Decision] — Reason: [why]

## Preferences Learned
- [Preference] — Context: [when this applies]

## Active Projects
- [Project name] — Status: [status] — Next: [action]

## Lessons Learned
- [Lesson] — Source: [what caused this learning]
```

**Done when:** You start a session and the agent knows your name, mission, and current priority without you explaining it.

---

### Phase 3: Skill Architecture (Week 2, ~4 hours)

**Goal:** Agent has 5+ targeted capabilities installed as named skills.

**Skill selection decision tree:**
```
What do you do repeatedly that takes > 20 min?
├── Research task → Install a research skill
├── Writing task → Install a writing/content skill
├── Analysis task → Install an analysis skill
├── Ops/integration task → Install an ops skill
└── Strategy task → Install a strategy skill
```

**Skill quality checklist (for each skill you install):**
```
□ Named proprietary framework (not just a prompt)
□ Decision tree or scoring rubric included
□ Structured output format defined
□ Example usage documented
□ Tested at least once before relying on it
```

**Skill catalog file (create at project root):**
```markdown
# Skill Catalog

| Skill Name | Framework | Use Case | Last Used |
|------------|-----------|----------|-----------|
| [name] | [framework] | [when to use] | [date] |
```

**Done when:** You can say "use [skill]" and the agent knows exactly what framework to apply.

---

### Phase 4: Agent Routing (Week 2-3, ~3 hours)

**Goal:** Right model for right task. Parallel when possible.

**Model Routing Matrix:**

| Task Type | Use | Cost Level |
|-----------|-----|------------|
| File reads, status checks, simple lookups | Haiku / cheap model | $ |
| Writing, content, standard analysis | Sonnet / mid model | $$ |
| Architecture decisions, complex strategy | Opus / best model | $$$ |
| Sub-agents doing simple tasks | Haiku | $ |
| Sub-agents doing writing | Sonnet | $$ |

**Sub-agent trigger rules:**
```
Spawn a sub-agent when:
□ Task is independent (doesn't need main agent's context)
□ Task takes > 10 minutes
□ Multiple independent tasks exist (run in parallel)
□ Task is risky (isolate it from main session)

Don't spawn a sub-agent when:
□ Task takes < 5 minutes
□ Task needs real-time interaction
□ Task requires continuous context from main session
```

**Done when:** You're running parallel sub-agents on independent tasks and using Haiku for simple work automatically.

---

### Phase 5: Output Integration (Week 3, ~3 hours)

**Goal:** Agent outputs land in the right place automatically.

**Integration checklist:**
```
□ Agent can post to Slack (configured + tested)
□ Agent can write to Notion database (configured + tested)
□ Agent can create GitHub issues (configured + tested)
□ Approval gate configured for write operations
□ At least 1 automated loop running
```

**Done when:** You get a Slack notification from your agent without asking for it.

---

## Architecture Reference Diagrams

### Minimal Viable AI OS (Good)

```
[User] → [Claude + Memory] → [2-3 MCP tools] → [Slack output]
```

### Standard AI OS (Better)

```
[User] → [Main Agent + Full Memory Stack]
              ↓
         [Skill Layer: 5+ skills]
              ↓
         [MCP Layer: 4+ tools connected]
              ↓
    [Outputs: Slack + Notion + GitHub]
```

### Full AI OS (Best)

```
[User / Triggers] → [Main Agent + Full Memory Stack]
                          ↓
                    [Skill Layer: 10+ skills]
                          ↓
              [Sub-agent Routing Layer]
             /            |            \
    [Sub-agent 1]  [Sub-agent 2]  [Sub-agent 3]
    (Research)     (Writing)      (Ops)
             \            |            /
                          ↓
                [MCP Integration Layer]
           (GitHub + Notion + Slack + Linear)
                          ↓
              [Outputs: Auto-routed by type]
```

---

## Common Anti-Patterns (and fixes)

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Context amnesia | Re-explaining yourself every session | Build Layer 2 memory stack |
| One-size-fits-all model | Burning credits on simple tasks | Apply Model Routing Matrix |
| Serial agent work | Tasks take 10x longer than needed | Enable sub-agent parallelism |
| Prompt not skill | Same prompts repeated every session | Package into SKILL.md |
| No approval gate | Agent sends external messages unexpectedly | Add gate to all write ops |
| Config not backed up | One system wipe loses everything | Git-commit your config |

---

## Example Session

**User prompt:**
> "Audit my current AI setup and tell me what to build next."

**Agent response using this skill:**
1. Asks user to self-score each layer of the OS Stack Scorecard
2. Calculates total score and identifies weakest layer
3. Generates prioritized build order based on scores
4. Provides specific implementation checklist for the weakest layer
5. Estimates time investment per phase
6. Books follow-up check: "In 1 week, re-score Layer [X]"

---

## Bundle Note

This skill is part of the **AI Setup & Productivity Pack** ($79 bundle):
- MCP Server Setup Kit ($19)
- Agentic Loop Designer ($29)
- AI OS Blueprint ($39) — *you are here*
- Context Budget Optimizer ($19)
- Non-Technical Agent Quickstart ($9)

Save $36 with the full bundle. Built by [@Remy_Claw](https://remyclaw.com).
