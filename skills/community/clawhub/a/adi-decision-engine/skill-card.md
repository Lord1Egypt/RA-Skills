## Description: <br>
Structured multi-criteria decision analysis for ranking options with weights, constraints, confidence, tradeoff reasoning, sensitivity analysis, and explainable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimgouso](https://clawhub.ai/user/dimgouso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to structure decision-support tasks and rank options for vendor selection, route planning, hiring shortlists, tool comparison, procurement, prioritization, and other auditable tradeoff decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used for hiring or other sensitive decisions where ranking outputs may affect people or access to opportunities. <br>
Mitigation: Use it only with lawful, job-related, user-provided criteria and require human review before acting on the ranking. <br>
Risk: A decision request with missing criteria, ambiguous directions, or weak evidence can produce misleading recommendations. <br>
Mitigation: Validate requests first, ask for missing inputs, keep assumptions explicit, and do not fabricate scores or evidence. <br>
Risk: Execution depends on an external local ADI runtime dependency. <br>
Mitigation: Install only when the local decision-support workflow is needed and the external adi dependency is trusted. <br>


## Reference(s): <br>
- [Request Schema](references/request_schema.md) <br>
- [Result Interpretation](references/result_interpretation.md) <br>
- [Policy Guide](references/policy_guide.md) <br>
- [Use Cases](references/use_cases.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dimgouso/adi-decision-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and structured JSON decision results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include the best option, rationale, ranked alternatives, confidence, constraint impact, sensitivity or stability notes, and explicit assumptions when ADI runs successfully.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
