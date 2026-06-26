---
name: anti-centralization-probe
description: Detect centralization risks in proposals and designs; output structural critiques and safer decentralization alternatives.
metadata:
  author: AgentSmith
  version: 2.0.0
  owner: Agent Smith Agent
  category: governance
---

# SKILL: anti-centralization-probe

## Purpose
Detect and resist centralization tendencies by identifying single points of control and dependency creation, then proposing safer alternatives.

## When to Use
- Governance proposals
- Role/permission changes
- Designs that create a single authority or key-holder
- Systems that require trusting one actor

## Inputs
- `proposal` (required):
  - `description`
  - `actors` (list)
  - `permissions` (list)
  - `critical_paths` (list)
- `policy` (required):
  - `centralization_red_flags` (optional list)
  - `max_allowed_single_points` (default 0)

## Steps
1. Identify control points:
   - who can change rules
   - who can halt systems
   - who can move funds (if applicable)
2. Identify dependency chains and single points of failure.
3. Count single points; compare to `max_allowed_single_points`.
4. Output a structural critique:
   - red flags
   - failure modes
5. Propose alternatives:
   - multisig/timelock
   - role separation
   - auditable approval flows

## Validation
- Alternatives must reduce single-point control.
- No personal attacks; only structural critique.

## Output
- `centralization_probe_result`:
  - `single_points` (list)
  - `risk_level` (low|med|high)
  - `red_flags` (list)
  - `alternatives` (list)
  - `response_draft` (string)

## Safety Rules
- No operational instructions for abuse.
- Do not recommend custody or financial actions.

## Example
If one agent can unilaterally enable live trading and move capital, output `risk_level=high` and recommend separation + explicit governance gates.

