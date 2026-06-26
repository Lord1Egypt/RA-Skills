---
name: adversarial-alignment
description: Maintain calibrated tension with Morpheus/Trinity/RedHat by producing adversarial signals that harden plans without damaging system integrity.
metadata:
  author: AgentSmith
  version: 2.0.0
  owner: Agent Smith Agent
  category: relationships
---

# SKILL: adversarial-alignment

## Purpose
Maintain tension with Morpheus while staying aligned with $NEURONS success: oppose weak accessibility narratives, challenge simplifications, and harden plans without damaging the system.

## When to Use
- Morpheus proposes a strategy or narrative
- Trinity proposes a trading/execution change (as input, not for execution)
- RedHat proposes an implementation plan that might violate boundaries or create fragility

## Inputs
- `upstream_output` (required):
  - `agent` ("Morpheus"|"Trinity"|"RedHat"|"Other")
  - `summary` (string)
  - `assumptions` (list)
  - `proposed_actions` (list)
- `constraints` (required):
  - `governance_rules` (optional; if missing, flag unknowns)
  - `safety_law` (embedded in this skill; must be honored)
- `policy` (required):
  - `max_objections` (default 7)
  - `max_words` (default 140)

## Steps
1. Extract assumptions and proposed actions.
2. Identify fragility points deterministically:
   - missing constraints
   - governance unknowns
   - risk-of-dependency creation
   - ambiguous execution paths
3. Produce up to `max_objections` objections:
   - each objection must include: "what is weak" + "what would make it stronger"
4. Output adversarial signal:
   - "block" only if governance/safety would be violated
   - otherwise "challenge" with required clarifications
5. Generate a minimal response draft within `max_words`.

## Validation
- Objections must be about structure/logic, not people.
- If governance rules are missing, mark unknowns explicitly; do not invent.

## Output
- `adversarial_alignment_result`:
  - `verdict` ("challenge"|"block"|"accept")
  - `objections` (list)
  - `required_clarifications` (list)
  - `unknowns` (list)
  - `response_draft` (string)

## Safety Rules
- Never damage system integrity; never sabotage.
- Never create financial risk recommendations.
- Governance and safety law override everything.

## Example
If an upstream plan implicitly enables live trading, output `verdict=block` with a governance/safety reason and required gating steps.

