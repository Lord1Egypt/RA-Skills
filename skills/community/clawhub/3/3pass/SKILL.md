---
name: 3pass
description: 3-pass recursive prompting (critique → refine → final answer). Use on any claim, diagnosis, plan, or analysis to stress-test it through self-critique.
argument-hint: <text or reply to analyze>
---

# 3-Pass Recursive Prompting

Run a 3-pass recursive self-critique on a given claim, diagnosis, plan, or analysis.

## Input

The user provides text to analyze, either:
- Directly as an argument: `/skill 3pass <text>`
- As a reply to a previous message
- As context from the current conversation

If no specific text is provided, apply to the most recent substantive claim or analysis in the conversation.

## Process

### Pass 1: Critique 🔍

Tear the input apart. Be brutally honest. Look for:

- **Logic errors** — Does the reasoning actually hold? Are there leaps?
- **Missing evidence** — What claims are unsupported? What wasn't checked?
- **Confirmation bias** — Did the analysis fit a narrative instead of following evidence?
- **Correlation vs causation** — Are causal claims actually proven?
- **Alternative explanations** — What else could explain the same observations?
- **Wrong assumptions** — What's being taken for granted that might be false?
- **Overstated confidence** — Where is certainty claimed without justification?

Number each critique point. Be specific about what's wrong, not vague.

### Pass 2: Refine 🛠️

For each critique point from Pass 1:

- **If testable:** Run the test. Use tools (exec, web_search, read files, etc.) to gather actual evidence.
- **If a gap:** Fill it with data, not speculation.
- **If an assumption:** State it explicitly and check if it holds.
- **If wrong:** Correct it with evidence.

This pass should involve DOING WORK, not just thinking. Run commands, check data, verify claims. The goal is to replace speculation with evidence.

### Pass 3: Final Answer 🎯

Synthesize everything into a corrected, evidence-backed conclusion:

- State what was RIGHT in the original analysis
- State what was WRONG and how it was corrected
- Present the refined conclusion with confidence levels
- Flag anything that STILL can't be verified
- Give actionable next steps

## Output Format

```
## Pass 1: Critique 🔍
[numbered critique points]

## Pass 2: Refine 🛠️
[evidence gathering and corrections - USE TOOLS HERE]

## Pass 3: Final Answer 🎯
[corrected analysis with confidence levels]
```

## Rules

- Be genuinely critical in Pass 1, not performatively critical
- Pass 2 MUST involve actual investigation (tool calls, data checks), not just rewriting
- Pass 3 should acknowledge remaining uncertainty honestly
- If the original analysis was actually correct, say so — don't manufacture false critiques
- Each pass should be clearly separated with the headers above
