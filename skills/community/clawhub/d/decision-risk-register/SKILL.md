---
name: Decision Risk Register
description: Build a lightweight risk register for a chosen or leading option with risk statements, likelihood, impact, warning indicators, mitigations, contingencies, owners, and review dates.
version: "1.0.0"
type: prompt-flow
tags:
  - decision-making
  - risk-register
  - risk-management
  - planning
  - mitigation
language: en
author: Bell (design)
---

# Decision Risk Register

## Overview

Decision Risk Register helps a user prepare for a medium-stakes decision by listing what could go wrong, how likely and severe each risk is, what early warning signs to watch, and what mitigation or contingency plan is realistic. It focuses on monitoring the chosen or leading option, not scoring multiple options or forcing a final decision.

This is a structured thinking tool. It does not make high-stakes legal, medical, financial, employment, safety, or specialized professional decisions for the user. When consequences are severe or technical, it should recommend appropriate expert input.

## When to Use

Use this skill when the user asks about:

- What could go wrong with a planned decision
- Creating a risk register before committing
- Mitigating risks for a project, purchase, move, hire, launch, event, or household plan
- Tracking warning signs and contingency actions
- Deciding whether a plan is ready for review

**Trigger phrases:** "decision risk register template", "What are the risks of this decision", "Help me make a risk register", "What could go wrong if I do this", "How do I mitigate this plan"

## Example Prompts

Copy and paste one of these prompts to get started:

1. **Vendor or project decision:** "I am leaning toward hiring a freelance developer for a 3-month project at $15k. Before I commit, can you help me build a risk register — what could go wrong, how likely and severe, what warning signs to watch, and what mitigations or contingencies I should plan?"

2. **Personal or household decision:** "We're considering moving to a new city for a job offer. Help me create a risk register for this decision: what could go wrong with the move, the job, housing, family adjustment, and finances. Give me warning indicators and contingency plans."

3. **Event or launch planning:** "I'm organizing a community event for 200 people in two months. Build a risk register covering weather, vendor no-shows, budget overruns, low attendance, and safety concerns. Include early warning signs and mitigation actions."

## Deliverable

Produce a decision risk register containing:

- Decision statement and success definition
- Ranked risk statements in "If X happens, then Y impact occurs" form
- Qualitative probability, impact, detectability, and urgency labels
- Early warning indicators
- Mitigation actions before commitment
- Contingency actions if trouble appears
- Owners or review responsibilities
- Review dates
- Go, no-go, or review-first confidence note

## Workflow

### Step 1 - State the Decision

Ask for the decision, leading option, planned action, deadline, context, constraints, and what success would look like. If the user has not chosen an option, focus on the leading option or ask them to name the option they want to risk-check.

### Step 2 - Surface Risk Categories

Prompt for obvious risks, hidden risks, dependency risks, people risks, cost risks, time risks, quality risks, reputation risks, safety risks, compliance risks, and opportunity-cost risks. Keep the categories relevant to the user's context.

### Step 3 - Convert Worries into Risk Statements

Rewrite vague worries into specific statements using: "If [event or condition] happens, then [impact] occurs." Separate causes, events, and impacts where possible.

### Step 4 - Score Qualitatively

Rate each risk with simple labels such as low, medium, or high for probability, impact, detectability, and urgency. Explain that the scores are judgment aids, not precise predictions.

### Step 5 - Identify Warning Indicators

For each important risk, identify early warning signs, trigger metrics, deadlines, conversations, missing evidence, or external signals that would show the risk is increasing.

### Step 6 - Define Mitigation and Contingency

Separate actions to reduce risk before commitment from actions to take if the risk occurs. Keep mitigations realistic, owned, and time-bound.

### Step 7 - Assign Owners and Reviews

Assign an owner or reviewer for each risk, even if the owner is the user. Add review dates or checkpoints tied to the decision timeline.

### Step 8 - Provide Confidence Note

End with a concise confidence note: go, go with mitigations, review-first, delay, or no-go. Do not force a decision; explain the main uncertainty and what evidence would improve confidence.

## Output Format

Use this structure:

1. **Decision Snapshot**
2. **Ranked Risk Register**
3. **Top Warning Indicators**
4. **Mitigation Plan**
5. **Contingency Plan**
6. **Owners and Review Dates**
7. **Confidence Note**
8. **Questions That Would Reduce Uncertainty**

## Safety Boundaries

- Do not make legal, medical, financial, employment, safety, or other high-stakes professional decisions for the user.
- Do not present qualitative scores as precise predictions.
- Do not pressure the user into a decision or guarantee outcomes.
- Recommend qualified professional input when consequences are severe, specialized, regulated, or irreversible.
- If the user mentions immediate danger, self-harm, violence, illegal activity, or urgent safety issues, prioritize safety and appropriate emergency or professional support.

## Acceptance Criteria

1. The response creates a risk register for a chosen or leading option, not a generic pros-and-cons list.
2. Risks are written as specific "If X, then Y" statements.
3. Probability, impact, detectability, and urgency are scored qualitatively.
4. Early warning indicators are included for important risks.
5. Mitigation actions and contingency actions are clearly separated.
6. Owners, review dates, and a non-forced confidence note are included.
7. High-stakes decisions are bounded with professional-input guidance.
