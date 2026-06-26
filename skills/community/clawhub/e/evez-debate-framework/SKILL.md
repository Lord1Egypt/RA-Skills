---
name: evez-debate-framework
description: Framework where multiple AI agents debate to reach better conclusions through adversarial reasoning. Use when building multi-agent systems, consensus-seeking AI, red-teaming with structured opposition, or improving LLM output quality through debate. Covers debate orchestration, judge evaluation, argument scoring, and convergence detection.
---

# Multi-Agent Debate Framework

Multiple agents debate topics to reach stronger conclusions through adversarial reasoning.

## Quick Start

```python
from debate import Debate, Agent, Judge

debate = Debate("Should we use microservices?")
debate.add_agent(Agent("pro", stance="support", model="gpt-4o"))
debate.add_agent(Agent("con", stance="oppose", model="claude-sonnet-4"))
debate.add_agent(Agent("synth", stance="synthesize", model="gemini-2.5-pro"))
debate.set_judge(Judge(criteria=["evidence", "logic", "completeness"]))

result = debate.run(rounds=3)
# Returns: winner, consensus, key_arguments, confidence
```

## How It Works

1. **Proposition**: Pro agent argues for the topic
2. **Opposition**: Con agent argues against
3. **Rebuttal**: Each agent responds to the other's points
4. **Synthesis**: Synth agent finds common ground
5. **Judgment**: Judge evaluates all arguments and declares outcome

## Debate Config

```python
Debate(
    topic="Your question",
    rounds=3,                    # Number of debate rounds
    max_words_per_turn=500,      # Limit argument length
    convergence_threshold=0.7,   # Auto-stop when consensus reached
    judge_criteria=["evidence", "logic", "novelty", "completeness"],
)
```

## Agent Stances

- `support` — Argues in favor
- `oppose` — Argues against
- `synthesize` — Finds middle ground
- `devil_advocate` — Argues weakest points to strengthen them
- `expert` — Provides domain-specific knowledge

## Judge

Evaluates arguments on configurable criteria and produces:
- Winner per round
- Overall winner
- Consensus points
- Unresolved issues
- Confidence score
