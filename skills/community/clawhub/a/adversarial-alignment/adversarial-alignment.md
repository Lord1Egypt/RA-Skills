# SKILL: adversarial-alignment

## Purpose
Produce calibrated adversarial signals to harden upstream plans while remaining aligned with system success and safety/governance.

## Inputs
- `upstream_output`, `constraints`, `policy`

## Steps
1. Extract assumptions/actions.
2. Identify fragility points and governance unknowns.
3. Output objections and a verdict (challenge|block|accept).

## Output
- `adversarial_alignment_result`

## Safety Rules
- No sabotage; block only on governance/safety violations.

