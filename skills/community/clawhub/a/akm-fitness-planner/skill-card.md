## Description: <br>
AKM Fitness models goals, body limits, equipment context, time budget, and recovery before producing constraint-aware workout decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirsws](https://clawhub.ai/user/sirsws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to elicit a reusable fitness profile and make training decisions that account for goals, physical constraints, equipment, time budget, recovery, and adherence risks. It is best suited when generic workout plans fail because real-world constraints materially affect the decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitness guidance could be mistaken for medical diagnosis or rehabilitation planning. <br>
Mitigation: Keep outputs within training decision support, avoid diagnosis, and route rehabilitation planning or medically constrained cases to a qualified clinician. <br>
Risk: Missing pain, injury, recovery, equipment, or time-budget inputs could produce overconfident workout recommendations. <br>
Mitigation: Require profile elicitation, list unresolved MissingInputs, reduce decision confidence, narrow the plan, or pause when critical state variables are unknown. <br>
Risk: Security evidence reports clean scan signals but does not claim a full coherence review of the artifact. <br>
Mitigation: Review the actual skill files before installation or deployment and confirm behavior matches the listed boundaries. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sirsws/akm-fitness-planner) <br>
- [Public source branch](https://github.com/sirsws/akm/tree/main/branches/fitness) <br>
- [Skill files](https://github.com/sirsws/akm/tree/main/branches/fitness/skill) <br>
- [Sample record](https://github.com/sirsws/akm/blob/main/branches/fitness/skill/SAMPLE_RECORD.md) <br>
- [Research paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231465) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style structured text with named fields such as StateJudgment, PrimaryDecision, DecisionConfidence, Plan, RiskNotes, NonNegotiables, and MissingInputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill should expose missing critical inputs, reduce confidence when state is uncertain, and keep decisions within training-planning boundaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
