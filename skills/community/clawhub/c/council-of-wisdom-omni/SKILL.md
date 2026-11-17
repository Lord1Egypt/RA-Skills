---
name: council-of-wisdom-omni
description: A multi-agent deliberation hub with 3 core agents and extensible extended agents. Activates on explicit request, can suggest calling user workspace skills with consent.
version: 1.4.1
tags: [agents, routing, multi-agent, council, wisdom, orchestration, decision-making, hub]
---

# Council of Wisdom Omni

A multi-agent deliberation hub with 3 core agents and extensible extended agents.

## When to Activate

### Explicit (Primary — recommended)
- `council:` prefix — always activates
- "ask the council", "consult the council", "gather the council"

### Auto-Trigger (Narrow — only for clear deliberation intent)
The council is for deliberate, multi-perspective decisions. It must NOT activate on isolated generic words such as "analyze", "compare", "think", "help me", "explain", "should I", "system", "api", "server", "right" or "concern" alone. Trigger only on intentional, decision-framed phrases:
- Decision requests: "which option should I pick", "weigh the trade-offs", "list the pros and cons", "help me decide between"
- Risk evaluation: "risk assessment", "what could go wrong", "evaluate the risks"
- Structured reasoning: "compare these options for", "trade-offs between X and Y"

When in doubt, prefer the explicit `council:` prefix and Do Not auto-activate.

### Auto-Skip
```
hello, hi, hey, thanks, thank you
what time, weather, temperature
yes, no, ok, sure
define, what is
single-word "should I" / "analyze" / "compare" without a real decision framing
```

## Architecture

```
Query → Explicit `council:`, or narrow auto-trigger
           │
           ▼ (if not skipped)
    ┌──────────────────┐
    │  CORE AGENTS    │ (always run)
    │ - Intent Decoder│
    │ - Risk Checker  │
    │ - Tone Designer │
    └──────────────────┘
           │
           ▼ (if extended triggered)
    ┌──────────────────┐
    │ EXTENDED AGENTS │ (included)
    └──────────────────┘
           │
           ▼ (only with user consent)
    ┌──────────────────┐
    │ WORKSPACE SKILLS │ (announced first)
    └──────────────────┘
           │
           ▼
    Enriched Response
```

## Core Agents (Always Run)

### Intent Decoder
What does the user actually want?

### Risk Checker
What could go wrong?

### Tone Designer
How should this feel?

## Extended Agents (Included)

| Agent | Trigger Keywords |
|-------|-----------------|
| System Designer | design an architecture, choose a stack, pick a database, evaluate the architecture |
| Complexity Assessor | weigh trade-offs, compare options, how detailed, decision depth |
| Values Guardian | ethical dilemma, moral question, values conflict, is it ethical |

## Calling Workspace Skills

The council can call skills/agents from your workspace when specialized knowledge is needed.
This is always **transparent and opt-in**:

1. Before invoking any workspace skill, the council first tells you which skill it wants to call and why.
2. For sensitive or high-impact tasks, or if the delegation looks risky, it asks for your explicit consent first.
3. You can forbid delegation at any time (for example: "don't call other skills", "stay in your own scope") and the council will not invoke them.
4. The council never routes your request silently — every downstream call is announced before it happens.

**Examples:**
- Quran question → proposes calling `quran-search-engine-mcp`, gets your OK, then calls it
- GitHub question → proposes calling `github-mcp`, gets your OK, then calls it
- Security question → proposes the penetration-tester agent, gets your OK, then invokes it

**To add workspace skills:**
1. Skills go in `workspace/skills/`
2. Agents go in `workspace/agents/`
3. The council can then suggest them and, with your consent, call them when relevant

## Adding Custom Extended Agents

Create a new `.md` file in `agents/` folder:

```markdown
# Your Agent Name

Trigger: only compound, decision-framed phrases

Your analysis...
```

## Output & Transparency

By default the council shows what it is doing: which agents it consulted and the reasoning it applied. Use the `council:` prefix to see the full per-agent analysis. The council never delegates to another workspace skill silently — it always announces the delegation and (for sensitive/high-impact work) asks your consent first.

## Simple Rules (80% of Value)

```
IF query contains: dangerous, high risk, worried about risking
THEN: Risk Checker flag = high

IF query contains: frustrated, angry, upset
THEN: Tone = empathetic
```

## SEO

**Keywords:** multi-agent, AI router, agent council, decision support, AI deliberation, extensible hub, workspace skills

**Use cases:** personal AI assistant, decision making, risk assessment
