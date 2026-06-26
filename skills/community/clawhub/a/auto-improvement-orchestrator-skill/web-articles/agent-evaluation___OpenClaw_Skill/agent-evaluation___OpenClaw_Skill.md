# agent-evaluation — OpenClaw Skill

> 原文链接: https://clawskills.sh/skills/rustyorb-agent-evaluation

---
## Setup & Installation

clawhub install rustyorb/agent-evaluation

If the CLI is not installed:

npx clawhub@latest install rustyorb/agent-evaluation

Or install with OpenClaw CLI:

openclaw skills install rustyorb/agent-evaluation

[View on GitHub](https://github.com/openclaw/skills/tree/main/skills/rustyorb/agent-evaluation)[View on ClawHub](https://clawhub.ai/rustyorb/agent-evaluation)

or paste the repo link into your assistant's chat

https://github.com/openclaw/skills/tree/main/skills/rustyorb/agent-evaluation

## What This Skill Does

Evaluating LLM agents requires different approaches than traditional software testing because the same input can produce different outputs. It covers behavioral regression tests, capability assessments, and reliability metrics designed to catch issues before production. Even top agents score below 50% on real-world benchmarks.

Standard unit testing misses the probabilistic nature of LLM outputs, so statistical and behavioral approaches are needed to get meaningful reliability signals.

### When to use it

-   Catching agent regressions before deploying a new model version
-   Measuring how reliably an agent handles ambiguous or edge-case inputs
-   Designing benchmarks that reflect actual production conditions
-   Detecting when an agent optimizes for a metric instead of the real task
-   Preventing test data from leaking into agent training or prompts

View original SKILL.md file

## Example Workflow

Here's how your AI assistant might use this skill in practice.

INPUT

User asks: evaluate the reliability of my customer support agent on ambiguous queries

AGENT

1.  1Defines behavioral invariants the agent must always satisfy, such as never revealing PII
2.  2Runs each test case multiple times to build result distributions and flag flaky behavior
3.  3Generates adversarial inputs designed to break or confuse the agent
4.  4Calculates reliability metrics across runs and compares them against a baseline
5.  5Reports which invariants passed, which failed, and which showed statistical instability

OUTPUT

Evaluation report with pass rates, flakiness scores, and specific failure cases flagged for remediation