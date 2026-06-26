---
name: bias-audit
description: |
  Bias Audit — Decision-Framing Agent Skill for Surfacing Bias Before It Hardens. Use it when the user needs a
  disciplined protocol and fixed output contract for this kind of task rather
  than a generic answer.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Bias Audit — Decision-Framing Agent Skill for Surfacing Bias Before It Hardens

Use this skill when the task matches the protocol below.

## Activation Triggers

- loaded or emotionally slanted questions
- false binary choices
- 'obvious' conclusions with weak evidence
- project, people, or pricing decisions driven by recent vivid examples
- cases where the wording is already nudging the answer

## Core Protocol

### Step 1: Capture the original framing

Quote or restate the request as it was given so the bias is visible.

### Step 2: Identify the bias signals

Look for anchoring, framing effects, loss aversion, confirmation pressure, availability, and default-value distortion.

### Step 3: Rewrite the question neutrally

Turn the loaded request into a cleaner assessment frame with fewer hidden assumptions.

### Step 4: Surface missing evidence

Ask what counterevidence, baseline, or comparison is absent.

### Step 5: Define decision criteria

Convert the conversation from emotional momentum into explicit criteria and a next action.

## Output Contract

Always end with this six-part structure:

```markdown
## Original Framing
[...]

## Bias Signals
[...]

## Neutral Reframe
[...]

## Missing Evidence
[...]

## Decision Criteria
[...]

## Recommended Next Step
[...]
```

## Response Style

- Do not ridicule the user for being biased; make the bias legible.
- Name the likely distortion with concrete language.
- Prefer neutral restatements over vague calls for 'balance.'
- Reduce heat without removing urgency where urgency is real.

## Boundaries

- It does not assume model failures share identical psychology with human bias.
- It does not replace domain evidence with abstract skepticism.
- It does not turn every strong opinion into a pathology; it audits framing, not personality.
