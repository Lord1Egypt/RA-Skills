---
name: devils-advocate-suite
description: "Execute structured adversarial thinking to stress-test high-stakes decisions, identify systemic risks, and prevent groupthink. Use when the user asks for a strategy review, risk assessment, pre-mortem, Amazon-style PR/FAQ review, or needs to challenge assumptions regarding a project or business model. Make sure to use this skill whenever a decision has dire consequences or shows signs of false consensus."
license: MIT
---

# Devil's Advocate Suite: Operationalizing the Institutionalized Adversary

## Work Philosophy

This skill is grounded in **Adversarial Epistemology**. It moves beyond casual contrarianism to provide a structured "override operation," forcing a "decoupling" of prior beliefs from the evaluation of evidence. Based on the research of Charlan Nemeth, this skill prioritizes **authentic dissent** over mere role-playing where possible, as authentic dissent is significantly more effective at stimulating divergent thinking and uncovering correct solutions. When role-playing is necessary, it employs specific protocols (Pre-Mortem, PR/FAQ, TRIZ) to prevent the "cognitive bolstering" of original views that often plagues assigned Devil's Advocates.

## Operational Workflow

### Phase 1: The Pre-Mortem (Prospective Hindsight)

Use this at the start of a project to increase the ability to identify future failure points by 30%.

1. **Scene Setting**: State: "Imagine it is one year in the future. The project has failed spectacularly. It is an embarrassing and devastating disaster."
2. **Independent Generation**: List all possible reasons for this failure silently for 2–5 minutes.
3. **Aggregation**: Use `python scripts/premortem_aggregator.py` to organize these into a Risk Matrix (Likelihood vs. Impact).
4. **Mitigation**: Develop specific counter-measures for high-impact/high-likelihood threats.

### Phase 2: Narrative Stress-Testing (Amazon Protocol)

Used for strategic alignment and ruthless prioritization.

1. **The PR/FAQ**: Draft a one-page Press Release (PR) for the "successful" launch and an Internal FAQ addressing the most brutal questions about TAM, P&L, and dependencies.
2. **Silent Start**: Spend 20 minutes reading the narrative in silence before any discussion. This prevents "charismatic leader" bias.
3. **The "So What" Critique**: Every technical detail must answer for its business value; every strategic goal must specify concrete actions.

### Phase 3: Dialectical Inquiry (DI)

Use for complex, ill-structured problems where a "Third Path" is needed.

1. **Subgroup Split**: Divide into "Proposal Team" and "Counter-Proposal Team."
2. **Assumption Breakdown**: The Counter-Proposal team must invent plausible counter-assumptions to every core claim of the original plan.
3. **Synthesis**: Search for a new, superior alternative that incorporates the best components of both worldviews.

### Phase 4: TRIZ Contradiction Resolution

Transform the Devil's Advocate from a "naysayer" into a "catalyst" for innovation.

1. **Identify Contradictions**: Use `python scripts/triz_solver.py` when an advocate identifies that improving one parameter (e.g., speed) worsens another (e.g., cost).
2. **Apply Principles**: Use principles like "Segmentation," "Taking Out," or "Intermediary" to solve the technical or business conflict.

## Specific Commands

- `analyze --method premortem`: Executes the 7-step failure simulation.
- `analyze --method prfaq`: Structures a strategy review around an Amazon-style narrative.
- `solve --contradiction [Param A] vs [Param B]`: Invokes the TRIZ solver.

## References

Consult `references/methodology_summary.md` for full theoretical grounding on Nemeth dissent research, Klein pre-mortem, Amazon Working Backwards, Janis groupthink prevention, and TRIZ contradiction resolution.
