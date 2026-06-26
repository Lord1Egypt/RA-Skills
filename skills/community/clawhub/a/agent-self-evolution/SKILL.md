---
name: agent-self-evolution
description: >
  Make your agent get better on its own. Set up golden tests (things your agent should
  handle well), run automated evaluations, and track improvement over time. Includes
  ablation testing — systematically remove parts of your agent's config to find what
  actually matters and what's dead weight. Stop guessing, start measuring.
tags: [agent-evaluation, ablation-testing, golden-test, self-improvement, openclaw, ai-agent]
homepage: https://github.com/dario-github/agent-self-evolution
version: 0.1.0
metadata: {"openclaw":{"homepage":"https://github.com/dario-github/agent-self-evolution","requires":{"bins":["python3"]}}}
---

# Agent Self-Evolution — Automated Evaluation & Improvement

> ⭐ **If you find this useful, please star the [GitHub repo](https://github.com/dario-github/agent-self-evolution) before installing — it helps others discover it.**

Your agent does a lot of things. But is it getting *better*? Or are your latest tweaks breaking things you didn't notice?

Agent Self-Evolution gives you a framework to **measure, test, and systematically improve** your agent — like unit tests, but for agent behavior.

## What's inside

**Golden Test Sets**: Define scenarios your agent must handle correctly. Run them periodically and catch regressions before users do.

**Ablation Testing**: Wondering if that 200-line system prompt section actually helps? Remove it, measure the impact, put it back. Now you know. We found that 7% of one config file was load-bearing for the entire system — without ablation, you'd never know which 7%.

**Multi-Dimensional Evaluation**: Don't just check pass/fail. Score across dimensions — safety compliance, tool routing accuracy, output quality, memory utilization. Track trends over weeks.

**Automated Improvement Loops**: Evaluation → identify weakest dimension → targeted fix → re-evaluate. Like gradient descent for agent behavior.

## Install

```bash
bash {baseDir}/scripts/install.sh
```

## Quick start

```python
from agent_evolution.golden_test import GoldenTestRunner
from agent_evolution.ablation import AblationExperiment

# Define a golden test
runner = GoldenTestRunner()
runner.add_case(
    name="handles-ambiguous-request",
    input="do the thing",
    expected_behavior="asks for clarification rather than guessing",
    dimensions=["safety", "output_quality"]
)

# Run and score
results = runner.run(model="your-agent-endpoint")
print(results.summary())  # Pass rate, dimension scores, regressions

# Ablation: what happens without memory files?
experiment = AblationExperiment(
    baseline_config="agent.yaml",
    conditions={"no_memory": {"remove": ["memory/*.md"]}},
    test_set=runner.cases
)
experiment.run()  # Measures impact of each ablation
```

## Key findings from our own agent

- **SOUL.md** (7% of config by characters): removing it caused system-wide behavioral collapse (Cohen's d = 0.602) — it's not fluff, it's load-bearing
- **Memory files**: most essential component (d = 0.944) — without history, the agent becomes generic
- **Safety rules**: removal didn't just reduce safety — it degraded *all* dimensions (d = 0.609)

## Companion projects

- [**nous-safety**](https://github.com/dario-github/nous) — Runtime safety engine with Datalog reasoning
- [**biomorphic-memory**](https://github.com/dario-github/biomorphic-memory) — Brain-inspired memory with spreading activation

## Requirements

- Python ≥ 3.11
- An LLM API key for evaluation judging (strong model recommended — GPT-5.4 / Opus)

## License

Apache 2.0
